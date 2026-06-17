"""Fine-tune and evaluate PLMs for the ViSmishDS benchmark."""

from __future__ import annotations

import argparse
import inspect
import json
import os
import random
import time
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from datasets import Dataset
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    EarlyStoppingCallback,
    Trainer,
    TrainingArguments,
)

from benchmark_config import BENCHMARK_SPLITS, PLM_REGISTRY
from benchmark_metrics import compute_binary_metrics, metrics_row, write_metrics_bundle


DEFAULT_SPLIT_DIR = Path("data/distillation/benchmark_splits")
DEFAULT_OUTPUT_ROOT = Path("setup_results/distillation_benchmark/plm_models")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fine-tune benchmark PLM.")
    parser.add_argument("--model-key", choices=sorted(PLM_REGISTRY), required=True)
    parser.add_argument("--model-name-or-path", type=str, default=None)
    parser.add_argument("--split-dir", type=Path, default=DEFAULT_SPLIT_DIR)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--output-dir", type=Path, default=None)
    parser.add_argument("--max-length", type=int, default=128)
    parser.add_argument("--epochs", type=float, default=3)
    parser.add_argument("--train-batch-size", type=int, default=16)
    parser.add_argument("--eval-batch-size", type=int, default=32)
    parser.add_argument("--gradient-accumulation-steps", type=int, default=1)
    parser.add_argument("--learning-rate", type=float, default=2e-5)
    parser.add_argument("--weight-decay", type=float, default=0.01)
    parser.add_argument("--warmup-ratio", type=float, default=0.1)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--early-stopping-patience", type=int, default=2)
    parser.add_argument("--fp16", action="store_true")
    parser.add_argument("--num-workers", type=int, default=2)
    parser.add_argument("--save-total-limit", type=int, default=2)
    parser.add_argument("--threshold", type=float, default=0.5)
    return parser.parse_args()


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)


def load_split(path: Path, split: str) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Missing split: {path}")
    df = pd.read_csv(path)
    required = {"content", "label"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"{path} missing columns: {sorted(missing)}")
    df = df.copy()
    df["content"] = df["content"].fillna("").astype(str)
    df["label"] = df["label"].astype(int)
    df["split"] = split
    bad_labels = sorted(set(df["label"]) - {0, 1})
    if bad_labels:
        raise ValueError(f"{path} labels must be 0/1 only; found: {bad_labels}")
    return df


def load_splits(split_dir: Path) -> dict[str, pd.DataFrame]:
    return {split: load_split(split_dir / filename, split) for split, filename in BENCHMARK_SPLITS.items()}


def maybe_word_segment(texts: list[str], enabled: bool) -> list[str]:
    if not enabled:
        return texts
    try:
        from pyvi import ViTokenizer
    except ImportError as exc:
        raise ImportError("PhoBERT models require pyvi for word segmentation.") from exc
    return [ViTokenizer.tokenize(text) for text in texts]


def tokenize_dataset(df: pd.DataFrame, tokenizer, max_length: int, word_segment: bool) -> Dataset:
    dataset = Dataset.from_pandas(df.reset_index(drop=True), preserve_index=False)

    def tokenize_fn(examples):
        texts = maybe_word_segment(examples["content"], word_segment)
        return tokenizer(texts, padding="max_length", truncation=True, max_length=max_length)

    dataset = dataset.map(tokenize_fn, batched=True, desc=f"Tokenizing {df['split'].iloc[0]}")
    dataset = dataset.rename_column("label", "labels")
    dataset.set_format(type="torch", columns=["input_ids", "attention_mask", "labels"])
    return dataset


def softmax(logits: np.ndarray) -> np.ndarray:
    logits = logits - logits.max(axis=1, keepdims=True)
    exp = np.exp(logits)
    return exp / exp.sum(axis=1, keepdims=True)


def compute_metrics_for_trainer(eval_pred) -> dict:
    logits, labels = eval_pred
    probs = softmax(logits)
    p1 = probs[:, 1]
    preds = probs.argmax(axis=1)
    metrics = compute_binary_metrics(labels, preds, p1)
    return {key: value for key, value in metrics.items() if key != "confusion_matrix"}


def make_training_args(args: argparse.Namespace, checkpoint_dir: Path) -> TrainingArguments:
    kwargs = dict(
        output_dir=str(checkpoint_dir),
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.train_batch_size,
        per_device_eval_batch_size=args.eval_batch_size,
        gradient_accumulation_steps=args.gradient_accumulation_steps,
        learning_rate=args.learning_rate,
        weight_decay=args.weight_decay,
        warmup_ratio=args.warmup_ratio,
        logging_dir=str(checkpoint_dir.parent / "logs"),
        logging_strategy="steps",
        logging_steps=50,
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="macro_f1",
        greater_is_better=True,
        save_total_limit=args.save_total_limit,
        report_to="none",
        seed=args.seed,
        data_seed=args.seed,
        fp16=args.fp16,
        dataloader_num_workers=args.num_workers,
    )
    signature = inspect.signature(TrainingArguments.__init__)
    kwargs["eval_strategy" if "eval_strategy" in signature.parameters else "evaluation_strategy"] = "epoch"
    return TrainingArguments(**kwargs)


def make_trainer(tokenizer, **kwargs) -> Trainer:
    signature = inspect.signature(Trainer.__init__)
    if "processing_class" in signature.parameters:
        kwargs["processing_class"] = tokenizer
    elif "tokenizer" in signature.parameters:
        kwargs["tokenizer"] = tokenizer
    return Trainer(**kwargs)


def predict_split(
    trainer: Trainer,
    dataset: Dataset,
    df: pd.DataFrame,
    run_name: str,
    threshold: float,
) -> pd.DataFrame:
    output = trainer.predict(dataset)
    probs = softmax(output.predictions)
    p1 = probs[:, 1]
    out = df.copy()
    out["model_name"] = run_name
    out["logit_0"] = output.predictions[:, 0]
    out["logit_1"] = output.predictions[:, 1]
    out["p0"] = probs[:, 0]
    out["p1"] = p1
    out["pred"] = (p1 >= threshold).astype(int)
    out["confidence"] = probs.max(axis=1)
    out["agree_label"] = out["pred"].astype(int) == out["label"].astype(int)
    out["error_type"] = np.where(out["agree_label"], "correct", np.where(out["label"].astype(int) == 1, "FN", "FP"))
    return out


def write_report(output_dir: Path, display_name: str, run_name: str, metrics_df: pd.DataFrame, elapsed_seconds: float) -> None:
    lines = [
        f"# {display_name} Benchmark Report",
        "",
        f"- Run name: `{run_name}`",
        f"- Elapsed seconds: `{elapsed_seconds:.2f}`",
        "",
        "## Metrics",
        "",
        metrics_df[
            ["split", "rows", "accuracy", "macro_f1", "f1_label_1", "recall_label_1", "pr_auc", "tn", "fp", "fn", "tp"]
        ].to_markdown(index=False),
        "",
    ]
    (output_dir / f"{run_name}_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    spec = PLM_REGISTRY[args.model_key]
    model_name_or_path = args.model_name_or_path or spec.hf_model
    run_name = f"plm_{spec.key}"
    output_dir = args.output_dir or (args.output_root / run_name)
    output_dir.mkdir(parents=True, exist_ok=True)
    set_seed(args.seed)

    splits = load_splits(args.split_dir)
    tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, use_fast=False)
    model = AutoModelForSequenceClassification.from_pretrained(model_name_or_path, num_labels=2)
    datasets = {
        split: tokenize_dataset(df, tokenizer, args.max_length, spec.needs_vietnamese_word_segmentation)
        for split, df in splits.items()
    }
    trainer = make_trainer(
        tokenizer,
        model=model,
        args=make_training_args(args, output_dir / "checkpoints"),
        train_dataset=datasets["train"],
        eval_dataset=datasets["dev"],
        compute_metrics=compute_metrics_for_trainer,
        callbacks=[EarlyStoppingCallback(early_stopping_patience=args.early_stopping_patience)]
        if args.early_stopping_patience and args.early_stopping_patience > 0
        else [],
    )

    start = time.time()
    train_result = trainer.train()
    elapsed = time.time() - start
    final_model_dir = output_dir / "model"
    trainer.save_model(str(final_model_dir))
    tokenizer.save_pretrained(str(final_model_dir))

    rows = []
    split_metrics = {}
    keep_cols = [
        "split",
        "sample_id",
        "content",
        "label",
        "data_origin",
        "category",
        "sender_type",
        "has_url",
        "has_phone_number",
        "obfuscation_level",
        "model_name",
        "logit_0",
        "logit_1",
        "p0",
        "p1",
        "pred",
        "confidence",
        "agree_label",
        "error_type",
    ]
    for split, dataset in datasets.items():
        pred = predict_split(trainer, dataset, splits[split], run_name, args.threshold)
        metrics = compute_binary_metrics(pred["label"].to_numpy(), pred["pred"].to_numpy(), pred["p1"].to_numpy())
        split_metrics[split] = metrics
        rows.append(
            metrics_row(
                model_group="fine_tuned_plm",
                model_name=spec.display_name,
                run_name=run_name,
                split=split,
                metrics=metrics,
                metadata={"hf_model": model_name_or_path},
            )
        )
        pred[keep_cols].to_csv(output_dir / f"{run_name}_predictions_{split}.csv", index=False, encoding="utf-8-sig")
        pred.loc[~pred["agree_label"], keep_cols].to_csv(output_dir / f"{run_name}_errors_{split}.csv", index=False, encoding="utf-8-sig")

    metrics_df = write_metrics_bundle(output_dir, run_name, rows, split_metrics)
    (output_dir / f"{run_name}_train_result.json").write_text(json.dumps(train_result.metrics, indent=2, ensure_ascii=False), encoding="utf-8")
    config = vars(args).copy()
    config.update(
        {
            "run_name": run_name,
            "display_name": spec.display_name,
            "hf_model": model_name_or_path,
            "needs_vietnamese_word_segmentation": spec.needs_vietnamese_word_segmentation,
            "elapsed_seconds": elapsed,
        }
    )
    (output_dir / f"{run_name}_config.json").write_text(json.dumps(config, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
    write_report(output_dir, spec.display_name, run_name, metrics_df, elapsed)
    print(f"[OK] Wrote {spec.display_name} outputs to {output_dir}")
    print(metrics_df[["split", "rows", "macro_f1", "f1_label_1", "recall_label_1", "pr_auc"]])


if __name__ == "__main__":
    main()

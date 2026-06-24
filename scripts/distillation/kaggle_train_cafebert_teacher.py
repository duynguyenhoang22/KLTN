"""Fine-tune CafeBERT and generate benchmark teacher outputs on Kaggle.

This is also the shared implementation used by the ViCLSR Kaggle entrypoint.
The generated CSV schema is directly compatible with:

    scripts/distillation/run_textcnn_distillation_study.py

Expected split files:

    train.csv
    dev.csv
    test.csv

Recommended Kaggle command:

    python kaggle_train_cafebert_teacher.py \
      --split-dir /kaggle/input/vismish-benchmark \
      --fp16
"""

from __future__ import annotations

import argparse
import inspect
import json
import os
import random
import shutil
import time
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from datasets import Dataset
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    EarlyStoppingCallback,
    Trainer,
    TrainingArguments,
)


@dataclass(frozen=True)
class ModelDefaults:
    model_name: str
    teacher_name: str
    output_name: str
    train_batch_size: int
    eval_batch_size: int
    gradient_accumulation_steps: int


CAFE_BERT_DEFAULTS = ModelDefaults(
    model_name="uitnlp/CafeBERT",
    teacher_name="CafeBERT",
    output_name="cafebert_teacher",
    train_batch_size=16,
    eval_batch_size=32,
    gradient_accumulation_steps=1,
)

SPLIT_FILES = {
    "train": "train.csv",
    "dev": "dev.csv",
    "test": "test.csv",
}


def build_parser(defaults: ModelDefaults) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=f"Fine-tune {defaults.teacher_name} and generate teacher outputs."
    )
    parser.add_argument("--split-dir", type=Path, default=None)
    parser.add_argument("--train-csv", type=Path, default=None)
    parser.add_argument("--dev-csv", type=Path, default=None)
    parser.add_argument("--test-csv", type=Path, default=None)
    parser.add_argument("--input-root", type=Path, default=Path("/kaggle/input"))
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("/kaggle/working") / defaults.output_name,
    )
    parser.add_argument("--model-name", default=defaults.model_name)
    parser.add_argument("--teacher-name", default=defaults.teacher_name)
    parser.add_argument("--max-length", type=int, default=128)
    parser.add_argument("--epochs", type=float, default=3.0)
    parser.add_argument(
        "--train-batch-size",
        type=int,
        default=defaults.train_batch_size,
    )
    parser.add_argument(
        "--eval-batch-size",
        type=int,
        default=defaults.eval_batch_size,
    )
    parser.add_argument(
        "--gradient-accumulation-steps",
        type=int,
        default=defaults.gradient_accumulation_steps,
    )
    parser.add_argument("--learning-rate", type=float, default=2e-5)
    parser.add_argument("--weight-decay", type=float, default=0.01)
    parser.add_argument("--warmup-ratio", type=float, default=0.1)
    parser.add_argument("--early-stopping-patience", type=int, default=2)
    parser.add_argument("--save-total-limit", type=int, default=2)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--temperature", type=float, default=2.0)
    parser.add_argument("--num-workers", type=int, default=2)
    parser.add_argument("--fp16", action="store_true")
    parser.add_argument("--bf16", action="store_true")
    parser.add_argument(
        "--trust-remote-code",
        action="store_true",
        help="Enable only if the selected Hugging Face model requires it.",
    )
    parser.add_argument(
        "--no-zip",
        action="store_true",
        help="Do not create a downloadable ZIP bundle in /kaggle/working.",
    )
    parser.add_argument(
        "--keep-checkpoints",
        action="store_true",
        help="Keep epoch checkpoints. By default they are removed after saving the best model.",
    )
    return parser


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)


def find_unique_file(input_root: Path, filename: str) -> Path:
    matches = sorted(input_root.rglob(filename))
    if not matches:
        raise FileNotFoundError(
            f"Cannot find `{filename}` under {input_root}. Pass --split-dir or "
            "the explicit --train-csv/--dev-csv/--test-csv arguments."
        )
    if len(matches) > 1:
        rendered = "\n".join(f"  - {path}" for path in matches)
        raise RuntimeError(
            f"Found multiple `{filename}` files. Refusing to guess:\n{rendered}\n"
            "Pass explicit CSV paths."
        )
    return matches[0]


def resolve_split_paths(args: argparse.Namespace) -> dict[str, Path]:
    explicit = {
        "train": args.train_csv,
        "dev": args.dev_csv,
        "test": args.test_csv,
    }
    paths: dict[str, Path] = {}
    for split, filename in SPLIT_FILES.items():
        if explicit[split] is not None:
            path = explicit[split]
        elif args.split_dir is not None:
            path = args.split_dir / filename
        else:
            path = find_unique_file(args.input_root, filename)
        if not path.exists():
            raise FileNotFoundError(f"Missing {split} split: {path}")
        paths[split] = path
    return paths


def load_split(path: Path, split: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    required = {"sample_id", "content", "label"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"{path} missing required columns: {sorted(missing)}")
    df = df.copy()
    df["sample_id"] = df["sample_id"].astype(str)
    df["content"] = df["content"].fillna("").astype(str)
    df["label"] = df["label"].astype(int)
    if not df["sample_id"].is_unique:
        raise ValueError(f"{path} contains duplicate sample_id values.")
    bad_labels = sorted(set(df["label"]) - {0, 1})
    if bad_labels:
        raise ValueError(f"{path} labels must be 0/1; found {bad_labels}")
    if df["content"].str.strip().eq("").any():
        raise ValueError(f"{path} contains empty content rows.")
    df["split"] = split
    return df


def tokenize_dataset(
    df: pd.DataFrame,
    tokenizer,
    max_length: int,
) -> Dataset:
    dataset = Dataset.from_pandas(df.reset_index(drop=True), preserve_index=False)

    def tokenize_fn(examples):
        return tokenizer(
            examples["content"],
            padding="max_length",
            truncation=True,
            max_length=max_length,
        )

    dataset = dataset.map(tokenize_fn, batched=True, desc=f"Tokenizing {df['split'].iloc[0]}")
    dataset = dataset.rename_column("label", "labels")
    dataset.set_format(type="torch", columns=["input_ids", "attention_mask", "labels"])
    return dataset


def softmax(logits: np.ndarray, temperature: float = 1.0) -> np.ndarray:
    scaled = logits / temperature
    scaled -= scaled.max(axis=1, keepdims=True)
    exp = np.exp(scaled)
    return exp / exp.sum(axis=1, keepdims=True)


def metric_values(labels: np.ndarray, preds: np.ndarray, p1: np.ndarray) -> dict:
    metrics = {
        "rows": int(len(labels)),
        "accuracy": accuracy_score(labels, preds),
        "macro_f1": f1_score(labels, preds, average="macro", zero_division=0),
        "weighted_f1": f1_score(labels, preds, average="weighted", zero_division=0),
        "precision_label_1": precision_score(labels, preds, pos_label=1, zero_division=0),
        "recall_label_1": recall_score(labels, preds, pos_label=1, zero_division=0),
        "f1_label_1": f1_score(labels, preds, pos_label=1, zero_division=0),
        "precision_label_0": precision_score(labels, preds, pos_label=0, zero_division=0),
        "recall_label_0": recall_score(labels, preds, pos_label=0, zero_division=0),
        "f1_label_0": f1_score(labels, preds, pos_label=0, zero_division=0),
        "confusion_matrix": confusion_matrix(labels, preds, labels=[0, 1]).tolist(),
    }
    if len(np.unique(labels)) == 2:
        metrics["roc_auc"] = roc_auc_score(labels, p1)
        metrics["pr_auc"] = average_precision_score(labels, p1)
    else:
        metrics["roc_auc"] = float("nan")
        metrics["pr_auc"] = float("nan")
    return metrics


def trainer_metrics(eval_pred) -> dict:
    logits, labels = eval_pred
    probs = softmax(logits)
    values = metric_values(labels, probs.argmax(axis=1), probs[:, 1])
    return {key: value for key, value in values.items() if key != "confusion_matrix"}


def training_args(args: argparse.Namespace) -> TrainingArguments:
    kwargs = dict(
        output_dir=str(args.output_dir / "checkpoints"),
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.train_batch_size,
        per_device_eval_batch_size=args.eval_batch_size,
        gradient_accumulation_steps=args.gradient_accumulation_steps,
        learning_rate=args.learning_rate,
        weight_decay=args.weight_decay,
        warmup_ratio=args.warmup_ratio,
        logging_dir=str(args.output_dir / "logs"),
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
        bf16=args.bf16,
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


def distill_weight(row: pd.Series) -> float:
    if bool(row["teacher_agree_label"]) and float(row["teacher_confidence"]) >= 0.8:
        return 1.0
    if bool(row["teacher_agree_label"]):
        return 0.7
    return 0.3


def add_teacher_columns(
    df: pd.DataFrame,
    logits: np.ndarray,
    args: argparse.Namespace,
    model_dir: Path,
) -> pd.DataFrame:
    probs_t1 = softmax(logits, temperature=1.0)
    probs_t = softmax(logits, temperature=args.temperature)
    out = df.copy()
    out["teacher_model"] = args.teacher_name
    out["teacher_version"] = str(model_dir)
    out["teacher_logit_0"] = logits[:, 0]
    out["teacher_logit_1"] = logits[:, 1]
    out["teacher_p0_t1"] = probs_t1[:, 0]
    out["teacher_p1_t1"] = probs_t1[:, 1]
    out[f"teacher_p0_t{args.temperature:g}"] = probs_t[:, 0]
    out[f"teacher_p1_t{args.temperature:g}"] = probs_t[:, 1]
    out["teacher_temperature"] = args.temperature
    out["teacher_pred"] = probs_t1.argmax(axis=1)
    out["teacher_confidence"] = probs_t1.max(axis=1)
    out["teacher_agree_label"] = out["teacher_pred"].astype(int) == out["label"].astype(int)
    out["distill_weight"] = out.apply(distill_weight, axis=1)
    return out


def metrics_row(split: str, metrics: dict) -> dict:
    cm = metrics["confusion_matrix"]
    return {
        "split": split,
        **{key: value for key, value in metrics.items() if key != "confusion_matrix"},
        "tn": cm[0][0],
        "fp": cm[0][1],
        "fn": cm[1][0],
        "tp": cm[1][1],
    }


def write_report(
    args: argparse.Namespace,
    paths: dict[str, Path],
    rows: list[dict],
    elapsed_seconds: float,
    archive_path: Path | None,
) -> None:
    display = pd.DataFrame(rows)[
        [
            "split",
            "rows",
            "macro_f1",
            "f1_label_1",
            "recall_label_1",
            "precision_label_1",
            "pr_auc",
            "tn",
            "fp",
            "fn",
            "tp",
        ]
    ]
    lines = [
        f"# {args.teacher_name} Teacher Report",
        "",
        "## Configuration",
        "",
        f"- Hugging Face model: `{args.model_name}`",
        f"- Seed: `{args.seed}`",
        f"- Epochs: `{args.epochs}`",
        f"- Max length: `{args.max_length}`",
        f"- Train batch size: `{args.train_batch_size}`",
        f"- Eval batch size: `{args.eval_batch_size}`",
        f"- Gradient accumulation: `{args.gradient_accumulation_steps}`",
        f"- Effective train batch size: `{args.train_batch_size * args.gradient_accumulation_steps}`",
        f"- Temperature: `{args.temperature}`",
        f"- FP16: `{args.fp16}`",
        f"- BF16: `{args.bf16}`",
        f"- Elapsed seconds: `{elapsed_seconds:.2f}`",
        "",
        "## Inputs",
        "",
        pd.DataFrame(
            [{"split": split, "path": str(path)} for split, path in paths.items()]
        ).to_markdown(index=False),
        "",
        "## Metrics",
        "",
        display.to_markdown(index=False),
        "",
        "## Artifact",
        "",
        f"- Model: `{args.output_dir / 'model'}`",
        f"- Teacher outputs: `{args.output_dir / 'teacher_outputs'}`",
        f"- ZIP: `{archive_path}`" if archive_path else "- ZIP generation disabled.",
        "",
    ]
    (args.output_dir / "teacher_report.md").write_text("\n".join(lines), encoding="utf-8")


def run_teacher_pipeline(defaults: ModelDefaults, argv: list[str] | None = None) -> None:
    args = build_parser(defaults).parse_args(argv)
    if args.fp16 and args.bf16:
        raise ValueError("Choose only one of --fp16 or --bf16.")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    set_seed(args.seed)
    paths = resolve_split_paths(args)
    splits = {split: load_split(path, split) for split, path in paths.items()}

    print("[INFO] Configuration")
    print(json.dumps({key: str(value) for key, value in vars(args).items()}, indent=2))
    print(f"[INFO] CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"[INFO] GPU: {torch.cuda.get_device_name(0)}")
    for split, df in splits.items():
        print(f"[INFO] {split}: {len(df):,} rows from {paths[split]}")

    tokenizer = AutoTokenizer.from_pretrained(
        args.model_name,
        use_fast=False,
        trust_remote_code=args.trust_remote_code,
    )
    model = AutoModelForSequenceClassification.from_pretrained(
        args.model_name,
        num_labels=2,
        trust_remote_code=args.trust_remote_code,
    )
    datasets = {
        split: tokenize_dataset(df, tokenizer, args.max_length)
        for split, df in splits.items()
    }
    callbacks = (
        [EarlyStoppingCallback(early_stopping_patience=args.early_stopping_patience)]
        if args.early_stopping_patience > 0
        else []
    )
    trainer = make_trainer(
        tokenizer,
        model=model,
        args=training_args(args),
        train_dataset=datasets["train"],
        eval_dataset=datasets["dev"],
        compute_metrics=trainer_metrics,
        callbacks=callbacks,
    )

    start = time.time()
    train_result = trainer.train()
    elapsed_seconds = time.time() - start
    model_dir = args.output_dir / "model"
    trainer.save_model(str(model_dir))
    tokenizer.save_pretrained(str(model_dir))
    if not args.keep_checkpoints:
        shutil.rmtree(args.output_dir / "checkpoints", ignore_errors=True)

    output_dir = args.output_dir / "teacher_outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    metrics_by_split = {}
    for split in SPLIT_FILES:
        prediction = trainer.predict(datasets[split])
        out = add_teacher_columns(
            splits[split],
            prediction.predictions,
            args,
            model_dir,
        )
        output_path = output_dir / f"{split}_teacher.csv"
        out.to_csv(output_path, index=False, encoding="utf-8-sig")
        metrics = metric_values(
            out["label"].to_numpy(),
            out["teacher_pred"].to_numpy(),
            out["teacher_p1_t1"].to_numpy(),
        )
        metrics_by_split[split] = metrics
        rows.append(metrics_row(split, metrics))
        print(
            f"[OK] {split}: macro_f1={metrics['macro_f1']:.4f}, "
            f"f1_label_1={metrics['f1_label_1']:.4f}, "
            f"recall_label_1={metrics['recall_label_1']:.4f}"
        )

    pd.DataFrame(rows).to_csv(
        args.output_dir / "teacher_metrics_by_split.csv",
        index=False,
    )
    (args.output_dir / "teacher_metrics.json").write_text(
        json.dumps(metrics_by_split, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    (args.output_dir / "train_metrics.json").write_text(
        json.dumps(train_result.metrics, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    config = {
        **{key: str(value) if isinstance(value, Path) else value for key, value in vars(args).items()},
        "defaults": asdict(defaults),
        "elapsed_seconds": elapsed_seconds,
        "cuda_available": torch.cuda.is_available(),
        "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
    }
    (args.output_dir / "teacher_config.json").write_text(
        json.dumps(config, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    archive_path = None
    if not args.no_zip:
        archive_base = Path("/kaggle/working") / f"{args.output_dir.name}_artifacts"
        archive_path = Path(
            shutil.make_archive(
                str(archive_base),
                "zip",
                root_dir=args.output_dir.parent,
                base_dir=args.output_dir.name,
            )
        )
    write_report(args, paths, rows, elapsed_seconds, archive_path)
    if archive_path is not None:
        # Regenerate once so the report itself is also included in the archive.
        archive_path.unlink(missing_ok=True)
        archive_path = Path(
            shutil.make_archive(
                str(archive_path.with_suffix("")),
                "zip",
                root_dir=args.output_dir.parent,
                base_dir=args.output_dir.name,
            )
        )

    print(f"[OK] Model: {model_dir}")
    print(f"[OK] Teacher outputs: {output_dir}")
    if archive_path is not None:
        print(f"[OK] Downloadable ZIP: {archive_path}")


if __name__ == "__main__":
    run_teacher_pipeline(CAFE_BERT_DEFAULTS)

"""Generate teacher logits/probabilities for all distillation splits on Kaggle.

Expected Kaggle usage after fine-tuning:
   python kaggle_generate_teacher_outputs.py \
     --model-dir /kaggle/working/distillation_teacher_phobert_base/model

The script auto-finds split CSV files under /kaggle/input by default:
train.csv, val.csv, test_real.csv, test_mixed.csv, test_challenge.csv.
"""

from __future__ import annotations

import argparse
import inspect
import json
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from datasets import Dataset
from pyvi import ViTokenizer
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from transformers import AutoModelForSequenceClassification, AutoTokenizer, Trainer, TrainingArguments


DEFAULT_INPUT_ROOT = Path("/kaggle/input")
DEFAULT_MODEL_DIR = Path("/kaggle/working/distillation_teacher_phobert_base/model")
DEFAULT_OUTPUT_DIR = Path("/kaggle/working/distillation_teacher_outputs")
SPLIT_NAMES = ["train", "val", "test_real", "test_mixed", "test_challenge"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate PhoBERT teacher outputs for offline soft-label distillation."
    )
    parser.add_argument("--model-dir", type=Path, default=DEFAULT_MODEL_DIR)
    parser.add_argument("--input-root", type=Path, default=DEFAULT_INPUT_ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--max-length", type=int, default=128)
    parser.add_argument("--eval-batch-size", type=int, default=64)
    parser.add_argument("--num-workers", type=int, default=2)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--temperature", type=float, default=2.0)
    parser.add_argument("--fp16", action="store_true")
    for split in SPLIT_NAMES:
        parser.add_argument(f"--{split}-csv", type=Path, default=None)
    return parser.parse_args()


def find_input_file(input_root: Path, filename: str) -> Path:
    matches = sorted(input_root.rglob(filename))
    if not matches:
        raise FileNotFoundError(f"Cannot find {filename} under {input_root}.")
    if len(matches) > 1:
        print(f"[WARN] Found multiple {filename}; using the first one:")
        for match in matches:
            print(f"  - {match}")
    return matches[0]


def split_paths(args: argparse.Namespace) -> dict[str, Path]:
    paths = {}
    for split in SPLIT_NAMES:
        explicit = getattr(args, f"{split}_csv")
        paths[split] = explicit or find_input_file(args.input_root, f"{split}.csv")
    return paths


def load_split(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    required = {"content", "label"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"{path} is missing required columns: {sorted(missing)}")
    df = df.copy()
    df["content"] = df["content"].astype(str).fillna("")
    df["label"] = df["label"].astype(int)
    labels = set(df["label"].unique().tolist())
    if labels - {0, 1}:
        raise ValueError(f"{path} labels must be 0/1 only; found {sorted(labels)}")
    return df


def softmax(logits: np.ndarray, temperature: float = 1.0) -> np.ndarray:
    scaled = logits / temperature
    scaled = scaled - scaled.max(axis=1, keepdims=True)
    exp = np.exp(scaled)
    return exp / exp.sum(axis=1, keepdims=True)


def tokenize_dataset(df: pd.DataFrame, tokenizer, max_length: int) -> Dataset:
    dataset = Dataset.from_pandas(df.reset_index(drop=True), preserve_index=False)

    def tokenize_fn(examples):
        segmented = [ViTokenizer.tokenize(text) for text in examples["content"]]
        return tokenizer(
            segmented,
            padding="max_length",
            truncation=True,
            max_length=max_length,
        )

    dataset = dataset.map(tokenize_fn, batched=True, desc="Tokenizing")
    if "label" in dataset.column_names:
        dataset = dataset.rename_column("label", "labels")
    dataset.set_format(type="torch", columns=["input_ids", "attention_mask", "labels"])
    return dataset


def make_training_args(args: argparse.Namespace) -> TrainingArguments:
    kwargs = dict(
        output_dir=str(args.output_dir / "_tmp_trainer"),
        per_device_eval_batch_size=args.eval_batch_size,
        report_to="none",
        seed=args.seed,
        data_seed=args.seed,
        fp16=args.fp16,
        dataloader_num_workers=args.num_workers,
    )
    signature = inspect.signature(TrainingArguments.__init__)
    if "eval_strategy" in signature.parameters:
        kwargs["eval_strategy"] = "no"
    else:
        kwargs["evaluation_strategy"] = "no"
    return TrainingArguments(**kwargs)


def make_trainer(model, tokenizer, args: argparse.Namespace) -> Trainer:
    kwargs = {
        "model": model,
        "args": make_training_args(args),
    }
    signature = inspect.signature(Trainer.__init__)
    if "processing_class" in signature.parameters:
        kwargs["processing_class"] = tokenizer
    elif "tokenizer" in signature.parameters:
        kwargs["tokenizer"] = tokenizer
    return Trainer(**kwargs)


def distill_weight(row: pd.Series) -> float:
    agree = bool(row["teacher_agree_label"])
    confidence = float(row["teacher_confidence"])
    if agree and confidence >= 0.8:
        return 1.0
    if agree:
        return 0.7
    return 0.3


def add_teacher_columns(
    df: pd.DataFrame,
    logits: np.ndarray,
    model_dir: Path,
    temperature: float,
) -> pd.DataFrame:
    probs_t1 = softmax(logits, temperature=1.0)
    probs_t = softmax(logits, temperature=temperature)
    preds = probs_t1.argmax(axis=1)

    out = df.copy()
    out["teacher_model"] = "vinai/phobert-base"
    out["teacher_version"] = str(model_dir)
    out["teacher_logit_0"] = logits[:, 0]
    out["teacher_logit_1"] = logits[:, 1]
    out["teacher_p0_t1"] = probs_t1[:, 0]
    out["teacher_p1_t1"] = probs_t1[:, 1]
    out[f"teacher_p0_t{temperature:g}"] = probs_t[:, 0]
    out[f"teacher_p1_t{temperature:g}"] = probs_t[:, 1]
    out["teacher_temperature"] = temperature
    out["teacher_pred"] = preds
    out["teacher_confidence"] = probs_t1.max(axis=1)
    out["teacher_agree_label"] = out["teacher_pred"].astype(int) == out["label"].astype(int)
    out["distill_weight"] = out.apply(distill_weight, axis=1)
    return out


def compute_metrics(df: pd.DataFrame) -> dict:
    labels = df["label"].to_numpy()
    preds = df["teacher_pred"].to_numpy()
    p1 = df["teacher_p1_t1"].to_numpy()

    metrics = {
        "rows": int(len(df)),
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
        "teacher_agree_rate": float(df["teacher_agree_label"].mean()),
        "mean_confidence": float(df["teacher_confidence"].mean()),
    }
    if len(np.unique(labels)) == 2:
        metrics["roc_auc"] = roc_auc_score(labels, p1)
        metrics["pr_auc"] = average_precision_score(labels, p1)
    return metrics


def table_value_counts(df: pd.DataFrame, column: str) -> str:
    if column not in df.columns:
        return f"_Column `{column}` not found._"
    counts = df[column].value_counts(dropna=False).rename_axis(column).reset_index(name="count")
    counts["percent"] = (counts["count"] / len(df) * 100).round(2)
    return counts.to_markdown(index=False)


def write_report(output_dir: Path, all_metrics: dict[str, dict], output_paths: dict[str, Path]) -> None:
    rows = []
    for split, metrics in all_metrics.items():
        rows.append(
            {
                "split": split,
                "rows": metrics["rows"],
                "accuracy": round(metrics["accuracy"], 4),
                "macro_f1": round(metrics["macro_f1"], 4),
                "f1_label_1": round(metrics["f1_label_1"], 4),
                "recall_label_1": round(metrics["recall_label_1"], 4),
                "precision_label_1": round(metrics["precision_label_1"], 4),
                "teacher_agree_rate": round(metrics["teacher_agree_rate"], 4),
                "mean_confidence": round(metrics["mean_confidence"], 4),
            }
        )

    lines = [
        "# Teacher Output Generation Report",
        "",
        "## Output Files",
        "",
        pd.DataFrame(
            [{"split": split, "path": str(path)} for split, path in output_paths.items()]
        ).to_markdown(index=False),
        "",
        "## Metrics Summary",
        "",
        pd.DataFrame(rows).to_markdown(index=False),
        "",
        "## Confusion Matrices",
        "",
    ]

    for split, metrics in all_metrics.items():
        cm = pd.DataFrame(
            metrics["confusion_matrix"],
            index=["true_0", "true_1"],
            columns=["pred_0", "pred_1"],
        )
        lines.extend([f"### {split}", "", cm.to_markdown(), ""])

    (output_dir / "teacher_outputs_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    print("[INFO] Configuration")
    print(json.dumps({key: str(value) for key, value in vars(args).items()}, indent=2, ensure_ascii=False))
    print(f"[INFO] cuda available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"[INFO] gpu: {torch.cuda.get_device_name(0)}")

    paths = split_paths(args)
    for split, path in paths.items():
        print(f"[INFO] {split}: {path}")

    tokenizer = AutoTokenizer.from_pretrained(args.model_dir, use_fast=False)
    model = AutoModelForSequenceClassification.from_pretrained(args.model_dir)
    trainer = make_trainer(model, tokenizer, args)

    all_metrics = {}
    output_paths = {}
    for split, path in paths.items():
        print(f"\n[RUN] Generating teacher outputs for {split}")
        df = load_split(path)
        dataset = tokenize_dataset(df, tokenizer, args.max_length)
        predictions = trainer.predict(dataset)
        out = add_teacher_columns(df, predictions.predictions, args.model_dir, args.temperature)

        output_path = args.output_dir / f"{split}_teacher.csv"
        out.to_csv(output_path, index=False, encoding="utf-8-sig")
        metrics = compute_metrics(out)
        all_metrics[split] = metrics
        output_paths[split] = output_path

        print(f"[OK] {split}: wrote {output_path}")
        print(json.dumps(metrics, indent=2, ensure_ascii=False))

    with (args.output_dir / "teacher_outputs_metrics.json").open("w", encoding="utf-8") as f:
        json.dump(all_metrics, f, indent=2, ensure_ascii=False)
    write_report(args.output_dir, all_metrics, output_paths)
    print(f"\n[OK] Wrote metrics: {args.output_dir / 'teacher_outputs_metrics.json'}")
    print(f"[OK] Wrote report : {args.output_dir / 'teacher_outputs_report.md'}")


if __name__ == "__main__":
    main()

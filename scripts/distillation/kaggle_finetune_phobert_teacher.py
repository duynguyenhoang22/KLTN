"""Fine-tune a PhoBERT-base teacher for ViSmishDS distillation on Kaggle.

Expected Kaggle usage:
1. Upload/add a Kaggle Dataset containing the split files:
   - train.csv
   - val.csv
2. Run:
   python kaggle_finetune_phobert_teacher.py

Optional explicit paths:
   python kaggle_finetune_phobert_teacher.py \
     --train-csv /kaggle/input/your-dataset/train.csv \
     --val-csv /kaggle/input/your-dataset/val.csv

Outputs are written under /kaggle/working by default.
"""

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
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    EarlyStoppingCallback,
    Trainer,
    TrainingArguments,
)


DEFAULT_MODEL_NAME = "vinai/phobert-base"
DEFAULT_INPUT_ROOT = Path("/kaggle/input")
DEFAULT_OUTPUT_DIR = Path("/kaggle/working/distillation_teacher_phobert_base")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fine-tune vinai/phobert-base as a teacher for offline soft-label distillation."
    )
    parser.add_argument("--train-csv", type=Path, default=None)
    parser.add_argument("--val-csv", type=Path, default=None)
    parser.add_argument("--input-root", type=Path, default=DEFAULT_INPUT_ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--model-name", type=str, default=DEFAULT_MODEL_NAME)
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
    parser.add_argument("--fp16", action="store_true", help="Enable fp16 training when Kaggle GPU supports it.")
    parser.add_argument("--num-workers", type=int, default=2)
    parser.add_argument("--save-total-limit", type=int, default=2)
    return parser.parse_args()


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)


def find_split_file(input_root: Path, filename: str) -> Path:
    matches = sorted(input_root.rglob(filename))
    if not matches:
        raise FileNotFoundError(
            f"Cannot find {filename} under {input_root}. "
            "Add a Kaggle Dataset containing train.csv and val.csv, "
            "or pass --train-csv/--val-csv explicitly."
        )
    if len(matches) > 1:
        print(f"[WARN] Found multiple {filename} files; using the first one:")
        for match in matches:
            print(f"  - {match}")
    return matches[0]


def load_split(path: Path, split_name: str) -> pd.DataFrame:
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
        raise ValueError(f"{split_name} labels must be 0/1 only; found: {sorted(labels)}")
    if df["content"].str.strip().eq("").any():
        raise ValueError(f"{split_name} contains empty content rows.")

    return df


def softmax(logits: np.ndarray) -> np.ndarray:
    logits = logits - logits.max(axis=1, keepdims=True)
    exp = np.exp(logits)
    return exp / exp.sum(axis=1, keepdims=True)


def make_compute_metrics():
    def compute_metrics(eval_pred):
        logits, labels = eval_pred
        probs = softmax(logits)
        preds = probs.argmax(axis=1)
        p1 = probs[:, 1]

        metrics = {
            "accuracy": accuracy_score(labels, preds),
            "macro_f1": f1_score(labels, preds, average="macro", zero_division=0),
            "weighted_f1": f1_score(labels, preds, average="weighted", zero_division=0),
            "precision_label_1": precision_score(labels, preds, pos_label=1, zero_division=0),
            "recall_label_1": recall_score(labels, preds, pos_label=1, zero_division=0),
            "f1_label_1": f1_score(labels, preds, pos_label=1, zero_division=0),
            "precision_label_0": precision_score(labels, preds, pos_label=0, zero_division=0),
            "recall_label_0": recall_score(labels, preds, pos_label=0, zero_division=0),
            "f1_label_0": f1_score(labels, preds, pos_label=0, zero_division=0),
        }

        if len(np.unique(labels)) == 2:
            metrics["roc_auc"] = roc_auc_score(labels, p1)
            metrics["pr_auc"] = average_precision_score(labels, p1)
        return metrics

    return compute_metrics


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
    dataset = dataset.rename_column("label", "labels")
    keep_columns = ["input_ids", "attention_mask", "labels"]
    dataset.set_format(type="torch", columns=keep_columns)
    return dataset


def make_training_args(args: argparse.Namespace) -> TrainingArguments:
    checkpoint_dir = args.output_dir / "checkpoints"
    common = dict(
        output_dir=str(checkpoint_dir),
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
        dataloader_num_workers=args.num_workers,
    )

    signature = inspect.signature(TrainingArguments.__init__)
    if "eval_strategy" in signature.parameters:
        common["eval_strategy"] = "epoch"
    else:
        common["evaluation_strategy"] = "epoch"

    return TrainingArguments(**common)


def make_trainer(tokenizer, **kwargs) -> Trainer:
    """Create Trainer across transformers versions.

    Newer transformers versions replaced the `tokenizer` argument with
    `processing_class`, while older versions still expect `tokenizer`.
    """

    signature = inspect.signature(Trainer.__init__)
    if "processing_class" in signature.parameters:
        kwargs["processing_class"] = tokenizer
    elif "tokenizer" in signature.parameters:
        kwargs["tokenizer"] = tokenizer
    return Trainer(**kwargs)


def evaluate_predictions(trainer: Trainer, val_ds: Dataset, val_df: pd.DataFrame) -> tuple[dict, pd.DataFrame]:
    output = trainer.predict(val_ds)
    logits = output.predictions
    labels = output.label_ids
    probs = softmax(logits)
    preds = probs.argmax(axis=1)
    cm = confusion_matrix(labels, preds, labels=[0, 1])

    metrics = make_compute_metrics()((logits, labels))
    metrics["confusion_matrix"] = cm.tolist()

    pred_df = val_df.copy()
    pred_df["teacher_logit_0"] = logits[:, 0]
    pred_df["teacher_logit_1"] = logits[:, 1]
    pred_df["teacher_p0_t1"] = probs[:, 0]
    pred_df["teacher_p1_t1"] = probs[:, 1]
    pred_df["teacher_pred"] = preds
    pred_df["teacher_confidence"] = probs.max(axis=1)
    pred_df["teacher_agree_label"] = pred_df["teacher_pred"].astype(int) == pred_df["label"].astype(int)
    return metrics, pred_df


def distribution_table(df: pd.DataFrame, column: str) -> str:
    if column not in df.columns:
        return f"_Column `{column}` not found._"
    counts = df[column].value_counts(dropna=False).rename_axis(column).reset_index(name="count")
    counts["percent"] = (counts["count"] / len(df) * 100).round(2)
    return counts.to_markdown(index=False)


def crosstab_table(df: pd.DataFrame, index: str, columns: str) -> str:
    if index not in df.columns or columns not in df.columns:
        return f"_Columns `{index}`/`{columns}` not found._"
    return pd.crosstab(df[index], df[columns]).to_markdown()


def write_report(
    args: argparse.Namespace,
    train_csv: Path,
    val_csv: Path,
    train_df: pd.DataFrame,
    val_df: pd.DataFrame,
    metrics: dict,
    elapsed_seconds: float,
) -> None:
    lines = [
        "# PhoBERT-base Teacher Fine-tuning Report",
        "",
        "## Configuration",
        "",
        f"- Model: `{args.model_name}`",
        f"- Train CSV: `{train_csv}`",
        f"- Val CSV: `{val_csv}`",
        f"- Seed: `{args.seed}`",
        f"- Max length: `{args.max_length}`",
        f"- Epochs: `{args.epochs}`",
        f"- Train batch size: `{args.train_batch_size}`",
        f"- Eval batch size: `{args.eval_batch_size}`",
        f"- Gradient accumulation steps: `{args.gradient_accumulation_steps}`",
        f"- Learning rate: `{args.learning_rate}`",
        f"- Weight decay: `{args.weight_decay}`",
        f"- Warmup ratio: `{args.warmup_ratio}`",
        f"- FP16: `{args.fp16}`",
        f"- Elapsed seconds: `{round(elapsed_seconds, 2)}`",
        "",
        "## Validation Metrics",
        "",
        pd.DataFrame(
            [{"metric": key, "value": value} for key, value in metrics.items() if key != "confusion_matrix"]
        ).to_markdown(index=False),
        "",
        "## Confusion Matrix",
        "",
        "`labels=[0, 1]`, rows are true labels and columns are predicted labels.",
        "",
        pd.DataFrame(metrics["confusion_matrix"], index=["true_0", "true_1"], columns=["pred_0", "pred_1"]).to_markdown(),
        "",
        "## Train Distribution",
        "",
        "### Label",
        "",
        distribution_table(train_df, "label"),
        "",
        "### Data Origin",
        "",
        distribution_table(train_df, "data_origin"),
        "",
        "### Category",
        "",
        distribution_table(train_df, "category"),
        "",
        "### Label x Data Origin",
        "",
        crosstab_table(train_df, "data_origin", "label"),
        "",
        "## Validation Distribution",
        "",
        "### Label",
        "",
        distribution_table(val_df, "label"),
        "",
        "### Data Origin",
        "",
        distribution_table(val_df, "data_origin"),
        "",
        "### Category",
        "",
        distribution_table(val_df, "category"),
        "",
        "### Label x Data Origin",
        "",
        crosstab_table(val_df, "data_origin", "label"),
        "",
    ]
    (args.output_dir / "teacher_phobert_base_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    set_seed(args.seed)

    train_csv = args.train_csv or find_split_file(args.input_root, "train.csv")
    val_csv = args.val_csv or find_split_file(args.input_root, "val.csv")

    print("[INFO] Configuration")
    print(json.dumps({key: str(value) for key, value in vars(args).items()}, indent=2, ensure_ascii=False))
    print(f"[INFO] train_csv: {train_csv}")
    print(f"[INFO] val_csv  : {val_csv}")
    print(f"[INFO] cuda available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"[INFO] gpu: {torch.cuda.get_device_name(0)}")

    train_df = load_split(train_csv, "train")
    val_df = load_split(val_csv, "val")
    print(f"[INFO] train rows: {len(train_df)}")
    print(f"[INFO] val rows  : {len(val_df)}")
    print("[INFO] train label distribution")
    print(train_df["label"].value_counts().sort_index().to_string())
    print("[INFO] val label distribution")
    print(val_df["label"].value_counts().sort_index().to_string())

    tokenizer = AutoTokenizer.from_pretrained(args.model_name, use_fast=False)
    model = AutoModelForSequenceClassification.from_pretrained(args.model_name, num_labels=2)

    train_ds = tokenize_dataset(train_df, tokenizer, args.max_length)
    val_ds = tokenize_dataset(val_df, tokenizer, args.max_length)

    training_args = make_training_args(args)
    callbacks = []
    if args.early_stopping_patience and args.early_stopping_patience > 0:
        callbacks.append(EarlyStoppingCallback(early_stopping_patience=args.early_stopping_patience))

    trainer = make_trainer(
        tokenizer,
        model=model,
        args=training_args,
        train_dataset=train_ds,
        eval_dataset=val_ds,
        compute_metrics=make_compute_metrics(),
        callbacks=callbacks,
    )

    start = time.time()
    train_result = trainer.train()
    elapsed = time.time() - start

    final_model_dir = args.output_dir / "model"
    trainer.save_model(str(final_model_dir))
    tokenizer.save_pretrained(str(final_model_dir))

    train_metrics = train_result.metrics
    val_metrics, val_predictions = evaluate_predictions(trainer, val_ds, val_df)

    with (args.output_dir / "train_metrics.json").open("w", encoding="utf-8") as f:
        json.dump(train_metrics, f, indent=2, ensure_ascii=False)
    with (args.output_dir / "teacher_phobert_base_metrics.json").open("w", encoding="utf-8") as f:
        json.dump(val_metrics, f, indent=2, ensure_ascii=False)

    val_predictions.to_csv(args.output_dir / "val_teacher_predictions.csv", index=False, encoding="utf-8-sig")
    write_report(args, train_csv, val_csv, train_df, val_df, val_metrics, elapsed)

    print("[OK] Training complete")
    print(f"[OK] Saved model to: {final_model_dir}")
    print(f"[OK] Saved metrics to: {args.output_dir / 'teacher_phobert_base_metrics.json'}")
    print(f"[OK] Saved report to: {args.output_dir / 'teacher_phobert_base_report.md'}")
    print(f"[OK] Saved validation predictions to: {args.output_dir / 'val_teacher_predictions.csv'}")
    print("[INFO] Validation metrics")
    print(json.dumps(val_metrics, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

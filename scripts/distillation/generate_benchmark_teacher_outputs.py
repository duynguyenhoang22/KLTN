"""Generate PhoBERT-base soft labels for benchmark distillation students."""

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
from transformers import AutoModelForSequenceClassification, AutoTokenizer, Trainer, TrainingArguments

from benchmark_config import BENCHMARK_SPLITS
from benchmark_metrics import compute_binary_metrics, metrics_row, write_metrics_bundle


DEFAULT_MODEL_DIR = Path("setup_results/distillation_benchmark/plm_phobert-base/model")
DEFAULT_SPLIT_DIR = Path("data/distillation/benchmark_splits")
DEFAULT_OUTPUT_DIR = Path("data/distillation/benchmark_teacher_outputs/phobert-base")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate PhoBERT-base benchmark teacher outputs.")
    parser.add_argument("--model-dir", type=Path, default=DEFAULT_MODEL_DIR)
    parser.add_argument("--split-dir", type=Path, default=DEFAULT_SPLIT_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--max-length", type=int, default=128)
    parser.add_argument("--eval-batch-size", type=int, default=64)
    parser.add_argument("--temperature", type=float, default=2.0)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--fp16", action="store_true")
    parser.add_argument("--num-workers", type=int, default=2)
    return parser.parse_args()


def softmax(logits: np.ndarray, temperature: float = 1.0) -> np.ndarray:
    scaled = logits / temperature
    scaled = scaled - scaled.max(axis=1, keepdims=True)
    exp = np.exp(scaled)
    return exp / exp.sum(axis=1, keepdims=True)


def load_split(path: Path, split: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    required = {"content", "label"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"{path} missing columns: {sorted(missing)}")
    df = df.copy()
    df["content"] = df["content"].fillna("").astype(str)
    df["label"] = df["label"].astype(int)
    df["split"] = split
    return df


def tokenize_dataset(df: pd.DataFrame, tokenizer, max_length: int) -> Dataset:
    dataset = Dataset.from_pandas(df.reset_index(drop=True), preserve_index=False)

    def tokenize_fn(examples):
        segmented = [ViTokenizer.tokenize(text) for text in examples["content"]]
        return tokenizer(segmented, padding="max_length", truncation=True, max_length=max_length)

    dataset = dataset.map(tokenize_fn, batched=True, desc=f"Tokenizing {df['split'].iloc[0]}")
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
    kwargs["eval_strategy" if "eval_strategy" in signature.parameters else "evaluation_strategy"] = "no"
    return TrainingArguments(**kwargs)


def make_trainer(model, tokenizer, args: argparse.Namespace) -> Trainer:
    kwargs = {"model": model, "args": make_training_args(args)}
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


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    tokenizer = AutoTokenizer.from_pretrained(args.model_dir, use_fast=False)
    model = AutoModelForSequenceClassification.from_pretrained(args.model_dir)
    trainer = make_trainer(model, tokenizer, args)
    rows = []
    split_metrics = {}
    for split, filename in BENCHMARK_SPLITS.items():
        df = load_split(args.split_dir / filename, split)
        dataset = tokenize_dataset(df, tokenizer, args.max_length)
        output = trainer.predict(dataset)
        probs_t1 = softmax(output.predictions, temperature=1.0)
        probs_t = softmax(output.predictions, temperature=args.temperature)
        out = df.copy()
        out["teacher_model"] = "PhoBERT-base"
        out["teacher_version"] = str(args.model_dir)
        out["teacher_logit_0"] = output.predictions[:, 0]
        out["teacher_logit_1"] = output.predictions[:, 1]
        out["teacher_p0_t1"] = probs_t1[:, 0]
        out["teacher_p1_t1"] = probs_t1[:, 1]
        out[f"teacher_p0_t{args.temperature:g}"] = probs_t[:, 0]
        out[f"teacher_p1_t{args.temperature:g}"] = probs_t[:, 1]
        out["teacher_temperature"] = args.temperature
        out["teacher_pred"] = probs_t1.argmax(axis=1)
        out["teacher_confidence"] = probs_t1.max(axis=1)
        out["teacher_agree_label"] = out["teacher_pred"].astype(int) == out["label"].astype(int)
        out["distill_weight"] = out.apply(distill_weight, axis=1)
        metrics = compute_binary_metrics(out["label"].to_numpy(), out["teacher_pred"].to_numpy(), out["teacher_p1_t1"].to_numpy())
        split_metrics[split] = metrics
        rows.append(metrics_row(model_group="teacher", model_name="PhoBERT-base teacher", run_name="teacher_phobert_base", split=split, metrics=metrics))
        out.to_csv(args.output_dir / f"{split}_teacher.csv", index=False, encoding="utf-8-sig")
    metrics_df = write_metrics_bundle(args.output_dir, "teacher_phobert_base", rows, split_metrics)
    print(f"[OK] Wrote teacher outputs to {args.output_dir}")
    print(metrics_df[["split", "rows", "macro_f1", "f1_label_1", "recall_label_1", "pr_auc"]])


if __name__ == "__main__":
    main()

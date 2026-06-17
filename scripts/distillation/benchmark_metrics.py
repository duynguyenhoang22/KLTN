"""Metric helpers used by benchmark training and aggregation scripts."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)

from benchmark_config import PRIMARY_METRICS


def compute_binary_metrics(y_true: np.ndarray, y_pred: np.ndarray, p1: np.ndarray) -> dict:
    metrics = {
        "rows": int(len(y_true)),
        "accuracy": accuracy_score(y_true, y_pred),
        "macro_f1": f1_score(y_true, y_pred, average="macro", zero_division=0),
        "weighted_f1": f1_score(y_true, y_pred, average="weighted", zero_division=0),
        "precision_label_1": precision_score(y_true, y_pred, pos_label=1, zero_division=0),
        "recall_label_1": recall_score(y_true, y_pred, pos_label=1, zero_division=0),
        "f1_label_1": f1_score(y_true, y_pred, pos_label=1, zero_division=0),
        "precision_label_0": precision_score(y_true, y_pred, pos_label=0, zero_division=0),
        "recall_label_0": recall_score(y_true, y_pred, pos_label=0, zero_division=0),
        "f1_label_0": f1_score(y_true, y_pred, pos_label=0, zero_division=0),
        "confusion_matrix": confusion_matrix(y_true, y_pred, labels=[0, 1]).tolist(),
    }
    if len(np.unique(y_true)) == 2:
        metrics["roc_auc"] = roc_auc_score(y_true, p1)
        metrics["pr_auc"] = average_precision_score(y_true, p1)
    else:
        metrics["roc_auc"] = float("nan")
        metrics["pr_auc"] = float("nan")
    return metrics


def metrics_row(
    *,
    model_group: str,
    model_name: str,
    run_name: str,
    split: str,
    metrics: dict,
    metadata: dict | None = None,
) -> dict:
    cm = metrics["confusion_matrix"]
    row = {
        "model_group": model_group,
        "model_name": model_name,
        "run_name": run_name,
        "split": split,
        **{k: v for k, v in metrics.items() if k != "confusion_matrix"},
        "tn": cm[0][0],
        "fp": cm[0][1],
        "fn": cm[1][0],
        "tp": cm[1][1],
    }
    if metadata:
        row.update(metadata)
    return row


def write_metrics_bundle(
    output_dir: Path,
    run_name: str,
    rows: list[dict],
    split_metrics: dict[str, dict],
) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    metrics_df = pd.DataFrame(rows)
    metrics_df.to_csv(output_dir / f"{run_name}_metrics_by_split.csv", index=False)
    with (output_dir / f"{run_name}_metrics.json").open("w", encoding="utf-8") as f:
        json.dump(split_metrics, f, indent=2, ensure_ascii=False)
    return metrics_df


def markdown_metrics_table(df: pd.DataFrame) -> str:
    cols = ["model_group", "model_name", "split", "rows", *PRIMARY_METRICS]
    present = [col for col in cols if col in df.columns]
    display = df[present].copy()
    for col in PRIMARY_METRICS:
        if col in display.columns:
            display[col] = display[col].map(lambda value: "" if pd.isna(value) else f"{value:.4f}")
    return display.to_markdown(index=False)

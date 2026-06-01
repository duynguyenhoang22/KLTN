"""Audit teacher outputs before student distillation.

This script summarizes teacher quality, disagreement, confidence, and error
patterns by split/data_origin/category. It is CPU-only and intended to run
locally after downloading Kaggle teacher output CSVs.
"""

from __future__ import annotations

import argparse
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


DEFAULT_INPUT_DIR = Path("data/distillation/teacher_outputs")
DEFAULT_OUTPUT_DIR = Path("setup_results/distillation/teacher_audit")
SPLIT_FILES = {
    "train": "train_teacher.csv",
    "val": "val_teacher.csv",
    "test_real": "test_real_teacher.csv",
    "test_mixed": "test_mixed_teacher.csv",
    "test_challenge": "test_challenge_teacher.csv",
}
REQUIRED_COLUMNS = {
    "sample_id",
    "content",
    "label",
    "data_origin",
    "category",
    "teacher_p1_t1",
    "teacher_pred",
    "teacher_confidence",
    "teacher_agree_label",
    "distill_weight",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit distillation teacher outputs.")
    parser.add_argument("--input-dir", type=Path, default=DEFAULT_INPUT_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--high-confidence-threshold", type=float, default=0.95)
    parser.add_argument("--uncertain-low", type=float, default=0.40)
    parser.add_argument("--uncertain-high", type=float, default=0.60)
    return parser.parse_args()


def load_outputs(input_dir: Path) -> dict[str, pd.DataFrame]:
    outputs = {}
    for split, filename in SPLIT_FILES.items():
        path = input_dir / filename
        if not path.exists():
            raise FileNotFoundError(f"Missing teacher output file: {path}")
        df = pd.read_csv(path)
        missing = REQUIRED_COLUMNS - set(df.columns)
        if missing:
            raise ValueError(f"{path} missing columns: {sorted(missing)}")
        df = df.copy()
        df["split"] = split
        df["label"] = df["label"].astype(int)
        df["teacher_pred"] = df["teacher_pred"].astype(int)
        df["teacher_agree_label"] = df["teacher_agree_label"].astype(bool)
        outputs[split] = df
    return outputs


def compute_metrics(df: pd.DataFrame) -> dict:
    y_true = df["label"].to_numpy()
    y_pred = df["teacher_pred"].to_numpy()
    p1 = df["teacher_p1_t1"].to_numpy()

    metrics = {
        "rows": int(len(df)),
        "accuracy": accuracy_score(y_true, y_pred),
        "macro_f1": f1_score(y_true, y_pred, average="macro", zero_division=0),
        "weighted_f1": f1_score(y_true, y_pred, average="weighted", zero_division=0),
        "precision_label_1": precision_score(y_true, y_pred, pos_label=1, zero_division=0),
        "recall_label_1": recall_score(y_true, y_pred, pos_label=1, zero_division=0),
        "f1_label_1": f1_score(y_true, y_pred, pos_label=1, zero_division=0),
        "precision_label_0": precision_score(y_true, y_pred, pos_label=0, zero_division=0),
        "recall_label_0": recall_score(y_true, y_pred, pos_label=0, zero_division=0),
        "f1_label_0": f1_score(y_true, y_pred, pos_label=0, zero_division=0),
        "teacher_agree_rate": float(df["teacher_agree_label"].mean()),
        "mean_confidence": float(df["teacher_confidence"].mean()),
        "median_confidence": float(df["teacher_confidence"].median()),
        "mean_p1": float(df["teacher_p1_t1"].mean()),
        "confusion_matrix": confusion_matrix(y_true, y_pred, labels=[0, 1]).tolist(),
    }
    if len(np.unique(y_true)) == 2:
        metrics["roc_auc"] = roc_auc_score(y_true, p1)
        metrics["pr_auc"] = average_precision_score(y_true, p1)
    return metrics


def metrics_by_group(df: pd.DataFrame, group_col: str, min_rows: int = 1) -> pd.DataFrame:
    rows = []
    for value, group in df.groupby(group_col, dropna=False, sort=True):
        if len(group) < min_rows:
            continue
        metrics = compute_metrics(group)
        rows.append(
            {
                group_col: value,
                "rows": metrics["rows"],
                "accuracy": metrics["accuracy"],
                "macro_f1": metrics["macro_f1"],
                "f1_label_1": metrics["f1_label_1"],
                "recall_label_1": metrics["recall_label_1"],
                "precision_label_1": metrics["precision_label_1"],
                "agree_rate": metrics["teacher_agree_rate"],
                "mean_confidence": metrics["mean_confidence"],
            }
        )
    return pd.DataFrame(rows).sort_values(["accuracy", "rows"], ascending=[True, False])


def disagreement_type(row: pd.Series) -> str:
    if bool(row["teacher_agree_label"]):
        return "agree"
    if int(row["label"]) == 0 and int(row["teacher_pred"]) == 1:
        return "false_positive"
    if int(row["label"]) == 1 and int(row["teacher_pred"]) == 0:
        return "false_negative"
    return "unknown"


def confidence_bucket(confidence: float) -> str:
    if confidence >= 0.99:
        return ">=0.99"
    if confidence >= 0.95:
        return "0.95-0.99"
    if confidence >= 0.90:
        return "0.90-0.95"
    if confidence >= 0.80:
        return "0.80-0.90"
    return "<0.80"


def pct(value: float) -> str:
    return f"{value * 100:.2f}%"


def table(df: pd.DataFrame, index: bool = False) -> str:
    if df.empty:
        return "_No rows._"
    return df.to_markdown(index=index)


def crosstab(df: pd.DataFrame, index: str, columns: str) -> str:
    if df.empty:
        return "_No rows._"
    return pd.crosstab(df[index], df[columns]).to_markdown()


def write_report(
    output_dir: Path,
    all_df: pd.DataFrame,
    metrics_summary: pd.DataFrame,
    split_metrics: dict[str, dict],
    high_conf_errors: pd.DataFrame,
    uncertain: pd.DataFrame,
    disagreement: pd.DataFrame,
    args: argparse.Namespace,
) -> None:
    lines = [
        "# Teacher Output Audit Report",
        "",
        "## 1. Scope",
        "",
        f"- Input dir: `{args.input_dir.as_posix()}`",
        f"- High-confidence error threshold: `{args.high_confidence_threshold}`",
        f"- Uncertain p1 range: `{args.uncertain_low}` to `{args.uncertain_high}`",
        "",
        "## 2. Metrics by Split",
        "",
        table(metrics_summary),
        "",
        "## 3. Confusion Matrices",
        "",
    ]

    for split, metrics in split_metrics.items():
        cm = pd.DataFrame(
            metrics["confusion_matrix"],
            index=["true_0", "true_1"],
            columns=["pred_0", "pred_1"],
        )
        lines.extend([f"### {split}", "", table(cm, index=True), ""])

    disagreement_counts = (
        all_df.groupby(["split", "disagreement_type"]).size().reset_index(name="count")
    )
    lines.extend(
        [
            "## 4. Disagreement Counts",
            "",
            table(disagreement_counts),
            "",
            "## 5. Confidence Buckets by Split",
            "",
            crosstab(all_df, "split", "confidence_bucket"),
            "",
            "## 6. Error Summary by Category",
            "",
            table(
                disagreement[disagreement["disagreement_type"] != "agree"]
                .groupby(["split", "category", "disagreement_type"])
                .size()
                .reset_index(name="count")
                .sort_values(["split", "count"], ascending=[True, False])
            ),
            "",
            "## 7. Metrics by Category: test_real",
            "",
            table(metrics_by_group(all_df[all_df["split"] == "test_real"], "category")),
            "",
            "## 8. Metrics by Data Origin",
            "",
            table(metrics_by_group(all_df, "data_origin")),
            "",
            "## 9. High-confidence Errors",
            "",
            f"Rows: `{len(high_conf_errors)}`",
            "",
            table(
                high_conf_errors[
                    [
                        "split",
                        "sample_id",
                        "label",
                        "teacher_pred",
                        "teacher_confidence",
                        "teacher_p1_t1",
                        "data_origin",
                        "category",
                        "content",
                    ]
                ].head(30)
            ),
            "",
            "## 10. Uncertain Samples",
            "",
            f"Rows: `{len(uncertain)}`",
            "",
            table(
                uncertain[
                    [
                        "split",
                        "sample_id",
                        "label",
                        "teacher_pred",
                        "teacher_confidence",
                        "teacher_p1_t1",
                        "data_origin",
                        "category",
                        "content",
                    ]
                ].head(30)
            ),
            "",
            "## 11. Interpretation Notes",
            "",
            "- `test_real` is the primary generalization check.",
            "- `test_mixed` and `test_challenge` are auxiliary checks.",
            "- High-confidence disagreements should be manually reviewed before treating teacher outputs as reliable soft labels.",
            "- `distill_weight` should reduce teacher influence on disagreement rows during student distillation.",
            "",
        ]
    )

    (output_dir / "teacher_audit_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    outputs = load_outputs(args.input_dir)
    all_df = pd.concat(outputs.values(), ignore_index=True)
    all_df["disagreement_type"] = all_df.apply(disagreement_type, axis=1)
    all_df["confidence_bucket"] = all_df["teacher_confidence"].apply(confidence_bucket)

    split_metrics = {split: compute_metrics(df) for split, df in outputs.items()}
    metrics_rows = []
    for split, metrics in split_metrics.items():
        metrics_rows.append(
            {
                "split": split,
                "rows": metrics["rows"],
                "accuracy": round(metrics["accuracy"], 4),
                "macro_f1": round(metrics["macro_f1"], 4),
                "f1_label_1": round(metrics["f1_label_1"], 4),
                "recall_label_1": round(metrics["recall_label_1"], 4),
                "precision_label_1": round(metrics["precision_label_1"], 4),
                "agree_rate": round(metrics["teacher_agree_rate"], 4),
                "mean_confidence": round(metrics["mean_confidence"], 4),
                "roc_auc": round(metrics.get("roc_auc", np.nan), 4),
                "pr_auc": round(metrics.get("pr_auc", np.nan), 4),
            }
        )
    metrics_summary = pd.DataFrame(metrics_rows)

    disagreement = all_df[all_df["disagreement_type"] != "agree"].copy()
    disagreement = disagreement.sort_values(
        ["split", "teacher_confidence"], ascending=[True, False]
    )
    high_conf_errors = disagreement[
        disagreement["teacher_confidence"] >= args.high_confidence_threshold
    ].copy()
    uncertain = all_df[
        (all_df["teacher_p1_t1"] >= args.uncertain_low)
        & (all_df["teacher_p1_t1"] <= args.uncertain_high)
    ].copy()
    uncertain = uncertain.sort_values(["split", "teacher_confidence"], ascending=[True, True])

    metrics_summary.to_csv(args.output_dir / "teacher_metrics_by_split.csv", index=False, encoding="utf-8-sig")
    disagreement.to_csv(args.output_dir / "teacher_disagreements.csv", index=False, encoding="utf-8-sig")
    high_conf_errors.to_csv(args.output_dir / "teacher_high_confidence_errors.csv", index=False, encoding="utf-8-sig")
    uncertain.to_csv(args.output_dir / "teacher_uncertain_samples.csv", index=False, encoding="utf-8-sig")

    category_metrics_rows = []
    for split, df in outputs.items():
        by_cat = metrics_by_group(df, "category")
        if not by_cat.empty:
            by_cat.insert(0, "split", split)
            category_metrics_rows.append(by_cat)
    if category_metrics_rows:
        pd.concat(category_metrics_rows, ignore_index=True).to_csv(
            args.output_dir / "teacher_metrics_by_category.csv",
            index=False,
            encoding="utf-8-sig",
        )

    origin_metrics_rows = []
    for split, df in outputs.items():
        by_origin = metrics_by_group(df, "data_origin")
        if not by_origin.empty:
            by_origin.insert(0, "split", split)
            origin_metrics_rows.append(by_origin)
    if origin_metrics_rows:
        pd.concat(origin_metrics_rows, ignore_index=True).to_csv(
            args.output_dir / "teacher_metrics_by_data_origin.csv",
            index=False,
            encoding="utf-8-sig",
        )

    with (args.output_dir / "teacher_audit_metrics.json").open("w", encoding="utf-8") as f:
        json.dump(split_metrics, f, indent=2, ensure_ascii=False)

    write_report(
        args.output_dir,
        all_df,
        metrics_summary,
        split_metrics,
        high_conf_errors,
        uncertain,
        all_df,
        args,
    )

    print(f"[OK] Wrote audit outputs to {args.output_dir}")
    print(metrics_summary.to_string(index=False))
    print(f"[INFO] disagreement rows: {len(disagreement)}")
    print(f"[INFO] high-confidence error rows: {len(high_conf_errors)}")
    print(f"[INFO] uncertain rows: {len(uncertain)}")


if __name__ == "__main__":
    main()

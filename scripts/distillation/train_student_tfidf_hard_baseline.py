"""Train a TF-IDF + Logistic Regression hard-label student baseline.

Phase 5 of the distillation POC uses only message text and hard labels. Teacher
outputs are intentionally not used here; this script creates the baseline that
Phase 6 distilled students must beat.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.pipeline import Pipeline


DEFAULT_SPLIT_DIR = Path("data/distillation/splits_v2")
DEFAULT_OUTPUT_DIR = Path("setup_results/distillation_v2/student_tfidf_hard_label")
SPLIT_FILES = {
    "train": "train.csv",
    "val": "val.csv",
    "test_real": "test_real.csv",
    "test_mixed": "test_mixed.csv",
    "test_challenge": "test_challenge.csv",
}
REQUIRED_COLUMNS = {
    "sample_id",
    "content",
    "label",
    "data_origin",
    "category",
    "sender_type",
    "has_url",
    "has_phone_number",
    "obfuscation_level",
}
GROUP_COLUMNS = [
    "data_origin",
    "category",
    "sender_type",
    "has_url",
    "has_phone_number",
    "obfuscation_level",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Train Phase 5 TF-IDF + Logistic Regression hard-label baseline."
    )
    parser.add_argument("--split-dir", type=Path, default=DEFAULT_SPLIT_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--threshold", type=float, default=0.5)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--max-features", type=int, default=200_000)
    parser.add_argument("--min-df", type=int, default=2)
    parser.add_argument("--c", type=float, default=2.0)
    parser.add_argument("--no-save-model", action="store_true")
    return parser.parse_args()


def load_splits(split_dir: Path) -> dict[str, pd.DataFrame]:
    splits = {}
    for split, filename in SPLIT_FILES.items():
        path = split_dir / filename
        if not path.exists():
            raise FileNotFoundError(f"Missing split file: {path}")
        df = pd.read_csv(path)
        missing = REQUIRED_COLUMNS - set(df.columns)
        if missing:
            raise ValueError(f"{path} missing columns: {sorted(missing)}")
        df = df.copy()
        df["label"] = df["label"].astype(int)
        df["content"] = df["content"].fillna("").astype(str)
        df["split"] = split
        splits[split] = df
    return splits


def build_pipeline(args: argparse.Namespace) -> Pipeline:
    return Pipeline(
        steps=[
            (
                "tfidf",
                TfidfVectorizer(
                    analyzer="char_wb",
                    ngram_range=(3, 5),
                    min_df=args.min_df,
                    max_features=args.max_features,
                    sublinear_tf=True,
                    lowercase=True,
                ),
            ),
            (
                "clf",
                LogisticRegression(
                    C=args.c,
                    class_weight="balanced",
                    max_iter=2000,
                    n_jobs=-1,
                    random_state=args.seed,
                    solver="saga",
                ),
            ),
        ]
    )


def compute_metrics(y_true: np.ndarray, y_pred: np.ndarray, p1: np.ndarray) -> dict:
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


def predict_split(model: Pipeline, df: pd.DataFrame, threshold: float) -> pd.DataFrame:
    p1 = model.predict_proba(df["content"])[:, 1]
    pred = (p1 >= threshold).astype(int)
    out = df.copy()
    out["student_model"] = "tfidf_char_wb_3_5_logreg"
    out["student_p1"] = p1
    out["student_p0"] = 1.0 - p1
    out["student_pred"] = pred
    out["student_confidence"] = np.maximum(out["student_p0"], out["student_p1"])
    out["student_agree_label"] = out["student_pred"].astype(int) == out["label"].astype(int)
    out["error_type"] = np.where(
        out["student_agree_label"],
        "correct",
        np.where(out["label"].astype(int) == 1, "FN", "FP"),
    )
    return out


def metrics_by_group(predictions: pd.DataFrame, split: str, group_col: str) -> pd.DataFrame:
    rows = []
    for value, group in predictions.groupby(group_col, dropna=False, sort=True):
        y_true = group["label"].to_numpy()
        y_pred = group["student_pred"].to_numpy()
        p1 = group["student_p1"].to_numpy()
        metrics = compute_metrics(y_true, y_pred, p1)
        rows.append(
            {
                "split": split,
                "group_col": group_col,
                "group_value": value,
                "rows": metrics["rows"],
                "accuracy": metrics["accuracy"],
                "macro_f1": metrics["macro_f1"],
                "f1_label_1": metrics["f1_label_1"],
                "recall_label_1": metrics["recall_label_1"],
                "precision_label_1": metrics["precision_label_1"],
                "roc_auc": metrics["roc_auc"],
                "pr_auc": metrics["pr_auc"],
            }
        )
    return pd.DataFrame(rows)


def format_float(value: float) -> str:
    if pd.isna(value):
        return ""
    return f"{value:.4f}"


def markdown_table(df: pd.DataFrame, columns: list[str]) -> str:
    if df.empty:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    rows = []
    for _, row in df[columns].iterrows():
        values = []
        for col in columns:
            value = row[col]
            if isinstance(value, float):
                values.append(format_float(value))
            else:
                values.append(str(value))
        rows.append("| " + " | ".join(values) + " |")
    return "\n".join([header, separator, *rows])


def write_report(
    output_dir: Path,
    args: argparse.Namespace,
    metrics_df: pd.DataFrame,
    group_metrics: pd.DataFrame,
    split_metrics: dict[str, dict],
    train_df: pd.DataFrame,
) -> None:
    table_cols = [
        "split",
        "rows",
        "accuracy",
        "macro_f1",
        "f1_label_1",
        "recall_label_1",
        "precision_label_1",
        "roc_auc",
        "pr_auc",
    ]
    lines = [
        "# Phase 5 Student Hard-label Baseline Report",
        "",
        "## 1. Scope",
        "",
        "- Student: `TF-IDF char_wb 3-5 + Logistic Regression`",
        "- Training signal: hard labels only",
        "- Teacher outputs: not used",
        f"- Split dir: `{args.split_dir}`",
        f"- Decision threshold: `{args.threshold}`",
        "",
        "## 2. Configuration",
        "",
        "```text",
        f"tfidf_analyzer = char_wb",
        f"tfidf_ngram_range = (3, 5)",
        f"tfidf_min_df = {args.min_df}",
        f"tfidf_max_features = {args.max_features}",
        f"logreg_C = {args.c}",
        "logreg_class_weight = balanced",
        f"seed = {args.seed}",
        "```",
        "",
        "The model uses only `content` as input. Metadata columns are kept only for audit.",
        "",
        "## 3. Metrics by Split",
        "",
        markdown_table(metrics_df, table_cols),
        "",
        "## 4. Confusion Matrices",
        "",
    ]
    for split, metrics in split_metrics.items():
        tn, fp = metrics["confusion_matrix"][0]
        fn, tp = metrics["confusion_matrix"][1]
        lines.extend(
            [
                f"### {split}",
                "",
                "| | pred_0 | pred_1 |",
                "|---|---:|---:|",
                f"| true_0 | {tn} | {fp} |",
                f"| true_1 | {fn} | {tp} |",
                "",
            ]
        )

    lines.extend(
        [
            "## 5. Train Distribution",
            "",
            "### Label",
            "",
            train_df["label"]
            .value_counts()
            .rename_axis("label")
            .reset_index(name="count")
            .to_markdown(index=False),
            "",
            "### Data Origin",
            "",
            train_df["data_origin"]
            .value_counts()
            .rename_axis("data_origin")
            .reset_index(name="count")
            .to_markdown(index=False),
            "",
            "## 6. Group Audit Files",
            "",
            "Full subgroup metrics are saved to `student_tfidf_hard_metrics_by_group.csv`.",
            "",
        ]
    )

    focus_groups = group_metrics[group_metrics["split"].isin(["test_real", "test_mixed", "test_challenge"])]
    focus_groups = focus_groups[focus_groups["group_col"].eq("data_origin")]
    if not focus_groups.empty:
        lines.extend(
            [
                "### Test Metrics by Data Origin",
                "",
                markdown_table(
                    focus_groups.sort_values(["split", "group_value"]),
                    [
                        "split",
                        "group_value",
                        "rows",
                        "macro_f1",
                        "f1_label_1",
                        "recall_label_1",
                        "precision_label_1",
                    ],
                ),
                "",
            ]
        )

    lines.extend(
        [
            "## 7. Outputs",
            "",
            "```text",
            "student_tfidf_hard_metrics.json",
            "student_tfidf_hard_metrics_by_split.csv",
            "student_tfidf_hard_metrics_by_group.csv",
            "student_tfidf_hard_predictions_<split>.csv",
            "student_tfidf_hard_errors_<split>.csv",
            "student_tfidf_hard_model.joblib",
            "student_tfidf_hard_report.md",
            "```",
            "",
            "## 8. Phase 6 Reminder",
            "",
            "This baseline must be compared against a distilled student with the same architecture. "
            "If Phase 6 reduces `recall_label_1` on `test_real`, report the trade-off explicitly.",
            "",
        ]
    )
    (output_dir / "student_tfidf_hard_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    splits = load_splits(args.split_dir)
    model = build_pipeline(args)
    model.fit(splits["train"]["content"], splits["train"]["label"])

    metrics_rows = []
    split_metrics = {}
    group_frames = []

    for split, df in splits.items():
        predictions = predict_split(model, df, args.threshold)
        y_true = predictions["label"].to_numpy()
        y_pred = predictions["student_pred"].to_numpy()
        p1 = predictions["student_p1"].to_numpy()
        metrics = compute_metrics(y_true, y_pred, p1)
        split_metrics[split] = metrics
        metrics_rows.append(
            {
                "split": split,
                **{k: v for k, v in metrics.items() if k != "confusion_matrix"},
                "tn": metrics["confusion_matrix"][0][0],
                "fp": metrics["confusion_matrix"][0][1],
                "fn": metrics["confusion_matrix"][1][0],
                "tp": metrics["confusion_matrix"][1][1],
            }
        )

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
            "student_model",
            "student_p0",
            "student_p1",
            "student_pred",
            "student_confidence",
            "student_agree_label",
            "error_type",
        ]
        predictions[keep_cols].to_csv(
            args.output_dir / f"student_tfidf_hard_predictions_{split}.csv", index=False
        )
        predictions.loc[~predictions["student_agree_label"], keep_cols].to_csv(
            args.output_dir / f"student_tfidf_hard_errors_{split}.csv", index=False
        )

        for group_col in GROUP_COLUMNS:
            group_frames.append(metrics_by_group(predictions, split, group_col))

    metrics_df = pd.DataFrame(metrics_rows)
    metrics_df.to_csv(args.output_dir / "student_tfidf_hard_metrics_by_split.csv", index=False)
    with (args.output_dir / "student_tfidf_hard_metrics.json").open("w", encoding="utf-8") as f:
        json.dump(split_metrics, f, ensure_ascii=False, indent=2)

    group_metrics = pd.concat(group_frames, ignore_index=True)
    group_metrics.to_csv(args.output_dir / "student_tfidf_hard_metrics_by_group.csv", index=False)

    config = {
        "student_model": "tfidf_char_wb_3_5_logreg",
        "split_dir": str(args.split_dir),
        "output_dir": str(args.output_dir),
        "threshold": args.threshold,
        "seed": args.seed,
        "max_features": args.max_features,
        "min_df": args.min_df,
        "C": args.c,
        "class_weight": "balanced",
        "teacher_outputs_used": False,
        "input_features": ["content"],
        "metadata_used_for_training": False,
    }
    with (args.output_dir / "student_tfidf_hard_config.json").open("w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

    if not args.no_save_model:
        joblib.dump(model, args.output_dir / "student_tfidf_hard_model.joblib")

    write_report(args.output_dir, args, metrics_df, group_metrics, split_metrics, splits["train"])

    print(f"Wrote Phase 5 hard-label baseline outputs to {args.output_dir}")
    print(metrics_df[["split", "rows", "macro_f1", "f1_label_1", "recall_label_1", "precision_label_1"]])


if __name__ == "__main__":
    main()

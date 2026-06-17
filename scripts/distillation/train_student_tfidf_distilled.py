"""Train a TF-IDF + Logistic Regression distilled student.

This is Phase 6 of the distillation POC. It keeps the same text-only TF-IDF
student architecture used in Phase 5, but trains Logistic Regression with soft
targets derived from hard labels plus teacher probabilities.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from scipy import sparse
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


DEFAULT_TEACHER_DIR = Path("data/distillation/teacher_outputs_v2")
DEFAULT_BASELINE_DIR = Path("setup_results/distillation_v2/student_tfidf_hard_label")
DEFAULT_OUTPUT_DIR = Path("setup_results/distillation_v2/student_tfidf_distilled")
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
    "sender_type",
    "has_url",
    "has_phone_number",
    "obfuscation_level",
    "teacher_p0_t2",
    "teacher_p1_t2",
    "teacher_pred",
    "teacher_confidence",
    "teacher_agree_label",
    "distill_weight",
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
        description="Train Phase 6 TF-IDF + Logistic Regression distilled student."
    )
    parser.add_argument("--teacher-dir", type=Path, default=DEFAULT_TEACHER_DIR)
    parser.add_argument("--baseline-dir", type=Path, default=DEFAULT_BASELINE_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--threshold", type=float, default=0.5)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--max-features", type=int, default=200_000)
    parser.add_argument("--min-df", type=int, default=2)
    parser.add_argument("--c", type=float, default=2.0)
    parser.add_argument("--alpha", type=float, default=0.8)
    parser.add_argument("--fn-distill-weight", type=float, default=0.0)
    parser.add_argument("--teacher-prob-column", choices=["t1", "t2"], default="t2")
    parser.add_argument("--no-save-model", action="store_true")
    return parser.parse_args()


def load_teacher_outputs(teacher_dir: Path) -> dict[str, pd.DataFrame]:
    splits = {}
    for split, filename in SPLIT_FILES.items():
        path = teacher_dir / filename
        if not path.exists():
            raise FileNotFoundError(f"Missing teacher output file: {path}")
        df = pd.read_csv(path)
        missing = REQUIRED_COLUMNS - set(df.columns)
        if missing:
            raise ValueError(f"{path} missing columns: {sorted(missing)}")
        df = df.copy()
        df["label"] = df["label"].astype(int)
        df["teacher_pred"] = df["teacher_pred"].astype(int)
        df["teacher_agree_label"] = df["teacher_agree_label"].astype(bool)
        df["content"] = df["content"].fillna("").astype(str)
        df["split"] = split
        splits[split] = df
    return splits


def teacher_prob_columns(args: argparse.Namespace) -> tuple[str, str]:
    if args.teacher_prob_column == "t1":
        return "teacher_p0_t1", "teacher_p1_t1"
    return "teacher_p0_t2", "teacher_p1_t2"


def effective_distill_weight(df: pd.DataFrame, fn_weight: float) -> np.ndarray:
    weights = df["distill_weight"].astype(float).to_numpy().copy()
    false_negative_teacher = (df["label"].astype(int).to_numpy() == 1) & (
        df["teacher_pred"].astype(int).to_numpy() == 0
    )
    weights[false_negative_teacher] = np.minimum(weights[false_negative_teacher], fn_weight)
    return np.clip(weights, 0.0, 1.0)


def soft_target_p1(df: pd.DataFrame, args: argparse.Namespace) -> np.ndarray:
    _, p1_col = teacher_prob_columns(args)
    hard = df["label"].astype(float).to_numpy()
    teacher_p1 = df[p1_col].astype(float).to_numpy()
    weights = effective_distill_weight(df, args.fn_distill_weight)
    beta = (1.0 - args.alpha) * weights
    return np.clip((1.0 - beta) * hard + beta * teacher_p1, 0.0, 1.0)


def make_soft_label_training_matrix(
    x_train: sparse.spmatrix, train_df: pd.DataFrame, args: argparse.Namespace
) -> tuple[sparse.spmatrix, np.ndarray, np.ndarray, pd.DataFrame]:
    p1_soft = soft_target_p1(train_df, args)
    p0_soft = 1.0 - p1_soft

    x_aug = sparse.vstack([x_train, x_train], format="csr")
    y_aug = np.concatenate(
        [
            np.zeros(len(train_df), dtype=int),
            np.ones(len(train_df), dtype=int),
        ]
    )
    sample_weight = np.concatenate([p0_soft, p1_soft])

    audit = train_df[
        [
            "sample_id",
            "label",
            "teacher_pred",
            "teacher_confidence",
            "teacher_agree_label",
            "distill_weight",
            "data_origin",
            "category",
        ]
    ].copy()
    audit["effective_distill_weight"] = effective_distill_weight(train_df, args.fn_distill_weight)
    audit["soft_target_p1"] = p1_soft
    audit["soft_target_p0"] = p0_soft
    audit["beta"] = (1.0 - args.alpha) * audit["effective_distill_weight"]
    return x_aug, y_aug, sample_weight, audit


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


def predict_split(
    vectorizer: TfidfVectorizer, clf: LogisticRegression, df: pd.DataFrame, threshold: float
) -> pd.DataFrame:
    x = vectorizer.transform(df["content"])
    p1 = clf.predict_proba(x)[:, 1]
    pred = (p1 >= threshold).astype(int)
    out = df.copy()
    out["student_model"] = "tfidf_char_wb_3_5_logreg_soft_target"
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
        metrics = compute_metrics(
            group["label"].to_numpy(),
            group["student_pred"].to_numpy(),
            group["student_p1"].to_numpy(),
        )
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


def load_baseline_metrics(baseline_dir: Path) -> pd.DataFrame | None:
    path = baseline_dir / "student_tfidf_hard_metrics_by_split.csv"
    if not path.exists():
        return None
    return pd.read_csv(path)


def format_float(value: float) -> str:
    if pd.isna(value):
        return ""
    return f"{value:.4f}"


def markdown_table(df: pd.DataFrame, columns: list[str]) -> str:
    if df is None or df.empty:
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


def comparison_table(metrics_df: pd.DataFrame, baseline_df: pd.DataFrame | None) -> pd.DataFrame:
    if baseline_df is None:
        return pd.DataFrame()
    cols = ["split", "macro_f1", "f1_label_1", "recall_label_1", "precision_label_1", "pr_auc"]
    left = baseline_df[cols].copy()
    right = metrics_df[cols].copy()
    merged = left.merge(right, on="split", suffixes=("_hard", "_distilled"))
    for metric in cols[1:]:
        merged[f"delta_{metric}"] = merged[f"{metric}_distilled"] - merged[f"{metric}_hard"]
    return merged


def write_report(
    output_dir: Path,
    args: argparse.Namespace,
    metrics_df: pd.DataFrame,
    group_metrics: pd.DataFrame,
    split_metrics: dict[str, dict],
    baseline_df: pd.DataFrame | None,
    soft_audit: pd.DataFrame,
) -> None:
    metric_cols = [
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
    compare = comparison_table(metrics_df, baseline_df)
    compare_cols = [
        "split",
        "macro_f1_hard",
        "macro_f1_distilled",
        "delta_macro_f1",
        "f1_label_1_hard",
        "f1_label_1_distilled",
        "delta_f1_label_1",
        "recall_label_1_hard",
        "recall_label_1_distilled",
        "delta_recall_label_1",
        "precision_label_1_hard",
        "precision_label_1_distilled",
        "delta_precision_label_1",
    ]
    lines = [
        "# Phase 6 Student Distilled Report",
        "",
        "## 1. Scope",
        "",
        "- Student: `TF-IDF char_wb 3-5 + Logistic Regression`",
        "- Training signal: hard labels plus teacher probabilities",
        "- Input features: `content` only",
        f"- Teacher dir: `{args.teacher_dir}`",
        f"- Baseline dir: `{args.baseline_dir}`",
        "",
        "## 2. Distillation Method",
        "",
        "Scikit-learn Logistic Regression does not accept soft targets directly. "
        "This implementation converts each training sample into two weighted rows: "
        "one with label 0 and weight `soft_target_p0`, one with label 1 and weight `soft_target_p1`.",
        "",
        "```text",
        "beta = (1 - alpha) * effective_distill_weight",
        "soft_target_p1 = (1 - beta) * hard_label + beta * teacher_p1",
        "soft_target_p0 = 1 - soft_target_p1",
        "```",
        "",
        "For teacher false negatives (`label=1`, `teacher_pred=0`), "
        "`effective_distill_weight` is capped to avoid teaching the student to miss smishing.",
        "",
        "## 3. Configuration",
        "",
        "```text",
        f"alpha = {args.alpha}",
        f"teacher_probability = {args.teacher_prob_column}",
        f"fn_distill_weight = {args.fn_distill_weight}",
        f"threshold = {args.threshold}",
        f"tfidf_min_df = {args.min_df}",
        f"tfidf_max_features = {args.max_features}",
        f"logreg_C = {args.c}",
        "class_weight = balanced",
        f"seed = {args.seed}",
        "```",
        "",
        "## 4. Metrics by Split",
        "",
        markdown_table(metrics_df, metric_cols),
        "",
        "## 5. Comparison with Phase 5 Hard-label Baseline",
        "",
        markdown_table(compare, compare_cols),
        "",
        "## 6. Confusion Matrices",
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
            "## 7. Soft Target Audit",
            "",
            "| statistic | value |",
            "|---|---:|",
            f"| mean_effective_distill_weight | {soft_audit['effective_distill_weight'].mean():.4f} |",
            f"| mean_beta | {soft_audit['beta'].mean():.4f} |",
            f"| mean_soft_target_p1 | {soft_audit['soft_target_p1'].mean():.4f} |",
            f"| teacher_disagreement_rows | {int((~soft_audit['teacher_agree_label']).sum())} |",
            "",
            "## 8. Group Audit Files",
            "",
            "Full subgroup metrics are saved to `student_tfidf_distilled_metrics_by_group.csv`.",
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
            "## 9. Outputs",
            "",
            "```text",
            "student_tfidf_distilled_metrics.json",
            "student_tfidf_distilled_metrics_by_split.csv",
            "student_tfidf_distilled_metrics_by_group.csv",
            "student_tfidf_distilled_comparison_with_hard.csv",
            "student_tfidf_distilled_predictions_<split>.csv",
            "student_tfidf_distilled_errors_<split>.csv",
            "student_tfidf_distilled_soft_target_audit_train.csv",
            "student_tfidf_distilled_model.joblib",
            "student_tfidf_distilled_report.md",
            "```",
            "",
        ]
    )
    (output_dir / "student_tfidf_distilled_report.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def main() -> None:
    args = parse_args()
    if not 0.0 <= args.alpha <= 1.0:
        raise ValueError("--alpha must be between 0 and 1")
    args.output_dir.mkdir(parents=True, exist_ok=True)

    splits = load_teacher_outputs(args.teacher_dir)
    train_df = splits["train"]

    vectorizer = TfidfVectorizer(
        analyzer="char_wb",
        ngram_range=(3, 5),
        min_df=args.min_df,
        max_features=args.max_features,
        sublinear_tf=True,
        lowercase=True,
    )
    x_train = vectorizer.fit_transform(train_df["content"])
    x_aug, y_aug, sample_weight, soft_audit = make_soft_label_training_matrix(
        x_train, train_df, args
    )
    soft_audit.to_csv(
        args.output_dir / "student_tfidf_distilled_soft_target_audit_train.csv", index=False
    )

    clf = LogisticRegression(
        C=args.c,
        class_weight="balanced",
        max_iter=2000,
        n_jobs=-1,
        random_state=args.seed,
        solver="saga",
    )
    clf.fit(x_aug, y_aug, sample_weight=sample_weight)

    metrics_rows = []
    split_metrics = {}
    group_frames = []

    for split, df in splits.items():
        predictions = predict_split(vectorizer, clf, df, args.threshold)
        metrics = compute_metrics(
            predictions["label"].to_numpy(),
            predictions["student_pred"].to_numpy(),
            predictions["student_p1"].to_numpy(),
        )
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
            "teacher_p1_t1",
            "teacher_p1_t2",
            "teacher_pred",
            "teacher_confidence",
            "teacher_agree_label",
            "distill_weight",
            "student_model",
            "student_p0",
            "student_p1",
            "student_pred",
            "student_confidence",
            "student_agree_label",
            "error_type",
        ]
        predictions[keep_cols].to_csv(
            args.output_dir / f"student_tfidf_distilled_predictions_{split}.csv", index=False
        )
        predictions.loc[~predictions["student_agree_label"], keep_cols].to_csv(
            args.output_dir / f"student_tfidf_distilled_errors_{split}.csv", index=False
        )

        for group_col in GROUP_COLUMNS:
            group_frames.append(metrics_by_group(predictions, split, group_col))

    metrics_df = pd.DataFrame(metrics_rows)
    metrics_df.to_csv(args.output_dir / "student_tfidf_distilled_metrics_by_split.csv", index=False)
    with (args.output_dir / "student_tfidf_distilled_metrics.json").open(
        "w", encoding="utf-8"
    ) as f:
        json.dump(split_metrics, f, ensure_ascii=False, indent=2)

    group_metrics = pd.concat(group_frames, ignore_index=True)
    group_metrics.to_csv(args.output_dir / "student_tfidf_distilled_metrics_by_group.csv", index=False)

    baseline_df = load_baseline_metrics(args.baseline_dir)
    compare = comparison_table(metrics_df, baseline_df)
    compare.to_csv(args.output_dir / "student_tfidf_distilled_comparison_with_hard.csv", index=False)

    config = {
        "student_model": "tfidf_char_wb_3_5_logreg_soft_target",
        "teacher_dir": str(args.teacher_dir),
        "baseline_dir": str(args.baseline_dir),
        "output_dir": str(args.output_dir),
        "threshold": args.threshold,
        "seed": args.seed,
        "max_features": args.max_features,
        "min_df": args.min_df,
        "C": args.c,
        "alpha": args.alpha,
        "teacher_prob_column": args.teacher_prob_column,
        "fn_distill_weight": args.fn_distill_weight,
        "class_weight": "balanced",
        "input_features": ["content"],
        "metadata_used_for_training": False,
        "distillation_method": "duplicated rows with soft-target sample weights",
    }
    with (args.output_dir / "student_tfidf_distilled_config.json").open(
        "w", encoding="utf-8"
    ) as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

    if not args.no_save_model:
        joblib.dump(
            {"vectorizer": vectorizer, "classifier": clf},
            args.output_dir / "student_tfidf_distilled_model.joblib",
        )

    write_report(
        args.output_dir,
        args,
        metrics_df,
        group_metrics,
        split_metrics,
        baseline_df,
        soft_audit,
    )

    print(f"Wrote Phase 6 distilled outputs to {args.output_dir}")
    print(
        metrics_df[
            ["split", "rows", "macro_f1", "f1_label_1", "recall_label_1", "precision_label_1"]
        ]
    )
    if not compare.empty:
        print(
            compare[
                [
                    "split",
                    "delta_macro_f1",
                    "delta_f1_label_1",
                    "delta_recall_label_1",
                    "delta_precision_label_1",
                ]
            ]
        )


if __name__ == "__main__":
    main()

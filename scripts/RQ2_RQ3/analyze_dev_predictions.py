"""Create moderate-depth RQ2/RQ3 analyses from benchmark dev predictions."""

from __future__ import annotations

from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score, f1_score, recall_score


PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = Path(__file__).resolve().parent

MODEL_FILES = {
    "CafeBERT": PROJECT_ROOT
    / "setup_results/distillation_benchmark/plm_cafebert/plm_cafebert_predictions_dev.csv",
    "DistilBERT multilingual": PROJECT_ROOT
    / "setup_results/distillation_benchmark/plm_distilledbert/plm_distilledbert_predictions_dev.csv",
    "TextCNN": PROJECT_ROOT
    / "setup_results/distillation_benchmark/char_models/char_textcnn_hard/char_textcnn_hard_predictions_dev.csv",
    "TextCNN distilled": PROJECT_ROOT
    / "setup_results/distillation_benchmark/char_models/char_textcnn_distilled_phobert_base/char_textcnn_distilled_phobert_base_predictions_dev.csv",
}


def load_predictions() -> pd.DataFrame:
    frames = []
    for model, path in MODEL_FILES.items():
        if not path.exists():
            raise FileNotFoundError(path)
        df = pd.read_csv(path)
        required = {
            "sample_id",
            "content",
            "label",
            "data_origin",
            "category",
            "sender_type",
            "has_url",
            "has_phone_number",
            "obfuscation_level",
            "p1",
            "pred",
            "confidence",
            "error_type",
        }
        missing = required - set(df.columns)
        if missing:
            raise ValueError(f"{path} missing columns: {sorted(missing)}")
        df = df.copy()
        df["analysis_model"] = model
        df["char_length"] = df["content"].fillna("").astype(str).str.len()
        df["length_group"] = pd.cut(
            df["char_length"],
            bins=[-1, 80, 160, 240, np.inf],
            labels=["≤80", "81–160", "161–240", ">240"],
        )
        frames.append(df)
    out = pd.concat(frames, ignore_index=True)
    return out


def binary_slice_metrics(group: pd.DataFrame) -> dict:
    y = group["label"].astype(int).to_numpy()
    pred = group["pred"].astype(int).to_numpy()
    p1 = group["p1"].astype(float).to_numpy()
    labels = set(y.tolist())
    row = {
        "n": len(group),
        "label_0": int((y == 0).sum()),
        "label_1": int((y == 1).sum()),
        "fp": int(((y == 0) & (pred == 1)).sum()),
        "fn": int(((y == 1) & (pred == 0)).sum()),
    }
    if labels == {0, 1}:
        row.update(
            {
                "macro_f1": f1_score(y, pred, average="macro", zero_division=0),
                "f1_label_1": f1_score(y, pred, pos_label=1, zero_division=0),
                "recall_label_1": recall_score(y, pred, pos_label=1, zero_division=0),
                "pr_auc": average_precision_score(y, p1),
            }
        )
    else:
        row.update(
            {
                "macro_f1": np.nan,
                "f1_label_1": np.nan,
                "recall_label_1": np.nan,
                "pr_auc": np.nan,
            }
        )
    if row["label_0"]:
        row["fpr_label_0"] = row["fp"] / row["label_0"]
    else:
        row["fpr_label_0"] = np.nan
    return row


def summarize_slice(df: pd.DataFrame, column: str) -> pd.DataFrame:
    rows = []
    for (model, value), group in df.groupby(
        ["analysis_model", column], observed=True, dropna=False
    ):
        rows.append(
            {
                "model": model,
                "slice": column,
                "group": value,
                **binary_slice_metrics(group),
            }
        )
    return pd.DataFrame(rows)


def summarize_obfuscation(df: pd.DataFrame) -> pd.DataFrame:
    positive = df[df["label"].eq(1)].copy()
    mapping = {
        "Level 0 - Formal": "Level 0",
        "Level 1 - Leet nhẹ": "Level 1–2",
        "Level 2 - Leet nặng": "Level 1–2",
        "Level 3 - Dot/Dash": "Level 3–4",
        "Level 4 - Mixed special characters": "Level 3–4",
    }
    positive["obfuscation_group"] = positive["obfuscation_level"].map(mapping)
    rows = []
    for (model, value), group in positive.groupby(
        ["analysis_model", "obfuscation_group"], observed=True, dropna=False
    ):
        y = group["label"].astype(int).to_numpy()
        pred = group["pred"].astype(int).to_numpy()
        rows.append(
            {
                "model": model,
                "group": value,
                "n_label_1": len(group),
                "tp": int((pred == 1).sum()),
                "fn": int((pred == 0).sum()),
                "recall_label_1": recall_score(
                    y, pred, pos_label=1, zero_division=0
                ),
            }
        )
    return pd.DataFrame(rows)


def error_overview(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for model, group in df.groupby("analysis_model"):
        errors = group[group["pred"].astype(int).ne(group["label"].astype(int))]
        rows.append(
            {
                "model": model,
                "fp": int(errors["error_type"].eq("FP").sum()),
                "fn": int(errors["error_type"].eq("FN").sum()),
                "total_errors": len(errors),
                "high_confidence_errors_0.9": int(
                    errors["confidence"].astype(float).ge(0.9).sum()
                ),
            }
        )
    return pd.DataFrame(rows)


def error_overlap(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    errors = {
        model: set(
            group.loc[
                group["pred"].astype(int).ne(group["label"].astype(int)), "sample_id"
            ]
        )
        for model, group in df.groupby("analysis_model")
    }
    pair_rows = []
    for left, right in combinations(errors, 2):
        intersection = errors[left] & errors[right]
        union = errors[left] | errors[right]
        pair_rows.append(
            {
                "model_a": left,
                "model_b": right,
                "shared_errors": len(intersection),
                "union_errors": len(union),
                "jaccard": len(intersection) / len(union) if union else np.nan,
            }
        )
    all_shared = set.intersection(*errors.values())
    shared_df = (
        df[
            df["sample_id"].isin(all_shared)
            & df["pred"].astype(int).ne(df["label"].astype(int))
        ][
            [
                "sample_id",
                "content",
                "label",
                "data_origin",
                "category",
                "sender_type",
                "has_url",
                "has_phone_number",
                "obfuscation_level",
                "analysis_model",
                "pred",
                "p1",
                "confidence",
                "error_type",
            ]
        ]
        .sort_values(["sample_id", "analysis_model"])
        .reset_index(drop=True)
    )
    return pd.DataFrame(pair_rows), shared_df


def representative_errors(df: pd.DataFrame) -> pd.DataFrame:
    errors = df[df["pred"].astype(int).ne(df["label"].astype(int))].copy()
    counts = (
        errors.groupby(
            [
                "sample_id",
                "content",
                "label",
                "data_origin",
                "category",
                "sender_type",
                "has_url",
                "has_phone_number",
                "obfuscation_level",
                "error_type",
            ],
            dropna=False,
        )
        .agg(
            models_wrong=("analysis_model", "nunique"),
            wrong_models=("analysis_model", lambda x: " | ".join(sorted(set(x)))),
            mean_wrong_confidence=("confidence", "mean"),
            max_wrong_confidence=("confidence", "max"),
            mean_p1=("p1", "mean"),
        )
        .reset_index()
    )
    counts = counts.sort_values(
        ["models_wrong", "max_wrong_confidence"], ascending=[False, False]
    )
    selected = pd.concat(
        [
            counts[counts["error_type"].eq("FN")].head(6),
            counts[counts["error_type"].eq("FP")].head(6),
        ],
        ignore_index=True,
    )
    return selected


def main() -> None:
    df = load_predictions()
    slice_frames = [
        summarize_slice(df, "length_group"),
        summarize_slice(df, "data_origin"),
        summarize_slice(df, "has_url"),
        summarize_slice(df, "has_phone_number"),
        summarize_slice(df, "sender_type"),
    ]
    slice_metrics = pd.concat(slice_frames, ignore_index=True)
    obfuscation = summarize_obfuscation(df)
    overview = error_overview(df)
    pair_overlap, shared_errors = error_overlap(df)
    examples = representative_errors(df)

    slice_metrics.to_csv(OUTPUT_DIR / "rq2_slice_metrics_dev.csv", index=False)
    obfuscation.to_csv(OUTPUT_DIR / "rq2_obfuscation_label1_dev.csv", index=False)
    overview.to_csv(OUTPUT_DIR / "rq3_error_overview_dev.csv", index=False)
    pair_overlap.to_csv(OUTPUT_DIR / "rq3_pairwise_error_overlap_dev.csv", index=False)
    shared_errors.to_csv(OUTPUT_DIR / "rq3_shared_errors_dev.csv", index=False)
    examples.to_csv(OUTPUT_DIR / "rq3_representative_errors_dev.csv", index=False)
    print(f"[OK] Wrote RQ2/RQ3 artifacts to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()

"""Create improved v2 splits for offline soft-label distillation.

Compared with the first split version, v2 reduces source-separation artifacts:
- test_mixed contains a holdout mixture from every data_origin, not only
  synthetic/paraphrased;
- test_challenge contains realistic hard candidates from real, synthetic,
  paraphrased, synthetic_hard_positive, and external sources;
- test_real remains real-only and continues to be the primary benchmark.

The script writes to data/distillation/splits_v2 by default and does not
overwrite the existing split files.
"""

from __future__ import annotations

import argparse
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd


DEFAULT_INPUT = Path("model/base/temp.csv")
DEFAULT_SPLIT_DIR = Path("data/distillation/splits_v2")
DEFAULT_REPORT = Path("setup_results/distillation/split_report_v2.md")
DEFAULT_SEED = 42

REQUIRED_COLUMNS = [
    "sample_id",
    "content",
    "label",
    "has_url",
    "has_phone_number",
    "sender_type",
    "category",
    "obfuscation_level",
    "data_origin",
]

SPLIT_FILES = {
    "train": "train.csv",
    "val": "val.csv",
    "test_real": "test_real.csv",
    "test_mixed": "test_mixed.csv",
    "test_challenge": "test_challenge.csv",
}

ORIGIN_FRACTIONS = {
    "real": {"val": 0.15, "test_real": 0.15, "test_mixed": 0.10, "test_challenge": 0.10},
    "synthetic": {"val": 0.10, "test_mixed": 0.10, "test_challenge": 0.05},
    "paraphrased": {"val": 0.10, "test_mixed": 0.10, "test_challenge": 0.03},
    "synthetic_hard_positive": {"val": 0.10, "test_mixed": 0.10, "test_challenge": 0.20},
    "external_curated": {"val": 0.10, "test_mixed": 0.10, "test_challenge": 0.10},
    "external_real": {"val": 0.10, "test_mixed": 0.10, "test_challenge": 0.10},
}

HARD_LABEL0_CATEGORIES = {
    "Ngân hàng thật",
    "Dịch vụ công thật",
    "Tin nhắn cá nhân và OTP",
    "Viễn thông",
    "Khác",
    "Quảng cáo hợp lệ",
    "P2P hard negative",
    "P2P hội thoại thông thường",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create v2 ViSmishDS distillation splits.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--split-dir", type=Path, default=DEFAULT_SPLIT_DIR)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    return parser.parse_args()


def validate_source(df: pd.DataFrame, input_path: Path) -> None:
    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_columns:
        raise ValueError(f"{input_path} is missing required columns: {missing_columns}")

    missing_values = df[REQUIRED_COLUMNS].isna().sum()
    missing_values = missing_values[missing_values > 0]
    if not missing_values.empty:
        raise ValueError(f"Missing values found:\n{missing_values.to_string()}")

    if df["category"].astype(str).str.strip().eq("").any():
        raise ValueError("Found empty category values.")

    duplicated_content = int(df.duplicated("content").sum())
    duplicated_sample_id = int(df.duplicated("sample_id").sum())
    if duplicated_content or duplicated_sample_id:
        raise ValueError(
            "Duplicates found: "
            f"content={duplicated_content}, sample_id={duplicated_sample_id}"
        )

    unknown_origins = sorted(set(df["data_origin"]) - set(ORIGIN_FRACTIONS))
    if unknown_origins:
        raise ValueError(f"Unknown data_origin values: {unknown_origins}")


def stable_group_seed(seed: int, key: tuple[object, object, object]) -> int:
    key_text = "||".join(str(part) for part in key)
    value = seed
    for char in key_text:
        value = (value * 131 + ord(char)) % (2**32 - 1)
    return value


def target_count(n: int, fraction: float) -> int:
    if fraction <= 0:
        return 0
    return max(1, int(round(n * fraction)))


def is_challenge_candidate(row: pd.Series) -> bool:
    label = int(row["label"])
    if label == 1:
        return True

    has_risk_signal = int(row["has_url"]) == 1 or int(row["has_phone_number"]) == 1
    category_is_hard = str(row["category"]) in HARD_LABEL0_CATEGORIES
    return has_risk_signal or category_is_hard


def take_indices(
    available: list[int],
    count: int,
    allowed: set[int] | None = None,
) -> list[int]:
    if count <= 0 or not available:
        return []

    selected = []
    remaining = []
    allowed = allowed if allowed is not None else set(available)

    for index in available:
        if len(selected) < count and index in allowed:
            selected.append(index)
        else:
            remaining.append(index)

    available[:] = remaining
    return selected


def assign_splits(df: pd.DataFrame, seed: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    assignments = {}
    summary_rows = []
    group_cols = ["label", "data_origin", "category"]

    for key, group in df.groupby(group_cols, sort=True, dropna=False):
        label, data_origin, category = key
        n = len(group)
        rng = np.random.default_rng(stable_group_seed(seed, key))
        available = rng.permutation(group.index.to_numpy()).tolist()
        fractions = ORIGIN_FRACTIONS[data_origin]
        counts = {split: 0 for split in SPLIT_FILES}

        if n < 5:
            selected_by_split = {"train": available[:]}
            available = []
            small_rule = "all_train"
        elif n < 10:
            val_selected = take_indices(available, 1)
            selected_by_split = {"val": val_selected, "train": available[:]}
            counts["val"] = len(val_selected)
            available = []
            small_rule = "train_val_only"
        else:
            selected_by_split = {}
            small_rule = "full_rule"

            if data_origin == "real":
                count = target_count(n, fractions["test_real"])
                selected_by_split["test_real"] = take_indices(available, count)

            challenge_count = target_count(n, fractions.get("test_challenge", 0.0))
            candidate_indices = set(group[group.apply(is_challenge_candidate, axis=1)].index)
            selected_by_split["test_challenge"] = take_indices(
                available, challenge_count, allowed=candidate_indices
            )

            mixed_count = target_count(n, fractions.get("test_mixed", 0.0))
            selected_by_split["test_mixed"] = take_indices(available, mixed_count)

            val_count = target_count(n, fractions.get("val", 0.0))
            selected_by_split["val"] = take_indices(available, val_count)
            selected_by_split["train"] = available[:]
            available = []

        for split_name, selected_indices in selected_by_split.items():
            counts[split_name] = len(selected_indices)
            for index in selected_indices:
                assignments[index] = split_name

        summary_rows.append(
            {
                "label": label,
                "data_origin": data_origin,
                "category": category,
                "n": n,
                "train": counts.get("train", 0),
                "val": counts.get("val", 0),
                "test_real": counts.get("test_real", 0),
                "test_mixed": counts.get("test_mixed", 0),
                "test_challenge": counts.get("test_challenge", 0),
                "small_stratum_rule": small_rule,
            }
        )

    result = df.copy()
    result["split"] = result.index.map(assignments)
    if result["split"].isna().any():
        raise RuntimeError("Some rows were not assigned to a split.")
    return result, pd.DataFrame(summary_rows)


def value_counts_markdown(df: pd.DataFrame, column: str) -> str:
    if df.empty:
        return "_No rows._"
    counts = df[column].value_counts(dropna=False).rename_axis(column).reset_index(name="count")
    counts["percent"] = (counts["count"] / len(df) * 100).round(2)
    return counts.to_markdown(index=False)


def crosstab_markdown(df: pd.DataFrame, index: str, columns: str) -> str:
    if df.empty:
        return "_No rows._"
    return pd.crosstab(df[index], df[columns]).to_markdown()


def overlap_report(split_frames: dict[str, pd.DataFrame], column: str) -> pd.DataFrame:
    rows = []
    for left, right in combinations(split_frames, 2):
        rows.append(
            {
                "left_split": left,
                "right_split": right,
                f"{column}_overlap": len(
                    set(split_frames[left][column]) & set(split_frames[right][column])
                ),
            }
        )
    return pd.DataFrame(rows)


def write_report(
    report_path: Path,
    source_path: Path,
    seed: int,
    split_frames: dict[str, pd.DataFrame],
    stratum_summary: pd.DataFrame,
) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    split_sizes = pd.DataFrame(
        [{"split": name, "rows": len(frame)} for name, frame in split_frames.items()]
    )
    split_sizes["percent"] = (split_sizes["rows"] / split_sizes["rows"].sum() * 100).round(2)
    small_strata = stratum_summary[stratum_summary["small_stratum_rule"] != "full_rule"].copy()

    lines = [
        "# Distillation Split Report V2",
        "",
        "## 1. Configuration",
        "",
        f"- Input file: `{source_path.as_posix()}`",
        f"- Seed: `{seed}`",
        "- Stratum key: `label x data_origin x category`",
        "- Goal: improve `test_mixed` and `test_challenge` by reducing source-only separation.",
        "- Small stratum rules: `n < 5 -> train`, `5 <= n < 10 -> train/val`, `n >= 10 -> full v2 rule`",
        "",
        "## 2. Split Sizes",
        "",
        split_sizes.to_markdown(index=False),
        "",
        "## 3. Content Overlap Check",
        "",
        overlap_report(split_frames, "content").to_markdown(index=False),
        "",
        "## 4. Sample ID Overlap Check",
        "",
        overlap_report(split_frames, "sample_id").to_markdown(index=False),
        "",
        "## 5. Strata Summary",
        "",
        stratum_summary.sort_values(["data_origin", "label", "category"]).to_markdown(index=False),
        "",
        "## 6. Small Strata",
        "",
        small_strata.sort_values(["n", "data_origin", "label", "category"]).to_markdown(index=False)
        if not small_strata.empty
        else "_No small strata._",
        "",
    ]

    for split_name, frame in split_frames.items():
        lines.extend(
            [
                f"## 7. Split Detail: `{split_name}`",
                "",
                f"Rows: `{len(frame)}`",
                "",
                "### Label Distribution",
                "",
                value_counts_markdown(frame, "label"),
                "",
                "### Data Origin Distribution",
                "",
                value_counts_markdown(frame, "data_origin"),
                "",
                "### Category Distribution",
                "",
                value_counts_markdown(frame, "category"),
                "",
                "### Sender Type Distribution",
                "",
                value_counts_markdown(frame, "sender_type"),
                "",
                "### URL Flag x Label",
                "",
                crosstab_markdown(frame, "has_url", "label"),
                "",
                "### Phone Flag x Label",
                "",
                crosstab_markdown(frame, "has_phone_number", "label"),
                "",
                "### Label x Data Origin",
                "",
                crosstab_markdown(frame, "data_origin", "label"),
                "",
                "### Label x Category",
                "",
                crosstab_markdown(frame, "category", "label"),
                "",
                "### Data Origin x Category",
                "",
                crosstab_markdown(frame, "data_origin", "category"),
                "",
            ]
        )

    report_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    df = pd.read_csv(args.input)
    validate_source(df, args.input)

    df = df.copy()
    for column in ["content", "category", "data_origin", "sender_type", "obfuscation_level"]:
        df[column] = df[column].astype(str).str.strip()

    assigned, stratum_summary = assign_splits(df, args.seed)
    args.split_dir.mkdir(parents=True, exist_ok=True)

    split_frames = {}
    output_columns = REQUIRED_COLUMNS
    for split_name, filename in SPLIT_FILES.items():
        frame = assigned[assigned["split"] == split_name].copy()
        frame = frame.sort_values("sample_id").reset_index(drop=True)
        split_frames[split_name] = frame[output_columns]
        split_frames[split_name].to_csv(args.split_dir / filename, index=False, encoding="utf-8-sig")

    write_report(args.report, args.input, args.seed, split_frames, stratum_summary)

    print(f"[OK] Wrote v2 splits to {args.split_dir}")
    print(f"[OK] Wrote v2 report to {args.report}")
    for split_name, frame in split_frames.items():
        print(f"  - {split_name}: {len(frame)} rows")


if __name__ == "__main__":
    main()

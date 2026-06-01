"""Create controlled splits for offline soft-label distillation.

The split strategy follows docs/offline_soft_label_distillation_codex_guidelines.md:
- source metadata from model/base/temp.csv;
- split by label x data_origin x category;
- keep test_real real-only;
- keep test_challenge for hard/external stress testing;
- avoid content/sample_id overlap across split files.
"""

from __future__ import annotations

import argparse
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd


DEFAULT_INPUT = Path("model/base/temp.csv")
DEFAULT_SPLIT_DIR = Path("data/distillation/splits")
DEFAULT_REPORT = Path("setup_results/distillation/split_report.md")
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

ORIGIN_SPLIT_RULES = {
    "real": {"train": 0.70, "val": 0.15, "test_real": 0.15},
    "synthetic": {"train": 0.80, "val": 0.10, "test_mixed": 0.10},
    "paraphrased": {"train": 0.80, "val": 0.10, "test_mixed": 0.10},
    "synthetic_hard_negative": {"train": 0.70, "val": 0.10, "test_challenge": 0.20},
    "external_curated": {"train": 0.70, "val": 0.10, "test_challenge": 0.20},
    "external_real": {"train": 0.70, "val": 0.10, "test_challenge": 0.20},
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create ViSmishDS distillation splits with category-aware stratification."
    )
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

    empty_category = df["category"].astype(str).str.strip().eq("")
    if empty_category.any():
        raise ValueError(f"Found {int(empty_category.sum())} empty category values.")

    duplicated_content = int(df.duplicated("content").sum())
    duplicated_sample_id = int(df.duplicated("sample_id").sum())
    if duplicated_content or duplicated_sample_id:
        raise ValueError(
            "Duplicates found: "
            f"content={duplicated_content}, sample_id={duplicated_sample_id}"
        )

    unknown_origins = sorted(set(df["data_origin"]) - set(ORIGIN_SPLIT_RULES))
    if unknown_origins:
        raise ValueError(f"Unknown data_origin values: {unknown_origins}")


def stable_group_seed(seed: int, key: tuple[object, object, object]) -> int:
    key_text = "||".join(str(part) for part in key)
    value = seed
    for char in key_text:
        value = (value * 131 + ord(char)) % (2**32 - 1)
    return value


def split_counts(n: int, rules: dict[str, float]) -> dict[str, int]:
    """Return split counts for one stratum.

    Small strata are kept conservative:
    - n < 5: all train;
    - 5 <= n < 10: train/val only;
    - n >= 10: all destinations in the origin-specific rule are allowed.
    """

    counts = {split: 0 for split in rules}
    if n < 5:
        counts["train"] = n
        return counts

    if n < 10:
        val_count = 1 if "val" in rules else 0
        counts["val"] = val_count
        counts["train"] = n - val_count
        return counts

    remaining = n
    non_train_splits = [split for split in rules if split != "train"]

    for split in non_train_splits:
        count = int(round(n * rules[split]))
        count = max(1, count) if rules[split] > 0 else 0
        counts[split] = count
        remaining -= count

    if remaining < 1:
        # Very defensive fallback; current n>=10 rules should not hit this.
        largest_non_train = max(non_train_splits, key=lambda split: counts[split])
        counts[largest_non_train] -= 1
        remaining += 1

    counts["train"] = remaining
    return counts


def assign_splits(df: pd.DataFrame, seed: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    assignments = []
    summary_rows = []

    group_cols = ["label", "data_origin", "category"]
    for key, group in df.groupby(group_cols, sort=True, dropna=False):
        label, data_origin, category = key
        rules = ORIGIN_SPLIT_RULES[data_origin]
        counts = split_counts(len(group), rules)

        rng = np.random.default_rng(stable_group_seed(seed, key))
        shuffled_positions = rng.permutation(group.index.to_numpy())

        cursor = 0
        for split_name, count in counts.items():
            if count <= 0:
                continue
            selected = shuffled_positions[cursor : cursor + count]
            cursor += count
            for index in selected:
                assignments.append({"index": index, "split": split_name})

        summary_rows.append(
            {
                "label": label,
                "data_origin": data_origin,
                "category": category,
                "n": len(group),
                "train": counts.get("train", 0),
                "val": counts.get("val", 0),
                "test_real": counts.get("test_real", 0),
                "test_mixed": counts.get("test_mixed", 0),
                "test_challenge": counts.get("test_challenge", 0),
                "small_stratum_rule": (
                    "all_train" if len(group) < 5 else "train_val_only" if len(group) < 10 else "full_rule"
                ),
            }
        )

    assignment_df = pd.DataFrame(assignments).set_index("index")
    result = df.join(assignment_df, how="left")
    if result["split"].isna().any():
        raise RuntimeError("Some rows were not assigned to a split.")

    summary = pd.DataFrame(summary_rows)
    return result, summary


def crosstab_markdown(df: pd.DataFrame, index: str, columns: str) -> str:
    table = pd.crosstab(df[index], df[columns])
    if table.empty:
        return "_No rows._"
    return table.to_markdown()


def value_counts_markdown(df: pd.DataFrame, column: str) -> str:
    if df.empty:
        return "_No rows._"
    counts = df[column].value_counts(dropna=False).rename_axis(column).reset_index(name="count")
    counts["percent"] = (counts["count"] / len(df) * 100).round(2)
    return counts.to_markdown(index=False)


def overlap_report(split_frames: dict[str, pd.DataFrame], column: str) -> pd.DataFrame:
    rows = []
    for left, right in combinations(split_frames, 2):
        left_values = set(split_frames[left][column])
        right_values = set(split_frames[right][column])
        rows.append(
            {
                "left_split": left,
                "right_split": right,
                f"{column}_overlap": len(left_values & right_values),
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
    content_overlap = overlap_report(split_frames, "content")
    sample_id_overlap = overlap_report(split_frames, "sample_id")

    lines = [
        "# Distillation Split Report",
        "",
        "## 1. Configuration",
        "",
        f"- Input file: `{source_path.as_posix()}`",
        f"- Seed: `{seed}`",
        "- Stratum key: `label x data_origin x category`",
        "- Small stratum rules: `n < 5 -> train`, `5 <= n < 10 -> train/val`, `n >= 10 -> origin rule`",
        "",
        "## 2. Split Sizes",
        "",
        split_sizes.to_markdown(index=False),
        "",
        "## 3. Content Overlap Check",
        "",
        content_overlap.to_markdown(index=False),
        "",
        "## 4. Sample ID Overlap Check",
        "",
        sample_id_overlap.to_markdown(index=False),
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

    # Normalize harmless whitespace while preserving user-visible category names.
    df = df.copy()
    df["content"] = df["content"].astype(str)
    df["category"] = df["category"].astype(str).str.strip()
    df["data_origin"] = df["data_origin"].astype(str).str.strip()
    df["sender_type"] = df["sender_type"].astype(str).str.strip()
    df["obfuscation_level"] = df["obfuscation_level"].astype(str).str.strip()

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

    print(f"[OK] Wrote splits to {args.split_dir}")
    print(f"[OK] Wrote report to {args.report}")
    for split_name, frame in split_frames.items():
        print(f"  - {split_name}: {len(frame)} rows")


if __name__ == "__main__":
    main()

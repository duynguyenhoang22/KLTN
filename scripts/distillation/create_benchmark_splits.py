"""Create benchmark train/dev/test splits from model/base/temp.csv.

Policy:
- real, external_real, external_curated: stratified 70/15/15 into train/dev/test.
- synthetic, paraphrased, synthetic_hard_positive: 100% train.

The stratum key is label x data_origin x category. Very small real strata are
kept in train so that dev/test do not receive single, unstable examples.
"""

from __future__ import annotations

import argparse
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd

from benchmark_config import BENCHMARK_SPLITS, REAL_HOLDOUT_ORIGINS, SUPPORTED_ORIGINS


DEFAULT_INPUT = Path("model/base/temp.csv")
DEFAULT_SPLIT_DIR = Path("data/distillation/benchmark_splits")
DEFAULT_REPORT = Path("setup_results/distillation_benchmark/split_report.md")
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create ViSmishDS benchmark splits.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--split-dir", type=Path, default=DEFAULT_SPLIT_DIR)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    return parser.parse_args()


def validate_source(df: pd.DataFrame, input_path: Path) -> None:
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"{input_path} is missing required columns: {missing}")
    nulls = df[REQUIRED_COLUMNS].isna().sum()
    nulls = nulls[nulls > 0]
    if not nulls.empty:
        raise ValueError(f"Missing values found:\n{nulls.to_string()}")
    duplicates = {
        "sample_id": int(df.duplicated("sample_id").sum()),
        "content": int(df.duplicated("content").sum()),
    }
    if duplicates["sample_id"] or duplicates["content"]:
        raise ValueError(f"Duplicates found: {duplicates}")
    unknown = sorted(set(df["data_origin"].astype(str)) - SUPPORTED_ORIGINS)
    if unknown:
        raise ValueError(f"Unknown data_origin values: {unknown}")


def stable_group_seed(seed: int, key: tuple[object, ...]) -> int:
    value = seed
    for char in "||".join(str(part) for part in key):
        value = (value * 131 + ord(char)) % (2**32 - 1)
    return value


def real_counts(n: int) -> tuple[int, int, int, str]:
    if n < 5:
        return n, 0, 0, "small_all_train"
    if n < 10:
        return n - 1, 1, 0, "small_train_dev"
    dev = max(1, int(round(n * 0.15)))
    test = max(1, int(round(n * 0.15)))
    train = n - dev - test
    if train < 1:
        train += 1
        if test >= dev and test > 0:
            test -= 1
        else:
            dev -= 1
    return train, dev, test, "real_70_15_15"


def assign_splits(df: pd.DataFrame, seed: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    assignments = {}
    summary = []
    group_cols = ["label", "data_origin", "category"]
    for key, group in df.groupby(group_cols, sort=True, dropna=False):
        label, origin, category = key
        rng = np.random.default_rng(stable_group_seed(seed, key))
        shuffled = rng.permutation(group.index.to_numpy()).tolist()
        if origin in REAL_HOLDOUT_ORIGINS:
            train_n, dev_n, test_n, rule = real_counts(len(group))
            selected = {
                "train": shuffled[:train_n],
                "dev": shuffled[train_n : train_n + dev_n],
                "test": shuffled[train_n + dev_n : train_n + dev_n + test_n],
            }
        else:
            selected = {"train": shuffled, "dev": [], "test": []}
            rule = "train_only_origin"
        for split, indices in selected.items():
            for idx in indices:
                assignments[idx] = split
        summary.append(
            {
                "label": label,
                "data_origin": origin,
                "category": category,
                "n": len(group),
                "train": len(selected["train"]),
                "dev": len(selected["dev"]),
                "test": len(selected["test"]),
                "rule": rule,
            }
        )
    out = df.copy()
    out["split"] = out.index.map(assignments)
    if out["split"].isna().any():
        raise RuntimeError("Some rows were not assigned to a split.")
    return out, pd.DataFrame(summary)


def value_counts_markdown(df: pd.DataFrame, column: str) -> str:
    counts = df[column].value_counts(dropna=False).rename_axis(column).reset_index(name="count")
    counts["percent"] = (counts["count"] / len(df) * 100).round(2)
    return counts.to_markdown(index=False)


def overlap_report(frames: dict[str, pd.DataFrame], column: str) -> pd.DataFrame:
    rows = []
    for left, right in combinations(frames, 2):
        rows.append(
            {
                "left_split": left,
                "right_split": right,
                f"{column}_overlap": len(set(frames[left][column]) & set(frames[right][column])),
            }
        )
    return pd.DataFrame(rows)


def write_report(
    report_path: Path,
    source_path: Path,
    seed: int,
    frames: dict[str, pd.DataFrame],
    summary: pd.DataFrame,
) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    sizes = pd.DataFrame([{"split": name, "rows": len(frame)} for name, frame in frames.items()])
    sizes["percent"] = (sizes["rows"] / sizes["rows"].sum() * 100).round(2)
    lines = [
        "# Distillation Benchmark Split Report",
        "",
        "## Policy",
        "",
        f"- Input file: `{source_path.as_posix()}`",
        f"- Seed: `{seed}`",
        "- Real-like origins `real`, `external_real`, `external_curated`: stratified 70/15/15.",
        "- Train-only origins `synthetic`, `paraphrased`, `synthetic_hard_positive`: 100% train.",
        "- Stratum key: `label x data_origin x category`.",
        "",
        "## Split Sizes",
        "",
        sizes.to_markdown(index=False),
        "",
        "## Content Overlap",
        "",
        overlap_report(frames, "content").to_markdown(index=False),
        "",
        "## Sample ID Overlap",
        "",
        overlap_report(frames, "sample_id").to_markdown(index=False),
        "",
        "## Strata Summary",
        "",
        summary.sort_values(["data_origin", "label", "category"]).to_markdown(index=False),
        "",
    ]
    for split, frame in frames.items():
        lines.extend(
            [
                f"## Split Detail: `{split}`",
                "",
                f"Rows: `{len(frame)}`",
                "",
                "### Label",
                "",
                value_counts_markdown(frame, "label"),
                "",
                "### Data Origin",
                "",
                value_counts_markdown(frame, "data_origin"),
                "",
                "### Category",
                "",
                value_counts_markdown(frame, "category"),
                "",
                "### Label x Data Origin",
                "",
                pd.crosstab(frame["data_origin"], frame["label"]).to_markdown(),
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
    assigned, summary = assign_splits(df, args.seed)
    args.split_dir.mkdir(parents=True, exist_ok=True)
    frames = {}
    for split, filename in BENCHMARK_SPLITS.items():
        frame = assigned[assigned["split"] == split].sort_values("sample_id").reset_index(drop=True)
        frames[split] = frame[REQUIRED_COLUMNS]
        frames[split].to_csv(args.split_dir / filename, index=False, encoding="utf-8-sig")
    write_report(args.report, args.input, args.seed, frames, summary)
    print(f"[OK] Wrote benchmark splits to {args.split_dir}")
    print(f"[OK] Wrote split report to {args.report}")
    for split, frame in frames.items():
        print(f"  - {split}: {len(frame)} rows")


if __name__ == "__main__":
    main()

"""Aggregate benchmark metrics from char-level and PLM runs."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from benchmark_config import PRIMARY_METRICS
from benchmark_metrics import markdown_metrics_table


DEFAULT_RESULTS_ROOT = Path("setup_results/distillation_benchmark")
DEFAULT_OUTPUT_DIR = Path("setup_results/distillation_benchmark/summary")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Aggregate distillation benchmark metrics.")
    parser.add_argument("--results-root", type=Path, default=DEFAULT_RESULTS_ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--include-train", action="store_true")
    return parser.parse_args()


def find_metrics_files(results_root: Path) -> list[Path]:
    return sorted(
        path
        for path in results_root.rglob("*_metrics_by_split.csv")
        if "summary" not in path.parts and path.is_file()
    )


def load_metrics(paths: list[Path]) -> pd.DataFrame:
    frames = []
    for path in paths:
        df = pd.read_csv(path)
        df["metrics_file"] = str(path)
        frames.append(df)
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True)


def pivot_dev_test(df: pd.DataFrame) -> pd.DataFrame:
    id_cols = ["model_group", "model_name", "run_name"]
    present_id_cols = [col for col in id_cols if col in df.columns]
    value_cols = ["rows", *PRIMARY_METRICS, "tn", "fp", "fn", "tp"]
    present_value_cols = [col for col in value_cols if col in df.columns]
    wide = df.pivot_table(
        index=present_id_cols,
        columns="split",
        values=present_value_cols,
        aggfunc="first",
    )
    wide.columns = [f"{split}_{metric}" for metric, split in wide.columns]
    return wide.reset_index()


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    paths = find_metrics_files(args.results_root)
    df = load_metrics(paths)
    if df.empty:
        raise FileNotFoundError(f"No *_metrics_by_split.csv files found under {args.results_root}")
    if not args.include_train:
        df = df[df["split"].isin(["dev", "test"])].copy()
    df = df.sort_values(["model_group", "model_name", "split"], na_position="last")
    wide = pivot_dev_test(df)

    long_csv = args.output_dir / "benchmark_metrics_long.csv"
    wide_csv = args.output_dir / "benchmark_metrics_dev_test_wide.csv"
    report_path = args.output_dir / "benchmark_report.md"
    df.to_csv(long_csv, index=False)
    wide.to_csv(wide_csv, index=False)

    lines = [
        "# Distillation Benchmark Summary",
        "",
        "## Primary Metrics",
        "",
        "- `macro_f1`: main balanced quality measure across both labels.",
        "- `f1_label_1`: smishing-class F1.",
        "- `recall_label_1`: missed-smishing control metric.",
        "- `pr_auc`: threshold-independent ranking metric for imbalanced binary detection.",
        "",
        "## Dev/Test Results",
        "",
        markdown_metrics_table(df),
        "",
        "## Output Files",
        "",
        f"- Long table: `{long_csv.as_posix()}`",
        f"- Dev/test wide table: `{wide_csv.as_posix()}`",
        "",
    ]
    report_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"[OK] Wrote {long_csv}")
    print(f"[OK] Wrote {wide_csv}")
    print(f"[OK] Wrote {report_path}")


if __name__ == "__main__":
    main()

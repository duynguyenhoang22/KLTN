"""Aggregate benchmark metrics from char-level, PLM, and LLM runs."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from benchmark_config import PLM_REGISTRY, PRIMARY_METRICS
from benchmark_metrics import markdown_metrics_table


DEFAULT_RESULTS_ROOT = Path("setup_results/distillation_benchmark")
DEFAULT_OUTPUT_DIR = Path("setup_results/distillation_benchmark/summary")

LLM_RUNS = {
    "Gemma_3_1b": "Gemma 3 1B",
    "Gemma_2b": "Gemma 2B",
    "Qwen3_0_6B": "Qwen3 0.6B",
    "Qwen2_5_0_5B": "Qwen2.5 0.5B",
}


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
        required = {
            "model_group",
            "model_name",
            "run_name",
            "split",
            "rows",
            *PRIMARY_METRICS,
        }
        missing = required - set(df.columns)
        if missing:
            raise ValueError(f"{path} is missing required columns: {sorted(missing)}")
        df["metrics_file"] = str(path)
        frames.append(df)
    if not frames:
        return pd.DataFrame()
    out = pd.concat(frames, ignore_index=True)
    llm_mask = out["run_name"].isin(LLM_RUNS)
    out.loc[llm_mask, "model_group"] = "fine_tuned_llm"
    out.loc[llm_mask, "model_name"] = out.loc[llm_mask, "run_name"].map(LLM_RUNS)
    duplicates = out.duplicated(["run_name", "split"], keep=False)
    if duplicates.any():
        duplicate_rows = out.loc[duplicates, ["run_name", "split", "metrics_file"]]
        raise ValueError(
            "Duplicate benchmark metrics found for the same run and split:\n"
            + duplicate_rows.to_string(index=False)
        )
    return out


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


def missing_configured_plms(df: pd.DataFrame) -> list[str]:
    observed = set(df.loc[df["model_group"].eq("fine_tuned_plm"), "run_name"].dropna())
    missing = []
    for key, spec in PLM_REGISTRY.items():
        if not spec.include_in_benchmark_suite:
            continue
        run_name = f"plm_{key}"
        if run_name not in observed:
            missing.append(f"- `{run_name}` ({spec.display_name})")
    return missing


def missing_configured_llms(df: pd.DataFrame) -> list[str]:
    observed = set(df.loc[df["model_group"].eq("fine_tuned_llm"), "run_name"].dropna())
    return [
        f"- `{run_name}` ({display_name})"
        for run_name, display_name in LLM_RUNS.items()
        if run_name not in observed
    ]


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
    missing_plms = missing_configured_plms(df)
    missing_llms = missing_configured_llms(df)

    long_csv = args.output_dir / "benchmark_metrics_long.csv"
    wide_csv = args.output_dir / "benchmark_metrics_dev_test_wide.csv"
    report_path = args.output_dir / "benchmark_report.md"
    df.to_csv(long_csv, index=False)
    wide.to_csv(wide_csv, index=False)

    lines = [
        "# Model Benchmark Summary",
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
        "## Configured PLMs Without Metrics Yet",
        "",
        *(missing_plms if missing_plms else ["- None"]),
        "",
        "## Configured LLMs Without Metrics Yet",
        "",
        *(missing_llms if missing_llms else ["- None"]),
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

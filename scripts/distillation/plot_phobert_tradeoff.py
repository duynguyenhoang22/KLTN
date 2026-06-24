"""Plot representative quality-efficiency trade-offs for PhoBERT-base KD study."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


DEFAULT_INPUT = Path(
    "setup_results/textcnn_distillation_study/phobert-base/deployment/deployment_feasibility_test.csv"
)
DEFAULT_OUTPUT_DIR = Path("setup_results/textcnn_distillation_study/phobert-base/deployment")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Plot PhoBERT-base deployment trade-offs.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args()


def model_style(model: str) -> tuple[str, str]:
    if model == "PhoBERT-base":
        return "#334155", "o"
    if "risk-aware" in model:
        return "#0f766e", "s"
    if "vanilla" in model:
        return "#b45309", "^"
    return "#2563eb", "D"


def annotate_points(ax: plt.Axes, df: pd.DataFrame, x_col: str) -> None:
    for _, row in df.iterrows():
        label = row["model"].replace("TextCNN ", "")
        ax.annotate(
            label,
            (row[x_col], row["f1_label_1"]),
            xytext=(6, 4),
            textcoords="offset points",
            fontsize=9,
        )


def plot_size_tradeoff(df: pd.DataFrame, output_dir: Path) -> Path:
    fig, ax = plt.subplots(figsize=(8.2, 5.2))
    for _, row in df.iterrows():
        color, marker = model_style(row["model"])
        ax.scatter(
            row["size_mb"],
            row["f1_label_1"],
            s=90,
            color=color,
            marker=marker,
            edgecolor="white",
            linewidth=0.8,
            zorder=3,
        )
    annotate_points(ax, df, "size_mb")
    ax.set_xscale("log")
    ax.set_xlabel("Model size (MB, log scale)")
    ax.set_ylabel("F1 label 1 on test")
    ax.set_title("Quality-size trade-off: PhoBERT-base teacher vs TextCNN students")
    ax.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.35)
    ax.set_ylim(max(0.0, df["f1_label_1"].min() - 0.04), min(1.0, df["f1_label_1"].max() + 0.04))
    fig.tight_layout()
    path = output_dir / "phobert_quality_size_tradeoff.png"
    fig.savefig(path, dpi=220)
    plt.close(fig)
    return path


def plot_latency_tradeoff(df: pd.DataFrame, output_dir: Path) -> Path:
    measured = df[df["cpu_latency_ms_per_msg"].notna()].copy()
    if measured.empty:
        raise ValueError("No latency measurements available.")
    fig, ax = plt.subplots(figsize=(8.2, 5.2))
    for _, row in measured.iterrows():
        color, marker = model_style(row["model"])
        ax.scatter(
            row["cpu_latency_ms_per_msg"],
            row["f1_label_1"],
            s=90,
            color=color,
            marker=marker,
            edgecolor="white",
            linewidth=0.8,
            zorder=3,
        )
    annotate_points(ax, measured, "cpu_latency_ms_per_msg")
    ax.set_xlabel("CPU latency (ms/SMS)")
    ax.set_ylabel("F1 label 1 on test")
    ax.set_title("Quality-latency trade-off among measured TextCNN students")
    ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.35)
    ax.set_ylim(
        max(0.0, measured["f1_label_1"].min() - 0.04),
        min(1.0, measured["f1_label_1"].max() + 0.04),
    )
    fig.tight_layout()
    path = output_dir / "phobert_textcnn_quality_latency_tradeoff.png"
    fig.savefig(path, dpi=220)
    plt.close(fig)
    return path


def write_summary(df: pd.DataFrame, output_dir: Path) -> Path:
    summary = df.copy()
    summary["latency_note"] = summary["cpu_latency_ms_per_msg"].apply(
        lambda value: "not measured" if pd.isna(value) else "measured on CPU"
    )
    path = output_dir / "phobert_tradeoff_plot_data.csv"
    summary.to_csv(path, index=False)
    return path


def main() -> None:
    args = parse_args()
    if not args.input.exists():
        raise FileNotFoundError(f"Missing deployment CSV: {args.input}")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(args.input)
    required = {"model", "size_mb", "cpu_latency_ms_per_msg", "f1_label_1"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"{args.input} missing columns: {sorted(missing)}")

    data_path = write_summary(df, args.output_dir)
    size_path = plot_size_tradeoff(df, args.output_dir)
    latency_path = plot_latency_tradeoff(df, args.output_dir)
    print(f"[OK] Wrote {data_path}")
    print(f"[OK] Wrote {size_path}")
    print(f"[OK] Wrote {latency_path}")


if __name__ == "__main__":
    main()

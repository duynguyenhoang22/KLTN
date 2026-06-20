"""Plot the RQ1 quality–deployment-cost trade-off.

The chart reads the deployment benchmark on the dev split and writes all
artifacts next to this script so it can be regenerated independently.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FuncFormatter


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_DIR = Path(__file__).resolve().parent
INPUT_CSV = (
    PROJECT_ROOT
    / "setup_results"
    / "distillation_benchmark"
    / "deployment_feasibility"
    / "deployment_feasibility_dev.csv"
)
OUTPUT_PNG = SCRIPT_DIR / "rq1_quality_deployment_tradeoff.png"
OUTPUT_PDF = SCRIPT_DIR / "rq1_quality_deployment_tradeoff.pdf"
OUTPUT_DATA = SCRIPT_DIR / "rq1_quality_deployment_tradeoff_data.csv"

MODEL_ORDER = ["PhoBERT-base", "BiLSTM distilled", "TextCNN Distilled"]
COLORS = {
    "PhoBERT-base": "#E76F51",
    "BiLSTM distilled": "#457B9D",
    "TextCNN Distilled": "#2A9D8F",
}
MARKERS = {
    "PhoBERT-base": "s",
    "BiLSTM distilled": "o",
    "TextCNN Distilled": "D",
}
LABEL_OFFSETS = {
    "PhoBERT-base": (-8, 10),
    "BiLSTM distilled": (10, -20),
    "TextCNN Distilled": (10, 10),
}


def load_data() -> pd.DataFrame:
    if not INPUT_CSV.exists():
        raise FileNotFoundError(f"Missing deployment benchmark: {INPUT_CSV}")

    df = pd.read_csv(INPUT_CSV)
    required = {
        "model",
        "params",
        "size_mb",
        "cpu_latency_ms_per_msg",
        "peak_ram_mb",
        "f1_label_1",
        "status",
    }
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"{INPUT_CSV} is missing columns: {sorted(missing)}")

    df = df[df["model"].isin(MODEL_ORDER)].copy()
    df = df[df["status"].eq("ok")].copy()
    if set(df["model"]) != set(MODEL_ORDER):
        missing_models = sorted(set(MODEL_ORDER) - set(df["model"]))
        raise ValueError(f"Missing successful model results: {missing_models}")

    df["model"] = pd.Categorical(df["model"], categories=MODEL_ORDER, ordered=True)
    df = df.sort_values("model").reset_index(drop=True)
    df["params_million"] = df["params"] / 1_000_000
    return df


def format_params(params: float) -> str:
    if params >= 1_000_000:
        return f"{params / 1_000_000:.1f}M params"
    return f"{params / 1_000:.1f}K params"


def plot(df: pd.DataFrame) -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 10.5,
            "axes.titlesize": 14,
            "axes.labelsize": 11.5,
        }
    )
    fig, ax = plt.subplots(figsize=(9.2, 5.6), constrained_layout=True)

    # Bubble area encodes peak RAM. A non-zero base keeps student points legible.
    bubble_sizes = 180 + 0.34 * df["peak_ram_mb"]

    for (_, row), bubble_size in zip(df.iterrows(), bubble_sizes):
        model = str(row["model"])
        ax.scatter(
            row["cpu_latency_ms_per_msg"],
            row["f1_label_1"],
            s=bubble_size,
            color=COLORS[model],
            marker=MARKERS[model],
            edgecolor="white",
            linewidth=1.6,
            alpha=0.94,
            zorder=3,
        )
        offset = LABEL_OFFSETS[model]
        annotation = (
            f"{model}\n"
            f"{row['cpu_latency_ms_per_msg']:.2f} ms · "
            f"F1={row['f1_label_1']:.4f}\n"
            f"{format_params(row['params'])} · {row['size_mb']:.2f} MB"
        )
        ax.annotate(
            annotation,
            (row["cpu_latency_ms_per_msg"], row["f1_label_1"]),
            xytext=offset,
            textcoords="offset points",
            ha="left" if offset[0] > 0 else "right",
            va="bottom" if offset[1] >= 0 else "top",
            fontsize=9.2,
            linespacing=1.25,
        )

    ax.set_xscale("log")
    ax.set_xlabel("Độ trễ CPU trên mỗi tin nhắn (ms, thang logarithm)")
    ax.set_ylabel("F1 Label 1 trên tập dev")
    ax.set_title("Đánh đổi giữa chất lượng và chi phí triển khai")
    ax.grid(True, which="major", linestyle="--", linewidth=0.8, alpha=0.38)
    ax.grid(True, which="minor", axis="x", linestyle=":", linewidth=0.6, alpha=0.25)
    ax.set_ylim(0.74, 0.86)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value:g}"))

    ax.text(
        0.015,
        0.025,
        "Diện tích điểm biểu diễn mức sử dụng RAM cực đại",
        transform=ax.transAxes,
        fontsize=9,
        color="#555555",
    )

    fig.savefig(OUTPUT_PNG, dpi=300, bbox_inches="tight")
    fig.savefig(OUTPUT_PDF, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    df = load_data()
    df.to_csv(OUTPUT_DATA, index=False, encoding="utf-8-sig")
    plot(df)
    print(f"[OK] Wrote {OUTPUT_PNG}")
    print(f"[OK] Wrote {OUTPUT_PDF}")
    print(f"[OK] Wrote {OUTPUT_DATA}")


if __name__ == "__main__":
    main()

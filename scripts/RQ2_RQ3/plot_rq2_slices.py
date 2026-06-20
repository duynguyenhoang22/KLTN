"""Plot representative RQ2 slices: message length and URL presence."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


SCRIPT_DIR = Path(__file__).resolve().parent
INPUT_CSV = SCRIPT_DIR / "rq2_slice_metrics_dev.csv"

MODEL_ORDER = [
    "CafeBERT",
    "DistilBERT multilingual",
    "TextCNN",
    "TextCNN distilled",
]
COLORS = {
    "CafeBERT": "#2A9D8F",
    "DistilBERT multilingual": "#E9C46A",
    "TextCNN": "#457B9D",
    "TextCNN distilled": "#E76F51",
}


def load_data() -> pd.DataFrame:
    if not INPUT_CSV.exists():
        raise FileNotFoundError(INPUT_CSV)
    df = pd.read_csv(INPUT_CSV)
    required = {
        "model",
        "slice",
        "group",
        "label_1",
        "f1_label_1",
        "recall_label_1",
    }
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"{INPUT_CSV} missing columns: {sorted(missing)}")
    return df


def grouped_bars(
    ax: plt.Axes,
    df: pd.DataFrame,
    groups: list[str],
    metric: str,
    title: str,
    xlabels: list[str],
) -> None:
    x = np.arange(len(groups))
    width = 0.19
    offsets = (np.arange(len(MODEL_ORDER)) - (len(MODEL_ORDER) - 1) / 2) * width

    for offset, model in zip(offsets, MODEL_ORDER):
        model_df = df[df["model"].eq(model)].set_index("group")
        values = [model_df.loc[group, metric] for group in groups]
        bars = ax.bar(
            x + offset,
            values,
            width=width,
            color=COLORS[model],
            edgecolor="white",
            linewidth=0.8,
            label=model,
            zorder=3,
        )
        for bar, value in zip(bars, values):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                value + 0.008,
                f"{value:.2f}",
                ha="center",
                va="bottom",
                fontsize=7.5,
                rotation=90,
            )

    ax.set_title(title, fontweight="semibold")
    ax.set_xticks(x, xlabels)
    ax.set_ylim(0.55, 1.055)
    ax.set_ylabel("Điểm số")
    ax.grid(axis="y", linestyle="--", alpha=0.32, zorder=0)


def save_length_plot(df: pd.DataFrame) -> None:
    subset = df[df["slice"].eq("length_group")].copy()
    groups = ["81–160", "161–240", ">240"]
    label_counts = (
        subset.drop_duplicates("group").set_index("group")["label_1"].astype(int)
    )
    xlabels = [f"{group}\n(n₁={label_counts[group]})" for group in groups]

    fig, axes = plt.subplots(1, 2, figsize=(12.2, 5.2), sharey=True)
    grouped_bars(
        axes[0],
        subset,
        groups,
        "f1_label_1",
        "F1 Label 1 theo độ dài",
        xlabels,
    )
    grouped_bars(
        axes[1],
        subset,
        groups,
        "recall_label_1",
        "Recall Label 1 theo độ dài",
        xlabels,
    )
    axes[0].set_xlabel("Độ dài tin nhắn (ký tự)")
    axes[1].set_xlabel("Độ dài tin nhắn (ký tự)")
    axes[1].set_ylabel("")

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(
        handles,
        labels,
        loc="upper center",
        ncol=4,
        frameon=False,
        bbox_to_anchor=(0.5, 1.01),
    )
    fig.suptitle(
        "Hiệu năng theo độ dài tin nhắn trên tập dev",
        fontsize=15,
        fontweight="bold",
        y=1.08,
    )
    fig.text(
        0.5,
        -0.015,
        "Nhóm ≤80 ký tự không được so sánh do chỉ có 2 mẫu Label 1.",
        ha="center",
        fontsize=9.5,
        color="#555555",
    )
    fig.tight_layout(rect=(0, 0.035, 1, 0.92))
    fig.savefig(
        SCRIPT_DIR / "rq2_performance_by_length.png",
        dpi=300,
        bbox_inches="tight",
    )
    fig.savefig(
        SCRIPT_DIR / "rq2_performance_by_length.pdf",
        bbox_inches="tight",
    )
    plt.close(fig)


def save_url_plot(df: pd.DataFrame) -> None:
    subset = df[df["slice"].eq("has_url")].copy()
    subset["group"] = subset["group"].astype(str)
    groups = ["0", "1"]
    label_counts = (
        subset.drop_duplicates("group").set_index("group")["label_1"].astype(int)
    )
    xlabels = [
        f"Không có URL\n(n₁={label_counts['0']})",
        f"Có URL\n(n₁={label_counts['1']})",
    ]

    fig, axes = plt.subplots(1, 2, figsize=(10.6, 5.2), sharey=True)
    grouped_bars(
        axes[0],
        subset,
        groups,
        "f1_label_1",
        "F1 Label 1 theo tín hiệu URL",
        xlabels,
    )
    grouped_bars(
        axes[1],
        subset,
        groups,
        "recall_label_1",
        "Recall Label 1 theo tín hiệu URL",
        xlabels,
    )
    axes[0].set_xlabel("Sự xuất hiện của URL")
    axes[1].set_xlabel("Sự xuất hiện của URL")
    axes[1].set_ylabel("")

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(
        handles,
        labels,
        loc="upper center",
        ncol=4,
        frameon=False,
        bbox_to_anchor=(0.5, 1.01),
    )
    fig.suptitle(
        "Hiệu năng theo tín hiệu URL trên tập dev",
        fontsize=15,
        fontweight="bold",
        y=1.08,
    )
    fig.tight_layout(rect=(0, 0.02, 1, 0.92))
    fig.savefig(
        SCRIPT_DIR / "rq2_performance_by_url.png",
        dpi=300,
        bbox_inches="tight",
    )
    fig.savefig(
        SCRIPT_DIR / "rq2_performance_by_url.pdf",
        bbox_inches="tight",
    )
    plt.close(fig)


def main() -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 10,
            "axes.titlesize": 12,
            "axes.labelsize": 10.5,
        }
    )
    df = load_data()
    save_length_plot(df)
    save_url_plot(df)
    print(f"[OK] Wrote RQ2 plots to {SCRIPT_DIR}")


if __name__ == "__main__":
    main()

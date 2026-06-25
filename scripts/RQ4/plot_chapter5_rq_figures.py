from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "thesis" / "figures"


MODEL_LABELS = ["CafeBERT", "DistilBERT\nmult.", "TextCNN", "TextCNN\nKD"]


def style() -> None:
    sns.set_theme(style="whitegrid", context="paper", font_scale=1.15)
    plt.rcParams.update(
        {
            "figure.dpi": 160,
            "savefig.dpi": 220,
            "font.family": "DejaVu Sans",
            "axes.titleweight": "bold",
            "axes.labelcolor": "#1f2937",
            "xtick.color": "#1f2937",
            "ytick.color": "#1f2937",
        }
    )


def save(fig: plt.Figure, filename: str) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / filename
    fig.savefig(path, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(path)


def plot_rq2_slice_recall() -> None:
    rows = [
        ("Length 81-160", 0.8824, 1.0000, 0.7647, 0.7647),
        ("Length 161-240", 0.8750, 1.0000, 0.7500, 0.8750),
        ("Length >240", 0.8000, 0.8000, 0.9000, 0.9000),
        ("Has URL", 0.8621, 1.0000, 0.8621, 0.8966),
        ("No URL", 0.8750, 0.7500, 0.6250, 0.6250),
        ("Click link", 0.8462, 1.0000, 0.8462, 0.8846),
        ("Call phone", 0.5000, 0.7500, 0.7500, 0.7500),
        ("Debt collection", 0.7500, 0.5000, 0.7500, 0.7500),
        ("Fear tactic", 0.3333, 0.6667, 0.3333, 0.3333),
        ("Threat tactic", 0.8333, 0.6667, 0.6667, 0.8333),
    ]
    data = pd.DataFrame(rows, columns=["Slice", *MODEL_LABELS]).set_index("Slice")

    fig, ax = plt.subplots(figsize=(9.5, 6.6))
    sns.heatmap(
        data,
        ax=ax,
        cmap=sns.color_palette("YlGnBu", as_cmap=True),
        vmin=0.3,
        vmax=1.0,
        annot=True,
        fmt=".2f",
        linewidths=0.8,
        linecolor="white",
        cbar_kws={"label": "Recall Label 1"},
    )
    ax.set_title("RQ2: Recall Label 1 thay đổi theo lát cắt dữ liệu")
    ax.set_xlabel("Mô hình")
    ax.set_ylabel("Lát cắt dữ liệu")
    ax.tick_params(axis="x", rotation=0)
    ax.tick_params(axis="y", rotation=0)

    ax.text(
        0.0,
        -0.17,
        "Insight: URL/click-link dễ hơn; no-URL, debt/fear và long SMS tạo các điểm yếu khác nhau giữa PLM và TextCNN.",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=10.5,
        color="#374151",
    )
    save(fig, "chapter5_rq2_slice_recall_heatmap.png")


def plot_rq3_error_overview() -> None:
    models = ["CafeBERT", "DistilBERT\nmult.", "TextCNN", "TextCNN\nKD"]
    fp = np.array([2, 7, 4, 6])
    fn = np.array([5, 2, 7, 6])
    high_conf = np.array([5, 8, 7, 5])
    jaccard = pd.DataFrame(
        [
            [1.0000, 0.1429, 0.2857, 0.2667],
            [0.1429, 1.0000, 0.1765, 0.1667],
            [0.2857, 0.1765, 1.0000, 0.7692],
            [0.2667, 0.1667, 0.7692, 1.0000],
        ],
        index=models,
        columns=models,
    )

    fig, axes = plt.subplots(
        1,
        2,
        figsize=(12.8, 5.2),
        gridspec_kw={"width_ratios": [1.1, 1.05]},
        constrained_layout=True,
    )

    x = np.arange(len(models))
    axes[0].bar(x, fp, color="#ef4444", label="FP")
    axes[0].bar(x, fn, bottom=fp, color="#f59e0b", label="FN")
    axes[0].plot(x, high_conf, color="#111827", marker="o", linewidth=2.0, label="Lỗi conf. ≥ 0,9")
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(models)
    axes[0].set_ylabel("Số lỗi trên dev")
    axes[0].set_title("Cấu trúc FP/FN và lỗi tự tin cao")
    axes[0].legend(frameon=True, loc="upper left")
    axes[0].set_ylim(0, 13)
    for idx, total in enumerate(fp + fn):
        axes[0].text(idx, total + 0.35, str(total), ha="center", va="bottom", fontsize=10)

    sns.heatmap(
        jaccard,
        ax=axes[1],
        cmap=sns.color_palette("rocket_r", as_cmap=True),
        vmin=0.0,
        vmax=1.0,
        annot=True,
        fmt=".2f",
        linewidths=0.8,
        linecolor="white",
        cbar_kws={"label": "Jaccard"},
    )
    axes[1].set_title("Giao thoa tập lỗi giữa các mô hình")
    axes[1].tick_params(axis="x", rotation=0)
    axes[1].tick_params(axis="y", rotation=0)

    fig.suptitle("RQ3: Lỗi không chỉ nhiều ít, mà còn khác kiểu giữa các mô hình", y=1.04, fontweight="bold")
    fig.text(
        0.01,
        -0.04,
        "Insight: CafeBERT và DistilBERT có tập lỗi ít giao nhau, trong khi TextCNN và TextCNN KD gần như lặp lại cùng vùng thất bại.",
        ha="left",
        va="top",
        fontsize=10.5,
        color="#374151",
    )
    save(fig, "chapter5_rq3_error_profile_jaccard.png")


def _read_bootstrap(path: Path, teacher: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df = df[(df["split"] == "test") & (df["metric"] == "recall_label_1")].copy()
    df["teacher"] = teacher
    df["mode"] = df["comparison"].str.replace(" - hard", "", regex=False)
    return df


def plot_rq4_kd_delta() -> None:
    files = [
        (
            "PhoBERT-base",
            ROOT / "setup_results" / "textcnn_distillation_study" / "phobert-base" / "summary" / "textcnn_kd_paired_bootstrap.csv",
        ),
        (
            "CafeBERT",
            ROOT
            / "setup_results"
            / "distillation_benchmark"
            / "cafebert_textcnn_distillation_study"
            / "textcnn_distillation_study"
            / "cafebert"
            / "summary"
            / "textcnn_kd_paired_bootstrap.csv",
        ),
        (
            "ViCLSR",
            ROOT
            / "setup_results"
            / "distillation_benchmark"
            / "viclsr_textcnn_distillation_study"
            / "textcnn_distillation_study"
            / "viclsr"
            / "summary"
            / "textcnn_kd_paired_bootstrap.csv",
        ),
    ]
    df = pd.concat([_read_bootstrap(path, teacher) for teacher, path in files], ignore_index=True)
    df["label"] = df["teacher"] + "\n" + df["mode"].map({"vanilla_kd": "Vanilla KD", "risk_aware_kd": "Risk-aware KD"})
    df["err_low"] = df["mean_delta"] - df["ci95_low"]
    df["err_high"] = df["ci95_high"] - df["mean_delta"]
    colors = df["mean_delta"].map(lambda v: "#2563eb" if v >= 0 else "#dc2626")

    fig, ax = plt.subplots(figsize=(10.2, 5.6))
    y = np.arange(len(df))
    ax.barh(y, df["mean_delta"], color=colors, alpha=0.9)
    ax.errorbar(
        df["mean_delta"],
        y,
        xerr=np.vstack([df["err_low"], df["err_high"]]),
        fmt="none",
        ecolor="#111827",
        elinewidth=1.4,
        capsize=4,
    )
    ax.axvline(0, color="#111827", linewidth=1.0)
    ax.set_yticks(y)
    ax.set_yticklabels(df["label"])
    ax.invert_yaxis()
    ax.set_xlabel("Delta Recall Label 1 trên test so với TextCNN hard")
    ax.set_title("RQ4: Distillation gain phụ thuộc teacher và cách dùng soft label")
    ax.set_xlim(-0.18, 0.18)
    for yi, value in enumerate(df["mean_delta"]):
        if abs(value) >= 0.035:
            ax.text(value / 2, yi, f"{value:+.3f}", ha="center", va="center", fontsize=10, color="white")
        else:
            ha = "left" if value >= 0 else "right"
            offset = 0.008 if value >= 0 else -0.008
            ax.text(value + offset, yi, f"{value:+.3f}", ha=ha, va="center", fontsize=10, color="#111827")

    ax.text(
        0.0,
        -0.17,
        "Insight: PhoBERT-base cần risk-aware KD để tăng recall; CafeBERT hợp vanilla KD; ViCLSR làm giảm recall ở cả hai chế độ.",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=10.5,
        color="#374151",
    )
    save(fig, "chapter5_rq4_kd_recall_delta.png")


def main() -> None:
    style()
    plot_rq2_slice_recall()
    plot_rq3_error_overview()
    plot_rq4_kd_delta()


if __name__ == "__main__":
    main()

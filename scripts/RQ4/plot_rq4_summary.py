"""Create a compact, slide-ready summary of the main RQ4 comparisons."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "setup_results"
OUTPUT_DIR = Path(__file__).resolve().parent


def read_summary(path, variant=None):
    df = pd.read_csv(path)
    if variant is not None:
        df = df[df["variant"] == variant]
    return {
        row["metric"]: (float(row["mean"]), float(row["std"]))
        for _, row in df.iterrows()
    }


def metric(summary, name):
    return summary[name][0]


def main():
    a = read_summary(RESULTS / "setup_a_results" / "setup_a_results.csv")
    c = read_summary(RESULTS / "setup_c_results" / "setup_c_results.csv")
    d = read_summary(RESULTS / "setup_d_results" / "setup_d_results.csv")

    e_path = RESULTS / "setup_e_results" / "setup_e_results.csv"
    e = {
        name: read_summary(e_path, name)
        for name in ("E1_500", "E2_1000", "E3_2000", "E4_all")
    }

    f_path = RESULTS / "setup_f_results" / "setup_f_partial_results.csv"
    f1 = read_summary(f_path, "F1_synthetic_label0_control")
    f2b = read_summary(f_path, "F2b_external_curated_label0")

    g_path = RESULTS / "setup_g_results" / "setup_g_results.csv"
    g0 = read_summary(g_path, "G0_E4_champion")
    g2 = read_summary(g_path, "G2_external_curated")

    rows = [
        ("Real-only", "A", "Real Test", a),
        ("Synthetic matched", "C", "Real Test", c),
        ("Synthetic balanced", "D", "Real Test", d),
        ("Real + 500 synthetic L1", "E1", "Real Test", e["E1_500"]),
        ("Real + 1,000 synthetic L1", "E2", "Real Test", e["E2_1000"]),
        ("Real + 2,000 synthetic L1", "E3", "Real Test", e["E3_2000"]),
        ("Real + all synthetic L1", "E4", "Real Test", e["E4_all"]),
        ("Synthetic L0 control", "F1", "Real Test", f1),
        ("External curated L0", "F2b", "Real Test", f2b),
        ("No external L0", "G0", "Challenge Test", g0),
        ("External curated L0", "G2", "Challenge Test", g2),
    ]
    export = []
    for label, code, test_set, values in rows:
        export.append(
            {
                "comparison": label,
                "code": code,
                "test_set": test_set,
                "macro_f1_mean": metric(values, "macro_f1"),
                "f1_label1_mean": metric(values, "f1_label1"),
                "recall_label1_mean": metric(values, "recall_label1"),
                "precision_label1_mean": metric(values, "precision_label1"),
                "pr_auc_mean": metric(values, "auprc"),
                "fpr_label0_mean": (
                    metric(values, "fpr_label0") if "fpr_label0" in values else None
                ),
            }
        )
    pd.DataFrame(export).to_csv(
        OUTPUT_DIR / "rq4_summary_metrics.csv",
        index=False,
        encoding="utf-8-sig",
    )

    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "axes.titleweight": "bold",
            "axes.titlesize": 13,
            "axes.labelsize": 10,
            "xtick.labelsize": 9.5,
            "ytick.labelsize": 9.5,
        }
    )
    fig, axes = plt.subplots(2, 2, figsize=(16, 9))
    fig.suptitle(
        "RQ4 — Giá trị và vai trò phù hợp của dữ liệu tạo sinh",
        fontsize=21,
        weight="bold",
        color="#243B64",
        y=0.98,
    )

    # 1. Replacement
    ax = axes[0, 0]
    labels = ["Real-only", "Synthetic\nmatched", "Synthetic\nbalanced"]
    values = [metric(a, "f1_label1"), metric(c, "f1_label1"), metric(d, "f1_label1")]
    bars = ax.bar(labels, values, color=["#376AA3", "#E58A55", "#E8B04A"], width=0.62)
    ax.set_ylim(0, 1.02)
    ax.set_ylabel("F1 Label 1")
    ax.set_title("1. Synthetic-only có thay thế dữ liệu thật?")
    ax.grid(axis="y", alpha=0.22)
    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.025,
            f"{value:.3f}",
            ha="center",
            weight="bold",
        )
    ax.text(
        0.5,
        0.66,
        "Không: giảm 41–61 điểm F1",
        transform=ax.transAxes,
        ha="center",
        color="#A33A2B",
        weight="bold",
        bbox={
            "boxstyle": "round,pad=0.35",
            "facecolor": "#FFF7F3",
            "edgecolor": "#D9A08F",
            "alpha": 0.95,
        },
    )

    # 2. Positive augmentation
    ax = axes[0, 1]
    x_labels = ["Real", "+500", "+1k", "+2k", "+all"]
    series = [
        ("F1 Label 1", [metric(a, "f1_label1")] + [metric(e[k], "f1_label1") for k in e]),
        ("Recall Label 1", [metric(a, "recall_label1")] + [metric(e[k], "recall_label1") for k in e]),
        ("Precision Label 1", [metric(a, "precision_label1")] + [metric(e[k], "precision_label1") for k in e]),
    ]
    colors = ["#5B4BA3", "#D65F5F", "#268A78"]
    for (name, values), color in zip(series, colors):
        ax.plot(x_labels, values, marker="o", linewidth=2.2, label=name, color=color)
    ax.set_ylim(0.84, 0.98)
    ax.set_title("2. Thêm synthetic Label 1 có hữu ích?")
    ax.set_ylabel("Điểm số")
    ax.grid(axis="y", alpha=0.22)
    ax.legend(frameon=False, fontsize=9, loc="lower right")
    ax.text(
        0.02,
        0.07,
        "Lợi ích nhẹ; không tăng tuyến tính theo số lượng",
        transform=ax.transAxes,
        color="#5B4BA3",
        weight="bold",
    )

    # 3. Negative coverage
    ax = axes[1, 0]
    labels = ["Synthetic L0 (F1)", "Curated external L0 (F2b)"]
    metrics = ["f1_label1", "precision_label1", "auprc"]
    metric_labels = ["F1 L1", "Precision L1", "PR-AUC"]
    x = range(len(metrics))
    width = 0.34
    ax.bar(
        [i - width / 2 for i in x],
        [metric(f1, m) for m in metrics],
        width,
        label=labels[0],
        color="#D99A3D",
    )
    ax.bar(
        [i + width / 2 for i in x],
        [metric(f2b, m) for m in metrics],
        width,
        label=labels[1],
        color="#4B9A73",
    )
    ax.set_xticks(list(x), metric_labels)
    ax.set_ylim(0.82, 1.01)
    ax.set_title("3. Nguồn Label 0 tạo ra trade-off nào?")
    ax.grid(axis="y", alpha=0.22)
    ax.legend(
        frameon=False,
        fontsize=9,
        loc="upper center",
        bbox_to_anchor=(0.5, 0.98),
        ncol=2,
        columnspacing=1.5,
    )
    ax.text(
        0.5,
        0.09,
        "Curated L0: PR-AUC tăng, F1/Precision giảm nhẹ",
        transform=ax.transAxes,
        ha="center",
        color="#287054",
        weight="bold",
        bbox={
            "boxstyle": "round,pad=0.35",
            "facecolor": "#F2FAF6",
            "edgecolor": "#86BDA2",
            "alpha": 0.96,
        },
    )

    # 4. Domain shift
    ax = axes[1, 1]
    labels = ["Không external L0\n(G0)", "External curated L0\n(G2)"]
    f1_values = [metric(g0, "f1_label1"), metric(g2, "f1_label1")]
    precision_values = [
        metric(g0, "precision_label1"),
        metric(g2, "precision_label1"),
    ]
    x = [0, 1]
    width = 0.32
    ax.bar(
        [i - width / 2 for i in x],
        f1_values,
        width,
        label="F1 Label 1",
        color="#5B70B5",
    )
    ax.bar(
        [i + width / 2 for i in x],
        precision_values,
        width,
        label="Precision Label 1",
        color="#48A6A7",
    )
    ax.set_xticks(x, labels)
    ax.set_ylim(0.4, 1.0)
    ax.set_title("4. External curated L0 có chống domain shift?")
    ax.grid(axis="y", alpha=0.22)
    ax.legend(frameon=False, fontsize=9, loc="upper left")
    reduction = 100 * (1 - metric(g2, "fpr_label0") / metric(g0, "fpr_label0"))
    ax.text(
        0.5,
        0.19,
        f"FPR: 7.73% → 0.73%\nGiảm {reduction:.1f}%",
        transform=ax.transAxes,
        ha="center",
        color="#A33A2B",
        weight="bold",
        fontsize=11,
        bbox={
            "boxstyle": "round,pad=0.4",
            "facecolor": "#FFF7F3",
            "edgecolor": "#D9A08F",
            "alpha": 0.96,
        },
    )

    fig.text(
        0.5,
        0.018,
        "Kết luận: dữ liệu tạo sinh phù hợp để augmentation có kiểm soát, "
        "không phù hợp để thay thế hoàn toàn dữ liệu thật; coverage Label 0 "
        "quyết định độ bền ngoài miền.",
        ha="center",
        fontsize=11.5,
        color="#37465E",
        weight="bold",
    )
    fig.tight_layout(rect=[0.025, 0.055, 0.98, 0.94], h_pad=2.2, w_pad=2.0)
    for suffix in ("png", "pdf"):
        fig.savefig(
            OUTPUT_DIR / f"rq4_summary.{suffix}",
            dpi=300,
            bbox_inches="tight",
            facecolor="white",
        )
    plt.close(fig)


if __name__ == "__main__":
    main()

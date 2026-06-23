"""Aggregate and statistically compare focused TextCNN distillation runs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

MODES = ("hard", "vanilla_kd", "risk_aware_kd")
METRICS = ("macro_f1", "f1_label_1", "recall_label_1", "pr_auc")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze TextCNN KD study.")
    parser.add_argument(
        "--study-root",
        type=Path,
        default=Path("setup_results/textcnn_distillation_study"),
    )
    parser.add_argument("--teacher-name", default="PhoBERT-base")
    parser.add_argument("--seeds", default="42,123,2025")
    parser.add_argument("--bootstrap-samples", type=int, default=2000)
    parser.add_argument("--bootstrap-seed", type=int, default=2026)
    return parser.parse_args()


def slug(value: str) -> str:
    return value.lower().replace(" ", "_")


def run_name(mode: str, seed: int) -> str:
    base = {
        "hard": "char_textcnn_hard",
        "vanilla_kd": "char_textcnn_vanilla_kd",
        "risk_aware_kd": "char_textcnn_risk_aware_kd",
    }[mode]
    return f"{base}_seed_{seed}"


def load_metrics(root: Path, teacher: str, seeds: list[int]) -> pd.DataFrame:
    frames = []
    for mode in MODES:
        for seed in seeds:
            name = run_name(mode, seed)
            path = root / slug(teacher) / mode / f"seed_{seed}" / f"{name}_metrics_by_split.csv"
            if not path.exists():
                raise FileNotFoundError(f"Missing study metrics: {path}")
            df = pd.read_csv(path)
            df["study_mode"] = mode
            df["study_seed"] = seed
            frames.append(df)
    return pd.concat(frames, ignore_index=True)


def prediction_path(root: Path, teacher: str, mode: str, seed: int, split: str) -> Path:
    name = run_name(mode, seed)
    return root / slug(teacher) / mode / f"seed_{seed}" / f"{name}_predictions_{split}.csv"


def fast_metrics(y_true: np.ndarray, y_pred: np.ndarray, p1: np.ndarray) -> dict[str, float]:
    """Compute study metrics without repeated sklearn object construction."""
    y_true = y_true.astype(np.int8, copy=False)
    y_pred = y_pred.astype(np.int8, copy=False)
    tp = int(np.sum((y_true == 1) & (y_pred == 1)))
    fp = int(np.sum((y_true == 0) & (y_pred == 1)))
    fn = int(np.sum((y_true == 1) & (y_pred == 0)))
    tn = int(np.sum((y_true == 0) & (y_pred == 0)))

    def f1(tp_value: int, fp_value: int, fn_value: int) -> float:
        denominator = 2 * tp_value + fp_value + fn_value
        return 0.0 if denominator == 0 else 2 * tp_value / denominator

    f1_1 = f1(tp, fp, fn)
    f1_0 = f1(tn, fn, fp)
    recall_1 = 0.0 if tp + fn == 0 else tp / (tp + fn)

    positives = int(y_true.sum())
    if positives == 0:
        pr_auc = float("nan")
    else:
        order = np.argsort(-p1, kind="mergesort")
        sorted_positive = y_true[order]
        cumulative_tp = np.cumsum(sorted_positive)
        ranks = np.arange(1, len(sorted_positive) + 1)
        pr_auc = float(np.sum((cumulative_tp / ranks) * sorted_positive) / positives)
    return {
        "macro_f1": (f1_0 + f1_1) / 2,
        "f1_label_1": f1_1,
        "recall_label_1": recall_1,
        "pr_auc": pr_auc,
    }


def bootstrap_differences(
    root: Path,
    teacher: str,
    seeds: list[int],
    mode: str,
    split: str,
    samples: int,
    rng: np.random.Generator,
) -> dict[str, tuple[float, float, float]]:
    paired = []
    for seed in seeds:
        hard = pd.read_csv(prediction_path(root, teacher, "hard", seed, split))
        candidate = pd.read_csv(prediction_path(root, teacher, mode, seed, split))
        merged = hard[["sample_id", "label", "pred", "p1"]].merge(
            candidate[["sample_id", "label", "pred", "p1"]],
            on=["sample_id", "label"],
            suffixes=("_hard", "_candidate"),
            validate="one_to_one",
        )
        paired.append(merged)

    deltas = {metric: np.empty(samples, dtype=float) for metric in METRICS}
    for index in range(samples):
        seed_deltas = {metric: [] for metric in METRICS}
        for df in paired:
            sampled = df.iloc[rng.integers(0, len(df), len(df))]
            hard_metrics = fast_metrics(
                sampled["label"].to_numpy(),
                sampled["pred_hard"].to_numpy(),
                sampled["p1_hard"].to_numpy(),
            )
            candidate_metrics = fast_metrics(
                sampled["label"].to_numpy(),
                sampled["pred_candidate"].to_numpy(),
                sampled["p1_candidate"].to_numpy(),
            )
            for metric in METRICS:
                seed_deltas[metric].append(
                    candidate_metrics[metric] - hard_metrics[metric]
                )
        for metric in METRICS:
            deltas[metric][index] = float(np.mean(seed_deltas[metric]))
    return {
        metric: (
            float(np.nanmean(values)),
            float(np.nanquantile(values, 0.025)),
            float(np.nanquantile(values, 0.975)),
        )
        for metric, values in deltas.items()
    }


def build_report(summary: pd.DataFrame, comparisons: pd.DataFrame, seeds: list[int]) -> str:
    display_summary = summary.copy()
    display_summary["mean_sd"] = display_summary.apply(
        lambda row: f"{row['mean']:.4f} ± {row['std']:.4f}", axis=1
    )
    summary_table = display_summary[
        ["split", "study_mode", "metric", "mean_sd", "min", "max"]
    ].to_markdown(index=False)
    display_comparisons = comparisons.copy()
    for column in ["mean_delta", "ci95_low", "ci95_high"]:
        display_comparisons[column] = display_comparisons[column].map(lambda value: f"{value:.4f}")
    comparison_table = display_comparisons.to_markdown(index=False)
    return (
        "# Focused TextCNN Distillation Study\n\n"
        f"- Seeds: `{', '.join(map(str, seeds))}`\n"
        "- Architecture and preprocessing are fixed across all modes.\n"
        "- `hard`: hard-label training only.\n"
        "- `vanilla_kd`: uniform teacher soft-target weight.\n"
        "- `risk_aware_kd`: confidence-aware weight with teacher false-negative suppression.\n\n"
        "## Mean ± SD across seeds\n\n"
        f"{summary_table}\n\n"
        "## Paired bootstrap difference versus hard-label\n\n"
        f"{comparison_table}\n\n"
        "A confidence interval containing zero is treated as insufficient evidence of a stable difference.\n"
    )


def main() -> None:
    args = parse_args()
    seeds = [int(value.strip()) for value in args.seeds.split(",") if value.strip()]
    metrics = load_metrics(args.study_root, args.teacher_name, seeds)
    long = metrics.melt(
        id_vars=["split", "study_mode", "study_seed"],
        value_vars=list(METRICS),
        var_name="metric",
        value_name="value",
    )
    summary = (
        long.groupby(["split", "study_mode", "metric"])["value"]
        .agg(["mean", "std", "min", "max"])
        .reset_index()
    )
    rng = np.random.default_rng(args.bootstrap_seed)
    comparisons = []
    for split in ("dev", "test"):
        for mode in ("vanilla_kd", "risk_aware_kd"):
            bootstrap = bootstrap_differences(
                args.study_root,
                args.teacher_name,
                seeds,
                mode,
                split,
                args.bootstrap_samples,
                rng,
            )
            for metric in METRICS:
                mean_delta, low, high = bootstrap[metric]
                raw = metrics[(metrics["split"] == split) & (metrics["study_mode"].isin(["hard", mode]))]
                pivot = raw.pivot(index="study_seed", columns="study_mode", values=metric)
                signs = int((pivot[mode] > pivot["hard"]).sum())
                comparisons.append(
                    {
                        "split": split,
                        "comparison": f"{mode} - hard",
                        "metric": metric,
                        "mean_delta": mean_delta,
                        "ci95_low": low,
                        "ci95_high": high,
                        "positive_seeds": f"{signs}/{len(seeds)}",
                    }
                )
    comparisons_df = pd.DataFrame(comparisons)
    output_dir = args.study_root / slug(args.teacher_name) / "summary"
    output_dir.mkdir(parents=True, exist_ok=True)
    metrics.to_csv(output_dir / "textcnn_kd_runs.csv", index=False)
    summary.to_csv(output_dir / "textcnn_kd_mean_sd.csv", index=False)
    comparisons_df.to_csv(output_dir / "textcnn_kd_paired_bootstrap.csv", index=False)
    payload = {
        "teacher": args.teacher_name,
        "seeds": seeds,
        "bootstrap_samples": args.bootstrap_samples,
        "bootstrap_seed": args.bootstrap_seed,
        "success_gate": {
            "recall_label_1_mean_delta_min": 0.03,
            "macro_f1_mean_delta_floor": -0.01,
            "positive_seed_min": 2,
            "risk_aware_should_outperform_vanilla_on_target_metric": True,
        },
    }
    (output_dir / "textcnn_kd_protocol.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (output_dir / "textcnn_kd_report.md").write_text(
        build_report(summary, comparisons_df, seeds), encoding="utf-8"
    )
    print(f"[OK] Wrote focused study summary to {output_dir}")


if __name__ == "__main__":
    main()

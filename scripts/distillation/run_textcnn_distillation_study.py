"""Run the focused multi-seed TextCNN distillation ablation study.

The main benchmark keeps both BiLSTM and TextCNN variants. This study is
deliberately narrower: it isolates the effect of knowledge distillation on the
same TextCNN architecture using hard labels, vanilla KD, and risk-aware KD.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


DEFAULT_SEEDS = (42, 123, 2025)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run focused TextCNN KD study.")
    parser.add_argument("--python", default=sys.executable)
    parser.add_argument("--seeds", default="42,123,2025")
    parser.add_argument("--epochs", type=int, default=12)
    parser.add_argument("--patience", type=int, default=3)
    parser.add_argument("--alpha", type=float, default=0.8)
    parser.add_argument("--fn-distill-weight", type=float, default=0.0)
    parser.add_argument(
        "--teacher-dir",
        type=Path,
        default=Path("data/distillation/benchmark_teacher_outputs/phobert-base"),
    )
    parser.add_argument(
        "--split-dir",
        type=Path,
        default=Path("data/distillation/benchmark_splits"),
    )
    parser.add_argument("--teacher-name", default="PhoBERT-base")
    parser.add_argument(
        "--output-root",
        type=Path,
        default=Path("setup_results/textcnn_distillation_study"),
    )
    parser.add_argument("--skip-existing", action="store_true")
    return parser.parse_args()


def parse_seeds(raw: str) -> list[int]:
    seeds = [int(value.strip()) for value in raw.split(",") if value.strip()]
    if not seeds:
        raise ValueError("At least one seed is required.")
    return seeds


def expected_metrics(output_dir: Path, mode: str, seed: int) -> Path:
    run_name = {
        "hard": "char_textcnn_hard",
        "vanilla_kd": "char_textcnn_vanilla_kd",
        "risk_aware_kd": "char_textcnn_risk_aware_kd",
    }[mode]
    run_name = f"{run_name}_seed_{seed}"
    return output_dir / f"{run_name}_metrics_by_split.csv"


def main() -> None:
    args = parse_args()
    seeds = parse_seeds(args.seeds)
    modes = ("hard", "vanilla_kd", "risk_aware_kd")
    script = Path(__file__).with_name("train_benchmark_char_model.py")
    args.output_root.mkdir(parents=True, exist_ok=True)

    for seed in seeds:
        for mode in modes:
            output_dir = args.output_root / args.teacher_name.lower().replace(" ", "_") / mode / f"seed_{seed}"
            if args.skip_existing and expected_metrics(output_dir, mode, seed).exists():
                print(f"[SKIP] {mode} seed={seed}")
                continue
            command = [
                args.python,
                str(script),
                "--architecture",
                "textcnn",
                "--mode",
                mode,
                "--seed",
                str(seed),
                "--epochs",
                str(args.epochs),
                "--patience",
                str(args.patience),
                "--alpha",
                str(args.alpha),
                "--fn-distill-weight",
                str(args.fn_distill_weight),
                "--teacher-dir",
                str(args.teacher_dir),
                "--split-dir",
                str(args.split_dir),
                "--teacher-name",
                args.teacher_name,
                "--run-suffix",
                f"seed_{seed}",
                "--output-dir",
                str(output_dir),
            ]
            print(f"[RUN] {mode} seed={seed}")
            subprocess.run(command, check=True)

    analysis_script = Path(__file__).with_name("analyze_textcnn_distillation_study.py")
    subprocess.run(
        [
            args.python,
            str(analysis_script),
            "--study-root",
            str(args.output_root),
            "--teacher-name",
            args.teacher_name,
            "--seeds",
            ",".join(str(seed) for seed in seeds),
        ],
        check=True,
    )


if __name__ == "__main__":
    main()

"""Evaluate deployment feasibility for teacher and distilled students.

The default benchmark uses split_v2 `test_real`, the main locked real-world
test split from the distillation study. Student checkpoints are measured
directly on CPU. PhoBERT is measured when local weights are present; otherwise
the script still reports teacher F1 from teacher output CSVs and marks runtime
metrics as unavailable.
"""

from __future__ import annotations

import argparse
import json
import math
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import numpy as np
import pandas as pd
import psutil
import torch
from sklearn.metrics import f1_score
from torch import nn
from torch.utils.data import DataLoader, Dataset


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SPLIT_DIR = PROJECT_ROOT / "data" / "distillation" / "splits_v2"
DEFAULT_TEACHER_OUTPUT_DIR = PROJECT_ROOT / "data" / "distillation" / "teacher_outputs_v2"
DEFAULT_TEACHER_MODEL_DIR = PROJECT_ROOT / "model" / "teacher_v2" / "distillation_teacher_phobert_base" / "model"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "setup_results" / "distillation_v2" / "deployment_feasibility"
DEFAULT_MODELS = {
    "BiLSTM": PROJECT_ROOT
    / "setup_results"
    / "distillation_v2"
    / "student_bilstm_distilled"
    / "char_bilstm_distilled_model.pt",
    "TextCNN Distilled": PROJECT_ROOT
    / "setup_results"
    / "distillation_v2"
    / "student_textcnn_distilled"
    / "char_textcnn_distilled_model.pt",
}
SPLIT_TO_FILE = {
    "test_real": "test_real.csv",
    "test_mixed": "test_mixed.csv",
    "test_challenge": "test_challenge.csv",
}
TEACHER_SPLIT_TO_FILE = {
    "test_real": "test_real_teacher.csv",
    "test_mixed": "test_mixed_teacher.csv",
    "test_challenge": "test_challenge_teacher.csv",
}


class CharDataset(Dataset):
    def __init__(self, texts: list[str], vocab: dict[str, int], max_len: int):
        self.x = torch.tensor(
            [encode_text(text, vocab, max_len) for text in texts],
            dtype=torch.long,
        )

    def __len__(self) -> int:
        return len(self.x)

    def __getitem__(self, idx: int) -> torch.Tensor:
        return self.x[idx]


class CharBiLstm(nn.Module):
    def __init__(self, vocab_size: int, embed_dim: int, hidden_dim: int, dropout: float):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        self.lstm = nn.LSTM(embed_dim, hidden_dim, batch_first=True, bidirectional=True)
        self.dropout = nn.Dropout(dropout)
        self.classifier = nn.Linear(hidden_dim * 4, 1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        mask = x.ne(0)
        emb = self.embedding(x)
        out, _ = self.lstm(emb)
        masked = out.masked_fill(~mask.unsqueeze(-1), 0.0)
        lengths = mask.sum(dim=1).clamp(min=1).unsqueeze(-1)
        mean_pool = masked.sum(dim=1) / lengths
        max_pool = out.masked_fill(~mask.unsqueeze(-1), -1e9).max(dim=1).values
        pooled = torch.cat([mean_pool, max_pool], dim=1)
        return self.classifier(self.dropout(pooled)).squeeze(-1)


class CharTextCnn(nn.Module):
    def __init__(
        self,
        vocab_size: int,
        embed_dim: int,
        num_filters: int,
        kernel_sizes: list[int],
        dropout: float,
    ):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        self.convs = nn.ModuleList(
            [
                nn.Conv1d(embed_dim, num_filters, kernel_size=size, padding=size // 2)
                for size in kernel_sizes
            ]
        )
        self.dropout = nn.Dropout(dropout)
        self.classifier = nn.Linear(num_filters * len(kernel_sizes), 1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        emb = self.embedding(x).transpose(1, 2)
        pooled = [torch.relu(conv(emb)).max(dim=2).values for conv in self.convs]
        return self.classifier(self.dropout(torch.cat(pooled, dim=1))).squeeze(-1)


@dataclass
class RuntimeMetrics:
    latency_ms_per_msg: float | None
    throughput_sms_per_s: float | None
    peak_ram_mb: float | None


class MemorySampler:
    def __init__(self, interval_s: float = 0.005):
        self.interval_s = interval_s
        self.process = psutil.Process()
        self.peak = self.process.memory_info().rss
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._sample, daemon=True)

    def __enter__(self) -> "MemorySampler":
        self._thread.start()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self._stop.set()
        self._thread.join()
        self.peak = max(self.peak, self.process.memory_info().rss)

    def _sample(self) -> None:
        while not self._stop.is_set():
            self.peak = max(self.peak, self.process.memory_info().rss)
            time.sleep(self.interval_s)

    @property
    def peak_mb(self) -> float:
        return self.peak / (1024 * 1024)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Deployment feasibility benchmark.")
    parser.add_argument("--split", choices=sorted(SPLIT_TO_FILE), default="test_real")
    parser.add_argument("--split-dir", type=Path, default=DEFAULT_SPLIT_DIR)
    parser.add_argument(
        "--data-file",
        type=Path,
        default=None,
        help="Optional explicit evaluation CSV, overriding --split-dir/--split.",
    )
    parser.add_argument("--teacher-output-dir", type=Path, default=DEFAULT_TEACHER_OUTPUT_DIR)
    parser.add_argument(
        "--teacher-output-file",
        type=Path,
        default=None,
        help="Optional explicit teacher-output CSV for the selected data file.",
    )
    parser.add_argument("--teacher-model-dir", type=Path, default=DEFAULT_TEACHER_MODEL_DIR)
    parser.add_argument("--bilstm-checkpoint", type=Path, default=DEFAULT_MODELS["BiLSTM"])
    parser.add_argument("--textcnn-checkpoint", type=Path, default=DEFAULT_MODELS["TextCNN Distilled"])
    parser.add_argument(
        "--student",
        action="append",
        default=[],
        metavar="LABEL=CHECKPOINT",
        help=(
            "Repeatable custom student checkpoint. When provided, these "
            "replace the default BiLSTM/TextCNN pair; useful for comparing "
            "TextCNN hard, vanilla KD, and risk-aware KD under one protocol."
        ),
    )
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--batch-size", type=int, default=128)
    parser.add_argument("--warmup-runs", type=int, default=2)
    parser.add_argument("--latency-runs", type=int, default=5)
    parser.add_argument("--torch-threads", type=int, default=1)
    parser.add_argument("--skip-teacher-runtime", action="store_true")
    return parser.parse_args()


def load_test_split(split_dir: Path, split: str, data_file: Path | None = None) -> pd.DataFrame:
    path = data_file if data_file is not None else split_dir / SPLIT_TO_FILE[split]
    if not path.exists():
        raise FileNotFoundError(f"Missing test split: {path}")
    df = pd.read_csv(path)
    required = {"content", "label"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"{path} missing columns: {sorted(missing)}")
    df = df.copy()
    df["content"] = df["content"].fillna("").astype(str)
    df["label"] = df["label"].astype(int)
    return df


def parse_student_specs(
    raw_specs: list[str],
    bilstm_checkpoint: Path,
    textcnn_checkpoint: Path,
) -> list[tuple[str, Path]]:
    if not raw_specs:
        return [
            ("BiLSTM", bilstm_checkpoint),
            ("TextCNN Distilled", textcnn_checkpoint),
        ]
    specs = []
    for raw in raw_specs:
        if "=" not in raw:
            raise ValueError(f"Invalid --student value `{raw}`; expected LABEL=CHECKPOINT")
        label, checkpoint = raw.split("=", 1)
        label = label.strip()
        checkpoint = checkpoint.strip()
        if not label or not checkpoint:
            raise ValueError(f"Invalid --student value `{raw}`; expected LABEL=CHECKPOINT")
        specs.append((label, Path(checkpoint)))
    return specs


def encode_text(text: str, vocab: dict[str, int], max_len: int) -> list[int]:
    ids = [vocab.get(char, 1) for char in text.lower()[:max_len]]
    ids.extend([0] * max(0, max_len - len(ids)))
    return ids[:max_len]


def checkpoint_size_mb(path: Path) -> float | None:
    if not path.exists():
        return None
    if path.is_file():
        return path.stat().st_size / (1024 * 1024)
    total = sum(p.stat().st_size for p in path.rglob("*") if p.is_file())
    return total / (1024 * 1024)


def count_params(model: nn.Module) -> int:
    return sum(param.numel() for param in model.parameters())


def load_student(checkpoint_path: Path) -> tuple[nn.Module, dict[str, int], dict]:
    if not checkpoint_path.exists():
        raise FileNotFoundError(f"Missing checkpoint: {checkpoint_path}")
    checkpoint = torch.load(checkpoint_path, map_location="cpu", weights_only=False)
    config = checkpoint["config"]
    vocab = checkpoint["vocab"]
    architecture = config.get("architecture", "bilstm")
    if "textcnn" in checkpoint_path.name or architecture == "textcnn":
        kernel_sizes = [int(size) for size in str(config["kernel_sizes"]).split(",")]
        model = CharTextCnn(
            vocab_size=len(vocab),
            embed_dim=int(config["embed_dim"]),
            num_filters=int(config["num_filters"]),
            kernel_sizes=kernel_sizes,
            dropout=float(config["dropout"]),
        )
    else:
        model = CharBiLstm(
            vocab_size=len(vocab),
            embed_dim=int(config["embed_dim"]),
            hidden_dim=int(config["hidden_dim"]),
            dropout=float(config["dropout"]),
        )
    model.load_state_dict(checkpoint["model_state_dict"])
    model.eval()
    return model, vocab, config


@torch.no_grad()
def predict_student(
    model: nn.Module,
    texts: list[str],
    vocab: dict[str, int],
    max_len: int,
    batch_size: int,
) -> np.ndarray:
    loader = DataLoader(CharDataset(texts, vocab, max_len), batch_size=batch_size)
    probs = []
    for x in loader:
        logits = model(x)
        probs.append(torch.sigmoid(logits).cpu().numpy())
    return np.concatenate(probs)


def benchmark_callable(
    single_run: Callable[[], None],
    batched_run: Callable[[], None],
    rows: int,
    warmup_runs: int,
    latency_runs: int,
) -> RuntimeMetrics:
    for _ in range(warmup_runs):
        single_run()
    start = time.perf_counter()
    for _ in range(latency_runs):
        single_run()
    latency_ms = (time.perf_counter() - start) * 1000.0 / latency_runs

    with MemorySampler() as sampler:
        start = time.perf_counter()
        batched_run()
        elapsed = time.perf_counter() - start
    throughput = rows / elapsed if elapsed > 0 else math.nan
    return RuntimeMetrics(latency_ms, throughput, sampler.peak_mb)


def teacher_weights_available(model_dir: Path) -> bool:
    names = {"pytorch_model.bin", "model.safetensors", "tf_model.h5"}
    return model_dir.exists() and any((model_dir / name).exists() for name in names)


def roberta_param_estimate(config: dict) -> int:
    hidden = int(config["hidden_size"])
    intermediate = int(config["intermediate_size"])
    layers = int(config["num_hidden_layers"])
    vocab = int(config["vocab_size"])
    positions = int(config["max_position_embeddings"])
    token_types = int(config.get("type_vocab_size", 1))
    num_labels = int(config.get("num_labels", 2))

    embeddings = vocab * hidden + positions * hidden + token_types * hidden + 2 * hidden
    layer = (
        4 * hidden * hidden
        + 2 * hidden * intermediate
        + 9 * hidden
        + intermediate
    )
    pooler = hidden * hidden + hidden
    classifier = hidden * num_labels + num_labels
    return int(embeddings + layers * layer + pooler + classifier)


def load_teacher_f1(
    teacher_output_dir: Path,
    split: str,
    teacher_output_file: Path | None = None,
) -> float | None:
    path = (
        teacher_output_file
        if teacher_output_file is not None
        else teacher_output_dir / TEACHER_SPLIT_TO_FILE[split]
    )
    if not path.exists():
        return None
    df = pd.read_csv(path)
    if not {"label", "teacher_pred"}.issubset(df.columns):
        return None
    return f1_score(df["label"].astype(int), df["teacher_pred"].astype(int), pos_label=1, zero_division=0)


def evaluate_teacher_runtime(
    model_dir: Path,
    texts: list[str],
    labels: np.ndarray,
    batch_size: int,
    warmup_runs: int,
    latency_runs: int,
) -> tuple[float, RuntimeMetrics, int]:
    from transformers import AutoModelForSequenceClassification, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    model = AutoModelForSequenceClassification.from_pretrained(model_dir)
    model.eval()
    params = count_params(model)

    @torch.no_grad()
    def predict(text_batch: list[str]) -> np.ndarray:
        encoded = tokenizer(
            text_batch,
            padding=True,
            truncation=True,
            max_length=256,
            return_tensors="pt",
        )
        logits = model(**encoded).logits
        return torch.softmax(logits, dim=-1)[:, 1].cpu().numpy()

    def single_run() -> None:
        predict([texts[0]])

    def batched_run() -> None:
        for start in range(0, len(texts), batch_size):
            predict(texts[start : start + batch_size])

    probs = []
    for start in range(0, len(texts), batch_size):
        probs.append(predict(texts[start : start + batch_size]))
    p1 = np.concatenate(probs)
    f1 = f1_score(labels, (p1 >= 0.5).astype(int), pos_label=1, zero_division=0)
    runtime = benchmark_callable(single_run, batched_run, len(texts), warmup_runs, latency_runs)
    return f1, runtime, params


def build_markdown(results: pd.DataFrame, split: str, rows: int) -> str:
    display = results.copy()
    for col in ["size_mb", "cpu_latency_ms_per_msg", "throughput_sms_per_s", "peak_ram_mb", "f1_label_1"]:
        display[col] = display[col].map(lambda x: "" if pd.isna(x) else f"{x:.4f}")
    display["params"] = display["params"].map(lambda x: "" if pd.isna(x) else f"{int(x):,}")
    table = display[
        [
            "model",
            "params",
            "size_mb",
            "cpu_latency_ms_per_msg",
            "throughput_sms_per_s",
            "peak_ram_mb",
            "f1_label_1",
            "status",
        ]
    ].to_markdown(index=False)
    return (
        "# Deployment Feasibility Evaluation\n\n"
        f"- Test split: `{split}`\n"
        f"- Rows: {rows:,}\n"
        "- Device: CPU\n\n"
        f"{table}\n\n"
        "Notes:\n"
        "- Latency is measured with batch size 1 after warmup.\n"
        "- Throughput and peak RAM are measured on one full batched pass.\n"
        "- Size is checkpoint size when weights exist; for PhoBERT without local weights, size is estimated as parameters x float32 bytes.\n"
        "- PhoBERT runtime metrics require local model weights in the teacher model directory.\n"
    )


def main() -> None:
    args = parse_args()
    torch.set_num_threads(args.torch_threads)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    effective_split = args.data_file.stem if args.data_file is not None else args.split
    test_df = load_test_split(args.split_dir, args.split, args.data_file)
    texts = test_df["content"].tolist()
    labels = test_df["label"].to_numpy()
    rows: list[dict] = []

    student_specs = parse_student_specs(
        args.student,
        args.bilstm_checkpoint,
        args.textcnn_checkpoint,
    )
    for model_name, checkpoint_path in student_specs:
        model, vocab, config = load_student(checkpoint_path)
        max_len = int(config["max_len"])
        threshold = float(config.get("threshold", 0.5))

        def single_run(model=model, vocab=vocab, max_len=max_len) -> None:
            predict_student(model, texts[:1], vocab, max_len, batch_size=1)

        def batched_run(model=model, vocab=vocab, max_len=max_len) -> None:
            predict_student(model, texts, vocab, max_len, batch_size=args.batch_size)

        p1 = predict_student(model, texts, vocab, max_len, batch_size=args.batch_size)
        f1 = f1_score(labels, (p1 >= threshold).astype(int), pos_label=1, zero_division=0)
        runtime = benchmark_callable(
            single_run,
            batched_run,
            len(texts),
            args.warmup_runs,
            args.latency_runs,
        )
        rows.append(
            {
                "model": model_name,
                "params": count_params(model),
                "size_mb": checkpoint_size_mb(checkpoint_path),
                "cpu_latency_ms_per_msg": runtime.latency_ms_per_msg,
                "throughput_sms_per_s": runtime.throughput_sms_per_s,
                "peak_ram_mb": runtime.peak_ram_mb,
                "f1_label_1": f1,
                "status": "ok",
            }
        )

    teacher_params = None
    teacher_status = "ok"
    teacher_f1 = load_teacher_f1(
        args.teacher_output_dir,
        args.split,
        args.teacher_output_file,
    )
    teacher_runtime = RuntimeMetrics(None, None, None)
    teacher_size = checkpoint_size_mb(args.teacher_model_dir)
    config_path = args.teacher_model_dir / "config.json"
    if config_path.exists():
        teacher_params = roberta_param_estimate(json.loads(config_path.read_text(encoding="utf-8")))
        if not teacher_weights_available(args.teacher_model_dir):
            teacher_size = teacher_params * 4 / (1024 * 1024)
    if not args.skip_teacher_runtime and teacher_weights_available(args.teacher_model_dir):
        teacher_f1, teacher_runtime, teacher_params = evaluate_teacher_runtime(
            args.teacher_model_dir,
            texts,
            labels,
            args.batch_size,
            args.warmup_runs,
            args.latency_runs,
        )
    elif not teacher_weights_available(args.teacher_model_dir):
        teacher_status = "runtime_not_measured_missing_weights_size_estimated"
    rows.append(
        {
            "model": "PhoBERT-base",
            "params": teacher_params,
            "size_mb": teacher_size,
            "cpu_latency_ms_per_msg": teacher_runtime.latency_ms_per_msg,
            "throughput_sms_per_s": teacher_runtime.throughput_sms_per_s,
            "peak_ram_mb": teacher_runtime.peak_ram_mb,
            "f1_label_1": teacher_f1,
            "status": teacher_status,
        }
    )

    result_df = pd.DataFrame(rows)
    model_order = {"PhoBERT-base": 0}
    model_order.update({name: index + 1 for index, (name, _) in enumerate(student_specs)})
    result_df["_order"] = result_df["model"].map(model_order)
    result_df = result_df.sort_values("_order").drop(columns="_order")
    result_csv = args.output_dir / f"deployment_feasibility_{effective_split}.csv"
    result_json = args.output_dir / f"deployment_feasibility_{effective_split}.json"
    result_md = args.output_dir / f"deployment_feasibility_{effective_split}.md"
    result_df.to_csv(result_csv, index=False)
    result_json.write_text(
        json.dumps(
            {
                "split": effective_split,
                "data_file": str(args.data_file) if args.data_file is not None else None,
                "teacher_output_file": (
                    str(args.teacher_output_file)
                    if args.teacher_output_file is not None
                    else None
                ),
                "rows": int(len(test_df)),
                "batch_size": args.batch_size,
                "warmup_runs": args.warmup_runs,
                "latency_runs": args.latency_runs,
                "torch_threads": args.torch_threads,
                "results": result_df.where(pd.notna(result_df), None).to_dict(orient="records"),
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    result_md.write_text(
        build_markdown(result_df, effective_split, len(test_df)),
        encoding="utf-8",
    )
    print(f"Wrote {result_csv}")
    print(f"Wrote {result_json}")
    print(f"Wrote {result_md}")


if __name__ == "__main__":
    main()

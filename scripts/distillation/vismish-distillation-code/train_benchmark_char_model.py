"""Train char-level BiLSTM/TextCNN benchmark models.

Supported runs:
- BiLSTM hard labels
- BiLSTM risk-aware distilled from PhoBERT-base (legacy benchmark run)
- TextCNN hard labels
- TextCNN vanilla knowledge distillation
- TextCNN risk-aware knowledge distillation
"""

from __future__ import annotations

import argparse
import json
import random
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from torch import nn
from torch.utils.data import DataLoader, Dataset

from benchmark_config import BENCHMARK_SPLITS, CHAR_MODELS
from benchmark_metrics import compute_binary_metrics, metrics_row, write_metrics_bundle


DEFAULT_SPLIT_DIR = Path("data/distillation/benchmark_splits")
DEFAULT_TEACHER_DIR = Path("data/distillation/benchmark_teacher_outputs/phobert-base")
DEFAULT_OUTPUT_ROOT = Path("setup_results/distillation_benchmark/char_models")

BASE_COLUMNS = {
    "sample_id",
    "content",
    "label",
    "data_origin",
    "category",
    "sender_type",
    "has_url",
    "has_phone_number",
    "obfuscation_level",
}
TEACHER_COLUMNS = {
    "teacher_p1_t2",
    "teacher_pred",
    "teacher_confidence",
    "teacher_agree_label",
    "distill_weight",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train char-level benchmark model.")
    parser.add_argument("--architecture", choices=["bilstm", "textcnn"], required=True)
    parser.add_argument(
        "--mode",
        choices=["hard", "distilled", "vanilla_kd", "risk_aware_kd"],
        required=True,
        help=(
            "`distilled` is retained as a backward-compatible alias for "
            "`risk_aware_kd`."
        ),
    )
    parser.add_argument("--split-dir", type=Path, default=DEFAULT_SPLIT_DIR)
    parser.add_argument("--teacher-dir", type=Path, default=DEFAULT_TEACHER_DIR)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--output-dir", type=Path, default=None)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--max-len", type=int, default=256)
    parser.add_argument("--min-freq", type=int, default=1)
    parser.add_argument("--embed-dim", type=int, default=64)
    parser.add_argument("--hidden-dim", type=int, default=64)
    parser.add_argument("--num-filters", type=int, default=96)
    parser.add_argument("--kernel-sizes", type=str, default="3,4,5")
    parser.add_argument("--dropout", type=float, default=0.3)
    parser.add_argument("--batch-size", type=int, default=128)
    parser.add_argument("--epochs", type=int, default=12)
    parser.add_argument("--patience", type=int, default=3)
    parser.add_argument("--lr", type=float, default=2e-3)
    parser.add_argument("--weight-decay", type=float, default=1e-4)
    parser.add_argument("--threshold", type=float, default=0.5)
    parser.add_argument("--alpha", type=float, default=0.8)
    parser.add_argument("--fn-distill-weight", type=float, default=0.0)
    parser.add_argument("--teacher-name", type=str, default="PhoBERT-base")
    parser.add_argument(
        "--run-suffix",
        type=str,
        default="",
        help="Optional suffix used to keep multi-seed study outputs separate.",
    )
    return parser.parse_args()


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.use_deterministic_algorithms(False)


def split_path(base_dir: Path, split: str, distilled: bool) -> Path:
    if distilled:
        return base_dir / f"{split}_teacher.csv"
    return base_dir / BENCHMARK_SPLITS[split]


def is_distilled_mode(mode: str) -> bool:
    return mode in {"distilled", "vanilla_kd", "risk_aware_kd"}


def normalized_mode(mode: str) -> str:
    return "risk_aware_kd" if mode == "distilled" else mode


def load_splits(args: argparse.Namespace) -> dict[str, pd.DataFrame]:
    distilled = is_distilled_mode(args.mode)
    base_dir = args.teacher_dir if distilled else args.split_dir
    required = BASE_COLUMNS | (TEACHER_COLUMNS if distilled else set())
    splits = {}
    for split in BENCHMARK_SPLITS:
        path = split_path(base_dir, split, distilled)
        if not path.exists():
            raise FileNotFoundError(f"Missing file: {path}")
        df = pd.read_csv(path)
        missing = required - set(df.columns)
        if missing:
            raise ValueError(f"{path} missing columns: {sorted(missing)}")
        df = df.copy()
        df["content"] = df["content"].fillna("").astype(str)
        df["label"] = df["label"].astype(int)
        df["split"] = split
        splits[split] = df
    return splits


def build_vocab(texts: pd.Series, min_freq: int) -> dict[str, int]:
    counter: Counter[str] = Counter()
    for text in texts.astype(str):
        counter.update(text.lower())
    vocab = {"<pad>": 0, "<unk>": 1}
    for char, count in sorted(counter.items()):
        if count >= min_freq:
            vocab[char] = len(vocab)
    return vocab


def encode_text(text: str, vocab: dict[str, int], max_len: int) -> list[int]:
    ids = [vocab.get(char, 1) for char in text.lower()[:max_len]]
    ids.extend([0] * max(0, max_len - len(ids)))
    return ids[:max_len]


def effective_distill_weight(df: pd.DataFrame, fn_weight: float) -> np.ndarray:
    weights = df["distill_weight"].astype(float).to_numpy().copy()
    teacher_fn = (df["label"].astype(int).to_numpy() == 1) & (
        df["teacher_pred"].astype(int).to_numpy() == 0
    )
    weights[teacher_fn] = np.minimum(weights[teacher_fn], fn_weight)
    return np.clip(weights, 0.0, 1.0)


class SmsDataset(Dataset):
    def __init__(self, df: pd.DataFrame, vocab: dict[str, int], args: argparse.Namespace):
        self.df = df.reset_index(drop=True)
        self.x = torch.tensor(
            [encode_text(text, vocab, args.max_len) for text in self.df["content"]],
            dtype=torch.long,
        )
        self.y = torch.tensor(self.df["label"].astype(float).to_numpy(), dtype=torch.float32)
        if is_distilled_mode(args.mode):
            self.teacher_p1 = torch.tensor(
                self.df["teacher_p1_t2"].astype(float).to_numpy(), dtype=torch.float32
            )
            if normalized_mode(args.mode) == "vanilla_kd":
                weights = np.ones(len(self.df), dtype=np.float32)
            else:
                weights = effective_distill_weight(self.df, args.fn_distill_weight)
            self.distill_weight = torch.tensor(weights, dtype=torch.float32)
        else:
            self.teacher_p1 = torch.zeros(len(self.df), dtype=torch.float32)
            self.distill_weight = torch.zeros(len(self.df), dtype=torch.float32)

    def __len__(self) -> int:
        return len(self.df)

    def __getitem__(self, idx: int) -> dict[str, torch.Tensor]:
        return {
            "x": self.x[idx],
            "y": self.y[idx],
            "teacher_p1": self.teacher_p1[idx],
            "distill_weight": self.distill_weight[idx],
        }


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
        return self.classifier(self.dropout(torch.cat([mean_pool, max_pool], dim=1))).squeeze(-1)


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
            [nn.Conv1d(embed_dim, num_filters, kernel_size=size, padding=size // 2) for size in kernel_sizes]
        )
        self.dropout = nn.Dropout(dropout)
        self.classifier = nn.Linear(num_filters * len(kernel_sizes), 1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        emb = self.embedding(x).transpose(1, 2)
        pooled = [torch.relu(conv(emb)).max(dim=2).values for conv in self.convs]
        return self.classifier(self.dropout(torch.cat(pooled, dim=1))).squeeze(-1)


def train_loss(
    logits: torch.Tensor,
    batch: dict[str, torch.Tensor],
    args: argparse.Namespace,
    hard_loss_fn: nn.Module,
) -> torch.Tensor:
    hard = hard_loss_fn(logits, batch["y"])
    if normalized_mode(args.mode) == "hard":
        return hard
    soft = nn.functional.binary_cross_entropy_with_logits(
        logits,
        batch["teacher_p1"],
        reduction="none",
    )
    return args.alpha * hard + (1.0 - args.alpha) * (soft * batch["distill_weight"]).mean()


@torch.no_grad()
def predict(
    model: nn.Module,
    loader: DataLoader,
    df: pd.DataFrame,
    threshold: float,
    device: torch.device,
    run_name: str,
) -> pd.DataFrame:
    model.eval()
    probs = []
    for batch in loader:
        logits = model(batch["x"].to(device))
        probs.append(torch.sigmoid(logits).cpu().numpy())
    p1 = np.concatenate(probs)
    out = df.copy()
    out["model_name"] = run_name
    out["p1"] = p1
    out["p0"] = 1.0 - p1
    out["pred"] = (p1 >= threshold).astype(int)
    out["confidence"] = np.maximum(out["p0"], out["p1"])
    out["agree_label"] = out["pred"].astype(int) == out["label"].astype(int)
    out["error_type"] = np.where(out["agree_label"], "correct", np.where(out["label"].astype(int) == 1, "FN", "FP"))
    return out


def make_model(args: argparse.Namespace, vocab_size: int) -> nn.Module:
    if args.architecture == "bilstm":
        return CharBiLstm(vocab_size, args.embed_dim, args.hidden_dim, args.dropout)
    kernel_sizes = [int(value.strip()) for value in args.kernel_sizes.split(",") if value.strip()]
    return CharTextCnn(vocab_size, args.embed_dim, args.num_filters, kernel_sizes, args.dropout)


def write_report(output_dir: Path, run_name: str, display_name: str, metrics_df: pd.DataFrame, history: list[dict]) -> None:
    lines = [
        f"# {display_name} Benchmark Report",
        "",
        "## Metrics",
        "",
        metrics_df[
            ["split", "rows", "accuracy", "macro_f1", "f1_label_1", "recall_label_1", "pr_auc", "tn", "fp", "fn", "tp"]
        ].to_markdown(index=False),
        "",
        "## Training History",
        "",
        pd.DataFrame(history).to_markdown(index=False),
        "",
    ]
    (output_dir / f"{run_name}_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    set_seed(args.seed)
    mode = normalized_mode(args.mode)
    if mode == "hard":
        run_key = f"{args.architecture}_hard"
        display_name = CHAR_MODELS[run_key]
        run_name = f"char_{run_key}"
    elif mode == "vanilla_kd":
        display_name = f"{args.architecture.upper()} vanilla KD fr {args.teacher_name}"
        run_name = f"char_{args.architecture}_vanilla_kd"
    else:
        run_key = f"{args.architecture}_distilled_phobert_base"
        display_name = CHAR_MODELS[run_key].replace(
            "PhoBERT-base", args.teacher_name
        )
        # Preserve the established benchmark artifact names when the legacy
        # `distilled` alias is used. Focused-study runs use the explicit
        # `risk_aware_kd` name.
        run_name = (
            f"char_{run_key}"
            if args.mode == "distilled"
            else f"char_{args.architecture}_risk_aware_kd"
        )
    if args.run_suffix:
        run_name = f"{run_name}_{args.run_suffix}"
    output_dir = args.output_dir or (args.output_root / run_name)
    output_dir.mkdir(parents=True, exist_ok=True)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    splits = load_splits(args)
    vocab = build_vocab(splits["train"]["content"], args.min_freq)
    datasets = {split: SmsDataset(df, vocab, args) for split, df in splits.items()}
    train_loader = DataLoader(datasets["train"], batch_size=args.batch_size, shuffle=True)
    eval_loaders = {split: DataLoader(ds, batch_size=args.batch_size, shuffle=False) for split, ds in datasets.items()}

    model = make_model(args, len(vocab)).to(device)
    y_train = splits["train"]["label"].to_numpy()
    pos_weight = torch.tensor([(len(y_train) - y_train.sum()) / max(y_train.sum(), 1)], dtype=torch.float32).to(device)
    hard_loss_fn = nn.BCEWithLogitsLoss(pos_weight=pos_weight)
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.lr, weight_decay=args.weight_decay)

    best_state = None
    best_score = -1.0
    stale = 0
    history = []
    for epoch in range(1, args.epochs + 1):
        model.train()
        losses = []
        for batch in train_loader:
            batch = {key: value.to(device) for key, value in batch.items()}
            optimizer.zero_grad()
            loss = train_loss(model(batch["x"]), batch, args, hard_loss_fn)
            loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            optimizer.step()
            losses.append(float(loss.detach().cpu()))
        dev_pred = predict(model, eval_loaders["dev"], splits["dev"], args.threshold, device, run_name)
        dev_metrics = compute_binary_metrics(
            dev_pred["label"].to_numpy(),
            dev_pred["pred"].to_numpy(),
            dev_pred["p1"].to_numpy(),
        )
        score = dev_metrics["macro_f1"]
        history.append(
            {
                "epoch": epoch,
                "train_loss": float(np.mean(losses)),
                "dev_macro_f1": score,
                "dev_f1_label_1": dev_metrics["f1_label_1"],
                "dev_recall_label_1": dev_metrics["recall_label_1"],
            }
        )
        if score > best_score:
            best_score = score
            best_state = {key: value.detach().cpu().clone() for key, value in model.state_dict().items()}
            stale = 0
        else:
            stale += 1
        if stale >= args.patience:
            break
    if best_state is not None:
        model.load_state_dict(best_state)

    rows = []
    split_metrics = {}
    keep_cols = [
        "split",
        "sample_id",
        "content",
        "label",
        "data_origin",
        "category",
        "sender_type",
        "has_url",
        "has_phone_number",
        "obfuscation_level",
        "model_name",
        "p0",
        "p1",
        "pred",
        "confidence",
        "agree_label",
        "error_type",
    ]
    if is_distilled_mode(args.mode):
        keep_cols[10:10] = ["teacher_p1_t2", "teacher_pred", "teacher_confidence", "teacher_agree_label", "distill_weight"]
    for split, df in splits.items():
        pred = predict(model, eval_loaders[split], df, args.threshold, device, run_name)
        metrics = compute_binary_metrics(
            pred["label"].to_numpy(),
            pred["pred"].to_numpy(),
            pred["p1"].to_numpy(),
        )
        split_metrics[split] = metrics
        rows.append(
            metrics_row(
                model_group="char_neural",
                model_name=display_name,
                run_name=run_name,
                split=split,
                metrics=metrics,
                metadata={
                    "architecture": args.architecture,
                    "mode": mode,
                    "teacher": args.teacher_name if is_distilled_mode(args.mode) else "",
                    "seed": args.seed,
                    "alpha": args.alpha if is_distilled_mode(args.mode) else "",
                    "fn_distill_weight": (
                        args.fn_distill_weight if mode == "risk_aware_kd" else ""
                    ),
                },
            )
        )
        pred[keep_cols].to_csv(output_dir / f"{run_name}_predictions_{split}.csv", index=False, encoding="utf-8-sig")
        pred.loc[~pred["agree_label"], keep_cols].to_csv(output_dir / f"{run_name}_errors_{split}.csv", index=False, encoding="utf-8-sig")

    metrics_df = write_metrics_bundle(output_dir, run_name, rows, split_metrics)
    pd.DataFrame(history).to_csv(output_dir / f"{run_name}_training_history.csv", index=False)
    config = vars(args).copy()
    config.update(
        {
            "mode_normalized": mode,
            "run_name": run_name,
            "display_name": display_name,
            "vocab_size": len(vocab),
            "device": str(device),
            "best_dev_macro_f1": best_score,
        }
    )
    (output_dir / f"{run_name}_config.json").write_text(json.dumps(config, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
    torch.save({"model_state_dict": model.state_dict(), "vocab": vocab, "config": config}, output_dir / f"{run_name}_model.pt")
    write_report(output_dir, run_name, display_name, metrics_df, history)
    print(f"[OK] Wrote {display_name} outputs to {output_dir}")
    print(metrics_df[["split", "rows", "macro_f1", "f1_label_1", "recall_label_1", "pr_auc"]])


if __name__ == "__main__":
    main()

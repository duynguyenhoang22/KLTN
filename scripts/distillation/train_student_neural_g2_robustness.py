"""Train BiLSTM/TextCNN students on the G2-style Setup G split.

This robustness check is separate from the split_v2 distillation POC. It uses:
- train: setup_g_train_G2_external_curated.csv
- val: setup_g_challenge_val.csv
- test: setup_g_challenge_test.csv

For distilled mode, teacher probabilities are joined from teacher_outputs_v2 by
exact content. The model input remains text-only (`content`).
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
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from torch import nn
from torch.utils.data import DataLoader, Dataset


SETUP_G_DIR = Path("setup_results/setup_g_results")
TEACHER_DIR = Path("data/distillation/teacher_outputs_v2")
OUTPUT_ROOT = Path("setup_results/distillation_g2_robustness")
SPLIT_FILES = {
    "train": "setup_g_train_G2_external_curated.csv",
    "val": "setup_g_challenge_val.csv",
    "test_challenge": "setup_g_challenge_test.csv",
}
REQUIRED_COLUMNS = {"content", "label", "data_origin"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train G2-style BiLSTM/TextCNN student.")
    parser.add_argument("--architecture", choices=["bilstm", "textcnn"], required=True)
    parser.add_argument("--mode", choices=["hard", "distilled"], required=True)
    parser.add_argument("--setup-g-dir", type=Path, default=SETUP_G_DIR)
    parser.add_argument("--teacher-dir", type=Path, default=TEACHER_DIR)
    parser.add_argument("--output-dir", type=Path, default=None)
    parser.add_argument("--baseline-dir", type=Path, default=None)
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
    return parser.parse_args()


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.use_deterministic_algorithms(False)


def load_teacher_table(teacher_dir: Path) -> pd.DataFrame:
    paths = sorted(teacher_dir.glob("*_teacher.csv"))
    if not paths:
        raise FileNotFoundError(f"No teacher output files found in {teacher_dir}")
    teacher = pd.concat([pd.read_csv(path) for path in paths], ignore_index=True)
    keep = [
        "content",
        "teacher_p1_t2",
        "teacher_pred",
        "teacher_confidence",
        "teacher_agree_label",
        "distill_weight",
    ]
    missing = set(keep) - set(teacher.columns)
    if missing:
        raise ValueError(f"Teacher outputs missing columns: {sorted(missing)}")
    teacher = teacher[keep].drop_duplicates("content")
    teacher["teacher_agree_label"] = teacher["teacher_agree_label"].astype(bool)
    teacher["teacher_pred"] = teacher["teacher_pred"].astype(int)
    return teacher


def load_splits(args: argparse.Namespace) -> dict[str, pd.DataFrame]:
    teacher = load_teacher_table(args.teacher_dir) if args.mode == "distilled" else None
    splits = {}
    for split, filename in SPLIT_FILES.items():
        path = args.setup_g_dir / filename
        if not path.exists():
            raise FileNotFoundError(f"Missing Setup G file: {path}")
        df = pd.read_csv(path)
        missing = REQUIRED_COLUMNS - set(df.columns)
        if missing:
            raise ValueError(f"{path} missing columns: {sorted(missing)}")
        df = df.copy()
        df["content"] = df["content"].fillna("").astype(str)
        df["label"] = df["label"].astype(int)
        df["split"] = split
        if "sample_id" not in df.columns:
            df["sample_id"] = [f"{split}_{i:05d}" for i in range(len(df))]
        if args.mode == "distilled":
            df = df.merge(teacher, on="content", how="left")
            missing_teacher = int(df["teacher_p1_t2"].isna().sum())
            if missing_teacher:
                raise ValueError(f"{split} has {missing_teacher} rows without teacher outputs")
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
        if args.mode == "distilled":
            self.teacher_p1 = torch.tensor(
                self.df["teacher_p1_t2"].astype(float).to_numpy(), dtype=torch.float32
            )
            self.distill_weight = torch.tensor(
                effective_distill_weight(self.df, args.fn_distill_weight), dtype=torch.float32
            )
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


def compute_metrics(y_true: np.ndarray, y_pred: np.ndarray, p1: np.ndarray) -> dict:
    metrics = {
        "rows": int(len(y_true)),
        "accuracy": accuracy_score(y_true, y_pred),
        "macro_f1": f1_score(y_true, y_pred, average="macro", zero_division=0),
        "weighted_f1": f1_score(y_true, y_pred, average="weighted", zero_division=0),
        "precision_label_1": precision_score(y_true, y_pred, pos_label=1, zero_division=0),
        "recall_label_1": recall_score(y_true, y_pred, pos_label=1, zero_division=0),
        "f1_label_1": f1_score(y_true, y_pred, pos_label=1, zero_division=0),
        "precision_label_0": precision_score(y_true, y_pred, pos_label=0, zero_division=0),
        "recall_label_0": recall_score(y_true, y_pred, pos_label=0, zero_division=0),
        "f1_label_0": f1_score(y_true, y_pred, pos_label=0, zero_division=0),
        "confusion_matrix": confusion_matrix(y_true, y_pred, labels=[0, 1]).tolist(),
    }
    if len(np.unique(y_true)) == 2:
        metrics["roc_auc"] = roc_auc_score(y_true, p1)
        metrics["pr_auc"] = average_precision_score(y_true, p1)
    else:
        metrics["roc_auc"] = float("nan")
        metrics["pr_auc"] = float("nan")
    return metrics


def train_loss(logits: torch.Tensor, batch: dict[str, torch.Tensor], args: argparse.Namespace, hard_loss_fn: nn.Module) -> torch.Tensor:
    hard = hard_loss_fn(logits, batch["y"])
    if args.mode == "hard":
        return hard
    soft = nn.functional.binary_cross_entropy_with_logits(
        logits, batch["teacher_p1"], reduction="none"
    )
    return args.alpha * hard + (1.0 - args.alpha) * (soft * batch["distill_weight"]).mean()


@torch.no_grad()
def predict(model: nn.Module, loader: DataLoader, df: pd.DataFrame, threshold: float, device: torch.device, model_name: str) -> pd.DataFrame:
    model.eval()
    probs = []
    for batch in loader:
        logits = model(batch["x"].to(device))
        probs.append(torch.sigmoid(logits).cpu().numpy())
    p1 = np.concatenate(probs)
    pred = (p1 >= threshold).astype(int)
    out = df.copy()
    out["student_model"] = model_name
    out["student_p1"] = p1
    out["student_p0"] = 1.0 - p1
    out["student_pred"] = pred
    out["student_confidence"] = np.maximum(out["student_p0"], out["student_p1"])
    out["student_agree_label"] = out["student_pred"].astype(int) == out["label"].astype(int)
    out["error_type"] = np.where(out["student_agree_label"], "correct", np.where(out["label"].astype(int) == 1, "FN", "FP"))
    return out


def metrics_by_origin(predictions: pd.DataFrame, split: str) -> pd.DataFrame:
    rows = []
    for value, group in predictions.groupby("data_origin", dropna=False, sort=True):
        metrics = compute_metrics(
            group["label"].to_numpy(),
            group["student_pred"].to_numpy(),
            group["student_p1"].to_numpy(),
        )
        rows.append(
            {
                "split": split,
                "data_origin": value,
                "rows": metrics["rows"],
                "accuracy": metrics["accuracy"],
                "macro_f1": metrics["macro_f1"],
                "f1_label_1": metrics["f1_label_1"],
                "recall_label_1": metrics["recall_label_1"],
                "precision_label_1": metrics["precision_label_1"],
                "roc_auc": metrics["roc_auc"],
                "pr_auc": metrics["pr_auc"],
            }
        )
    return pd.DataFrame(rows)


def markdown_table(df: pd.DataFrame, columns: list[str]) -> str:
    if df.empty:
        return "_No rows._"
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for _, row in df[columns].iterrows():
        values = [f"{row[col]:.4f}" if isinstance(row[col], float) else str(row[col]) for col in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def load_baseline_metrics(args: argparse.Namespace) -> pd.DataFrame | None:
    if args.mode != "distilled":
        return None
    baseline_dir = args.baseline_dir or OUTPUT_ROOT / f"student_{args.architecture}_hard_label"
    path = baseline_dir / f"g2_{args.architecture}_hard_metrics_by_split.csv"
    return pd.read_csv(path) if path.exists() else None


def write_report(
    output_dir: Path,
    args: argparse.Namespace,
    metrics_df: pd.DataFrame,
    split_metrics: dict[str, dict],
    origin_metrics: pd.DataFrame,
    history: list[dict],
    baseline: pd.DataFrame | None,
) -> None:
    model_name = f"g2_{args.architecture}_{args.mode}"
    metric_cols = ["split", "rows", "accuracy", "macro_f1", "f1_label_1", "recall_label_1", "precision_label_1", "roc_auc", "pr_auc"]
    lines = [
        f"# {model_name} Report",
        "",
        "## 1. Scope",
        "",
        f"- Architecture: `{args.architecture}`",
        f"- Mode: `{args.mode}`",
        "- Setup: `G2_external_curated` robustness check",
        "- Input features: `content` only",
        "",
        "## 2. Metrics by Split",
        "",
        markdown_table(metrics_df, metric_cols),
        "",
    ]
    if baseline is not None:
        cols = ["split", "macro_f1", "f1_label_1", "recall_label_1", "precision_label_1", "pr_auc"]
        compare = baseline[cols].merge(metrics_df[cols], on="split", suffixes=("_hard", "_distilled"))
        for metric in cols[1:]:
            compare[f"delta_{metric}"] = compare[f"{metric}_distilled"] - compare[f"{metric}_hard"]
        compare.to_csv(output_dir / f"{model_name}_comparison_with_hard.csv", index=False)
        lines.extend(
            [
                "## 3. Comparison with Hard Baseline",
                "",
                markdown_table(
                    compare,
                    ["split", "macro_f1_hard", "macro_f1_distilled", "delta_macro_f1", "f1_label_1_hard", "f1_label_1_distilled", "delta_f1_label_1", "recall_label_1_hard", "recall_label_1_distilled", "delta_recall_label_1"],
                ),
                "",
            ]
        )
    lines.extend(["## 4. Confusion Matrices", ""])
    for split, metrics in split_metrics.items():
        tn, fp = metrics["confusion_matrix"][0]
        fn, tp = metrics["confusion_matrix"][1]
        lines.extend(
            [
                f"### {split}",
                "",
                "| | pred_0 | pred_1 |",
                "|---|---:|---:|",
                f"| true_0 | {tn} | {fp} |",
                f"| true_1 | {fn} | {tp} |",
                "",
            ]
        )
    lines.extend(
        [
            "## 5. Metrics by Data Origin",
            "",
            markdown_table(origin_metrics.sort_values(["split", "data_origin"]), ["split", "data_origin", "rows", "macro_f1", "f1_label_1", "recall_label_1", "precision_label_1"]),
            "",
            "## 6. Training History",
            "",
            pd.DataFrame(history).to_markdown(index=False),
            "",
        ]
    )
    (output_dir / f"{model_name}_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    set_seed(args.seed)
    if args.output_dir is None:
        args.output_dir = OUTPUT_ROOT / f"student_{args.architecture}_{'distilled' if args.mode == 'distilled' else 'hard_label'}"
    args.output_dir.mkdir(parents=True, exist_ok=True)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    splits = load_splits(args)
    vocab = build_vocab(splits["train"]["content"], args.min_freq)
    datasets = {split: SmsDataset(df, vocab, args) for split, df in splits.items()}
    train_loader = DataLoader(datasets["train"], batch_size=args.batch_size, shuffle=True)
    eval_loaders = {split: DataLoader(ds, batch_size=args.batch_size, shuffle=False) for split, ds in datasets.items()}

    if args.architecture == "bilstm":
        model = CharBiLstm(len(vocab), args.embed_dim, args.hidden_dim, args.dropout).to(device)
    else:
        kernel_sizes = [int(value.strip()) for value in args.kernel_sizes.split(",") if value.strip()]
        model = CharTextCnn(len(vocab), args.embed_dim, args.num_filters, kernel_sizes, args.dropout).to(device)

    y_train = splits["train"]["label"].to_numpy()
    pos_weight = torch.tensor([(len(y_train) - y_train.sum()) / max(y_train.sum(), 1)], dtype=torch.float32).to(device)
    hard_loss_fn = nn.BCEWithLogitsLoss(pos_weight=pos_weight)
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.lr, weight_decay=args.weight_decay)
    model_name = f"g2_{args.architecture}_{args.mode}"

    best_state = None
    best_score = -1.0
    stale = 0
    history = []
    for epoch in range(1, args.epochs + 1):
        model.train()
        losses = []
        for batch in train_loader:
            batch = {k: v.to(device) for k, v in batch.items()}
            optimizer.zero_grad()
            logits = model(batch["x"])
            loss = train_loss(logits, batch, args, hard_loss_fn)
            loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            optimizer.step()
            losses.append(float(loss.detach().cpu()))
        val_pred = predict(model, eval_loaders["val"], splits["val"], args.threshold, device, model_name)
        val_metrics = compute_metrics(val_pred["label"].to_numpy(), val_pred["student_pred"].to_numpy(), val_pred["student_p1"].to_numpy())
        score = val_metrics["macro_f1"]
        history.append({"epoch": epoch, "train_loss": float(np.mean(losses)), "val_macro_f1": score, "val_f1_label_1": val_metrics["f1_label_1"], "val_recall_label_1": val_metrics["recall_label_1"]})
        if score > best_score:
            best_score = score
            best_state = {k: v.detach().cpu().clone() for k, v in model.state_dict().items()}
            stale = 0
        else:
            stale += 1
        if stale >= args.patience:
            break

    if best_state is not None:
        model.load_state_dict(best_state)

    metrics_rows = []
    split_metrics = {}
    origin_frames = []
    keep_cols = [
        "split",
        "sample_id",
        "content",
        "label",
        "data_origin",
        "student_model",
        "student_p0",
        "student_p1",
        "student_pred",
        "student_confidence",
        "student_agree_label",
        "error_type",
    ]
    if args.mode == "distilled":
        keep_cols[5:5] = ["teacher_p1_t2", "teacher_pred", "teacher_confidence", "teacher_agree_label", "distill_weight"]

    for split, df in splits.items():
        pred = predict(model, eval_loaders[split], df, args.threshold, device, model_name)
        metrics = compute_metrics(pred["label"].to_numpy(), pred["student_pred"].to_numpy(), pred["student_p1"].to_numpy())
        split_metrics[split] = metrics
        metrics_rows.append(
            {
                "split": split,
                **{k: v for k, v in metrics.items() if k != "confusion_matrix"},
                "tn": metrics["confusion_matrix"][0][0],
                "fp": metrics["confusion_matrix"][0][1],
                "fn": metrics["confusion_matrix"][1][0],
                "tp": metrics["confusion_matrix"][1][1],
            }
        )
        pred[keep_cols].to_csv(args.output_dir / f"{model_name}_predictions_{split}.csv", index=False)
        pred.loc[~pred["student_agree_label"], keep_cols].to_csv(args.output_dir / f"{model_name}_errors_{split}.csv", index=False)
        origin_frames.append(metrics_by_origin(pred, split))

    metrics_df = pd.DataFrame(metrics_rows)
    metrics_df.to_csv(args.output_dir / f"{model_name}_metrics_by_split.csv", index=False)
    with (args.output_dir / f"{model_name}_metrics.json").open("w", encoding="utf-8") as f:
        json.dump(split_metrics, f, ensure_ascii=False, indent=2)
    origin_metrics = pd.concat(origin_frames, ignore_index=True)
    origin_metrics.to_csv(args.output_dir / f"{model_name}_metrics_by_data_origin.csv", index=False)
    pd.DataFrame(history).to_csv(args.output_dir / f"{model_name}_training_history.csv", index=False)

    config = vars(args).copy()
    config.update({"model_name": model_name, "vocab_size": len(vocab), "device": str(device), "best_val_macro_f1": best_score, "input_features": ["content"]})
    with (args.output_dir / f"{model_name}_config.json").open("w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2, default=str)
    torch.save({"model_state_dict": model.state_dict(), "vocab": vocab, "config": config}, args.output_dir / f"{model_name}_model.pt")

    baseline = load_baseline_metrics(args)
    write_report(args.output_dir, args, metrics_df, split_metrics, origin_metrics, history, baseline)
    print(f"Wrote G2 {args.architecture} {args.mode} outputs to {args.output_dir}")
    print(metrics_df[["split", "rows", "macro_f1", "f1_label_1", "recall_label_1", "precision_label_1"]])


if __name__ == "__main__":
    main()

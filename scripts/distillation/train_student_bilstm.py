"""Train lightweight character-level neural students.

Modes:
- hard: hard-label baseline trained from split CSVs.
- distilled: same architecture trained with hard-label CE plus teacher soft BCE.

The model uses only `content` as input. Metadata is retained only for audit.
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


SPLIT_DIR = Path("data/distillation/splits_v2")
TEACHER_DIR = Path("data/distillation/teacher_outputs_v2")
OUTPUT_ROOT = Path("setup_results/distillation_v2")
SPLIT_FILES = {
    "train": "train.csv",
    "val": "val.csv",
    "test_real": "test_real.csv",
    "test_mixed": "test_mixed.csv",
    "test_challenge": "test_challenge.csv",
}
TEACHER_FILES = {
    "train": "train_teacher.csv",
    "val": "val_teacher.csv",
    "test_real": "test_real_teacher.csv",
    "test_mixed": "test_mixed_teacher.csv",
    "test_challenge": "test_challenge_teacher.csv",
}
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
GROUP_COLUMNS = [
    "data_origin",
    "category",
    "sender_type",
    "has_url",
    "has_phone_number",
    "obfuscation_level",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train character-level BiLSTM/TextCNN students.")
    parser.add_argument("--architecture", choices=["bilstm", "textcnn"], default="bilstm")
    parser.add_argument("--mode", choices=["hard", "distilled"], required=True)
    parser.add_argument("--split-dir", type=Path, default=SPLIT_DIR)
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


def load_splits(args: argparse.Namespace) -> dict[str, pd.DataFrame]:
    use_teacher = args.mode == "distilled"
    files = TEACHER_FILES if use_teacher else SPLIT_FILES
    base_dir = args.teacher_dir if use_teacher else args.split_dir
    required = BASE_COLUMNS | (TEACHER_COLUMNS if use_teacher else set())
    out = {}
    for split, filename in files.items():
        path = base_dir / filename
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
        if use_teacher:
            df["teacher_agree_label"] = df["teacher_agree_label"].astype(bool)
            df["teacher_pred"] = df["teacher_pred"].astype(int)
        out[split] = df
    return out


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
    if len(ids) < max_len:
        ids.extend([0] * (max_len - len(ids)))
    return ids


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
        if args.mode == "distilled" and "teacher_p1_t2" in self.df.columns:
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
        self.lstm = nn.LSTM(
            embed_dim,
            hidden_dim,
            batch_first=True,
            bidirectional=True,
        )
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
                nn.Conv1d(
                    in_channels=embed_dim,
                    out_channels=num_filters,
                    kernel_size=kernel_size,
                    padding=kernel_size // 2,
                )
                for kernel_size in kernel_sizes
            ]
        )
        self.dropout = nn.Dropout(dropout)
        self.classifier = nn.Linear(num_filters * len(kernel_sizes), 1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        emb = self.embedding(x).transpose(1, 2)
        pooled = []
        for conv in self.convs:
            features = torch.relu(conv(emb))
            pooled.append(torch.max(features, dim=2).values)
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


def train_loss(
    logits: torch.Tensor,
    batch: dict[str, torch.Tensor],
    args: argparse.Namespace,
    hard_loss_fn: nn.Module,
) -> torch.Tensor:
    hard = hard_loss_fn(logits, batch["y"])
    if args.mode == "hard":
        return hard
    soft = nn.functional.binary_cross_entropy_with_logits(
        logits, batch["teacher_p1"], reduction="none"
    )
    weighted_soft = (soft * batch["distill_weight"]).mean()
    return args.alpha * hard + (1.0 - args.alpha) * weighted_soft


@torch.no_grad()
def predict(
    model: nn.Module,
    loader: DataLoader,
    df: pd.DataFrame,
    threshold: float,
    device: torch.device,
    model_name: str,
) -> pd.DataFrame:
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
    out["error_type"] = np.where(
        out["student_agree_label"],
        "correct",
        np.where(out["label"].astype(int) == 1, "FN", "FP"),
    )
    return out


def metrics_by_group(predictions: pd.DataFrame, split: str, group_col: str) -> pd.DataFrame:
    rows = []
    for value, group in predictions.groupby(group_col, dropna=False, sort=True):
        metrics = compute_metrics(
            group["label"].to_numpy(),
            group["student_pred"].to_numpy(),
            group["student_p1"].to_numpy(),
        )
        rows.append(
            {
                "split": split,
                "group_col": group_col,
                "group_value": value,
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
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for _, row in df[columns].iterrows():
        values = []
        for col in columns:
            value = row[col]
            values.append(f"{value:.4f}" if isinstance(value, float) else str(value))
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def load_baseline_metrics(args: argparse.Namespace) -> pd.DataFrame | None:
    if args.mode != "distilled":
        return None
    if args.baseline_dir is None:
        args.baseline_dir = OUTPUT_ROOT / f"student_{args.architecture}_hard_label"
    candidates = [
        args.baseline_dir / f"char_{args.architecture}_hard_metrics_by_split.csv",
        args.baseline_dir / f"student_{args.architecture}_hard_metrics_by_split.csv",
    ]
    for path in candidates:
        if path.exists():
            return pd.read_csv(path)
    return None


def comparison_table(metrics_df: pd.DataFrame, baseline: pd.DataFrame | None) -> pd.DataFrame:
    if baseline is None:
        return pd.DataFrame()
    cols = ["split", "macro_f1", "f1_label_1", "recall_label_1", "precision_label_1", "pr_auc"]
    merged = baseline[cols].merge(metrics_df[cols], on="split", suffixes=("_hard", "_distilled"))
    for metric in cols[1:]:
        merged[f"delta_{metric}"] = merged[f"{metric}_distilled"] - merged[f"{metric}_hard"]
    return merged


def write_report(
    output_dir: Path,
    args: argparse.Namespace,
    metrics_df: pd.DataFrame,
    split_metrics: dict[str, dict],
    group_metrics: pd.DataFrame,
    history: list[dict],
    baseline: pd.DataFrame | None,
) -> None:
    name = (
        f"student_{args.architecture}_distilled"
        if args.mode == "distilled"
        else f"student_{args.architecture}_hard"
    )
    metric_cols = [
        "split",
        "rows",
        "accuracy",
        "macro_f1",
        "f1_label_1",
        "recall_label_1",
        "precision_label_1",
        "roc_auc",
        "pr_auc",
    ]
    lines = [
        f"# {name} Report",
        "",
        "## 1. Scope",
        "",
        f"- Student: `character-level {args.architecture}`",
        f"- Mode: `{args.mode}`",
        "- Input features: `content` only",
        f"- Threshold: `{args.threshold}`",
        "",
        "## 2. Configuration",
        "",
        "```text",
        f"max_len = {args.max_len}",
        f"embed_dim = {args.embed_dim}",
        f"hidden_dim = {args.hidden_dim}",
        f"num_filters = {args.num_filters}",
        f"kernel_sizes = {args.kernel_sizes}",
        f"dropout = {args.dropout}",
        f"batch_size = {args.batch_size}",
        f"epochs = {args.epochs}",
        f"patience = {args.patience}",
        f"lr = {args.lr}",
        f"alpha = {args.alpha if args.mode == 'distilled' else 'N/A'}",
        f"fn_distill_weight = {args.fn_distill_weight if args.mode == 'distilled' else 'N/A'}",
        "```",
        "",
        "## 3. Metrics by Split",
        "",
        markdown_table(metrics_df, metric_cols),
        "",
    ]
    compare = comparison_table(metrics_df, baseline)
    if not compare.empty:
        compare_cols = [
            "split",
            "macro_f1_hard",
            "macro_f1_distilled",
            "delta_macro_f1",
            "f1_label_1_hard",
            "f1_label_1_distilled",
            "delta_f1_label_1",
            "recall_label_1_hard",
            "recall_label_1_distilled",
            "delta_recall_label_1",
        ]
        lines.extend(["## 4. Comparison with Hard Baseline", "", markdown_table(compare, compare_cols), ""])
        compare.to_csv(output_dir / f"student_{args.architecture}_distilled_comparison_with_hard.csv", index=False)

    lines.extend(["## 5. Confusion Matrices", ""])
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

    focus = group_metrics[
        group_metrics["split"].isin(["test_real", "test_mixed", "test_challenge"])
        & group_metrics["group_col"].eq("data_origin")
    ]
    lines.extend(
        [
            "## 6. Test Metrics by Data Origin",
            "",
            markdown_table(
                focus.sort_values(["split", "group_value"]),
                ["split", "group_value", "rows", "macro_f1", "f1_label_1", "recall_label_1", "precision_label_1"],
            ),
            "",
            "## 7. Training History",
            "",
            pd.DataFrame(history).to_markdown(index=False),
            "",
        ]
    )
    (output_dir / f"{name}_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    set_seed(args.seed)
    if args.output_dir is None:
        args.output_dir = OUTPUT_ROOT / f"student_{args.architecture}_{'distilled' if args.mode == 'distilled' else 'hard_label'}"
    if args.baseline_dir is None:
        args.baseline_dir = OUTPUT_ROOT / f"student_{args.architecture}_hard_label"
    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    splits = load_splits(args)
    vocab = build_vocab(splits["train"]["content"], args.min_freq)
    datasets = {split: SmsDataset(df, vocab, args) for split, df in splits.items()}
    train_loader = DataLoader(datasets["train"], batch_size=args.batch_size, shuffle=True)
    eval_loaders = {
        split: DataLoader(ds, batch_size=args.batch_size, shuffle=False)
        for split, ds in datasets.items()
    }

    if args.architecture == "bilstm":
        model = CharBiLstm(len(vocab), args.embed_dim, args.hidden_dim, args.dropout).to(device)
    else:
        kernel_sizes = [int(value.strip()) for value in args.kernel_sizes.split(",") if value.strip()]
        model = CharTextCnn(
            len(vocab),
            args.embed_dim,
            args.num_filters,
            kernel_sizes,
            args.dropout,
        ).to(device)
    y_train = splits["train"]["label"].to_numpy()
    pos_weight = torch.tensor([(len(y_train) - y_train.sum()) / max(y_train.sum(), 1)], dtype=torch.float32).to(device)
    hard_loss_fn = nn.BCEWithLogitsLoss(pos_weight=pos_weight)
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.lr, weight_decay=args.weight_decay)

    best_state = None
    best_score = -1.0
    stale = 0
    history = []
    model_name = (
        f"char_{args.architecture}_distilled"
        if args.mode == "distilled"
        else f"char_{args.architecture}_hard"
    )

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
        val_metrics = compute_metrics(
            val_pred["label"].to_numpy(),
            val_pred["student_pred"].to_numpy(),
            val_pred["student_p1"].to_numpy(),
        )
        score = val_metrics["macro_f1"]
        history.append(
            {
                "epoch": epoch,
                "train_loss": float(np.mean(losses)),
                "val_macro_f1": score,
                "val_f1_label_1": val_metrics["f1_label_1"],
                "val_recall_label_1": val_metrics["recall_label_1"],
            }
        )
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
    group_frames = []
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
        "student_model",
        "student_p0",
        "student_p1",
        "student_pred",
        "student_confidence",
        "student_agree_label",
        "error_type",
    ]
    if args.mode == "distilled":
        keep_cols[10:10] = [
            "teacher_p1_t2",
            "teacher_pred",
            "teacher_confidence",
            "teacher_agree_label",
            "distill_weight",
        ]

    for split, df in splits.items():
        pred = predict(model, eval_loaders[split], df, args.threshold, device, model_name)
        metrics = compute_metrics(
            pred["label"].to_numpy(),
            pred["student_pred"].to_numpy(),
            pred["student_p1"].to_numpy(),
        )
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
        pred[keep_cols].to_csv(output_dir / f"{model_name}_predictions_{split}.csv", index=False)
        pred.loc[~pred["student_agree_label"], keep_cols].to_csv(
            output_dir / f"{model_name}_errors_{split}.csv", index=False
        )
        for group_col in GROUP_COLUMNS:
            group_frames.append(metrics_by_group(pred, split, group_col))

    metrics_df = pd.DataFrame(metrics_rows)
    metrics_df.to_csv(output_dir / f"{model_name}_metrics_by_split.csv", index=False)
    with (output_dir / f"{model_name}_metrics.json").open("w", encoding="utf-8") as f:
        json.dump(split_metrics, f, ensure_ascii=False, indent=2)
    group_metrics = pd.concat(group_frames, ignore_index=True)
    group_metrics.to_csv(output_dir / f"{model_name}_metrics_by_group.csv", index=False)
    pd.DataFrame(history).to_csv(output_dir / f"{model_name}_training_history.csv", index=False)

    config = vars(args).copy()
    config.update(
        {
            "model_name": model_name,
            "vocab_size": len(vocab),
            "device": str(device),
            "input_features": ["content"],
            "metadata_used_for_training": False,
            "best_val_macro_f1": best_score,
        }
    )
    with (output_dir / f"{model_name}_config.json").open("w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2, default=str)
    torch.save(
        {
            "model_state_dict": model.state_dict(),
            "vocab": vocab,
            "config": config,
        },
        output_dir / f"{model_name}_model.pt",
    )

    baseline = load_baseline_metrics(args)
    write_report(output_dir, args, metrics_df, split_metrics, group_metrics, history, baseline)
    print(f"Wrote {args.mode} {args.architecture} outputs to {output_dir}")
    print(metrics_df[["split", "rows", "macro_f1", "f1_label_1", "recall_label_1", "precision_label_1"]])


if __name__ == "__main__":
    main()

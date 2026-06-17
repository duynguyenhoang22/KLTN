"""Audit Phase 1 synthetic-data quality metrics for ViSmishDS.

The embedding encoder defaults to ``vinai/phobert-base`` from Transformers.
This intentionally avoids reusing the fine-tuned PhoBERT classifier checkpoint,
so the embedding audit is not biased by the previous downstream training run.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import math
import re
import warnings
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy.linalg import sqrtm
from scipy.spatial.distance import jensenshannon
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, pairwise_distances, roc_auc_score
from sklearn.metrics.pairwise import cosine_similarity, rbf_kernel
from sklearn.model_selection import StratifiedKFold
from sklearn.neighbors import NearestNeighbors
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


DEFAULT_PHASE1 = Path("data/final/vismishds_phase1_final.csv")
DEFAULT_CURRENT = Path("model/base/temp.csv")
DEFAULT_OUT_DIR = Path("data/reports/phase1_quality_metrics")
DEFAULT_EMBEDDING_MODEL = "vinai/phobert-base"
SYNTHETIC_ORIGINS = {"synthetic", "paraphrased", "synthetic_hard_positive"}
REQUIRED_COLUMNS = {"sample_id", "content", "label", "data_origin"}
OPTIONAL_DISTRIBUTION_COLUMNS = [
    "category",
    "sender_type",
    "has_url",
    "has_phone_number",
    "obfuscation_level",
]


@dataclass(frozen=True)
class SliceSpec:
    name: str
    label: int | None = None
    synthetic_like: bool | None = None


SLICE_SPECS = [
    SliceSpec("all"),
    SliceSpec("label_1_all", label=1),
    SliceSpec("label_1_synthetic_like", label=1, synthetic_like=True),
    SliceSpec("label_1_real", label=1, synthetic_like=False),
    SliceSpec("label_0_synthetic_like", label=0, synthetic_like=True),
    SliceSpec("label_0_real", label=0, synthetic_like=False),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate quantitative quality audit files for ViSmishDS Phase 1."
    )
    parser.add_argument("--phase1", type=Path, default=DEFAULT_PHASE1)
    parser.add_argument("--current", type=Path, default=DEFAULT_CURRENT)
    parser.add_argument("--embedding-model", default=DEFAULT_EMBEDDING_MODEL)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--bootstrap", type=int, default=1000)
    parser.add_argument("--permutations", type=int, default=1000)
    parser.add_argument("--max-pairs-output", type=int, default=200)
    parser.add_argument("--max-mmd-samples", type=int, default=2000)
    parser.add_argument("--max-separability-samples", type=int, default=8000)
    parser.add_argument("--max-length", type=int, default=256)
    parser.add_argument("--no-embedding", action="store_true")
    parser.add_argument("--force-recompute-embeddings", action="store_true")
    parser.add_argument(
        "--local-files-only",
        action="store_true",
        help="Require Transformers to load the embedding model from local cache only.",
    )
    parser.add_argument(
        "--strict-invariants",
        action="store_true",
        help="Treat dataset sanity-check mismatches as fatal errors.",
    )
    return parser.parse_args()


def configure_logging(out_dir: Path) -> logging.Logger:
    out_dir.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("phase1_quality_audit")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    file_handler = logging.FileHandler(out_dir / "audit_phase1_quality_metrics.log", encoding="utf-8")
    file_handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger


def read_dataset(path: Path, dataset_name: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["dataset"] = dataset_name
    if "content" in df.columns:
        df["content"] = df["content"].fillna("").astype(str)
    if "label" in df.columns:
        df["label"] = pd.to_numeric(df["label"], errors="coerce").astype("Int64")
    return df


def synthetic_like_mask(df: pd.DataFrame) -> pd.Series:
    origin = df.get("data_origin", pd.Series("", index=df.index)).fillna("").astype(str).str.lower()
    source_dataset = df.get("source_dataset", pd.Series("", index=df.index)).fillna("").astype(str).str.lower()
    return origin.isin(SYNTHETIC_ORIGINS) | source_dataset.str.startswith("synthetic")


def apply_slice(df: pd.DataFrame, spec: SliceSpec) -> pd.DataFrame:
    mask = pd.Series(True, index=df.index)
    if spec.label is not None:
        mask &= df["label"].eq(spec.label)
    if spec.synthetic_like is not None:
        mask &= synthetic_like_mask(df).eq(spec.synthetic_like)
    return df.loc[mask].copy()


def build_slices(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    return {spec.name: apply_slice(df, spec) for spec in SLICE_SPECS}


def record_check(
    checks: list[dict[str, Any]],
    name: str,
    expected: Any,
    actual: Any,
    hard: bool,
    passed: bool,
) -> None:
    status = "pass" if passed else ("error" if hard else "warning")
    checks.append(
        {
            "name": name,
            "expected": expected,
            "actual": actual,
            "severity": "hard" if hard else "soft",
            "status": status,
        }
    )


def validate_inputs(
    phase1: pd.DataFrame,
    current: pd.DataFrame,
    args: argparse.Namespace,
    logger: logging.Logger,
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    for name, path in [("phase1_path", args.phase1), ("current_path", args.current)]:
        record_check(checks, name, "exists", str(path), True, path.exists())

    for name, df in [("phase1", phase1), ("current", current)]:
        missing = sorted(REQUIRED_COLUMNS - set(df.columns))
        record_check(checks, f"{name}_required_columns", [], missing, True, not missing)
        if missing:
            continue
        labels = sorted(x for x in df["label"].dropna().unique().tolist())
        record_check(checks, f"{name}_labels", [0, 1], labels, True, labels == [0, 1])
        empty_content_rate = float(df["content"].str.strip().eq("").mean())
        record_check(checks, f"{name}_empty_content_rate", "<=0.01", empty_content_rate, True, empty_content_rate <= 0.01)

    p1_slices = build_slices(phase1)
    current_slices = build_slices(current)
    for dataset_name, slices in [("phase1", p1_slices), ("current", current_slices)]:
        for slice_name in ["label_1_synthetic_like", "label_1_real"]:
            record_check(
                checks,
                f"{dataset_name}_{slice_name}_non_empty",
                ">0",
                int(len(slices[slice_name])),
                True,
                len(slices[slice_name]) > 0,
            )

    phase1_label_counts = {
        str(k): int(v) for k, v in phase1["label"].value_counts().sort_index().to_dict().items()
    }
    current_label_counts = {
        str(k): int(v) for k, v in current["label"].value_counts().sort_index().to_dict().items()
    }
    record_check(checks, "phase1_row_count", 10562, int(len(phase1)), False, len(phase1) == 10562)
    record_check(checks, "current_row_count", 10562, int(len(current)), False, len(current) == 10562)
    record_check(checks, "phase1_label_counts", {"0": 5320, "1": 5242}, phase1_label_counts, False, phase1_label_counts == {"0": 5320, "1": 5242})
    record_check(
        checks,
        "phase1_label_1_synthetic_like_count",
        "about 4996",
        int(len(p1_slices["label_1_synthetic_like"])),
        False,
        abs(len(p1_slices["label_1_synthetic_like"]) - 4996) <= 100,
    )

    errors = [check for check in checks if check["status"] == "error"]
    warnings_ = [check for check in checks if check["status"] == "warning"]
    if warnings_:
        logger.warning("Soft invariant warnings: %s", json.dumps(warnings_, ensure_ascii=False))
    if errors:
        raise ValueError(f"Hard invariant failures: {json.dumps(errors, ensure_ascii=False)}")
    if args.strict_invariants and warnings_:
        raise ValueError(f"Strict invariant failures: {json.dumps(warnings_, ensure_ascii=False)}")
    return checks


def model_cache_key(model_name: str, dataset_name: str, texts: pd.Series, max_length: int) -> str:
    digest = hashlib.sha256()
    digest.update(model_name.encode("utf-8"))
    digest.update(dataset_name.encode("utf-8"))
    digest.update(str(max_length).encode("utf-8"))
    for text in texts.fillna("").astype(str):
        digest.update(b"\0")
        digest.update(text.encode("utf-8", errors="ignore"))
    return digest.hexdigest()[:16]


def maybe_word_segment(texts: list[str], logger: logging.Logger) -> list[str]:
    try:
        from pyvi.ViTokenizer import tokenize
    except Exception as exc:  # pragma: no cover - depends on Kaggle image.
        logger.warning("pyvi is unavailable; using raw text for PhoBERT tokenization: %s", exc)
        return texts
    return [tokenize(text) for text in texts]


def load_embeddings(
    df: pd.DataFrame,
    dataset_name: str,
    args: argparse.Namespace,
    logger: logging.Logger,
) -> np.ndarray:
    cache_dir = args.out_dir / "cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    key = model_cache_key(args.embedding_model, dataset_name, df["content"], args.max_length)
    cache_path = cache_dir / f"embeddings_{dataset_name}_{key}.npy"
    if cache_path.exists() and not args.force_recompute_embeddings:
        logger.info("Loading cached embeddings for %s from %s", dataset_name, cache_path)
        return np.load(cache_path)

    import torch
    from transformers import AutoModel, AutoTokenizer

    logger.info("Loading embedding model %s from Transformers", args.embedding_model)
    warning_messages: list[str] = []
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        tokenizer = AutoTokenizer.from_pretrained(
            args.embedding_model,
            use_fast=False,
            local_files_only=args.local_files_only,
        )
        model = AutoModel.from_pretrained(
            args.embedding_model,
            local_files_only=args.local_files_only,
        )
        warning_messages = [str(item.message) for item in caught]
    if warning_messages:
        logger.warning("Suppressed/logged model-loading warnings: %s", warning_messages)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)
    model.eval()

    all_embeddings: list[np.ndarray] = []
    texts = df["content"].fillna("").astype(str).tolist()
    for start in range(0, len(texts), args.batch_size):
        batch_texts = maybe_word_segment(texts[start : start + args.batch_size], logger)
        encoded = tokenizer(
            batch_texts,
            padding=True,
            truncation=True,
            max_length=args.max_length,
            return_tensors="pt",
        )
        encoded = {key: value.to(device) for key, value in encoded.items()}
        with torch.no_grad():
            outputs = model(**encoded)
            token_embeddings = outputs.last_hidden_state
            attention_mask = encoded["attention_mask"].unsqueeze(-1).expand(token_embeddings.size()).float()
            summed = (token_embeddings * attention_mask).sum(dim=1)
            counts = attention_mask.sum(dim=1).clamp(min=1e-9)
            mean_pooled = summed / counts
            normalized = torch.nn.functional.normalize(mean_pooled, p=2, dim=1)
        all_embeddings.append(normalized.cpu().numpy())

    embeddings = np.vstack(all_embeddings).astype(np.float32)
    np.save(cache_path, embeddings)
    logger.info("Saved embeddings for %s to %s", dataset_name, cache_path)
    return embeddings


def nearest_neighbor_stats(vectors: np.ndarray) -> tuple[dict[str, float], np.ndarray, np.ndarray]:
    if len(vectors) < 2:
        empty = {key: float("nan") for key in ["mean", "median", "p75", "p90", "p95", "max"]}
        return empty, np.array([]), np.array([], dtype=int)
    nn = NearestNeighbors(n_neighbors=2, metric="cosine")
    nn.fit(vectors)
    distances, indices = nn.kneighbors(vectors)
    similarities = 1.0 - distances[:, 1]
    neighbor_indices = indices[:, 1]
    stats = {
        "mean": float(np.mean(similarities)),
        "median": float(np.median(similarities)),
        "p75": float(np.percentile(similarities, 75)),
        "p90": float(np.percentile(similarities, 90)),
        "p95": float(np.percentile(similarities, 95)),
        "max": float(np.max(similarities)),
        "rate_ge_0_80": float(np.mean(similarities >= 0.80)),
        "rate_ge_0_85": float(np.mean(similarities >= 0.85)),
        "rate_ge_0_90": float(np.mean(similarities >= 0.90)),
        "rate_ge_0_95": float(np.mean(similarities >= 0.95)),
    }
    return stats, similarities, neighbor_indices


def tfidf_nn_metrics(df: pd.DataFrame, analyzer: str) -> dict[str, float]:
    if len(df) < 2:
        return {"mean": float("nan"), "p90": float("nan"), "p95": float("nan"), "max": float("nan")}
    if analyzer == "char":
        vectorizer = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), min_df=1)
    else:
        vectorizer = TfidfVectorizer(analyzer="word", ngram_range=(1, 2), min_df=1)
    matrix = vectorizer.fit_transform(df["content"])
    nn = NearestNeighbors(n_neighbors=2, metric="cosine")
    nn.fit(matrix)
    distances, _ = nn.kneighbors(matrix)
    sims = 1.0 - distances[:, 1]
    return {
        "mean": float(np.mean(sims)),
        "p90": float(np.percentile(sims, 90)),
        "p95": float(np.percentile(sims, 95)),
        "max": float(np.max(sims)),
    }


URL_RE = re.compile(r"https?://\S+|www\.\S+|\b[a-zA-Z0-9.-]+\.(?:com|vn|net|org|info)\S*")
PHONE_RE = re.compile(r"(?:\+?84|0)\d{8,10}")
NUM_RE = re.compile(r"\d+")
LEET_CHARS = set("01345789@$!")


def normalize_for_ngram(text: str) -> list[str]:
    text = URL_RE.sub(" URL ", text)
    text = PHONE_RE.sub(" PHONE ", text)
    text = NUM_RE.sub(" NUM ", text)
    return re.findall(r"\w+|URL|PHONE|NUM", text.lower(), flags=re.UNICODE)


def ngram_repetition(df: pd.DataFrame, n: int) -> tuple[dict[str, float], list[tuple[str, int]]]:
    counts: Counter[str] = Counter()
    total = 0
    for text in df["content"]:
        tokens = normalize_for_ngram(text)
        grams = [" ".join(tokens[i : i + n]) for i in range(max(0, len(tokens) - n + 1))]
        counts.update(grams)
        total += len(grams)
    if total == 0:
        return {"total": 0, "unique_ratio": float("nan"), "repeated_mass": float("nan")}, []
    repeated = sum(count for count in counts.values() if count > 1)
    return (
        {
            "total": int(total),
            "unique_ratio": float(len(counts) / total),
            "repeated_mass": float(repeated / total),
        },
        counts.most_common(20),
    )


def exact_masked_duplicate_rate(df: pd.DataFrame) -> float:
    if df.empty:
        return float("nan")
    masked = df["content"].map(lambda x: " ".join(normalize_for_ngram(x)))
    return float(masked.duplicated(keep=False).mean())


def leet_metrics(df: pd.DataFrame) -> dict[str, float]:
    row_with_leet = 0
    leet_tokens = 0
    all_tokens = 0
    leet_density_values: list[float] = []
    special_rows = 0
    special_chars = set("@$!#%&*_=+~/\\|<>")
    for text in df["content"]:
        tokens = re.findall(r"\S+", str(text))
        row_leet_tokens = 0
        for token in tokens:
            has_alpha = any(ch.isalpha() for ch in token)
            has_leet = any(ch in LEET_CHARS for ch in token)
            if has_alpha and has_leet:
                row_leet_tokens += 1
        all_tokens += len(tokens)
        leet_tokens += row_leet_tokens
        row_with_leet += int(row_leet_tokens > 0)
        leet_density_values.append(row_leet_tokens / max(1, len(tokens)))
        special_rows += int(any(ch in special_chars for ch in str(text)))
    denom = max(1, len(df))
    return {
        "row_with_leet_rate": float(row_with_leet / denom),
        "leet_token_rate": float(leet_tokens / max(1, all_tokens)),
        "mean_leet_density": float(np.mean(leet_density_values)) if leet_density_values else float("nan"),
        "special_char_row_rate": float(special_rows / denom),
    }


def row_leet_token_rate(text: str) -> float:
    tokens = re.findall(r"\S+", str(text))
    if not tokens:
        return 0.0
    leet_count = 0
    for token in tokens:
        has_alpha = any(ch.isalpha() for ch in token)
        has_leet = any(ch in LEET_CHARS for ch in token)
        leet_count += int(has_alpha and has_leet)
    return float(leet_count / len(tokens))


def length_metrics(df: pd.DataFrame) -> dict[str, float]:
    lengths = df["content"].str.len().to_numpy()
    if len(lengths) == 0:
        return {key: float("nan") for key in ["mean", "std", "cv", "min", "p50", "p90", "max"]}
    mean = float(np.mean(lengths))
    std = float(np.std(lengths))
    return {
        "mean": mean,
        "std": std,
        "cv": float(std / mean) if mean else float("nan"),
        "min": float(np.min(lengths)),
        "p50": float(np.percentile(lengths, 50)),
        "p90": float(np.percentile(lengths, 90)),
        "max": float(np.max(lengths)),
    }


def bootstrap_ci(values: np.ndarray, reducer, iterations: int, rng: np.random.Generator) -> tuple[float, float]:
    values = np.asarray(values)
    values = values[~pd.isna(values)]
    if len(values) == 0 or iterations <= 0:
        return float("nan"), float("nan")
    stats = []
    for _ in range(iterations):
        sample = rng.choice(values, size=len(values), replace=True)
        stats.append(reducer(sample))
    return float(np.percentile(stats, 2.5)), float(np.percentile(stats, 97.5))


def permutation_p_value(
    phase1_values: np.ndarray,
    current_values: np.ndarray,
    iterations: int,
    rng: np.random.Generator,
) -> float:
    phase1_values = np.asarray(phase1_values)
    current_values = np.asarray(current_values)
    phase1_values = phase1_values[~pd.isna(phase1_values)]
    current_values = current_values[~pd.isna(current_values)]
    if len(phase1_values) == 0 or len(current_values) == 0 or iterations <= 0:
        return float("nan")
    observed = abs(float(np.mean(phase1_values) - np.mean(current_values)))
    pooled = np.concatenate([phase1_values, current_values])
    n_phase1 = len(phase1_values)
    count = 0
    for _ in range(iterations):
        rng.shuffle(pooled)
        diff = abs(float(np.mean(pooled[:n_phase1]) - np.mean(pooled[n_phase1:])))
        count += int(diff >= observed)
    return float((count + 1) / (iterations + 1))


def source_separability_tfidf(df: pd.DataFrame, seed: int, max_samples: int) -> dict[str, float]:
    work = df[df["label"].eq(1)].copy()
    if work.empty:
        return {"roc_auc": float("nan"), "f1": float("nan"), "n": 0}
    if len(work) > max_samples:
        work = (
            work.assign(_synthetic_like=synthetic_like_mask(work).astype(int))
            .groupby("_synthetic_like", group_keys=False)
            .sample(frac=min(1.0, max_samples / len(work)), random_state=seed)
            .drop(columns=["_synthetic_like"])
        )
    y = synthetic_like_mask(work).astype(int).to_numpy()
    if len(np.unique(y)) < 2 or min(np.bincount(y)) < 5:
        return {"roc_auc": float("nan"), "f1": float("nan"), "n": int(len(work))}
    folds = min(5, int(min(np.bincount(y))))
    skf = StratifiedKFold(n_splits=folds, shuffle=True, random_state=seed)
    probs = np.zeros(len(work))
    preds = np.zeros(len(work))
    texts = work["content"].to_numpy()
    for train_idx, test_idx in skf.split(texts, y):
        clf = make_pipeline(
            TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), min_df=2),
            LogisticRegression(max_iter=1000, class_weight="balanced"),
        )
        clf.fit(texts[train_idx], y[train_idx])
        probs[test_idx] = clf.predict_proba(texts[test_idx])[:, 1]
        preds[test_idx] = clf.predict(texts[test_idx])
    return {"roc_auc": float(roc_auc_score(y, probs)), "f1": float(f1_score(y, preds)), "n": int(len(work))}


def source_separability_embedding(
    df: pd.DataFrame,
    embeddings: np.ndarray,
    seed: int,
    max_samples: int,
) -> dict[str, float]:
    mask = df["label"].eq(1).to_numpy()
    x = embeddings[mask]
    work = df.loc[mask].copy()
    y = synthetic_like_mask(work).astype(int).to_numpy()
    if len(x) > max_samples:
        rng = np.random.default_rng(seed)
        chosen = []
        for value in np.unique(y):
            idx = np.flatnonzero(y == value)
            n = max(1, int(round(len(idx) * max_samples / len(y))))
            chosen.extend(rng.choice(idx, min(n, len(idx)), replace=False).tolist())
        chosen = np.array(sorted(chosen))[:max_samples]
        x = x[chosen]
        y = y[chosen]
    if len(x) == 0 or len(np.unique(y)) < 2 or min(np.bincount(y)) < 5:
        return {"roc_auc": float("nan"), "f1": float("nan"), "n": int(len(x))}
    folds = min(5, int(min(np.bincount(y))))
    skf = StratifiedKFold(n_splits=folds, shuffle=True, random_state=seed)
    probs = np.zeros(len(x))
    preds = np.zeros(len(x))
    for train_idx, test_idx in skf.split(x, y):
        clf = make_pipeline(
            StandardScaler(),
            LogisticRegression(max_iter=1000, class_weight="balanced"),
        )
        clf.fit(x[train_idx], y[train_idx])
        probs[test_idx] = clf.predict_proba(x[test_idx])[:, 1]
        preds[test_idx] = clf.predict(x[test_idx])
    return {"roc_auc": float(roc_auc_score(y, probs)), "f1": float(f1_score(y, preds)), "n": int(len(x))}


def distribution_distances(
    df: pd.DataFrame,
    embeddings: np.ndarray | None,
    args: argparse.Namespace,
    rng: np.random.Generator,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    real_mask = df["label"].eq(1).to_numpy() & ~synthetic_like_mask(df).to_numpy()
    synth_mask = df["label"].eq(1).to_numpy() & synthetic_like_mask(df).to_numpy()
    if embeddings is not None and real_mask.sum() > 1 and synth_mask.sum() > 1:
        real = embeddings[real_mask]
        synth = embeddings[synth_mask]
        centroid_sim = cosine_similarity(real.mean(axis=0, keepdims=True), synth.mean(axis=0, keepdims=True))[0, 0]
        rows.append({"metric": "centroid_cosine_distance", "value": float(1.0 - centroid_sim)})

        sample_n = min(args.max_mmd_samples, len(real), len(synth))
        real_sample = real[rng.choice(len(real), sample_n, replace=False)]
        synth_sample = synth[rng.choice(len(synth), sample_n, replace=False)]
        pooled = np.vstack([real_sample, synth_sample])
        dists = pairwise_distances(pooled, metric="euclidean")
        median_dist = np.median(dists[dists > 0])
        gamma = float(1.0 / (2.0 * median_dist**2)) if median_dist > 0 else 1.0
        k_xx = rbf_kernel(real_sample, real_sample, gamma=gamma).mean()
        k_yy = rbf_kernel(synth_sample, synth_sample, gamma=gamma).mean()
        k_xy = rbf_kernel(real_sample, synth_sample, gamma=gamma).mean()
        rows.append({"metric": "mmd_rbf", "value": float(k_xx + k_yy - 2 * k_xy), "gamma": gamma, "sample_n": sample_n})

        pca_dim = min(50, embeddings.shape[1], len(pooled) - 1)
        if pca_dim >= 2:
            pca = PCA(n_components=pca_dim, random_state=args.seed)
            reduced = pca.fit_transform(pooled)
            r = reduced[:sample_n]
            s = reduced[sample_n:]
            mu_r, mu_s = r.mean(axis=0), s.mean(axis=0)
            cov_r = np.cov(r, rowvar=False)
            cov_s = np.cov(s, rowvar=False)
            covmean = sqrtm(cov_r @ cov_s)
            if np.iscomplexobj(covmean):
                covmean = covmean.real
            frechet = np.sum((mu_r - mu_s) ** 2) + np.trace(cov_r + cov_s - 2 * covmean)
            rows.append({"metric": "frechet_pca50", "value": float(frechet), "sample_n": sample_n, "pca_dim": pca_dim})

    for column in OPTIONAL_DISTRIBUTION_COLUMNS:
        if column not in df.columns:
            continue
        real_values = df.loc[real_mask, column].fillna("__NA__").astype(str)
        synth_values = df.loc[synth_mask, column].fillna("__NA__").astype(str)
        keys = sorted(set(real_values) | set(synth_values))
        if not keys:
            continue
        real_dist = np.array([(real_values == key).mean() for key in keys], dtype=float)
        synth_dist = np.array([(synth_values == key).mean() for key in keys], dtype=float)
        rows.append({"metric": f"js_divergence_{column}", "value": float(jensenshannon(real_dist, synth_dist, base=2.0) ** 2)})
    return rows


def top_embedding_pairs(
    df: pd.DataFrame,
    similarities: np.ndarray,
    neighbor_indices: np.ndarray,
    max_pairs: int,
) -> pd.DataFrame:
    if len(similarities) == 0:
        return pd.DataFrame()
    work = df.reset_index(drop=True)
    pair_keys = set()
    rows = []
    for i in np.argsort(-similarities):
        j = int(neighbor_indices[i])
        key = tuple(sorted((int(i), j)))
        if key in pair_keys:
            continue
        pair_keys.add(key)
        rows.append(
            {
                "similarity": float(similarities[i]),
                "sample_id_a": work.loc[i, "sample_id"],
                "sample_id_b": work.loc[j, "sample_id"],
                "content_a": work.loc[i, "content"],
                "content_b": work.loc[j, "content"],
            }
        )
        if len(rows) >= max_pairs:
            break
    return pd.DataFrame(rows)


def artifact_examples(df: pd.DataFrame, max_rows: int = 100) -> pd.DataFrame:
    masked_counts = df["content"].map(lambda x: " ".join(normalize_for_ngram(x))).value_counts()
    rows = []
    for _, row in df.iterrows():
        text = str(row["content"])
        masked = " ".join(normalize_for_ngram(text))
        reasons = []
        if URL_RE.search(text):
            reasons.append("url")
        if PHONE_RE.search(text):
            reasons.append("phone")
        if row_leet_token_rate(text) > 0:
            reasons.append("leet")
        if masked_counts.get(masked, 0) > 1:
            reasons.append("masked_duplicate")
        if reasons:
            rows.append(
                {
                    "sample_id": row.get("sample_id"),
                    "label": row.get("label"),
                    "data_origin": row.get("data_origin"),
                    "artifact_types": "|".join(reasons),
                    "content": text,
                }
            )
        if len(rows) >= max_rows:
            break
    return pd.DataFrame(rows)


def save_figures(
    phase1: pd.DataFrame,
    current: pd.DataFrame,
    phase1_embedding_sims: np.ndarray | None,
    out_dir: Path,
) -> None:
    import matplotlib.pyplot as plt

    plt.figure(figsize=(8, 5))
    plt.hist(phase1["content"].str.len(), bins=60, alpha=0.6, label="phase1")
    plt.hist(current["content"].str.len(), bins=60, alpha=0.6, label="current")
    plt.legend()
    plt.xlabel("content length")
    plt.ylabel("count")
    plt.tight_layout()
    plt.savefig(out_dir / "fig_length_distribution.png", dpi=160)
    plt.close()

    if phase1_embedding_sims is not None and len(phase1_embedding_sims) > 0:
        plt.figure(figsize=(8, 5))
        plt.hist(phase1_embedding_sims, bins=50, color="#3b6ea8")
        plt.xlabel("nearest-neighbor embedding cosine similarity")
        plt.ylabel("count")
        plt.tight_layout()
        plt.savefig(out_dir / "fig_embedding_similarity_hist.png", dpi=160)
        plt.close()

    p1_leet = phase1["content"].map(row_leet_token_rate)
    cur_leet = current["content"].map(row_leet_token_rate)
    plt.figure(figsize=(8, 5))
    plt.hist(p1_leet, bins=30, alpha=0.6, label="phase1")
    plt.hist(cur_leet, bins=30, alpha=0.6, label="current")
    plt.legend()
    plt.xlabel("row leet density")
    plt.ylabel("count")
    plt.tight_layout()
    plt.savefig(out_dir / "fig_leet_density.png", dpi=160)
    plt.close()


def write_csv(path: Path, rows: list[dict[str, Any]] | pd.DataFrame) -> None:
    df = rows if isinstance(rows, pd.DataFrame) else pd.DataFrame(rows)
    df.to_csv(path, index=False, encoding="utf-8-sig")


def main() -> None:
    args = parse_args()
    logger = configure_logging(args.out_dir)
    rng = np.random.default_rng(args.seed)
    logger.info("Technical decision: embedding model defaults to %s from Transformers, not a fine-tuned local checkpoint.", args.embedding_model)

    missing_paths = [str(path) for path in [args.phase1, args.current] if not path.exists()]
    if missing_paths:
        summary = {
            "technical_decisions": {
                "embedding_model": args.embedding_model,
                "embedding_source": "Transformers AutoTokenizer/AutoModel",
                "fine_tuned_phobert_checkpoint_used": False,
            },
            "invariant_checks": [
                {
                    "name": "input_paths",
                    "expected": "all input paths exist",
                    "actual": missing_paths,
                    "severity": "hard",
                    "status": "error",
                }
            ],
        }
        with (args.out_dir / "summary_metrics.json").open("w", encoding="utf-8") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        raise FileNotFoundError(f"Missing input files: {missing_paths}")

    phase1 = read_dataset(args.phase1, "phase1")
    current = read_dataset(args.current, "current")
    invariant_checks = validate_inputs(phase1, current, args, logger)

    phase1_embeddings = current_embeddings = None
    if not args.no_embedding:
        phase1_embeddings = load_embeddings(phase1, "phase1", args, logger)
        current_embeddings = load_embeddings(current, "current", args, logger)

    datasets = {"phase1": phase1, "current": current}
    embeddings = {"phase1": phase1_embeddings, "current": current_embeddings}

    summary_rows: list[dict[str, Any]] = []
    embedding_rows: list[dict[str, Any]] = []
    tfidf_rows: list[dict[str, Any]] = []
    ngram_rows: list[dict[str, Any]] = []
    leet_rows: list[dict[str, Any]] = []
    length_rows: list[dict[str, Any]] = []
    separability_rows: list[dict[str, Any]] = []
    distance_rows: list[dict[str, Any]] = []
    repeated_values: dict[str, np.ndarray] = {}
    leet_values: dict[str, np.ndarray] = {}
    embedding_nn_values: dict[str, np.ndarray] = {}
    phase1_embedding_pairs = pd.DataFrame()

    for dataset_name, df in datasets.items():
        logger.info("Computing slice-level metrics for %s", dataset_name)
        slices = build_slices(df)
        emb = embeddings[dataset_name]
        for slice_name, slice_df in slices.items():
            slice_indices = slice_df.index.to_numpy()
            leet = leet_metrics(slice_df)
            length = length_metrics(slice_df)
            leet_rows.append({"dataset": dataset_name, "slice": slice_name, **leet})
            length_rows.append({"dataset": dataset_name, "slice": slice_name, **length})
            leet_values[f"{dataset_name}:{slice_name}"] = slice_df["content"].map(row_leet_token_rate).to_numpy()

            for n in [5, 6]:
                metrics, top = ngram_repetition(slice_df, n)
                ngram_rows.append(
                    {
                        "dataset": dataset_name,
                        "slice": slice_name,
                        "n": n,
                        "exact_masked_duplicate_rate": exact_masked_duplicate_rate(slice_df),
                        **metrics,
                        "top_repeated_ngrams": json.dumps(top, ensure_ascii=False),
                    }
                )
                repeated_values[f"{dataset_name}:{slice_name}:n{n}"] = np.array([metrics.get("repeated_mass", np.nan)])

            if slice_name.endswith("synthetic_like") or slice_name == "label_1_all":
                for analyzer in ["char", "word"]:
                    tfidf_rows.append({"dataset": dataset_name, "slice": slice_name, "analyzer": analyzer, **tfidf_nn_metrics(slice_df, analyzer)})

            if emb is not None and slice_name == "label_1_synthetic_like":
                slice_emb = emb[slice_indices]
                nn_stats, sims, neighbor_indices = nearest_neighbor_stats(slice_emb)
                embedding_rows.append({"dataset": dataset_name, "slice": slice_name, **nn_stats})
                embedding_nn_values[f"{dataset_name}:{slice_name}"] = sims
                if dataset_name == "phase1":
                    phase1_embedding_pairs = top_embedding_pairs(slice_df, sims, neighbor_indices, args.max_pairs_output)

        logger.info("Computing source separability for %s", dataset_name)
        sep = source_separability_tfidf(df, args.seed, args.max_separability_samples)
        separability_rows.append({"dataset": dataset_name, "feature": "tfidf_char", **sep})
        if emb is not None:
            sep_emb = source_separability_embedding(df, emb, args.seed, args.max_separability_samples)
            separability_rows.append({"dataset": dataset_name, "feature": "embedding", **sep_emb})
            logger.info("Computing distribution distances for %s", dataset_name)
            for row in distribution_distances(df, emb, args, rng):
                distance_rows.append({"dataset": dataset_name, **row})
        else:
            logger.info("Computing distribution distances for %s without embedding metrics", dataset_name)
            for row in distribution_distances(df, None, args, rng):
                distance_rows.append({"dataset": dataset_name, **row})

    for row in embedding_rows:
        key = f"{row['dataset']}:{row['slice']}"
        values = embedding_nn_values.get(key, np.array([]))
        ci_low, ci_high = bootstrap_ci(values, np.mean, args.bootstrap, rng)
        row["ci_low"] = ci_low
        row["ci_high"] = ci_high
        summary_rows.append({"metric_group": "embedding_similarity", **row})

    for row in leet_rows:
        key = f"{row['dataset']}:{row['slice']}"
        values = leet_values.get(key, np.array([]))
        ci_low, ci_high = bootstrap_ci(values, np.mean, args.bootstrap, rng)
        row["leet_token_rate_ci_low"] = ci_low
        row["leet_token_rate_ci_high"] = ci_high
        summary_rows.append({"metric_group": "leet_obfuscation", **row})

    phase1_key = "phase1:label_1_synthetic_like"
    current_key = "current:label_1_synthetic_like"
    if phase1_key in embedding_nn_values and current_key in embedding_nn_values:
        p_value = permutation_p_value(
            embedding_nn_values[phase1_key],
            embedding_nn_values[current_key],
            args.permutations,
            rng,
        )
        summary_rows.append(
            {
                "metric_group": "permutation_test",
                "metric": "embedding_nn_mean_diff_label_1_synthetic_like",
                "p_value": p_value,
            }
        )
    if phase1_key in leet_values and current_key in leet_values:
        p_value = permutation_p_value(leet_values[phase1_key], leet_values[current_key], args.permutations, rng)
        summary_rows.append(
            {
                "metric_group": "permutation_test",
                "metric": "leet_token_rate_diff_label_1_synthetic_like",
                "p_value": p_value,
            }
        )

    write_csv(args.out_dir / "summary_metrics.csv", summary_rows)
    write_csv(args.out_dir / "embedding_similarity_metrics.csv", embedding_rows)
    write_csv(args.out_dir / "embedding_high_similarity_pairs.csv", phase1_embedding_pairs)
    write_csv(args.out_dir / "tfidf_similarity_metrics.csv", tfidf_rows)
    write_csv(args.out_dir / "ngram_repetition_metrics.csv", ngram_rows)
    write_csv(args.out_dir / "leet_obfuscation_metrics.csv", leet_rows)
    write_csv(args.out_dir / "length_distribution_metrics.csv", length_rows)
    write_csv(args.out_dir / "source_separability_metrics.csv", separability_rows)
    write_csv(args.out_dir / "distribution_distance_metrics.csv", distance_rows)
    write_csv(args.out_dir / "artifact_examples.csv", artifact_examples(phase1))

    phase1_sims = embedding_nn_values.get("phase1:label_1_synthetic_like")
    save_figures(phase1, current, phase1_sims, args.out_dir)

    summary = {
        "technical_decisions": {
            "embedding_model": args.embedding_model,
            "embedding_source": "Transformers AutoTokenizer/AutoModel",
            "fine_tuned_phobert_checkpoint_used": False,
            "pooling": "L2-normalized mean pooling over last_hidden_state with attention mask",
            "cache_embeddings": True,
            "strict_invariants": bool(args.strict_invariants),
        },
        "inputs": {
            "phase1": str(args.phase1),
            "current": str(args.current),
        },
        "invariant_checks": invariant_checks,
        "summary_rows": summary_rows,
    }
    with (args.out_dir / "summary_metrics.json").open("w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    logger.info("Audit complete. Outputs written to %s", args.out_dir)


if __name__ == "__main__":
    main()

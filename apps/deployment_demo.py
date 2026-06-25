"""ViSmish deployment demo app.

Run:
    streamlit run apps/deployment_demo.py

The app focuses on RQ4-style deployment trade-off:
- manual SMS inference,
- test-set sample inference,
- batch benchmark with latency, throughput, model size, and quality metrics.
"""

from __future__ import annotations

import math
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import numpy as np
import pandas as pd
import psutil
import streamlit as st
import torch
from sklearn.metrics import (
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from torch import nn
from torch.utils.data import DataLoader, Dataset


ROOT = Path(__file__).resolve().parents[1]
TEST_SPLIT = ROOT / "data" / "distillation" / "benchmark_splits" / "test.csv"
TEXTCNN_HARD = (
    ROOT
    / "setup_results"
    / "textcnn_distillation_study"
    / "phobert-base"
    / "hard"
    / "seed_42"
    / "char_textcnn_hard_seed_42_model.pt"
)
TEXTCNN_KD = (
    ROOT
    / "setup_results"
    / "textcnn_distillation_study"
    / "phobert-base"
    / "risk_aware_kd"
    / "seed_42"
    / "char_textcnn_risk_aware_kd_seed_42_model.pt"
)


@dataclass(frozen=True)
class StudentSpec:
    key: str
    display_name: str
    checkpoint: Path
    note: str


@dataclass(frozen=True)
class TeacherSpec:
    key: str
    display_name: str
    output_csv: Path
    model_dir: Path
    note: str


TEACHER_SPECS = [
    TeacherSpec(
        key="phobert",
        display_name="PhoBERT-base teacher",
        output_csv=ROOT
        / "data"
        / "distillation"
        / "benchmark_teacher_outputs"
        / "phobert-base"
        / "test_teacher.csv",
        model_dir=ROOT
        / "setup_results"
        / "distillation_benchmark"
        / "plm_phobert-base"
        / "model",
        note="Precomputed benchmark teacher output; local weights may be unavailable.",
    ),
    TeacherSpec(
        key="cafebert",
        display_name="CafeBERT teacher",
        output_csv=ROOT
        / "setup_results"
        / "distillation_benchmark"
        / "benchmark_teacher_outputs"
        / "cafebert_teacher"
        / "test_teacher.csv",
        model_dir=ROOT
        / "setup_results"
        / "distillation_benchmark"
        / "cafebert_teacher"
        / "model",
        note="Local teacher weights and precomputed test outputs are available.",
    ),
    TeacherSpec(
        key="viclsr",
        display_name="ViCLSR teacher",
        output_csv=ROOT
        / "setup_results"
        / "distillation_benchmark"
        / "benchmark_teacher_outputs"
        / "viclsr_teacher"
        / "test_teacher.csv",
        model_dir=ROOT
        / "setup_results"
        / "distillation_benchmark"
        / "viclsr_teacher"
        / "model",
        note="Local teacher weights and precomputed test outputs are available.",
    ),
]


STUDENT_SPECS = [
    StudentSpec(
        key="textcnn_hard",
        display_name="TextCNN hard",
        checkpoint=TEXTCNN_HARD,
        note="Student baseline trained with hard labels.",
    ),
    StudentSpec(
        key="textcnn_kd",
        display_name="TextCNN risk-aware KD",
        checkpoint=TEXTCNN_KD,
        note="Student trained with PhoBERT soft labels.",
    ),
]


st.set_page_config(
    page_title="ViSmish Deployment Demo",
    page_icon="SMS",
    layout="wide",
)


st.markdown(
    """
<style>
body, .stApp { background: #f8fafc; }
.hero {
    border-bottom: 1px solid #d9e2ec;
    padding: 0.25rem 0 1rem 0;
    margin-bottom: 1rem;
}
.hero h1 {
    color: #14365d;
    font-size: 2rem;
    margin-bottom: 0.25rem;
}
.hero p {
    color: #52606d;
    margin: 0;
}
.metric-note {
    color: #52606d;
    font-size: 0.9rem;
}
.ok-badge {
    color: #166534;
    background: #dcfce7;
    padding: 0.15rem 0.45rem;
    border-radius: 0.35rem;
    font-weight: 700;
}
.bad-badge {
    color: #991b1b;
    background: #fee2e2;
    padding: 0.15rem 0.45rem;
    border-radius: 0.35rem;
    font-weight: 700;
}
.muted {
    color: #64748b;
}
</style>
""",
    unsafe_allow_html=True,
)


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


def encode_text(text: str, vocab: dict[str, int], max_len: int) -> list[int]:
    ids = [vocab.get(char, 1) for char in str(text).lower()[:max_len]]
    ids.extend([0] * max(0, max_len - len(ids)))
    return ids[:max_len]


def file_or_dir_size_mb(path: Path) -> float | None:
    if not path.exists():
        return None
    if path.is_file():
        return path.stat().st_size / (1024 * 1024)
    return sum(p.stat().st_size for p in path.rglob("*") if p.is_file()) / (1024 * 1024)


def count_params(model: nn.Module) -> int:
    return sum(param.numel() for param in model.parameters())


def checkpoint_exists(path: Path) -> str:
    return "found" if path.exists() else "missing"


def teacher_weights_available(path: Path) -> bool:
    return path.exists() and any(
        (path / name).exists()
        for name in ("pytorch_model.bin", "model.safetensors", "tf_model.h5")
    )


def teacher_by_display_name(display_name: str) -> TeacherSpec:
    for spec in TEACHER_SPECS:
        if spec.display_name == display_name:
            return spec
    raise KeyError(display_name)


@st.cache_data(show_spinner=False)
def load_test_data() -> pd.DataFrame:
    df = pd.read_csv(TEST_SPLIT)
    df["content"] = df["content"].fillna("").astype(str)
    df["label"] = df["label"].astype(int)
    return df


@st.cache_data(show_spinner=False)
def load_teacher_test(output_csv: str) -> pd.DataFrame | None:
    path = Path(output_csv)
    if not path.exists():
        return None
    df = pd.read_csv(path)
    df["sample_id"] = df["sample_id"].astype(str)
    df["label"] = df["label"].astype(int)
    df["teacher_pred"] = df["teacher_pred"].astype(int)
    return df


@st.cache_resource(show_spinner=False)
def load_student(checkpoint_path: str) -> tuple[nn.Module, dict[str, int], dict, float]:
    start = time.perf_counter()
    checkpoint = torch.load(checkpoint_path, map_location="cpu", weights_only=False)
    config = checkpoint["config"]
    vocab = checkpoint["vocab"]
    kernel_sizes = [int(size) for size in str(config["kernel_sizes"]).split(",")]
    model = CharTextCnn(
        vocab_size=len(vocab),
        embed_dim=int(config["embed_dim"]),
        num_filters=int(config["num_filters"]),
        kernel_sizes=kernel_sizes,
        dropout=float(config["dropout"]),
    )
    model.load_state_dict(checkpoint["model_state_dict"])
    model.eval()
    load_ms = (time.perf_counter() - start) * 1000
    return model, vocab, config, load_ms


@st.cache_resource(show_spinner=False)
def load_teacher_live(model_dir: str):
    from transformers import AutoModelForSequenceClassification, AutoTokenizer

    start = time.perf_counter()
    # Some saved CafeBERT/ViCLSR tokenizer configs store
    # `extra_special_tokens` as a list, while recent transformers expects a
    # mapping. Overriding it keeps the artifact untouched and avoids a live-demo
    # crash during AutoTokenizer initialization.
    tokenizer = AutoTokenizer.from_pretrained(model_dir, extra_special_tokens={})
    model = AutoModelForSequenceClassification.from_pretrained(model_dir)
    model.eval()
    load_ms = (time.perf_counter() - start) * 1000
    return tokenizer, model, load_ms


@torch.no_grad()
def predict_student(
    model: nn.Module,
    texts: list[str],
    vocab: dict[str, int],
    max_len: int,
    batch_size: int = 128,
) -> np.ndarray:
    loader = DataLoader(CharDataset(texts, vocab, max_len), batch_size=batch_size)
    probs = []
    for x in loader:
        logits = model(x)
        probs.append(torch.sigmoid(logits).cpu().numpy())
    return np.concatenate(probs)


@torch.no_grad()
def predict_teacher_live(tokenizer, model, texts: list[str], batch_size: int = 16) -> np.ndarray:
    probs = []
    for start in range(0, len(texts), batch_size):
        batch = texts[start : start + batch_size]
        encoded = tokenizer(
            batch,
            padding=True,
            truncation=True,
            max_length=256,
            return_tensors="pt",
        )
        logits = model(**encoded).logits
        probs.append(torch.softmax(logits, dim=-1)[:, 1].cpu().numpy())
    return np.concatenate(probs)


def measure_latency(call: Callable[[], np.ndarray], warmup: int, runs: int) -> tuple[np.ndarray, float]:
    for _ in range(warmup):
        call()
    elapsed = []
    last = None
    for _ in range(runs):
        start = time.perf_counter()
        last = call()
        elapsed.append((time.perf_counter() - start) * 1000)
    return last if last is not None else call(), float(np.mean(elapsed))


def binary_metrics(y_true: np.ndarray, y_pred: np.ndarray, p1: np.ndarray) -> dict[str, float | int]:
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    return {
        "F1 Label 1": f1_score(y_true, y_pred, pos_label=1, zero_division=0),
        "Recall Label 1": recall_score(y_true, y_pred, pos_label=1, zero_division=0),
        "Precision Label 1": precision_score(y_true, y_pred, pos_label=1, zero_division=0),
        "FP": int(fp),
        "FN": int(fn),
        "Avg P(smishing)": float(np.mean(p1)) if len(p1) else math.nan,
    }


def format_label(pred: int) -> str:
    return "SMISHING" if int(pred) == 1 else "BENIGN"


def prediction_badge(pred: int) -> str:
    cls = "bad-badge" if int(pred) == 1 else "ok-badge"
    return f'<span class="{cls}">{format_label(pred)}</span>'


def model_status_table() -> pd.DataFrame:
    rows = [
        {
            "Model": spec.display_name,
            "Mode": "live inference",
            "Artifact": checkpoint_exists(spec.checkpoint),
            "Size MB": file_or_dir_size_mb(spec.checkpoint),
        }
        for spec in STUDENT_SPECS
    ]
    for spec in TEACHER_SPECS:
        rows.append(
            {
                "Model": spec.display_name,
                "Mode": "precomputed test; optional live if weights exist",
                "Artifact": (
                    "weights + test outputs"
                    if teacher_weights_available(spec.model_dir)
                    else "precomputed only"
                ),
                "Size MB": file_or_dir_size_mb(spec.model_dir),
            }
        )
    return pd.DataFrame(rows)


def run_student_models(
    texts: list[str],
    threshold: float,
    batch_size: int,
    warmup: int,
    runs: int,
) -> list[dict]:
    rows = []
    for spec in STUDENT_SPECS:
        if not spec.checkpoint.exists():
            rows.append(
                {
                    "Model": spec.display_name,
                    "Status": "missing checkpoint",
                }
            )
            continue
        model, vocab, config, load_ms = load_student(str(spec.checkpoint))
        max_len = int(config.get("max_len", 256))

        def call() -> np.ndarray:
            return predict_student(model, texts, vocab, max_len, batch_size=batch_size)

        with MemorySampler() as sampler:
            p1, latency_total_ms = measure_latency(call, warmup=warmup, runs=runs)
        pred = (p1 >= threshold).astype(int)
        rows.append(
            {
                "Model": spec.display_name,
                "Status": "live",
                "P(smishing)": p1,
                "Pred": pred,
                "Latency total ms": latency_total_ms,
                "Latency ms/msg": latency_total_ms / max(len(texts), 1),
                "Throughput msg/s": 1000 * len(texts) / latency_total_ms
                if latency_total_ms > 0
                else math.nan,
                "Peak RAM MB": sampler.peak_mb,
                "Load time ms": load_ms,
                "Params": count_params(model),
                "Size MB": file_or_dir_size_mb(spec.checkpoint),
                "Note": spec.note,
            }
        )
    return rows


def run_teacher_live_if_available(
    spec: TeacherSpec,
    texts: list[str],
    threshold: float,
    batch_size: int,
    warmup: int,
    runs: int,
) -> dict | None:
    if not teacher_weights_available(spec.model_dir):
        return None
    try:
        tokenizer, model, load_ms = load_teacher_live(str(spec.model_dir))
    except Exception as exc:
        return {
            "Model": spec.display_name,
            "Status": "load_error",
            "Note": f"Live teacher load failed: {exc}",
        }

    def call() -> np.ndarray:
        return predict_teacher_live(tokenizer, model, texts, batch_size=batch_size)

    try:
        with MemorySampler() as sampler:
            p1, latency_total_ms = measure_latency(call, warmup=warmup, runs=runs)
    except Exception as exc:
        return {
            "Model": spec.display_name,
            "Status": "inference_error",
            "Note": f"Live teacher inference failed: {exc}",
        }
    return {
        "Model": spec.display_name,
        "Status": "live",
        "P(smishing)": p1,
        "Pred": (p1 >= threshold).astype(int),
        "Latency total ms": latency_total_ms,
        "Latency ms/msg": latency_total_ms / max(len(texts), 1),
        "Throughput msg/s": 1000 * len(texts) / latency_total_ms
        if latency_total_ms > 0
        else math.nan,
        "Peak RAM MB": sampler.peak_mb,
        "Load time ms": load_ms,
        "Params": count_params(model),
        "Size MB": file_or_dir_size_mb(spec.model_dir),
        "Note": "Teacher live inference.",
    }


def teacher_precomputed_for_ids(spec: TeacherSpec, sample_ids: list[str]) -> pd.DataFrame | None:
    teacher_df = load_teacher_test(str(spec.output_csv))
    if teacher_df is None:
        return None
    subset = teacher_df[teacher_df["sample_id"].astype(str).isin(sample_ids)].copy()
    if subset.empty:
        return None
    return subset


st.markdown(
    """
<div class="hero">
  <h1>ViSmish Deployment Demo</h1>
  <p>Manual prediction, test-set inspection, and CPU deployment trade-off for TextCNN hard vs TextCNN KD, with teacher outputs from PhoBERT/CafeBERT/ViCLSR.</p>
</div>
""",
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("Demo controls")
    threshold = st.slider("Decision threshold", 0.1, 0.9, 0.5, 0.05)
    batch_size = st.slider("Batch size", 1, 256, 128, 1)
    warmup_runs = st.slider("Warmup runs", 0, 5, 2, 1)
    latency_runs = st.slider("Measured runs", 1, 10, 3, 1)
    st.caption("Latency is measured after warmup on the current machine.")
    selected_teacher_names = st.multiselect(
        "Teacher outputs to show",
        options=[spec.display_name for spec in TEACHER_SPECS],
        default=[spec.display_name for spec in TEACHER_SPECS],
    )
    live_teacher_name = st.selectbox(
        "Optional live teacher for manual/batch",
        options=["Skip live teacher"] + [spec.display_name for spec in TEACHER_SPECS],
        index=0,
        help="Teacher models are large. Keep this skipped unless you need to prove live teacher inference.",
    )
    st.divider()
    st.subheader("Artifact status")
    status_df = model_status_table()
    st.dataframe(
        status_df.assign(**{"Size MB": status_df["Size MB"].map(lambda x: None if pd.isna(x) else round(x, 3))}),
        hide_index=True,
        width="stretch",
    )


test_df = load_test_data()
selected_teacher_specs = [teacher_by_display_name(name) for name in selected_teacher_names]
teacher_output_count = sum(
    1 for spec in selected_teacher_specs if load_teacher_test(str(spec.output_csv)) is not None
)

summary_cols = st.columns(4)
summary_cols[0].metric("Test rows", f"{len(test_df):,}")
summary_cols[1].metric("Label 1", f"{int(test_df['label'].sum()):,}")
summary_cols[2].metric("Label 0", f"{int((test_df['label'] == 0).sum()):,}")
summary_cols[3].metric("Teacher outputs", f"{teacher_output_count}/{len(selected_teacher_specs)}")

tab_manual, tab_test, tab_batch = st.tabs(
    ["Manual SMS", "Test sample", "Batch deployment benchmark"]
)

with tab_manual:
    st.subheader("Manual SMS inference")
    st.markdown(
        '<p class="metric-note">TextCNN models run live from checkpoint. Teacher live inference is optional because CafeBERT/ViCLSR/PhoBERT are large.</p>',
        unsafe_allow_html=True,
    )
    default_text = (
        "Tai khoan cua quy khach se bi khoa trong 24h. "
        "Vui long truy cap https://secure-vpb.example/xacminh de cap nhat thong tin."
    )
    manual_text = st.text_area("SMS content", value=default_text, height=120)
    if st.button("Run manual prediction", type="primary"):
        texts = [manual_text.strip()] if manual_text.strip() else []
        if not texts:
            st.warning("Please enter one SMS.")
        else:
            rows = run_student_models(
                texts,
                threshold=threshold,
                batch_size=batch_size,
                warmup=warmup_runs,
                runs=latency_runs,
            )
            if live_teacher_name != "Skip live teacher":
                live_teacher = teacher_by_display_name(live_teacher_name)
                teacher_live = run_teacher_live_if_available(
                    live_teacher,
                    texts,
                    threshold=threshold,
                    batch_size=min(batch_size, 16),
                    warmup=warmup_runs,
                    runs=latency_runs,
                )
                if teacher_live is not None:
                    rows.insert(0, teacher_live)
                else:
                    rows.insert(
                        0,
                        {
                            "Model": live_teacher.display_name,
                            "Status": "not loaded",
                            "Note": "Local teacher weights are unavailable or failed to load; manual teacher inference is skipped.",
                        },
                    )

            display_rows = []
            for row in rows:
                if "P(smishing)" not in row:
                    display_rows.append(
                        {
                            "Model": row["Model"],
                            "Prediction": "N/A",
                            "P(smishing)": None,
                            "Latency ms/msg": None,
                            "Status": row["Status"],
                            "Note": row.get("Note", ""),
                        }
                    )
                    continue
                display_rows.append(
                    {
                        "Model": row["Model"],
                        "Prediction": format_label(int(row["Pred"][0])),
                        "P(smishing)": float(row["P(smishing)"][0]),
                        "Latency ms/msg": row["Latency ms/msg"],
                        "Status": row["Status"],
                        "Note": row.get("Note", ""),
                    }
                )
            st.dataframe(pd.DataFrame(display_rows), hide_index=True, width="stretch")

with tab_test:
    st.subheader("Inspect a locked test-set sample")
    test_df_view = test_df.copy()
    test_df_view["short"] = test_df_view.apply(
        lambda row: f"{row['sample_id']} | y={row['label']} | {str(row['content'])[:90]}",
        axis=1,
    )
    sample_selector = st.selectbox(
        "Choose sample",
        options=test_df_view["short"].tolist(),
        index=0,
    )
    sample_id = sample_selector.split(" | ", 1)[0]
    sample = test_df[test_df["sample_id"].astype(str) == sample_id].iloc[0]
    st.write("**Content**")
    st.info(sample["content"])
    meta_cols = st.columns(5)
    meta_cols[0].metric("Label", int(sample["label"]))
    meta_cols[1].metric("Sender", str(sample.get("sender_type", "")))
    meta_cols[2].metric("Has URL", str(sample.get("has_url", "")))
    meta_cols[3].metric("Has phone", str(sample.get("has_phone_number", "")))
    meta_cols[4].metric("Origin", str(sample.get("data_origin", "")))

    if st.button("Run selected sample", type="primary"):
        texts = [str(sample["content"])]
        rows = run_student_models(
            texts,
            threshold=threshold,
            batch_size=batch_size,
            warmup=warmup_runs,
            runs=latency_runs,
        )
        display_rows = []
        for spec in selected_teacher_specs:
            teacher_subset = teacher_precomputed_for_ids(spec, [str(sample_id)])
            if teacher_subset is None:
                continue
            teacher_row = teacher_subset.iloc[0]
            display_rows.append(
                    {
                        "Model": spec.display_name,
                        "Mode": "precomputed test output",
                        "Prediction": format_label(int(teacher_row["teacher_pred"])),
                        "P(smishing)": float(teacher_row["teacher_p1_t1"]),
                        "Confidence": float(teacher_row["teacher_confidence"]),
                        "Latency ms/msg": None,
                    }
                )
        for row in rows:
            if "P(smishing)" not in row:
                continue
            display_rows.append(
                {
                    "Model": row["Model"],
                    "Mode": "live inference",
                    "Prediction": format_label(int(row["Pred"][0])),
                    "P(smishing)": float(row["P(smishing)"][0]),
                    "Confidence": max(float(row["P(smishing)"][0]), 1.0 - float(row["P(smishing)"][0])),
                    "Latency ms/msg": row["Latency ms/msg"],
                }
            )
        st.dataframe(pd.DataFrame(display_rows), hide_index=True, width="stretch")

with tab_batch:
    st.subheader("Batch deployment benchmark")
    st.markdown(
        '<p class="metric-note">Run on a subset of the locked test split. TextCNN models are measured live; selected teachers are reported from precomputed test outputs unless optional live inference is enabled.</p>',
        unsafe_allow_html=True,
    )
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        sample_n = st.slider("Number of test rows", 10, int(len(test_df)), min(100, int(len(test_df))), 10)
    with col_b:
        only_real = st.checkbox("Only real-origin rows", value=False)
    with col_c:
        include_teacher_live = st.checkbox(
            "Try optional live teacher runtime",
            value=False,
            help="This requires local teacher weights and may be slow.",
        )

    candidate_df = test_df[test_df["data_origin"].eq("real")] if only_real else test_df
    batch_df = candidate_df.head(sample_n).copy()
    st.caption(
        f"Selected {len(batch_df)} rows; label 1 = {int(batch_df['label'].sum())}, label 0 = {int((batch_df['label'] == 0).sum())}."
    )

    if st.button("Run batch benchmark", type="primary"):
        texts = batch_df["content"].astype(str).tolist()
        labels = batch_df["label"].astype(int).to_numpy()
        rows = run_student_models(
            texts,
            threshold=threshold,
            batch_size=batch_size,
            warmup=warmup_runs,
            runs=latency_runs,
        )

        result_rows = []
        for spec in selected_teacher_specs:
            teacher_subset = teacher_precomputed_for_ids(
                spec,
                batch_df["sample_id"].astype(str).tolist(),
            )
            if teacher_subset is None:
                continue
            teacher_subset = teacher_subset.set_index("sample_id").loc[
                batch_df["sample_id"].astype(str).tolist()
            ]
            teacher_p1 = teacher_subset["teacher_p1_t1"].astype(float).to_numpy()
            teacher_pred = teacher_subset["teacher_pred"].astype(int).to_numpy()
            metrics = binary_metrics(labels, teacher_pred, teacher_p1)
            result_rows.append(
                {
                    "Model": spec.display_name,
                    "Inference": "precomputed test output",
                    "Size MB": file_or_dir_size_mb(spec.model_dir),
                    "Params": None,
                    "Load time ms": None,
                    "Latency ms/msg": None,
                    "Throughput msg/s": None,
                    "Peak RAM MB": None,
                    **metrics,
                }
            )

        if include_teacher_live:
            if live_teacher_name == "Skip live teacher":
                st.warning("Choose a live teacher in the sidebar before enabling live teacher runtime.")
            else:
                live_teacher = teacher_by_display_name(live_teacher_name)
                teacher_live = run_teacher_live_if_available(
                    live_teacher,
                    texts,
                    threshold=threshold,
                    batch_size=min(batch_size, 16),
                    warmup=warmup_runs,
                    runs=latency_runs,
                )
                if teacher_live is not None and "P(smishing)" in teacher_live:
                    metrics = binary_metrics(labels, teacher_live["Pred"], teacher_live["P(smishing)"])
                    result_rows.append(
                        {
                            "Model": teacher_live["Model"],
                            "Inference": "live",
                            "Size MB": teacher_live["Size MB"],
                            "Params": teacher_live["Params"],
                            "Load time ms": teacher_live["Load time ms"],
                            "Latency ms/msg": teacher_live["Latency ms/msg"],
                            "Throughput msg/s": teacher_live["Throughput msg/s"],
                            "Peak RAM MB": teacher_live["Peak RAM MB"],
                            **metrics,
                        }
                    )
                else:
                    st.warning(f"{live_teacher.display_name} live runtime skipped because weights are unavailable or failed to load.")

        for row in rows:
            if "P(smishing)" not in row:
                continue
            metrics = binary_metrics(labels, row["Pred"], row["P(smishing)"])
            result_rows.append(
                {
                    "Model": row["Model"],
                    "Inference": "live",
                    "Size MB": row["Size MB"],
                    "Params": row["Params"],
                    "Load time ms": row["Load time ms"],
                    "Latency ms/msg": row["Latency ms/msg"],
                    "Throughput msg/s": row["Throughput msg/s"],
                    "Peak RAM MB": row["Peak RAM MB"],
                    **metrics,
                }
            )

        result_df = pd.DataFrame(result_rows)
        numeric_cols = [
            "Size MB",
            "Load time ms",
            "Latency ms/msg",
            "Throughput msg/s",
            "Peak RAM MB",
            "F1 Label 1",
            "Recall Label 1",
            "Precision Label 1",
            "Avg P(smishing)",
        ]
        for col in numeric_cols:
            if col in result_df:
                result_df[col] = result_df[col].map(lambda x: None if pd.isna(x) else round(float(x), 4))
        st.dataframe(result_df, hide_index=True, width="stretch")

        st.markdown(
            """
**Interpretation cue for the defense**

- TextCNN hard and TextCNN KD have similar size/latency because they share the same architecture.
- KD changes the training signal, not the inference architecture.
- The deployment trade-off is therefore: keep low inference cost while trying to improve quality metrics such as Recall/F1 for label 1.
"""
        )

        csv = result_df.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")
        st.download_button(
            "Download benchmark CSV",
            data=csv,
            file_name="vismish_deployment_demo_benchmark.csv",
            mime="text/csv",
        )

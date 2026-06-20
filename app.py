"""
ViSmish Demo — Phát hiện SMS lừa đảo tiếng Việt
Hỗ trợ 3 mô hình: PhoBERT (teacher) + 2 Student distilled từ PhoBERT
"""

import streamlit as st
import pandas as pd
import numpy as np
import time
import torch
import os
from pathlib import Path
from torch import nn
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="ViSmish — SMS Phishing Detector",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* Font */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Background */
.stApp {
    background-color: #0f1117;
    color: #e2e8f0;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #161b27;
    border-right: 1px solid #1e293b;
}

/* Header banner */
.header-banner {
    background: linear-gradient(135deg, #0f2942 0%, #1a1f35 60%, #0f1117 100%);
    border: 1px solid #1e3a5f;
    border-radius: 12px;
    padding: 28px 32px;
    margin-bottom: 24px;
}
.header-banner h1 {
    font-size: 1.75rem;
    font-weight: 700;
    color: #f1f5f9;
    margin: 0 0 6px 0;
    letter-spacing: -0.5px;
}
.header-banner p {
    color: #64748b;
    margin: 0;
    font-size: 0.9rem;
}
.header-tag {
    display: inline-block;
    background: #1e3a5f;
    color: #60a5fa;
    font-size: 0.72rem;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 20px;
    letter-spacing: 0.5px;
    margin-bottom: 10px;
}

/* Cards */
.result-card {
    background: #161b27;
    border: 1px solid #1e293b;
    border-radius: 10px;
    padding: 16px 20px;
    margin-bottom: 10px;
    position: relative;
}
.result-card.smishing {
    border-left: 4px solid #ef4444;
}
.result-card.ham {
    border-left: 4px solid #22c55e;
}
.badge-smishing {
    display: inline-block;
    background: #450a0a;
    color: #f87171;
    font-weight: 600;
    font-size: 0.72rem;
    padding: 3px 10px;
    border-radius: 20px;
    letter-spacing: 0.4px;
}
.badge-ham {
    display: inline-block;
    background: #052e16;
    color: #4ade80;
    font-weight: 600;
    font-size: 0.72rem;
    padding: 3px 10px;
    border-radius: 20px;
    letter-spacing: 0.4px;
}
.sms-content {
    font-size: 0.88rem;
    color: #cbd5e1;
    margin: 8px 0 10px 0;
    line-height: 1.6;
    font-family: 'Inter', sans-serif;
}
.meta-row {
    display: flex;
    gap: 16px;
    font-size: 0.78rem;
    color: #475569;
}
.meta-row span {
    font-family: 'JetBrains Mono', monospace;
}
.prob-high { color: #f87171; }
.prob-low  { color: #4ade80; }

/* Timing box */
.timing-box {
    background: #161b27;
    border: 1px solid #1e293b;
    border-radius: 10px;
    padding: 16px 20px;
    text-align: center;
}
.timing-box .time-val {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.8rem;
    font-weight: 600;
    color: #60a5fa;
}
.timing-box .time-label {
    font-size: 0.78rem;
    color: #475569;
    margin-top: 4px;
}
.timing-box .time-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    color: #334155;
    margin-top: 2px;
}

/* Section label */
.section-label {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 1px;
    color: #334155;
    text-transform: uppercase;
    margin-bottom: 10px;
    margin-top: 20px;
}

/* Divider */
hr { border-color: #1e293b; }

/* Threshold slider label */
.threshold-note {
    font-size: 0.78rem;
    color: #475569;
    margin-top: -8px;
    margin-bottom: 16px;
}

/* Summary stat */
.stat-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 0;
    border-bottom: 1px solid #1e293b;
    font-size: 0.85rem;
}
.stat-row:last-child { border-bottom: none; }
.stat-val {
    font-family: 'JetBrains Mono', monospace;
    font-weight: 600;
    color: #e2e8f0;
}

/* Model badge in sidebar */
.model-info-box {
    background: #0f1929;
    border: 1px solid #1e3a5f;
    border-radius: 8px;
    padding: 12px 14px;
    font-size: 0.8rem;
    color: #64748b;
    margin-top: 8px;
}
.model-info-box b { color: #93c5fd; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# MODEL DEFINITIONS
# ─────────────────────────────────────────────
MODEL_OPTIONS = {
    "   PhoBERT (Teacher)": {
        "key": "phobert_teacher",
        "desc": "vinai/phobert-base — mô hình gốc, độ chính xác cao nhất",
        "type": "teacher",
        "path": "./setup_results/distillation_benchmark/plm_phobert-base/model",
    },
    "   Student 1 (Distilled)": {
        "key": "student_1",
        "desc": "Character-level TextCNN distilled từ PhoBERT",
        "type": "student",
        "path": "./setup_results/distillation_benchmark/char_models/char_textcnn_distilled_phobert_base/char_textcnn_distilled_phobert_base_model.pt",
    },
    "   Student 2 (Distilled)": {
        "key": "student_2",
        "desc": "Character-level BiLSTM distilled từ PhoBERT",
        "type": "student",
        "path": "./setup_results/distillation_benchmark/char_models/char_bilstm_distilled_phobert_base/char_bilstm_distilled_phobert_base_model.pt",
    },
}

# ─────────────────────────────────────────────
# LOAD MODEL (cached)
# ─────────────────────────────────────────────
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


def resolve_student_checkpoint(model_path: str) -> Path:
    path = Path(model_path)
    if path.is_file():
        return path
    if path.is_dir():
        checkpoints = sorted(path.glob("*_model.pt"))
        if len(checkpoints) == 1:
            return checkpoints[0]
        if not checkpoints:
            raise FileNotFoundError(f"Không tìm thấy file '*_model.pt' trong {path}")
        raise ValueError(f"Có nhiều checkpoint trong {path}; vui lòng chọn trực tiếp một file .pt")
    raise FileNotFoundError(f"Không tìm thấy checkpoint: {path}")


@st.cache_resource(show_spinner=False)
def load_model(model_path: str, model_type: str):
    """Load teacher Hugging Face hoặc student character-level từ local checkpoint."""
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    if model_type == "teacher":
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        model = AutoModelForSequenceClassification.from_pretrained(model_path)
        vocab = None
        config = {"max_len": 256}
    else:
        checkpoint_path = resolve_student_checkpoint(model_path)
        checkpoint = torch.load(checkpoint_path, map_location="cpu", weights_only=False)
        config = checkpoint["config"]
        vocab = checkpoint["vocab"]
        architecture = str(config.get("architecture", "bilstm")).lower()

        if architecture == "textcnn":
            kernel_sizes = [
                int(size.strip())
                for size in str(config["kernel_sizes"]).split(",")
                if size.strip()
            ]
            model = CharTextCnn(
                vocab_size=len(vocab),
                embed_dim=int(config["embed_dim"]),
                num_filters=int(config["num_filters"]),
                kernel_sizes=kernel_sizes,
                dropout=float(config["dropout"]),
            )
        elif architecture == "bilstm":
            model = CharBiLstm(
                vocab_size=len(vocab),
                embed_dim=int(config["embed_dim"]),
                hidden_dim=int(config["hidden_dim"]),
                dropout=float(config["dropout"]),
            )
        else:
            raise ValueError(f"Kiến trúc student không được hỗ trợ: {architecture}")

        model.load_state_dict(checkpoint["model_state_dict"], strict=True)
        tokenizer = None

    model.eval()
    model.to(device)
    parameter_count = sum(parameter.numel() for parameter in model.parameters())
    return tokenizer, model, device, vocab, config, parameter_count


def encode_student_texts(
    texts: list[str],
    vocab: dict[str, int],
    max_len: int,
    device: torch.device,
) -> torch.Tensor:
    encoded = []
    for text in texts:
        ids = [vocab.get(char, 1) for char in text.lower()[:max_len]]
        ids.extend([0] * (max_len - len(ids)))
        encoded.append(ids)
    return torch.tensor(encoded, dtype=torch.long, device=device)


def predict_batch(
    texts: list[str],
    tokenizer,
    model,
    device,
    threshold: float,
    model_type: str,
    vocab=None,
    config=None,
):
    """
    Chạy inference trên danh sách texts.
    Trả về (labels, probabilities, total_time_ms, per_sample_ms)
    """
    t0 = time.perf_counter()

    with torch.no_grad():
        if model_type == "student":
            if vocab is None:
                raise ValueError("Checkpoint student không chứa vocabulary")
            max_len = int((config or {}).get("max_len", 256))
            inputs = encode_student_texts(texts, vocab, max_len, device)
            logits = model(inputs)
            probs = torch.sigmoid(logits).cpu().numpy()
        else:
            inputs = tokenizer(
                texts,
                padding=True,
                truncation=True,
                max_length=256,
                return_tensors="pt",
            )
            inputs = {k: v.to(device) for k, v in inputs.items()}
            logits = model(**inputs).logits
            probs = torch.softmax(logits, dim=-1)[:, 1].cpu().numpy()

    labels = (probs >= threshold).astype(int)

    t1 = time.perf_counter()
    total_ms = (t1 - t0) * 1000
    per_ms = total_ms / len(texts) if texts else 0

    return labels, probs, total_ms, per_ms


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="header-tag">CẤU HÌNH</div>', unsafe_allow_html=True)
    st.markdown("### Mô hình")

    selected_model_name = st.selectbox(
        "Chọn mô hình để chạy",
        options=list(MODEL_OPTIONS.keys()),
        index=0,
        label_visibility="collapsed",
    )
    model_meta = MODEL_OPTIONS[selected_model_name]

    st.markdown(
        f'<div class="model-info-box"><b>{selected_model_name}</b><br>{model_meta["desc"]}</div>',
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown("### Đường dẫn mô hình")
    model_path = st.text_input(
        "Local path",
        value=model_meta["path"],
        key=f"model_path_{model_meta['key']}",
        help="Teacher dùng thư mục Hugging Face; student dùng file checkpoint .pt hoặc thư mục chứa file đó.",
    )

    st.markdown("---")
    st.markdown("### Ngưỡng phân loại (Threshold)")
    threshold = st.slider(
        "Ngưỡng P(smishing) ≥",
        min_value=0.1,
        max_value=0.9,
        value=0.5,
        step=0.05,
        format="%.2f",
        label_visibility="collapsed",
    )
    st.markdown(
        f'<div class="threshold-note">Tin nhắn có P(smishing) ≥ <b style="color:#f87171">{threshold:.2f}</b> sẽ bị gán nhãn <b style="color:#f87171">SMISHING</b></div>',
        unsafe_allow_html=True,
    )

    st.markdown("---")
    load_btn = st.button("Load mô hình", use_container_width=True, type="primary")
    model_status = st.empty()

# ─────────────────────────────────────────────
# MODEL LOADING STATE
# ─────────────────────────────────────────────
for state_key, default_value in {
    "loaded_model_path": None,
    "loaded_model_name": None,
    "loaded_model_type": None,
    "tokenizer": None,
    "model": None,
    "device": None,
    "vocab": None,
    "model_config": None,
    "parameter_count": None,
}.items():
    if state_key not in st.session_state:
        st.session_state[state_key] = default_value

if load_btn:
    if not os.path.exists(model_path):
        model_status.error(f"Không tìm thấy đường dẫn: `{model_path}`")
    else:
        with st.spinner(f"Đang load **{selected_model_name}** từ `{model_path}` …"):
            try:
                tok, mdl, dev, vocab, config, parameter_count = load_model(
                    model_path,
                    model_meta["type"],
                )
                st.session_state.tokenizer = tok
                st.session_state.model = mdl
                st.session_state.device = dev
                st.session_state.vocab = vocab
                st.session_state.model_config = config
                st.session_state.parameter_count = parameter_count
                st.session_state.loaded_model_path = model_path
                st.session_state.loaded_model_name = selected_model_name
                st.session_state.loaded_model_type = model_meta["type"]
                model_status.success(f"Load thành công — {parameter_count:,} tham số")
            except Exception as e:
                model_status.error(f"Lỗi: {e}")

model_ready = st.session_state.model is not None

# ─────────────────────────────────────────────
# MAIN AREA
# ─────────────────────────────────────────────
st.markdown("""
<div class="header-banner">
    <div class="header-tag">VISMISH DEMO</div>
    <h1>Phát hiện SMS Lừa đảo Tiếng Việt</h1>
    <p>Mô hình PhoBERT fine-tuned trên dataset ViSmishDS — UIT NLP Lab</p>
</div>
""", unsafe_allow_html=True)

# Status bar
if model_ready:
    loaded_name = st.session_state.get("loaded_model_name", "")
    dev_name = "GPU 🟢" if st.session_state.device.type == "cuda" else "CPU 🟡"
    parameter_count = st.session_state.get("parameter_count", 0)
    st.info(f"**Mô hình đang dùng:** {loaded_name} &nbsp;|&nbsp; **Tham số:** {parameter_count:,} &nbsp;|&nbsp; **Thiết bị:** {dev_name} &nbsp;|&nbsp; **Threshold:** {threshold:.2f}", icon="🤖")
else:
    st.warning("⬅️ Chưa load mô hình. Cấu hình đường dẫn và nhấn **Load mô hình** ở sidebar.", icon="⚠️")

st.markdown("")

# ─────────────────────────────────────────────
# INPUT TABS
# ─────────────────────────────────────────────
tab_text, tab_file = st.tabs(["Nhập trực tiếp", "Tải lên CSV / Excel"])

texts_to_predict: list[str] = []

with tab_text:
    st.markdown('<div class="section-label">Nội dung tin nhắn</div>', unsafe_allow_html=True)
    user_text = st.text_area(
        "Nhập nội dung SMS",
        height=140,
        placeholder="Dán nội dung tin nhắn vào đây …\nMỗi dòng là một tin nhắn riêng.",
        label_visibility="collapsed",
    )
    run_text = st.button("Phân tích", key="run_text", disabled=not model_ready, type="primary")

    if run_text and user_text.strip():
        texts_to_predict = [line.strip() for line in user_text.strip().splitlines() if line.strip()]

with tab_file:
    st.markdown('<div class="section-label">Upload file</div>', unsafe_allow_html=True)
    uploaded = st.file_uploader(
        "Chọn file CSV hoặc Excel (cột 'content')",
        type=["csv", "xlsx", "xls"],
        label_visibility="collapsed",
    )
    run_file = st.button("Phân tích file", key="run_file", disabled=not model_ready, type="primary")

    if uploaded is not None:
        try:
            if uploaded.name.endswith(".csv"):
                df_upload = pd.read_csv(uploaded)
            else:
                df_upload = pd.read_excel(uploaded)

            if "content" not in df_upload.columns:
                st.error(f"Không tìm thấy cột **'content'** trong file. Các cột hiện có: {list(df_upload.columns)}")
            else:
                st.success(f"Đã đọc **{len(df_upload)}** hàng từ `{uploaded.name}`")
                st.dataframe(
                    df_upload[["content"]].head(5),
                    use_container_width=True,
                    hide_index=True,
                )
                if run_file:
                    texts_to_predict = df_upload["content"].dropna().astype(str).tolist()
        except Exception as e:
            st.error(f"Lỗi đọc file: {e}")

# ─────────────────────────────────────────────
# RUN INFERENCE
# ─────────────────────────────────────────────
if texts_to_predict and model_ready:
    st.markdown("---")
    with st.spinner("Đang chạy mô hình …"):
        labels, probs, total_ms, per_ms = predict_batch(
            texts_to_predict,
            st.session_state.tokenizer,
            st.session_state.model,
            st.session_state.device,
            threshold,
            st.session_state.loaded_model_type,
            st.session_state.vocab,
            st.session_state.model_config,
        )

    n_smishing = int(labels.sum())
    n_ham = len(labels) - n_smishing

    # ── Timing summary ──
    st.markdown('<div class="section-label">Thời gian suy luận</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
        <div class="timing-box">
            <div class="time-val">{total_ms:.1f} ms</div>
            <div class="time-label">Tổng thời gian</div>
            <div class="time-sub">{len(texts_to_predict)} tin nhắn</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="timing-box">
            <div class="time-val">{per_ms:.2f} ms</div>
            <div class="time-label">Trung bình / tin</div>
            <div class="time-sub">per-sample latency</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        tps = 1000 / per_ms if per_ms > 0 else 0
        st.markdown(f"""
        <div class="timing-box">
            <div class="time-val">{tps:.1f}</div>
            <div class="time-label">Tin nhắn / giây</div>
            <div class="time-sub">throughput</div>
        </div>""", unsafe_allow_html=True)

    # ── Stats summary ──
    st.markdown('<div class="section-label">Tóm tắt kết quả</div>', unsafe_allow_html=True)
    sc1, sc2 = st.columns(2)
    with sc1:
        st.markdown(f"""
        <div class="result-card">
            <div class="stat-row"><span>Tổng tin nhắn</span><span class="stat-val">{len(labels)}</span></div>
            <div class="stat-row"><span>🔴 SMISHING</span><span class="stat-val prob-high">{n_smishing} ({n_smishing/len(labels)*100:.1f}%)</span></div>
            <div class="stat-row"><span>🟢 HỢP LỆ (HAM)</span><span class="stat-val prob-low">{n_ham} ({n_ham/len(labels)*100:.1f}%)</span></div>
        </div>""", unsafe_allow_html=True)
    with sc2:
        avg_prob = float(probs.mean())
        max_prob = float(probs.max())
        min_prob = float(probs.min())
        st.markdown(f"""
        <div class="result-card">
            <div class="stat-row"><span>P(smishing) trung bình</span><span class="stat-val">{avg_prob:.4f}</span></div>
            <div class="stat-row"><span>P(smishing) cao nhất</span><span class="stat-val prob-high">{max_prob:.4f}</span></div>
            <div class="stat-row"><span>P(smishing) thấp nhất</span><span class="stat-val prob-low">{min_prob:.4f}</span></div>
        </div>""", unsafe_allow_html=True)

    # ── Per-message results ──
    st.markdown('<div class="section-label">Chi tiết từng tin nhắn</div>', unsafe_allow_html=True)

    for i, (text, label, prob) in enumerate(zip(texts_to_predict, labels, probs)):
        is_smishing = label == 1
        card_cls = "smishing" if is_smishing else "ham"
        badge = '<span class="badge-smishing">⚠️ SMISHING</span>' if is_smishing else '<span class="badge-ham">✅ HỢP LỆ</span>'
        prob_cls = "prob-high" if is_smishing else "prob-low"
        preview = text if len(text) <= 220 else text[:220] + "…"

        st.markdown(f"""
        <div class="result-card {card_cls}">
            <div style="display:flex; align-items:center; gap:10px;">
                {badge}
                <span style="font-size:0.72rem;color:#334155;font-family:'JetBrains Mono',monospace;">#{i+1}</span>
            </div>
            <div class="sms-content">{preview}</div>
            <div class="meta-row">
                <span>P(smishing): <span class="{prob_cls}">{prob:.4f}</span></span>
                <span style="color:#1e293b">|</span>
                <span>Threshold: {threshold:.2f}</span>
            </div>
        </div>""", unsafe_allow_html=True)

    # ── Export ──
    st.markdown("---")
    st.markdown('<div class="section-label">Xuất kết quả</div>', unsafe_allow_html=True)
    df_out = pd.DataFrame({
        "content": texts_to_predict,
        "label": ["SMISHING" if l == 1 else "HAM" for l in labels],
        "prob_smishing": [round(float(p), 6) for p in probs],
        "threshold": threshold,
        "model": st.session_state.get("loaded_model_name", ""),
    })
    csv_bytes = df_out.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")
    st.download_button(
        label="Tải kết quả CSV",
        data=csv_bytes,
        file_name=f"vismish_results_{model_meta['key']}.csv",
        mime="text/csv",
        use_container_width=True,
    )

elif texts_to_predict and not model_ready:
    st.error("Vui lòng load mô hình trước khi chạy phân tích.")

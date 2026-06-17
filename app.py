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
    },
    "   Student 1 (Distilled)": {
        "key": "student_1",
        "desc": "cnn",
        "type": "student",
    },
    "   Student 2 (Distilled)": {
        "key": "student_2",
        "desc": "bilstm",
        "type": "student",
    },
}

# ─────────────────────────────────────────────
# LOAD MODEL (cached)
# ─────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_model(model_path: str):
    """Load tokenizer + model từ local path."""
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    model.eval()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    return tokenizer, model, device


def predict_batch(texts: list[str], tokenizer, model, device, threshold: float):
    """
    Chạy inference trên danh sách texts.
    Trả về (labels, probabilities, total_time_ms, per_sample_ms)
    """
    t0 = time.perf_counter()

    inputs = tokenizer(
        texts,
        padding=True,
        truncation=True,
        max_length=256,
        return_tensors="pt",
    )
    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        logits = model(**inputs).logits

    probs = torch.softmax(logits, dim=-1)[:, 1].cpu().numpy()  # P(smishing)
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
        value=f"./models/{model_meta['key']}",
        help="Thư mục chứa config.json, pytorch_model.bin, tokenizer_config.json …",
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
if "loaded_model_path" not in st.session_state:
    st.session_state.loaded_model_path = None
    st.session_state.tokenizer = None
    st.session_state.model = None
    st.session_state.device = None

if load_btn:
    if not os.path.isdir(model_path):
        model_status.error(f"Không tìm thấy thư mục: `{model_path}`")
    else:
        with st.spinner(f"Đang load **{selected_model_name}** từ `{model_path}` …"):
            try:
                tok, mdl, dev = load_model(model_path)
                st.session_state.tokenizer = tok
                st.session_state.model = mdl
                st.session_state.device = dev
                st.session_state.loaded_model_path = model_path
                st.session_state.loaded_model_name = selected_model_name
                model_status.success("Load thành công!")
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
    st.info(f"**Mô hình đang dùng:** {loaded_name} &nbsp;|&nbsp; **Thiết bị:** {dev_name} &nbsp;|&nbsp; **Threshold:** {threshold:.2f}", icon="🤖")
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

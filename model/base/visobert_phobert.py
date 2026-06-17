import pandas as pd
import torch
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    f1_score, precision_score, recall_score,
    confusion_matrix, average_precision_score
)
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from pyvi import ViTokenizer

os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

# ---------------------------------------------------------
# 1. CHUẨN BỊ DATA
# ---------------------------------------------------------
df = pd.read_csv("vismishds_phase1_final.csv")

# Đảm bảo dữ liệu ở dạng chuỗi và xử lý các giá trị rỗng (nếu có)
df['content'] = df['content'].astype(str).fillna("")

# ---------------------------------------------------------
# Split: train = 100% synthetic, val = 100% real
# ---------------------------------------------------------
train_df = df[df['data_origin'] == 'synthetic'].copy()
val_df   = df[df['data_origin'] == 'real'].copy()

print(f"[INFO] Kích thước tập train (synthetic): {len(train_df)}  ({len(train_df)/len(df)*100:.1f}%)")
print(f"[INFO] Kích thước tập val   (real)      : {len(val_df)}  ({len(val_df)/len(df)*100:.1f}%)")
print(f"[INFO] Phân phối label trong train:\n{train_df['label'].value_counts()}")
print(f"[INFO] Phân phối label trong val  :\n{val_df['label'].value_counts()}")


# ---------------------------------------------------------
# 2. ĐÁNH GIÁ METRICS
# ---------------------------------------------------------
def compute_metrics(pred):
    labels     = pred.label_ids
    preds      = pred.predictions.argmax(-1)

    # Stable softmax để lấy xác suất class 1 cho AUPRC
    logits     = pred.predictions
    exp_logits = np.exp(logits - logits.max(axis=-1, keepdims=True))
    probs_pos  = (exp_logits / exp_logits.sum(axis=-1, keepdims=True))[:, 1]

    return {
        "macro_f1"         : f1_score(labels, preds, average="macro",  zero_division=0),
        "f1_label1"        : f1_score(labels, preds, pos_label=1, average="binary", zero_division=0),
        "recall_label1"    : recall_score(labels,    preds, pos_label=1, average="binary", zero_division=0),
        "precision_label1" : precision_score(labels, preds, pos_label=1, average="binary", zero_division=0),
        "auprc"            : average_precision_score(labels, probs_pos),
    }

# ---------------------------------------------------------
# 3. VẼ CONFUSION MATRIX
# ---------------------------------------------------------
def plot_confusion_matrix(labels, preds, model_name, save_path):
    cm      = confusion_matrix(labels, preds)
    cm_norm = confusion_matrix(labels, preds, normalize="true")

    # Ô hiển thị: số lượng + phần trăm
    annot = np.array([
        [f"{cm[i, j]}\n({cm_norm[i, j]*100:.1f}%)" for j in range(cm.shape[1])]
        for i in range(cm.shape[0])
    ])

    fig, ax = plt.subplots(figsize=(6, 5))
    sns.heatmap(
        cm_norm, annot=annot, fmt="", cmap="Blues", ax=ax,
        xticklabels=["Ham (0)", "Spam (1)"],
        yticklabels=["Ham (0)", "Spam (1)"],
        vmin=0, vmax=1,
    )
    ax.set_title(f"Confusion Matrix — {model_name}", fontsize=13, fontweight="bold")
    ax.set_ylabel("Actual",    fontsize=11)
    ax.set_xlabel("Predicted", fontsize=11)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.close()
    print(f"[INFO] Confusion matrix đã lưu tại: {save_path}")


# =========================================================
def run_phobert_baseline(train_data, val_data):
    print(f"\n{'='*50}\n[RUNNING] PHOBERT BASELINE\n{'='*50}")
    
    model_name = "vinai/phobert-base"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)
    
    # Hàm gán token đặc thù cho PhoBERT: NỐI TỪ BẰNG VITOKENIZER TRƯỚC
    def phobert_tokenize_fn(examples):
        segmented_texts = [ViTokenizer.tokenize(text) for text in examples['content']]
        return tokenizer(segmented_texts, padding="max_length", truncation=True, max_length=128)
    
    # Chuyển đổi Dataset
    train_ds = Dataset.from_pandas(train_data)
    val_ds = Dataset.from_pandas(val_data)
    
    train_ds = train_ds.map(phobert_tokenize_fn, batched=True)
    val_ds = val_ds.map(phobert_tokenize_fn, batched=True)
    
    train_ds.set_format(type='torch', columns=['input_ids', 'attention_mask', 'label'])
    val_ds.set_format(type='torch', columns=['input_ids', 'attention_mask', 'label'])
    
    training_args = TrainingArguments(
        output_dir='./results_phobert',
        num_train_epochs=3,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=32,
        weight_decay=0.01,
        eval_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        logging_dir='./logs_phobert',
    )
    
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_ds,
        eval_dataset=val_ds,
        compute_metrics=compute_metrics,
    )
    
    trainer.train()

    # Predict một lần: lấy preds cho confusion matrix + metrics
    preds_output = trainer.predict(val_ds)
    preds  = preds_output.predictions.argmax(-1)
    labels = preds_output.label_ids
    plot_confusion_matrix(labels, preds, "PhoBERT", "confusion_matrix_phobert.png")

    return preds_output.metrics

# =========================================================
# 4. NHÁNH 2: VISOBERT
# =========================================================
def run_visobert_baseline(train_data, val_data):
    print(f"\n{'='*50}\n[RUNNING] VISOBERT BASELINE\n{'='*50}")
    
    model_name = "uitnlp/visobert"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)
    
    # Hàm gán token cho ViSoBERT: Dùng luôn chuỗi text gốc
    def visobert_tokenize_fn(examples):
        return tokenizer(examples['content'], padding="max_length", truncation=True, max_length=128)
        
    # Chuyển đổi Dataset
    train_ds = Dataset.from_pandas(train_data)
    val_ds = Dataset.from_pandas(val_data)
    
    train_ds = train_ds.map(visobert_tokenize_fn, batched=True)
    val_ds = val_ds.map(visobert_tokenize_fn, batched=True)
    
    train_ds.set_format(type='torch', columns=['input_ids', 'attention_mask', 'label'])
    val_ds.set_format(type='torch', columns=['input_ids', 'attention_mask', 'label'])
    
    training_args = TrainingArguments(
        output_dir='./results_visobert',
        num_train_epochs=3,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=32,
        weight_decay=0.01,
        eval_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        logging_dir='./logs_visobert',
    )
    
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_ds,
        eval_dataset=val_ds,
        compute_metrics=compute_metrics,
    )
    
    trainer.train()

    # Predict một lần: lấy preds cho confusion matrix + metrics
    preds_output = trainer.predict(val_ds)
    preds  = preds_output.predictions.argmax(-1)
    labels = preds_output.label_ids
    plot_confusion_matrix(labels, preds, "ViSoBERT", "confusion_matrix_visobert.png")

    return preds_output.metrics

# ---------------------------------------------------------
# 5. MAIN
# ---------------------------------------------------------
if __name__ == "__main__":
    phobert_results  = run_phobert_baseline(train_df, val_df)
    visobert_results = run_visobert_baseline(train_df, val_df)

    # Mapping key → tên hiển thị
    METRIC_LABELS = {
        "macro_f1"         : "Macro-F1",
        "f1_label1"        : "F1 (Label 1)",
        "recall_label1"    : "Recall (Label 1)",
        "precision_label1" : "Precision (Label 1)",
        "auprc"            : "AUPRC",
    }

    def print_results(model_label, results):
        print(f"\n[THỐNG KÊ {model_label}]")
        for key, display_name in METRIC_LABELS.items():
            val = results.get(f"test_{key}", results.get(f"eval_{key}", None))
            if val is not None:
                print(f"  - {display_name:<22}: {val:.4f}")

    print(f"\n{'='*50}\nTHỐNG KÊ KẾT QUẢ BASELINE\n{'='*50}")
    print_results("PHOBERT",  phobert_results)
    print_results("VISOBERT", visobert_results)

    # Bảng so sánh ngang
    print(f"\n{'='*50}\nBẢNG SO SÁNH\n{'='*50}")
    header = f"{'Metric':<22}  {'PhoBERT':>10}  {'ViSoBERT':>10}"
    print(header)
    print("-" * len(header))
    for key, display_name in METRIC_LABELS.items():
        pb = phobert_results.get(f"test_{key}", phobert_results.get(f"eval_{key}", float("nan")))
        vs = visobert_results.get(f"test_{key}", visobert_results.get(f"eval_{key}", float("nan")))
        print(f"  {display_name:<22}  {pb:>10.4f}  {vs:>10.4f}")

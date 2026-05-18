import re
import pandas as pd
import torch
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, confusion_matrix
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from pyvi import ViTokenizer

from layer1_masking import AggressiveMasker   # <-- import lớp masking

os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

# ---------------------------------------------------------
# 1. CHUẨN BỊ DATA
# ---------------------------------------------------------
df = pd.read_csv("vismishds_phase1_final.csv")

# Đảm bảo dữ liệu ở dạng chuỗi và xử lý các giá trị rỗng (nếu có)
df['content'] = df['content'].astype(str).fillna("")

# ---------------------------------------------------------
# 1.5. MASKING (Layer 1)
# ---------------------------------------------------------
print("[INFO] Đang áp dụng AggressiveMasker lên toàn bộ content...")
masker = AggressiveMasker()
masked_texts, _ = masker._mask_batch(df['content'].tolist())
df['content'] = masked_texts
print(f"[INFO] Masking hoàn tất. Ví dụ:\n  Gốc   : {df['content'].iloc[0]}\n  Masked: {masked_texts[0]}")

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
    labels = pred.label_ids
    preds = pred.predictions.argmax(-1)
    return {
        "accuracy": accuracy_score(labels, preds),
        "f1": f1_score(labels, preds, average='weighted'),
        "precision": precision_score(labels, preds, average='weighted', zero_division=0),
        "recall": recall_score(labels, preds, average='weighted', zero_division=0)
    }

# ---------------------------------------------------------
# 3. VẼ CONFUSION MATRIX
# ---------------------------------------------------------
def plot_confusion_matrix(labels, preds, model_name, save_path):
    cm = confusion_matrix(labels, preds)
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.heatmap(
        cm, annot=True, fmt='d', cmap='Blues', ax=ax,
        xticklabels=['Predicted 0', 'Predicted 1'],
        yticklabels=['Actual 0', 'Actual 1']
    )
    ax.set_title(f'Confusion Matrix — {model_name}', fontsize=13, fontweight='bold')
    ax.set_ylabel('Actual', fontsize=11)
    ax.set_xlabel('Predicted', fontsize=11)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.close()
    print(f"[INFO] Confusion matrix đã lưu tại: {save_path}")


# =========================================================
# 4. NHÁNH 1: PHOBERT
# =========================================================
def run_phobert_baseline(train_data, val_data):
    print(f"\n{'='*50}\n[RUNNING] PHOBERT BASELINE\n{'='*50}")

    model_name = "vinai/phobert-base"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)

    # PhoBERT yêu cầu word-segment bằng ViTokenizer trước khi tokenize.
    # Tách special tokens ra trước để ViTokenizer không làm hỏng chúng,
    # chỉ segment phần text thuần, rồi ghép lại.
    _SPECIAL_TOK_PATTERN = r'(<URL>|<PHONE>|<EMAIL>|<BANK_ACC>|<MONEY>|<CODE>|<TIME>|<APP_LINK>)'
    _SPECIAL_TOK_SET = {"<URL>", "<PHONE>", "<EMAIL>",
                        "<BANK_ACC>", "<MONEY>", "<CODE>",
                        "<TIME>", "<APP_LINK>"}

    def phobert_tokenize_fn(examples):
        segmented_texts = []
        for text in examples['content']:
            parts = re.split(_SPECIAL_TOK_PATTERN, text)
            processed = [
                part if part in _SPECIAL_TOK_SET else ViTokenizer.tokenize(part)
                for part in parts
            ]
            segmented_texts.append("".join(processed))
        return tokenizer(segmented_texts, padding="max_length", truncation=True, max_length=128)

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

    preds_output = trainer.predict(val_ds)
    preds  = preds_output.predictions.argmax(-1)
    labels = preds_output.label_ids
    plot_confusion_matrix(labels, preds, "PhoBERT", "confusion_matrix_phobert.png")

    return trainer.evaluate()


# =========================================================
# 5. NHÁNH 2: VISOBERT
# =========================================================
def run_visobert_baseline(train_data, val_data):
    print(f"\n{'='*50}\n[RUNNING] VISOBERT BASELINE\n{'='*50}")

    model_name = "uitnlp/visobert"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)

    # ViSoBERT dùng thẳng text gốc (đã masked)
    def visobert_tokenize_fn(examples):
        return tokenizer(examples['content'], padding="max_length", truncation=True, max_length=128)

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

    preds_output = trainer.predict(val_ds)
    preds  = preds_output.predictions.argmax(-1)
    labels = preds_output.label_ids
    plot_confusion_matrix(labels, preds, "ViSoBERT", "confusion_matrix_visobert.png")

    return trainer.evaluate()


# ---------------------------------------------------------
# 6. MAIN
# ---------------------------------------------------------
if __name__ == "__main__":
    phobert_results  = run_phobert_baseline(train_df, val_df)
    visobert_results = run_visobert_baseline(train_df, val_df)

    print(f"\n{'='*50}\nTHỐNG KÊ KẾT QUẢ BASELINE\n{'='*50}")

    print("\n[THỐNG KÊ PHOBERT]")
    for key, value in phobert_results.items():
        if key.startswith("eval_"):
            print(f"- {key.replace('eval_', '').capitalize():<15}: {value:.4f}")

    print("\n[THỐNG KÊ VISOBERT]")
    for key, value in visobert_results.items():
        if key.startswith("eval_"):
            print(f"- {key.replace('eval_', '').capitalize():<15}: {value:.4f}")

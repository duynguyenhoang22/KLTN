import pandas as pd
import torch
import os
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from pyvi import ViTokenizer

os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

# ---------------------------------------------------------
# 1. CHUẨN BỊ DATA
# ---------------------------------------------------------
df = pd.read_csv("model/smishing_mixed_dataset.csv")

# Đảm bảo dữ liệu ở dạng chuỗi và xử lý các giá trị rỗng (nếu có)
df['content'] = df['content'].astype(str).fillna("")

# Chia tập dữ liệu Train/Val dùng chung cấu trúc gốc
train_df, val_df = train_test_split(df, test_size=0.2, random_state=42)

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

# =========================================================
# 3. NHÁNH 1: PHOBERT
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
    return trainer.evaluate()

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
    return trainer.evaluate()

# ---------------------------------------------------------
# 5. MAIN
# ---------------------------------------------------------
if __name__ == "__main__":
    phobert_results = run_phobert_baseline(train_df, val_df)
    visobert_results = run_visobert_baseline(train_df, val_df)
    
    print(f"\n{'='*50}\nTHỐNG KÊ KẾT QUẢ BASELINE\n{'='*50}")
    
    print("\n[THỐNG KÊ PHOBERT]")
    for key, value in phobert_results.items():
        if key.startswith("eval_"):
            metric_name = key.replace("eval_", "").capitalize()
            print(f"- {metric_name:<15}: {value:.4f}")
            
    print("\n[THỐNG KÊ VISOBERT]")
    for key, value in visobert_results.items():
        if key.startswith("eval_"):
            metric_name = key.replace("eval_", "").capitalize()
            print(f"- {metric_name:<15}: {value:.4f}")
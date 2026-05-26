# %% [markdown]
# # Setup B — TRTR với xử lý mất cân bằng (PhoBERT)
#
# **Phương pháp:** Train on Real, Test on Real (TRTR) với xử lý mất cân bằng  
# **Model:** `vinai/phobert-base` + `ViTokenizer`  
# **Seeds:** `[42, 123, 2025]`  
# **Split:** Stratified 70 / 15 / 15 (`split_seed=0`, cố định như Setup A)  
# **Báo cáo:** mean ± std trên tập test thật
#
# ---
# **Biến thể trong notebook này:**
# - **B1:** Class weight + ngưỡng mặc định theo `argmax`
# - **B2:** Class weight + threshold tuning trên Real Validation
#
# **Chỉ số chính:**
# - Macro-F1
# - F1 Label 1
# - Recall Label 1
# - Precision Label 1
# - AUPRC
# - Confusion Matrix
#
# **Chỉ số phụ:** Accuracy (tham khảo), AUROC

# %%
# Cell 1 — Cài đặt dependencies
!pip uninstall -y peft torchvision torchaudio bitsandbytes
!pip install -q transformers==4.46.3 accelerate==1.1.1 datasets pyvi scikit-learn

# %%
from transformers import TrainingArguments
print("TrainingArguments OK")
from transformers import Trainer
print("Trainer OK")

# %%
# Cell 2 — Cấu hình
# Giữ nguyên các thiết lập cốt lõi từ Setup A để so sánh công bằng.

CFG = dict(
    # Model
    model_name           = "vinai/phobert-base",
    max_length           = 128,

    # Training
    seeds                = [42, 123, 2025],
    num_epochs           = 10,
    train_batch          = 16,
    eval_batch           = 32,
    learning_rate        = 2e-5,
    weight_decay         = 0.01,
    warmup_ratio         = 0.1,
    early_stop_patience  = 3,

    # Data split — KHÔNG thay đổi để tái tạo đúng split của Setup A
    split_seed           = 0,
    train_ratio          = 0.70,
    val_ratio            = 0.15,

    # Threshold tuning — chỉ tuning trên Real Validation
    threshold_min        = 0.05,
    threshold_max        = 0.95,
    threshold_step       = 0.01,

    # Đường dẫn Google Drive
    drive_root           = "/content/drive/MyDrive/KLTN",
    data_file            = "vismishds_real.csv",
    setup_a_test_file    = "/content/drive/MyDrive/KLTN/setup_a_results/setup_a_real_test.csv",
    output_dir           = "/content/drive/MyDrive/KLTN/setup_b_results",
    work_dir             = "/content/tmp_checkpoints_setup_b",
)

import os
os.makedirs(CFG["output_dir"], exist_ok=True)
print("Đã load CFG.")
print(f"  model_name          : {CFG['model_name']}")
print(f"  seeds               : {CFG['seeds']}")
print(f"  split_seed          : {CFG['split_seed']}")
print(f"  max_length          : {CFG['max_length']}")
print(f"  num_epochs (max)    : {CFG['num_epochs']}")
print(f"  early_stop_patience : {CFG['early_stop_patience']}")
print(f"  learning_rate       : {CFG['learning_rate']}")
print(f"  output_dir          : {CFG['output_dir']}")

# %%
# Cell 3 — Mount Google Drive và load dữ liệu thật
# Trước khi chạy: upload vismishds_real.csv lên MyDrive/KLTN/

import os
import shutil
from google.colab import drive

mountpoint = "/content/drive"

drive.flush_and_unmount()
drive.mount(mountpoint, force_remount=True)

import pandas as pd

data_path = os.path.join(CFG["drive_root"], CFG["data_file"])
df = pd.read_csv(data_path)

required_columns = {"content", "label"}
missing_columns = required_columns - set(df.columns)
assert not missing_columns, f"Dataset thiếu cột bắt buộc: {missing_columns}"

df["content"] = df["content"].astype(str).fillna("")
labels_found = set(df["label"].dropna().unique().tolist())
assert labels_found <= {0, 1}, f"Label chỉ được gồm 0/1, nhưng tìm thấy: {labels_found}"
df["label"] = df["label"].astype(int)

print(f"Tổng số mẫu: {len(df)}")
print(f"Cột: {list(df.columns)}")
print("\nPhân phối label (toàn bộ):")
print(df["label"].value_counts().sort_index().to_string())
print(f"\nTỷ lệ Label 1: {df['label'].mean()*100:.1f}%")

# %%
# Cell 4 — Stratified split 70/15/15 và kiểm tra Real Test Set của Setup A
#
# Setup B không chạy lại Setup A. Cell này chỉ tái tạo split bằng đúng logic
# và tham số của Setup A. Nếu file setup_a_real_test.csv tồn tại, sẽ đối chiếu
# để đảm bảo Real Test Set không bị lệch.

from sklearn.model_selection import train_test_split
from pandas.testing import assert_frame_equal

df_trainval, df_test = train_test_split(
    df,
    test_size=0.15,
    stratify=df["label"],
    random_state=CFG["split_seed"],
)

val_size_relative = CFG["val_ratio"] / (CFG["train_ratio"] + CFG["val_ratio"])
df_train, df_val = train_test_split(
    df_trainval,
    test_size=val_size_relative,
    stratify=df_trainval["label"],
    random_state=CFG["split_seed"],
)

setup_a_test_path = CFG["setup_a_test_file"]
if os.path.exists(setup_a_test_path):
    setup_a_test = pd.read_csv(setup_a_test_path)
    setup_a_test["content"] = setup_a_test["content"].astype(str).fillna("")
    setup_a_test["label"] = setup_a_test["label"].astype(int)

    recreated = df_test.reset_index(drop=True)[["content", "label"]]
    locked = setup_a_test.reset_index(drop=True)[["content", "label"]]
    assert_frame_equal(recreated, locked, check_dtype=False)
    print(f"[OK] Real Test Set trùng khớp với Setup A: {setup_a_test_path}")
else:
    print("[WARNING] Không tìm thấy setup_a_real_test.csv.")
    print("          Setup B sẽ dùng Real Test Set tái tạo từ split_seed=0.")

def print_split_info(name, split_df):
    counts = split_df["label"].value_counts().sort_index()
    print(f"\n{name}: {len(split_df)} mẫu")
    print(f"  Label 0: {counts.get(0, 0)}  ({counts.get(0,0)/len(split_df)*100:.1f}%)")
    print(f"  Label 1: {counts.get(1, 0)}  ({counts.get(1,0)/len(split_df)*100:.1f}%)")

print_split_info("Real Train (70%)", df_train)
print_split_info("Real Val   (15%)", df_val)
print_split_info("Real Test  (15%)", df_test)

# %%
# Cell 5 — Tokenization (ViTokenizer + PhoBERT AutoTokenizer)

from pyvi import ViTokenizer
from transformers import AutoTokenizer
from datasets import Dataset

tokenizer = AutoTokenizer.from_pretrained(CFG["model_name"])

def tokenize_batch(examples):
    segmented = [ViTokenizer.tokenize(text) for text in examples["content"]]
    return tokenizer(
        segmented,
        padding="max_length",
        truncation=True,
        max_length=CFG["max_length"],
    )

def make_hf_dataset(split_df):
    ds = Dataset.from_pandas(split_df[["content", "label"]].reset_index(drop=True))
    ds = ds.map(tokenize_batch, batched=True, batch_size=256)
    ds = ds.rename_column("label", "labels")
    ds.set_format(type="torch", columns=["input_ids", "attention_mask", "labels"])
    return ds

print("Đã load tokenizer.")
print(f"Vocab size: {tokenizer.vocab_size}")

# %%
# Cell 6 — Metrics và threshold tuning helpers
#
# compute_metrics dùng cho Trainer/eval checkpoint: mặc định argmax.
# compute_metrics_from_probs dùng để đánh giá B1/B2 trên test với ngưỡng tùy chọn.

import numpy as np
from scipy.special import softmax
from sklearn.metrics import (
    f1_score,
    precision_score,
    recall_score,
    accuracy_score,
    average_precision_score,
    roc_auc_score,
    confusion_matrix,
)

PRIMARY_METRICS   = ["macro_f1", "f1_label1", "recall_label1",
                     "precision_label1", "auprc"]
SECONDARY_METRICS = ["accuracy", "auroc"]
ALL_METRICS       = PRIMARY_METRICS + SECONDARY_METRICS

def compute_metrics_from_probs(labels, probs, threshold=0.5):
    preds = (probs >= threshold).astype(int)
    return {
        "macro_f1":         f1_score(labels, preds, average="macro", zero_division=0),
        "f1_label1":        f1_score(labels, preds, pos_label=1, average="binary", zero_division=0),
        "recall_label1":    recall_score(labels, preds, pos_label=1, zero_division=0),
        "precision_label1": precision_score(labels, preds, pos_label=1, zero_division=0),
        "auprc":            average_precision_score(labels, probs),
        "accuracy":         accuracy_score(labels, preds),
        "auroc":            roc_auc_score(labels, probs),
    }

def compute_metrics(pred):
    labels = pred.label_ids
    logits = pred.predictions
    probs  = softmax(logits, axis=-1)[:, 1]
    preds  = logits.argmax(-1)

    return {
        "macro_f1":         f1_score(labels, preds, average="macro", zero_division=0),
        "f1_label1":        f1_score(labels, preds, pos_label=1, average="binary", zero_division=0),
        "recall_label1":    recall_score(labels, preds, pos_label=1, zero_division=0),
        "precision_label1": precision_score(labels, preds, pos_label=1, zero_division=0),
        "auprc":            average_precision_score(labels, probs),
        "accuracy":         accuracy_score(labels, preds),
        "auroc":            roc_auc_score(labels, probs),
    }

def tune_threshold_on_validation(labels, probs):
    thresholds = np.round(
        np.arange(
            CFG["threshold_min"],
            CFG["threshold_max"] + CFG["threshold_step"] / 2,
            CFG["threshold_step"],
        ),
        2,
    )

    best = None
    for threshold in thresholds:
        metrics = compute_metrics_from_probs(labels, probs, threshold=threshold)
        candidate = {
            "threshold": float(threshold),
            "f1_label1": metrics["f1_label1"],
            "macro_f1": metrics["macro_f1"],
            "recall_label1": metrics["recall_label1"],
            "precision_label1": metrics["precision_label1"],
        }

        # Ưu tiên f1_label1, sau đó macro_f1. Nếu vẫn hòa, chọn threshold gần 0.5 hơn.
        if best is None:
            best = candidate
            continue

        current_key = (
            candidate["f1_label1"],
            candidate["macro_f1"],
            -abs(candidate["threshold"] - 0.5),
        )
        best_key = (
            best["f1_label1"],
            best["macro_f1"],
            -abs(best["threshold"] - 0.5),
        )
        if current_key > best_key:
            best = candidate

    return best

print("Đã đăng ký metrics và threshold tuning helpers.")
print("Chỉ số chính: macro_f1, f1_label1, recall_label1, precision_label1, auprc")
print("Chỉ số phụ  : accuracy, auroc")

# %%
# Cell 7 — set_seed_everything

import random
import torch
from transformers import set_seed as hf_set_seed

def set_seed_everything(seed: int):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    hf_set_seed(seed)
    print(f"[seed] Đã đặt toàn bộ seed = {seed}")

print("Đã định nghĩa set_seed_everything.")

# %%
# Cell 8 — Import Trainer và định nghĩa WeightedTrainer
# Kernel crash ở đây = peft/torchvision vẫn lỗi, hoặc Colab GPU bị ngắt kết nối.
# Fix: Runtime -> Factory reset -> Cell 1 -> Restart -> Cell 2-8.

import subprocess, sys
subprocess.run([sys.executable, "-m", "pip", "uninstall", "-y", "peft"], capture_output=True)

from transformers import (
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments,
    EarlyStoppingCallback,
)

class WeightedTrainer(Trainer):
    def __init__(self, *args, class_weights=None, **kwargs):
        super().__init__(*args, **kwargs)
        if class_weights is None:
            raise ValueError("class_weights is required for WeightedTrainer")
        self.class_weights = class_weights

    def compute_loss(self, model, inputs, return_outputs=False, **kwargs):
        labels = inputs.pop("labels")
        outputs = model(**inputs)
        logits = outputs.logits
        weights = self.class_weights.to(logits.device)
        loss_fct = torch.nn.CrossEntropyLoss(weight=weights)
        loss = loss_fct(logits.view(-1, model.config.num_labels), labels.view(-1))
        return (loss, outputs) if return_outputs else loss

print("transformers OK — đã định nghĩa WeightedTrainer.")
print(f"  transformers : {__import__('transformers').__version__}")
print(f"  CUDA         : {torch.cuda.is_available()}")

# %%
# Cell 9 — Class weights và train_one_seed
#
# Mỗi seed chỉ train 1 lần với class weight. Sau đó dùng cùng model để báo cáo:
# - B1: default argmax
# - B2: threshold tune trên Real Validation

import gc
import shutil

def _free_gpu():
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.synchronize()

def compute_class_weights(train_df):
    counts = train_df["label"].value_counts().sort_index()
    assert set(counts.index.tolist()) == {0, 1}, "Real Train phải có đủ Label 0 và Label 1"
    total = len(train_df)
    num_classes = 2
    weights = [total / (num_classes * counts[label]) for label in [0, 1]]
    return torch.tensor(weights, dtype=torch.float)

class_weights = compute_class_weights(df_train)
print(f"Class weights [Label 0, Label 1]: {class_weights.tolist()}")

def _clean_trainer_metrics(metrics):
    return {
        k.replace("test_", ""): v
        for k, v in metrics.items()
        if k not in (
            "test_loss",
            "test_runtime",
            "test_samples_per_second",
            "test_steps_per_second",
        )
    }

def train_one_seed(seed: int, train_ds, val_ds, test_ds):
    print(f"\n{'='*70}")
    print(f"  SEED {seed} — Setup B: class weight + threshold trên validation")
    print(f"{'='*70}")

    set_seed_everything(seed)
    _free_gpu()

    model = AutoModelForSequenceClassification.from_pretrained(
        CFG["model_name"], num_labels=2
    )

    run_dir = os.path.join(CFG["work_dir"], f"seed_{seed}")
    if os.path.exists(run_dir):
        shutil.rmtree(run_dir)
    os.makedirs(run_dir, exist_ok=True)

    training_args = TrainingArguments(
        output_dir                  = run_dir,
        num_train_epochs            = CFG["num_epochs"],
        per_device_train_batch_size = CFG["train_batch"],
        per_device_eval_batch_size  = CFG["eval_batch"],
        learning_rate               = CFG["learning_rate"],
        weight_decay                = CFG["weight_decay"],
        warmup_ratio                = CFG["warmup_ratio"],
        eval_strategy               = "epoch",
        save_strategy               = "epoch",
        load_best_model_at_end      = True,
        metric_for_best_model       = "f1_label1",
        greater_is_better           = True,
        logging_dir                 = os.path.join(run_dir, "logs"),
        logging_steps               = 20,
        save_total_limit            = 1,
        seed                        = seed,
        report_to                   = "none",
        fp16                        = torch.cuda.is_available(),
        dataloader_num_workers      = 0,
        dataloader_pin_memory       = False,
    )

    trainer = WeightedTrainer(
        model           = model,
        args            = training_args,
        train_dataset   = train_ds,
        eval_dataset    = val_ds,
        compute_metrics = compute_metrics,
        callbacks       = [EarlyStoppingCallback(
                              early_stopping_patience=CFG["early_stop_patience"]
                           )],
        class_weights   = class_weights,
    )

    trainer.train()

    val_output = trainer.predict(val_ds)
    val_probs = softmax(val_output.predictions, axis=-1)[:, 1]
    val_labels = val_output.label_ids
    threshold_info = tune_threshold_on_validation(val_labels, val_probs)
    tuned_threshold = threshold_info["threshold"]

    print("\n[Threshold tuning trên validation]")
    print(f"  best_threshold       : {tuned_threshold:.2f}")
    print(f"  val_f1_label1        : {threshold_info['f1_label1']:.4f}")
    print(f"  val_macro_f1         : {threshold_info['macro_f1']:.4f}")
    print(f"  val_recall_label1    : {threshold_info['recall_label1']:.4f}")
    print(f"  val_precision_label1 : {threshold_info['precision_label1']:.4f}")

    test_output = trainer.predict(test_ds)
    test_logits = test_output.predictions
    test_probs = softmax(test_logits, axis=-1)[:, 1]
    test_labels = test_output.label_ids

    default_metrics = _clean_trainer_metrics(test_output.metrics)
    default_preds = test_logits.argmax(-1)
    default_cm = confusion_matrix(test_labels, default_preds, labels=[0, 1])

    threshold_metrics = compute_metrics_from_probs(
        test_labels, test_probs, threshold=tuned_threshold
    )
    threshold_preds = (test_probs >= tuned_threshold).astype(int)
    threshold_cm = confusion_matrix(test_labels, threshold_preds, labels=[0, 1])

    b1 = {
        **default_metrics,
        "setup": "B1_class_weight_default",
        "seed": seed,
        "threshold": 0.5,
        "confusion_matrix": default_cm,
        "best_epoch": trainer.state.best_model_checkpoint,
    }
    b2 = {
        **threshold_metrics,
        "setup": "B2_class_weight_threshold",
        "seed": seed,
        "threshold": tuned_threshold,
        "val_threshold_f1_label1": threshold_info["f1_label1"],
        "val_threshold_macro_f1": threshold_info["macro_f1"],
        "confusion_matrix": threshold_cm,
        "best_epoch": trainer.state.best_model_checkpoint,
    }

    for result in [b1, b2]:
        print(f"\n[Seed {seed}] Kết quả test — {result['setup']}:")
        print(f"  threshold             : {result['threshold']:.2f}")
        for k in ALL_METRICS:
            print(f"  {k:<22}: {result[k]:.4f}")
        print(f"  confusion_matrix:\n{result['confusion_matrix']}")

    del trainer, model, val_output, test_output
    if os.path.exists(run_dir):
        shutil.rmtree(run_dir, ignore_errors=True)
    _free_gpu()

    return [b1, b2]

print("Đã định nghĩa train_one_seed.")

# %%
# Cell 10 — Tokenize một lần + vòng lặp huấn luyện nhiều seed

if torch.cuda.is_available():
    props = torch.cuda.get_device_properties(0)
    print(f"GPU: {props.name}  |  VRAM: {props.total_memory / 1e9:.1f} GB")
else:
    print("WARNING: Không có GPU — huấn luyện trên CPU sẽ rất chậm.")

print("Đang tokenize train / val / test (một lần)...")
train_ds = make_hf_dataset(df_train)
val_ds   = make_hf_dataset(df_val)
test_ds  = make_hf_dataset(df_test)
print(f"  train: {len(train_ds)}  val: {len(val_ds)}  test: {len(test_ds)}")

all_results = []

for seed in CFG["seeds"]:
    seed_results = train_one_seed(seed, train_ds, val_ds, test_ds)
    all_results.extend(seed_results)

expected_results = len(CFG["seeds"]) * 2
assert len(all_results) == expected_results, (
    f"Expected {expected_results} results, got {len(all_results)}"
)
print(f"\nHoàn thành {len(CFG['seeds'])}/{len(CFG['seeds'])} seed.")
print(f"Tổng số result rows: {len(all_results)}")

# %%
# Cell 11 — Tổng hợp kết quả: per-seed và mean ± std

print("\n" + "="*78)
print("  SETUP B — TRTR với xử lý mất cân bằng (PhoBERT)")
print("  B1: Class Weight default argmax | B2: Class Weight + Threshold Tuning")
print("  Kết quả trên Real Test Set")
print("="*78)

summary_rows = []
per_seed_rows = []

for result in all_results:
    row = {
        "setup": result["setup"],
        "seed": result["seed"],
        "threshold": round(result["threshold"], 4),
        "best_epoch": result["best_epoch"],
    }
    for k in ALL_METRICS:
        row[k] = round(result[k], 4)
    if "val_threshold_f1_label1" in result:
        row["val_threshold_f1_label1"] = round(result["val_threshold_f1_label1"], 4)
        row["val_threshold_macro_f1"] = round(result["val_threshold_macro_f1"], 4)
    per_seed_rows.append(row)

per_seed_df = pd.DataFrame(per_seed_rows)
per_seed_path = os.path.join(CFG["output_dir"], "setup_b_per_seed_results.csv")
per_seed_df.to_csv(per_seed_path, index=False)
print(f"\nKết quả từng seed đã lưu tại: {per_seed_path}")

for setup_name in ["B1_class_weight_default", "B2_class_weight_threshold"]:
    setup_results = [r for r in all_results if r["setup"] == setup_name]
    assert len(setup_results) == len(CFG["seeds"]), (
        f"{setup_name} thiếu kết quả seed: {len(setup_results)}"
    )

    print(f"\n--- {setup_name} — kết quả từng seed ---")
    header = f"{'Metric':<22}" + "".join(f"  Seed {r['seed']}" for r in setup_results)
    print(header)
    print("-" * len(header))
    for k in ALL_METRICS:
        row = f"{k:<22}" + "".join(f"  {r[k]:.4f}   " for r in setup_results)
        print(row)

    print(f"\n--- {setup_name} — mean ± std (3 seeds) ---")
    print(f"{'Metric':<22}  {'mean ± std':>18}")
    print("-" * 45)
    for k in ALL_METRICS:
        vals = np.array([r[k] for r in setup_results])
        mean, std = vals.mean(), vals.std()
        marker = " *" if k in PRIMARY_METRICS else ""
        print(f"{k:<22}  {mean:.3f} ± {std:.3f}{marker}")
        summary_rows.append({
            "setup": setup_name,
            "metric": k,
            "mean": round(mean, 4),
            "std": round(std, 4),
            "is_primary": k in PRIMARY_METRICS,
            **{f"seed_{r['seed']}": round(r[k], 4) for r in setup_results},
        })

    thresholds = np.array([r["threshold"] for r in setup_results])
    print(f"Thresholds: {', '.join(f'{t:.2f}' for t in thresholds)}")

print("\n* = chỉ số chính")

results_df = pd.DataFrame(summary_rows)
results_path = os.path.join(CFG["output_dir"], "setup_b_results.csv")
results_df.to_csv(results_path, index=False)
print(f"\nKết quả tổng hợp đã lưu tại: {results_path}")

# %%
# Cell 12 — Confusion Matrix cho B1 và B2

import matplotlib.pyplot as plt
import seaborn as sns

labels_cm = ["Label 0 (Legit)", "Label 1 (Smishing)"]

def plot_aggregated_confusion_matrix(setup_name, file_name, title_suffix):
    setup_results = [r for r in all_results if r["setup"] == setup_name]
    cm_sum = sum(r["confusion_matrix"] for r in setup_results)
    cm_norm = cm_sum.astype(float) / cm_sum.sum(axis=1, keepdims=True)

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    fig.suptitle(
        f"Setup B — {title_suffix}\n"
        f"Seeds: {CFG['seeds']}  |  Confusion Matrix (aggregated, n={len(setup_results)} seeds)",
        fontsize=12, fontweight="bold",
    )

    sns.heatmap(
        cm_sum, annot=True, fmt="d", cmap="Blues", ax=axes[0],
        xticklabels=labels_cm, yticklabels=labels_cm,
        linewidths=0.5, linecolor="grey",
    )
    axes[0].set_title("Absolute counts (sum across seeds)", fontsize=10)
    axes[0].set_ylabel("Actual", fontsize=10)
    axes[0].set_xlabel("Predicted", fontsize=10)

    sns.heatmap(
        cm_norm, annot=True, fmt=".2f", cmap="Blues", ax=axes[1],
        xticklabels=labels_cm, yticklabels=labels_cm,
        linewidths=0.5, linecolor="grey",
        vmin=0, vmax=1,
    )
    axes[1].set_title("Normalized per actual class (rate)", fontsize=10)
    axes[1].set_ylabel("Actual", fontsize=10)
    axes[1].set_xlabel("Predicted", fontsize=10)

    vals_f1 = np.array([r["f1_label1"] for r in setup_results])
    vals_rc = np.array([r["recall_label1"] for r in setup_results])
    fig.text(
        0.5, -0.02,
        f"F1 Label1: {vals_f1.mean():.3f} ± {vals_f1.std():.3f}  |  "
        f"Recall Label1: {vals_rc.mean():.3f} ± {vals_rc.std():.3f}",
        ha="center", fontsize=10, style="italic",
    )

    plt.tight_layout()

    cm_path = os.path.join(CFG["output_dir"], file_name)
    plt.savefig(cm_path, dpi=150, bbox_inches="tight")
    plt.show()
    print(f"Confusion matrix đã lưu tại: {cm_path}")

plot_aggregated_confusion_matrix(
    "B1_class_weight_default",
    "setup_b_confusion_matrix_class_weight_default.png",
    "B1 Class Weight Default Argmax",
)

plot_aggregated_confusion_matrix(
    "B2_class_weight_threshold",
    "setup_b_confusion_matrix_class_weight_threshold.png",
    "B2 Class Weight + Validation Threshold",
)

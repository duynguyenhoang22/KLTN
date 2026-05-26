# %% [markdown]
# # Setup A — TRTR Real-only Baseline (PhoBERT)
# 
# **Phương pháp:** Train on Real, Test on Real (TRTR)  
# **Model:** `vinai/phobert-base` + `ViTokenizer`  
# **Seeds:** `[42, 123, 2025]`  
# **Split:** Stratified 70 / 15 / 15 (`split_seed=0`, cố định)  
# **Báo cáo:** mean ± std trên tập test thật
# 
# ---
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
# Cell 1 — Install dependencies
!pip uninstall -y peft torchvision torchaudio bitsandbytes
!pip install -q transformers==4.46.3 accelerate==1.1.1 datasets pyvi scikit-learn

# %%
from transformers import TrainingArguments
print("TrainingArguments OK")
from transformers import Trainer          # nếu crash ở đây → xem bước 5
print("Trainer OK")

# %%
# Cell 2 — Configuration
# Toàn bộ hyperparameter và thiết lập thí nghiệm ở một chỗ duy nhất.
# Không thay đổi split_seed để đảm bảo test set giống nhau qua Setup A–F.

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
    early_stop_patience  = 3,           # epochs không cải thiện f1_label1

    # Data split — KHÔNG thay đổi sau khi đã khóa test set
    split_seed           = 0,
    train_ratio          = 0.70,
    val_ratio            = 0.15,
    # test_ratio = 0.15 (phần còn lại)

    # Google Drive paths
    drive_root           = "/content/drive/MyDrive/KLTN",
    data_file            = "vismishds_real.csv",
    output_dir           = "/content/drive/MyDrive/KLTN/setup_a_results",
    work_dir             = "/content/tmp_checkpoints",
)

import os
os.makedirs(CFG["output_dir"], exist_ok=True)
print("CFG loaded.")
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

# Force flush và remount hoàn toàn
drive.flush_and_unmount()
drive.mount(mountpoint, force_remount=True)


import pandas as pd

data_path = os.path.join(CFG["drive_root"], CFG["data_file"])
df = pd.read_csv(data_path)
df["content"] = df["content"].astype(str).fillna("")

print(f"Tổng số mẫu: {len(df)}")
print(f"Cột: {list(df.columns)}")
print("\nPhân phối label (toàn bộ):")
print(df["label"].value_counts().to_string())
print(f"\nTỷ lệ Label 1: {df['label'].mean()*100:.1f}%")

# %%
# Cell 4 — Stratified split 70/15/15 và khóa Real Test Set
#
# split_seed=0 cố định — không thay đổi để đảm bảo test set giống nhau
# qua tất cả setup (A, B, C, D, E, F).
# Test set được lưu ra file riêng ngay lập tức và không tham gia
# vào huấn luyện, chọn checkpoint, hay tuning threshold.

from sklearn.model_selection import train_test_split

# Bước 1: tách test (15%) khỏi phần còn lại (85%)
df_trainval, df_test = train_test_split(
    df,
    test_size=0.15,
    stratify=df["label"],
    random_state=CFG["split_seed"],
)

# Bước 2: tách val (15% tổng = ~17.6% của trainval) khỏi train
val_size_relative = CFG["val_ratio"] / (CFG["train_ratio"] + CFG["val_ratio"])
df_train, df_val = train_test_split(
    df_trainval,
    test_size=val_size_relative,
    stratify=df_trainval["label"],
    random_state=CFG["split_seed"],
)

# Lưu test set — KHÔNG chạy lại cell này sau khi đã lưu
test_save_path = os.path.join(CFG["output_dir"], "setup_a_real_test.csv")
df_test.to_csv(test_save_path, index=False)
print(f"[LOCKED] Real Test Set đã lưu tại: {test_save_path}")

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
#
# PhoBERT yêu cầu word-segmented input. ViTokenizer.tokenize() chèn
# dấu gạch dưới để nối syllable thành word token trước khi
# AutoTokenizer xử lý BPE.

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

print("Tokenizer loaded.")
print(f"Vocab size: {tokenizer.vocab_size}")

# %%
# Cell 6 — compute_metrics (đầy đủ chỉ số theo kế hoạch đánh giá)
#
# Chỉ số chính: macro_f1, f1_label1, recall_label1, precision_label1, auprc
# Chỉ số phụ : accuracy, auroc
# AUPRC và AUROC dùng xác suất class-1 từ softmax (không chỉ argmax).

import numpy as np
from scipy.special import softmax
from sklearn.metrics import (
    f1_score,
    precision_score,
    recall_score,
    accuracy_score,
    average_precision_score,
    roc_auc_score,
)

def compute_metrics(pred):
    labels = pred.label_ids
    logits = pred.predictions
    probs  = softmax(logits, axis=-1)[:, 1]   # P(label=1)
    preds  = logits.argmax(-1)

    return {
        # --- chỉ số chính ---
        "macro_f1":         f1_score(labels, preds, average="macro",  zero_division=0),
        "f1_label1":        f1_score(labels, preds, pos_label=1, average="binary", zero_division=0),
        "recall_label1":    recall_score(labels, preds, pos_label=1, zero_division=0),
        "precision_label1": precision_score(labels, preds, pos_label=1, zero_division=0),
        "auprc":            average_precision_score(labels, probs),
        # --- chỉ số phụ ---
        "accuracy":         accuracy_score(labels, preds),
        "auroc":            roc_auc_score(labels, probs),
    }

print("compute_metrics registered.")
print("Primary   : macro_f1, f1_label1, recall_label1, precision_label1, auprc")
print("Secondary : accuracy, auroc")

# %%
# Cell 7 — set_seed_everything
#
# Seed đồng thời random, numpy, torch (CPU + CUDA), và transformers
# để đảm bảo reproducibility giữa các lần chạy.

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
    print(f"[seed] Set all seeds to {seed}")

print("set_seed_everything defined.")

# %%
# Cell 8 — Import Trainer (run AFTER Cell 1 + restart)
# Kernel crash here = peft/torchvision still broken, or Colab GPU disconnected.
# Fix: Runtime → Factory reset → Cell 1 → Restart → Cell 2–8.

import subprocess, sys
subprocess.run([sys.executable, "-m", "pip", "uninstall", "-y", "peft"], capture_output=True)

from transformers import (
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments,
    EarlyStoppingCallback,
)

import torch
print("transformers OK — Trainer imported.")
print(f"  transformers : {__import__('transformers').__version__}")
print(f"  CUDA         : {torch.cuda.is_available()}")

# %%
# Cell 9 — train_one_seed
#
# Trainer imported in Cell 8. This cell only defines the training function.

import gc
import shutil
from sklearn.metrics import confusion_matrix

def _free_gpu():
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.synchronize()

def train_one_seed(seed: int, train_ds, val_ds, test_ds):
    print(f"\n{'='*60}")
    print(f"  SEED {seed}")
    print(f"{'='*60}")

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
        dataloader_num_workers      = 0,   # tránh fork crash trên Colab
        dataloader_pin_memory       = False,
    )

    trainer = Trainer(
        model           = model,
        args            = training_args,
        train_dataset   = train_ds,
        eval_dataset    = val_ds,
        compute_metrics = compute_metrics,
        callbacks       = [EarlyStoppingCallback(
                              early_stopping_patience=CFG["early_stop_patience"]
                           )],
    )

    trainer.train()

    test_output = trainer.predict(test_ds)
    test_metrics = test_output.metrics

    logits = test_output.predictions
    preds  = logits.argmax(-1)
    labels = test_output.label_ids
    cm     = confusion_matrix(labels, preds, labels=[0, 1])

    clean = {k.replace("test_", ""): v for k, v in test_metrics.items()
             if k not in ("test_loss", "test_runtime",
                          "test_samples_per_second", "test_steps_per_second")}

    clean["seed"]             = seed
    clean["confusion_matrix"] = cm
    clean["best_epoch"]       = trainer.state.best_model_checkpoint

    print(f"\n[Seed {seed}] Test results:")
    for k, v in clean.items():
        if k not in ("confusion_matrix", "seed", "best_epoch"):
            print(f"  {k:<22}: {v:.4f}")
    print(f"  confusion_matrix:\n{cm}")

    # Giải phóng GPU/RAM trước seed tiếp theo
    del trainer, model, test_output
    if os.path.exists(run_dir):
        shutil.rmtree(run_dir, ignore_errors=True)
    _free_gpu()

    return clean

print("train_one_seed defined.")

# %%
# Cell 10 — Pre-tokenize once + multi-seed training loop
#
# Tokenize trước vòng lặp (1 lần) thay vì 3 lần/seed.
# Nếu crash giữa chừng: chạy lại từ cell này (all_results = [] nếu chạy lại từ đầu).

# Kiểm tra GPU trước khi train
if torch.cuda.is_available():
    props = torch.cuda.get_device_properties(0)
    print(f"GPU: {props.name}  |  VRAM: {props.total_memory / 1e9:.1f} GB")
else:
    print("WARNING: No GPU — training will be very slow on CPU.")

print("Tokenizing train / val / test (one time)...")
train_ds = make_hf_dataset(df_train)
val_ds   = make_hf_dataset(df_val)
test_ds  = make_hf_dataset(df_test)
print(f"  train: {len(train_ds)}  val: {len(val_ds)}  test: {len(test_ds)}")

all_results = []

for seed in CFG["seeds"]:
    result = train_one_seed(seed, train_ds, val_ds, test_ds)
    all_results.append(result)

print(f"\nHoàn thành {len(all_results)}/{len(CFG['seeds'])} seed.")

# %%
# Cell 11 — Tổng hợp kết quả: mean ± std
#
# Chỉ số chính báo cáo mean ± std theo kế hoạch (section 5.2, 11).
# Kết quả lưu ra setup_a_results.csv trên Drive.

import pandas as pd

PRIMARY_METRICS   = ["macro_f1", "f1_label1", "recall_label1",
                     "precision_label1", "auprc"]
SECONDARY_METRICS = ["accuracy", "auroc"]
ALL_METRICS       = PRIMARY_METRICS + SECONDARY_METRICS

print("\n" + "="*65)
print("  SETUP A — TRTR Real-only Baseline (PhoBERT)")
print("  Kết quả trên Real Test Set")
print("="*65)

summary_rows = []

# Per-seed
print("\n--- Kết quả từng seed ---")
header = f"{'Metric':<22}" + "".join(f"  Seed {r['seed']}" for r in all_results)
print(header)
print("-" * len(header))
for k in ALL_METRICS:
    row = f"{k:<22}" + "".join(f"  {r[k]:.4f}   " for r in all_results)
    print(row)

# Mean ± std
print("\n--- mean ± std (3 seeds) ---")
print(f"{'Metric':<22}  {'mean ± std':>18}")
print("-" * 45)
for k in ALL_METRICS:
    vals = np.array([r[k] for r in all_results])
    mean, std = vals.mean(), vals.std()
    marker = " *" if k in PRIMARY_METRICS else ""
    print(f"{k:<22}  {mean:.3f} ± {std:.3f}{marker}")
    summary_rows.append({"metric": k, "mean": round(mean, 4), "std": round(std, 4),
                         "is_primary": k in PRIMARY_METRICS,
                         **{f"seed_{r['seed']}": round(r[k], 4) for r in all_results}})

print("\n* = chỉ số chính")

# Lưu CSV
results_df = pd.DataFrame(summary_rows)
results_path = os.path.join(CFG["output_dir"], "setup_a_results.csv")
results_df.to_csv(results_path, index=False)
print(f"\nKết quả đã lưu tại: {results_path}")

# %%
# Cell 12 — Confusion Matrix (tổng hợp qua 3 seed)
#
# Vẽ hai panel:
#   - Trái: confusion matrix tổng (sum across seeds) — hiển thị số tuyệt đối.
#   - Phải: confusion matrix chuẩn hóa theo actual (tỷ lệ per row).
# Lưu PNG lên Drive.

import matplotlib.pyplot as plt
import seaborn as sns

cm_sum = sum(r["confusion_matrix"] for r in all_results)
cm_norm = cm_sum.astype(float) / cm_sum.sum(axis=1, keepdims=True)

labels_cm = ["Label 0 (Legit)", "Label 1 (Smishing)"]

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
fig.suptitle(
    f"Setup A — TRTR Real-only Baseline (PhoBERT)\n"
    f"Seeds: {CFG['seeds']}  |  Confusion Matrix (aggregated, n={len(all_results)} seeds)",
    fontsize=12, fontweight="bold",
)

# Panel 1: absolute counts
sns.heatmap(
    cm_sum, annot=True, fmt="d", cmap="Blues", ax=axes[0],
    xticklabels=labels_cm, yticklabels=labels_cm,
    linewidths=0.5, linecolor="grey",
)
axes[0].set_title("Absolute counts (sum across seeds)", fontsize=10)
axes[0].set_ylabel("Actual", fontsize=10)
axes[0].set_xlabel("Predicted", fontsize=10)

# Panel 2: normalized (rate per row)
sns.heatmap(
    cm_norm, annot=True, fmt=".2f", cmap="Blues", ax=axes[1],
    xticklabels=labels_cm, yticklabels=labels_cm,
    linewidths=0.5, linecolor="grey",
    vmin=0, vmax=1,
)
axes[1].set_title("Normalized per actual class (rate)", fontsize=10)
axes[1].set_ylabel("Actual", fontsize=10)
axes[1].set_xlabel("Predicted", fontsize=10)

# Annotate summary stats
vals_f1 = np.array([r["f1_label1"] for r in all_results])
vals_rc = np.array([r["recall_label1"] for r in all_results])
fig.text(
    0.5, -0.02,
    f"F1 Label1: {vals_f1.mean():.3f} ± {vals_f1.std():.3f}  |  "
    f"Recall Label1: {vals_rc.mean():.3f} ± {vals_rc.std():.3f}",
    ha="center", fontsize=10, style="italic",
)

plt.tight_layout()

cm_path = os.path.join(CFG["output_dir"], "setup_a_confusion_matrix.png")
plt.savefig(cm_path, dpi=150, bbox_inches="tight")
plt.show()
print(f"Confusion matrix đã lưu tại: {cm_path}")



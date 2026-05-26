# %% [markdown]
# # Setup C — TSTR matched distribution (PhoBERT)
#
# **Phương pháp:** Train on Synthetic, Test on Real (TSTR)  
# **Model:** `vinai/phobert-base` + `ViTokenizer`  
# **Seeds:** `[42, 123, 2025]`  
# **Split real:** Stratified 70 / 15 / 15 (`split_seed=0`, cố định như Setup A/B)  
# **Synthetic train:** matched distribution theo số lượng Label 0/1 của Real Train  
# **Báo cáo:** mean ± std trên Real Test Set
#
# ---
# **Mục tiêu Setup C:** kiểm tra synthetic data có mang tín hiệu phân loại tương tự real data
# khi không có lợi thế về số lượng hoặc tỷ lệ nhãn.
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
# Giữ nguyên các thiết lập cốt lõi từ Setup A/B để so sánh công bằng.

CFG = dict(
    # Model
    model_name              = "vinai/phobert-base",
    max_length              = 128,

    # Training
    seeds                   = [42, 123, 2025],
    num_epochs              = 10,
    train_batch             = 16,
    eval_batch              = 32,
    learning_rate           = 2e-5,
    weight_decay            = 0.01,
    warmup_ratio            = 0.1,
    early_stop_patience     = 3,

    # Real data split — KHÔNG thay đổi để tái tạo đúng split của Setup A/B
    split_seed              = 0,
    train_ratio             = 0.70,
    val_ratio               = 0.15,

    # Synthetic matched sampling — cố định subset synthetic cho cả 3 training seeds
    synthetic_sample_seed   = 0,

    # data_origin mapping
    real_origin_values      = ["real"],
    synthetic_origin_values = ["synthetic", "paraphrased", "synthetic_hard_negative"],

    # Đường dẫn Google Drive
    drive_root              = "/content/drive/MyDrive/KLTN",
    data_file               = "vismishds_content_label_origin.csv",
    setup_a_test_file       = "/content/drive/MyDrive/KLTN/setup_a_results/setup_a_real_test.csv",
    output_dir              = "/content/drive/MyDrive/KLTN/setup_c_results",
    work_dir                = "/content/tmp_checkpoints_setup_c",
)

import os
os.makedirs(CFG["output_dir"], exist_ok=True)
print("Đã load CFG.")
print(f"  model_name              : {CFG['model_name']}")
print(f"  seeds                   : {CFG['seeds']}")
print(f"  split_seed              : {CFG['split_seed']}")
print(f"  synthetic_sample_seed   : {CFG['synthetic_sample_seed']}")
print(f"  max_length              : {CFG['max_length']}")
print(f"  num_epochs (max)        : {CFG['num_epochs']}")
print(f"  early_stop_patience     : {CFG['early_stop_patience']}")
print(f"  learning_rate           : {CFG['learning_rate']}")
print(f"  output_dir              : {CFG['output_dir']}")

# %%
# Cell 3 — Mount Google Drive và load dữ liệu tổng hợp đã rút gọn
# Trước khi chạy: upload vismishds_content_label_origin.csv lên MyDrive/KLTN/

import os
import shutil
from google.colab import drive

mountpoint = "/content/drive"

drive.flush_and_unmount()
drive.mount(mountpoint, force_remount=True)

import pandas as pd

data_path = os.path.join(CFG["drive_root"], CFG["data_file"])
df_all = pd.read_csv(data_path)

required_columns = {"content", "label", "data_origin"}
missing_columns = required_columns - set(df_all.columns)
assert not missing_columns, f"Dataset thiếu cột bắt buộc: {missing_columns}"

df_all["content"] = df_all["content"].astype(str).fillna("")
df_all["data_origin"] = df_all["data_origin"].astype(str).fillna("")
labels_found = set(df_all["label"].dropna().unique().tolist())
assert labels_found <= {0, 1}, f"Label chỉ được gồm 0/1, nhưng tìm thấy: {labels_found}"
df_all["label"] = df_all["label"].astype(int)

print(f"Tổng số mẫu: {len(df_all)}")
print(f"Cột: {list(df_all.columns)}")
print("\nPhân phối data_origin:")
print(df_all["data_origin"].value_counts(dropna=False).to_string())
print("\nPhân phối label x data_origin:")
print(pd.crosstab(df_all["data_origin"], df_all["label"]).to_string())

# %%
# Cell 4 — Tách real/synthetic theo data_origin
#
# - Real chỉ dùng data_origin == "real" để khớp Setup A/B.
# - Synthetic gồm "synthetic", "paraphrased", "synthetic_hard_negative".
#   Trong đó "paraphrased" là synthetic đã được paraphrase để giảm pattern rập khuôn.

real_origins = set(CFG["real_origin_values"])
synthetic_origins = set(CFG["synthetic_origin_values"])

df_real = df_all[df_all["data_origin"].isin(real_origins)].copy()
df_synthetic_candidates = df_all[df_all["data_origin"].isin(synthetic_origins)].copy()

assert len(df_real) > 0, "Không có mẫu real nào sau khi lọc data_origin."
assert len(df_synthetic_candidates) > 0, "Không có mẫu synthetic nào sau khi lọc data_origin."

print("\nReal origins dùng cho split:")
print(df_real["data_origin"].value_counts().to_string())
print("\nSynthetic origins dùng cho Setup C:")
print(df_synthetic_candidates["data_origin"].value_counts().to_string())

def print_label_info(name, frame):
    counts = frame["label"].value_counts().sort_index()
    print(f"\n{name}: {len(frame)} mẫu")
    print(f"  Label 0: {counts.get(0, 0)}")
    print(f"  Label 1: {counts.get(1, 0)}")

print_label_info("Real data", df_real)
print_label_info("Synthetic candidates", df_synthetic_candidates)

# %%
# Cell 5 — Tạo Real Val/Test và ưu tiên Real Test Set đã khóa của Setup A
#
# vismishds_content_label_origin.csv không nhất thiết giữ cùng thứ tự dòng real như
# vismishds_real.csv. Vì vậy nếu setup_a_real_test.csv tồn tại, Setup C sẽ dùng
# chính file đó làm Real Test Set đã khóa, thay vì tin vào split theo vị trí dòng.
#
# Real Test chỉ dùng để đánh giá cuối, không dùng để tune threshold, và không dùng
# để chọn hyperparameter.

from sklearn.model_selection import train_test_split

def add_match_index(frame):
    matched = frame.copy()
    matched["_match_key"] = (
        matched["content"].astype(str) + "||" + matched["label"].astype(str)
    )
    matched["_match_ord"] = matched.groupby("_match_key").cumcount()
    return matched

def drop_locked_test_from_real(real_frame, locked_test_frame):
    real_indexed = add_match_index(real_frame)
    locked_indexed = add_match_index(locked_test_frame)

    locked_keys = locked_indexed[["_match_key", "_match_ord"]].copy()
    locked_keys["_is_locked_test"] = True

    test_selected = locked_indexed.merge(
        real_indexed,
        on=["_match_key", "_match_ord"],
        how="left",
        suffixes=("_locked", ""),
    )
    assert test_selected["content"].notna().all(), (
        "Một số dòng trong setup_a_real_test.csv không tìm thấy trong real pool của file mới."
    )

    real_marked = real_indexed.merge(
        locked_keys,
        on=["_match_key", "_match_ord"],
        how="left",
    )
    trainval_pool = (
        real_marked[real_marked["_is_locked_test"].isna()]
        .drop(columns=["_match_key", "_match_ord", "_is_locked_test"])
        .copy()
    )
    test_frame = locked_test_frame.copy()
    return trainval_pool, test_frame

setup_a_test_path = CFG["setup_a_test_file"]
if os.path.exists(setup_a_test_path):
    setup_a_test = pd.read_csv(setup_a_test_path)
    setup_a_test["content"] = setup_a_test["content"].astype(str).fillna("")
    setup_a_test["label"] = setup_a_test["label"].astype(int)

    df_trainval_pool, df_test = drop_locked_test_from_real(
        df_real,
        setup_a_test[["content", "label"]],
    )
    print(f"[OK] Đã dùng Real Test Set đã khóa của Setup A: {setup_a_test_path}")
    print("     Lưu ý: Real Val được split lại từ phần real còn lại vì file mới không giữ thứ tự gốc.")
else:
    print("[WARNING] Không tìm thấy setup_a_real_test.csv.")
    print("          Setup C sẽ dùng Real Test Set tái tạo từ split_seed=0.")
    df_trainval_pool, df_test = train_test_split(
        df_real,
        test_size=0.15,
        stratify=df_real["label"],
        random_state=CFG["split_seed"],
    )

val_size_relative = CFG["val_ratio"] / (CFG["train_ratio"] + CFG["val_ratio"])
df_train_real, df_val = train_test_split(
    df_trainval_pool,
    test_size=val_size_relative,
    stratify=df_trainval_pool["label"],
    random_state=CFG["split_seed"],
)

def print_split_info(name, split_df):
    counts = split_df["label"].value_counts().sort_index()
    print(f"\n{name}: {len(split_df)} mẫu")
    print(f"  Label 0: {counts.get(0, 0)}  ({counts.get(0,0)/len(split_df)*100:.1f}%)")
    print(f"  Label 1: {counts.get(1, 0)}  ({counts.get(1,0)/len(split_df)*100:.1f}%)")

print_split_info("Real Train reference (70%)", df_train_real)
print_split_info("Real Val             (15%)", df_val)
print_split_info("Real Test            (15%)", df_test)

# %%
# Cell 6 — Kiểm tra duplicate giữa synthetic candidates và Real Test
#
# Setup C loại exact duplicate và normalized duplicate trước khi sampling synthetic train.
# Đây là kiểm tra nhẹ, tiết kiệm tài nguyên, nhưng chặn rò rỉ trực tiếp vào Real Test.

import re

def normalize_text_for_leak_check(text):
    text = str(text).lower().strip()
    text = re.sub(r"\s+", " ", text)
    return text

real_test_exact = set(df_test["content"].astype(str))
real_test_norm = set(df_test["content"].map(normalize_text_for_leak_check))

leak_rows = []
for idx, row in df_synthetic_candidates.iterrows():
    content = str(row["content"])
    exact_match = content in real_test_exact
    normalized_match = normalize_text_for_leak_check(content) in real_test_norm
    if exact_match or normalized_match:
        leak_rows.append({
            "source_index": idx,
            "content": content,
            "label": row["label"],
            "data_origin": row["data_origin"],
            "exact_match": exact_match,
            "normalized_match": normalized_match,
        })

leakage_report = pd.DataFrame(leak_rows)
leakage_path = os.path.join(CFG["output_dir"], "setup_c_leakage_report.csv")
leakage_report.to_csv(leakage_path, index=False)
print(f"Leakage report đã lưu tại: {leakage_path}")
print(f"Số synthetic candidate trùng Real Test: {len(leakage_report)}")

if len(leakage_report) > 0:
    leaked_indices = set(leakage_report["source_index"].tolist())
    df_synthetic_clean = df_synthetic_candidates.drop(index=leaked_indices).copy()
else:
    df_synthetic_clean = df_synthetic_candidates.copy()

print_label_info("Synthetic candidates sau khi loại duplicate với Real Test", df_synthetic_clean)

# %%
# Cell 7 — Tạo Synthetic Train matched distribution
#
# Số lượng Label 0/1 của Synthetic Train khớp với Real Train reference.
# Synthetic subset được sample cố định bằng synthetic_sample_seed và dùng chung cho 3 training seeds.

target_counts = df_train_real["label"].value_counts().sort_index().to_dict()
available_counts = df_synthetic_clean["label"].value_counts().sort_index().to_dict()

for label, target_count in target_counts.items():
    available_count = available_counts.get(label, 0)
    assert available_count >= target_count, (
        f"Không đủ synthetic Label {label}: cần {target_count}, chỉ có {available_count}"
    )

matched_parts = []
for label in [0, 1]:
    n = target_counts.get(label, 0)
    part = (
        df_synthetic_clean[df_synthetic_clean["label"] == label]
        .sample(n=n, random_state=CFG["synthetic_sample_seed"])
        .copy()
    )
    matched_parts.append(part)

df_train_synthetic = (
    pd.concat(matched_parts, axis=0)
    .sample(frac=1.0, random_state=CFG["synthetic_sample_seed"])
    .reset_index(drop=True)
)

synthetic_train_path = os.path.join(CFG["output_dir"], "setup_c_synthetic_train_matched.csv")
df_train_synthetic[["content", "label", "data_origin"]].to_csv(synthetic_train_path, index=False)

print_split_info("Synthetic Train matched", df_train_synthetic)
print("\nPhân phối data_origin trong Synthetic Train matched:")
print(df_train_synthetic["data_origin"].value_counts().to_string())
print(f"\nSynthetic Train matched đã lưu tại: {synthetic_train_path}")

# %%
# Cell 8 — Tokenization (ViTokenizer + PhoBERT AutoTokenizer)

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
# Cell 9 — compute_metrics
#
# Chỉ số chính: macro_f1, f1_label1, recall_label1, precision_label1, auprc
# Chỉ số phụ : accuracy, auroc
# AUPRC và AUROC dùng xác suất class-1 từ softmax.

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

PRIMARY_METRICS   = ["macro_f1", "f1_label1", "recall_label1",
                     "precision_label1", "auprc"]
SECONDARY_METRICS = ["accuracy", "auroc"]
ALL_METRICS       = PRIMARY_METRICS + SECONDARY_METRICS

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

print("Đã đăng ký compute_metrics.")
print("Chỉ số chính: macro_f1, f1_label1, recall_label1, precision_label1, auprc")
print("Chỉ số phụ  : accuracy, auroc")

# %%
# Cell 10 — set_seed_everything

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
# Cell 11 — Import Trainer
# Kernel crash ở đây = peft/torchvision vẫn lỗi, hoặc Colab GPU bị ngắt kết nối.
# Fix: Runtime -> Factory reset -> Cell 1 -> Restart -> Cell 2-11.

import subprocess, sys
subprocess.run([sys.executable, "-m", "pip", "uninstall", "-y", "peft"], capture_output=True)

from transformers import (
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments,
    EarlyStoppingCallback,
)

import torch
print("transformers OK — đã import Trainer.")
print(f"  transformers : {__import__('transformers').__version__}")
print(f"  CUDA         : {torch.cuda.is_available()}")

# %%
# Cell 12 — train_one_seed

import gc
import shutil
from sklearn.metrics import confusion_matrix

def _free_gpu():
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.synchronize()

def train_one_seed(seed: int, train_ds, val_ds, test_ds):
    print(f"\n{'='*70}")
    print(f"  SEED {seed} — Setup C: Synthetic matched -> Real Test")
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

    clean["setup"]            = "C_tstr_matched"
    clean["seed"]             = seed
    clean["confusion_matrix"] = cm
    clean["best_epoch"]       = trainer.state.best_model_checkpoint

    print(f"\n[Seed {seed}] Kết quả test — Setup C:")
    for k in ALL_METRICS:
        print(f"  {k:<22}: {clean[k]:.4f}")
    print(f"  confusion_matrix:\n{cm}")

    del trainer, model, test_output
    if os.path.exists(run_dir):
        shutil.rmtree(run_dir, ignore_errors=True)
    _free_gpu()

    return clean

print("Đã định nghĩa train_one_seed.")

# %%
# Cell 13 — Tokenize một lần + vòng lặp huấn luyện nhiều seed

if torch.cuda.is_available():
    props = torch.cuda.get_device_properties(0)
    print(f"GPU: {props.name}  |  VRAM: {props.total_memory / 1e9:.1f} GB")
else:
    print("WARNING: Không có GPU — huấn luyện trên CPU sẽ rất chậm.")

print("Đang tokenize synthetic train / real val / real test (một lần)...")
train_ds = make_hf_dataset(df_train_synthetic)
val_ds   = make_hf_dataset(df_val)
test_ds  = make_hf_dataset(df_test)
print(f"  synthetic train: {len(train_ds)}  real val: {len(val_ds)}  real test: {len(test_ds)}")

all_results = []

for seed in CFG["seeds"]:
    result = train_one_seed(seed, train_ds, val_ds, test_ds)
    all_results.append(result)

assert len(all_results) == len(CFG["seeds"]), (
    f"Thiếu kết quả seed: expected {len(CFG['seeds'])}, got {len(all_results)}"
)
print(f"\nHoàn thành {len(all_results)}/{len(CFG['seeds'])} seed.")

# %%
# Cell 14 — Tổng hợp kết quả: per-seed và mean ± std

print("\n" + "="*78)
print("  SETUP C — TSTR matched distribution (PhoBERT)")
print("  Train: Synthetic matched | Validation/Test: Real")
print("  Kết quả trên Real Test Set")
print("="*78)

summary_rows = []
per_seed_rows = []

for result in all_results:
    row = {
        "setup": result["setup"],
        "seed": result["seed"],
        "best_epoch": result["best_epoch"],
    }
    for k in ALL_METRICS:
        row[k] = round(result[k], 4)
    per_seed_rows.append(row)

per_seed_df = pd.DataFrame(per_seed_rows)
per_seed_path = os.path.join(CFG["output_dir"], "setup_c_per_seed_results.csv")
per_seed_df.to_csv(per_seed_path, index=False)
print(f"\nKết quả từng seed đã lưu tại: {per_seed_path}")

print("\n--- Kết quả từng seed ---")
header = f"{'Metric':<22}" + "".join(f"  Seed {r['seed']}" for r in all_results)
print(header)
print("-" * len(header))
for k in ALL_METRICS:
    row = f"{k:<22}" + "".join(f"  {r[k]:.4f}   " for r in all_results)
    print(row)

print("\n--- mean ± std (3 seeds) ---")
print(f"{'Metric':<22}  {'mean ± std':>18}")
print("-" * 45)
for k in ALL_METRICS:
    vals = np.array([r[k] for r in all_results])
    mean, std = vals.mean(), vals.std()
    marker = " *" if k in PRIMARY_METRICS else ""
    print(f"{k:<22}  {mean:.3f} ± {std:.3f}{marker}")
    summary_rows.append({
        "setup": "C_tstr_matched",
        "metric": k,
        "mean": round(mean, 4),
        "std": round(std, 4),
        "is_primary": k in PRIMARY_METRICS,
        **{f"seed_{r['seed']}": round(r[k], 4) for r in all_results},
    })

print("\n* = chỉ số chính")

results_df = pd.DataFrame(summary_rows)
results_path = os.path.join(CFG["output_dir"], "setup_c_results.csv")
results_df.to_csv(results_path, index=False)
print(f"\nKết quả tổng hợp đã lưu tại: {results_path}")

# %%
# Cell 15 — Confusion Matrix tổng hợp qua 3 seed

import matplotlib.pyplot as plt
import seaborn as sns

cm_sum = sum(r["confusion_matrix"] for r in all_results)
cm_norm = cm_sum.astype(float) / cm_sum.sum(axis=1, keepdims=True)

labels_cm = ["Label 0 (Legit)", "Label 1 (Smishing)"]

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
fig.suptitle(
    f"Setup C — TSTR matched distribution (PhoBERT)\n"
    f"Seeds: {CFG['seeds']}  |  Confusion Matrix (aggregated, n={len(all_results)} seeds)",
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

vals_f1 = np.array([r["f1_label1"] for r in all_results])
vals_rc = np.array([r["recall_label1"] for r in all_results])
fig.text(
    0.5, -0.02,
    f"F1 Label1: {vals_f1.mean():.3f} ± {vals_f1.std():.3f}  |  "
    f"Recall Label1: {vals_rc.mean():.3f} ± {vals_rc.std():.3f}",
    ha="center", fontsize=10, style="italic",
)

plt.tight_layout()

cm_path = os.path.join(CFG["output_dir"], "setup_c_confusion_matrix.png")
plt.savefig(cm_path, dpi=150, bbox_inches="tight")
plt.show()
print(f"Confusion matrix đã lưu tại: {cm_path}")

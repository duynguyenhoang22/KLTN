# %% [markdown]
# # Setup F3 — Kaggle run (Label 0 source augmentation, PhoBERT)
#
# **Variant:** `F3_external_plus_synthetic_label0`  
# **Train:** Real Train + Synthetic Label 1 + external_real Label 0 + external_curated Label 0 + Synthetic Label 0  
# **Validation/Test:** Real Validation / Real Test Set đã khóa từ Setup A  
# **Model:** `vinai/phobert-base` + `ViTokenizer`  
# **Seeds:** `[42, 123, 2025]`
#
# Notebook/script này được tách riêng để chạy F3 trên Kaggle. Kết quả được lưu
# sau từng seed để tránh mất dữ liệu nếu session hết hạn.

# %%
# Cell 1 — Install dependencies
# Kaggle: bật Internet nếu môi trường chưa có transformers/datasets/pyvi.
!pip uninstall -y peft torchvision torchaudio bitsandbytes
!pip install -q transformers==4.46.3 accelerate==1.1.1 datasets pyvi scikit-learn seaborn

# %%
# Cell 2 — Configuration

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

    # Real validation split — dùng khi Real Test đã lấy từ file khóa của Setup A
    split_seed              = 0,
    val_ratio               = 0.15,
    train_ratio             = 0.70,

    # F3 fixed variant
    variant_name            = "F3_external_plus_synthetic_label0",
    synthetic_sample_seed   = 0,

    # data_origin mapping
    real_origin_values      = ["real"],
    synthetic_origin_values = ["synthetic", "paraphrased", "synthetic_hard_negative"],
    external_real_origin_values = ["external_real"],
    external_curated_origin_values = ["external_curated"],

    # Kaggle paths
    input_root              = "/kaggle/input",
    output_dir              = "/kaggle/working/setup_f3_results",
    work_dir                = "/kaggle/working/tmp_checkpoints_setup_f3",

    # File names to auto-find under /kaggle/input
    data_file_name          = "vismishds_content_label_origin.csv",
    setup_a_test_file_name  = "setup_a_real_test.csv",
)

import os
os.makedirs(CFG["output_dir"], exist_ok=True)
os.makedirs(CFG["work_dir"], exist_ok=True)

print("Loaded CFG")
for key in [
    "model_name", "seeds", "variant_name", "split_seed", "synthetic_sample_seed",
    "max_length", "num_epochs", "learning_rate", "output_dir",
]:
    print(f"  {key:<24}: {CFG[key]}")

# %%
# Cell 3 — Locate Kaggle input files
#
# Upload/create a Kaggle Dataset containing:
# - vismishds_content_label_origin.csv
# - setup_a_real_test.csv
#
# Then add that dataset to this Kaggle notebook.

from pathlib import Path

def find_input_file(file_name):
    matches = sorted(Path(CFG["input_root"]).rglob(file_name))
    assert matches, (
        f"Không tìm thấy {file_name} dưới {CFG['input_root']}. "
        "Hãy add Kaggle Dataset chứa file này vào notebook."
    )
    if len(matches) > 1:
        print(f"[WARNING] Tìm thấy nhiều file {file_name}, dùng file đầu tiên:")
        for path in matches:
            print(f"  - {path}")
    return str(matches[0])

data_path = find_input_file(CFG["data_file_name"])
setup_a_test_path = find_input_file(CFG["setup_a_test_file_name"])

print(f"data_path        : {data_path}")
print(f"setup_a_test_path: {setup_a_test_path}")

# %%
# Cell 4 — Load data

import pandas as pd

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
# Cell 5 — Split real/synthetic/external pools

real_origins = set(CFG["real_origin_values"])
synthetic_origins = set(CFG["synthetic_origin_values"])
external_real_origins = set(CFG["external_real_origin_values"])
external_curated_origins = set(CFG["external_curated_origin_values"])

df_real = df_all[df_all["data_origin"].isin(real_origins)].copy()
df_synthetic_candidates = df_all[df_all["data_origin"].isin(synthetic_origins)].copy()
df_external_real_label0_candidates = df_all[df_all["data_origin"].isin(external_real_origins)].copy()
df_external_curated_label0_candidates = df_all[df_all["data_origin"].isin(external_curated_origins)].copy()
df_external_label0_candidates = pd.concat(
    [df_external_real_label0_candidates, df_external_curated_label0_candidates],
    axis=0,
).copy()

assert len(df_real) > 0, "Không có mẫu real nào sau khi lọc data_origin."
assert len(df_synthetic_candidates) > 0, "Không có mẫu synthetic nào sau khi lọc data_origin."
assert len(df_external_real_label0_candidates) > 0, "Không có external_real Label 0."
assert len(df_external_curated_label0_candidates) > 0, "Không có external_curated Label 0."
assert set(df_external_label0_candidates["label"].unique().tolist()) <= {0}, (
    "Nhóm external_real/external_curated chỉ được chứa Label 0 trong Setup F3."
)

def print_label_info(name, frame):
    counts = frame["label"].value_counts().sort_index()
    print(f"\n{name}: {len(frame)} mẫu")
    print(f"  Label 0: {counts.get(0, 0)}")
    print(f"  Label 1: {counts.get(1, 0)}")

print_label_info("Real data", df_real)
print_label_info("Synthetic candidates", df_synthetic_candidates)
print_label_info("External real Label 0 candidates", df_external_real_label0_candidates)
print_label_info("External curated Label 0 candidates", df_external_curated_label0_candidates)

# %%
# Cell 6 — Recreate locked Real Train/Validation/Test

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
        "Một số dòng trong setup_a_real_test.csv không tìm thấy trong real pool."
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

setup_a_test = pd.read_csv(setup_a_test_path)
setup_a_test["content"] = setup_a_test["content"].astype(str).fillna("")
setup_a_test["label"] = setup_a_test["label"].astype(int)

df_real_trainval_pool, df_test = drop_locked_test_from_real(
    df_real,
    setup_a_test[["content", "label"]],
)

val_size_relative = CFG["val_ratio"] / (CFG["train_ratio"] + CFG["val_ratio"])
df_train_real, df_val = train_test_split(
    df_real_trainval_pool,
    test_size=val_size_relative,
    stratify=df_real_trainval_pool["label"],
    random_state=CFG["split_seed"],
)

def print_split_info(name, split_df):
    counts = split_df["label"].value_counts().sort_index()
    print(f"\n{name}: {len(split_df)} mẫu")
    print(f"  Label 0: {counts.get(0, 0)}  ({counts.get(0,0)/len(split_df)*100:.1f}%)")
    print(f"  Label 1: {counts.get(1, 0)}  ({counts.get(1,0)/len(split_df)*100:.1f}%)")

print_split_info("Real Train", df_train_real)
print_split_info("Real Val", df_val)
print_split_info("Real Test", df_test)

# %%
# Cell 7 — Leakage check against Real Test

import re

def normalize_text_for_leak_check(text):
    text = str(text).lower().strip()
    text = re.sub(r"\s+", " ", text)
    return text

real_test_exact = set(df_test["content"].astype(str))
real_test_norm = set(df_test["content"].map(normalize_text_for_leak_check))

df_augmentation_candidates = pd.concat(
    [df_synthetic_candidates, df_external_label0_candidates],
    axis=0,
).copy()

leak_rows = []
for idx, row in df_augmentation_candidates.iterrows():
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
leakage_path = os.path.join(CFG["output_dir"], "setup_f3_leakage_report.csv")
leakage_report.to_csv(leakage_path, index=False)
print(f"Leakage report đã lưu tại: {leakage_path}")
print(f"Số augmentation candidate trùng Real Test: {len(leakage_report)}")

if len(leakage_report) > 0:
    leaked_indices = set(leakage_report["source_index"].tolist())
    df_synthetic_clean = df_synthetic_candidates.drop(
        index=df_synthetic_candidates.index.intersection(leaked_indices)
    ).copy()
    df_external_real_label0_clean = df_external_real_label0_candidates.drop(
        index=df_external_real_label0_candidates.index.intersection(leaked_indices)
    ).copy()
    df_external_curated_label0_clean = df_external_curated_label0_candidates.drop(
        index=df_external_curated_label0_candidates.index.intersection(leaked_indices)
    ).copy()
else:
    df_synthetic_clean = df_synthetic_candidates.copy()
    df_external_real_label0_clean = df_external_real_label0_candidates.copy()
    df_external_curated_label0_clean = df_external_curated_label0_candidates.copy()

df_synthetic_label0 = df_synthetic_clean[df_synthetic_clean["label"] == 0].copy()
df_synthetic_label1 = df_synthetic_clean[df_synthetic_clean["label"] == 1].copy()
df_external_real_label0_clean = df_external_real_label0_clean[df_external_real_label0_clean["label"] == 0].copy()
df_external_curated_label0_clean = df_external_curated_label0_clean[df_external_curated_label0_clean["label"] == 0].copy()

print_label_info("Synthetic Label 0 sạch", df_synthetic_label0)
print_label_info("Synthetic Label 1 sạch", df_synthetic_label1)
print_label_info("External real Label 0 sạch", df_external_real_label0_clean)
print_label_info("External curated Label 0 sạch", df_external_curated_label0_clean)

# %%
# Cell 8 — Build F3 train dataframe

assert len(df_synthetic_label0) > 0, "Không có synthetic Label 0 sạch."
assert len(df_synthetic_label1) > 0, "Không có synthetic Label 1 sạch."
assert len(df_external_real_label0_clean) > 0, "Không có external_real Label 0 sạch."
assert len(df_external_curated_label0_clean) > 0, "Không có external_curated Label 0 sạch."

synthetic_label0_pool = (
    df_synthetic_label0
    .sample(frac=1.0, random_state=CFG["synthetic_sample_seed"])
    .reset_index(drop=True)
)
synthetic_label1_pool = (
    df_synthetic_label1
    .sample(frac=1.0, random_state=CFG["synthetic_sample_seed"])
    .reset_index(drop=True)
)
external_real_label0_pool = (
    df_external_real_label0_clean
    .sample(frac=1.0, random_state=CFG["synthetic_sample_seed"])
    .reset_index(drop=True)
)
external_curated_label0_pool = (
    df_external_curated_label0_clean
    .sample(frac=1.0, random_state=CFG["synthetic_sample_seed"])
    .reset_index(drop=True)
)

df_train_f3 = (
    pd.concat(
        [
            df_train_real,
            synthetic_label0_pool,
            external_real_label0_pool,
            external_curated_label0_pool,
            synthetic_label1_pool,
        ],
        axis=0,
    )
    .sample(frac=1.0, random_state=CFG["synthetic_sample_seed"])
    .reset_index(drop=True)
)

train_path = os.path.join(CFG["output_dir"], "setup_f3_train.csv")
df_train_f3[["content", "label", "data_origin"]].to_csv(train_path, index=False)

metadata = pd.DataFrame([{
    "variant": CFG["variant_name"],
    "actual_synthetic_label0": len(synthetic_label0_pool),
    "actual_external_real_label0": len(external_real_label0_pool),
    "actual_external_curated_label0": len(external_curated_label0_pool),
    "actual_external_all_label0": len(external_real_label0_pool) + len(external_curated_label0_pool),
    "actual_synthetic_label1": len(synthetic_label1_pool),
    "train_total": len(df_train_f3),
    "train_label0": int((df_train_f3["label"] == 0).sum()),
    "train_label1": int((df_train_f3["label"] == 1).sum()),
    "train_file": train_path,
}])
metadata_path = os.path.join(CFG["output_dir"], "setup_f3_variant_metadata.csv")
metadata.to_csv(metadata_path, index=False)

print_split_info("F3 Train", df_train_f3)
print(f"F3 train file     : {train_path}")
print(f"F3 metadata file  : {metadata_path}")
print("\nData origin trong F3 Train:")
print(df_train_f3["data_origin"].value_counts().to_string())

# %%
# Cell 9 — Tokenization

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
# Cell 10 — Metrics and seed helpers

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

print("Đã đăng ký metrics và seed helper.")

# %%
# Cell 11 — Import Trainer

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
# Cell 12 — Tokenize datasets

if torch.cuda.is_available():
    props = torch.cuda.get_device_properties(0)
    print(f"GPU: {props.name}  |  VRAM: {props.total_memory / 1e9:.1f} GB")
else:
    print("WARNING: Không có GPU — huấn luyện trên CPU sẽ rất chậm.")

print("Đang tokenize F3 train / real val / real test...")
train_ds = make_hf_dataset(df_train_f3)
val_ds = make_hf_dataset(df_val)
test_ds = make_hf_dataset(df_test)
print(f"  F3 train: {len(train_ds)}  real val: {len(val_ds)}  real test: {len(test_ds)}")

# %%
# Cell 13 — Train one seed with incremental save

import gc
import shutil
from sklearn.metrics import confusion_matrix

def _free_gpu():
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.synchronize()

def existing_completed_seeds():
    path = os.path.join(CFG["output_dir"], "setup_f3_per_seed_results.csv")
    if not os.path.exists(path):
        return set()
    old = pd.read_csv(path)
    if "seed" not in old.columns:
        return set()
    return set(old["seed"].astype(int).tolist())

def append_seed_result(result):
    cm = result["confusion_matrix"]
    row = {
        "setup": result["setup"],
        "variant": result["variant"],
        "seed": result["seed"],
        "best_epoch": result["best_epoch"],
        "tn": int(cm[0, 0]),
        "fp": int(cm[0, 1]),
        "fn": int(cm[1, 0]),
        "tp": int(cm[1, 1]),
    }
    for k in ALL_METRICS:
        row[k] = round(result[k], 4)

    path = os.path.join(CFG["output_dir"], "setup_f3_per_seed_results.csv")
    new_df = pd.DataFrame([row])
    if os.path.exists(path):
        old_df = pd.read_csv(path)
        old_df = old_df[old_df["seed"].astype(int) != int(result["seed"])]
        out_df = pd.concat([old_df, new_df], axis=0).sort_values("seed")
    else:
        out_df = new_df
    out_df.to_csv(path, index=False)
    print(f"[SAVE] Per-seed result saved: {path}")

def train_one_seed(seed: int):
    variant_name = CFG["variant_name"]
    print(f"\n{'='*80}")
    print(f"  VARIANT {variant_name} | SEED {seed} — Kaggle F3")
    print(f"{'='*80}")

    set_seed_everything(seed)
    _free_gpu()

    model = AutoModelForSequenceClassification.from_pretrained(
        CFG["model_name"], num_labels=2
    )

    run_dir = os.path.join(CFG["work_dir"], variant_name, f"seed_{seed}")
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

    clean["setup"]            = "F_label0_source_augmentation"
    clean["variant"]          = variant_name
    clean["seed"]             = seed
    clean["confusion_matrix"] = cm
    clean["best_epoch"]       = trainer.state.best_model_checkpoint

    print(f"\n[Variant {variant_name} | Seed {seed}] Kết quả test:")
    for k in ALL_METRICS:
        print(f"  {k:<22}: {clean[k]:.4f}")
    print(f"  confusion_matrix:\n{cm}")

    append_seed_result(clean)

    del trainer, model, test_output
    if os.path.exists(run_dir):
        shutil.rmtree(run_dir, ignore_errors=True)
    _free_gpu()

    return clean

print("Đã định nghĩa train_one_seed + incremental save.")

# %%
# Cell 14 — Run F3 seeds (resume-safe)

completed = existing_completed_seeds()
print(f"Completed seeds found: {sorted(completed)}")

all_results = []
for seed in CFG["seeds"]:
    if seed in completed:
        print(f"[SKIP] Seed {seed} đã có trong setup_f3_per_seed_results.csv")
        continue
    result = train_one_seed(seed)
    all_results.append(result)

print("Training loop finished or current session saved all completed seeds.")

# %%
# Cell 15 — Summarize saved F3 results

per_seed_path = os.path.join(CFG["output_dir"], "setup_f3_per_seed_results.csv")
assert os.path.exists(per_seed_path), "Chưa có setup_f3_per_seed_results.csv"

per_seed_df = pd.read_csv(per_seed_path).sort_values("seed")
print(per_seed_df.to_string(index=False))

summary_rows = []
for metric in ALL_METRICS:
    vals = per_seed_df[metric].astype(float).to_numpy()
    summary_rows.append({
        "setup": "F_label0_source_augmentation",
        "variant": CFG["variant_name"],
        "n_seeds_completed": len(per_seed_df),
        "metric": metric,
        "mean": round(vals.mean(), 4),
        "std": round(vals.std(), 4),
        "is_primary": metric in PRIMARY_METRICS,
        **{f"seed_{int(row.seed)}": round(float(row[metric]), 4)
           for _, row in per_seed_df.iterrows()},
    })

summary_df = pd.DataFrame(summary_rows)
summary_path = os.path.join(CFG["output_dir"], "setup_f3_results.csv")
summary_df.to_csv(summary_path, index=False)

print(f"\nSaved summary: {summary_path}")
print(summary_df.to_string(index=False))

# %%
# Cell 16 — Aggregated confusion matrix

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

labels_cm = ["Label 0 (Legit)", "Label 1 (Smishing)"]

cm_sum = np.array([
    [per_seed_df["tn"].sum(), per_seed_df["fp"].sum()],
    [per_seed_df["fn"].sum(), per_seed_df["tp"].sum()],
], dtype=int)
cm_norm = cm_sum.astype(float) / cm_sum.sum(axis=1, keepdims=True)

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
fig.suptitle(
    f"Setup F3 — {CFG['variant_name']}\n"
    f"Confusion Matrix (aggregated, n={len(per_seed_df)} seeds)",
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

plt.tight_layout()
cm_path = os.path.join(CFG["output_dir"], f"setup_f3_confusion_matrix_{CFG['variant_name']}.png")
plt.savefig(cm_path, dpi=150, bbox_inches="tight")
plt.show()
print(f"Confusion matrix saved: {cm_path}")

# %%
# Cell 17 — Zip output for Kaggle download

import shutil

zip_base = "/kaggle/working/setup_f3_results"
zip_path = shutil.make_archive(zip_base, "zip", CFG["output_dir"])
print(f"Created zip: {zip_path}")


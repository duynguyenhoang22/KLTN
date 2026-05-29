# %% [markdown]
# # Setup G — External Challenge Evaluation (PhoBERT, Kaggle)
#
# **Mục tiêu:** đánh giá khả năng chịu miền `external_real` / `external_curated`
# từ ViLexNorm khi test set mới cũng chứa external.
#
# **Điểm quan trọng:** các setup A-F trước đó chỉ lưu kết quả, không lưu model.
# Vì vậy Setup G chạy lại đúng split/công thức E4 như `G0_E4_champion`, rồi so
# sánh với các mô hình được huấn luyện thêm external.
#
# **Model:** `vinai/phobert-base` + `ViTokenizer`  
# **Seeds:** `[42, 123, 2025]`  
# **Nền tảng:** Kaggle GPU runtime

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

    # Challenge split
    split_seed              = 0,
    train_ratio             = 0.70,
    val_ratio               = 0.15,
    test_ratio              = 0.15,
    synthetic_sample_seed   = 0,

    # Variants
    variants_to_run         = [
        "G0_E4_champion",
        "G1_external_all",
        "G2_external_curated",
        "G3_external_plus_synthetic_label0",
    ],
    variant_components      = {
        # Rerun công thức E4: real challenge train + toàn bộ synthetic Label 1.
        # Không đưa external vào train.
        "G0_E4_champion": {
            "external_real_label0": False,
            "external_curated_label0": False,
            "synthetic_label0": False,
            "synthetic_label1": True,
        },
        "G1_external_all": {
            "external_real_label0": True,
            "external_curated_label0": True,
            "synthetic_label0": False,
            "synthetic_label1": True,
        },
        "G2_external_curated": {
            "external_real_label0": False,
            "external_curated_label0": True,
            "synthetic_label0": False,
            "synthetic_label1": True,
        },
        "G3_external_plus_synthetic_label0": {
            "external_real_label0": True,
            "external_curated_label0": True,
            "synthetic_label0": True,
            "synthetic_label1": True,
        },
    },

    # data_origin mapping
    real_origin_values      = ["real"],
    synthetic_origin_values = ["synthetic", "paraphrased", "synthetic_hard_negative"],
    external_real_origin_values = ["external_real"],
    external_curated_origin_values = ["external_curated"],

    # Kaggle paths
    input_root              = "/kaggle/input",
    output_dir              = "/kaggle/working/setup_g_results",
    work_dir                = "/kaggle/working/tmp_checkpoints_setup_g",
    model_dir               = "/kaggle/working/setup_g_results/models",

    # File names to auto-find under /kaggle/input
    data_file_name          = "vismishds_content_label_origin.csv",
    setup_a_test_file_name  = "setup_a_real_test.csv",

    # Artifact policy
    save_model_artifacts    = True,
    zip_models              = False,
)

import os
os.makedirs(CFG["output_dir"], exist_ok=True)
os.makedirs(CFG["work_dir"], exist_ok=True)
os.makedirs(CFG["model_dir"], exist_ok=True)

print("Loaded CFG")
for key in [
    "model_name", "seeds", "variants_to_run", "split_seed",
    "synthetic_sample_seed", "max_length", "num_epochs",
    "learning_rate", "output_dir", "save_model_artifacts", "zip_models",
]:
    print(f"  {key:<24}: {CFG[key]}")

# %%
# Cell 3 — Locate Kaggle input file
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
# Cell 5 — Split source pools

real_origins = set(CFG["real_origin_values"])
synthetic_origins = set(CFG["synthetic_origin_values"])
external_real_origins = set(CFG["external_real_origin_values"])
external_curated_origins = set(CFG["external_curated_origin_values"])

df_real = df_all[df_all["data_origin"].isin(real_origins)].copy()
df_synthetic_candidates = df_all[df_all["data_origin"].isin(synthetic_origins)].copy()
df_external_real_label0 = df_all[df_all["data_origin"].isin(external_real_origins)].copy()
df_external_curated_label0 = df_all[df_all["data_origin"].isin(external_curated_origins)].copy()

assert len(df_real) > 0, "Không có mẫu real nào sau khi lọc data_origin."
assert len(df_synthetic_candidates) > 0, "Không có mẫu synthetic nào sau khi lọc data_origin."
assert len(df_external_real_label0) > 0, "Không có external_real Label 0."
assert len(df_external_curated_label0) > 0, "Không có external_curated Label 0."
assert set(df_external_real_label0["label"].unique().tolist()) <= {0}, "external_real phải là Label 0."
assert set(df_external_curated_label0["label"].unique().tolist()) <= {0}, "external_curated phải là Label 0."

def print_label_info(name, frame):
    counts = frame["label"].value_counts().sort_index()
    print(f"\n{name}: {len(frame)} mẫu")
    print(f"  Label 0: {counts.get(0, 0)}")
    print(f"  Label 1: {counts.get(1, 0)}")
    if "data_origin" in frame.columns:
        print("  data_origin:")
        print(frame["data_origin"].value_counts().to_string())

print_label_info("Real data", df_real)
print_label_info("Synthetic candidates", df_synthetic_candidates)
print_label_info("External real Label 0", df_external_real_label0)
print_label_info("External curated Label 0", df_external_curated_label0)

# %%
# Cell 6 — Recreate original Setup E real split and build external challenge split
#
# G0_E4_champion phải giữ y nguyên tinh thần Setup E4:
# - Real Train/Val/Test tái tạo từ Real Test đã khóa của Setup A.
# - Train chỉ dùng Real Train cũ + toàn bộ Synthetic Label 1.
# - Validation của G0 là Real Validation cũ.
#
# Challenge Test mới = Real Test cũ + external test split.
# Synthetic chỉ dùng làm train augmentation, không đưa vào Challenge Val/Test.

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
    test_frame["data_origin"] = "real"
    return trainval_pool, test_frame

setup_a_test = pd.read_csv(setup_a_test_path)
setup_a_test["content"] = setup_a_test["content"].astype(str).fillna("")
setup_a_test["label"] = setup_a_test["label"].astype(int)

df_real_trainval_pool, df_real_test_locked = drop_locked_test_from_real(
    df_real,
    setup_a_test[["content", "label"]],
)

val_size_relative = CFG["val_ratio"] / (CFG["train_ratio"] + CFG["val_ratio"])
df_e4_train_real, df_e4_val_real = train_test_split(
    df_real_trainval_pool,
    test_size=val_size_relative,
    stratify=df_real_trainval_pool["label"],
    random_state=CFG["split_seed"],
)

df_external_pool = pd.concat(
    [df_external_real_label0, df_external_curated_label0],
    axis=0,
).sample(frac=1.0, random_state=CFG["split_seed"]).reset_index(drop=True)

df_external_train, df_external_temp = train_test_split(
    df_external_pool,
    test_size=CFG["val_ratio"] + CFG["test_ratio"],
    stratify=df_external_pool["data_origin"],
    random_state=CFG["split_seed"],
)

temp_test_ratio = CFG["test_ratio"] / (CFG["val_ratio"] + CFG["test_ratio"])
df_external_val, df_external_test = train_test_split(
    df_external_temp,
    test_size=temp_test_ratio,
    stratify=df_external_temp["data_origin"],
    random_state=CFG["split_seed"],
)

df_challenge_train = (
    pd.concat([df_e4_train_real, df_external_train], axis=0)
    .sample(frac=1.0, random_state=CFG["split_seed"])
    .reset_index(drop=True)
)
df_challenge_val = (
    pd.concat([df_e4_val_real, df_external_val], axis=0)
    .sample(frac=1.0, random_state=CFG["split_seed"])
    .reset_index(drop=True)
)
df_challenge_test = (
    pd.concat([df_real_test_locked, df_external_test], axis=0)
    .sample(frac=1.0, random_state=CFG["split_seed"])
    .reset_index(drop=True)
)

for frame in [
    df_e4_train_real, df_e4_val_real, df_real_test_locked,
    df_external_train, df_external_val, df_external_test,
]:
    frame.reset_index(drop=True, inplace=True)

def save_split(frame, name):
    path = os.path.join(CFG["output_dir"], f"setup_g_challenge_{name}.csv")
    frame[["content", "label", "data_origin"]].to_csv(path, index=False)
    return path

split_paths = {
    "train": save_split(df_challenge_train, "train"),
    "val": save_split(df_challenge_val, "val"),
    "test": save_split(df_challenge_test, "test"),
    "e4_train_real": save_split(df_e4_train_real, "e4_train_real"),
    "e4_val_real": save_split(df_e4_val_real, "e4_val_real"),
    "e4_test_real_locked": save_split(df_real_test_locked, "e4_test_real_locked"),
    "external_train": save_split(df_external_train, "external_train"),
    "external_val": save_split(df_external_val, "external_val"),
    "external_test": save_split(df_external_test, "external_test"),
}

def split_summary_row(split_name, frame):
    rows = []
    for origin, part in frame.groupby("data_origin"):
        counts = part["label"].value_counts().sort_index()
        rows.append({
            "split": split_name,
            "data_origin": origin,
            "total": len(part),
            "label0": int(counts.get(0, 0)),
            "label1": int(counts.get(1, 0)),
        })
    counts = frame["label"].value_counts().sort_index()
    rows.append({
        "split": split_name,
        "data_origin": "ALL",
        "total": len(frame),
        "label0": int(counts.get(0, 0)),
        "label1": int(counts.get(1, 0)),
    })
    return rows

split_metadata = pd.DataFrame(
    split_summary_row("train", df_challenge_train)
    + split_summary_row("val", df_challenge_val)
    + split_summary_row("test", df_challenge_test)
    + split_summary_row("e4_train_real", df_e4_train_real)
    + split_summary_row("e4_val_real", df_e4_val_real)
    + split_summary_row("e4_test_real_locked", df_real_test_locked)
    + split_summary_row("external_train", df_external_train)
    + split_summary_row("external_val", df_external_val)
    + split_summary_row("external_test", df_external_test)
)
split_metadata_path = os.path.join(CFG["output_dir"], "setup_g_challenge_split_metadata.csv")
split_metadata.to_csv(split_metadata_path, index=False)

print("\nChallenge split paths:")
for name, path in split_paths.items():
    print(f"  {name:<5}: {path}")
print("\nChallenge split metadata:")
print(split_metadata.to_string(index=False))

# %%
# Cell 7 — Leakage check for synthetic augmentation
#
# Để G0 giữ đúng Setup E4, synthetic được lọc theo Real Test cũ giống Setup E.
# Ta vẫn ghi thêm cờ trùng Challenge external Val/Test để biết rủi ro phụ.

import re

def normalize_text_for_leak_check(text):
    text = str(text).lower().strip()
    text = re.sub(r"\s+", " ", text)
    return text

e4_real_test_exact = set(df_real_test_locked["content"].astype(str))
e4_real_test_norm = set(df_real_test_locked["content"].map(normalize_text_for_leak_check))

challenge_external_holdout = pd.concat(
    [df_external_val, df_external_test],
    axis=0,
).copy()
challenge_external_exact = set(challenge_external_holdout["content"].astype(str))
challenge_external_norm = set(
    challenge_external_holdout["content"].map(normalize_text_for_leak_check)
)

leak_rows = []
for idx, row in df_synthetic_candidates.iterrows():
    content = str(row["content"])
    exact_match_e4_real_test = content in e4_real_test_exact
    normalized_match_e4_real_test = normalize_text_for_leak_check(content) in e4_real_test_norm
    exact_match_challenge_external = content in challenge_external_exact
    normalized_match_challenge_external = (
        normalize_text_for_leak_check(content) in challenge_external_norm
    )
    if exact_match_e4_real_test or normalized_match_e4_real_test:
        leak_rows.append({
            "source_index": idx,
            "content": content,
            "label": row["label"],
            "data_origin": row["data_origin"],
            "exact_match_e4_real_test": exact_match_e4_real_test,
            "normalized_match_e4_real_test": normalized_match_e4_real_test,
            "exact_match_challenge_external": exact_match_challenge_external,
            "normalized_match_challenge_external": normalized_match_challenge_external,
        })

leakage_report = pd.DataFrame(leak_rows)
leakage_path = os.path.join(CFG["output_dir"], "setup_g_synthetic_leakage_report.csv")
leakage_report.to_csv(leakage_path, index=False)
print(f"Leakage report đã lưu tại: {leakage_path}")
print(f"Số synthetic candidate trùng Real Test cũ của Setup E: {len(leakage_report)}")

if len(leakage_report) > 0:
    leaked_indices = set(leakage_report["source_index"].tolist())
    df_synthetic_clean = df_synthetic_candidates.drop(
        index=df_synthetic_candidates.index.intersection(leaked_indices)
    ).copy()
else:
    df_synthetic_clean = df_synthetic_candidates.copy()

df_synthetic_label0 = df_synthetic_clean[df_synthetic_clean["label"] == 0].copy()
df_synthetic_label1 = df_synthetic_clean[df_synthetic_clean["label"] == 1].copy()

print_label_info("Synthetic Label 0 sạch", df_synthetic_label0)
print_label_info("Synthetic Label 1 sạch", df_synthetic_label1)

# %%
# Cell 8 — Build train dataframe for each Setup G variant

assert len(df_synthetic_label1) > 0, "Không có synthetic Label 1 sạch."
assert len(df_synthetic_label0) > 0, "Không có synthetic Label 0 sạch."

df_train_real = df_e4_train_real.copy()
df_train_external_real = df_external_train[
    df_external_train["data_origin"].isin(external_real_origins)
].copy()
df_train_external_curated = df_external_train[
    df_external_train["data_origin"].isin(external_curated_origins)
].copy()

assert len(df_train_real) > 0, "Challenge Train không có real."
assert len(df_train_external_real) > 0, "Challenge Train không có external_real."
assert len(df_train_external_curated) > 0, "Challenge Train không có external_curated."

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

variant_train_frames = {}
variant_eval_frames = {}
variant_metadata_rows = []

for variant_name in CFG["variants_to_run"]:
    components = CFG["variant_components"][variant_name]
    parts = [df_train_real.copy()]

    if components["external_real_label0"]:
        parts.append(df_train_external_real.copy())
    if components["external_curated_label0"]:
        parts.append(df_train_external_curated.copy())
    if components["synthetic_label0"]:
        parts.append(synthetic_label0_pool.copy())
    if components["synthetic_label1"]:
        parts.append(synthetic_label1_pool.copy())

    train_frame = (
        pd.concat(parts, axis=0)
        .sample(frac=1.0, random_state=CFG["synthetic_sample_seed"])
        .reset_index(drop=True)
    )
    variant_train_frames[variant_name] = train_frame
    if variant_name == "G0_E4_champion":
        variant_eval_frames[variant_name] = df_e4_val_real.copy()
    else:
        variant_eval_frames[variant_name] = df_challenge_val.copy()

    out_path = os.path.join(CFG["output_dir"], f"setup_g_train_{variant_name}.csv")
    train_frame[["content", "label", "data_origin"]].to_csv(out_path, index=False)

    counts = train_frame["label"].value_counts().sort_index()
    origins = train_frame["data_origin"].value_counts()
    variant_metadata_rows.append({
        "variant": variant_name,
        "uses_external_real_label0": components["external_real_label0"],
        "uses_external_curated_label0": components["external_curated_label0"],
        "uses_synthetic_label0": components["synthetic_label0"],
        "uses_synthetic_label1": components["synthetic_label1"],
        "train_total": len(train_frame),
        "train_label0": int(counts.get(0, 0)),
        "train_label1": int(counts.get(1, 0)),
        "train_real": int(origins.get("real", 0)),
        "train_external_real": int(origins.get("external_real", 0)),
        "train_external_curated": int(origins.get("external_curated", 0)),
        "train_synthetic": int(origins.get("synthetic", 0)),
        "train_paraphrased": int(origins.get("paraphrased", 0)),
        "train_synthetic_hard_negative": int(origins.get("synthetic_hard_negative", 0)),
        "train_file": out_path,
        "validation_frame": "e4_val_real" if variant_name == "G0_E4_champion" else "challenge_val",
    })

    print_label_info(f"Train {variant_name}", train_frame)
    print(f"  Train file: {out_path}")

variant_metadata = pd.DataFrame(variant_metadata_rows)
metadata_path = os.path.join(CFG["output_dir"], "setup_g_variant_metadata.csv")
variant_metadata.to_csv(metadata_path, index=False)
print(f"\nVariant metadata đã lưu tại: {metadata_path}")
print(variant_metadata.to_string(index=False))

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
# Cell 10 — Metrics and helpers

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
SECONDARY_METRICS = ["accuracy", "auroc", "fpr_label0"]
ALL_METRICS       = PRIMARY_METRICS + SECONDARY_METRICS

def binary_metrics_from_logits(labels, logits):
    labels = np.asarray(labels)
    logits = np.asarray(logits)
    probs = softmax(logits, axis=-1)[:, 1]
    preds = logits.argmax(-1)
    cm = confusion_matrix(labels, preds, labels=[0, 1])
    tn, fp, fn, tp = [int(x) for x in cm.ravel()]

    if len(np.unique(labels)) > 1:
        auprc = average_precision_score(labels, probs)
        auroc = roc_auc_score(labels, probs)
    else:
        auprc = np.nan
        auroc = np.nan

    fpr_label0 = fp / (tn + fp) if (tn + fp) > 0 else np.nan

    return {
        "macro_f1": f1_score(labels, preds, average="macro", labels=[0, 1], zero_division=0),
        "f1_label1": f1_score(labels, preds, pos_label=1, average="binary", zero_division=0),
        "recall_label1": recall_score(labels, preds, pos_label=1, zero_division=0),
        "precision_label1": precision_score(labels, preds, pos_label=1, zero_division=0),
        "auprc": auprc,
        "accuracy": accuracy_score(labels, preds),
        "auroc": auroc,
        "fpr_label0": fpr_label0,
        "tn": tn,
        "fp": fp,
        "fn": fn,
        "tp": tp,
    }

def compute_metrics(pred):
    out = binary_metrics_from_logits(pred.label_ids, pred.predictions)
    return {k: out[k] for k in ALL_METRICS}

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

def safe_round(value, ndigits=4):
    if value is None:
        return np.nan
    try:
        if np.isnan(value):
            return np.nan
    except TypeError:
        pass
    return round(float(value), ndigits)

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

print("Đang tokenize Challenge Val/Test...")
test_ds = make_hf_dataset(df_challenge_test)
print(f"  challenge test: {len(test_ds)}")

variant_train_datasets = {}
variant_eval_datasets = {}
for variant_name, train_frame in variant_train_frames.items():
    print(f"\nĐang tokenize train dataset cho {variant_name}...")
    variant_train_datasets[variant_name] = make_hf_dataset(train_frame)
    print(f"  {variant_name} train: {len(variant_train_datasets[variant_name])}")

    print(f"Đang tokenize validation dataset cho {variant_name}...")
    variant_eval_datasets[variant_name] = make_hf_dataset(variant_eval_frames[variant_name])
    print(f"  {variant_name} val: {len(variant_eval_datasets[variant_name])}")

# %%
# Cell 13 — Train one seed with incremental save

import gc
import shutil

def _free_gpu():
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.synchronize()

def per_seed_path():
    return os.path.join(CFG["output_dir"], "setup_g_per_seed_results.csv")

def subset_path():
    return os.path.join(CFG["output_dir"], "setup_g_subset_results.csv")

def existing_completed_runs():
    path = per_seed_path()
    if not os.path.exists(path):
        return set()
    old = pd.read_csv(path)
    if not {"variant", "seed"} <= set(old.columns):
        return set()
    return set(zip(old["variant"].astype(str), old["seed"].astype(int)))

def rows_for_test_subsets(variant_name, seed, logits, labels, test_frame):
    subset_defs = {
        "challenge_all": test_frame.index == test_frame.index,
        "real": test_frame["data_origin"].isin(CFG["real_origin_values"]),
        "external_real": test_frame["data_origin"].isin(CFG["external_real_origin_values"]),
        "external_curated": test_frame["data_origin"].isin(CFG["external_curated_origin_values"]),
        "external_all": (
            test_frame["data_origin"].isin(CFG["external_real_origin_values"])
            | test_frame["data_origin"].isin(CFG["external_curated_origin_values"])
        ),
    }

    rows = []
    for subset_name, mask in subset_defs.items():
        mask_arr = np.asarray(mask)
        subset_labels = labels[mask_arr]
        subset_logits = logits[mask_arr]
        if len(subset_labels) == 0:
            continue
        metrics = binary_metrics_from_logits(subset_labels, subset_logits)
        label_counts = pd.Series(subset_labels).value_counts().sort_index()
        row = {
            "setup": "G_external_challenge",
            "variant": variant_name,
            "seed": seed,
            "subset": subset_name,
            "n": int(len(subset_labels)),
            "label0": int(label_counts.get(0, 0)),
            "label1": int(label_counts.get(1, 0)),
            "tn": metrics["tn"],
            "fp": metrics["fp"],
            "fn": metrics["fn"],
            "tp": metrics["tp"],
        }
        for metric in ALL_METRICS:
            row[metric] = safe_round(metrics[metric])
        rows.append(row)
    return rows

def append_rows(path, key_columns, rows):
    new_df = pd.DataFrame(rows)
    if os.path.exists(path):
        old_df = pd.read_csv(path)
        if len(old_df) > 0:
            for row in rows:
                mask = pd.Series(True, index=old_df.index)
                for col in key_columns:
                    mask &= old_df[col].astype(str) == str(row[col])
                old_df = old_df[~mask]
        out_df = pd.concat([old_df, new_df], axis=0)
    else:
        out_df = new_df
    out_df.to_csv(path, index=False)
    print(f"[SAVE] Saved rows: {path}")

def train_one_variant_seed(variant_name: str, seed: int):
    print(f"\n{'='*88}")
    print(f"  VARIANT {variant_name} | SEED {seed} — Setup G External Challenge")
    print(f"{'='*88}")

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
        train_dataset   = variant_train_datasets[variant_name],
        eval_dataset    = variant_eval_datasets[variant_name],
        compute_metrics = compute_metrics,
        callbacks       = [EarlyStoppingCallback(
                              early_stopping_patience=CFG["early_stop_patience"]
                           )],
    )

    trainer.train()

    if CFG["save_model_artifacts"]:
        model_out_dir = os.path.join(CFG["model_dir"], variant_name, f"seed_{seed}")
        os.makedirs(model_out_dir, exist_ok=True)
        trainer.save_model(model_out_dir)
        tokenizer.save_pretrained(model_out_dir)
        print(f"[SAVE] Best model artifact: {model_out_dir}")

    test_output = trainer.predict(test_ds)
    logits = test_output.predictions
    labels = test_output.label_ids
    metrics = binary_metrics_from_logits(labels, logits)

    per_seed_row = {
        "setup": "G_external_challenge",
        "variant": variant_name,
        "seed": seed,
        "best_epoch": trainer.state.best_model_checkpoint,
        "tn": metrics["tn"],
        "fp": metrics["fp"],
        "fn": metrics["fn"],
        "tp": metrics["tp"],
    }
    for metric in ALL_METRICS:
        per_seed_row[metric] = safe_round(metrics[metric])

    append_rows(per_seed_path(), ["variant", "seed"], [per_seed_row])

    subset_rows = rows_for_test_subsets(
        variant_name, seed, logits, labels, df_challenge_test.reset_index(drop=True)
    )
    append_rows(subset_path(), ["variant", "seed", "subset"], subset_rows)

    print(f"\n[Variant {variant_name} | Seed {seed}] Challenge Test:")
    for metric in ALL_METRICS:
        print(f"  {metric:<22}: {per_seed_row[metric]}")
    print(f"  confusion_matrix:\n[[{metrics['tn']} {metrics['fp']}]\n [{metrics['fn']} {metrics['tp']}]]")

    del trainer, model, test_output
    if os.path.exists(run_dir):
        shutil.rmtree(run_dir, ignore_errors=True)
    _free_gpu()

print("Đã định nghĩa train_one_variant_seed + incremental save.")

# %%
# Cell 14 — Run variants and seeds (resume-safe)

completed = existing_completed_runs()
print(f"Completed runs found: {sorted(completed)}")

for variant_name in CFG["variants_to_run"]:
    for seed in CFG["seeds"]:
        if (variant_name, seed) in completed:
            print(f"[SKIP] {variant_name} | seed {seed} đã có trong setup_g_per_seed_results.csv")
            continue
        train_one_variant_seed(variant_name, seed)

print("Training loop finished or current session saved all completed runs.")

# %%
# Cell 15 — Summarize Setup G results

assert os.path.exists(per_seed_path()), "Chưa có setup_g_per_seed_results.csv"
per_seed_df = pd.read_csv(per_seed_path()).sort_values(["variant", "seed"])
print(per_seed_df.to_string(index=False))

summary_rows = []
for variant_name in CFG["variants_to_run"]:
    variant_df = per_seed_df[per_seed_df["variant"] == variant_name].copy()
    if len(variant_df) == 0:
        continue
    for metric in ALL_METRICS:
        vals = variant_df[metric].astype(float).to_numpy()
        summary_rows.append({
            "setup": "G_external_challenge",
            "variant": variant_name,
            "n_seeds_completed": len(variant_df),
            "metric": metric,
            "mean": safe_round(np.nanmean(vals)),
            "std": safe_round(np.nanstd(vals)),
            "is_primary": metric in PRIMARY_METRICS,
            **{f"seed_{int(row.seed)}": safe_round(row[metric])
               for _, row in variant_df.iterrows()},
        })

summary_df = pd.DataFrame(summary_rows)
summary_path = os.path.join(CFG["output_dir"], "setup_g_results.csv")
summary_df.to_csv(summary_path, index=False)

print(f"\nSaved summary: {summary_path}")
print(summary_df.to_string(index=False))

# %%
# Cell 16 — Summarize subset results

assert os.path.exists(subset_path()), "Chưa có setup_g_subset_results.csv"
subset_df = pd.read_csv(subset_path()).sort_values(["variant", "subset", "seed"])

subset_summary_rows = []
for (variant_name, subset_name), group in subset_df.groupby(["variant", "subset"]):
    for metric in ALL_METRICS:
        vals = group[metric].astype(float).to_numpy()
        subset_summary_rows.append({
            "setup": "G_external_challenge",
            "variant": variant_name,
            "subset": subset_name,
            "n_seeds_completed": len(group),
            "metric": metric,
            "mean": safe_round(np.nanmean(vals)),
            "std": safe_round(np.nanstd(vals)),
            "is_primary": metric in PRIMARY_METRICS or metric == "fpr_label0",
            **{f"seed_{int(row.seed)}": safe_round(row[metric])
               for _, row in group.iterrows()},
        })

subset_summary_df = pd.DataFrame(subset_summary_rows)
subset_summary_path = os.path.join(CFG["output_dir"], "setup_g_subset_summary.csv")
subset_summary_df.to_csv(subset_summary_path, index=False)

print(f"\nSaved subset raw rows: {subset_path()}")
print(f"Saved subset summary : {subset_summary_path}")
print(subset_summary_df.to_string(index=False))

# %%
# Cell 17 — Aggregated confusion matrices

import matplotlib.pyplot as plt
import seaborn as sns

labels_cm = ["Label 0", "Label 1"]

def plot_confusion_matrix_for_rows(rows_df, title, out_path):
    cm_sum = np.array([
        [rows_df["tn"].sum(), rows_df["fp"].sum()],
        [rows_df["fn"].sum(), rows_df["tp"].sum()],
    ], dtype=int)
    with np.errstate(divide="ignore", invalid="ignore"):
        cm_norm = cm_sum.astype(float) / cm_sum.sum(axis=1, keepdims=True)
        cm_norm = np.nan_to_num(cm_norm)

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    fig.suptitle(title, fontsize=12, fontweight="bold")

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
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.show()
    print(f"Confusion matrix saved: {out_path}")

for variant_name in CFG["variants_to_run"]:
    variant_all = per_seed_df[per_seed_df["variant"] == variant_name]
    if len(variant_all) > 0:
        plot_confusion_matrix_for_rows(
            variant_all,
            f"Setup G — {variant_name}\nChallenge Test All",
            os.path.join(CFG["output_dir"], f"setup_g_confusion_matrix_{variant_name}_challenge_all.png"),
        )

    variant_subset = subset_df[subset_df["variant"] == variant_name]
    for subset_name in ["real", "external_all", "external_real", "external_curated"]:
        rows = variant_subset[variant_subset["subset"] == subset_name]
        if len(rows) == 0:
            continue
        plot_confusion_matrix_for_rows(
            rows,
            f"Setup G — {variant_name}\nChallenge Test subset: {subset_name}",
            os.path.join(CFG["output_dir"], f"setup_g_confusion_matrix_{variant_name}_{subset_name}.png"),
        )

# %%
# Cell 18 — Zip output for Kaggle download

import shutil
from pathlib import Path

results_pack_dir = "/kaggle/working/setup_g_results_package"
if os.path.exists(results_pack_dir):
    shutil.rmtree(results_pack_dir)
os.makedirs(results_pack_dir, exist_ok=True)

for item in Path(CFG["output_dir"]).iterdir():
    if item.name == "models":
        continue
    target = Path(results_pack_dir) / item.name
    if item.is_dir():
        shutil.copytree(item, target)
    else:
        shutil.copy2(item, target)

zip_base = "/kaggle/working/setup_g_results"
zip_path = shutil.make_archive(zip_base, "zip", results_pack_dir)
print(f"Created results zip without models: {zip_path}")

if CFG["zip_models"]:
    model_zip_base = "/kaggle/working/setup_g_models"
    model_zip_path = shutil.make_archive(model_zip_base, "zip", CFG["model_dir"])
    print(f"Created model zip: {model_zip_path}")
else:
    print("Model artifacts remain in setup_g_results/models but are not included in the results zip.")

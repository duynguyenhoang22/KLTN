# %% [markdown]
# # Fine-tune BARTpho for Vietnamese SMS normalization
#
# Colab workflow for `phase2_full_normalization_content_only.csv`.
#
# This notebook-style script trains two variants:
#
# - `vinai/bartpho-syllable`: apply tone normalization only.
# - `vinai/bartpho-word`: apply tone normalization, then VNCoreNLP word segmentation.
#
# In Colab, upload the CSV to `/content`, or mount Google Drive and update
# `DATA_PATH` below.

# %% [markdown]
# ## 1. Install dependencies
#
# Colab normally has Internet access, so install Python dependencies. The
# `py_vncorenlp` wrapper downloads VNCoreNLP assets in the segmentation cell.

# %%
INSTALL_DEPENDENCIES = True

if INSTALL_DEPENDENCIES:
    import subprocess as _subprocess
    import sys as _sys

    _subprocess.check_call(
        [
            _sys.executable,
            "-m",
            "pip",
            "install",
            "-q",
            "-U",
            "transformers",
            "datasets",
            "accelerate",
            "evaluate",
            "sacrebleu",
            "rouge-score",
            "jiwer",
            "sentencepiece",
            "py_vncorenlp",
        ]
    )
else:
    print("Skipping pip install.")

DOWNLOAD_VNCORENLP = True
VNCORENLP_DIR = "/content/vncorenlp"

# %% [markdown]
# ## 2. Imports and configuration

# %%
import gc
import inspect
import os
import random
import re

import evaluate
import numpy as np
import pandas as pd
import torch
from datasets import Dataset, DatasetDict
from sklearn.model_selection import train_test_split
from transformers import (
    AutoModelForSeq2SeqLM,
    AutoTokenizer,
    DataCollatorForSeq2Seq,
    Seq2SeqTrainer,
    Seq2SeqTrainingArguments,
    set_seed,
)

DATA_PATH = "/content/phase2_full_normalization_content_only.csv"
OUTPUT_ROOT = "/content/bartpho-normalization"

BARTPHO_SYLLABLE_MODEL = "vinai/bartpho-syllable"
BARTPHO_WORD_MODEL = "vinai/bartpho-word"

SOURCE_COL = "source_text"
TARGET_COL = "normalized_text"
ID_COL = "norm_id"

SEED = 42
MAX_SOURCE_LENGTH = 128
MAX_TARGET_LENGTH = 128
TRAIN_SIZE = 0.90
VAL_SIZE_FROM_TEMP = 0.50

NUM_EPOCHS = 5
LEARNING_RATE = 2e-5
WEIGHT_DECAY = 0.01
PER_DEVICE_TRAIN_BATCH_SIZE = 8
PER_DEVICE_EVAL_BATCH_SIZE = 8
GRADIENT_ACCUMULATION_STEPS = 2
GENERATION_NUM_BEAMS = 4

MODEL_CONFIGS = {
    "syllable": {
        "model_name": BARTPHO_SYLLABLE_MODEL,
        "needs_word_segmentation": False,
    },
    "word": {
        "model_name": BARTPHO_WORD_MODEL,
        "needs_word_segmentation": True,
    },
}

os.makedirs(OUTPUT_ROOT, exist_ok=True)
set_seed(SEED)
random.seed(SEED)
np.random.seed(SEED)

# %% [markdown]
# ## 3. Tone normalization
#
# BARTpho authors recommend this before fine-tuning. Apply it to both source and target text.

# %%
DICT_MAP = {
    "òa": "oà",
    "Òa": "Oà",
    "ÒA": "OÀ",
    "óa": "oá",
    "Óa": "Oá",
    "ÓA": "OÁ",
    "ỏa": "oả",
    "Ỏa": "Oả",
    "ỎA": "OẢ",
    "õa": "oã",
    "Õa": "Oã",
    "ÕA": "OÃ",
    "ọa": "oạ",
    "Ọa": "Oạ",
    "ỌA": "OẠ",
    "òe": "oè",
    "Òe": "Oè",
    "ÒE": "OÈ",
    "óe": "oé",
    "Óe": "Oé",
    "ÓE": "OÉ",
    "ỏe": "oẻ",
    "Ỏe": "Oẻ",
    "ỎE": "OẺ",
    "õe": "oẽ",
    "Õe": "Oẽ",
    "ÕE": "OẼ",
    "ọe": "oẹ",
    "Ọe": "Oẹ",
    "ỌE": "OẸ",
    "ùy": "uỳ",
    "Ùy": "Uỳ",
    "ÙY": "UỲ",
    "úy": "uý",
    "Úy": "Uý",
    "ÚY": "UÝ",
    "ủy": "uỷ",
    "Ủy": "Uỷ",
    "ỦY": "UỶ",
    "ũy": "uỹ",
    "Ũy": "Uỹ",
    "ŨY": "UỸ",
    "ụy": "uỵ",
    "Ụy": "Uỵ",
    "ỤY": "UỴ",
}


def replace_all(text, dict_map=DICT_MAP):
    text = str(text)
    for old, new in dict_map.items():
        text = text.replace(old, new)
    return text


def clean_spaces(text):
    return re.sub(r"\s+", " ", str(text)).strip()


def tone_normalize(text):
    return clean_spaces(replace_all(text))

# %% [markdown]
# ## 4. Optional VNCoreNLP word segmentation
#
# Use this only for `vinai/bartpho-word`. The syllable model must keep regular whitespace-separated syllables.
# The word variant uses VNCoreNLP, matching the BARTpho authors' recommendation.

# %%
_RDRSEGMENTER = None


def get_word_segmenter():
    global _RDRSEGMENTER
    if _RDRSEGMENTER is None:
        import os
        import py_vncorenlp

        if DOWNLOAD_VNCORENLP or not os.path.isdir(os.path.join(VNCORENLP_DIR, "models")):
            py_vncorenlp.download_model(save_dir=VNCORENLP_DIR)
        _RDRSEGMENTER = py_vncorenlp.VnCoreNLP(
            annotators=["wseg"],
            save_dir=VNCORENLP_DIR,
        )
    return _RDRSEGMENTER


def segment_vietnamese_text(text):
    segmented_sentences = get_word_segmenter().word_segment(str(text))
    return " ".join(segmented_sentences)


def word_segment_text(text):
    return clean_spaces(segment_vietnamese_text(str(text)))

# %% [markdown]
# ## 5. Load, clean, split

# %%
df = pd.read_csv(DATA_PATH)
df = df[[ID_COL, SOURCE_COL, TARGET_COL]].copy()

missing_counts = df[[SOURCE_COL, TARGET_COL]].isna().sum()
if missing_counts.any():
    raise ValueError(f"Missing source/target values: {missing_counts.to_dict()}")

df[SOURCE_COL] = df[SOURCE_COL].map(tone_normalize)
df[TARGET_COL] = df[TARGET_COL].map(tone_normalize)

empty_counts = (df[[SOURCE_COL, TARGET_COL]] == "").sum()
if empty_counts.any():
    raise ValueError(f"Empty source/target values after cleaning: {empty_counts.to_dict()}")

duplicate_count = df.duplicated(subset=[SOURCE_COL, TARGET_COL]).sum()
if duplicate_count:
    print(f"Dropping {duplicate_count} duplicate source-target pairs after tone normalization")
    df = df.drop_duplicates(subset=[SOURCE_COL, TARGET_COL]).reset_index(drop=True)

df.to_csv(f"{OUTPUT_ROOT}/tone_normalized_full.csv", index=False)

train_df, temp_df = train_test_split(
    df,
    train_size=TRAIN_SIZE,
    random_state=SEED,
    shuffle=True,
)
val_df, test_df = train_test_split(
    temp_df,
    train_size=VAL_SIZE_FROM_TEMP,
    random_state=SEED,
    shuffle=True,
)

print("Rows:", {"train": len(train_df), "validation": len(val_df), "test": len(test_df)})
print(train_df[[SOURCE_COL, TARGET_COL]].head(3).to_string(index=False))

train_df.to_csv(f"{OUTPUT_ROOT}/train.csv", index=False)
val_df.to_csv(f"{OUTPUT_ROOT}/validation.csv", index=False)
test_df.to_csv(f"{OUTPUT_ROOT}/test.csv", index=False)

# %% [markdown]
# ## 6. Preprocessing helpers

# %%
def prepare_text_frames(train_df, val_df, test_df, needs_word_segmentation):
    frames = {
        "train": train_df.copy(),
        "validation": val_df.copy(),
        "test": test_df.copy(),
    }

    if needs_word_segmentation:
        for split_name, frame in frames.items():
            frame[SOURCE_COL] = frame[SOURCE_COL].map(word_segment_text)
            frame[TARGET_COL] = frame[TARGET_COL].map(word_segment_text)
            print(f"Word-segmented {split_name}: {len(frame)} rows")

    return DatasetDict({name: Dataset.from_pandas(frame.reset_index(drop=True)) for name, frame in frames.items()})


def tokenize_dataset(dataset_dict, tokenizer):
    def preprocess(batch):
        model_inputs = tokenizer(
            batch[SOURCE_COL],
            max_length=MAX_SOURCE_LENGTH,
            truncation=True,
        )
        labels = tokenizer(
            text_target=batch[TARGET_COL],
            max_length=MAX_TARGET_LENGTH,
            truncation=True,
        )
        model_inputs["labels"] = labels["input_ids"]
        return model_inputs

    return dataset_dict.map(
        preprocess,
        batched=True,
        remove_columns=dataset_dict["train"].column_names,
    )

# %% [markdown]
# ## 7. Metrics
#
# BLEU/ROUGE are useful sanity checks. Exact match is stricter and often more meaningful for normalization.

# %%
sacrebleu = evaluate.load("sacrebleu")
rouge = evaluate.load("rouge")
wer_metric = evaluate.load("wer")


def normalize_for_metric(text, desegment=False):
    text = clean_spaces(text)
    return text.replace("_", " ") if desegment else text


def make_compute_metrics(tokenizer, desegment=False):
    def compute_metrics(eval_pred):
        predictions, labels = eval_pred
        if isinstance(predictions, tuple):
            predictions = predictions[0]

        predictions = np.where(predictions != -100, predictions, tokenizer.pad_token_id)
        labels = np.where(labels != -100, labels, tokenizer.pad_token_id)
        decoded_predictions = tokenizer.batch_decode(predictions, skip_special_tokens=True)
        decoded_labels = tokenizer.batch_decode(labels, skip_special_tokens=True)

        decoded_predictions = [
            normalize_for_metric(text, desegment=desegment) for text in decoded_predictions
        ]
        decoded_labels = [normalize_for_metric(text, desegment=desegment) for text in decoded_labels]

        exact_match = np.mean(
            [pred == label for pred, label in zip(decoded_predictions, decoded_labels)]
        )
        bleu = sacrebleu.compute(
            predictions=decoded_predictions,
            references=[[label] for label in decoded_labels],
        )["score"]
        rouge_scores = rouge.compute(
            predictions=decoded_predictions,
            references=decoded_labels,
            use_stemmer=False,
        )
        wer = wer_metric.compute(predictions=decoded_predictions, references=decoded_labels)

        return {
            "exact_match": round(float(exact_match), 4),
            "bleu": round(float(bleu), 4),
            "rougeL": round(float(rouge_scores["rougeL"]), 4),
            "wer": round(float(wer), 4),
        }

    return compute_metrics


def build_training_args(output_dir):
    common_kwargs = dict(
        output_dir=output_dir,
        save_strategy="epoch",
        learning_rate=LEARNING_RATE,
        per_device_train_batch_size=PER_DEVICE_TRAIN_BATCH_SIZE,
        per_device_eval_batch_size=PER_DEVICE_EVAL_BATCH_SIZE,
        gradient_accumulation_steps=GRADIENT_ACCUMULATION_STEPS,
        weight_decay=WEIGHT_DECAY,
        num_train_epochs=NUM_EPOCHS,
        predict_with_generate=True,
        generation_max_length=MAX_TARGET_LENGTH,
        generation_num_beams=GENERATION_NUM_BEAMS,
        fp16=torch.cuda.is_available(),
        logging_steps=50,
        save_total_limit=2,
        load_best_model_at_end=True,
        metric_for_best_model="exact_match",
        greater_is_better=True,
        report_to="none",
        seed=SEED,
    )

    try:
        return Seq2SeqTrainingArguments(evaluation_strategy="epoch", **common_kwargs)
    except TypeError:
        return Seq2SeqTrainingArguments(eval_strategy="epoch", **common_kwargs)


def build_seq2seq_trainer(
    model,
    training_args,
    tokenizer,
    tokenized,
    data_collator,
    compute_metrics,
):
    trainer_kwargs = dict(
        model=model,
        args=training_args,
        train_dataset=tokenized["train"],
        eval_dataset=tokenized["validation"],
        data_collator=data_collator,
        compute_metrics=compute_metrics,
    )

    trainer_signature = inspect.signature(Seq2SeqTrainer.__init__)
    if "processing_class" in trainer_signature.parameters:
        trainer_kwargs["processing_class"] = tokenizer
    elif "tokenizer" in trainer_signature.parameters:
        trainer_kwargs["tokenizer"] = tokenizer

    return Seq2SeqTrainer(**trainer_kwargs)

# %% [markdown]
# ## 8. Train one BARTpho variant

# %%
def train_variant(variant_name):
    config = MODEL_CONFIGS[variant_name]
    model_name = config["model_name"]
    output_dir = f"{OUTPUT_ROOT}/{variant_name}"

    print(f"Training {variant_name}: {model_name}")
    dataset_dict = prepare_text_frames(
        train_df,
        val_df,
        test_df,
        needs_word_segmentation=config["needs_word_segmentation"],
    )

    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    tokenized = tokenize_dataset(dataset_dict, tokenizer)

    data_collator = DataCollatorForSeq2Seq(
        tokenizer=tokenizer,
        model=model,
        label_pad_token_id=-100,
    )

    training_args = build_training_args(output_dir)

    trainer = build_seq2seq_trainer(
        model=model,
        training_args=training_args,
        tokenizer=tokenizer,
        tokenized=tokenized,
        data_collator=data_collator,
        compute_metrics=make_compute_metrics(
            tokenizer,
            desegment=config["needs_word_segmentation"],
        ),
    )

    trainer.train()
    validation_metrics = trainer.evaluate(tokenized["validation"], metric_key_prefix="validation")
    test_metrics = trainer.evaluate(tokenized["test"], metric_key_prefix="test")

    trainer.save_model(f"{output_dir}/best")
    tokenizer.save_pretrained(f"{output_dir}/best")

    print("Validation metrics:", validation_metrics)
    print("Test metrics:", test_metrics)
    return validation_metrics, test_metrics

# %% [markdown]
# ## 9. Run training
#
# Start with one variant if your Colab GPU memory/runtime is tight. Then run the other variant in a fresh session.

# %%
RUN_VARIANTS = ["syllable"]

results = {}
for variant_name in RUN_VARIANTS:
    validation_metrics, test_metrics = train_variant(variant_name)
    results[variant_name] = {
        "validation": validation_metrics,
        "test": test_metrics,
    }

    gc.collect()
    torch.cuda.empty_cache()

# %% [markdown]
# ## 10. Inference helper
#
# For `bartpho-word`, raw input must be tone-normalized and word-segmented before generation.

# %%
def load_variant_for_inference(variant_name):
    config = MODEL_CONFIGS[variant_name]
    model_dir = f"{OUTPUT_ROOT}/{variant_name}/best"
    if not os.path.isdir(model_dir):
        raise FileNotFoundError(
            f"Missing trained checkpoint: {model_dir}. "
            f"Train this variant first with RUN_VARIANTS = ['{variant_name}'], "
            "or load an existing checkpoint by updating OUTPUT_ROOT."
        )

    tokenizer = AutoTokenizer.from_pretrained(model_dir, use_fast=False)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_dir)
    model.eval()
    if torch.cuda.is_available():
        model.cuda()

    needs_word_segmentation = config["needs_word_segmentation"]
    if needs_word_segmentation:
        get_word_segmenter()
    return model, tokenizer, needs_word_segmentation


def generate_normalization(text, model, tokenizer, needs_word_segmentation=False):
    text = tone_normalize(text)
    if needs_word_segmentation:
        text = word_segment_text(text)

    inputs = tokenizer(
        [text],
        max_length=MAX_SOURCE_LENGTH,
        truncation=True,
        return_tensors="pt",
    )
    if torch.cuda.is_available():
        inputs = {key: value.cuda() for key, value in inputs.items()}

    with torch.no_grad():
        generated_ids = model.generate(
            **inputs,
            max_length=MAX_TARGET_LENGTH,
            num_beams=GENERATION_NUM_BEAMS,
    )
    prediction = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return prediction.replace("_", " ") if needs_word_segmentation else prediction


sample_text = "Linh oi anh Tuan ne, hom nay vo tinh gap c Mai nen xjn dc so e"
sample_model, sample_tokenizer, sample_needs_word_segmentation = load_variant_for_inference("syllable")
print(generate_normalization(sample_text, sample_model, sample_tokenizer, sample_needs_word_segmentation))

# %% [markdown]
# ## 11. Save predictions for error analysis

# %%
def save_test_predictions(variant_name, limit=None):
    model, tokenizer, needs_word_segmentation = load_variant_for_inference(variant_name)
    frame = test_df.copy()
    if limit is not None:
        frame = frame.head(limit).copy()
    frame["prediction"] = frame[SOURCE_COL].map(
        lambda text: generate_normalization(text, model, tokenizer, needs_word_segmentation)
    )
    output_path = f"{OUTPUT_ROOT}/{variant_name}_test_predictions.csv"
    frame[[ID_COL, SOURCE_COL, TARGET_COL, "prediction"]].to_csv(output_path, index=False)
    print(output_path)
    return frame


# Example:
# syllable_predictions = save_test_predictions("syllable")
# word_predictions = save_test_predictions("word")

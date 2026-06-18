"""Shared configuration for the ViSmishDS model benchmark."""

from __future__ import annotations

from dataclasses import dataclass


PRIMARY_METRICS = ["macro_f1", "f1_label_1", "recall_label_1", "pr_auc"]

BENCHMARK_SPLITS = {
    "train": "train.csv",
    "dev": "dev.csv",
    "test": "test.csv",
}

REAL_HOLDOUT_ORIGINS = {"real", "external_real", "external_curated"}
TRAIN_ONLY_ORIGINS = {"synthetic", "paraphrased", "synthetic_hard_positive"}
SUPPORTED_ORIGINS = REAL_HOLDOUT_ORIGINS | TRAIN_ONLY_ORIGINS


@dataclass(frozen=True)
class PlmSpec:
    key: str
    display_name: str
    hf_model: str | None
    needs_vietnamese_word_segmentation: bool = False
    default_train_batch_size: int = 16
    default_eval_batch_size: int = 32
    default_gradient_accumulation_steps: int = 1
    include_in_benchmark_suite: bool = True


PLM_REGISTRY: dict[str, PlmSpec] = {
    "phobert-base": PlmSpec(
        key="phobert-base",
        display_name="PhoBERT-base",
        hf_model="vinai/phobert-base",
        needs_vietnamese_word_segmentation=True,
    ),
    "phobert-large": PlmSpec(
        key="phobert-large",
        display_name="PhoBERT-large",
        hf_model="vinai/phobert-large",
        needs_vietnamese_word_segmentation=True,
    ),
    "mbert": PlmSpec(
        key="mbert",
        display_name="mBERT",
        hf_model="bert-base-multilingual-cased",
    ),
    "visobert": PlmSpec(
        key="visobert",
        display_name="VisoBERT",
        hf_model="uitnlp/visobert",
    ),
    "cafebert": PlmSpec(
        key="cafebert",
        display_name="CafeBERT",
        hf_model="uitnlp/CafeBERT",
    ),
    "distilbert": PlmSpec(
        key="distilbert",
        display_name="DistilBERT multilingual",
        hf_model="distilbert-base-multilingual-cased",
        include_in_benchmark_suite=False,
    ),
    "distilledbert": PlmSpec(
        key="distilledbert",
        display_name="DistilBERT multilingual",
        hf_model="distilbert-base-multilingual-cased",
    ),
    "xlm-roberta-base": PlmSpec(
        key="xlm-roberta-base",
        display_name="XLM-RoBERTa-base",
        hf_model="xlm-roberta-base",
    ),
    "xlm-roberta-large": PlmSpec(
        key="xlm-roberta-large",
        display_name="XLM-RoBERTa-large",
        hf_model="xlm-roberta-large",
        default_train_batch_size=8,
        default_eval_batch_size=16,
        default_gradient_accumulation_steps=2,
    ),
    "viclsr": PlmSpec(
        key="viclsr",
        display_name="ViCLSR",
        hf_model="huynhtin/ViCLSR",
        default_train_batch_size=8,
        default_eval_batch_size=16,
        default_gradient_accumulation_steps=2,
    ),
}


CHAR_MODELS = {
    "bilstm_hard": "BiLSTM",
    "bilstm_distilled_phobert_base": "BiLSTM distilled fr PhoBERT-base",
    "textcnn_hard": "TextCNN",
    "textcnn_distilled_phobert_base": "TextCNN distilled fr PhoBERT-base",
}

# Distillation Benchmark

This benchmark replaces the previous narrow distillation setup with two model groups.

## Model Groups

Neural char-level models:

- BiLSTM
- BiLSTM distilled fr PhoBERT-base
- TextCNN
- TextCNN distilled fr PhoBERT-base

Fine-tuned PLMs:

- PhoBERT-base
- PhoBERT-large
- mBERT
- VisoBERT
- CafeBERT
- DistilledBERT/DistilBERT multilingual
- XLM-RoBERTa-base
- XLM-RoBERTa-large
- ViCLSR

## Split Policy

Source file: `model/base/temp.csv`

- `real`, `external_real`, `external_curated`: stratified 70/15/15 into `train`, `dev`, `test`.
- `synthetic`, `paraphrased`, `synthetic_hard_positive`: 100% into `train`.
- Stratification key: `label x data_origin x category`.

Create splits:

```powershell
python scripts/distillation/create_benchmark_splits.py
```

Outputs:

- `data/distillation/benchmark_splits/train.csv`
- `data/distillation/benchmark_splits/dev.csv`
- `data/distillation/benchmark_splits/test.csv`
- `setup_results/distillation_benchmark/split_report.md`

## Primary Metrics

The benchmark reports dev and test results. The four primary metrics are:

- `macro_f1`: balanced headline metric across both classes.
- `f1_label_1`: smishing-class F1.
- `recall_label_1`: prioritizes avoiding missed smishing messages.
- `pr_auc`: threshold-independent metric suitable for imbalanced binary detection.

Confusion matrix counts (`tn`, `fp`, `fn`, `tp`) are also saved for error analysis.

## Run Order

Train PLMs:

```powershell
python scripts/distillation/train_benchmark_plm.py --model-key phobert-base
python scripts/distillation/train_benchmark_plm.py --model-key phobert-large
python scripts/distillation/train_benchmark_plm.py --model-key mbert
python scripts/distillation/train_benchmark_plm.py --model-key visobert
python scripts/distillation/train_benchmark_plm.py --model-key cafebert
python scripts/distillation/train_benchmark_plm.py --model-key distilledbert
python scripts/distillation/train_benchmark_plm.py --model-key xlm-roberta-base
python scripts/distillation/train_benchmark_plm.py --model-key xlm-roberta-large
python scripts/distillation/train_benchmark_plm.py --model-key viclsr
```

Or run the PLM sweep:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/distillation/run_benchmark_plms.ps1
```

ViCLSR uses the public Hugging Face model `huynhtin/ViCLSR`.

Train CafeBERT or ViCLSR as a distillation teacher on Kaggle and generate
`train/dev/test_teacher.csv` in the same run:

```text
scripts/distillation/kaggle_train_cafebert_teacher.py
scripts/distillation/kaggle_train_viclsr_teacher.py
```

Complete Kaggle input, commands, artifact layout, and local integration:

```text
docs/kaggle_cafebert_viclsr_teacher_guide.md
```

Generate PhoBERT-base teacher outputs after the PhoBERT-base PLM run:

```powershell
python scripts/distillation/generate_benchmark_teacher_outputs.py
```

Train char-level models:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/distillation/run_benchmark_char_models.ps1
```

Aggregate all benchmark results:

```powershell
python scripts/distillation/aggregate_benchmark_results.py
```

Final summary:

- `setup_results/distillation_benchmark/summary/benchmark_metrics_long.csv`
- `setup_results/distillation_benchmark/summary/benchmark_metrics_dev_test_wide.csv`
- `setup_results/distillation_benchmark/summary/benchmark_report.md`

## Focused TextCNN Distillation Study

BiLSTM hard-label and distilled remain in the full benchmark. The focused
distillation analysis fixes the student architecture to TextCNN and compares
three supervision modes over seeds 42, 123, and 2025:

- hard labels;
- vanilla KD;
- risk-aware KD.

Run:

```powershell
python scripts/distillation/run_textcnn_distillation_study.py
```

Protocol and interpretation:

- `docs/textcnn_distillation_study_protocol.md`
- `docs/textcnn_distillation_study_results.md`

# Model Benchmark Summary

## Primary Metrics

- `macro_f1`: main balanced quality measure across both labels.
- `f1_label_1`: smishing-class F1.
- `recall_label_1`: missed-smishing control metric.
- `pr_auc`: threshold-independent ranking metric for imbalanced binary detection.

## Dev/Test Results

| model_group    | model_name                        | split   |   rows |   macro_f1 |   f1_label_1 |   recall_label_1 |   pr_auc |
|:---------------|:----------------------------------|:--------|-------:|-----------:|-------------:|-----------------:|---------:|
| char_neural    | BiLSTM                            | dev     |    535 |     0.8984 |       0.8108 |           0.8108 |   0.8378 |
| char_neural    | BiLSTM                            | test    |    535 |     0.8471 |       0.7143 |           0.6757 |   0.7925 |
| char_neural    | BiLSTM distilled fr PhoBERT-base  | dev     |    535 |     0.8839 |       0.7838 |           0.7838 |   0.8241 |
| char_neural    | BiLSTM distilled fr PhoBERT-base  | test    |    535 |     0.8671 |       0.7532 |           0.7838 |   0.7273 |
| char_neural    | TextCNN                           | dev     |    535 |     0.917  |       0.8451 |           0.8108 |   0.8529 |
| char_neural    | TextCNN                           | test    |    535 |     0.9129 |       0.8378 |           0.8378 |   0.8852 |
| char_neural    | TextCNN distilled fr PhoBERT-base | dev     |    535 |     0.9129 |       0.8378 |           0.8378 |   0.8818 |
| char_neural    | TextCNN distilled fr PhoBERT-base | test    |    535 |     0.9189 |       0.85   |           0.9189 |   0.8776 |
| fine_tuned_llm | Gemma 2B                          | dev     |    535 |     0.9553 |       0.9167 |           0.8919 |   0.8965 |
| fine_tuned_llm | Gemma 2B                          | test    |    535 |     0.9585 |       0.9231 |           0.973  |   0.9853 |
| fine_tuned_llm | Gemma 3 1B                        | dev     |    535 |     0.9389 |       0.8857 |           0.8378 |   0.9405 |
| fine_tuned_llm | Gemma 3 1B                        | test    |    535 |     0.9472 |       0.9014 |           0.8649 |   0.9183 |
| fine_tuned_llm | Qwen2.5 0.5B                      | dev     |    535 |     0.9433 |       0.8947 |           0.9189 |   0.9648 |
| fine_tuned_llm | Qwen2.5 0.5B                      | test    |    535 |     0.9248 |       0.8608 |           0.9189 |   0.9489 |
| fine_tuned_llm | Qwen3 0.6B                        | dev     |    535 |     0.9236 |       0.8571 |           0.8108 |   0.9262 |
| fine_tuned_llm | Qwen3 0.6B                        | test    |    535 |     0.9485 |       0.9041 |           0.8919 |   0.9688 |
| fine_tuned_plm | CafeBERT                          | dev     |    535 |     0.9472 |       0.9014 |           0.8649 |   0.9477 |
| fine_tuned_plm | CafeBERT                          | test    |    535 |     0.9355 |       0.88   |           0.8919 |   0.9261 |
| fine_tuned_plm | DistilBERT multilingual           | dev     |    535 |     0.9385 |       0.8861 |           0.9459 |   0.8959 |
| fine_tuned_plm | DistilBERT multilingual           | test    |    535 |     0.915  |       0.8421 |           0.8649 |   0.8421 |
| fine_tuned_plm | PhoBERT-base                      | dev     |    535 |     0.875  |       0.7671 |           0.7568 |   0.8439 |
| fine_tuned_plm | PhoBERT-base                      | test    |    535 |     0.9068 |       0.8267 |           0.8378 |   0.9191 |
| fine_tuned_plm | PhoBERT-large                     | dev     |    535 |     0.8975 |       0.8101 |           0.8649 |   0.8648 |
| fine_tuned_plm | PhoBERT-large                     | test    |    535 |     0.937  |       0.8831 |           0.9189 |   0.9248 |
| fine_tuned_plm | ViCLSR                            | dev     |    535 |     0.9419 |       0.8919 |           0.8919 |   0.9441 |
| fine_tuned_plm | ViCLSR                            | test    |    535 |     0.9447 |       0.8974 |           0.9459 |   0.9457 |
| fine_tuned_plm | VisoBERT                          | dev     |    535 |     0.8958 |       0.8056 |           0.7838 |   0.8866 |
| fine_tuned_plm | VisoBERT                          | test    |    535 |     0.9009 |       0.8158 |           0.8378 |   0.8442 |
| fine_tuned_plm | XLM-RoBERTa-base                  | dev     |    535 |     0.909  |       0.8312 |           0.8649 |   0.9212 |
| fine_tuned_plm | XLM-RoBERTa-base                  | test    |    535 |     0.915  |       0.8421 |           0.8649 |   0.8701 |
| fine_tuned_plm | XLM-RoBERTa-large                 | dev     |    535 |     0.9211 |       0.8533 |           0.8649 |   0.9294 |
| fine_tuned_plm | XLM-RoBERTa-large                 | test    |    535 |     0.9419 |       0.8919 |           0.8919 |   0.9259 |
| fine_tuned_plm | mBERT                             | dev     |    535 |     0.9338 |       0.8767 |           0.8649 |   0.8745 |
| fine_tuned_plm | mBERT                             | test    |    535 |     0.909  |       0.8312 |           0.8649 |   0.9198 |

## Configured PLMs Without Metrics Yet

- None

## Configured LLMs Without Metrics Yet

- None

## Output Files

- Long table: `setup_results/distillation_benchmark/summary/benchmark_metrics_long.csv`
- Dev/test wide table: `setup_results/distillation_benchmark/summary/benchmark_metrics_dev_test_wide.csv`

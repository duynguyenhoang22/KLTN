# g2_bilstm_distilled Report

## 1. Scope

- Architecture: `bilstm`
- Mode: `distilled`
- Setup: `G2_external_curated` robustness check
- Input features: `content` only

## 2. Metrics by Split

| split | rows | accuracy | macro_f1 | f1_label_1 | recall_label_1 | precision_label_1 | roc_auc | pr_auc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| train | 7142 | 0.9857 | 0.9824 | 0.9900 | 0.9814 | 0.9988 | 0.9995 | 0.9998 |
| val | 535 | 0.9607 | 0.8416 | 0.7042 | 0.6757 | 0.7353 | 0.9510 | 0.7626 |
| test_challenge | 537 | 0.9590 | 0.8172 | 0.6562 | 0.5676 | 0.7778 | 0.9557 | 0.7454 |

## 3. Comparison with Hard Baseline

| split | macro_f1_hard | macro_f1_distilled | delta_macro_f1 | f1_label_1_hard | f1_label_1_distilled | delta_f1_label_1 | recall_label_1_hard | recall_label_1_distilled | delta_recall_label_1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| train | 0.9856 | 0.9824 | -0.0032 | 0.9919 | 0.9900 | -0.0019 | 0.9853 | 0.9814 | -0.0039 |
| val | 0.8341 | 0.8416 | 0.0075 | 0.6923 | 0.7042 | 0.0119 | 0.7297 | 0.6757 | -0.0541 |
| test_challenge | 0.8398 | 0.8172 | -0.0226 | 0.6984 | 0.6562 | -0.0422 | 0.5946 | 0.5676 | -0.0270 |

## 4. Confusion Matrices

### train

| | pred_0 | pred_1 |
|---|---:|---:|
| true_0 | 1968 | 6 |
| true_1 | 96 | 5072 |

### val

| | pred_0 | pred_1 |
|---|---:|---:|
| true_0 | 489 | 9 |
| true_1 | 12 | 25 |

### test_challenge

| | pred_0 | pred_1 |
|---|---:|---:|
| true_0 | 494 | 6 |
| true_1 | 16 | 21 |

## 5. Metrics by Data Origin

| split | data_origin | rows | macro_f1 | f1_label_1 | recall_label_1 | precision_label_1 |
| --- | --- | --- | --- | --- | --- | --- |
| test_challenge | external_curated | 76 | 0.4967 | 0.0000 | 0.0000 | 0.0000 |
| test_challenge | external_real | 75 | 0.4966 | 0.0000 | 0.0000 | 0.0000 |
| test_challenge | real | 386 | 0.8246 | 0.6774 | 0.5676 | 0.8400 |
| train | external_curated | 350 | 0.4993 | 0.0000 | 0.0000 | 0.0000 |
| train | paraphrased | 4333 | 0.4983 | 0.9966 | 0.9933 | 1.0000 |
| train | real | 1796 | 0.9039 | 0.8239 | 0.7209 | 0.9612 |
| train | synthetic | 10 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| train | synthetic_hard_positive | 653 | 0.4926 | 0.9852 | 0.9709 | 1.0000 |
| val | external_curated | 75 | 1.0000 | 0.0000 | 0.0000 | 0.0000 |
| val | external_real | 75 | 1.0000 | 0.0000 | 0.0000 | 0.0000 |
| val | real | 385 | 0.8371 | 0.7042 | 0.6757 | 0.7353 |

## 6. Training History

|   epoch |   train_loss |   val_macro_f1 |   val_f1_label_1 |   val_recall_label_1 |
|--------:|-------------:|---------------:|-----------------:|---------------------:|
|       1 |    0.296287  |       0.679493 |         0.442857 |             0.837838 |
|       2 |    0.118962  |       0.777806 |         0.593407 |             0.72973  |
|       3 |    0.0912525 |       0.716288 |         0.490909 |             0.72973  |
|       4 |    0.0742265 |       0.815491 |         0.658228 |             0.702703 |
|       5 |    0.0685945 |       0.797348 |         0.625    |             0.675676 |
|       6 |    0.0612628 |       0.797086 |         0.623377 |             0.648649 |
|       7 |    0.0600541 |       0.832497 |         0.694737 |             0.891892 |
|       8 |    0.0539131 |       0.841602 |         0.704225 |             0.675676 |
|       9 |    0.0455596 |       0.815491 |         0.658228 |             0.702703 |
|      10 |    0.0470824 |       0.818583 |         0.666667 |             0.783784 |
|      11 |    0.0432584 |       0.823672 |         0.674699 |             0.756757 |

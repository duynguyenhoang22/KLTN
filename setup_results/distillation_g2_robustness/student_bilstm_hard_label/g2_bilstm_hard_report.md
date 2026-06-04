# g2_bilstm_hard Report

## 1. Scope

- Architecture: `bilstm`
- Mode: `hard`
- Setup: `G2_external_curated` robustness check
- Input features: `content` only

## 2. Metrics by Split

| split | rows | accuracy | macro_f1 | f1_label_1 | recall_label_1 | precision_label_1 | roc_auc | pr_auc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| train | 7142 | 0.9884 | 0.9856 | 0.9919 | 0.9853 | 0.9986 | 0.9992 | 0.9997 |
| val | 535 | 0.9551 | 0.8341 | 0.6923 | 0.7297 | 0.6585 | 0.9483 | 0.7427 |
| test_challenge | 537 | 0.9646 | 0.8398 | 0.6984 | 0.5946 | 0.8462 | 0.9462 | 0.7301 |

## 4. Confusion Matrices

### train

| | pred_0 | pred_1 |
|---|---:|---:|
| true_0 | 1967 | 7 |
| true_1 | 76 | 5092 |

### val

| | pred_0 | pred_1 |
|---|---:|---:|
| true_0 | 484 | 14 |
| true_1 | 10 | 27 |

### test_challenge

| | pred_0 | pred_1 |
|---|---:|---:|
| true_0 | 496 | 4 |
| true_1 | 15 | 22 |

## 5. Metrics by Data Origin

| split | data_origin | rows | macro_f1 | f1_label_1 | recall_label_1 | precision_label_1 |
| --- | --- | --- | --- | --- | --- | --- |
| test_challenge | external_curated | 76 | 1.0000 | 0.0000 | 0.0000 | 0.0000 |
| test_challenge | external_real | 75 | 0.4966 | 0.0000 | 0.0000 | 0.0000 |
| test_challenge | real | 386 | 0.8422 | 0.7097 | 0.5946 | 0.8800 |
| train | external_curated | 350 | 1.0000 | 0.0000 | 0.0000 | 0.0000 |
| train | paraphrased | 4333 | 0.4990 | 0.9980 | 0.9961 | 1.0000 |
| train | real | 1796 | 0.9153 | 0.8452 | 0.7616 | 0.9493 |
| train | synthetic | 10 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| train | synthetic_hard_negative | 653 | 0.4930 | 0.9860 | 0.9724 | 1.0000 |
| val | external_curated | 75 | 0.4966 | 0.0000 | 0.0000 | 0.0000 |
| val | external_real | 75 | 1.0000 | 0.0000 | 0.0000 | 0.0000 |
| val | real | 385 | 0.8341 | 0.7013 | 0.7297 | 0.6750 |

## 6. Training History

|   epoch |   train_loss |   val_macro_f1 |   val_f1_label_1 |   val_recall_label_1 |
|--------:|-------------:|---------------:|-----------------:|---------------------:|
|       1 |    0.26112   |       0.797787 |         0.629213 |             0.756757 |
|       2 |    0.0897828 |       0.824369 |         0.675    |             0.72973  |
|       3 |    0.0559079 |       0.786807 |         0.613861 |             0.837838 |
|       4 |    0.0464396 |       0.815869 |         0.657895 |             0.675676 |
|       5 |    0.0353481 |       0.83304  |         0.691358 |             0.756757 |
|       6 |    0.0288033 |       0.811272 |         0.648649 |             0.648649 |
|       7 |    0.0326087 |       0.834057 |         0.692308 |             0.72973  |
|       8 |    0.0299328 |       0.797787 |         0.629213 |             0.756757 |
|       9 |    0.0204408 |       0.822982 |         0.674419 |             0.783784 |
|      10 |    0.0166595 |       0.797841 |         0.631579 |             0.810811 |

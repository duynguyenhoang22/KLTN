# g2_textcnn_distilled Report

## 1. Scope

- Architecture: `textcnn`
- Mode: `distilled`
- Setup: `G2_external_curated` robustness check
- Input features: `content` only

## 2. Metrics by Split

| split | rows | accuracy | macro_f1 | f1_label_1 | recall_label_1 | precision_label_1 | roc_auc | pr_auc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| train | 7142 | 0.9996 | 0.9995 | 0.9997 | 0.9994 | 1.0000 | 1.0000 | 1.0000 |
| val | 535 | 0.9757 | 0.9112 | 0.8354 | 0.8919 | 0.7857 | 0.9811 | 0.8781 |
| test_challenge | 537 | 0.9832 | 0.9355 | 0.8800 | 0.8919 | 0.8684 | 0.9835 | 0.8954 |

## 3. Comparison with Hard Baseline

| split | macro_f1_hard | macro_f1_distilled | delta_macro_f1 | f1_label_1_hard | f1_label_1_distilled | delta_f1_label_1 | recall_label_1_hard | recall_label_1_distilled | delta_recall_label_1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| train | 0.9951 | 0.9995 | 0.0044 | 0.9973 | 0.9997 | 0.0024 | 0.9952 | 0.9994 | 0.0043 |
| val | 0.8702 | 0.9112 | 0.0410 | 0.7595 | 0.8354 | 0.0759 | 0.8108 | 0.8919 | 0.0811 |
| test_challenge | 0.9068 | 0.9355 | 0.0287 | 0.8267 | 0.8800 | 0.0533 | 0.8378 | 0.8919 | 0.0541 |

## 4. Confusion Matrices

### train

| | pred_0 | pred_1 |
|---|---:|---:|
| true_0 | 1974 | 0 |
| true_1 | 3 | 5165 |

### val

| | pred_0 | pred_1 |
|---|---:|---:|
| true_0 | 489 | 9 |
| true_1 | 4 | 33 |

### test_challenge

| | pred_0 | pred_1 |
|---|---:|---:|
| true_0 | 495 | 5 |
| true_1 | 4 | 33 |

## 5. Metrics by Data Origin

| split | data_origin | rows | macro_f1 | f1_label_1 | recall_label_1 | precision_label_1 |
| --- | --- | --- | --- | --- | --- | --- |
| test_challenge | external_curated | 76 | 1.0000 | 0.0000 | 0.0000 | 0.0000 |
| test_challenge | external_real | 75 | 0.4966 | 0.0000 | 0.0000 | 0.0000 |
| test_challenge | real | 386 | 0.9402 | 0.8919 | 0.8919 | 0.8919 |
| train | external_curated | 350 | 1.0000 | 0.0000 | 0.0000 | 0.0000 |
| train | paraphrased | 4333 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| train | real | 1796 | 0.9951 | 0.9912 | 0.9826 | 1.0000 |
| train | synthetic | 10 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| train | synthetic_hard_positive | 653 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| val | external_curated | 75 | 0.4966 | 0.0000 | 0.0000 | 0.0000 |
| val | external_real | 75 | 0.4966 | 0.0000 | 0.0000 | 0.0000 |
| val | real | 385 | 0.9206 | 0.8571 | 0.8919 | 0.8250 |

## 6. Training History

|   epoch |   train_loss |   val_macro_f1 |   val_f1_label_1 |   val_recall_label_1 |
|--------:|-------------:|---------------:|-----------------:|---------------------:|
|       1 |    0.186211  |       0.821309 |         0.666667 |             0.648649 |
|       2 |    0.0696778 |       0.849869 |         0.725275 |             0.891892 |
|       3 |    0.057037  |       0.856688 |         0.732394 |             0.702703 |
|       4 |    0.0527233 |       0.875543 |         0.769231 |             0.810811 |
|       5 |    0.0471804 |       0.870161 |         0.759494 |             0.810811 |
|       6 |    0.0440792 |       0.878591 |         0.776471 |             0.891892 |
|       7 |    0.0444943 |       0.873558 |         0.767442 |             0.891892 |
|       8 |    0.0413121 |       0.891919 |         0.8      |             0.864865 |
|       9 |    0.0384453 |       0.883729 |         0.785714 |             0.891892 |
|      10 |    0.0388076 |       0.911162 |         0.835443 |             0.891892 |
|      11 |    0.0362814 |       0.894342 |         0.804878 |             0.891892 |
|      12 |    0.0357281 |       0.891919 |         0.8      |             0.864865 |

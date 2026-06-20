# Deployment Trade-off Relative to PhoBERT-base

- Benchmark split: `test`
- Positive metric deltas mean the student outperforms the teacher.
- Reduction and speedup values greater than 1 indicate lower student cost.

| student           |   parameter_reduction_x |   size_reduction_x |   latency_speedup_x |   throughput_gain_x |   peak_ram_reduction_percent |   macro_f1_delta |   f1_label_1_delta |   recall_label_1_delta |   pr_auc_delta |
|:------------------|------------------------:|-------------------:|--------------------:|--------------------:|-----------------------------:|-----------------:|-------------------:|-----------------------:|---------------:|
| BiLSTM distilled  |                 1686.13 |            1647.87 |             68.3906 |            222.467  |                      77.667  |          -0.0397 |            -0.0734 |                -0.0541 |        -0.1918 |
| TextCNN Distilled |                 1541.92 |            1512.96 |            152.102  |             97.4356 |                      77.0659 |           0.0121 |             0.0233 |                 0.0811 |        -0.0415 |

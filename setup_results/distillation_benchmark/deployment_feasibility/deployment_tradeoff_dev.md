# Deployment Trade-off Relative to PhoBERT-base

- Benchmark split: `dev`
- Positive metric deltas mean the student outperforms the teacher.
- Reduction and speedup values greater than 1 indicate lower student cost.

| student           |   parameter_reduction_x |   size_reduction_x |   latency_speedup_x |   throughput_gain_x |   peak_ram_reduction_percent |   macro_f1_delta |   f1_label_1_delta |   recall_label_1_delta |   pr_auc_delta |
|:------------------|------------------------:|-------------------:|--------------------:|--------------------:|-----------------------------:|-----------------:|-------------------:|-----------------------:|---------------:|
| BiLSTM distilled  |                 1686.13 |            1647.87 |             96.5356 |             239.447 |                      77.638  |           0.0088 |             0.0167 |                 0.027  |        -0.0198 |
| TextCNN Distilled |                 1541.92 |            1512.96 |            153.575  |             238.708 |                      77.1967 |           0.0379 |             0.0707 |                 0.0811 |         0.0379 |

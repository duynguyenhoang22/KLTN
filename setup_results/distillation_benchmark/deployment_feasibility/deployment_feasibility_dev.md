# Deployment Feasibility Evaluation

- Benchmark split: `dev`
- Rows: 535
- Device: CPU

| model             | params      |   size_mb |   cpu_latency_ms_per_msg |   throughput_sms_per_s |   peak_ram_mb |   macro_f1 |   f1_label_1 |   recall_label_1 |   pr_auc | status   |
|:------------------|:------------|----------:|-------------------------:|-----------------------:|--------------:|-----------:|-------------:|-----------------:|---------:|:---------|
| PhoBERT-base      | 134,999,810 |  516.95   |                 248.142  |                 4.1966 |      1788.75  |     0.875  |       0.7671 |           0.7568 |   0.8439 | ok       |
| BiLSTM distilled  | 80,065      |    0.3137 |                   2.5705 |              1004.88   |       400     |     0.8839 |       0.7838 |           0.7838 |   0.8241 | ok       |
| TextCNN Distilled | 87,553      |    0.3417 |                   1.6158 |              1001.77   |       407.894 |     0.9129 |       0.8378 |           0.8378 |   0.8818 | ok       |

Notes:
- Latency is measured with batch size 1 after warmup.
- Throughput and peak RAM are measured on one full batched pass.
- All quality metrics are recomputed on the selected benchmark split.
- PhoBERT uses the same ViTokenizer segmentation and max length as the model benchmark.
- Size is checkpoint size when weights exist; for PhoBERT without local weights, size is estimated as parameters x float32 bytes.
- PhoBERT runtime metrics require local model weights in the teacher model directory.

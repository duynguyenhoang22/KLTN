# Deployment Feasibility Evaluation

- Benchmark split: `test`
- Rows: 535
- Device: CPU

| model             | params      |   size_mb |   cpu_latency_ms_per_msg |   throughput_sms_per_s |   peak_ram_mb |   macro_f1 |   f1_label_1 |   recall_label_1 |   pr_auc | status   |
|:------------------|:------------|----------:|-------------------------:|-----------------------:|--------------:|-----------:|-------------:|-----------------:|---------:|:---------|
| PhoBERT-base      | 134,999,810 |  516.95   |                 179.778  |                 4.5547 |      1789.64  |     0.9068 |       0.8267 |           0.8378 |   0.9191 | ok       |
| BiLSTM distilled  | 80,065      |    0.3137 |                   2.6287 |              1013.28   |       399.68  |     0.8671 |       0.7532 |           0.7838 |   0.7273 | ok       |
| TextCNN Distilled | 87,553      |    0.3417 |                   1.182  |               443.793  |       410.438 |     0.9189 |       0.85   |           0.9189 |   0.8776 | ok       |

Notes:
- Latency is measured with batch size 1 after warmup.
- Throughput and peak RAM are measured on one full batched pass.
- All quality metrics are recomputed on the selected benchmark split.
- PhoBERT uses the same ViTokenizer segmentation and max length as the model benchmark.
- Size is checkpoint size when weights exist; for PhoBERT without local weights, size is estimated as parameters x float32 bytes.
- PhoBERT runtime metrics require local model weights in the teacher model directory.

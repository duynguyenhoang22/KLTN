# Deployment Feasibility Evaluation

- Test split: `test`
- Rows: 535
- Device: CPU

| model                                 | params      |   size_mb |   cpu_latency_ms_per_msg |   throughput_sms_per_s |   peak_ram_mb |   f1_label_1 | status   |
|:--------------------------------------|:------------|----------:|-------------------------:|-----------------------:|--------------:|-------------:|:---------|
| CafeBERT                              | 559,892,482 | 2152.83   |                 847.316  |                 0.7092 |      4358.34  |       0.88   | ok       |
| TextCNN hard CafeBERT seed42          | 87,553      |    0.342  |                   1.4801 |              1183.5    |       357.148 |       0.7416 | ok       |
| TextCNN vanilla KD CafeBERT seed42    | 87,553      |    0.3421 |                   1.2689 |              1069.82   |       373.785 |       0.8312 | ok       |
| TextCNN risk-aware KD CafeBERT seed42 | 87,553      |    0.3422 |                   1.1508 |              1239.91   |       373.406 |       0.8049 | ok       |

Notes:
- Latency is measured with batch size 1 after warmup.
- Throughput and peak RAM are measured on one full batched pass.
- Size is checkpoint size when weights exist; for PhoBERT without local weights, size is estimated as parameters x float32 bytes.
- PhoBERT runtime metrics require local model weights in the teacher model directory.

# Deployment Feasibility Evaluation

- Test split: `test_real`
- Rows: 385
- Device: CPU

| model             | params      |   size_mb |   cpu_latency_ms_per_msg |   throughput_sms_per_s |   peak_ram_mb |   f1_label_1 | status   |
|:------------------|:------------|----------:|-------------------------:|-----------------------:|--------------:|-------------:|:---------|
| PhoBERT-base      | 134,999,810 |  516.95   |                 171.654  |                 2.1438 |      2742.28  |       0.8182 | ok       |
| BiLSTM            | 79,105      |    0.3095 |                   4.4101 |               711.019  |       397.137 |       0.6494 | ok       |
| TextCNN Distilled | 86,593      |    0.3377 |                   1.9932 |               894.359  |       405.359 |       0.7879 | ok       |

Notes:
- Latency is measured with batch size 1 after warmup.
- Throughput and peak RAM are measured on one full batched pass.
- Size is checkpoint size when weights exist; for PhoBERT without local weights, size is estimated as parameters x float32 bytes.
- PhoBERT runtime metrics require local model weights in the teacher model directory.

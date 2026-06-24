# Deployment Feasibility Evaluation

- Test split: `test`
- Rows: 535
- Device: CPU

| model                 | params      |   size_mb | cpu_latency_ms_per_msg   | throughput_sms_per_s   | peak_ram_mb   |   f1_label_1 | status                                              |
|:----------------------|:------------|----------:|:-------------------------|:-----------------------|:--------------|-------------:|:----------------------------------------------------|
| PhoBERT-base          | 134,999,810 |  514.983  |                          |                        |               |       0.8267 | runtime_not_measured_missing_weights_size_estimated |
| TextCNN hard          | 87,553      |    0.3417 | 2.1863                   | 566.4592               | 352.0781      |       0.8378 | ok                                                  |
| TextCNN vanilla KD    | 87,553      |    0.3418 | 2.4339                   | 602.2287               | 370.9922      |       0.7692 | ok                                                  |
| TextCNN risk-aware KD | 87,553      |    0.3419 | 1.4243                   | 902.5750               | 370.7773      |       0.85   | ok                                                  |

Notes:
- Latency is measured with batch size 1 after warmup.
- Throughput and peak RAM are measured on one full batched pass.
- Size is checkpoint size when weights exist; for PhoBERT without local weights, size is estimated as parameters x float32 bytes.
- PhoBERT runtime metrics require local model weights in the teacher model directory.

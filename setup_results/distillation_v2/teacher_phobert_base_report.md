# PhoBERT-base Teacher Fine-tuning Report

## Configuration

- Model: `vinai/phobert-base`
- Train CSV: `/kaggle/input/datasets/duynguynhoang/distillation-dataset-v2/train.csv`
- Val CSV: `/kaggle/input/datasets/duynguynhoang/distillation-dataset-v2/val.csv`
- Seed: `42`
- Max length: `128`
- Epochs: `3`
- Train batch size: `16`
- Eval batch size: `32`
- Gradient accumulation steps: `1`
- Learning rate: `2e-05`
- Weight decay: `0.01`
- Warmup ratio: `0.1`
- FP16: `True`
- Elapsed seconds: `344.45`

## Validation Metrics

| metric            |    value |
|:------------------|---------:|
| accuracy          | 0.988196 |
| macro_f1          | 0.988089 |
| weighted_f1       | 0.988196 |
| precision_label_1 | 0.986965 |
| recall_label_1    | 0.986965 |
| f1_label_1        | 0.986965 |
| precision_label_0 | 0.989214 |
| recall_label_0    | 0.989214 |
| f1_label_0        | 0.989214 |
| roc_auc           | 0.998849 |
| pr_auc            | 0.998841 |

## Confusion Matrix

`labels=[0, 1]`, rows are true labels and columns are predicted labels.

|        |   pred_0 |   pred_1 |
|:-------|---------:|---------:|
| true_0 |      642 |        7 |
| true_1 |        7 |      530 |

## Train Distribution

### Label

|   label |   count |   percent |
|--------:|--------:|----------:|
|       1 |    3856 |     53.47 |
|       0 |    3356 |     46.53 |

### Data Origin

| data_origin             |   count |   percent |
|:------------------------|--------:|----------:|
| paraphrased             |    3333 |     46.21 |
| synthetic               |    1506 |     20.88 |
| real                    |    1281 |     17.76 |
| synthetic_hard_negative |     391 |      5.42 |
| external_curated        |     351 |      4.87 |
| external_real           |     350 |      4.85 |

### Category

| category                   |   count |   percent |
|:---------------------------|--------:|----------:|
| Viễn thông                 |     676 |      9.37 |
| Tuyển dụng giả             |     522 |      7.24 |
| Cờ bạc / Betting           |     502 |      6.96 |
| BHXH / Trợ cấp giả         |     496 |      6.88 |
| Crypto / Đầu tư giả        |     491 |      6.81 |
| Nội dung nhạy cảm          |     485 |      6.72 |
| Khác                       |     445 |      6.17 |
| Dịch vụ công giả           |     423 |      5.87 |
| Tin nhắn cá nhân và OTP    |     416 |      5.77 |
| Giả mạo ngân hàng          |     375 |      5.2  |
| Đòi nợ / Đe dọa            |     370 |      5.13 |
| P2P hard negative          |     351 |      4.87 |
| P2P hội thoại thông thường |     350 |      4.85 |
| Ngân hàng thật             |     291 |      4.03 |
| Quảng cáo hợp lệ           |     237 |      3.29 |
| Dịch vụ công thật          |     229 |      3.18 |
| Vận chuyển                 |     207 |      2.87 |
| Thương mại điện tử         |     190 |      2.63 |
| Dịch vụ y tế               |     156 |      2.16 |

### Label x Data Origin

| data_origin             |    0 |    1 |
|:------------------------|-----:|-----:|
| external_curated        |  351 |    0 |
| external_real           |  350 |    0 |
| paraphrased             |    0 | 3333 |
| real                    | 1159 |  122 |
| synthetic               | 1496 |   10 |
| synthetic_hard_negative |    0 |  391 |

## Validation Distribution

### Label

|   label |   count |   percent |
|--------:|--------:|----------:|
|       0 |     649 |     54.72 |
|       1 |     537 |     45.28 |

### Data Origin

| data_origin             |   count |   percent |
|:------------------------|--------:|----------:|
| paraphrased             |     434 |     36.59 |
| real                    |     385 |     32.46 |
| synthetic               |     201 |     16.95 |
| synthetic_hard_negative |      66 |      5.56 |
| external_curated        |      50 |      4.22 |
| external_real           |      50 |      4.22 |

### Category

| category                   |   count |   percent |
|:---------------------------|--------:|----------:|
| Viễn thông                 |     179 |     15.09 |
| Khác                       |     111 |      9.36 |
| Tin nhắn cá nhân và OTP    |      80 |      6.75 |
| Tuyển dụng giả             |      73 |      6.16 |
| Cờ bạc / Betting           |      70 |      5.9  |
| BHXH / Trợ cấp giả         |      67 |      5.65 |
| Nội dung nhạy cảm          |      64 |      5.4  |
| Crypto / Đầu tư giả        |      63 |      5.31 |
| Dịch vụ công giả           |      57 |      4.81 |
| Giả mạo ngân hàng          |      57 |      4.81 |
| Đòi nợ / Đe dọa            |      51 |      4.3  |
| P2P hard negative          |      50 |      4.22 |
| Ngân hàng thật             |      50 |      4.22 |
| P2P hội thoại thông thường |      50 |      4.22 |
| Dịch vụ công thật          |      46 |      3.88 |
| Quảng cáo hợp lệ           |      43 |      3.63 |
| Vận chuyển                 |      29 |      2.45 |
| Thương mại điện tử         |      25 |      2.11 |
| Dịch vụ y tế               |      21 |      1.77 |

### Label x Data Origin

| data_origin             |   0 |   1 |
|:------------------------|----:|----:|
| external_curated        |  50 |   0 |
| external_real           |  50 |   0 |
| paraphrased             |   0 | 434 |
| real                    | 348 |  37 |
| synthetic               | 201 |   0 |
| synthetic_hard_negative |   0 |  66 |

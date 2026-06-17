# Distillation Split Report

## 1. Configuration

- Input file: `model/base/temp.csv`
- Seed: `42`
- Stratum key: `label x data_origin x category`
- Small stratum rules: `n < 5 -> train`, `5 <= n < 10 -> train/val`, `n >= 10 -> origin rule`

## 2. Split Sizes

| split          |   rows |   percent |
|:---------------|-------:|----------:|
| train          |   8026 |     75.99 |
| val            |   1186 |     11.23 |
| test_real      |    385 |      3.65 |
| test_mixed     |    635 |      6.01 |
| test_challenge |    330 |      3.12 |

## 3. Content Overlap Check

| left_split   | right_split    |   content_overlap |
|:-------------|:---------------|------------------:|
| train        | val            |                 0 |
| train        | test_real      |                 0 |
| train        | test_mixed     |                 0 |
| train        | test_challenge |                 0 |
| val          | test_real      |                 0 |
| val          | test_mixed     |                 0 |
| val          | test_challenge |                 0 |
| test_real    | test_mixed     |                 0 |
| test_real    | test_challenge |                 0 |
| test_mixed   | test_challenge |                 0 |

## 4. Sample ID Overlap Check

| left_split   | right_split    |   sample_id_overlap |
|:-------------|:---------------|--------------------:|
| train        | val            |                   0 |
| train        | test_real      |                   0 |
| train        | test_mixed     |                   0 |
| train        | test_challenge |                   0 |
| val          | test_real      |                   0 |
| val          | test_mixed     |                   0 |
| val          | test_challenge |                   0 |
| test_real    | test_mixed     |                   0 |
| test_real    | test_challenge |                   0 |
| test_mixed   | test_challenge |                   0 |

## 5. Strata Summary

|   label | data_origin             | category                   |    n |   train |   val |   test_real |   test_mixed |   test_challenge | small_stratum_rule   |
|--------:|:------------------------|:---------------------------|-----:|--------:|------:|------------:|-------------:|-----------------:|:---------------------|
|       0 | external_curated        | P2P hard negative          |  501 |     351 |    50 |           0 |            0 |              100 | full_rule            |
|       0 | external_real           | P2P hội thoại thông thường |  500 |     350 |    50 |           0 |            0 |              100 | full_rule            |
|       1 | paraphrased             | BHXH / Trợ cấp giả         |  587 |     469 |    59 |           0 |           59 |                0 | full_rule            |
|       1 | paraphrased             | Crypto / Đầu tư giả        |  625 |     501 |    62 |           0 |           62 |                0 | full_rule            |
|       1 | paraphrased             | Cờ bạc / Betting           |  618 |     494 |    62 |           0 |           62 |                0 | full_rule            |
|       1 | paraphrased             | Dịch vụ công giả           |  474 |     380 |    47 |           0 |           47 |                0 | full_rule            |
|       1 | paraphrased             | Giả mạo ngân hàng          |  386 |     308 |    39 |           0 |           39 |                0 | full_rule            |
|       1 | paraphrased             | Nội dung nhạy cảm          |  621 |     497 |    62 |           0 |           62 |                0 | full_rule            |
|       1 | paraphrased             | Tuyển dụng giả             |  595 |     475 |    60 |           0 |           60 |                0 | full_rule            |
|       1 | paraphrased             | Đòi nợ / Đe dọa            |  427 |     341 |    43 |           0 |           43 |                0 | full_rule            |
|       0 | real                    | Dịch vụ công thật          |  170 |     118 |    26 |          26 |            0 |                0 | full_rule            |
|       0 | real                    | Dịch vụ y tế               |    2 |       2 |     0 |           0 |            0 |                0 | all_train            |
|       0 | real                    | Khác                       |  507 |     355 |    76 |          76 |            0 |                0 | full_rule            |
|       0 | real                    | Ngân hàng thật             |  126 |      88 |    19 |          19 |            0 |                0 | full_rule            |
|       0 | real                    | Quảng cáo hợp lệ           |  136 |      96 |    20 |          20 |            0 |                0 | full_rule            |
|       0 | real                    | Thương mại điện tử         |    1 |       1 |     0 |           0 |            0 |                0 | all_train            |
|       0 | real                    | Tin nhắn cá nhân và OTP    |  301 |     211 |    45 |          45 |            0 |                0 | full_rule            |
|       0 | real                    | Viễn thông                 | 1060 |     742 |   159 |         159 |            0 |                0 | full_rule            |
|       0 | real                    | Vận chuyển                 |   18 |      12 |     3 |           3 |            0 |                0 | full_rule            |
|       1 | real                    | BHXH / Trợ cấp giả         |   15 |      11 |     2 |           2 |            0 |                0 | full_rule            |
|       1 | real                    | Crypto / Đầu tư giả        |    2 |       2 |     0 |           0 |            0 |                0 | all_train            |
|       1 | real                    | Cờ bạc / Betting           |   53 |      37 |     8 |           8 |            0 |                0 | full_rule            |
|       1 | real                    | Dịch vụ công giả           |   16 |      12 |     2 |           2 |            0 |                0 | full_rule            |
|       1 | real                    | Giả mạo ngân hàng          |   65 |      45 |    10 |          10 |            0 |                0 | full_rule            |
|       1 | real                    | Khác                       |   46 |      32 |     7 |           7 |            0 |                0 | full_rule            |
|       1 | real                    | Nội dung nhạy cảm          |   10 |       6 |     2 |           2 |            0 |                0 | full_rule            |
|       1 | real                    | Tuyển dụng giả             |   27 |      19 |     4 |           4 |            0 |                0 | full_rule            |
|       1 | real                    | Đòi nợ / Đe dọa            |   12 |       8 |     2 |           2 |            0 |                0 | full_rule            |
|       0 | synthetic               | Dịch vụ công thật          |  195 |     155 |    20 |           0 |           20 |                0 | full_rule            |
|       0 | synthetic               | Dịch vụ y tế               |  206 |     164 |    21 |           0 |           21 |                0 | full_rule            |
|       0 | synthetic               | Ngân hàng thật             |  306 |     244 |    31 |           0 |           31 |                0 | full_rule            |
|       0 | synthetic               | Quảng cáo hợp lệ           |  226 |     180 |    23 |           0 |           23 |                0 | full_rule            |
|       0 | synthetic               | Thương mại điện tử         |  252 |     202 |    25 |           0 |           25 |                0 | full_rule            |
|       0 | synthetic               | Tin nhắn cá nhân và OTP    |  353 |     283 |    35 |           0 |           35 |                0 | full_rule            |
|       0 | synthetic               | Viễn thông                 |  196 |     156 |    20 |           0 |           20 |                0 | full_rule            |
|       0 | synthetic               | Vận chuyển                 |  264 |     212 |    26 |           0 |           26 |                0 | full_rule            |
|       1 | synthetic               | BHXH / Trợ cấp giả         |    2 |       2 |     0 |           0 |            0 |                0 | all_train            |
|       1 | synthetic               | Dịch vụ công giả           |    2 |       2 |     0 |           0 |            0 |                0 | all_train            |
|       1 | synthetic               | Giả mạo ngân hàng          |    1 |       1 |     0 |           0 |            0 |                0 | all_train            |
|       1 | synthetic               | Nội dung nhạy cảm          |    3 |       3 |     0 |           0 |            0 |                0 | all_train            |
|       1 | synthetic               | Tuyển dụng giả             |    1 |       1 |     0 |           0 |            0 |                0 | all_train            |
|       1 | synthetic               | Đòi nợ / Đe dọa            |    1 |       1 |     0 |           0 |            0 |                0 | all_train            |
|       1 | synthetic_hard_positive | BHXH / Trợ cấp giả         |   60 |      42 |     6 |           0 |            0 |               12 | full_rule            |
|       1 | synthetic_hard_positive | Crypto / Đầu tư giả        |   11 |       8 |     1 |           0 |            0 |                2 | full_rule            |
|       1 | synthetic_hard_positive | Dịch vụ công giả           |   79 |      55 |     8 |           0 |            0 |               16 | full_rule            |
|       1 | synthetic_hard_positive | Giả mạo ngân hàng          |   76 |      53 |     8 |           0 |            0 |               15 | full_rule            |
|       1 | synthetic_hard_positive | Khác                       |  282 |     198 |    28 |           0 |            0 |               56 | full_rule            |
|       1 | synthetic_hard_positive | Tuyển dụng giả             |   86 |      60 |     9 |           0 |            0 |               17 | full_rule            |
|       1 | synthetic_hard_positive | Đòi nợ / Đe dọa            |   59 |      41 |     6 |           0 |            0 |               12 | full_rule            |

## 6. Small Strata

|   label | data_origin   | category            |   n |   train |   val |   test_real |   test_mixed |   test_challenge | small_stratum_rule   |
|--------:|:--------------|:--------------------|----:|--------:|------:|------------:|-------------:|-----------------:|:---------------------|
|       0 | real          | Thương mại điện tử  |   1 |       1 |     0 |           0 |            0 |                0 | all_train            |
|       1 | synthetic     | Giả mạo ngân hàng   |   1 |       1 |     0 |           0 |            0 |                0 | all_train            |
|       1 | synthetic     | Tuyển dụng giả      |   1 |       1 |     0 |           0 |            0 |                0 | all_train            |
|       1 | synthetic     | Đòi nợ / Đe dọa     |   1 |       1 |     0 |           0 |            0 |                0 | all_train            |
|       0 | real          | Dịch vụ y tế        |   2 |       2 |     0 |           0 |            0 |                0 | all_train            |
|       1 | real          | Crypto / Đầu tư giả |   2 |       2 |     0 |           0 |            0 |                0 | all_train            |
|       1 | synthetic     | BHXH / Trợ cấp giả  |   2 |       2 |     0 |           0 |            0 |                0 | all_train            |
|       1 | synthetic     | Dịch vụ công giả    |   2 |       2 |     0 |           0 |            0 |                0 | all_train            |
|       1 | synthetic     | Nội dung nhạy cảm   |   3 |       3 |     0 |           0 |            0 |                0 | all_train            |

## 7. Split Detail: `train`

Rows: `8026`

### Label Distribution

|   label |   count |   percent |
|--------:|--------:|----------:|
|       1 |    4104 |     51.13 |
|       0 |    3922 |     48.87 |

### Data Origin Distribution

| data_origin             |   count |   percent |
|:------------------------|--------:|----------:|
| paraphrased             |    3465 |     43.17 |
| real                    |    1797 |     22.39 |
| synthetic               |    1606 |     20.01 |
| synthetic_hard_positive |     457 |      5.69 |
| external_curated        |     351 |      4.37 |
| external_real           |     350 |      4.36 |

### Category Distribution

| category                   |   count |   percent |
|:---------------------------|--------:|----------:|
| Viễn thông                 |     898 |     11.19 |
| Khác                       |     585 |      7.29 |
| Tuyển dụng giả             |     555 |      6.92 |
| Cờ bạc / Betting           |     531 |      6.62 |
| BHXH / Trợ cấp giả         |     524 |      6.53 |
| Crypto / Đầu tư giả        |     511 |      6.37 |
| Nội dung nhạy cảm          |     506 |      6.3  |
| Tin nhắn cá nhân và OTP    |     494 |      6.15 |
| Dịch vụ công giả           |     449 |      5.59 |
| Giả mạo ngân hàng          |     407 |      5.07 |
| Đòi nợ / Đe dọa            |     391 |      4.87 |
| P2P hard negative          |     351 |      4.37 |
| P2P hội thoại thông thường |     350 |      4.36 |
| Ngân hàng thật             |     332 |      4.14 |
| Quảng cáo hợp lệ           |     276 |      3.44 |
| Dịch vụ công thật          |     273 |      3.4  |
| Vận chuyển                 |     224 |      2.79 |
| Thương mại điện tử         |     203 |      2.53 |
| Dịch vụ y tế               |     166 |      2.07 |

### Label x Data Origin

| data_origin             |    0 |    1 |
|:------------------------|-----:|-----:|
| external_curated        |  351 |    0 |
| external_real           |  350 |    0 |
| paraphrased             |    0 | 3465 |
| real                    | 1625 |  172 |
| synthetic               | 1596 |   10 |
| synthetic_hard_positive |    0 |  457 |

### Label x Category

| category                   |   0 |   1 |
|:---------------------------|----:|----:|
| BHXH / Trợ cấp giả         |   0 | 524 |
| Crypto / Đầu tư giả        |   0 | 511 |
| Cờ bạc / Betting           |   0 | 531 |
| Dịch vụ công giả           |   0 | 449 |
| Dịch vụ công thật          | 273 |   0 |
| Dịch vụ y tế               | 166 |   0 |
| Giả mạo ngân hàng          |   0 | 407 |
| Khác                       | 355 | 230 |
| Ngân hàng thật             | 332 |   0 |
| Nội dung nhạy cảm          |   0 | 506 |
| P2P hard negative          | 351 |   0 |
| P2P hội thoại thông thường | 350 |   0 |
| Quảng cáo hợp lệ           | 276 |   0 |
| Thương mại điện tử         | 203 |   0 |
| Tin nhắn cá nhân và OTP    | 494 |   0 |
| Tuyển dụng giả             |   0 | 555 |
| Viễn thông                 | 898 |   0 |
| Vận chuyển                 | 224 |   0 |
| Đòi nợ / Đe dọa            |   0 | 391 |

### Data Origin x Category

| data_origin             |   BHXH / Trợ cấp giả |   Crypto / Đầu tư giả |   Cờ bạc / Betting |   Dịch vụ công giả |   Dịch vụ công thật |   Dịch vụ y tế |   Giả mạo ngân hàng |   Khác |   Ngân hàng thật |   Nội dung nhạy cảm |   P2P hard negative |   P2P hội thoại thông thường |   Quảng cáo hợp lệ |   Thương mại điện tử |   Tin nhắn cá nhân và OTP |   Tuyển dụng giả |   Viễn thông |   Vận chuyển |   Đòi nợ / Đe dọa |
|:------------------------|---------------------:|----------------------:|-------------------:|-------------------:|--------------------:|---------------:|--------------------:|-------:|-----------------:|--------------------:|--------------------:|-----------------------------:|-------------------:|---------------------:|--------------------------:|-----------------:|-------------:|-------------:|------------------:|
| external_curated        |                    0 |                     0 |                  0 |                  0 |                   0 |              0 |                   0 |      0 |                0 |                   0 |                 351 |                            0 |                  0 |                    0 |                         0 |                0 |            0 |            0 |                 0 |
| external_real           |                    0 |                     0 |                  0 |                  0 |                   0 |              0 |                   0 |      0 |                0 |                   0 |                   0 |                          350 |                  0 |                    0 |                         0 |                0 |            0 |            0 |                 0 |
| paraphrased             |                  469 |                   501 |                494 |                380 |                   0 |              0 |                 308 |      0 |                0 |                 497 |                   0 |                            0 |                  0 |                    0 |                         0 |              475 |            0 |            0 |               341 |
| real                    |                   11 |                     2 |                 37 |                 12 |                 118 |              2 |                  45 |    387 |               88 |                   6 |                   0 |                            0 |                 96 |                    1 |                       211 |               19 |          742 |           12 |                 8 |
| synthetic               |                    2 |                     0 |                  0 |                  2 |                 155 |            164 |                   1 |      0 |              244 |                   3 |                   0 |                            0 |                180 |                  202 |                       283 |                1 |          156 |          212 |                 1 |
| synthetic_hard_positive |                   42 |                     8 |                  0 |                 55 |                   0 |              0 |                  53 |    198 |                0 |                   0 |                   0 |                            0 |                  0 |                    0 |                         0 |               60 |            0 |            0 |                41 |

## 7. Split Detail: `val`

Rows: `1186`

### Label Distribution

|   label |   count |   percent |
|--------:|--------:|----------:|
|       0 |     649 |     54.72 |
|       1 |     537 |     45.28 |

### Data Origin Distribution

| data_origin             |   count |   percent |
|:------------------------|--------:|----------:|
| paraphrased             |     434 |     36.59 |
| real                    |     385 |     32.46 |
| synthetic               |     201 |     16.95 |
| synthetic_hard_positive |      66 |      5.56 |
| external_real           |      50 |      4.22 |
| external_curated        |      50 |      4.22 |

### Category Distribution

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
| Ngân hàng thật             |      50 |      4.22 |
| P2P hội thoại thông thường |      50 |      4.22 |
| P2P hard negative          |      50 |      4.22 |
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
| synthetic_hard_positive |   0 |  66 |

### Label x Category

| category                   |   0 |   1 |
|:---------------------------|----:|----:|
| BHXH / Trợ cấp giả         |   0 |  67 |
| Crypto / Đầu tư giả        |   0 |  63 |
| Cờ bạc / Betting           |   0 |  70 |
| Dịch vụ công giả           |   0 |  57 |
| Dịch vụ công thật          |  46 |   0 |
| Dịch vụ y tế               |  21 |   0 |
| Giả mạo ngân hàng          |   0 |  57 |
| Khác                       |  76 |  35 |
| Ngân hàng thật             |  50 |   0 |
| Nội dung nhạy cảm          |   0 |  64 |
| P2P hard negative          |  50 |   0 |
| P2P hội thoại thông thường |  50 |   0 |
| Quảng cáo hợp lệ           |  43 |   0 |
| Thương mại điện tử         |  25 |   0 |
| Tin nhắn cá nhân và OTP    |  80 |   0 |
| Tuyển dụng giả             |   0 |  73 |
| Viễn thông                 | 179 |   0 |
| Vận chuyển                 |  29 |   0 |
| Đòi nợ / Đe dọa            |   0 |  51 |

### Data Origin x Category

| data_origin             |   BHXH / Trợ cấp giả |   Crypto / Đầu tư giả |   Cờ bạc / Betting |   Dịch vụ công giả |   Dịch vụ công thật |   Dịch vụ y tế |   Giả mạo ngân hàng |   Khác |   Ngân hàng thật |   Nội dung nhạy cảm |   P2P hard negative |   P2P hội thoại thông thường |   Quảng cáo hợp lệ |   Thương mại điện tử |   Tin nhắn cá nhân và OTP |   Tuyển dụng giả |   Viễn thông |   Vận chuyển |   Đòi nợ / Đe dọa |
|:------------------------|---------------------:|----------------------:|-------------------:|-------------------:|--------------------:|---------------:|--------------------:|-------:|-----------------:|--------------------:|--------------------:|-----------------------------:|-------------------:|---------------------:|--------------------------:|-----------------:|-------------:|-------------:|------------------:|
| external_curated        |                    0 |                     0 |                  0 |                  0 |                   0 |              0 |                   0 |      0 |                0 |                   0 |                  50 |                            0 |                  0 |                    0 |                         0 |                0 |            0 |            0 |                 0 |
| external_real           |                    0 |                     0 |                  0 |                  0 |                   0 |              0 |                   0 |      0 |                0 |                   0 |                   0 |                           50 |                  0 |                    0 |                         0 |                0 |            0 |            0 |                 0 |
| paraphrased             |                   59 |                    62 |                 62 |                 47 |                   0 |              0 |                  39 |      0 |                0 |                  62 |                   0 |                            0 |                  0 |                    0 |                         0 |               60 |            0 |            0 |                43 |
| real                    |                    2 |                     0 |                  8 |                  2 |                  26 |              0 |                  10 |     83 |               19 |                   2 |                   0 |                            0 |                 20 |                    0 |                        45 |                4 |          159 |            3 |                 2 |
| synthetic               |                    0 |                     0 |                  0 |                  0 |                  20 |             21 |                   0 |      0 |               31 |                   0 |                   0 |                            0 |                 23 |                   25 |                        35 |                0 |           20 |           26 |                 0 |
| synthetic_hard_positive |                    6 |                     1 |                  0 |                  8 |                   0 |              0 |                   8 |     28 |                0 |                   0 |                   0 |                            0 |                  0 |                    0 |                         0 |                9 |            0 |            0 |                 6 |

## 7. Split Detail: `test_real`

Rows: `385`

### Label Distribution

|   label |   count |   percent |
|--------:|--------:|----------:|
|       0 |     348 |     90.39 |
|       1 |      37 |      9.61 |

### Data Origin Distribution

| data_origin   |   count |   percent |
|:--------------|--------:|----------:|
| real          |     385 |       100 |

### Category Distribution

| category                |   count |   percent |
|:------------------------|--------:|----------:|
| Viễn thông              |     159 |     41.3  |
| Khác                    |      83 |     21.56 |
| Tin nhắn cá nhân và OTP |      45 |     11.69 |
| Dịch vụ công thật       |      26 |      6.75 |
| Quảng cáo hợp lệ        |      20 |      5.19 |
| Ngân hàng thật          |      19 |      4.94 |
| Giả mạo ngân hàng       |      10 |      2.6  |
| Cờ bạc / Betting        |       8 |      2.08 |
| Tuyển dụng giả          |       4 |      1.04 |
| Vận chuyển              |       3 |      0.78 |
| Nội dung nhạy cảm       |       2 |      0.52 |
| Đòi nợ / Đe dọa         |       2 |      0.52 |
| BHXH / Trợ cấp giả      |       2 |      0.52 |
| Dịch vụ công giả        |       2 |      0.52 |

### Label x Data Origin

| data_origin   |   0 |   1 |
|:--------------|----:|----:|
| real          | 348 |  37 |

### Label x Category

| category                |   0 |   1 |
|:------------------------|----:|----:|
| BHXH / Trợ cấp giả      |   0 |   2 |
| Cờ bạc / Betting        |   0 |   8 |
| Dịch vụ công giả        |   0 |   2 |
| Dịch vụ công thật       |  26 |   0 |
| Giả mạo ngân hàng       |   0 |  10 |
| Khác                    |  76 |   7 |
| Ngân hàng thật          |  19 |   0 |
| Nội dung nhạy cảm       |   0 |   2 |
| Quảng cáo hợp lệ        |  20 |   0 |
| Tin nhắn cá nhân và OTP |  45 |   0 |
| Tuyển dụng giả          |   0 |   4 |
| Viễn thông              | 159 |   0 |
| Vận chuyển              |   3 |   0 |
| Đòi nợ / Đe dọa         |   0 |   2 |

### Data Origin x Category

| data_origin   |   BHXH / Trợ cấp giả |   Cờ bạc / Betting |   Dịch vụ công giả |   Dịch vụ công thật |   Giả mạo ngân hàng |   Khác |   Ngân hàng thật |   Nội dung nhạy cảm |   Quảng cáo hợp lệ |   Tin nhắn cá nhân và OTP |   Tuyển dụng giả |   Viễn thông |   Vận chuyển |   Đòi nợ / Đe dọa |
|:--------------|---------------------:|-------------------:|-------------------:|--------------------:|--------------------:|-------:|-----------------:|--------------------:|-------------------:|--------------------------:|-----------------:|-------------:|-------------:|------------------:|
| real          |                    2 |                  8 |                  2 |                  26 |                  10 |     83 |               19 |                   2 |                 20 |                        45 |                4 |          159 |            3 |                 2 |

## 7. Split Detail: `test_mixed`

Rows: `635`

### Label Distribution

|   label |   count |   percent |
|--------:|--------:|----------:|
|       1 |     434 |     68.35 |
|       0 |     201 |     31.65 |

### Data Origin Distribution

| data_origin   |   count |   percent |
|:--------------|--------:|----------:|
| paraphrased   |     434 |     68.35 |
| synthetic     |     201 |     31.65 |

### Category Distribution

| category                |   count |   percent |
|:------------------------|--------:|----------:|
| Crypto / Đầu tư giả     |      62 |      9.76 |
| Nội dung nhạy cảm       |      62 |      9.76 |
| Cờ bạc / Betting        |      62 |      9.76 |
| Tuyển dụng giả          |      60 |      9.45 |
| BHXH / Trợ cấp giả      |      59 |      9.29 |
| Dịch vụ công giả        |      47 |      7.4  |
| Đòi nợ / Đe dọa         |      43 |      6.77 |
| Giả mạo ngân hàng       |      39 |      6.14 |
| Tin nhắn cá nhân và OTP |      35 |      5.51 |
| Ngân hàng thật          |      31 |      4.88 |
| Vận chuyển              |      26 |      4.09 |
| Thương mại điện tử      |      25 |      3.94 |
| Quảng cáo hợp lệ        |      23 |      3.62 |
| Dịch vụ y tế            |      21 |      3.31 |
| Dịch vụ công thật       |      20 |      3.15 |
| Viễn thông              |      20 |      3.15 |

### Label x Data Origin

| data_origin   |   0 |   1 |
|:--------------|----:|----:|
| paraphrased   |   0 | 434 |
| synthetic     | 201 |   0 |

### Label x Category

| category                |   0 |   1 |
|:------------------------|----:|----:|
| BHXH / Trợ cấp giả      |   0 |  59 |
| Crypto / Đầu tư giả     |   0 |  62 |
| Cờ bạc / Betting        |   0 |  62 |
| Dịch vụ công giả        |   0 |  47 |
| Dịch vụ công thật       |  20 |   0 |
| Dịch vụ y tế            |  21 |   0 |
| Giả mạo ngân hàng       |   0 |  39 |
| Ngân hàng thật          |  31 |   0 |
| Nội dung nhạy cảm       |   0 |  62 |
| Quảng cáo hợp lệ        |  23 |   0 |
| Thương mại điện tử      |  25 |   0 |
| Tin nhắn cá nhân và OTP |  35 |   0 |
| Tuyển dụng giả          |   0 |  60 |
| Viễn thông              |  20 |   0 |
| Vận chuyển              |  26 |   0 |
| Đòi nợ / Đe dọa         |   0 |  43 |

### Data Origin x Category

| data_origin   |   BHXH / Trợ cấp giả |   Crypto / Đầu tư giả |   Cờ bạc / Betting |   Dịch vụ công giả |   Dịch vụ công thật |   Dịch vụ y tế |   Giả mạo ngân hàng |   Ngân hàng thật |   Nội dung nhạy cảm |   Quảng cáo hợp lệ |   Thương mại điện tử |   Tin nhắn cá nhân và OTP |   Tuyển dụng giả |   Viễn thông |   Vận chuyển |   Đòi nợ / Đe dọa |
|:--------------|---------------------:|----------------------:|-------------------:|-------------------:|--------------------:|---------------:|--------------------:|-----------------:|--------------------:|-------------------:|---------------------:|--------------------------:|-----------------:|-------------:|-------------:|------------------:|
| paraphrased   |                   59 |                    62 |                 62 |                 47 |                   0 |              0 |                  39 |                0 |                  62 |                  0 |                    0 |                         0 |               60 |            0 |            0 |                43 |
| synthetic     |                    0 |                     0 |                  0 |                  0 |                  20 |             21 |                   0 |               31 |                   0 |                 23 |                   25 |                        35 |                0 |           20 |           26 |                 0 |

## 7. Split Detail: `test_challenge`

Rows: `330`

### Label Distribution

|   label |   count |   percent |
|--------:|--------:|----------:|
|       0 |     200 |     60.61 |
|       1 |     130 |     39.39 |

### Data Origin Distribution

| data_origin             |   count |   percent |
|:------------------------|--------:|----------:|
| synthetic_hard_positive |     130 |     39.39 |
| external_curated        |     100 |     30.3  |
| external_real           |     100 |     30.3  |

### Category Distribution

| category                   |   count |   percent |
|:---------------------------|--------:|----------:|
| P2P hard negative          |     100 |     30.3  |
| P2P hội thoại thông thường |     100 |     30.3  |
| Khác                       |      56 |     16.97 |
| Tuyển dụng giả             |      17 |      5.15 |
| Dịch vụ công giả           |      16 |      4.85 |
| Giả mạo ngân hàng          |      15 |      4.55 |
| BHXH / Trợ cấp giả         |      12 |      3.64 |
| Đòi nợ / Đe dọa            |      12 |      3.64 |
| Crypto / Đầu tư giả        |       2 |      0.61 |

### Label x Data Origin

| data_origin             |   0 |   1 |
|:------------------------|----:|----:|
| external_curated        | 100 |   0 |
| external_real           | 100 |   0 |
| synthetic_hard_positive |   0 | 130 |

### Label x Category

| category                   |   0 |   1 |
|:---------------------------|----:|----:|
| BHXH / Trợ cấp giả         |   0 |  12 |
| Crypto / Đầu tư giả        |   0 |   2 |
| Dịch vụ công giả           |   0 |  16 |
| Giả mạo ngân hàng          |   0 |  15 |
| Khác                       |   0 |  56 |
| P2P hard negative          | 100 |   0 |
| P2P hội thoại thông thường | 100 |   0 |
| Tuyển dụng giả             |   0 |  17 |
| Đòi nợ / Đe dọa            |   0 |  12 |

### Data Origin x Category

| data_origin             |   BHXH / Trợ cấp giả |   Crypto / Đầu tư giả |   Dịch vụ công giả |   Giả mạo ngân hàng |   Khác |   P2P hard negative |   P2P hội thoại thông thường |   Tuyển dụng giả |   Đòi nợ / Đe dọa |
|:------------------------|---------------------:|----------------------:|-------------------:|--------------------:|-------:|--------------------:|-----------------------------:|-----------------:|------------------:|
| external_curated        |                    0 |                     0 |                  0 |                   0 |      0 |                 100 |                            0 |                0 |                 0 |
| external_real           |                    0 |                     0 |                  0 |                   0 |      0 |                   0 |                          100 |                0 |                 0 |
| synthetic_hard_positive |                   12 |                     2 |                 16 |                  15 |     56 |                   0 |                            0 |               17 |                12 |

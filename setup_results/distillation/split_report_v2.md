# Distillation Split Report V2

## 1. Configuration

- Input file: `model/base/temp.csv`
- Seed: `42`
- Stratum key: `label x data_origin x category`
- Goal: improve `test_mixed` and `test_challenge` by reducing source-only separation.
- Small stratum rules: `n < 5 -> train`, `5 <= n < 10 -> train/val`, `n >= 10 -> full v2 rule`

## 2. Split Sizes

| split          |   rows |   percent |
|:---------------|-------:|----------:|
| train          |   7212 |     68.28 |
| val            |   1186 |     11.23 |
| test_real      |    385 |      3.65 |
| test_mixed     |   1059 |     10.03 |
| test_challenge |    720 |      6.82 |

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
|       0 | external_curated        | P2P hard negative          |  501 |     351 |    50 |           0 |           50 |               50 | full_rule            |
|       0 | external_real           | P2P hội thoại thông thường |  500 |     350 |    50 |           0 |           50 |               50 | full_rule            |
|       1 | paraphrased             | BHXH / Trợ cấp giả         |  587 |     451 |    59 |           0 |           59 |               18 | full_rule            |
|       1 | paraphrased             | Crypto / Đầu tư giả        |  625 |     482 |    62 |           0 |           62 |               19 | full_rule            |
|       1 | paraphrased             | Cờ bạc / Betting           |  618 |     475 |    62 |           0 |           62 |               19 | full_rule            |
|       1 | paraphrased             | Dịch vụ công giả           |  474 |     366 |    47 |           0 |           47 |               14 | full_rule            |
|       1 | paraphrased             | Giả mạo ngân hàng          |  386 |     296 |    39 |           0 |           39 |               12 | full_rule            |
|       1 | paraphrased             | Nội dung nhạy cảm          |  621 |     478 |    62 |           0 |           62 |               19 | full_rule            |
|       1 | paraphrased             | Tuyển dụng giả             |  595 |     457 |    60 |           0 |           60 |               18 | full_rule            |
|       1 | paraphrased             | Đòi nợ / Đe dọa            |  427 |     328 |    43 |           0 |           43 |               13 | full_rule            |
|       0 | real                    | Dịch vụ công thật          |  170 |      84 |    26 |          26 |           17 |               17 | full_rule            |
|       0 | real                    | Dịch vụ y tế               |    2 |       2 |     0 |           0 |            0 |                0 | all_train            |
|       0 | real                    | Khác                       |  507 |     253 |    76 |          76 |           51 |               51 | full_rule            |
|       0 | real                    | Ngân hàng thật             |  126 |      62 |    19 |          19 |           13 |               13 | full_rule            |
|       0 | real                    | Quảng cáo hợp lệ           |  136 |      68 |    20 |          20 |           14 |               14 | full_rule            |
|       0 | real                    | Thương mại điện tử         |    1 |       1 |     0 |           0 |            0 |                0 | all_train            |
|       0 | real                    | Tin nhắn cá nhân và OTP    |  301 |     151 |    45 |          45 |           30 |               30 | full_rule            |
|       0 | real                    | Viễn thông                 | 1060 |     530 |   159 |         159 |          106 |              106 | full_rule            |
|       0 | real                    | Vận chuyển                 |   18 |       8 |     3 |           3 |            2 |                2 | full_rule            |
|       1 | real                    | BHXH / Trợ cấp giả         |   15 |       7 |     2 |           2 |            2 |                2 | full_rule            |
|       1 | real                    | Crypto / Đầu tư giả        |    2 |       2 |     0 |           0 |            0 |                0 | all_train            |
|       1 | real                    | Cờ bạc / Betting           |   53 |      27 |     8 |           8 |            5 |                5 | full_rule            |
|       1 | real                    | Dịch vụ công giả           |   16 |       8 |     2 |           2 |            2 |                2 | full_rule            |
|       1 | real                    | Giả mạo ngân hàng          |   65 |      33 |    10 |          10 |            6 |                6 | full_rule            |
|       1 | real                    | Khác                       |   46 |      22 |     7 |           7 |            5 |                5 | full_rule            |
|       1 | real                    | Nội dung nhạy cảm          |   10 |       4 |     2 |           2 |            1 |                1 | full_rule            |
|       1 | real                    | Tuyển dụng giả             |   27 |      13 |     4 |           4 |            3 |                3 | full_rule            |
|       1 | real                    | Đòi nợ / Đe dọa            |   12 |       6 |     2 |           2 |            1 |                1 | full_rule            |
|       0 | synthetic               | Dịch vụ công thật          |  195 |     145 |    20 |           0 |           20 |               10 | full_rule            |
|       0 | synthetic               | Dịch vụ y tế               |  206 |     154 |    21 |           0 |           21 |               10 | full_rule            |
|       0 | synthetic               | Ngân hàng thật             |  306 |     229 |    31 |           0 |           31 |               15 | full_rule            |
|       0 | synthetic               | Quảng cáo hợp lệ           |  226 |     169 |    23 |           0 |           23 |               11 | full_rule            |
|       0 | synthetic               | Thương mại điện tử         |  252 |     189 |    25 |           0 |           25 |               13 | full_rule            |
|       0 | synthetic               | Tin nhắn cá nhân và OTP    |  353 |     265 |    35 |           0 |           35 |               18 | full_rule            |
|       0 | synthetic               | Viễn thông                 |  196 |     146 |    20 |           0 |           20 |               10 | full_rule            |
|       0 | synthetic               | Vận chuyển                 |  264 |     199 |    26 |           0 |           26 |               13 | full_rule            |
|       1 | synthetic               | BHXH / Trợ cấp giả         |    2 |       2 |     0 |           0 |            0 |                0 | all_train            |
|       1 | synthetic               | Dịch vụ công giả           |    2 |       2 |     0 |           0 |            0 |                0 | all_train            |
|       1 | synthetic               | Giả mạo ngân hàng          |    1 |       1 |     0 |           0 |            0 |                0 | all_train            |
|       1 | synthetic               | Nội dung nhạy cảm          |    3 |       3 |     0 |           0 |            0 |                0 | all_train            |
|       1 | synthetic               | Tuyển dụng giả             |    1 |       1 |     0 |           0 |            0 |                0 | all_train            |
|       1 | synthetic               | Đòi nợ / Đe dọa            |    1 |       1 |     0 |           0 |            0 |                0 | all_train            |
|       1 | synthetic_hard_negative | BHXH / Trợ cấp giả         |   60 |      36 |     6 |           0 |            6 |               12 | full_rule            |
|       1 | synthetic_hard_negative | Crypto / Đầu tư giả        |   11 |       7 |     1 |           0 |            1 |                2 | full_rule            |
|       1 | synthetic_hard_negative | Dịch vụ công giả           |   79 |      47 |     8 |           0 |            8 |               16 | full_rule            |
|       1 | synthetic_hard_negative | Giả mạo ngân hàng          |   76 |      45 |     8 |           0 |            8 |               15 | full_rule            |
|       1 | synthetic_hard_negative | Khác                       |  282 |     170 |    28 |           0 |           28 |               56 | full_rule            |
|       1 | synthetic_hard_negative | Tuyển dụng giả             |   86 |      51 |     9 |           0 |            9 |               17 | full_rule            |
|       1 | synthetic_hard_negative | Đòi nợ / Đe dọa            |   59 |      35 |     6 |           0 |            6 |               12 | full_rule            |

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

Rows: `7212`

### Label Distribution

|   label |   count |   percent |
|--------:|--------:|----------:|
|       1 |    3856 |     53.47 |
|       0 |    3356 |     46.53 |

### Data Origin Distribution

| data_origin             |   count |   percent |
|:------------------------|--------:|----------:|
| paraphrased             |    3333 |     46.21 |
| synthetic               |    1506 |     20.88 |
| real                    |    1281 |     17.76 |
| synthetic_hard_negative |     391 |      5.42 |
| external_curated        |     351 |      4.87 |
| external_real           |     350 |      4.85 |

### Category Distribution

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

### Sender Type Distribution

| sender_type     |   count |   percent |
|:----------------|--------:|----------:|
| personal_number |    3791 |     52.57 |
| brandname       |    2714 |     37.63 |
| shortcode       |     707 |      9.8  |

### URL Flag x Label

|   has_url |    0 |    1 |
|----------:|-----:|-----:|
|         0 | 2544 | 1220 |
|         1 |  812 | 2636 |

### Phone Flag x Label

|   has_phone_number |    0 |    1 |
|-------------------:|-----:|-----:|
|                  0 | 2568 | 2745 |
|                  1 |  788 | 1111 |

### Label x Data Origin

| data_origin             |    0 |    1 |
|:------------------------|-----:|-----:|
| external_curated        |  351 |    0 |
| external_real           |  350 |    0 |
| paraphrased             |    0 | 3333 |
| real                    | 1159 |  122 |
| synthetic               | 1496 |   10 |
| synthetic_hard_negative |    0 |  391 |

### Label x Category

| category                   |   0 |   1 |
|:---------------------------|----:|----:|
| BHXH / Trợ cấp giả         |   0 | 496 |
| Crypto / Đầu tư giả        |   0 | 491 |
| Cờ bạc / Betting           |   0 | 502 |
| Dịch vụ công giả           |   0 | 423 |
| Dịch vụ công thật          | 229 |   0 |
| Dịch vụ y tế               | 156 |   0 |
| Giả mạo ngân hàng          |   0 | 375 |
| Khác                       | 253 | 192 |
| Ngân hàng thật             | 291 |   0 |
| Nội dung nhạy cảm          |   0 | 485 |
| P2P hard negative          | 351 |   0 |
| P2P hội thoại thông thường | 350 |   0 |
| Quảng cáo hợp lệ           | 237 |   0 |
| Thương mại điện tử         | 190 |   0 |
| Tin nhắn cá nhân và OTP    | 416 |   0 |
| Tuyển dụng giả             |   0 | 522 |
| Viễn thông                 | 676 |   0 |
| Vận chuyển                 | 207 |   0 |
| Đòi nợ / Đe dọa            |   0 | 370 |

### Data Origin x Category

| data_origin             |   BHXH / Trợ cấp giả |   Crypto / Đầu tư giả |   Cờ bạc / Betting |   Dịch vụ công giả |   Dịch vụ công thật |   Dịch vụ y tế |   Giả mạo ngân hàng |   Khác |   Ngân hàng thật |   Nội dung nhạy cảm |   P2P hard negative |   P2P hội thoại thông thường |   Quảng cáo hợp lệ |   Thương mại điện tử |   Tin nhắn cá nhân và OTP |   Tuyển dụng giả |   Viễn thông |   Vận chuyển |   Đòi nợ / Đe dọa |
|:------------------------|---------------------:|----------------------:|-------------------:|-------------------:|--------------------:|---------------:|--------------------:|-------:|-----------------:|--------------------:|--------------------:|-----------------------------:|-------------------:|---------------------:|--------------------------:|-----------------:|-------------:|-------------:|------------------:|
| external_curated        |                    0 |                     0 |                  0 |                  0 |                   0 |              0 |                   0 |      0 |                0 |                   0 |                 351 |                            0 |                  0 |                    0 |                         0 |                0 |            0 |            0 |                 0 |
| external_real           |                    0 |                     0 |                  0 |                  0 |                   0 |              0 |                   0 |      0 |                0 |                   0 |                   0 |                          350 |                  0 |                    0 |                         0 |                0 |            0 |            0 |                 0 |
| paraphrased             |                  451 |                   482 |                475 |                366 |                   0 |              0 |                 296 |      0 |                0 |                 478 |                   0 |                            0 |                  0 |                    0 |                         0 |              457 |            0 |            0 |               328 |
| real                    |                    7 |                     2 |                 27 |                  8 |                  84 |              2 |                  33 |    275 |               62 |                   4 |                   0 |                            0 |                 68 |                    1 |                       151 |               13 |          530 |            8 |                 6 |
| synthetic               |                    2 |                     0 |                  0 |                  2 |                 145 |            154 |                   1 |      0 |              229 |                   3 |                   0 |                            0 |                169 |                  189 |                       265 |                1 |          146 |          199 |                 1 |
| synthetic_hard_negative |                   36 |                     7 |                  0 |                 47 |                   0 |              0 |                  45 |    170 |                0 |                   0 |                   0 |                            0 |                  0 |                    0 |                         0 |               51 |            0 |            0 |                35 |

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
| synthetic_hard_negative |      66 |      5.56 |
| external_curated        |      50 |      4.22 |
| external_real           |      50 |      4.22 |

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
| P2P hard negative          |      50 |      4.22 |
| Ngân hàng thật             |      50 |      4.22 |
| P2P hội thoại thông thường |      50 |      4.22 |
| Dịch vụ công thật          |      46 |      3.88 |
| Quảng cáo hợp lệ           |      43 |      3.63 |
| Vận chuyển                 |      29 |      2.45 |
| Thương mại điện tử         |      25 |      2.11 |
| Dịch vụ y tế               |      21 |      1.77 |

### Sender Type Distribution

| sender_type     |   count |   percent |
|:----------------|--------:|----------:|
| personal_number |     537 |     45.28 |
| brandname       |     517 |     43.59 |
| shortcode       |     132 |     11.13 |

### URL Flag x Label

|   has_url |   0 |   1 |
|----------:|----:|----:|
|         0 | 445 | 177 |
|         1 | 204 | 360 |

### Phone Flag x Label

|   has_phone_number |   0 |   1 |
|-------------------:|----:|----:|
|                  0 | 471 | 377 |
|                  1 | 178 | 160 |

### Label x Data Origin

| data_origin             |   0 |   1 |
|:------------------------|----:|----:|
| external_curated        |  50 |   0 |
| external_real           |  50 |   0 |
| paraphrased             |   0 | 434 |
| real                    | 348 |  37 |
| synthetic               | 201 |   0 |
| synthetic_hard_negative |   0 |  66 |

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
| synthetic_hard_negative |                    6 |                     1 |                  0 |                  8 |                   0 |              0 |                   8 |     28 |                0 |                   0 |                   0 |                            0 |                  0 |                    0 |                         0 |                9 |            0 |            0 |                 6 |

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
| Dịch vụ công giả        |       2 |      0.52 |
| BHXH / Trợ cấp giả      |       2 |      0.52 |
| Đòi nợ / Đe dọa         |       2 |      0.52 |

### Sender Type Distribution

| sender_type     |   count |   percent |
|:----------------|--------:|----------:|
| brandname       |     277 |     71.95 |
| shortcode       |      70 |     18.18 |
| personal_number |      38 |      9.87 |

### URL Flag x Label

|   has_url |   0 |   1 |
|----------:|----:|----:|
|         0 | 168 |   9 |
|         1 | 180 |  28 |

### Phone Flag x Label

|   has_phone_number |   0 |   1 |
|-------------------:|----:|----:|
|                  0 | 198 |  26 |
|                  1 | 150 |  11 |

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

Rows: `1059`

### Label Distribution

|   label |   count |   percent |
|--------:|--------:|----------:|
|       0 |     534 |     50.42 |
|       1 |     525 |     49.58 |

### Data Origin Distribution

| data_origin             |   count |   percent |
|:------------------------|--------:|----------:|
| paraphrased             |     434 |     40.98 |
| real                    |     258 |     24.36 |
| synthetic               |     201 |     18.98 |
| synthetic_hard_negative |      66 |      6.23 |
| external_real           |      50 |      4.72 |
| external_curated        |      50 |      4.72 |

### Category Distribution

| category                   |   count |   percent |
|:---------------------------|--------:|----------:|
| Viễn thông                 |     126 |     11.9  |
| Khác                       |      84 |      7.93 |
| Tuyển dụng giả             |      72 |      6.8  |
| Cờ bạc / Betting           |      67 |      6.33 |
| BHXH / Trợ cấp giả         |      67 |      6.33 |
| Tin nhắn cá nhân và OTP    |      65 |      6.14 |
| Crypto / Đầu tư giả        |      63 |      5.95 |
| Nội dung nhạy cảm          |      63 |      5.95 |
| Dịch vụ công giả           |      57 |      5.38 |
| Giả mạo ngân hàng          |      53 |      5    |
| Đòi nợ / Đe dọa            |      50 |      4.72 |
| P2P hội thoại thông thường |      50 |      4.72 |
| P2P hard negative          |      50 |      4.72 |
| Ngân hàng thật             |      44 |      4.15 |
| Dịch vụ công thật          |      37 |      3.49 |
| Quảng cáo hợp lệ           |      37 |      3.49 |
| Vận chuyển                 |      28 |      2.64 |
| Thương mại điện tử         |      25 |      2.36 |
| Dịch vụ y tế               |      21 |      1.98 |

### Sender Type Distribution

| sender_type     |   count |   percent |
|:----------------|--------:|----------:|
| personal_number |     518 |     48.91 |
| brandname       |     443 |     41.83 |
| shortcode       |      98 |      9.25 |

### URL Flag x Label

|   has_url |   0 |   1 |
|----------:|----:|----:|
|         0 | 387 | 181 |
|         1 | 147 | 344 |

### Phone Flag x Label

|   has_phone_number |   0 |   1 |
|-------------------:|----:|----:|
|                  0 | 408 | 369 |
|                  1 | 126 | 156 |

### Label x Data Origin

| data_origin             |   0 |   1 |
|:------------------------|----:|----:|
| external_curated        |  50 |   0 |
| external_real           |  50 |   0 |
| paraphrased             |   0 | 434 |
| real                    | 233 |  25 |
| synthetic               | 201 |   0 |
| synthetic_hard_negative |   0 |  66 |

### Label x Category

| category                   |   0 |   1 |
|:---------------------------|----:|----:|
| BHXH / Trợ cấp giả         |   0 |  67 |
| Crypto / Đầu tư giả        |   0 |  63 |
| Cờ bạc / Betting           |   0 |  67 |
| Dịch vụ công giả           |   0 |  57 |
| Dịch vụ công thật          |  37 |   0 |
| Dịch vụ y tế               |  21 |   0 |
| Giả mạo ngân hàng          |   0 |  53 |
| Khác                       |  51 |  33 |
| Ngân hàng thật             |  44 |   0 |
| Nội dung nhạy cảm          |   0 |  63 |
| P2P hard negative          |  50 |   0 |
| P2P hội thoại thông thường |  50 |   0 |
| Quảng cáo hợp lệ           |  37 |   0 |
| Thương mại điện tử         |  25 |   0 |
| Tin nhắn cá nhân và OTP    |  65 |   0 |
| Tuyển dụng giả             |   0 |  72 |
| Viễn thông                 | 126 |   0 |
| Vận chuyển                 |  28 |   0 |
| Đòi nợ / Đe dọa            |   0 |  50 |

### Data Origin x Category

| data_origin             |   BHXH / Trợ cấp giả |   Crypto / Đầu tư giả |   Cờ bạc / Betting |   Dịch vụ công giả |   Dịch vụ công thật |   Dịch vụ y tế |   Giả mạo ngân hàng |   Khác |   Ngân hàng thật |   Nội dung nhạy cảm |   P2P hard negative |   P2P hội thoại thông thường |   Quảng cáo hợp lệ |   Thương mại điện tử |   Tin nhắn cá nhân và OTP |   Tuyển dụng giả |   Viễn thông |   Vận chuyển |   Đòi nợ / Đe dọa |
|:------------------------|---------------------:|----------------------:|-------------------:|-------------------:|--------------------:|---------------:|--------------------:|-------:|-----------------:|--------------------:|--------------------:|-----------------------------:|-------------------:|---------------------:|--------------------------:|-----------------:|-------------:|-------------:|------------------:|
| external_curated        |                    0 |                     0 |                  0 |                  0 |                   0 |              0 |                   0 |      0 |                0 |                   0 |                  50 |                            0 |                  0 |                    0 |                         0 |                0 |            0 |            0 |                 0 |
| external_real           |                    0 |                     0 |                  0 |                  0 |                   0 |              0 |                   0 |      0 |                0 |                   0 |                   0 |                           50 |                  0 |                    0 |                         0 |                0 |            0 |            0 |                 0 |
| paraphrased             |                   59 |                    62 |                 62 |                 47 |                   0 |              0 |                  39 |      0 |                0 |                  62 |                   0 |                            0 |                  0 |                    0 |                         0 |               60 |            0 |            0 |                43 |
| real                    |                    2 |                     0 |                  5 |                  2 |                  17 |              0 |                   6 |     56 |               13 |                   1 |                   0 |                            0 |                 14 |                    0 |                        30 |                3 |          106 |            2 |                 1 |
| synthetic               |                    0 |                     0 |                  0 |                  0 |                  20 |             21 |                   0 |      0 |               31 |                   0 |                   0 |                            0 |                 23 |                   25 |                        35 |                0 |           20 |           26 |                 0 |
| synthetic_hard_negative |                    6 |                     1 |                  0 |                  8 |                   0 |              0 |                   8 |     28 |                0 |                   0 |                   0 |                            0 |                  0 |                    0 |                         0 |                9 |            0 |            0 |                 6 |

## 7. Split Detail: `test_challenge`

Rows: `720`

### Label Distribution

|   label |   count |   percent |
|--------:|--------:|----------:|
|       0 |     433 |     60.14 |
|       1 |     287 |     39.86 |

### Data Origin Distribution

| data_origin             |   count |   percent |
|:------------------------|--------:|----------:|
| real                    |     258 |     35.83 |
| paraphrased             |     132 |     18.33 |
| synthetic_hard_negative |     130 |     18.06 |
| synthetic               |     100 |     13.89 |
| external_curated        |      50 |      6.94 |
| external_real           |      50 |      6.94 |

### Category Distribution

| category                   |   count |   percent |
|:---------------------------|--------:|----------:|
| Viễn thông                 |     116 |     16.11 |
| Khác                       |     112 |     15.56 |
| P2P hard negative          |      50 |      6.94 |
| P2P hội thoại thông thường |      50 |      6.94 |
| Tin nhắn cá nhân và OTP    |      48 |      6.67 |
| Tuyển dụng giả             |      38 |      5.28 |
| Giả mạo ngân hàng          |      33 |      4.58 |
| BHXH / Trợ cấp giả         |      32 |      4.44 |
| Dịch vụ công giả           |      32 |      4.44 |
| Ngân hàng thật             |      28 |      3.89 |
| Dịch vụ công thật          |      27 |      3.75 |
| Đòi nợ / Đe dọa            |      26 |      3.61 |
| Quảng cáo hợp lệ           |      25 |      3.47 |
| Cờ bạc / Betting           |      24 |      3.33 |
| Crypto / Đầu tư giả        |      21 |      2.92 |
| Nội dung nhạy cảm          |      20 |      2.78 |
| Vận chuyển                 |      15 |      2.08 |
| Thương mại điện tử         |      13 |      1.81 |
| Dịch vụ y tế               |      10 |      1.39 |

### Sender Type Distribution

| sender_type     |   count |   percent |
|:----------------|--------:|----------:|
| brandname       |     366 |     50.83 |
| personal_number |     277 |     38.47 |
| shortcode       |      77 |     10.69 |

### URL Flag x Label

|   has_url |   0 |   1 |
|----------:|----:|----:|
|         0 | 292 | 164 |
|         1 | 141 | 123 |

### Phone Flag x Label

|   has_phone_number |   0 |   1 |
|-------------------:|----:|----:|
|                  0 | 305 | 184 |
|                  1 | 128 | 103 |

### Label x Data Origin

| data_origin             |   0 |   1 |
|:------------------------|----:|----:|
| external_curated        |  50 |   0 |
| external_real           |  50 |   0 |
| paraphrased             |   0 | 132 |
| real                    | 233 |  25 |
| synthetic               | 100 |   0 |
| synthetic_hard_negative |   0 | 130 |

### Label x Category

| category                   |   0 |   1 |
|:---------------------------|----:|----:|
| BHXH / Trợ cấp giả         |   0 |  32 |
| Crypto / Đầu tư giả        |   0 |  21 |
| Cờ bạc / Betting           |   0 |  24 |
| Dịch vụ công giả           |   0 |  32 |
| Dịch vụ công thật          |  27 |   0 |
| Dịch vụ y tế               |  10 |   0 |
| Giả mạo ngân hàng          |   0 |  33 |
| Khác                       |  51 |  61 |
| Ngân hàng thật             |  28 |   0 |
| Nội dung nhạy cảm          |   0 |  20 |
| P2P hard negative          |  50 |   0 |
| P2P hội thoại thông thường |  50 |   0 |
| Quảng cáo hợp lệ           |  25 |   0 |
| Thương mại điện tử         |  13 |   0 |
| Tin nhắn cá nhân và OTP    |  48 |   0 |
| Tuyển dụng giả             |   0 |  38 |
| Viễn thông                 | 116 |   0 |
| Vận chuyển                 |  15 |   0 |
| Đòi nợ / Đe dọa            |   0 |  26 |

### Data Origin x Category

| data_origin             |   BHXH / Trợ cấp giả |   Crypto / Đầu tư giả |   Cờ bạc / Betting |   Dịch vụ công giả |   Dịch vụ công thật |   Dịch vụ y tế |   Giả mạo ngân hàng |   Khác |   Ngân hàng thật |   Nội dung nhạy cảm |   P2P hard negative |   P2P hội thoại thông thường |   Quảng cáo hợp lệ |   Thương mại điện tử |   Tin nhắn cá nhân và OTP |   Tuyển dụng giả |   Viễn thông |   Vận chuyển |   Đòi nợ / Đe dọa |
|:------------------------|---------------------:|----------------------:|-------------------:|-------------------:|--------------------:|---------------:|--------------------:|-------:|-----------------:|--------------------:|--------------------:|-----------------------------:|-------------------:|---------------------:|--------------------------:|-----------------:|-------------:|-------------:|------------------:|
| external_curated        |                    0 |                     0 |                  0 |                  0 |                   0 |              0 |                   0 |      0 |                0 |                   0 |                  50 |                            0 |                  0 |                    0 |                         0 |                0 |            0 |            0 |                 0 |
| external_real           |                    0 |                     0 |                  0 |                  0 |                   0 |              0 |                   0 |      0 |                0 |                   0 |                   0 |                           50 |                  0 |                    0 |                         0 |                0 |            0 |            0 |                 0 |
| paraphrased             |                   18 |                    19 |                 19 |                 14 |                   0 |              0 |                  12 |      0 |                0 |                  19 |                   0 |                            0 |                  0 |                    0 |                         0 |               18 |            0 |            0 |                13 |
| real                    |                    2 |                     0 |                  5 |                  2 |                  17 |              0 |                   6 |     56 |               13 |                   1 |                   0 |                            0 |                 14 |                    0 |                        30 |                3 |          106 |            2 |                 1 |
| synthetic               |                    0 |                     0 |                  0 |                  0 |                  10 |             10 |                   0 |      0 |               15 |                   0 |                   0 |                            0 |                 11 |                   13 |                        18 |                0 |           10 |           13 |                 0 |
| synthetic_hard_negative |                   12 |                     2 |                  0 |                 16 |                   0 |              0 |                  15 |     56 |                0 |                   0 |                   0 |                            0 |                  0 |                    0 |                         0 |               17 |            0 |            0 |                12 |

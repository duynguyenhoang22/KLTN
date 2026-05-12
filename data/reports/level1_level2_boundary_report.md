# LEVEL 1 vs LEVEL 2 Boundary Analysis

## Purpose

Put repaired `LEVEL 2` beside current `LEVEL 1` to check whether the boundary is coherent.

Expected boundary:

- `LEVEL 1`: sparse intentional homoglyphs, mostly 1-2 sensitive terms, little secondary camouflage.
- `LEVEL 2`: stronger sensitive-word-focused leet, plus camouflage such as casing/separators/accent loss. Whole-sentence leet should be minority behavior.

## Row Counts

| category            |   LEVEL 1 – Leet nhẹ (thay 1-2 ký tự) |   LEVEL 2 – Leet nặng + tên riêng |
|:--------------------|--------------------------------------:|----------------------------------:|
| BHXH / Trợ cấp      |                                   209 |                               467 |
| Crypto / Đầu tư giả |                                    13 |                               540 |
| Cờ bạc / Betting    |                                    12 |                               537 |
| Dịch vụ công giả    |                                    92 |                               364 |
| Giả mạo ngân hàng   |                                    98 |                               318 |
| Nội dung nhạy cảm   |                                     0 |                                 1 |
| Tuyển dụng giả      |                                   142 |                               279 |
| Đòi nợ / Đe dọa     |                                    85 |                               141 |

## Metric Summary by Level

| level                               |   ('token_count', 'mean') |   ('token_count', 'median') |   ('leet_token_count', 'mean') |   ('leet_token_count', 'median') |   ('leet_token_ratio', 'mean') |   ('leet_token_ratio', 'median') |   ('sensitive_token_count', 'mean') |   ('sensitive_token_count', 'median') |   ('leet_sensitive_token_count', 'mean') |   ('leet_sensitive_token_count', 'median') |   ('sensitive_leet_coverage', 'mean') |   ('sensitive_leet_coverage', 'median') |   ('nonsensitive_leet_token_count', 'mean') |   ('nonsensitive_leet_token_count', 'median') |   ('nonsensitive_leet_ratio', 'mean') |   ('nonsensitive_leet_ratio', 'median') |   ('separator_token_count', 'mean') |   ('separator_token_count', 'median') |   ('mid_upper_count', 'mean') |   ('mid_upper_count', 'median') |   ('digit_ratio', 'mean') |   ('digit_ratio', 'median') |   ('symbol_ratio', 'mean') |   ('symbol_ratio', 'median') |   ('diacritic_count', 'mean') |   ('diacritic_count', 'median') |
|:------------------------------------|--------------------------:|----------------------------:|-------------------------------:|---------------------------------:|-------------------------------:|---------------------------------:|------------------------------------:|--------------------------------------:|-----------------------------------------:|-------------------------------------------:|--------------------------------------:|----------------------------------------:|--------------------------------------------:|----------------------------------------------:|--------------------------------------:|----------------------------------------:|------------------------------------:|--------------------------------------:|------------------------------:|--------------------------------:|--------------------------:|----------------------------:|---------------------------:|-----------------------------:|------------------------------:|--------------------------------:|
| LEVEL 1 – Leet nhẹ (thay 1-2 ký tự) |                    21.897 |                          21 |                          5.687 |                                5 |                          0.256 |                             0.25 |                               3.748 |                                     4 |                                    1.72  |                                          2 |                                 0.469 |                                     0.5 |                                       3.966 |                                             3 |                                 0.174 |                                   0.167 |                               1.238 |                                     1 |                         0.066 |                               0 |                     0.139 |                       0.11  |                      0.093 |                        0.088 |                         0.146 |                               0 |
| LEVEL 2 – Leet nặng + tên riêng     |                    18.689 |                          18 |                          8.903 |                                8 |                          0.485 |                             0.5  |                               2.724 |                                     3 |                                    1.621 |                                          2 |                                 0.534 |                                     0.5 |                                       7.283 |                                             6 |                                 0.394 |                                   0.389 |                               1.862 |                                     1 |                         0.053 |                               0 |                     0.199 |                       0.194 |                      0.116 |                        0.099 |                         0.188 |                               0 |

## Mean Metrics by Category and Level

| category            | level                               |   leet_token_ratio |   sensitive_leet_coverage |   nonsensitive_leet_ratio |   separator_token_count |
|:--------------------|:------------------------------------|-------------------:|--------------------------:|--------------------------:|------------------------:|
| BHXH / Trợ cấp      | LEVEL 1 – Leet nhẹ (thay 1-2 ký tự) |              0.131 |                     0.344 |                     0.067 |                   2.019 |
| BHXH / Trợ cấp      | LEVEL 2 – Leet nặng + tên riêng     |              0.326 |                     0.49  |                     0.221 |                   4.296 |
| Crypto / Đầu tư giả | LEVEL 1 – Leet nhẹ (thay 1-2 ký tự) |              0.269 |                     0.442 |                     0.214 |                   0.692 |
| Crypto / Đầu tư giả | LEVEL 2 – Leet nặng + tên riêng     |              0.551 |                     0.624 |                     0.478 |                   1.7   |
| Cờ bạc / Betting    | LEVEL 1 – Leet nhẹ (thay 1-2 ký tự) |              0.36  |                     0.358 |                     0.254 |                   0.833 |
| Cờ bạc / Betting    | LEVEL 2 – Leet nặng + tên riêng     |              0.566 |                     0.517 |                     0.434 |                   2.108 |
| Dịch vụ công giả    | LEVEL 1 – Leet nhẹ (thay 1-2 ký tự) |              0.265 |                     0.509 |                     0.183 |                   0.185 |
| Dịch vụ công giả    | LEVEL 2 – Leet nặng + tên riêng     |              0.433 |                     0.55  |                     0.362 |                   0.31  |
| Giả mạo ngân hàng   | LEVEL 1 – Leet nhẹ (thay 1-2 ký tự) |              0.334 |                     0.52  |                     0.226 |                   0.02  |
| Giả mạo ngân hàng   | LEVEL 2 – Leet nặng + tên riêng     |              0.404 |                     0.48  |                     0.301 |                   0.17  |
| Nội dung nhạy cảm   | LEVEL 2 – Leet nặng + tên riêng     |              0.231 |                     0     |                     0.231 |                   0     |
| Tuyển dụng giả      | LEVEL 1 – Leet nhẹ (thay 1-2 ký tự) |              0.282 |                     0.495 |                     0.19  |                   1.915 |
| Tuyển dụng giả      | LEVEL 2 – Leet nặng + tên riêng     |              0.602 |                     0.374 |                     0.566 |                   1.961 |
| Đòi nợ / Đe dọa     | LEVEL 1 – Leet nhẹ (thay 1-2 ký tự) |              0.403 |                     0.651 |                     0.325 |                   0.871 |
| Đòi nợ / Đe dọa     | LEVEL 2 – Leet nặng + tên riêng     |              0.532 |                     0.802 |                     0.439 |                   1.121 |

## Boundary Flags

| level                               |   level1_too_heavy |   level2_separator_dominant |   level2_still_overleeted |   level2_too_mild |   ok |
|:------------------------------------|-------------------:|----------------------------:|--------------------------:|------------------:|-----:|
| LEVEL 1 – Leet nhẹ (thay 1-2 ký tự) |                218 |                           0 |                         0 |                 0 |  433 |
| LEVEL 2 – Leet nặng + tên riêng     |                  0 |                         498 |                        92 |               134 | 1923 |

Flag definitions:

- `level1_too_heavy`: LEVEL 1 has high leet density or many non-sensitive leet tokens.
- `level2_too_mild`: LEVEL 2 has low leet density and weak sensitive-term obfuscation.
- `level2_still_overleeted`: LEVEL 2 remains dominated by non-sensitive leet.
- `level2_separator_dominant`: LEVEL 2 may behave more like separator/special-char levels.

## Key Interpretation

- If `LEVEL 2` mean leet density remains clearly above `LEVEL 1`, the repair preserved a useful severity gap.
- If many `LEVEL 1` rows are flagged as too heavy, the main remaining issue is not only LEVEL 2. LEVEL 1 may also need a softening pass or metadata relabeling.
- If `LEVEL 2` has high sensitive-term coverage but only moderate non-sensitive leet, the repaired style matches the intended targeted-obfuscation definition.
- Rows in the borderline CSV should be manually reviewed before any second correction pass.

## Example Borderline Rows

### level1_too_heavy

- row 3740 | Đòi nợ / Đe dọa | leet_ratio=0.64 | sensitive_coverage=0.67: [CANH CAO LAN CUOI]: Ph4m V4n M1nh CMND 281234567 n0 3.125.400VND t41 FE Cred1t. Truoc 24H nu4 khong th4nh t04n se gu1 v4n ban v3 d14 phu0ng v4 n13m y3t h1nh 4nh. LH Zalo: 0911998877.
- row 3975 | Giả mạo ngân hàng | leet_ratio=0.59 | sensitive_coverage=0.67: MB B4NK: Canh b4o r0 r1 thong t1n th3 t1n dung. Dang nh4p mbbank.vn-0nline.top de kh04 th3 ngay.
- row 3631 | Dịch vụ công giả | leet_ratio=0.58 | sensitive_coverage=1.00: Bo C0ng 4n: L3nh t4m g1am da duoc f3 duy3t. Lien he: 0912233445
- row 3645 | Dịch vụ công giả | leet_ratio=0.58 | sensitive_coverage=1.00: Bo C0ng 4n: L3nh b4t g14m da duoc f3 zuy3t. Lien he 0777445566
- row 989 | Giả mạo ngân hàng | leet_ratio=0.57 | sensitive_coverage=0.67: VIETCOMBANK: d13m t1ch luy se h3t han. Vui l0ng d01 thu0ng t41 vietcombank.vn-io.top truoc 24h.

### level2_too_mild

- row 1 | BHXH / Trợ cấp | leet_ratio=0.25 | sensitive_coverage=0.50: Ong (Ba) da du d!eu k1en NH4N T1EN ho tro tu wy BHTN. Bam vao www.qpwnm.icu de l4y. QUA HAN KHONG DUOC CHAP NHAN. aS9k
- row 8 | BHXH / Trợ cấp | leet_ratio=0.25 | sensitive_coverage=0.40: Quyet dinh BHXH: Ban da du d!eu k1en nh4n t1en BHTN. Bam vao www.rfvbg.icu. QUA HAN KHONG DUOC CHAP NHAN. vB7n
- row 44 | BHXH / Trợ cấp | leet_ratio=0.25 | sensitive_coverage=0.40: Quyet dinh BHXH: ong (B4) da du d!eu k1en nh4n t1en tu quy BHTN. Bam vao www.mnpqr.icu. QUA HAN SE KHONG DUOC CHAP NHAN! pL0s
- row 254 | BHXH / Trợ cấp | leet_ratio=0.25 | sensitive_coverage=0.40: BHXH: Ong (Ba) da du d!eu k1en nh4n t1en h0 tro tu wuy BHTN. Bam vao www.asdfgh.icu. QUA HAN SE KHONG DUOC CHAP NHAN! mS8s
- row 128 | Giả mạo ngân hàng | leet_ratio=0.25 | sensitive_coverage=0.67: [BIDV] TAI-kh04n-cua-ban-da-bi-kh04. Vu1-l0ng-nh4n-v40-bidv.vn-home.top-d3-m0-kh04-ng4y.

### level2_still_overleeted

- row 1662 | Cờ bạc / Betting | leet_ratio=1.00 | sensitive_coverage=0.00: 8D4Y_Tuy3n-CTV_Ch13t-kh4u-C40! Z4lo: 0922889900. L1nk: 8dag.vip
- row 1051 | Cờ bạc / Betting | leet_ratio=0.91 | sensitive_coverage=0.67: 789B3t c4s1n0, x0 s0, ch01 g4. Rut t1en s13u t0c. L!nk: k12js.com
- row 4739 | Cờ bạc / Betting | leet_ratio=0.90 | sensitive_coverage=0.00: 789B3t tuy3n d41 ly. H04 h0ng mo1 th4ng. Z4l0: 0977889900. L1nk: 789b.vip
- row 4757 | Cờ bạc / Betting | leet_ratio=0.88 | sensitive_coverage=0.00: V7B3t tuy3n d41 ly h04 h0ng 45%. Z4l0: 0900112233. L1nk: v7v7.vip
- row 1658 | Cờ bạc / Betting | leet_ratio=0.88 | sensitive_coverage=0.00: 789B3t_Tuy3n-D41_Ly-H04-h0ng-50%_L1nk: 789ag.bet, Z4lo: 0944112233

### level2_separator_dominant

- row 3231 | Cờ bạc / Betting | leet_ratio=1.00 | sensitive_coverage=1.00: V7B3t_rut-t13n^s!3u-t0c. B4cc4r4t-Ch0i_g4-Th3_th40. DK_nh4n-88k: v7win.vip/aK5jH
- row 4259 | Crypto / Đầu tư giả | leet_ratio=1.00 | sensitive_coverage=0.00: C0py tr4z3 f0r3x l01 n-h-u4n c-a-0, r-u1 r0 t-h-4-p. J140 v13n h-u0nz z4n c-u-c k-y t-h-@-n t-h!3n. t.me/forex_master_vn
- row 4688 | Cờ bạc / Betting | leet_ratio=0.92 | sensitive_coverage=1.00: Aw1n_t4ng-299k_kh1-t4i_4pp! x3 n4p d4u. Ch0i T.L.M.N, X.0c-D.1a, N.0hu... cuc ph3. L1nk: awin6.tech/XyZ78
- row 2524 | Crypto / Đầu tư giả | leet_ratio=0.92 | sensitive_coverage=1.00: Ch@o_b4n! M1nh-th@y-b4n_phu-h0p_v01_v13c-l4m_th4-t1m_v!d30-k13m_t13n. Khong-c4n_v0n, nh4n_100k-cu01-ng4y_nhe.
- row 154 | Crypto / Đầu tư giả | leet_ratio=0.92 | sensitive_coverage=1.00: H1_b4n! Cv_nh3-nh4ng_k0-mat-f33. K13m_300k-500k/ng4y_ch1-v01-sh0p33-v4-t1kt0k. Nh4n_v13c_t41: t.me/shopee_nv_24h

## Output

Manual review rows: `data\reports\level1_level2_borderline_rows.csv`

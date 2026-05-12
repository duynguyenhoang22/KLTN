# LEVEL 1 Obfuscation Correction Report

## Purpose

Repair existing synthetic `LEVEL 1` rows so they better represent sparse intentional homoglyph substitution rather than dense sentence-wide leet.

This pass did not regenerate data, did not modify labels/categories, and did not modify URL/domain strings.

## Rule Summary

- Only rows with `LEVEL 1 – Leet nhẹ (thay 1-2 ký tự)` were eligible.
- URL/domain-like spans were protected before normalization.
- At most two sensitive obfuscated tokens were preserved per row.
- Known non-sensitive leet/teencode tokens were normalized where deterministic.
- Unknown tokens were left unchanged to avoid semantic damage.

## Impact

- Total rows: 5000
- LEVEL 1 rows reviewed: 651
- LEVEL 1 rows modified: 437
- Mean LEVEL 1 leet-token ratio before: 0.3606
- Mean LEVEL 1 leet-token ratio after: 0.2887

## Level Distribution

Distribution is expected to remain unchanged because this pass repairs content style, not metadata labels.

| level                                |   count |
|:-------------------------------------|--------:|
| LEVEL 0 – Không obfuscation (formal) |     638 |
| LEVEL 1 – Leet nhẹ (thay 1-2 ký tự)  |     651 |
| LEVEL 2 – Leet nặng + tên riêng      |    2647 |
| LEVEL 3 – Dot/dash insertion         |     670 |
| LEVEL 4 – Mixed special chars        |     255 |
| LEVEL 5 – Extreme noise              |     139 |

## Modified Rows by Category

| category            |   count |
|:--------------------|--------:|
| BHXH / Trợ cấp      |     196 |
| Crypto / Đầu tư giả |       2 |
| Cờ bạc / Betting    |       9 |
| Dịch vụ công giả    |      74 |
| Giả mạo ngân hàng   |      63 |
| Tuyển dụng giả      |      37 |
| Đòi nợ / Đe dọa     |      56 |

## Manual Review File

Changed rows were written to `data\reports\level1_correction_changed_rows.csv`.

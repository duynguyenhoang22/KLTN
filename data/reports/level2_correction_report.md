# LEVEL 2 Obfuscation Correction Report

## Purpose

Repair existing synthetic `LEVEL 2` rows so they better represent targeted sensitive-word leet plus camouflage, rather than full-sentence leet by default.

This pass did not regenerate data, did not modify labels/categories, and did not modify URL/domain strings.

## Rule Summary

- Only rows with `LEVEL 2 – Leet nặng + tên riêng` were eligible.
- URL/domain-like spans were protected before normalization.
- Common non-sensitive glue/context words were normalized, for example `B4n -> Ban`, `v4o -> vao`, `kh0ng -> khong`, `zu0c -> duoc`.
- Scam-sensitive words were intentionally left obfuscated, including terms around money, account locking, verification, debt, betting, and finance.
- The `level` column was preserved because the repair changes style within Level 2 rather than changing the intended obfuscation level.

## Impact

- Total rows: 5000
- Original LEVEL 2 rows reviewed: 2647
- LEVEL 2 rows modified: 2261
- Mean LEVEL 2 leet-token ratio before: 0.7086
- Mean LEVEL 2 leet-token ratio after: 0.5055

## Level Distribution

Distribution is expected to remain unchanged because this pass repairs content style, not metadata labels.

### Before

| level                                |   count |
|:-------------------------------------|--------:|
| LEVEL 0 – Không obfuscation (formal) |     638 |
| LEVEL 1 – Leet nhẹ (thay 1-2 ký tự)  |     651 |
| LEVEL 2 – Leet nặng + tên riêng      |    2647 |
| LEVEL 3 – Dot/dash insertion         |     670 |
| LEVEL 4 – Mixed special chars        |     255 |
| LEVEL 5 – Extreme noise              |     139 |

### After

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
| BHXH / Trợ cấp      |     389 |
| Crypto / Đầu tư giả |     522 |
| Cờ bạc / Betting    |     254 |
| Dịch vụ công giả    |     362 |
| Giả mạo ngân hàng   |     318 |
| Tuyển dụng giả      |     278 |
| Đòi nợ / Đe dọa     |     138 |

## Manual Review File

Changed rows were written to `data\reports\level2_correction_changed_rows.csv`.

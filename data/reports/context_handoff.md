# Context Handoff

Project: Vietnamese smishing thesis project. Data augmentation is one part of a broader thesis involving ViSmishDS dataset construction, text normalization, rationale-aware knowledge distillation, and final model evaluation.

Current focus: validating synthetic datasets before building the final merged dataset.

## Key Decisions

- `has_url = 1` means the SMS contains a URL/domain-like link target, including bare domains such as `momo.vn`, `Booking.com`, or `zalo.me/...`.
- Numeric values such as prices and dates should not count as URLs.
- `has_phone_number = 1` means the SMS contains a contactable number: mobile number, hotline, service shortcode, SMS opt-out shortcode, or Zalo number.
- `has_phone_number` should exclude CCCD/CMND, account numbers, order IDs, tracking IDs, transaction refs, and OTPs.
- Ground-truth data was not modified during this validation pass. Only synthetic metadata was corrected.

## Files Added Or Changed

- Added `data/validate_synthetic.py`.
- Added/generated `data/reports/synthetic_validation_report.md`.
- Updated `data/synthetic/synthetic_label_0.csv`.
- Updated `data/synthetic/synthetic_label_1.csv`.
- Used `data/synthetic/synthetic_label_1_with_obf_level.csv` as the metadata source for synthetic label 1 `category` and `level`.

## Completed Validation Fixes

Synthetic `has_url` metadata:

- `synthetic_label_0`: fixed 24 rows.
- `synthetic_label_1`: fixed 70 rows.

Synthetic `has_phone_number` metadata:

- `synthetic_label_0`: fixed 193 rows.
- `synthetic_label_1`: fixed 284 rows.

Latest validation result:

- `synthetic_label_0` `has_url mismatch`: 0.
- `synthetic_label_0` `has_phone_number mismatch`: 0.
- `synthetic_label_1` `has_url mismatch`: 0.
- `synthetic_label_1` `has_phone_number mismatch`: 0.
- `synthetic_label_1` smishing category metadata: present.

## Synthetic Label 1 Metadata

`data/synthetic/synthetic_label_1.csv` now has:

```text
content,label,has_url,has_phone_number,sender_type,category,level
```

The `category` and `level` columns were copied from `data/synthetic/synthetic_label_1_with_obf_level.csv` while preserving the cleaned `has_url` and `has_phone_number` values in `synthetic_label_1.csv`.

Category distribution:

- `Nội dung nhạy cảm`: 722
- `Cờ bạc / Betting`: 721
- `Crypto / Đầu tư giả`: 720
- `BHXH / Trợ cấp`: 681
- `Tuyển dụng giả`: 676
- `Dịch vụ công giả`: 549
- `Đòi nợ / Đe dọa`: 477
- `Giả mạo ngân hàng`: 454

Obfuscation level distribution:

- `LEVEL 0 – Không obfuscation (formal)`: 638
- `LEVEL 1 – Leet nhẹ (thay 1-2 ký tự)`: 651
- `LEVEL 2 – Leet nặng + tên riêng`: 2647
- `LEVEL 3 – Dot/dash insertion`: 670
- `LEVEL 4 – Mixed special chars`: 255
- `LEVEL 5 – Extreme noise`: 139

Important observation: `LEVEL 2` dominates the dataset. This needs deeper discussion before finalizing the dataset, especially how leet was applied versus how leet should be applied for realistic Vietnamese smishing.

## Validator Notes

`data/validate_synthetic.py` now includes a module-level docstring describing:

- validation purpose,
- quality layers checked,
- output report path,
- run command,
- agreed definitions for `has_url` and `has_phone_number`.

Run command:

```bash
python data/validate_synthetic.py
```

Output:

```text
data/reports/synthetic_validation_report.md
```

## Remaining Known Issue

The next discussion should focus on `LEVEL 2 – Leet nặng + tên riêng` in synthetic label 1:

- why level 2 is heavily overrepresented,
- how leet was actually applied in the generated messages,
- how leet should be applied for realistic Vietnamese smishing,
- whether the level taxonomy or generation prompts need revision before final merge.

## Suggested Next Step

Discuss and audit the `LEVEL 2` leet strategy before building the final merged dataset.

## LEVEL 2 Correction Update

Decision: do not regenerate synthetic data from prompts. Repair the existing synthetic label 1 data in place.

Agreed boundary:

- `LEVEL 1` = sparse intentional homoglyph substitution, usually 1–2 sensitive words, mainly for filter evasion.
- `LEVEL 2` = stronger targeted sensitive-word leet plus camouflage such as uppercase mixing, separators, or accent loss. It should not default to leeting every word in the sentence.
- Whole-sentence leet can exist as a viable minority subtype, but should not dominate `LEVEL 2`.

Added `data/fix_level2_obfuscation.py`.

The script:

- reads `data/synthetic/synthetic_label_1.csv`,
- only edits rows labeled `LEVEL 2 – Leet nặng + tên riêng`,
- protects URLs/domains before editing,
- normalizes common non-sensitive glue/context words such as `B4n`, `v4o`, `kh0ng`, `zu0c`,
- preserves scam-sensitive obfuscation around money, account locking, verification, debt, betting, finance, and similar cues,
- keeps labels/categories/level metadata unchanged.

Correction result:

- `LEVEL 2` rows reviewed: 2647.
- `LEVEL 2` rows modified: 2261.
- Mean `LEVEL 2` leet-token ratio changed from 0.7086 to 0.5055.
- Level distribution intentionally unchanged.
- Synthetic validation after correction still reports 0 mismatches for `synthetic_label_0` and `synthetic_label_1` `has_url` / `has_phone_number`.

Added/generated:

- `data/reports/level2_correction_report.md`
- `data/reports/level2_correction_changed_rows.csv`

## LEVEL 1 vs LEVEL 2 Boundary Analysis

Added `data/analyze_level1_level2_boundary.py`.

Generated:

- `data/reports/level1_level2_boundary_report.md`
- `data/reports/level1_level2_borderline_rows.csv`

Main finding:

- Repaired `LEVEL 2` is improved, but `LEVEL 1` is not clean under the intended definition.
- `LEVEL 1` should mean sparse intentional homoglyph substitution, mostly 1–2 sensitive terms.
- Current `LEVEL 1` often contains dense leet across many words.

Boundary analysis counts:

- `LEVEL 1` rows analyzed: 651.
- Before `LEVEL 1` repair, `LEVEL 1` flagged as too heavy: 598.
- `LEVEL 2` rows analyzed: 2647.
- `LEVEL 2` OK by heuristic: 1923.
- `LEVEL 2` separator-dominant: 498.
- `LEVEL 2` still over-leeted: 92.
- `LEVEL 2` too mild: 134.

Important interpretation:

- The remaining issue is not only overrepresented `LEVEL 2`.
- The `LEVEL 1` / `LEVEL 2` boundary is blurred because many `LEVEL 1` rows behave more like moderate or heavy leet.
- Before final merge, consider a second repair pass for `LEVEL 1`: normalize non-sensitive leet more aggressively while preserving 1–2 sensitive obfuscated terms.

## LEVEL 1 Correction Update

Added `data/fix_level1_obfuscation.py`.

Decision: repair existing `LEVEL 1` rows conservatively, without regeneration and without changing labels/categories.

Rule:

- only rows labeled `LEVEL 1 – Leet nhẹ (thay 1-2 ký tự)` are eligible,
- protect URL/domain spans before editing,
- preserve at most two sensitive obfuscated tokens per row,
- normalize known non-sensitive or extra generated leet tokens where deterministic,
- leave unknown/ambiguous generated tokens unchanged.

The script was run twice: first broad conservative cleanup, then a small deterministic refinement for obvious residual forms such as `N4p`, `nh4n`, `t13n`, `h0 tr0`, `C4nh s4t`, `G140 thong`, and `T0ng cuc Thu3`.

Final effect:

- `LEVEL 1` rows reviewed: 651.
- Final refinement modified 437 rows on top of the first pass.
- Script-level mean `LEVEL 1` leet-token ratio decreased cumulatively from 0.6507 before repair to 0.2887 after repair.
- Boundary-analysis mean `LEVEL 1` leet-token ratio is now 0.256.
- Boundary-analysis mean `LEVEL 2` leet-token ratio remains 0.485.
- Final boundary flags: `LEVEL 1` OK = 433, `LEVEL 1` too heavy = 218.
- `LEVEL 2` final flags remain: OK = 1923, separator-dominant = 498, still-overleeted = 92, too-mild = 134.
- Synthetic validation after the repair still reports `synthetic_label_1` `has_url mismatch = 0` and `has_phone_number mismatch = 0`.

Generated:

- `data/reports/level1_correction_report.md`
- `data/reports/level1_correction_changed_rows.csv`

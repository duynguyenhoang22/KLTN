# Báo cáo Mistral metadata pilot

- Model: `mistral-small-2506`
- Taxonomy: `2.1.0-locked`
- Records: 100
- Unique sample IDs: 100
- API output status: `auto_labeled`

## Message domain

| Domain | Count |
|---|---:|
| public_service | 17 |
| commerce | 15 |
| telecom | 14 |
| marketing_promotion | 10 |
| personal_social | 7 |
| debt_collection | 7 |
| other | 6 |
| banking_finance | 6 |
| logistics | 4 |
| investment | 4 |
| unknown | 3 |
| employment | 3 |
| healthcare | 2 |
| adult_service | 1 |
| gambling | 1 |

## Text noise score

| Score | Count |
|---:|---:|
| 0 | 44 |
| 1 | 28 |
| 2 | 14 |
| 3 | 8 |
| 4 | 6 |

## Review flags

- `obfuscation_intent_uncertain`: 6
- `unreadable_content`: 2

## Field confidence

| Field | Mean | Min |
|---|---:|---:|
| message_domain | 0.938 | 0.100 |
| surface_features | 0.964 | 0.800 |
| target_audience | 0.900 | 0.100 |
| obfuscation | 0.968 | 0.700 |
| persuasion_tactics | 0.936 | 0.100 |
| requested_actions | 0.955 | 0.100 |

## Lưu ý

Báo cáo này chỉ xác nhận pipeline/API/schema chạy thành công. Chất lượng metadata chỉ được đánh giá sau khi hai human annotation sheet hoàn tất và được so sánh với output này.

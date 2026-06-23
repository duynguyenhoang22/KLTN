# Báo cáo review taxonomy P0.2

- Tổng field/value: 103
- Exact agreement: 77 (74.8%)
- Mục vào adjudication queue: 27
- Lỗi review sheet: 4

## Cặp decision

| Reviewer A | Reviewer B | Số lượng |
|---|---|---:|
| accept | accept | 76 |
| merge | accept | 11 |
| accept | merge | 5 |
| rename | accept | 4 |
| remove | accept | 3 |
| merge | merge | 2 |
| (blank) | accept | 1 |
| rename | merge | 1 |

## Lỗi cần sửa trước khi khóa

- reviewer_a text_phenomena.code_switching line 34: invalid/blank decision ''
- reviewer_a text_phenomena.code_switching line 34: non-accept decision requires comment
- reviewer_a obfuscation_techniques.unicode_noise line 45: non-accept decision requires comment
- reviewer_b target_roles.shopper line 99: merge requires proposed_value_or_target

## Cách adjudicate

Hai reviewer chỉ cần thảo luận các dòng trong queue và điền ba cột cuối. Các mục cả hai cùng `accept` không xuất hiện trong queue.

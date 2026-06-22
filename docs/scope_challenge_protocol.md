# Protocol gán 50 ca khó để khóa P0.1

Hai annotator làm **độc lập**, không xem file của nhau và không mở:

```text
data/processed/scope_challenge_internal_key.csv
```

File làm việc:

- Annotator A: `data/annotations/scope_challenge_annotator_a.csv`
- Annotator B: `data/annotations/scope_challenge_annotator_b.csv`

Hai file chứa cùng 50 mẫu nhưng có thứ tự khác nhau. Chỉ sử dụng `content` để
ra quyết định; không tìm kiếm nguồn hoặc kiểm tra label/category cũ.

## Cách điền

### `scope_decision`

Chỉ dùng một trong các giá trị:

- `accepted`
- `needs_adjudication`
- `excluded_out_of_scope_malicious`
- `excluded_language_scope`
- `excluded_insufficient_context`
- `excluded_invalid_record`
- `excluded_privacy_or_safety`

### `proposed_label`

- Điền `0` hoặc `1` khi `scope_decision=accepted`.
- Để trống với mọi quyết định còn lại.

### `evidence`

Ghi cụm từ ngắn trích từ `content` làm căn cứ. Không ghi kiến thức hoặc giả
định bên ngoài.

### `confidence`

Sử dụng một trong ba mức:

- `high`
- `medium`
- `low`

Confidence không thay đổi quy tắc nhãn. Nếu không thể ra quyết định theo scope,
chọn `needs_adjudication` thay vì đoán với confidence thấp.

### `reason`

Ghi một câu ngắn giải thích tại sao quy tắc scope dẫn đến quyết định đó.

### `needs_discussion`

- `0`: guideline đã đủ rõ;
- `1`: dù đã đưa ra quyết định, mẫu cho thấy guideline cần thảo luận hoặc bổ sung.

## Nguyên tắc làm việc

1. Không trao đổi từng mẫu trong lúc gán.
2. Không sửa `sample_id`, `content` hoặc `item_order`.
3. Không đổi thứ tự dòng.
4. Không dùng category, obfuscation hoặc label Phase 1.
5. Không dùng LLM để ra quyết định thay annotator trong vòng này.
6. Có thể đọc lại `docs/dataset_scope.md` trong quá trình gán.
7. Không mở internal key trước khi cả hai đã nộp file.

## Sau khi hoàn thành

Không tự so sánh thủ công. Pipeline tiếp theo sẽ:

- join bằng `sample_id`;
- tính agreement cho scope decision và proposed label;
- liệt kê disagreement;
- nhóm bất đồng theo loại ca khó;
- tạo adjudication sheet.

Mục tiêu của vòng này không phải đạt điểm cao bằng mọi giá. Bất đồng là tín
hiệu để phát hiện chỗ scope chưa rõ trước khi gán dữ liệu lớn.

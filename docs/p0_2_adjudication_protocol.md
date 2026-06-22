# Protocol adjudication taxonomy P0.2

Trạng thái: hoàn tất ngày 2026-06-22; taxonomy đã khóa `2.1.0-locked`.

Đầu vào:

- `data/annotations/p0_2_taxonomy_adjudication.csv`
- `data/processed/p0_2_taxonomy_review_report.md`

Hai reviewer cùng thảo luận 27 dòng trong queue. Các mục cả hai cùng `accept`
đã được loại khỏi sheet.

## Ba cột cần điền

- `final_decision`: `accept`, `rename`, `merge`, `split`, `remove`;
- `final_value_or_target`: bắt buộc với rename/merge/split;
- `adjudication_comment`: lý do ngắn cho quyết định cuối.

Với `accept` hoặc `remove`, `final_value_or_target` để trống.

## Bốn lỗi hồ sơ cần làm rõ trong buổi họp

1. Reviewer A chưa điền decision cho `text_phenomena.code_switching`.
2. Reviewer A remove `obfuscation_techniques.unicode_noise` nhưng thiếu comment.
3. Reviewer B merge `target_roles.shopper` nhưng thiếu target.
4. `comemerce_logistics` là typo; nếu quyết định merge, chuẩn hóa thành
   `commerce_logistics`.

Không cần quay lại sửa review sheet độc lập. Quyết định đúng được ghi trong
adjudication sheet để giữ nguyên bằng chứng review ban đầu.

## Thứ tự thảo luận nhanh

### Nhóm 1 — Hai người cùng muốn thay đổi

- `target_roles.taxpayer`: cả hai merge vào `general_public`.
- `target_roles.employee`: cùng muốn gộp employee/worker nhưng tên đích khác.
- `target_roles.shopper`: cùng muốn merge nhưng Reviewer B thiếu target.

### Nhóm 2 — Ranh giới kỹ thuật

- `leetspeak`, `character_substitution`, `homoglyph`;
- `token_splitting` → `whitespace_splitting`;
- `token_joining` → `word_concatenation`;
- `unicode_noise`;
- `code_switching`.

Thảo luận một lần rồi áp dụng cùng quyết định cho cả `text_phenomena` và
`obfuscation_techniques` khi khái niệm tương ứng giống nhau.

### Nhóm 3 — Domain và sentinel

- `commerce` + `logistics`;
- `message_domain.unknown` và `other`;
- `target_gender.not_applicable` và `all`.

Không merge sentinel chỉ vì chúng thường cho cùng kết quả. `unknown`,
`other`, `not_applicable`, `all` biểu diễn các trạng thái dữ liệu khác nhau.

### Nhóm 4 — Granularity

- `child`, `young_adult`;
- các target roles cần gộp;
- `provide_credentials` và `provide_personal_information`.

Ưu tiên khả năng gán ổn định và giá trị phân tích, không ưu tiên taxonomy càng
chi tiết càng tốt.

## Sau khi hoàn tất

Codex sẽ:

1. validate adjudication;
2. áp dụng decision vào taxonomy;
3. cập nhật schema, guideline và review sheets;
4. tăng version lên `2.1.0-locked`;
5. chạy contract audit;
6. mở khóa metadata pilot và Mistral pilot.

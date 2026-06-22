# Kết quả review và adjudication taxonomy P0.2

Ngày hoàn tất: 2026-06-22  
Taxonomy cuối: `2.1.0-locked`  
Scope: `2.0.0-locked`

## Review độc lập

- 103 field/value được review;
- exact agreement: 77/103, tương đương 74,8%;
- 27 mục được đưa vào adjudication;
- mọi mục adjudication đã có quyết định, target hợp lệ khi cần và comment.

## Quyết định chính

### Giữ nguyên

- `commerce` và `logistics` vẫn là hai domain độc lập;
- `message_domain.unknown` độc lập với `other`;
- `character_substitution` là khái niệm hợp nhất;
- `retired_person` được giữ.

### Gộp

- leetspeak và homoglyph → `character_substitution`;
- `provide_credentials` → `provide_personal_information`;
- `young_adult` → `adult`;
- `target_gender.not_applicable` → `all`;
- account holder và shopper → `customer`;
- taxpayer và benefit recipient → `general_public`;
- worker → `employee_or_worker`.

### Đổi tên

- `token_splitting` → `whitespace_splitting`;
- `token_joining` → `word_concatenation`;
- `code_switching` → `lang_switching`;
- employee → `employee_or_worker`.

### Loại

- `unicode_noise` khỏi text phenomena và obfuscation techniques;
- `child` khỏi target age groups.

Trong adjudication sheet có typo `character_subtitution`; khi áp dụng đã được
chuẩn hóa thành value hiện có `character_substitution`.

## Kết quả kỹ thuật

- taxonomy và JSON Schema đồng bộ;
- không có token làm lộ label;
- sender policy được giữ:
  - real dùng legacy sender type human-verified;
  - synthetic/external dùng `not_applicable`;
- Mistral prompt/schema đọc động taxonomy cuối;
- live metadata run được mở khóa ở cấp taxonomy.

## Điều kiện tiếp theo

P0.2 hoàn thành. Chuyển sang metadata pilot:

1. tạo human annotation pilot theo taxonomy locked;
2. chạy Mistral pilot 50–100 mẫu;
3. so sánh LLM với human annotation;
4. sửa prompt nếu cần trước full run.

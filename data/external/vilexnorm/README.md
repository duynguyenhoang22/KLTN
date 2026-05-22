# ViLexNorm workspace

Thư mục này gồm toàn bộ artifact liên quan đến việc khai thác ViLexNorm để mở rộng/cải thiện ViSmishDS.

## Quy ước

- `raw/`: dữ liệu ViLexNorm gốc, giữ bất biến.
- `processed/`: file trung gian sau khi hợp nhất, lọc rule, tách candidate/rejected.
- `curated/`: các mẫu đã được chọn để đưa vào label 0 của ViSmishDS.
- `docs/`: tai lieu, bao cao audit, filtering report va integration report lien quan rieng den ViLexNorm.

Tat ca mau duoc lay tu ViLexNorm can giu provenance rieng qua cac cot nhu `source_dataset`, `source_file`, `source_row_id`, `external_source_type`, `text_variant_type`, `hard_case_type` va `review_status`.

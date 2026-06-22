# Pipeline gán metadata bằng Mistral Small 2506

Trạng thái: dựng sẵn, **chưa gọi API**  
Model đã chốt: `mistral-small-2506`

## Mục tiêu

Pipeline gán metadata từ `content` sau khi taxonomy được khóa. Nó không sửa:

- `content`;
- `label`;
- sender type real đã human-verified.

Synthetic và external luôn dùng `sender_type=not_applicable`.

## Luồng xử lý

```text
Phase 1 reference
→ kiểm sender policy
→ mask PII cục bộ
→ batch 8 mẫu
→ Mistral JSON object
→ kiểm sample_id/schema/invariant
→ lưu raw provider response
→ checkpoint JSONL
→ low-confidence/human review queue
```

## Bảo vệ dữ liệu

Trước khi gửi API, pipeline mask:

- email;
- số điện thoại;
- định danh có nhãn như CCCD, số tài khoản, mã hồ sơ;
- tên người khi có tiền tố rõ như `Họ tên:`.

URL được giữ vì cần cho domain/action/tactic annotation. Nội dung gốc chỉ được
ghép lại cục bộ sau phản hồi. Masking không phải khử định danh hoàn hảo; cần
audit thêm trước live run.

## Metadata giao cho LLM

- `message_domain`;
- `text_phenomena`;
- `text_noise_score`;
- `target_audience` và evidence;
- `obfuscation` và confidence;
- `persuasion_tactics`;
- `requested_actions` và evidence;
- confidence theo từng nhóm;
- review flags.

Không giao:

- label;
- data origin;
- category/obfuscation legacy;
- sender type;
- `has_url`/`has_phone_number` — hai trường này tính cục bộ.

## Provenance

Mỗi output lưu:

- provider/model;
- prompt version;
- taxonomy version;
- SHA-256 của prompt;
- thống kê masking;
- raw provider response theo batch;
- trạng thái `auto_labeled`.

Raw response và output nằm trong `data/processed/`, bị Git ignore.

## Dry-run trước taxonomy lock

```powershell
$env:PYTHONPATH="src"
python -m vismishds preview-metadata-llm --limit 16
```

Lệnh này tạo:

```text
data/processed/metadata_llm_request_preview.json
```

Không gửi request và không cần API key.

Dry-run toàn bộ snapshot Phase 1 ngày 2026-06-22:

- 10.562 records;
- batch size 8;
- 1.321 requests dự kiến;
- 2.324 số điện thoại được mask;
- 435 định danh có nhãn được mask;
- 11 email được mask;
- 1 tên người có nhãn rõ được mask.

Con số tên thấp không có nghĩa dữ liệu chỉ có một tên người; masker hiện chỉ
mask tên có tiền tố rõ để tránh phá nội dung quá mức. Human masking audit vẫn
là điều kiện trước live run.

## Live run

Chỉ chạy sau khi:

1. taxonomy có `status=locked`;
2. Reviewer A/B và adjudication hoàn tất;
3. prompt được pilot trên 50–100 mẫu;
4. masking audit đạt yêu cầu;
5. API key được đặt trong environment.

CLI tự động nạp file `.env` ở project root. Biến môi trường đã được đặt trong
process/CI có độ ưu tiên cao hơn và không bị `.env` ghi đè.

```powershell
$env:PYTHONPATH="src"
python -m vismishds run-metadata-llm --limit 100 --execute
```

Sau pilot mới bỏ `--limit`.

Pipeline hỗ trợ resume bằng cách bỏ qua `sample_id` đã có trong output JSONL.
Không xóa output giữa chừng nếu muốn tiếp tục.

## Khóa an toàn

- Không có `--execute` → không gọi API.
- Taxonomy chưa `locked` → live run bị chặn.
- Thiếu API key → live run bị chặn.
- Batch sai sample ID/số lượng → lưu raw response nhưng không nhận output.
- Retry tối đa lấy từ `configs/metadata_llm.json`.

## Việc còn làm sau taxonomy lock

- cập nhật prompt theo tên value cuối;
- bổ sung semantic validator đầy đủ cho `llm_metadata`;
- tạo low-confidence/disagreement review queue;
- chạy pilot và đo với human metadata annotation;
- chỉ sau đó mới chạy toàn bộ dataset.

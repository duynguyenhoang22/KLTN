# Protocol human metadata pilot

Taxonomy: `2.1.0-locked`  
Số mẫu: 100  
Thiết kế: 25 mẫu cho mỗi `label × data_origin`

Đọc [sổ tay thực hành](metadata_annotator_handbook.md) trước khi bắt đầu.

File:

- Annotator A: `data/annotations/metadata_pilot_annotator_a.csv`
- Annotator B: `data/annotations/metadata_pilot_annotator_b.csv`

Hai file chứa cùng mẫu nhưng thứ tự khác nhau. Không mở:

- `data/processed/metadata_pilot_internal_key.csv`;
- output Mistral;
- label/category/obfuscation legacy.

## Quy ước điền

Các trường multi-label dùng dấu `|`, ví dụ:

```text
urgency|fear|impersonation
```

Các evidence khác nhau dùng ` || `.

Boolean dùng `true` hoặc `false`. Score/severity dùng số nguyên 0–4.
Confidence dùng số từ 0 đến 1.

## Trường cần gán

- `message_domain`
- `text_phenomena`
- `text_noise_score`
- `target_age_groups`
- `target_gender`
- `target_roles`
- `target_evidence`
- `obfuscation_present`
- `obfuscation_techniques`
- `obfuscation_severity`
- `obfuscation_confidence`
- `persuasion_tactics`
- `requested_actions`
- `requested_action_evidence`
- `overall_confidence`
- `review_notes`

Không gán sender type, URL/phone hoặc label.

## Nguyên tắc

1. Chỉ dùng content.
2. Mọi target/action cụ thể phải có evidence.
3. Không obfuscation → techniques trống, severity 0.
4. Multi-label có thể để trống khi không có giá trị; riêng requested action
   dùng `none`.
5. Hai người làm độc lập, không xem file hoặc quyết định của nhau.
6. Không dùng LLM để gán thay trong vòng human pilot.

Sau khi hai file hoàn tất, pipeline sẽ đo agreement và so sánh Mistral với
human adjudication.

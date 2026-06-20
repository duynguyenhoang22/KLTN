# Kế hoạch migration từ Phase 1 sang v2

## Giai đoạn 1 — Audit và pilot

1. Chạy `python -m vismishds audit-reference`.
2. Tạo pilot 400 mẫu bằng `python -m vismishds init-pilot --size 400`.
3. Pilot được stratify theo `label × data_origin`.
4. Hai annotator gán độc lập tối thiểu 150–200 mẫu giao nhau.
5. Adjudicate bất đồng và cập nhật guideline.

## Giai đoạn 2 — Gán metadata

1. Khóa taxonomy `2.0.0`.
2. LLM chỉ tạo đề xuất kèm confidence và evidence.
3. Review toàn bộ mẫu confidence thấp, bất đồng giữa judge và mẫu ngẫu nhiên
   theo từng stratum.
4. Không đưa category/obfuscation cũ vào prompt gán mới.
5. Lưu provenance của annotator, model và guideline version.

## Giai đoạn 3 — Quality gates

- Schema validation không có lỗi.
- Không trùng `sample_id`.
- Không có leakage giữa split theo content/template/source family.
- Báo cáo IAA và adjudication.
- Báo cáo phân phối metadata và các ô có cỡ mẫu nhỏ.
- Hai LLM-as-judge độc lập cho synthetic; bất đồng chuyển human review.

## Giai đoạn 4 — Release và thí nghiệm

Chỉ sau khi release v2 được đóng băng mới thiết kế lại benchmark:

- real-only anchor;
- random augmentation đối chứng;
- metadata-matched augmentation;
- ablation theo domain, tactic và text phenomena;
- template/source-family holdout;
- nhiều seed và confidence interval.

Distillation không phải quality gate của dataset và được triển khai sau cùng.

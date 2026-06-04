# Phân tích thủ công FP/FN cho Setup A/B/E/G

## Phạm vi

Báo cáo này dùng các file `*_errors.csv` sinh từ prediction-level output của Setup A, B, E và G. Mục tiêu là giải thích pattern lỗi, không thay thế các chỉ số định lượng chính.

Các lỗi được gom theo `variant_key`, `seed`, `error_type`, metadata và một taxonomy nguyên nhân lỗi sơ bộ. Cột `suggested_reason` là nhãn gợi ý bằng rule; khi đưa vào khóa luận có thể rà lại các dòng trong `manual_review_candidates.csv`.

## Tổng quan lỗi ở các setup trọng tâm

| variant_key               |   seed |   FN |   FP |   total_errors |
|:--------------------------|-------:|-----:|-----:|---------------:|
| A_real_only               |     42 |    3 |    3 |              6 |
| A_real_only               |    123 |    3 |    4 |              7 |
| A_real_only               |   2025 |    3 |    4 |              7 |
| B1_class_weight_default   |     42 |    3 |    4 |              7 |
| B1_class_weight_default   |    123 |    3 |    3 |              6 |
| B1_class_weight_default   |   2025 |    2 |    5 |              7 |
| B2_class_weight_threshold |     42 |    3 |    6 |              9 |
| B2_class_weight_threshold |    123 |    3 |    3 |              6 |
| B2_class_weight_threshold |   2025 |    2 |    7 |              9 |
| E4_all                    |     42 |    3 |    5 |              8 |
| E4_all                    |    123 |    3 |    1 |              4 |
| E4_all                    |   2025 |    5 |    1 |              6 |
| G0_E4_champion            |     42 |    4 |   44 |             48 |
| G0_E4_champion            |    123 |    2 |   45 |             47 |
| G0_E4_champion            |   2025 |    3 |   27 |             30 |
| G2_external_curated       |     42 |    5 |    1 |              6 |
| G2_external_curated       |    123 |    3 |    4 |              7 |
| G2_external_curated       |   2025 |    3 |    6 |              9 |

## Nhóm nguyên nhân lỗi nổi bật

### A_real_only
| variant_key   | error_type   | suggested_reason               |   n |
|:--------------|:-------------|:-------------------------------|----:|
| A_real_only   | FN           | FN_obfuscation_or_leet         |   9 |
| A_real_only   | FP           | FP_official_brandlike          |   4 |
| A_real_only   | FP           | FP_legitimate_recruitment_like |   3 |
| A_real_only   | FP           | FP_legitimate_with_url         |   3 |
| A_real_only   | FP           | FP_legitimate_promotion_reward |   1 |

### B1_class_weight_default
| variant_key             | error_type   | suggested_reason               |   n |
|:------------------------|:-------------|:-------------------------------|----:|
| B1_class_weight_default | FN           | FN_obfuscation_or_leet         |   8 |
| B1_class_weight_default | FP           | FP_legitimate_recruitment_like |   3 |
| B1_class_weight_default | FP           | FP_legitimate_with_url         |   3 |
| B1_class_weight_default | FP           | FP_official_brandlike          |   3 |
| B1_class_weight_default | FP           | FP_legitimate_promotion_reward |   2 |
| B1_class_weight_default | FP           | FP_legitimate_url_and_phone    |   1 |

### B2_class_weight_threshold
| variant_key               | error_type   | suggested_reason               |   n |
|:--------------------------|:-------------|:-------------------------------|----:|
| B2_class_weight_threshold | FN           | FN_obfuscation_or_leet         |   8 |
| B2_class_weight_threshold | FP           | FP_legitimate_promotion_reward |   4 |
| B2_class_weight_threshold | FP           | FP_legitimate_recruitment_like |   4 |
| B2_class_weight_threshold | FP           | FP_official_brandlike          |   4 |
| B2_class_weight_threshold | FP           | FP_legitimate_with_url         |   3 |
| B2_class_weight_threshold | FP           | FP_legitimate_url_and_phone    |   1 |

### E4_all
| variant_key   | error_type   | suggested_reason               |   n |
|:--------------|:-------------|:-------------------------------|----:|
| E4_all        | FN           | FN_obfuscation_or_leet         |  11 |
| E4_all        | FP           | FP_legitimate_with_url         |   3 |
| E4_all        | FP           | FP_legitimate_recruitment_like |   2 |
| E4_all        | FP           | FP_official_brandlike          |   1 |
| E4_all        | FP           | FP_other_or_ambiguous          |   1 |

### G0_E4_champion
| variant_key    | error_type   | suggested_reason               |   n |
|:---------------|:-------------|:-------------------------------|----:|
| G0_E4_champion | FN           | FN_obfuscation_or_leet         |   9 |
| G0_E4_champion | FP           | FP_other_or_ambiguous          |  63 |
| G0_E4_champion | FP           | FP_legitimate_recruitment_like |  35 |
| G0_E4_champion | FP           | FP_legitimate_promotion_reward |   9 |
| G0_E4_champion | FP           | FP_official_brandlike          |   6 |
| G0_E4_champion | FP           | FP_legitimate_with_url         |   3 |

### G2_external_curated
| variant_key         | error_type   | suggested_reason               |   n |
|:--------------------|:-------------|:-------------------------------|----:|
| G2_external_curated | FN           | FN_obfuscation_or_leet         |  11 |
| G2_external_curated | FP           | FP_legitimate_recruitment_like |   6 |
| G2_external_curated | FP           | FP_legitimate_with_url         |   4 |
| G2_external_curated | FP           | FP_other_or_ambiguous          |   1 |

## Nhận định chính

1. Trên Real Test, các setup A/B/E mắc rất ít lỗi tuyệt đối vì test set nhỏ; do đó phân tích lỗi nên xem như minh họa định tính cho trade-off precision/recall.

2. Cặp A vs E4 phù hợp để phân tích tác động của synthetic Label 1 augmentation: E4 giữ số lỗi thấp, nhưng cần kiểm tra các FP xem mô hình có nhạy hơn với URL/khuyến mãi/brandname hay không.

3. Cặp G0 vs G2 là bằng chứng định tính mạnh nhất: G0 tạo nhiều FP trên external Label 0, trong khi G2 loại bỏ lỗi external ở cả ba seed và chỉ còn lỗi trên real subset. Điều này ủng hộ luận điểm cần mở rộng miền Label 0 khi dùng synthetic Label 1 augmentation.

4. Các lỗi FN ổn định qua nhiều seed thường là smishing có bề mặt giống tin hợp lệ: thiếu URL, dùng shortcode/brandname, văn phong khuyến mãi hoặc tuyển sinh hợp lệ. Đây là nhóm nên được mô tả trong phần hạn chế.

## File artefact

- `all_errors_labeled.csv`: toàn bộ FP/FN đã gán `suggested_reason`.

- `stable_error_cases.csv`: lỗi gộp theo mẫu và số seed mắc lỗi.

- `manual_review_candidates.csv`: tập mẫu ưu tiên để rà thủ công và viết ví dụ trong khóa luận.

- `error_summary_by_setup_seed.csv`, `error_summary_by_reason.csv`, `error_summary_by_category.csv`: các bảng tổng hợp.

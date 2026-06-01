# Báo cáo audit chất lượng dữ liệu: Phase 1 final vs temp.csv

## Mục tiêu

Báo cáo này tổng hợp kết quả audit định lượng từ script `scripts/data_pipeline/audit_phase1_quality_metrics.py` nhằm so sánh bộ dữ liệu `vismishds_phase1_final.csv` với phiên bản hiện tại `temp.csv`. Mục tiêu của dữ liệu tạo sinh trong đề tài là augmentation: mở rộng số lượng mẫu và miền dữ liệu trong bối cảnh dữ liệu thật hạn chế, không phải thay thế dữ liệu thật. Vì vậy, audit tập trung vào việc kiểm tra dữ liệu tạo sinh có đa dạng hơn, ít lặp mẫu hơn, ít artifact cực đoan hơn và có phân phối metadata hợp lý hơn để hỗ trợ huấn luyện mô hình hay không. Các metric so sánh với real được dùng như kiểm soát độ lệch phân phối, không phải tiêu chí bắt synthetic phải đồng nhất với real.

## Thiết lập audit

Script sử dụng hai đầu vào:

- Phase 1 final: `data/final/vismishds_phase1_final.csv`
- Phiên bản hiện tại: `model/base/temp.csv`

Cả hai bộ dữ liệu đều có 10.562 mẫu, cân bằng nhãn với 5.320 mẫu label 0 và 5.242 mẫu label 1. Các kiểm tra invariant đều đạt: file tồn tại, có đủ cột bắt buộc, nhãn hợp lệ `[0, 1]`, không có nội dung rỗng, và số mẫu label 1 synthetic-like của Phase 1 là 4.996 như kỳ vọng.

Embedding audit sử dụng `vinai/phobert-base` từ Transformers, không dùng checkpoint PhoBERT đã fine-tune cho bài toán phân loại. Embedding được tính bằng mean pooling trên last hidden state và chuẩn hóa L2. Điều này giúp giảm nguy cơ metric bị thiên lệch bởi mô hình phân loại đã huấn luyện trước đó.

## Thay đổi về nguồn dữ liệu

Phase 1 final chỉ gồm hai nguồn:

| Nguồn | Số mẫu |
|---|---:|
| synthetic | 7.995 |
| real | 2.567 |

Trong `temp.csv`, nguồn dữ liệu được tách chi tiết hơn:

| Nguồn | Số mẫu |
|---|---:|
| paraphrased | 4.333 |
| real | 2.567 |
| synthetic | 2.008 |
| synthetic_hard_negative | 653 |
| external_curated | 501 |
| external_real | 500 |

Việc bổ sung `paraphrased`, `synthetic_hard_negative`, `external_real` và `external_curated` cho thấy `temp.csv` không chỉ là bản làm sạch nhỏ của Phase 1, mà là một phiên bản được tái cấu trúc nguồn dữ liệu rõ ràng hơn.

## Đa dạng và lặp mẫu

Với nhóm label 1 synthetic-like, embedding nearest-neighbor similarity giảm rõ rệt:

| Metric | Phase 1 | temp.csv |
|---|---:|---:|
| Mean NN cosine similarity | 0,9533 | 0,9273 |
| Median | 0,9621 | 0,9288 |
| Rate >= 0,90 | 92,73% | 76,68% |
| Rate >= 0,95 | 63,17% | 27,48% |

Điều này cho thấy `temp.csv` đa dạng hơn ở mức biểu diễn ngữ nghĩa: mỗi mẫu synthetic label 1 trung bình ít giống mẫu synthetic gần nhất hơn so với Phase 1.

TF-IDF nearest-neighbor similarity cũng giảm ở trung bình:

| Slice | Analyzer | Phase 1 mean | temp.csv mean |
|---|---|---:|---:|
| label 1 synthetic-like | char | 0,4962 | 0,4192 |
| label 1 synthetic-like | word | 0,4130 | 0,3652 |
| label 0 synthetic-like | char | 0,5368 | 0,5186 |
| label 0 synthetic-like | word | 0,4251 | 0,4076 |

N-gram repetition cũng giảm:

| Slice | N-gram | Phase 1 repeated mass | temp.csv repeated mass |
|---|---:|---:|---:|
| label 1 synthetic-like | 5-gram | 0,6008 | 0,4873 |
| label 1 synthetic-like | 6-gram | 0,5202 | 0,3951 |
| label 0 synthetic-like | 5-gram | 0,5188 | 0,4712 |
| label 0 synthetic-like | 6-gram | 0,4321 | 0,3867 |

Tuy nhiên, exact masked duplicate rate của label 1 synthetic-like tăng từ 1,20% lên 2,54%. Vì vậy, có thể kết luận rằng `temp.csv` cải thiện đa dạng tổng thể và giảm lặp n-gram, nhưng vẫn cần kiểm tra một nhóm nhỏ near-duplicate/exact masked duplicate trong label 1 synthetic-like.

## Obfuscation và leet

Mức độ leet trong label 1 synthetic-like giảm mạnh:

| Metric | Phase 1 | temp.csv |
|---|---:|---:|
| Row with leet rate | 82,45% | 72,78% |
| Leet token rate | 18,87% | 4,91% |
| Mean leet density | 0,2700 | 0,0671 |

Đây là cải thiện quan trọng. Phase 1 có dấu hiệu over-obfuscation ở nhóm smishing synthetic, trong khi `temp.csv` đưa mức leet về gần nhóm real hơn. Điều này giúp dữ liệu sinh tránh việc mô hình học shortcut quá mạnh từ ký tự leet thay vì học nội dung lừa đảo thực sự.

## Độ dài văn bản

Nhóm label 1 synthetic-like trong `temp.csv` dài hơn Phase 1:

| Metric | Phase 1 | temp.csv |
|---|---:|---:|
| Mean length | 117,48 | 159,83 |
| Median length | 110 | 149 |
| P90 | 182 | 238 |
| Max | 298 | 554 |

So với label 1 real có mean length 194,09 và median 156, `temp.csv` đưa độ dài synthetic label 1 gần dữ liệu thật hơn Phase 1. Đây là cải thiện về hình thái dữ liệu.

## Kiểm soát độ lệch phân phối giữa real và synthetic label 1

Vì dữ liệu tạo sinh được dùng để augmentation, mục tiêu không phải làm cho synthetic trùng hoàn toàn với real. Tuy nhiên, nếu synthetic lệch quá mạnh ở các thuộc tính bề mặt như category, sender type hoặc obfuscation level, mô hình có thể học shortcut không mong muốn. Do đó, các khoảng cách phân phối dưới đây được dùng như chỉ báo kiểm soát độ lệch.

Một số phân phối metadata trong `temp.csv` gần real hơn đáng kể:

| Metric | Phase 1 | temp.csv | Diễn giải |
|---|---:|---:|---|
| JS divergence category | 0,5792 | 0,1490 | Cải thiện mạnh |
| JS divergence sender_type | 0,0521 | 0,0226 | Cải thiện |
| JS divergence obfuscation_level | 0,3507 | 0,0717 | Cải thiện mạnh |
| JS divergence has_url | 0,0002 | 0,0046 | Xấu hơn nhẹ, nhưng giá trị vẫn nhỏ |
| JS divergence has_phone_number | 0,0011 | 0,0025 | Xấu hơn nhẹ, nhưng giá trị vẫn nhỏ |

Tuy nhiên, các khoảng cách embedding giữa real label 1 và synthetic-like label 1 lại tăng:

| Metric | Phase 1 | temp.csv |
|---|---:|---:|
| Centroid cosine distance | 0,0261 | 0,0594 |
| MMD RBF | 0,0512 | 0,0838 |
| Frechet PCA50 | 0,1246 | 0,1523 |

Vì vậy, kết luận nên được diễn giải theo mục tiêu augmentation: `temp.csv` cải thiện rõ rệt phân phối metadata và hình thái dữ liệu, nhưng đồng thời mở rộng miền biểu đạt của synthetic label 1 thay vì ép nó sát hoàn toàn vào cụm real. Việc khoảng cách embedding tăng không tự động là tín hiệu xấu trong bối cảnh augmentation; nó cho thấy dữ liệu tạo sinh có thể bao phủ thêm biến thể mới. Tác động thực sự cần được xác nhận bằng TSTR và downstream classification trên tập test real/challenge.

## Source separability

Khả năng phân biệt real và synthetic-like trong label 1 vẫn rất cao:

| Feature | Phase 1 ROC-AUC | temp.csv ROC-AUC | Phase 1 F1 | temp.csv F1 |
|---|---:|---:|---:|---:|
| TF-IDF char | 0,9938 | 0,9925 | 0,9923 | 0,9907 |
| Embedding | 0,9908 | 0,9926 | 0,9938 | 0,9949 |

Điều này cho thấy dù `temp.csv` đã cải thiện nhiều đặc điểm bề mặt, nguồn real và synthetic-like vẫn còn dễ phân biệt. Trong bối cảnh augmentation, đây không phải là tiêu chí loại bỏ dữ liệu, vì synthetic được thiết kế để bổ sung biến thể và mở rộng miền dữ liệu. Kết quả này chỉ cho thấy không nên diễn giải synthetic như dữ liệu thay thế real; thay vào đó, cần đánh giá nó bằng hiệu quả khi trộn vào tập train và kiểm tra trên real/challenge test.

## Kết luận

So với Phase 1 final, `temp.csv` có cải thiện rõ rệt ở các điểm sau:

1. Đa dạng ngữ nghĩa tốt hơn, thể hiện qua embedding nearest-neighbor similarity giảm.
2. Lặp n-gram giảm ở cả label 1 synthetic-like và label 0 synthetic-like.
3. Mức leet/obfuscation của label 1 synthetic-like giảm mạnh, tránh over-obfuscation.
4. Độ dài văn bản label 1 synthetic-like gần real hơn.
5. Phân phối category, sender type và obfuscation level giữa real và synthetic label 1 gần nhau hơn.

Tuy nhiên, vẫn còn một số hạn chế:

1. Exact masked duplicate rate của label 1 synthetic-like tăng từ 1,20% lên 2,54%.
2. Khoảng cách embedding giữa real label 1 và synthetic-like label 1 tăng trên centroid distance, MMD và Frechet PCA50; điều này cần được diễn giải như dấu hiệu mở rộng miền dữ liệu, không phải bằng chứng synthetic kém chất lượng nếu downstream performance cải thiện.
3. Source separability vẫn rất cao, nghĩa là real và synthetic-like vẫn dễ bị phân biệt bằng TF-IDF hoặc embedding; do đó synthetic không nên được xem là dữ liệu thay thế real.

Nhìn chung, `temp.csv` là phiên bản cải thiện đáng kể về đa dạng, kiểm soát obfuscation và cân bằng metadata so với Phase 1 final. Quan trọng hơn, các cải thiện này phù hợp với mục tiêu augmentation: tăng độ phủ biến thể, giảm lặp mẫu và giảm artifact quá mức để bổ sung cho dữ liệu thật vốn hạn chế. Khi tích hợp vào khóa luận, nên trình bày `temp.csv` như một bước cải thiện chất lượng dữ liệu tạo sinh phục vụ augmentation, còn kết quả TSTR/downstream classification trên real/challenge test là bằng chứng chính cho hiệu quả thực nghiệm.

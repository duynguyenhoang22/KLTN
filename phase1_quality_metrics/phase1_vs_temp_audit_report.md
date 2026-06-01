# Báo cáo audit chất lượng dữ liệu: Phase 1 final vs temp.csv

## Mục tiêu

Báo cáo này tổng hợp kết quả audit định lượng từ script `scripts/data_pipeline/audit_phase1_quality_metrics.py` nhằm so sánh bộ dữ liệu `vismishds_phase1_final.csv` với phiên bản hiện tại `temp.csv`. Mục tiêu của dữ liệu tạo sinh trong đề tài là augmentation: mở rộng số lượng mẫu và miền dữ liệu trong bối cảnh dữ liệu thật hạn chế, không phải thay thế dữ liệu thật. Vì vậy, audit tập trung vào việc kiểm tra dữ liệu tạo sinh có đa dạng hơn, ít lặp mẫu hơn, ít artifact cực đoan hơn và có phân phối metadata hợp lý hơn để hỗ trợ huấn luyện mô hình hay không. Các metric so sánh với real được dùng như kiểm soát độ lệch phân phối, không phải tiêu chí bắt synthetic phải đồng nhất với real.

## Thiết lập audit

Script sử dụng hai đầu vào:

- Phase 1 final: `data/final/vismishds_phase1_final.csv`
- Phiên bản hiện tại: `model/base/temp.csv`

Cả hai bộ dữ liệu đều có 10.562 mẫu, cân bằng nhãn với 5.320 mẫu label 0 và 5.242 mẫu label 1. Các kiểm tra invariant đều đạt: file tồn tại, có đủ cột bắt buộc, nhãn hợp lệ `[0, 1]`, không có nội dung rỗng, và số mẫu label 1 synthetic-like của Phase 1 là 4.996 như kỳ vọng.

Embedding audit sử dụng `vinai/phobert-base` từ Transformers, không dùng checkpoint PhoBERT đã fine-tune cho bài toán phân loại. Embedding được tính bằng mean pooling trên last hidden state và chuẩn hóa L2.

## Cơ sở lý thuyết

Audit này được xây dựng theo mục tiêu đánh giá dữ liệu tạo sinh dùng cho data augmentation. Về nguyên tắc, augmentation không yêu cầu dữ liệu synthetic phải trùng hoàn toàn với dữ liệu thật; mục tiêu chính là mở rộng độ phủ biến thể của tập huấn luyện trong khi vẫn kiểm soát các artifact có thể làm mô hình học shortcut. Cách tiếp cận này phù hợp với các khảo sát về data augmentation cho học máy và NLP: dữ liệu bổ sung chỉ hữu ích khi nó tăng tính đa dạng có liên quan đến tác vụ, không làm méo phân phối nhãn hoặc đưa vào tín hiệu giả quá dễ nhận biết [1], [2].

Các metric nearest-neighbor dựa trên embedding và TF-IDF được dùng để đo mức độ trùng lặp hoặc quá gần nhau giữa các mẫu synthetic. TF-IDF là biểu diễn thống kê cổ điển cho biết tầm quan trọng tương đối của token/ngram trong văn bản [3], còn cosine similarity là thước đo phổ biến để so sánh hướng của vector đặc trưng trong không gian văn bản. Với embedding, script sử dụng `vinai/phobert-base`, một mô hình ngôn ngữ tiền huấn luyện cho tiếng Việt dựa trên kiến trúc Transformer/BERT [4], [5]. Khi nearest-neighbor similarity quá cao, nhiều mẫu có thể chỉ là biến thể bề mặt của nhau, làm giảm lợi ích augmentation và tăng nguy cơ overfitting.

Nhóm metric n-gram repetition và exact masked duplicate bổ sung góc nhìn ở mức chuỗi ký tự/từ. Việc chuẩn hóa URL, số điện thoại và chữ số trước khi đếm n-gram giúp phát hiện các mẫu dùng cùng template nhưng thay đổi token định danh. Đây là kiểm tra quan trọng trong dữ liệu smishing vì các tin nhắn lừa đảo thường có cấu trúc mẫu lặp lại; nếu dữ liệu tạo sinh lặp template quá nhiều, mô hình có thể học khuôn mẫu nhân tạo thay vì đặc trưng ngữ nghĩa của hành vi lừa đảo.

Các metric về leet/obfuscation được dùng để kiểm soát artifact bề mặt. Obfuscation như thay chữ bằng số hoặc ký tự đặc biệt có thể xuất hiện trong tin nhắn độc hại, nhưng nếu tần suất quá cao trong synthetic, mô hình phân loại có thể dựa vào tín hiệu dễ thấy này như một shortcut. Vì vậy, report diễn giải việc giảm leet density như một cải thiện chất lượng: synthetic vẫn giữ được biến thể obfuscation nhưng không để artifact chi phối phân phối dữ liệu.

Khoảng cách phân phối giữa real và synthetic được đo bằng Jensen-Shannon divergence cho metadata rời rạc và bằng centroid distance, Maximum Mean Discrepancy (MMD) cùng Frechet distance cho embedding. Jensen-Shannon divergence là biến thể đối xứng, hữu hạn của KL divergence, phù hợp để so sánh hai phân phối xác suất rời rạc [6]. MMD là kiểm định khoảng cách giữa hai phân phối dựa trên kernel, thường dùng để phát hiện khác biệt phân phối trong không gian đặc trưng [7]. Frechet distance, thường được dùng trong đánh giá dữ liệu sinh ở không gian đặc trưng, so sánh khác biệt trung bình và hiệp phương sai giữa hai tập biểu diễn [8]. Trong bối cảnh augmentation, các khoảng cách này được xem như tín hiệu kiểm soát độ lệch, không phải điều kiện bắt synthetic phải giống real tuyệt đối.

Cuối cùng, source separability kiểm tra liệu một bộ phân loại đơn giản có dễ phân biệt real và synthetic-like hay không. Script huấn luyện Logistic Regression với TF-IDF char n-gram hoặc embedding và đánh giá bằng ROC-AUC/F1 qua Stratified K-Fold. Nếu separability quá cao, dữ liệu synthetic vẫn mang dấu vết nguồn rõ ràng; kết quả này không tự động phủ định giá trị augmentation, nhưng nhắc rằng synthetic không nên được diễn giải như dữ liệu thay thế real. Hiệu quả cuối cùng cần được xác nhận bằng đánh giá downstream, đặc biệt là huấn luyện có/không có synthetic và kiểm tra trên tập real/challenge.

## Định nghĩa metric theo script audit

Các định nghĩa dưới đây bám theo đúng cách triển khai trong `scripts/data_pipeline/audit_phase1_quality_metrics.py`.

### Slice dữ liệu

Script tính metric trên các lát cắt dữ liệu sau:

- `all`: toàn bộ dữ liệu.
- `label_1_all`: toàn bộ mẫu có `label = 1`.
- `label_1_synthetic_like`: mẫu có `label = 1` và được xem là synthetic-like.
- `label_1_real`: mẫu có `label = 1` và không thuộc synthetic-like.
- `label_0_synthetic_like`: mẫu có `label = 0` và được xem là synthetic-like.
- `label_0_real`: mẫu có `label = 0` và không thuộc synthetic-like.

Một mẫu được xem là synthetic-like nếu `data_origin` sau khi chuyển về chữ thường thuộc một trong ba giá trị `synthetic`, `paraphrased`, `synthetic_hard_negative`, hoặc nếu cột `source_dataset` sau khi chuyển về chữ thường bắt đầu bằng chuỗi `synthetic`.

### Embedding nearest-neighbor similarity

Metric này chỉ được tính cho slice `label_1_synthetic_like` khi không bật `--no-embedding`. Script dùng `AutoTokenizer` và `AutoModel` từ Transformers với model mặc định `vinai/phobert-base`. Văn bản được word-segment bằng `pyvi.ViTokenizer.tokenize` nếu thư viện có sẵn; nếu không, script dùng trực tiếp văn bản gốc. Đầu vào được padding, truncation với `max_length = 256` mặc định. Embedding của mỗi mẫu là mean pooling trên `last_hidden_state` theo `attention_mask`, sau đó chuẩn hóa L2.

Với tập vector đã chuẩn hóa, script dùng `NearestNeighbors(n_neighbors=2, metric="cosine")`. Hàng xóm thứ nhất là chính mẫu đó, nên similarity được lấy từ hàng xóm thứ hai:

`similarity = 1 - cosine_distance_to_second_nearest_neighbor`

Các chỉ số được báo cáo gồm `mean`, `median`, `p75`, `p90`, `p95`, `max`, `rate_ge_0_80`, `rate_ge_0_85`, `rate_ge_0_90`, và `rate_ge_0_95`.

### TF-IDF nearest-neighbor similarity

Metric này được tính cho các slice có tên kết thúc bằng `synthetic_like` và slice `label_1_all`. Script có hai chế độ biểu diễn:

- `char`: `TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), min_df=1)`.
- `word`: `TfidfVectorizer(analyzer="word", ngram_range=(1, 2), min_df=1)`.

Sau khi fit TF-IDF trên nội dung của từng slice, script cũng dùng `NearestNeighbors(n_neighbors=2, metric="cosine")` và lấy similarity với hàng xóm gần thứ hai theo công thức `1 - cosine_distance`. Các chỉ số được báo cáo gồm `mean`, `p90`, `p95`, và `max`.

### N-gram repetition

Metric này được tính cho mọi slice với `n = 5` và `n = 6`. Trước khi tách n-gram, nội dung được chuẩn hóa bằng hàm `normalize_for_ngram`:

- URL được thay bằng token `URL`.
- Số điện thoại khớp regex `(?:\+?84|0)\d{8,10}` được thay bằng token `PHONE`.
- Dãy chữ số được thay bằng token `NUM`.
- Văn bản được chuyển về chữ thường.
- Token được trích bằng regex `\w+|URL|PHONE|NUM`.

Với mỗi mẫu, script tạo tất cả n-gram liên tiếp từ danh sách token đã chuẩn hóa. Nếu `total` là tổng số n-gram trong slice và `counts` là tần suất từng n-gram, các metric được định nghĩa như sau:

- `total`: tổng số n-gram được tạo.
- `unique_ratio = số n-gram duy nhất / total`.
- `repeated_mass = tổng tần suất của các n-gram có count > 1 / total`.
- `top_repeated_ngrams`: 20 n-gram có tần suất cao nhất, lưu dưới dạng JSON.

### Exact masked duplicate rate

Metric này được tính cùng với nhóm n-gram cho mọi slice. Với mỗi dòng, script chuẩn hóa nội dung bằng `normalize_for_ngram`, sau đó nối token lại thành một chuỗi masked. `exact_masked_duplicate_rate` là tỷ lệ dòng có chuỗi masked bị trùng với ít nhất một dòng khác trong cùng slice, dùng `duplicated(keep=False).mean()`.

### Leet và special-character metrics

Các metric này được tính cho mọi slice. Script tách token bằng regex `\S+`. Một token được tính là leet token nếu đồng thời có ít nhất một ký tự chữ cái và có ít nhất một ký tự thuộc tập `01345789@$!`.

Các chỉ số được định nghĩa như sau:

- `row_with_leet_rate`: tỷ lệ dòng có ít nhất một leet token.
- `leet_token_rate`: tổng số leet token chia cho tổng số token trong slice.
- `mean_leet_density`: trung bình theo dòng của `số leet token trong dòng / max(1, số token trong dòng)`.
- `special_char_row_rate`: tỷ lệ dòng có ít nhất một ký tự thuộc tập `@$!#%&*_=+~/\|<>`.

### Length distribution

Metric độ dài được tính cho mọi slice bằng `df["content"].str.len()`, tức số ký tự của chuỗi nội dung. Các chỉ số gồm `mean`, `std`, `cv = std / mean`, `min`, `p50`, `p90`, và `max`.

### Distribution distance giữa real và synthetic label 1

Nhóm metric này so sánh `label_1_real` và `label_1_synthetic_like` trong từng dataset.

Với metadata rời rạc, script xét các cột nếu tồn tại: `category`, `sender_type`, `has_url`, `has_phone_number`, `obfuscation_level`. Giá trị thiếu được thay bằng `__NA__`. Với mỗi cột, script tạo phân phối xác suất trên hợp các giá trị xuất hiện ở real và synthetic, sau đó tính:

`js_divergence = scipy.spatial.distance.jensenshannon(real_dist, synth_dist, base=2.0) ** 2`

Do `scipy.spatial.distance.jensenshannon` trả về Jensen-Shannon distance, script bình phương giá trị này để thu được Jensen-Shannon divergence.

Nếu có embedding, script tính thêm ba metric:

- `centroid_cosine_distance = 1 - cosine_similarity(mean(real_embeddings), mean(synth_embeddings))`.
- `mmd_rbf = mean(K(real, real)) + mean(K(synth, synth)) - 2 * mean(K(real, synth))`, với RBF kernel. Script lấy số mẫu `sample_n = min(max_mmd_samples, số real, số synthetic)`, mặc định `max_mmd_samples = 2000`. `gamma` được chọn bằng median heuristic: `gamma = 1 / (2 * median_dist^2)`, trong đó `median_dist` là median của các khoảng cách Euclidean khác 0 trên tập pooled sample.
- `frechet_pca50`: script gộp real sample và synthetic sample, giảm chiều bằng PCA với `pca_dim = min(50, embedding_dim, len(pooled) - 1)`, rồi tính Frechet distance giữa hai Gaussian xấp xỉ: bình phương khoảng cách giữa hai vector trung bình cộng với trace của `cov_real + cov_synth - 2 * sqrtm(cov_real @ cov_synth)`.

### Source separability metric

Metric này đo mức dễ phân biệt nguồn real và synthetic-like trong nhóm `label = 1`. Nhãn phân loại phụ là `1` nếu mẫu synthetic-like, `0` nếu không synthetic-like. Nếu một lớp có ít hơn 5 mẫu hoặc chỉ có một lớp, metric trả về `NaN`.

Với đặc trưng TF-IDF, script dùng pipeline:

`TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), min_df=2)` + `LogisticRegression(max_iter=1000, class_weight="balanced")`

Với đặc trưng embedding, script dùng pipeline:

`StandardScaler()` + `LogisticRegression(max_iter=1000, class_weight="balanced")`

Đánh giá dùng `StratifiedKFold`, số fold là `min(5, số mẫu của lớp nhỏ nhất)`, có shuffle và `random_state = seed`. Script thu xác suất dự đoán positive class để tính `roc_auc`, đồng thời lấy nhãn dự đoán để tính `f1`.

### Confidence interval và permutation test

Với embedding nearest-neighbor mean và leet token rate, script tính khoảng tin cậy bootstrap 95% bằng cách lấy mẫu lại có hoàn lại trên vector giá trị của từng slice, mặc định `bootstrap = 1000`, rồi lấy percentile 2.5 và 97.5.

Script cũng tính permutation p-value cho hai so sánh trên slice `label_1_synthetic_like`: khác biệt mean embedding nearest-neighbor similarity giữa Phase 1 và current, và khác biệt mean leet token rate giữa Phase 1 và current. Giá trị quan sát là trị tuyệt đối của chênh lệch mean. Ở mỗi permutation, script trộn pooled values, chia lại theo kích thước Phase 1 ban đầu, tính chênh lệch mean tuyệt đối, rồi tính:

`p_value = (số lần diff_permuted >= diff_observed + 1) / (số permutation + 1)`

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

## Tài liệu tham khảo

[1] Shorten, C., & Khoshgoftaar, T. M. (2019). A survey on Image Data Augmentation for Deep Learning. *Journal of Big Data, 6*, 60. <https://doi.org/10.1186/s40537-019-0197-0>

[2] Wei, J., & Zou, K. (2019). EDA: Easy Data Augmentation Techniques for Boosting Performance on Text Classification Tasks. *Proceedings of EMNLP-IJCNLP 2019*. <https://aclanthology.org/D19-1670/>

[3] scikit-learn developers. (2026). `TfidfVectorizer` documentation. <https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html>

[4] Nguyen, D. Q., & Nguyen, A. T. (2020). PhoBERT: Pre-trained language models for Vietnamese. *Findings of EMNLP 2020*. <https://aclanthology.org/2020.findings-emnlp.92/>

[5] Devlin, J., Chang, M.-W., Lee, K., & Toutanova, K. (2019). BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding. *Proceedings of NAACL-HLT 2019*. <https://aclanthology.org/N19-1423/>

[6] SciPy developers. (2026). `scipy.spatial.distance.jensenshannon` documentation. <https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.jensenshannon.html>

[7] Gretton, A., Borgwardt, K. M., Rasch, M. J., Scholkopf, B., & Smola, A. (2012). A Kernel Two-Sample Test. *Journal of Machine Learning Research, 13*, 723-773. <https://jmlr.org/papers/v13/gretton12a.html>

[8] Heusel, M., Ramsauer, H., Unterthiner, T., Nessler, B., & Hochreiter, S. (2017). GANs Trained by a Two Time-Scale Update Rule Converge to a Local Nash Equilibrium. *Advances in Neural Information Processing Systems 30*. <https://proceedings.neurips.cc/paper/2017/hash/8a1d694707eb0fefe65871369074926d-Abstract.html>

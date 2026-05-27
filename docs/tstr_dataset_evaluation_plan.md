# Kế hoạch đánh giá Bộ dữ liệu bằng phương pháp TSTR

> **Phạm vi:** Đánh giá tính hữu dụng của dữ liệu SMS tổng hợp cho bài toán phân loại nhị phân `Label 0` và `Label 1`.
>
> **Bối cảnh:** Dữ liệu thật bị mất cân bằng mạnh, với khoảng `2200+` mẫu `Label 0` và khoảng `242-246` mẫu `Label 1`. Dữ liệu tổng hợp hiện có khoảng `3000` mẫu `Label 0` và `5000` mẫu `Label 1`.
>
> **Mục tiêu trung tâm:** Kiểm tra liệu dữ liệu tổng hợp có giúp mô hình nhận diện tốt hơn `Label 1` trên dữ liệu thật hay không.

---

## 1. Động lực đánh giá

Các chỉ số mô tả như PPL, MAUVE, độ trùng lặp n-gram, phân phối độ dài câu, phân phối token hoặc độ đa dạng từ vựng chỉ trả lời câu hỏi:

```text
Dữ liệu tổng hợp có nhìn giống dữ liệu thật không?
```

Trong khi đó, câu hỏi quan trọng hơn đối với huấn luyện mô hình là:

```text
Dữ liệu tổng hợp có giúp mô hình học được ranh giới phân loại trên dữ liệu thật không?
```

Vì vậy, cần triển khai đánh giá theo phương pháp TSTR:

```text
Train on Synthetic, Test on Real
```

Tuy nhiên, không nên áp dụng TSTR cổ điển một cách máy móc. Với bộ dữ liệu hiện tại, dữ liệu thật vừa nhỏ vừa mất cân bằng, trong khi dữ liệu tổng hợp lớn hơn nhiều và có tỷ lệ nhãn khác đáng kể. Nếu so sánh trực tiếp:

```text
TRTR: 2200+ Label 0 + 242 Label 1
TSTR: 3000 Label 0 + 5000 Label 1
```

thì kết quả sẽ bị nhiễu bởi nhiều yếu tố:

- số lượng dữ liệu giữa hai nhánh không tương đương;
- tỷ lệ nhãn giữa real và synthetic khác nhau;
- `Label 1` tổng hợp nhiều hơn `Label 1` thật rất lớn;
- mô hình có thể cải thiện chỉ vì được thấy nhiều mẫu `Label 1` hơn, không nhất thiết vì synthetic data có chất lượng cao.

Do đó, kế hoạch này sử dụng TSTR theo hướng thích nghi cho bài toán **low-resource** và **imbalanced classification**. Mục tiêu không chỉ là kiểm tra synthetic data có thay thế được real data hay không, mà còn kiểm tra nó có giá trị như một nguồn augmentation hay không.

---

## 2. Câu hỏi nghiên cứu

Kế hoạch đánh giá cần trả lời bốn câu hỏi chính.

### 2.1 Synthetic-only có học được miền dữ liệu thật không?

Thiết lập TSTR thuần túy kiểm tra câu hỏi này:

```text
Train: Synthetic Train
Test: Real Test
```

Nếu mô hình chỉ học từ synthetic data nhưng vẫn đạt kết quả tốt trên `Real Test`, điều đó cho thấy dữ liệu tổng hợp có chứa tín hiệu gần với miền dữ liệu thật.

### 2.2 Synthetic data có cải thiện khả năng nhận diện Label 1 không?

Đây là câu hỏi quan trọng nhất vì lý do chính của data generation là bù thiếu dữ liệu cho lớp thiểu số.

Các chỉ số cần ưu tiên:

- `Recall` của `Label 1`;
- `Precision` của `Label 1`;
- `F1-score` của `Label 1`;
- `Macro-F1`;
- `AUPRC`;
- confusion matrix.

Không nên lấy `Accuracy` làm chỉ số chính. Với dữ liệu mất cân bằng, mô hình thiên về `Label 0` vẫn có thể đạt accuracy cao dù bỏ sót nhiều mẫu `Label 1`.

### 2.3 Synthetic data có tốt hơn các kỹ thuật xử lý mất cân bằng truyền thống không?

Trước khi kết luận synthetic data hữu ích, cần so sánh với các baseline đơn giản hơn:

- class weighting;
- oversampling `Label 1` thật;
- undersampling `Label 0`;
- focal loss;
- threshold tuning trên validation set.

Quyết định này giúp tránh kết luận quá sớm. Nếu `Real + Synthetic` không vượt được `Real only + class weight` hoặc `Real only + threshold tuning`, thì synthetic data chưa chứng minh được giá trị thực dụng vượt trội.

### 2.4 Synthetic data nên được dùng như thay thế hay augmentation?

Trong bối cảnh hiện tại, giả thuyết hợp lý nhất không phải:

```text
Synthetic data thay thế hoàn toàn real data.
```

Mà là:

```text
Synthetic data bổ sung cho real data để cải thiện khả năng nhận diện Label 1.
```

Vì vậy, ngoài TSTR synthetic-only, kế hoạch bắt buộc phải có các thiết lập `Real + Synthetic`.

---

## 3. Nguyên tắc chia dữ liệu

### 3.1 Tạo Hold-out Real Test Set

Toàn bộ đánh giá phải xoay quanh một tập test thật cố định:

```text
Real Test Set
```

Tập này chỉ chứa dữ liệu thật và không được dùng trong:

- sinh dữ liệu tổng hợp;
- chọn prompt;
- lọc synthetic sample;
- huấn luyện mô hình;
- chọn checkpoint;
- tuning threshold;
- chọn hyperparameter;
- phân tích lỗi trước khi khóa kết quả cuối.

Lý do: TSTR chỉ có ý nghĩa nếu `Real Test Set` đóng vai trò như môi trường triển khai thực tế. Nếu tập test bị lộ vào quá trình sinh hoặc lọc dữ liệu, kết quả sẽ bị thổi phồng do data leakage.

### 3.2 Chia Real Data thành train/validation/test

Khuyến nghị:

```text
Real Train: 70%
Real Validation: 10-15%
Real Test: 15-20%
```

Việc chia phải dùng `stratified split` theo nhãn.

Lý do: `Label 1` rất ít. Nếu chia ngẫu nhiên không stratify, validation hoặc test có thể chứa quá ít mẫu `Label 1`, khiến `Recall`, `Precision` và `F1 Label 1` dao động mạnh, khó tin cậy.

### 3.3 Không dùng Real Test để chọn ngưỡng

Với bài toán mất cân bằng, ngưỡng dự đoán mặc định `0.5` có thể không tối ưu. Tuy nhiên, nếu cần tuning threshold, chỉ được tuning trên:

```text
Real Validation Set
```

Lý do: Nếu dùng `Real Test` để chọn ngưỡng, tập test không còn độc lập. Khi đó kết quả cuối không còn phản ánh năng lực tổng quát hóa thật.

---

## 4. Các thiết lập thí nghiệm

### 4.1 Setup A - TRTR Real-only baseline

```text
Train: Real Train
Validation: Real Validation
Test: Real Test
```

Mục đích: tạo baseline khi chỉ dùng dữ liệu thật hiện có.

Quyết định: trong bối cảnh này, TRTR không được xem là upper bound tuyệt đối. Nó chỉ là baseline thực tế dưới điều kiện dữ liệu thật khan hiếm.

Lý do: `Label 1` thật quá ít, nên mô hình TRTR có thể chưa học tốt ranh giới của lớp thiểu số. Nếu synthetic data được tạo tốt, `Real + Synthetic` hoàn toàn có thể vượt TRTR.

Các chỉ số cần quan sát:

- `Macro-F1`;
- `F1 Label 1`;
- `Recall Label 1`;
- `Precision Label 1`;
- `AUPRC`;
- confusion matrix.

### 4.2 Setup B - TRTR với xử lý mất cân bằng

```text
Train: Real Train
Validation: Real Validation
Test: Real Test
```

Áp dụng thêm một hoặc nhiều kỹ thuật:

- class weight;
- oversampling `Label 1`;
- undersampling `Label 0`;
- focal loss;
- threshold tuning.

Mục đích: tạo baseline mạnh hơn cho dữ liệu thật.

Quyết định: đây là setup đối chứng bắt buộc.

Lý do: Nếu synthetic data chỉ tốt hơn `Real only` nhưng không tốt hơn `Real only + imbalance handling`, thì synthetic chưa chứng minh được rằng nó cần thiết hơn các kỹ thuật đơn giản.

### 4.3 Setup C - TSTR matched distribution

```text
Train: Synthetic Train có kích thước và tỷ lệ nhãn gần với Real Train
Validation: Real Validation
Test: Real Test
```

Ví dụ:

```text
Synthetic Label 0 ~= số lượng Real Train Label 0
Synthetic Label 1 ~= số lượng Real Train Label 1
```

Mục đích: kiểm tra synthetic data có mang tín hiệu phân loại tương tự real data hay không, trong điều kiện không có lợi thế về số lượng hoặc tỷ lệ nhãn.

Quyết định: cần có thiết lập matched distribution để tách tác động của chất lượng synthetic khỏi tác động của việc tăng kích thước dữ liệu.

Lý do: Nếu chỉ dùng synthetic balanced với 5000 mẫu `Label 1`, mô hình có thể tốt hơn chỉ vì đã thấy nhiều positive sample hơn. Setup matched distribution kiểm tra câu hỏi cơ bản hơn: với cùng ngân sách dữ liệu, synthetic có gần real không?

### 4.4 Setup D - TSTR balanced synthetic

```text
Train: Synthetic Train cân bằng hoặc gần cân bằng
Validation: Real Validation
Test: Real Test
```

Ví dụ:

```text
Synthetic Label 0: 3000
Synthetic Label 1: 3000 hoặc 5000
```

Mục đích: kiểm tra khả năng synthetic data giải quyết bài toán thiếu `Label 1`.

Quyết định: cho phép phân phối synthetic khác phân phối thật trong setup này, nhưng phải báo cáo rõ đây là setup `balanced synthetic`, không phải setup matched distribution.

Lý do: mục tiêu thực tế của data generation là bổ sung `Label 1`, nên cần một setup cho phép `Label 1` xuất hiện nhiều hơn để xem mô hình có học được ranh giới lớp thiểu số tốt hơn hay không.

Rủi ro: mô hình có thể tăng `Recall Label 1` nhưng làm `Precision Label 1` giảm mạnh. Vì vậy không được kết luận dựa trên recall riêng lẻ; phải đọc cùng precision, F1 và confusion matrix.

### 4.5 Setup E - Real + Synthetic Label 1

```text
Train: Real Train + Synthetic Label 1
Validation: Real Validation
Test: Real Test
```

Mục đích: đánh giá tác động trực tiếp của việc bổ sung synthetic cho lớp thiểu số.

Quyết định: đây là setup có giá trị thực dụng cao nhất đối với bài toán hiện tại.

Lý do: vấn đề gốc là thiếu `Label 1`. Nếu thêm synthetic `Label 1` giúp giảm false negative trên `Real Test` mà không làm false positive tăng quá mức, synthetic data có giá trị rõ ràng.

Nên thử nhiều mức bổ sung:

| Biến thể | Synthetic Label 1 thêm vào |
|---|---:|
| E1 | 500 |
| E2 | 1000 |
| E3 | 2000 |
| E4 | toàn bộ synthetic Label 1 |

Lý do cần thử nhiều mức: dùng toàn bộ synthetic data không phải lúc nào cũng tốt. Nếu synthetic có pattern lặp lại, thêm quá nhiều có thể làm mô hình overfit vào văn phong giả hoặc shortcut token.

### 4.6 Setup F - Real + external/synthetic Label 0 augmentation

```text
Train: Real Train + các nguồn augmentation theo từng biến thể
Validation: Real Validation
Test: Real Test
```

Mục đích: kiểm tra giá trị của từng nguồn bổ sung `Label 0`, đặc biệt tách riêng
`external_real` và `external_curated` lấy từ ViLexNorm, khi kết hợp với synthetic
`Label 1` cố định.

Quyết định: setup này nên chạy sau Setup E, không thay thế Setup E.

Lý do: nếu chỉ thêm synthetic `Label 1`, mô hình có thể lệch về positive class.
Thêm miền `Label 0` từ ViLexNorm có thể giúp giữ ranh giới giữa tin nhắn hợp lệ
và tin nhắn lừa đảo ổn định hơn so với chỉ dùng synthetic `Label 0`. Riêng
`external_curated` cần tách riêng vì đây là nhóm bình luận đã vượt câu hỏi
"có thể coi như tin nhắn P2P hay không" và có nhiều cue dễ nhầm với `Label 1`
như lương, số tiền, nợ.

Các biến thể cần chạy:

| Biến thể | Train augmentation | Ghi chú |
|---|---|---|
| F1 | Synthetic Label 0 + Synthetic Label 1 | Synthetic Label 0 đối chứng |
| F2a | external_real Label 0 + Synthetic Label 1 | Kiểm tra external real Label 0 |
| F2b | external_curated Label 0 + Synthetic Label 1 | Kiểm tra hard-negative/P2P-like external curated |
| F2c | external_real + external_curated Label 0 + Synthetic Label 1 | Kiểm tra toàn bộ external Label 0 |
| F3 | external_real + external_curated Label 0 + Synthetic Label 0 + Synthetic Label 1 | Kiểm tra kết hợp external và synthetic Label 0 |

---

## 5. Chuẩn hóa điều kiện huấn luyện

Tất cả setup phải giữ cố định các thành phần sau:

| Thành phần | Quyết định |
|---|---|
| Model backbone | Dùng cùng một pretrained model |
| Tokenizer | Giữ cố định |
| Max sequence length | Giữ cố định |
| Learning rate | Giữ cố định |
| Batch size | Giữ cố định nếu tài nguyên cho phép |
| Epoch tối đa | Giữ cố định |
| Early stopping | Dùng cùng tiêu chí trên validation |
| Random seed | Chạy cùng danh sách seed |
| Real Test Set | Tuyệt đối cố định |

### 5.1 Không cần train model từ đầu

Khuyến nghị dùng một pretrained model như:

- PhoBERT;
- XLM-R;
- multilingual BERT;
- Vietnamese sentence-transformer + classifier;
- classifier truyền thống trên embedding nếu cần baseline nhẹ.

Quyết định: không yêu cầu train Transformer từ đầu.

Lý do: với vài nghìn tin nhắn, train model từ đầu sẽ chủ yếu đo mức độ thiếu dữ liệu, không đo chất lượng synthetic data. Điều cần kiểm soát là mọi setup dùng cùng backbone, cùng tokenizer và cùng pipeline huấn luyện.

### 5.2 Chạy nhiều random seed

Mỗi setup nên chạy ít nhất:

```text
3 seeds: 42, 123, 2025
```

Nếu đủ tài nguyên, nên chạy 5 seeds.

Báo cáo kết quả theo dạng:

```text
mean ± std
```

Lý do: `Label 1` thật rất ít, nên kết quả dễ dao động theo split, initialization và thứ tự batch. Một seed duy nhất có thể tạo kết luận sai.

---

## 6. Chỉ số đánh giá

### 6.1 Chỉ số chính

| Chỉ số | Lý do sử dụng |
|---|---|
| Macro-F1 | Cân bằng ảnh hưởng giữa hai lớp |
| F1 Label 1 | Đo trực tiếp chất lượng phân loại lớp thiểu số |
| Recall Label 1 | Đo khả năng bắt đúng tin nhắn lừa đảo |
| Precision Label 1 | Kiểm soát báo động sai |
| AUPRC | Phù hợp khi positive class hiếm |
| Confusion matrix | Cho thấy false positive và false negative cụ thể |

### 6.2 Chỉ số phụ

| Chỉ số | Vai trò |
|---|---|
| Accuracy | Chỉ báo cáo tham khảo |
| AUROC | Hữu ích nhưng có thể lạc quan khi dữ liệu mất cân bằng |
| Weighted-F1 | Tham khảo hiệu năng tổng thể |
| Calibration | Cần nếu mô hình dùng xác suất để ra quyết định |

Quyết định: báo cáo `Accuracy`, nhưng không dùng nó làm chỉ số kết luận chính.

Lý do: trong bài toán smishing, bỏ sót `Label 1` thường nghiêm trọng hơn việc đạt accuracy tổng thể cao. Một mô hình có accuracy tốt nhưng recall `Label 1` thấp không phải là mô hình hữu dụng.

---

## 7. Phân tích khoảng cách TSTR

Sau khi có kết quả, cần tính các khoảng cách:

```text
Gap A = TRTR Real-only - TSTR matched
Gap B = TRTR Real-only - TSTR balanced
Gap C = Real + Synthetic Label 1 - TRTR Real-only
Gap D = Label 0 source augmentation - TRTR imbalance handling
```

Nên tính gap theo:

- `Macro-F1`;
- `F1 Label 1`;
- `Recall Label 1`;
- `AUPRC`.

Không nên chỉ tính gap theo `Accuracy`.

| Kết quả | Diễn giải |
|---|---|
| TSTR matched gần TRTR | Synthetic data có tín hiệu miền tốt |
| TSTR matched thấp hơn TRTR nhiều | Synthetic data chưa thay thế được real data |
| TSTR balanced tăng recall nhưng precision giảm mạnh | Synthetic làm mô hình quá nhạy với Label 1 |
| Real + Synthetic vượt Real-only | Synthetic có giá trị augmentation |
| Real + Synthetic vượt TRTR imbalance handling | Synthetic có giá trị thực dụng mạnh |
| Real + Synthetic không cải thiện | Synthetic có thể không thêm tín hiệu mới hoặc có pattern giả |

---

## 8. Kiểm tra rò rỉ và trùng lặp dữ liệu

Trước khi huấn luyện, cần kiểm tra synthetic data có quá gần `Real Test` không.

Các kiểm tra bắt buộc:

- exact duplicate;
- gần trùng lặp sau khi normalize text;
- overlap n-gram;
- similarity bằng embedding;
- kiểm tra thủ công một số cặp synthetic/real có độ tương đồng cao.

Quyết định: nếu synthetic sample quá gần `Real Test`, cần loại khỏi tập train synthetic.

Lý do: nếu synthetic train chứa bản sao hoặc gần bản sao của `Real Test`, điểm TSTR sẽ bị thổi phồng. Khi đó mô hình có thể chỉ ghi nhớ nội dung thay vì học quy luật tổng quát.

Nguyên tắc:

```text
Real Test Set là vùng bất khả xâm phạm.
```

---

## 9. Phân tích lỗi sau đánh giá

Sau khi có kết quả định lượng, cần đọc lại các mẫu `Real Test` bị dự đoán sai.

| Nhóm lỗi | Ý nghĩa |
|---|---|
| False Negative Label 1 | Tin nhắn lừa đảo bị bỏ sót |
| False Positive Label 1 | Tin nhắn hợp lệ bị cảnh báo sai |
| Label 1 đúng sau khi thêm synthetic | Synthetic có thể đã bổ sung pattern hữu ích |
| Label 1 sai sau khi thêm synthetic | Synthetic có thể gây nhiễu hoặc thiếu pattern |
| Lỗi liên quan URL/SĐT/ký tự đặc biệt | Kiểm tra mô hình có học shortcut không |
| Lỗi theo category | Xác định category cần sinh lại hoặc bổ sung |

Lý do: chỉ số tổng hợp như F1 không cho biết synthetic data đang giúp theo cách nào. Phân tích lỗi giúp xác định liệu synthetic data thật sự bổ sung biến thể hữu ích, hay chỉ khiến mô hình học văn phong LLM và các shortcut bề mặt.

---

## 10. Bảng thí nghiệm tổng hợp

| Nhóm | Setup | Train | Validation | Test | Mục đích |
|---|---|---|---|---|---|
| A | TRTR Real-only | Real Train | Real Validation | Real Test | Baseline dữ liệu thật |
| B | TRTR imbalance handling | Real Train + kỹ thuật xử lý imbalance | Real Validation | Real Test | Baseline mạnh hơn cho dữ liệu thật |
| C | TSTR matched distribution | Synthetic có tỷ lệ/kích thước gần Real Train | Real Validation | Real Test | Kiểm tra tín hiệu miền của synthetic |
| D | TSTR balanced synthetic | Synthetic cân bằng hoặc gần cân bằng | Real Validation | Real Test | Kiểm tra synthetic cho lớp thiểu số |
| E | Real + Synthetic Label 1 | Real Train + Synthetic Label 1 | Real Validation | Real Test | Kiểm tra augmentation lớp thiểu số |
| F | Label 0 source augmentation | Real Train + external/synthetic Label 0 + Synthetic Label 1 | Real Validation | Real Test | Kiểm tra nguồn bổ sung Label 0 |

---

## 11. Mẫu bảng báo cáo kết quả

| Setup | Macro-F1 | F1 Label 1 | Recall Label 1 | Precision Label 1 | AUPRC | AUROC | Accuracy |
|---|---:|---:|---:|---:|---:|---:|---:|
| A - TRTR Real-only |  |  |  |  |  |  |  |
| B - TRTR imbalance handling |  |  |  |  |  |  |  |
| C - TSTR matched |  |  |  |  |  |  |  |
| D - TSTR balanced |  |  |  |  |  |  |  |
| E - Real + Synthetic Label 1 |  |  |  |  |  |  |  |
| F - Label 0 source augmentation |  |  |  |  |  |  |  |

Mỗi ô kết quả chính nên báo cáo theo dạng:

```text
mean ± std
```

Ví dụ:

```text
0.812 ± 0.018
```

---

## 12. Tiêu chí kết luận

### 12.1 Synthetic có thể thay thế một phần real data

Kết luận này chỉ nên đưa ra nếu:

- TSTR matched gần TRTR Real-only;
- `F1 Label 1` không giảm nhiều;
- `AUPRC` ổn định;
- confusion matrix không có mẫu lỗi bất thường.

Đây là kết luận mạnh nhất, nhưng cũng khó đạt nhất.

### 12.2 Synthetic hữu ích cho augmentation

Kết luận này phù hợp nếu:

- `Real + Synthetic` vượt `Real-only`;
- `Recall Label 1` tăng;
- `F1 Label 1` tăng hoặc giữ ổn định;
- `Precision Label 1` không giảm quá mạnh;
- kết quả ổn định qua nhiều seed.

Đây là kết luận nhiều khả năng phù hợp nhất với mục tiêu ban đầu của dự án.

### 12.3 Synthetic chưa hữu dụng

Cần kết luận thận trọng nếu:

- TSTR thấp hơn TRTR rõ rệt;
- `Real + Synthetic` không cải thiện so với `Real-only`;
- recall tăng nhưng precision sụp mạnh;
- mô hình tạo nhiều false positive trên tin nhắn hợp lệ;
- phân tích lỗi cho thấy mô hình học shortcut hoặc văn phong giả.

---

## 13. Trình tự triển khai đề xuất

1. Khóa `Real Test Set` bằng stratified split.
2. Kiểm tra duplicate và near-duplicate giữa synthetic data và `Real Test`.
3. Chuẩn hóa pipeline train/evaluate với một model backbone cố định.
4. Chạy Setup A để có TRTR Real-only baseline.
5. Chạy Setup B để có baseline xử lý imbalance.
6. Chạy Setup C để kiểm tra synthetic matched distribution.
7. Chạy Setup D để kiểm tra synthetic balanced.
8. Chạy Setup E với nhiều mức synthetic `Label 1`.
9. Chạy Setup F với các nguồn bổ sung Label 0: synthetic, external ViLexNorm, và kết hợp cả hai.
10. Lặp lại các setup chính với nhiều seed.
11. Tổng hợp bảng kết quả `mean ± std`.
12. Phân tích confusion matrix và lỗi trên `Real Test`.
13. Kết luận synthetic data thuộc mức nào: thay thế một phần, hữu ích cho augmentation, hay chưa hữu ích.

---

## 14. Kết luận phương pháp

Trong bối cảnh bộ dữ liệu SMS bị mất cân bằng mạnh, TSTR không nên được hiểu là một phép so sánh đơn giản giữa:

```text
Real train nhỏ
Synthetic train lớn
```

Thay vào đó, cần đánh giá theo ba lớp:

```text
TRTR: mô hình học từ dữ liệu thật hiện có.
TSTR: mô hình học từ synthetic và bị kiểm tra trên dữ liệu thật.
Real + Synthetic: mô hình học từ dữ liệu thật được bổ sung synthetic.
```

Nếu TSTR cho kết quả gần TRTR, synthetic data có tín hiệu miền tốt. Nếu `Real + Synthetic` vượt `Real-only`, synthetic data có giá trị augmentation. Nếu `Real + Synthetic` vượt cả baseline xử lý imbalance truyền thống, synthetic data có giá trị thực dụng mạnh và có thể được xem là thành phần quan trọng trong pipeline huấn luyện.

Với bộ dữ liệu hiện tại, câu hỏi kết luận nên là:

```text
Synthetic data có làm mô hình nhận diện Label 1 tốt hơn trên Real Test Set không?
```

Đây là câu hỏi phù hợp nhất với lý do tạo dữ liệu ban đầu và cũng là tiêu chuẩn thực dụng nhất để quyết định có nên sử dụng bộ dữ liệu tổng hợp trong huấn luyện mô hình cuối hay không.

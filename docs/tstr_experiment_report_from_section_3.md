# 3. Nguyên tắc thiết kế thí nghiệm

Phần này trình bày cách thiết kế thí nghiệm nhằm đánh giá giá trị thực tế của dữ liệu tạo sinh đối với bài toán phân loại tin nhắn hợp lệ và tin nhắn smishing. Do bộ dữ liệu thật có kích thước nhỏ và mất cân bằng mạnh, việc so sánh trực tiếp giữa dữ liệu thật và dữ liệu tạo sinh có thể dẫn đến kết luận sai lệch. Một mô hình có thể đạt kết quả tốt hơn không phải vì dữ liệu tạo sinh có chất lượng cao hơn, mà chỉ vì nó được huấn luyện trên nhiều mẫu Label 1 hơn.

Vì vậy, các thí nghiệm được chia thành nhiều setup, trong đó mỗi setup trả lời một câu hỏi riêng. Setup A và B đóng vai trò baseline khi chỉ sử dụng dữ liệu thật. Setup C và D kiểm tra khả năng dùng dữ liệu tạo sinh độc lập theo hướng TSTR. Setup E kiểm tra giả thuyết thực dụng hơn: dữ liệu tạo sinh không thay thế hoàn toàn dữ liệu thật, nhưng có thể đóng vai trò augmentation cho lớp Label 1.

Tất cả các setup đều sử dụng cùng một tập Real Validation và Real Test. Real Test Set được khóa cố định ngay từ đầu, chỉ chứa dữ liệu thật và không tham gia vào huấn luyện, chọn checkpoint, tuning threshold hoặc lựa chọn hyperparameter. Cách thiết kế này giúp bảo đảm kết quả cuối phản ánh năng lực tổng quát hóa trên dữ liệu thật, thay vì phản ánh việc mô hình đã nhìn thấy hoặc bị tối ưu gián tiếp theo tập test.

Bộ dữ liệu thật được chia theo stratified split với tỷ lệ 70/15/15 và `split_seed = 0`. Kích thước các tập sau khi chia như sau:


| Tập dữ liệu     | Tổng số mẫu | Label 0 | Label 1 |
| --------------- | ----------- | ------- | ------- |
| Real Train      | 1796        | 1624    | 172     |
| Real Validation | 385         | 348     | 37      |
| Real Test       | 386         | 349     | 37      |


Việc stratify theo nhãn là cần thiết vì Label 1 chỉ chiếm tỷ lệ nhỏ trong dữ liệu thật. Nếu chia ngẫu nhiên không stratify, tập validation hoặc test có thể có quá ít mẫu Label 1, khiến các chỉ số như Recall Label 1, Precision Label 1 và F1 Label 1 dao động mạnh.

Các điều kiện huấn luyện được giữ cố định giữa các setup:


| Thành phần               | Thiết lập                                       |
| ------------------------ | ----------------------------------------------- |
| Backbone                 | `vinai/phobert-base`                            |
| Tiền xử lý tiếng Việt    | ViTokenizer trước khi đưa vào PhoBERT tokenizer |
| Task                     | Binary sequence classification                  |
| Max length               | 128                                             |
| Learning rate            | 2e-5                                            |
| Batch size huấn luyện    | 16                                              |
| Batch size đánh giá      | 32                                              |
| Weight decay             | 0.01                                            |
| Warmup ratio             | 0.1                                             |
| Epoch tối đa             | 10                                              |
| Early stopping           | patience = 3                                    |
| Random seeds             | 42, 123, 2025                                   |
| Tiêu chí chọn checkpoint | F1 Label 1 trên Real Validation                 |


Accuracy chỉ được báo cáo như chỉ số tham khảo, không được dùng làm chỉ số kết luận chính. Trong bài toán smishing, lớp quan trọng hơn là Label 1. Một mô hình có accuracy cao nhưng bỏ sót nhiều tin nhắn smishing vẫn không có giá trị thực dụng cao. Vì vậy, phần đánh giá ưu tiên Macro-F1, F1 Label 1, Recall Label 1, Precision Label 1, AUPRC và confusion matrix.

# 4. Mô tả các thiết lập thí nghiệm

## 4.1. Setup A - TRTR Real-only Baseline

Setup A dùng Real Train để huấn luyện, Real Validation để chọn checkpoint và Real Test để đánh giá cuối cùng. Đây là baseline thực tế khi mô hình chỉ được học từ dữ liệu thật hiện có.

Thiết lập:


| Thành phần | Dữ liệu         |
| ---------- | --------------- |
| Train      | Real Train      |
| Validation | Real Validation |
| Test       | Real Test       |


Setup A không được xem là upper bound tuyệt đối, vì số lượng Label 1 thật trong Real Train chỉ có 172 mẫu. Tuy nhiên, đây là mốc so sánh quan trọng để biết mô hình đạt được mức hiệu năng nào khi không dùng dữ liệu tạo sinh.

## 4.2. Setup B - TRTR với xử lý mất cân bằng

Setup B vẫn chỉ sử dụng dữ liệu thật, nhưng bổ sung kỹ thuật xử lý mất cân bằng. Hai biến thể được sử dụng:


| Biến thể | Mô tả                                                |
| -------- | ---------------------------------------------------- |
| B1       | Class weight                                         |
| B2       | Class weight + threshold tuning trên Real Validation |


Mục đích của Setup B là tạo một baseline mạnh hơn Setup A. Nếu dữ liệu tạo sinh chỉ vượt Setup A nhưng không vượt Setup B, cần thận trọng khi kết luận rằng dữ liệu tạo sinh có giá trị vượt trội so với các kỹ thuật xử lý mất cân bằng truyền thống.

## 4.3. Setup C - TSTR Matched Distribution

Setup C huấn luyện mô hình hoàn toàn bằng dữ liệu tạo sinh, nhưng số lượng và tỷ lệ nhãn được matched với Real Train. Cụ thể, tập train synthetic matched gồm 1796 mẫu, trong đó có 1624 mẫu Label 0 và 172 mẫu Label 1.

Thiết lập:


| Thành phần | Dữ liệu                                |
| ---------- | -------------------------------------- |
| Train      | Synthetic Train matched với Real Train |
| Validation | Real Validation                        |
| Test       | Real Test                              |


Mục đích của Setup C là kiểm tra dữ liệu tạo sinh có thể thay thế dữ liệu thật trong điều kiện công bằng về kích thước và phân phối nhãn hay không. Nếu Setup C đạt kết quả gần Setup A, có thể xem dữ liệu tạo sinh đã học được tín hiệu miền tương đối tốt. Ngược lại, nếu Setup C thấp hơn nhiều, dữ liệu tạo sinh chưa đủ để thay thế dữ liệu thật.

## 4.4. Setup D - TSTR Balanced Synthetic

Setup D cũng huấn luyện mô hình chỉ bằng dữ liệu tạo sinh, nhưng tập train được cân bằng giữa hai lớp. Tập train của Setup D gồm 3996 mẫu, trong đó Label 0 và Label 1 đều có 1998 mẫu.

Thiết lập:


| Thành phần | Dữ liệu                |
| ---------- | ---------------------- |
| Train      | Synthetic balanced 1:1 |
| Validation | Real Validation        |
| Test       | Real Test              |


Mục đích của Setup D là kiểm tra liệu việc bổ sung mạnh Label 1 trong dữ liệu tạo sinh có giúp mô hình học tốt hơn lớp thiểu số hay không. Setup này cho phép phân phối train khác phân phối thật, vì mục tiêu là đánh giá khả năng dữ liệu tạo sinh hỗ trợ bài toán thiếu mẫu Label 1. Tuy nhiên, nếu recall tăng nhưng precision giảm mạnh, điều đó cho thấy mô hình có xu hướng dự đoán Label 1 quá rộng.

## 4.5. Setup E - Real + Synthetic Label 1

Setup E kết hợp Real Train với dữ liệu tạo sinh thuộc Label 1 ở nhiều mức khác nhau. Đây là setup quan trọng nhất về mặt thực dụng, vì mục tiêu ban đầu của dữ liệu tạo sinh là bổ sung biến thể cho lớp smishing vốn có rất ít mẫu thật.


| Biến thể | Synthetic Label 1 bổ sung | Tổng số mẫu train | Label 0 | Label 1 |
| -------- | ------------------------- | ----------------- | ------- | ------- |
| E1       | 500                       | 2296              | 1624    | 672     |
| E2       | 1000                      | 2796              | 1624    | 1172    |
| E3       | 2000                      | 3796              | 1624    | 2172    |
| E4       | 4996                      | 6792              | 1624    | 5168    |


Thiết lập:


| Thành phần | Dữ liệu                        |
| ---------- | ------------------------------ |
| Train      | Real Train + Synthetic Label 1 |
| Validation | Real Validation                |
| Test       | Real Test                      |


Setup E kiểm tra liệu dữ liệu tạo sinh có giá trị như một nguồn augmentation hay không. Trong setup này, Real Train đóng vai trò giữ mô hình bám vào miền dữ liệu thật, còn synthetic Label 1 bổ sung các biến thể tấn công mà dữ liệu thật chưa bao phủ đầy đủ.

# 5. Kiểm tra rò rỉ dữ liệu

Trước khi huấn luyện các setup có sử dụng dữ liệu tạo sinh, cần kiểm tra nguy cơ rò rỉ giữa synthetic train candidates và Real Test Set. Nếu dữ liệu tạo sinh chứa bản sao hoặc gần bản sao của mẫu trong Real Test, kết quả TSTR có thể bị thổi phồng vì mô hình chỉ cần ghi nhớ nội dung thay vì học quy luật tổng quát.

Trong các thí nghiệm hiện tại, kiểm tra rò rỉ được thực hiện theo hai mức:

- exact duplicate theo nội dung gốc;
- normalized duplicate sau khi lowercase và chuẩn hóa khoảng trắng.

Các leakage report của Setup C, D và E không phát hiện duplicate trực tiếp giữa synthetic candidates và Real Test Set. Điều này giúp giảm rủi ro data leakage ở mức trùng lặp bề mặt.

Tuy nhiên, kiểm tra hiện tại vẫn có hạn chế. Các bước kiểm tra chưa bao gồm near-duplicate theo embedding similarity hoặc kiểm tra tương đồng ngữ nghĩa sâu. Vì vậy, kết quả cần được diễn giải thận trọng, đặc biệt với các mẫu synthetic có cấu trúc câu gần với tin nhắn thật.

# 6. Kết quả thực nghiệm

## 6.1. Kết quả Setup A và Setup B


| Setup                         | Macro-F1        | F1 Label 1      | Recall Label 1  | Precision Label 1 | AUPRC           |
| ----------------------------- | --------------- | --------------- | --------------- | ----------------- | --------------- |
| A - Real-only                 | 0.9506 ± 0.0032 | 0.9108 ± 0.0058 | 0.9189 ± 0.0000 | 0.9028 ± 0.0114   | 0.9766 ± 0.0022 |
| B1 - Class weight             | 0.9510 ± 0.0030 | 0.9116 ± 0.0053 | 0.9279 ± 0.0127 | 0.8962 ± 0.0180   | 0.9854 ± 0.0028 |
| B2 - Class weight + threshold | 0.9423 ± 0.0091 | 0.8960 ± 0.0162 | 0.9279 ± 0.0127 | 0.8674 ± 0.0370   | 0.9854 ± 0.0028 |


Setup A cho thấy baseline real-only đã đạt hiệu năng cao trên Real Test, với F1 Label 1 đạt 0.9108 và Recall Label 1 đạt 0.9189. Điều này cho thấy dù dữ liệu thật ít, mô hình PhoBERT vẫn học được ranh giới phân loại tương đối tốt khi train và test đều thuộc miền dữ liệu thật.

So với Setup A, B1 cải thiện rất nhẹ F1 Label 1 từ 0.9108 lên 0.9116 và tăng Recall Label 1 từ 0.9189 lên 0.9279. Tuy nhiên, Precision Label 1 giảm từ 0.9028 xuống 0.8962. Điều này phù hợp với kỳ vọng của class weight: mô hình nhạy hơn với lớp thiểu số, nhưng có thể đánh đổi bằng việc tăng false positive.

B2 không tốt hơn B1. Mặc dù Recall Label 1 giữ ở mức 0.9279, Precision Label 1 giảm xuống 0.8674, khiến F1 Label 1 giảm còn 0.8960. Kết quả này cho thấy threshold tuning trong thiết lập hiện tại làm mô hình dự đoán Label 1 rộng hơn mức cần thiết.

## 6.2. Kết quả Setup C và Setup D


| Setup             | Macro-F1        | F1 Label 1      | Recall Label 1  | Precision Label 1 | AUPRC           |
| ----------------- | --------------- | --------------- | --------------- | ----------------- | --------------- |
| C - TSTR matched  | 0.5975 ± 0.0353 | 0.3014 ± 0.0508 | 0.4054 ± 0.1147 | 0.2608 ± 0.0832   | 0.3495 ± 0.0683 |
| D - TSTR balanced | 0.7041 ± 0.0487 | 0.4938 ± 0.0716 | 0.7117 ± 0.0709 | 0.3902 ± 0.0978   | 0.6415 ± 0.0234 |


Setup C suy giảm mạnh so với Setup A. F1 Label 1 giảm từ 0.9108 xuống 0.3014, Macro-F1 giảm từ 0.9506 xuống 0.5975 và AUPRC giảm từ 0.9766 xuống 0.3495. Kết quả này cho thấy dữ liệu tạo sinh matched chưa thể thay thế dữ liệu thật khi được dùng độc lập.

Setup D cải thiện rõ rệt so với Setup C nhờ cân bằng số lượng Label 0 và Label 1 trong train set. Recall Label 1 tăng từ 0.4054 lên 0.7117, F1 Label 1 tăng từ 0.3014 lên 0.4938 và AUPRC tăng từ 0.3495 lên 0.6415. Tuy nhiên, Precision Label 1 vẫn chỉ đạt 0.3902, thấp hơn rất nhiều so với Setup A/B. Điều này cho thấy synthetic-only balanced giúp mô hình bắt được nhiều mẫu smishing hơn, nhưng đồng thời làm mô hình tạo ra nhiều cảnh báo sai trên tin nhắn hợp lệ.

Nhìn chung, Setup C và D cho thấy tồn tại domain gap đáng kể giữa synthetic train và Real Test. Dữ liệu tạo sinh có chứa một phần tín hiệu hữu ích cho Label 1, nhưng khi thiếu dữ liệu thật làm điểm neo, mô hình chưa học được ranh giới phân loại ổn định trên miền thật.

## 6.3. Kết quả Setup E


| Variant | Synthetic L1 | Macro-F1        | F1 Label 1      | Recall Label 1  | Precision Label 1 | AUPRC           |
| ------- | ------------ | --------------- | --------------- | --------------- | ----------------- | --------------- |
| E1      | 500          | 0.9518 ± 0.0100 | 0.9132 ± 0.0175 | 0.9369 ± 0.0337 | 0.8954 ± 0.0622   | 0.9617 ± 0.0095 |
| E2      | 1000         | 0.9538 ± 0.0112 | 0.9167 ± 0.0197 | 0.9279 ± 0.0337 | 0.9111 ± 0.0665   | 0.9460 ± 0.0188 |
| E3      | 2000         | 0.9434 ± 0.0035 | 0.8978 ± 0.0064 | 0.9099 ± 0.0127 | 0.8861 ± 0.0102   | 0.9587 ± 0.0061 |
| E4      | 4996         | 0.9546 ± 0.0114 | 0.9178 ± 0.0204 | 0.9009 ± 0.0255 | 0.9376 ± 0.0466   | 0.9600 ± 0.0028 |


Khi synthetic Label 1 được kết hợp với Real Train, kết quả cải thiện rõ rệt so với các setup synthetic-only và đạt mức cạnh tranh với Setup A/B. Điều này cho thấy dữ liệu tạo sinh phù hợp hơn với vai trò augmentation thay vì replacement.

E1 đạt Recall Label 1 cao nhất trong nhóm E, với 0.9369. Điều này cho thấy bổ sung 500 mẫu synthetic Label 1 giúp mô hình phát hiện thêm các mẫu smishing, nhưng Precision Label 1 giảm nhẹ so với Setup A. E2 đạt sự cân bằng tốt hơn giữa recall và precision, với F1 Label 1 = 0.9167, cao hơn Setup A và B1. E4 đạt F1 Label 1 cao nhất trong nhóm E, 0.9178, đồng thời có Precision Label 1 cao nhất, 0.9376. Điều này cho thấy khi dùng toàn bộ synthetic Label 1, mô hình ít tạo false positive hơn, nhưng Recall Label 1 giảm xuống 0.9009.

E3 là biến thể kém nhất trong nhóm E, với F1 Label 1 = 0.8978, thấp hơn cả Setup A. Kết quả này cho thấy việc tăng số lượng synthetic không tạo ra cải thiện tuyến tính. Một lượng synthetic lớn hơn không nhất thiết tốt hơn nếu dữ liệu bổ sung làm thay đổi phân phối train hoặc đưa vào các pattern chưa phù hợp với Real Test.

# 7. Phân tích confusion matrix

Do Real Test có 37 mẫu Label 1 và 349 mẫu Label 0, confusion matrix là công cụ trực quan quan trọng để đọc kết quả. Các chỉ số như F1 hoặc AUPRC cho biết hiệu năng tổng hợp, nhưng confusion matrix cho thấy mô hình đang sai theo hướng nào: bỏ sót tin nhắn smishing hay cảnh báo nhầm tin nhắn hợp lệ.

Trong báo cáo, không cần đưa toàn bộ confusion matrix của tất cả setup và biến thể, vì điều đó có thể làm phần phân tích bị dàn trải. Nên chọn các hình đại diện cho từng câu hỏi thí nghiệm:


| Hình nên đưa | Vai trò trong phân tích                                                 |
| ------------ | ----------------------------------------------------------------------- |
| Setup A      | Baseline real-only để làm mốc so sánh                                   |
| Setup C      | TSTR matched, kiểm tra khả năng thay thế real data                      |
| Setup D      | TSTR balanced, kiểm tra tác động của synthetic-only cân bằng nhãn       |
| Setup E2     | Biến thể augmentation cân bằng giữa precision và recall                 |
| Setup E4     | Biến thể augmentation có precision cao nhất và false positive thấp nhất |


Các confusion matrix của Setup B, E1 và E3 vẫn có thể đặt ở phụ lục. Trong phần chính, chỉ cần nhắc đến chúng khi so sánh định tính: B1/B2 là baseline xử lý imbalance, E1 thiên về recall, còn E3 là ví dụ cho thấy thêm nhiều synthetic hơn không nhất thiết tốt hơn.

Confusion matrix của Setup A

Confusion matrix của Setup A cho thấy mô hình real-only đã có ranh giới phân loại khá ổn định trên Real Test. Phần lớn mẫu Label 0 được nhận diện đúng, đồng thời số mẫu Label 1 bị bỏ sót ở mức thấp. Đây là mốc quan trọng để so sánh với các setup còn lại, vì nó phản ánh năng lực của mô hình khi chỉ học từ dữ liệu thật.

Confusion matrix của Setup C

Ở Setup C, mô hình được huấn luyện chỉ bằng dữ liệu synthetic matched với Real Train về kích thước và tỷ lệ nhãn. Confusion matrix cho thấy số lỗi tăng rõ rệt ở cả hai hướng, đặc biệt là false positive và false negative. Mô hình vừa bỏ sót nhiều mẫu smishing thật, vừa dự đoán nhầm nhiều tin nhắn hợp lệ thành smishing. Kết quả này cho thấy synthetic matched chưa đủ để thay thế dữ liệu thật: dù số lượng và tỷ lệ nhãn được giữ công bằng, phân phối synthetic vẫn chưa tái tạo tốt miền dữ liệu thật.

Confusion matrix của Setup D

So với Setup C, Setup D làm giảm đáng kể số false negative của Label 1. Điều này phù hợp với mục tiêu của synthetic balanced: khi mô hình được thấy nhiều mẫu Label 1 hơn, khả năng phát hiện smishing tăng lên. Tuy nhiên, hình confusion matrix cũng cho thấy số false positive vẫn còn cao. Nói cách khác, mô hình trở nên nhạy hơn với smishing nhưng đồng thời mở rộng vùng dự đoán Label 1 quá mức, khiến nhiều tin nhắn hợp lệ bị cảnh báo nhầm. Đây là dấu hiệu cho thấy synthetic-only balanced có thể cải thiện recall, nhưng chưa đủ để tạo ranh giới phân loại ổn định.

Confusion matrix của Setup E2

Setup E2 thể hiện vai trò của synthetic data trong bối cảnh augmentation. Khi Real Train vẫn được giữ lại và chỉ bổ sung thêm 1000 mẫu synthetic Label 1, confusion matrix gần với Setup A hơn nhiều so với Setup C/D. Số false positive được kiểm soát, trong khi số false negative vẫn ở mức thấp. Điều này cho thấy dữ liệu thật đóng vai trò neo mô hình vào miền real, còn synthetic Label 1 có thể bổ sung thêm tín hiệu cho lớp thiểu số mà không làm mô hình lệch mạnh khỏi phân phối thật.

Confusion matrix của Setup E4

Setup E4 là biến thể dùng toàn bộ synthetic Label 1. Confusion matrix của E4 cho thấy mô hình kiểm soát false positive tốt nhất trong nhóm E, phù hợp với việc Precision Label 1 của E4 là cao nhất. Tuy nhiên, E4 không phải biến thể có recall cao nhất; số false negative cao hơn E1/E2. Điều này phản ánh một trade-off quan trọng: thêm nhiều synthetic Label 1 có thể giúp mô hình thận trọng hơn khi dự đoán smishing, nhưng không nhất thiết làm tăng khả năng bắt hết các mẫu smishing thật.

Nhìn tổng thể, các confusion matrix cho thấy ba xu hướng chính. Thứ nhất, Setup C và D xác nhận rằng synthetic data chưa phù hợp để dùng độc lập thay thế real data, vì lỗi tăng mạnh khi mô hình không được học từ dữ liệu thật. Thứ hai, Setup D cho thấy cân bằng synthetic giúp tăng khả năng phát hiện Label 1 nhưng đánh đổi bằng nhiều cảnh báo sai. Thứ ba, các biến thể Setup E cho thấy synthetic Label 1 có giá trị hơn khi được dùng như augmentation: Real Train giữ ranh giới miền thật, còn synthetic data bổ sung tín hiệu cho lớp smishing.

Vì vậy, phân tích confusion matrix củng cố kết luận từ các chỉ số định lượng: dữ liệu tạo sinh chưa nên được xem là nguồn thay thế dữ liệu thật, nhưng có thể hữu ích khi được bổ sung có kiểm soát vào Real Train, đặc biệt để hỗ trợ lớp Label 1.

# 8. Thảo luận

## 8.1. Dữ liệu tạo sinh chưa thể thay thế dữ liệu thật

Kết quả Setup C và D cho thấy dữ liệu tạo sinh khi dùng độc lập chưa tái tạo đủ tốt phân phối của dữ liệu thật. Setup C, dù matched với Real Train về kích thước và tỷ lệ nhãn, vẫn suy giảm mạnh so với Setup A. Setup D cải thiện recall nhờ cân bằng nhãn, nhưng precision vẫn thấp và false positive tăng mạnh.

Điều này không có nghĩa dữ liệu tạo sinh hoàn toàn kém chất lượng. Kết quả nên được hiểu là dữ liệu tạo sinh hiện tại chưa đủ để thay thế real data trong bài toán smishing tiếng Việt. Synthetic data có thể học được một số tín hiệu liên quan đến Label 1, nhưng vẫn tồn tại khoảng cách về văn phong, phân phối độ dài, cấu trúc URL/số điện thoại, sender type và các mẫu hợp lệ dễ nhầm.

## 8.2. Dữ liệu tạo sinh có giá trị trong vai trò augmentation

Setup E cho thấy khi kết hợp với Real Train, synthetic Label 1 giúp mô hình đạt kết quả cạnh tranh và trong một số biến thể vượt nhẹ baseline real-only. E2 và E4 đều có F1 Label 1 cao hơn Setup A. E1 giúp tăng Recall Label 1, còn E4 giúp tăng Precision Label 1 và giảm false positive.

Kết quả này phù hợp với giả thuyết ban đầu: dữ liệu tạo sinh nên được sử dụng như nguồn bổ sung cho lớp thiểu số, không phải nguồn thay thế hoàn toàn dữ liệu thật. Real data giữ vai trò neo miền thật, còn synthetic data mở rộng không gian biến thể của Label 1.

## 8.3. Số lượng synthetic cần được kiểm soát

Kết quả Setup E cho thấy không phải càng thêm nhiều synthetic thì hiệu năng càng tăng. E3 dùng 2000 mẫu synthetic Label 1 nhưng có kết quả thấp hơn E1, E2 và E4. Điều này cho thấy tác động của synthetic phụ thuộc vào phân phối, chất lượng và mức độ phù hợp của các mẫu được thêm, không chỉ phụ thuộc vào số lượng.

Nếu mục tiêu ưu tiên phát hiện nhiều smishing hơn, E1 là biến thể đáng chú ý vì đạt Recall Label 1 cao nhất. Nếu mục tiêu ưu tiên cân bằng giữa recall và precision, E2 là lựa chọn hợp lý. Nếu mục tiêu giảm cảnh báo sai, E4 có ưu thế nhờ Precision Label 1 cao nhất và số false positive thấp nhất.

# 9. Hạn chế

Các kết quả hiện tại cần được diễn giải trong phạm vi một số hạn chế. Thứ nhất, Real Test Set còn nhỏ, đặc biệt chỉ có 37 mẫu Label 1. Điều này làm các chỉ số trên lớp thiểu số dễ dao động khi thay đổi seed hoặc split. Thứ hai, mỗi setup mới được chạy trên 3 random seed; số seed này đủ để giảm bớt nhiễu ban đầu nhưng chưa đủ mạnh để kết luận thống kê chắc chắn.

Thứ ba, kiểm tra leakage mới dừng ở exact duplicate và normalized duplicate. Chưa có kiểm tra near-duplicate bằng embedding similarity hoặc rà soát thủ công các cặp synthetic-real có độ tương đồng cao. Thứ tư, phân tích lỗi thủ công trên từng false positive và false negative chưa được hoàn tất, nên chưa thể xác định chính xác nhóm nội dung nào được synthetic cải thiện hoặc gây nhiễu.

Cuối cùng, Setup F chưa được hoàn tất. Do đó, báo cáo hiện tại mới đánh giá tác động của việc bổ sung synthetic Label 1, chưa đánh giá đầy đủ việc bổ sung synthetic cho cả hai lớp hoặc bổ sung external curated Label 0 để ổn định ranh giới phân loại.

# 10. Kết luận sơ bộ

Nhóm thí nghiệm A-E cho thấy dữ liệu tạo sinh chưa phù hợp để thay thế hoàn toàn dữ liệu thật trong bài toán phân loại smishing tiếng Việt. Khi huấn luyện chỉ bằng synthetic data, mô hình suy giảm mạnh trên Real Test, đặc biệt ở F1 Label 1, Precision Label 1 và AUPRC. Điều này phản ánh domain gap đáng kể giữa dữ liệu tạo sinh và dữ liệu thật.

Tuy nhiên, khi synthetic Label 1 được sử dụng như dữ liệu augmentation cho Real Train, mô hình đạt kết quả cạnh tranh với baseline real-only và trong một số biến thể vượt nhẹ F1 Label 1 hoặc Precision Label 1. Điều này cho thấy dữ liệu tạo sinh có giá trị khoa học và thực dụng khi được dùng có kiểm soát để bổ sung cho lớp thiểu số.


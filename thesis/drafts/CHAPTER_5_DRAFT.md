# CHƯƠNG 5. KẾT QUẢ VÀ PHÂN TÍCH

## 5.1. RQ1: Mô hình nào đạt hiệu quả tốt nhất?

Bảng 5.1 trình bày kết quả của 17 cấu hình trên tập dev và test theo bốn độ đo Macro-F1, F1 Label 1, Recall Label 1 và PR-AUC. Các mô hình được chia thành ba nhóm gồm neural network cấp ký tự (character-level), encoder PLM được fine-tune toàn phần và LLM được fine-tune hiệu quả tham số bằng LoRA. Trong phần này, kết quả dev được sử dụng để so sánh và lựa chọn mô hình; kết quả test chỉ được xem xét sau đó nhằm kiểm tra liệu xu hướng quan sát trên dev có được duy trì hay không.

**Bảng 5.1: Kết quả benchmark của 17 cấu hình mô hình trên tập dev và test**

| Nhóm mô hình | Tên mô hình / Cấu hình | Split | Macro-F1 | F1 Label 1 | Recall Label 1 | PR-AUC |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Character-level** | BiLSTM | dev | 0,8984 | 0,8108 | 0,8108 | 0,8378 |
| | | test | 0,8471 | 0,7143 | 0,6757 | 0,7925 |
| | BiLSTM distilled fr PhoBERT-base | dev | 0,8839 | 0,7838 | 0,7838 | 0,8241 |
| | | test | 0,8671 | 0,7532 | 0,7838 | 0,7273 |
| | TextCNN | dev | 0,9170 | 0,8451 | 0,8108 | 0,8529 |
| | | test | 0,9129 | 0,8378 | 0,8378 | 0,8852 |
| | TextCNN distilled fr PhoBERT-base | dev | 0,9129 | 0,8378 | 0,8378 | 0,8818 |
| | | test | 0,9189 | 0,8500 | 0,9189 | 0,8776 |
| **Fine-tuned PLM** | CafeBERT | dev | 0,9472 | 0,9014 | 0,8649 | 0,9477 |
| | | test | 0,9355 | 0,8800 | 0,8919 | 0,9261 |
| | DistilBERT multilingual | dev | 0,9385 | 0,8861 | **0,9459** | 0,8959 |
| | | test | 0,9150 | 0,8421 | 0,8649 | 0,8421 |
| | PhoBERT-base | dev | 0,8750 | 0,7671 | 0,7568 | 0,8439 |
| | | test | 0,9068 | 0,8267 | 0,8378 | 0,9191 |
| | PhoBERT-large | dev | 0,8975 | 0,8101 | 0,8649 | 0,8648 |
| | | test | 0,9370 | 0,8831 | 0,9189 | 0,9248 |
| | ViCLSR | dev | 0,9419 | 0,8919 | 0,8919 | 0,9441 |
| | | test | 0,9447 | 0,8974 | 0,9459 | 0,9457 |
| | VisoBERT | dev | 0,8958 | 0,8056 | 0,7838 | 0,8866 |
| | | test | 0,9009 | 0,8158 | 0,8378 | 0,8442 |
| | XLM-RoBERTa-base | dev | 0,9090 | 0,8312 | 0,8649 | 0,9212 |
| | | test | 0,9150 | 0,8421 | 0,8649 | 0,8701 |
| | XLM-RoBERTa-large | dev | 0,9211 | 0,8533 | 0,8649 | 0,9294 |
| | | test | 0,9419 | 0,8919 | 0,8919 | 0,9259 |
| | mBERT | dev | 0,9338 | 0,8767 | 0,8649 | 0,8745 |
| | | test | 0,9090 | 0,8312 | 0,8649 | 0,9198 |
| **LoRA LLM** | Gemma 2B | dev | **0,9553** | **0,9167** | 0,8919 | 0,8965 |
| | | test | **0,9585** | **0,9231** | **0,9730** | **0,9853** |
| | Gemma 3 1B | dev | 0,9389 | 0,8857 | 0,8378 | 0,9405 |
| | | test | 0,9472 | 0,9014 | 0,8649 | 0,9183 |
| | Qwen2.5 0.5B | dev | 0,9433 | 0,8947 | 0,9189 | **0,9648** |
| | | test | 0,9248 | 0,8608 | 0,9189 | 0,9489 |
| | Qwen3 0.6B | dev | 0,9236 | 0,8571 | 0,8108 | 0,9262 |
| | | test | 0,9485 | 0,9041 | 0,8919 | 0,9688 |

*Ghi chú: In đậm thể hiện giá trị tốt nhất trong cột tương ứng.*

Xét theo tiêu chí chính là Macro-F1 trên dev, Gemma 2B đạt kết quả cao nhất với 0,9553. Mô hình này đồng thời đứng đầu về F1 Label 1 với 0,9167, cho thấy sự cân bằng tốt nhất giữa hiệu năng trên hai nhãn và chất lượng phân loại lớp smishing tại ngưỡng 0,5. Confusion matrix tương ứng gồm 2 FP và 4 FN trên dev. Kết quả này đưa Gemma 2B trở thành mô hình được ưu tiên theo tiêu chí tổng thể của benchmark.

Tuy nhiên, Gemma 2B không đứng đầu ở mọi độ đo. Recall Label 1 cao nhất trên dev thuộc về DistilBERT multilingual với 0,9459, tương ứng phát hiện đúng 35 trong 37 mẫu smishing và chỉ bỏ sót 2 mẫu. Đổi lại, mô hình tạo ra 7 FP và đạt F1 Label 1 bằng 0,8861, thấp hơn Gemma 2B. Qwen2.5 0.5B đứng đầu về PR-AUC với 0,9648, đồng thời đạt Recall Label 1 bằng 0,9189. Điều này cho thấy mô hình xếp hạng các mẫu smishing tốt trên nhiều mức ngưỡng, dù Macro-F1 tại ngưỡng 0,5 đạt 0,9433 và đứng sau Gemma 2B cùng CafeBERT.

Sự khác biệt trên dẫn đến ba cách nhìn bổ sung thay vì một khái niệm “tốt nhất” duy nhất. Gemma 2B là mô hình cân bằng tổng thể tốt nhất theo Macro-F1 và F1 Label 1; DistilBERT multilingual phù hợp hơn nếu ưu tiên tối đa Recall tại ngưỡng hiện tại; còn Qwen2.5 0.5B có chất lượng xếp hạng xác suất tốt nhất theo PR-AUC. Theo nguyên tắc đã xác lập ở Chương 4, Macro-F1 trên dev vẫn là tiêu chí lựa chọn chính, trong khi Recall và PR-AUC được dùng để mô tả các trade-off vận hành.

Trong nhóm encoder PLM, CafeBERT đạt Macro-F1 cao nhất trên dev với 0,9472 và F1 Label 1 bằng 0,9014. Mô hình chỉ tạo 2 FP và 5 FN, thể hiện xu hướng dự đoán thận trọng hơn DistilBERT multilingual. ViCLSR theo sát với Macro-F1 bằng 0,9419, F1 Label 1 bằng 0,8919 và PR-AUC bằng 0,9441. Hai kết quả này cho thấy các mô hình được tiền huấn luyện trên tiếng Việt hoặc miền văn bản có tính phi chuẩn có thể cạnh tranh tốt trong bài toán smishing, nhưng lợi thế này không xuất hiện đồng đều ở mọi mô hình cùng nhóm: VisoBERT chỉ đạt Macro-F1 bằng 0,8958 và F1 Label 1 bằng 0,8056.

Các encoder đa ngữ cũng cho kết quả không đồng nhất. DistilBERT multilingual đạt Recall cao nhất toàn benchmark nhưng PR-AUC chỉ bằng 0,8959. mBERT đạt Macro-F1 0,9338 và F1 Label 1 0,8767, trong khi XLM-RoBERTa-base đạt lần lượt 0,9090 và 0,8312. Phiên bản XLM-RoBERTa-large cải thiện hai độ đo này lên 0,9211 và 0,8533. Như vậy, tri thức đa ngữ có thể chuyển giao hiệu quả sang smishing tiếng Việt, nhưng hiệu năng còn phụ thuộc đáng kể vào kiến trúc, quy mô và miền tiền huấn luyện.

So sánh trong cùng họ mô hình cho thấy phiên bản large đều cải thiện so với phiên bản base trong hai cặp được khảo sát. PhoBERT-large cao hơn PhoBERT-base 0,0225 điểm Macro-F1, 0,0430 điểm F1 Label 1 và 0,1081 điểm Recall Label 1 trên dev. XLM-RoBERTa-large cũng cao hơn bản base 0,0121 điểm Macro-F1 và 0,0222 điểm F1 Label 1, dù Recall không thay đổi. Kết quả này cho thấy quy mô lớn hơn có thể mang lại lợi ích trong cùng một họ kiến trúc. Tuy nhiên, quy mô không quyết định toàn bộ thứ hạng: CafeBERT và ViCLSR vẫn vượt cả PhoBERT-large và XLM-RoBERTa-large về Macro-F1 trên dev.

Kết quả của nhóm LLM tiếp tục cho thấy số lượng tham số lớn hơn không tự động bảo đảm ưu thế tuyệt đối. Gemma 2B đứng đầu benchmark, nhưng Qwen2.5 0.5B — có quy mô nhỏ hơn đáng kể — vẫn đứng thứ ba về Macro-F1 trên dev và đứng đầu về PR-AUC. Ngược lại, Qwen3 0.6B đạt Macro-F1 0,9236, thấp hơn Qwen2.5 0.5B. Trong cùng họ Gemma, Gemma 2B vượt Gemma 3 1B ở cả bốn độ đo dev. Do cả bốn LLM sử dụng chung cấu hình LoRA, kết quả cho thấy lựa chọn mô hình nền có ảnh hưởng rõ rệt; không thể suy ra hiệu năng chỉ từ quy mô danh nghĩa.

Nhóm character-level có hiệu năng thấp hơn hai nhóm pretrained khi xét các mô hình đứng đầu. TextCNN hard-label là cấu hình tốt nhất của nhóm trên dev với Macro-F1 bằng 0,9170 và F1 Label 1 bằng 0,8451. BiLSTM đạt lần lượt 0,8984 và 0,8108. Khoảng cách giữa TextCNN và BiLSTM gợi ý rằng các mẫu ký tự cục bộ có thể hữu ích hơn biểu diễn tuần tự trong thiết lập hiện tại. Dù vậy, TextCNN vẫn thấp hơn Gemma 2B 0,0383 điểm Macro-F1 và thấp hơn CafeBERT 0,0302 điểm. Kết quả này thể hiện mức đánh đổi về chất lượng của mô hình gọn nhẹ; ý nghĩa triển khai của mức đánh đổi sẽ được đánh giá cùng độ trễ, kích thước và bộ nhớ sau khi hoàn thành benchmark tài nguyên.

Ảnh hưởng của distillation không đồng nhất giữa hai kiến trúc student. Trên dev, BiLSTM distilled thấp hơn BiLSTM hard-label 0,0145 điểm Macro-F1, 0,0270 điểm F1 Label 1 và 0,0270 điểm Recall Label 1. Như vậy, soft target từ PhoBERT-base không cải thiện BiLSTM trong tiêu chí lựa chọn chính. Với TextCNN, phiên bản distilled cũng thấp hơn hard-label 0,0041 điểm Macro-F1 và 0,0072 điểm F1 Label 1, nhưng Recall tăng từ 0,8108 lên 0,8378 và PR-AUC tăng từ 0,8529 lên 0,8818. Distillation trong trường hợp này làm mô hình nhạy hơn với lớp smishing và cải thiện chất lượng xếp hạng, nhưng chưa cải thiện cân bằng tổng thể tại ngưỡng 0,5.

Kết quả distillation cần được diễn giải tương đối với năng lực của teacher. PhoBERT-base chỉ đạt Macro-F1 0,8750 và F1 Label 1 0,7671 trên dev, thấp hơn cả hai student TextCNN. Điều này giới hạn lượng thông tin hữu ích mà soft target có thể truyền sang student và có thể giải thích vì sao cải thiện không đồng đều. Vì vậy, kết quả hiện tại không ủng hộ kết luận rằng distillation luôn nâng cao chất lượng dự đoán; giá trị rõ ràng hơn của phương pháp cần được xem xét trong mối quan hệ giữa hiệu năng được giữ lại và tài nguyên triển khai được tiết kiệm.

Để đánh giá liệu các student có tạo ra lợi ích triển khai thực tế hay không, PhoBERT-base, BiLSTM distilled và TextCNN distilled được đo lại trên benchmark dev split trong cùng môi trường CPU (sử dụng một luồng xử lý). Độ trễ được đo với batch size 1 sau ba lượt warm-up và 20 lần lặp; throughput được đo với batch size 128. Các metric chất lượng được tính lại từ dự đoán của chính checkpoint được đo, nhờ đó bảo đảm bảng tài nguyên và bảng benchmark sử dụng cùng mô hình.

**Bảng 5.2: So sánh chất lượng dự đoán và chi phí triển khai của PhoBERT-base với các student distilled trên benchmark dev split**

| Mô hình | Tham số | Kích thước (MB) | Latency (ms/tin) | Throughput (tin/s) | Peak RAM (MB) | Macro-F1 | F1 L1 | Recall L1 | PR-AUC |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **PhoBERT-base** | 134.999.810 | 516,95 | 248,14 | 4,20 | 1.788,75 | 0,8750 | 0,7671 | 0,7568 | 0,8439 |
| **BiLSTM distilled** | 80.065 | 0,314 | 2,57 | 1.004,88 | 400,00 | 0,8839 | 0,7838 | 0,7838 | 0,8241 |
| **TextCNN distilled** | 87.553 | 0,342 | 1,62 | 1.001,77 | 407,89 | 0,9129 | 0,8378 | 0,8378 | 0,8818 |

So với teacher, BiLSTM distilled giảm khoảng 1.686 lần số tham số và 1.648 lần kích thước checkpoint. Độ trễ CPU giảm từ 248,14 xuống 2,57 ms mỗi tin nhắn, tương ứng nhanh hơn khoảng 96,5 lần; throughput tăng từ 4,20 lên khoảng 1.004,88 tin nhắn/giây. Peak RAM giảm khoảng 77,6%. Mức tiết kiệm này không đi kèm suy giảm ở các metric phụ thuộc ngưỡng trên dev: Macro-F1 tăng 0,0088 điểm, F1 Label 1 tăng 0,0167 và Recall tăng 0,0270. Tuy nhiên, PR-AUC giảm 0,0198, cho thấy chất lượng xếp hạng xác suất trên nhiều ngưỡng chưa được bảo toàn hoàn toàn.

TextCNN distilled tạo ra trade-off thuận lợi hơn. Mô hình giảm khoảng 1.542 lần số tham số và 1.513 lần kích thước checkpoint so với PhoBERT-base. Độ trễ chỉ còn 1,62 ms mỗi tin nhắn, nhanh hơn teacher khoảng 153,6 lần, trong khi peak RAM giảm khoảng 77,2%. Đồng thời, TextCNN distilled cao hơn teacher 0,0379 điểm Macro-F1, 0,0707 điểm F1 Label 1, 0,0811 điểm Recall Label 1 và 0,0379 điểm PR-AUC trên dev. Trong thiết lập này, student không chỉ nhẹ hơn mà còn vượt teacher ở cả bốn độ đo.

Kết quả trên test cho thấy lợi ích chất lượng của hai student không ổn định như nhau. BiLSTM distilled thấp hơn teacher 0,0397 điểm Macro-F1, 0,0734 điểm F1 Label 1, 0,0541 điểm Recall và 0,1918 điểm PR-AUC. Ngược lại, TextCNN distilled vẫn cao hơn teacher 0,0121 điểm Macro-F1, 0,0233 điểm F1 Label 1 và 0,0811 điểm Recall, dù PR-AUC thấp hơn 0,0415. Do đó, BiLSTM distilled chủ yếu mang lại lợi ích tài nguyên nhưng đánh đổi chất lượng tổng quát hóa, trong khi TextCNN distilled duy trì trade-off thuyết phục hơn giữa chất lượng và chi phí triển khai.

Việc student vượt teacher ở một số metric không có nghĩa distillation đã tạo ra một mô hình có năng lực biểu diễn tổng quát hơn PhoBERT-base trong mọi điều kiện. Student khác teacher về kiến trúc, biểu diễn ký tự và hàm mất mát; hơn nữa mỗi split chỉ có 37 mẫu Label 1. Kết quả nên được hiểu là trong benchmark hiện tại, TextCNN distilled tận dụng tốt cả nhãn cứng và soft target để đạt điểm vận hành tốt hơn teacher, đồng thời có chi phí suy luận thấp hơn đáng kể.

Sau khi các nhận xét được hình thành từ dev, kết quả test được sử dụng để kiểm tra mức độ duy trì xu hướng. Gemma 2B tiếp tục đứng đầu về Macro-F1 (0,9585), F1 Label 1 (0,9231), Recall Label 1 (0,9730) và PR-AUC (0,9853). Mô hình chỉ bỏ sót 1 trong 37 mẫu smishing trên test, dù số FP tăng từ 2 trên dev lên 5 trên test. Việc Gemma 2B giữ vị trí dẫn đầu trên cả hai split củng cố lựa chọn mô hình theo dev.

Một số mô hình có thứ hạng thay đổi đáng kể trên test. Qwen3 0.6B tăng Macro-F1 từ 0,9236 lên 0,9485 và trở thành mô hình đứng thứ hai trên test; PhoBERT-large tăng từ 0,8975 lên 0,9370; trong khi Qwen2.5 0.5B giảm từ 0,9433 xuống 0,9248 và CafeBERT giảm từ 0,9472 xuống 0,9355. BiLSTM có mức giảm rõ nhất, từ Macro-F1 0,8984 xuống 0,8471 và Recall Label 1 từ 0,8108 xuống 0,6757.

Những biến động này không nên được hiểu là mô hình “cải thiện” sau khi chuyển sang test. Dev và test có cùng quy mô nhưng chỉ chứa 37 mẫu Label 1; một dự đoán smishing tương ứng khoảng 2,70 điểm phần trăm Recall. Vì vậy, khác biệt vài FP hoặc FN có thể làm thay đổi metric và thứ hạng đáng kể. Test được dùng để quan sát tính ổn định, không dùng để đảo ngược tiêu chí lựa chọn đã xác lập từ dev.

Ở cấp độ nhóm, các mô hình pretrained nhìn chung vẫn chiếm phần lớn vị trí đầu trên test. Bốn trong năm mô hình có Macro-F1 cao nhất là Gemma 2B, Qwen3 0.6B, Gemma 3 1B và ViCLSR; vị trí còn lại thuộc XLM-RoBERTa-large. TextCNN distilled là mô hình character-level tốt nhất trên test với Macro-F1 0,9189 và Recall Label 1 0,9189, nhưng vẫn có khoảng cách với các cấu hình pretrained đứng đầu. Điều này cho thấy mô hình ký tự có thể đạt độ nhạy cao với smishing trong một cấu hình gọn nhẹ, song các mô hình pretrained vẫn có lợi thế về hiệu năng tổng thể.

Tóm lại, RQ1 cho thấy không có một kiến trúc duy nhất tối ưu cho mọi tiêu chí. Gemma 2B là lựa chọn tốt nhất theo tiêu chí chính nhờ đứng đầu Macro-F1 và F1 Label 1 trên dev, đồng thời duy trì vị trí dẫn đầu trên test. DistilBERT multilingual đạt Recall dev cao nhất, còn Qwen2.5 0.5B đạt PR-AUC dev cao nhất. Trong nhóm encoder, CafeBERT là mô hình cân bằng tốt nhất trên dev; trong nhóm character-level, TextCNN vượt BiLSTM. Distillation chưa tạo cải thiện nhất quán về Macro-F1, nhưng TextCNN distilled cho thấy khả năng tăng Recall và duy trì hiệu năng tương đối tốt trên test. Quyết định triển khai cuối cùng cần kết hợp các kết quả này với benchmark tài nguyên thay vì chỉ dựa trên chất lượng dự đoán.

---

## 5.2. RQ2: Đặc điểm nào của dữ liệu làm thay đổi hiệu năng?

Để hiểu sâu sắc về cách thức các đặc trưng dữ liệu ảnh hưởng đến khả năng nhận diện của mô hình, phân tích theo lát cắt (slice evaluation) được thực hiện trên tập dev đối với bốn mô hình đại diện: **CafeBERT** (PLM đơn ngữ tiếng Việt xuất sắc nhất), **DistilBERT multilingual** (PLM đa ngữ có Recall cao nhất), **TextCNN** (mô hình character-level nguyên bản tốt nhất) và **TextCNN distilled** (mô hình chưng cất tri thức có trade-off triển khai tốt). Phân tích sử dụng bộ nhãn metadata v2.1 để khảo sát theo độ dài, đặc trưng bề mặt, lĩnh vực tin nhắn, hành động yêu cầu, đối tượng nhắm đến và thủ đoạn thuyết phục.

### 5.2.1. Ảnh hưởng của độ dài tin nhắn và đặc trưng bề mặt

Độ dài tin nhắn tạo ra ảnh hưởng khác biệt rõ rệt giữa mô hình pre-trained PLM (dựa trên token) và mô hình học máy cấp ký tự (dựa trên ký tự thô).

**Bảng 5.3: Hiệu năng phân loại theo nhóm độ dài tin nhắn trên tập dev**

| Nhóm độ dài (ký tự) | Số mẫu (n) | Nhãn 1 (n1) | Mô hình | F1 Label 1 | Recall Label 1 | FP | FN |
| :--- | :---: | :---: | :--- | :---: | :---: | :---: | :---: |
| **81–160** | 146 | 17 | CafeBERT | 0,9091 | 0,8824 | 1 | 2 |
| | | | DistilBERT multilingual | 0,9444 | 1,0000 | 2 | 0 |
| | | | TextCNN | 0,8387 | 0,7647 | 1 | 4 |
| | | | TextCNN distilled | 0,8125 | 0,7647 | 2 | 4 |
| **161–240** | 82 | 8 | CafeBERT | 0,9333 | 0,8750 | 0 | 1 |
| | | | DistilBERT multilingual | 0,8889 | 1,0000 | 2 | 0 |
| | | | TextCNN | 0,8571 | 0,7500 | 0 | 2 |
| | | | TextCNN distilled | 0,9333 | 0,8750 | 0 | 1 |
| **>240** | 167 | 10 | CafeBERT | 0,8421 | 0,8000 | 1 | 2 |
| | | | DistilBERT multilingual | 0,7619 | 0,8000 | 3 | 2 |
| | | | TextCNN | 0,8571 | 0,9000 | 2 | 1 |
| | | | TextCNN distilled | 0,8182 | 0,9000 | 3 | 1 |

*Ghi chú: Nhóm tin nhắn ngắn \(\le 80\) ký tự chỉ chứa 2 mẫu Label 1 (và 138 mẫu Label 0) nên không được đưa vào bảng so sánh để tránh thiên lệch thống kê.*

Số liệu từ Bảng 5.3 cho thấy khi độ dài vượt quá 240 ký tự, hiệu năng F1-score của CafeBERT giảm từ 0,9333 xuống 0,8421, và DistilBERT multilingual giảm mạnh từ 0,8889 xuống 0,7619. Sự suy giảm này chủ yếu do mô hình PLM bị giới hạn độ dài tokenizer hoặc bị loãng thông tin ngữ cảnh trong các tin nhắn quá dài. Ngược lại, TextCNN thể hiện sự ổn định cao hơn với F1-score duy trì ở mức 0,8571 ở cả nhóm 161–240 và nhóm >240 ký tự, đồng thời Recall Label 1 tăng từ 0,7500 lên 0,9000. Điều này chỉ ra rằng các bộ lọc tích chập cục bộ (CNN) trên biểu diễn ký tự có lợi thế trong việc bắt được các tín hiệu đặc trưng (như từ khóa hoặc liên kết độc hại) bất kể vị trí của chúng trong các đoạn văn bản dài.

Các đặc trưng bề mặt khác như sự xuất hiện của liên kết URL, số điện thoại, loại người gửi và nguồn gốc dữ liệu cũng tạo ra các tác động không đồng nhất được tóm tắt trong Bảng 5.4.

**Bảng 5.4: Hiệu năng phân loại theo đặc trưng bề mặt và nguồn dữ liệu trên tập dev**

| Lát cắt | Phân phối mẫu (n0/n1) | Phát hiện chính |
| :--- | :---: | :--- |
| **Có URL** | 168 / 29 | Tín hiệu mạnh hỗ trợ phát hiện smishing. Recall đạt mức rất cao (DistilBERT: 100%, TextCNN distilled: 89,66%, CafeBERT & TextCNN: 86,21%). Kiểm soát FP cực tốt (CafeBERT: 0, TextCNN: 1). |
| **Không URL** | 330 / 8 | Là nhóm khó đối với mô hình ký tự. Recall của TextCNN & TextCNN distilled giảm mạnh còn 62,5%, DistilBERT giảm còn 75%, riêng CafeBERT duy trì ổn định ở 87,5%. |
| **Brandname** | 260 / 14 | Recall đạt mức cao (DistilBERT: 100%, TextCNN distilled: 92,86%, CafeBERT & TextCNN: 85,71%). |
| **Personal Number** | 16 / 23 | Là nhóm khó đối với mô hình ký tự (TextCNN & TextCNN distilled: Recall chỉ đạt 78,26%). CafeBERT và DistilBERT xử lý tốt hơn với Recall lần lượt là 86,96% và 91,30%. |
| **Nguồn dữ liệu** | 348 / 37 (Real)<br>150 / 0 (External) | Lỗi của mô hình tập trung chủ yếu ở dữ liệu Real. Các mô hình kiểm soát FP trên dữ liệu hội thoại đời thường và bài viết mạng xã hội (tập External) cực tốt (tổng cộng chỉ có 1 FP với DistilBERT, và 2 FP với mỗi mô hình TextCNN). |

Sự hiện diện của URL là một trong những tín hiệu phân loại mạnh nhất. Với các tin nhắn chứa liên kết URL, DistilBERT multilingual đạt Recall 100% (bắt được toàn bộ 29 tin smishing chứa URL). Tuy nhiên, khi chuyển sang nhóm không có URL (chỉ có 8 mẫu smishing), Recall của DistilBERT giảm xuống 75,00% và hai mô hình TextCNN giảm mạnh xuống 62,50%. Điều này chứng minh các mô hình học máy bị phụ thuộc đáng kể vào đặc trưng bề mặt dễ nhận biết như URL để đưa ra quyết định dự đoán nhãn smishing, dẫn đến việc bỏ sót các tin nhắn lừa đảo tinh vi chỉ dùng số điện thoại liên hệ hoặc yêu cầu phản hồi trực tiếp. Riêng CafeBERT thể hiện khả năng hiểu ngữ cảnh tốt khi duy trì Recall 87,50% trên nhóm không chứa URL.

Đối với loại người gửi, tin nhắn gửi từ số cá nhân (`personal_number`) gây nhiều khó khăn hơn cho mô hình ký tự. Recall của TextCNN giảm từ 85,71% trên brandname xuống 78,26% trên số cá nhân. Đối với nguồn dữ liệu, các mô hình thể hiện khả năng chống cảnh báo sai (False Positive) rất tốt trên tập dữ liệu ngoài miền (`external`), cho thấy miền dữ liệu trò chuyện thông thường hoặc bài viết mạng xã hội (vốn chứa nhiều teencode và ngôn ngữ phi chuẩn) không dễ bị mô hình nhầm lẫn là smishing, ngoại trừ một vài trường hợp cá biệt của mô hình TextCNN.

### 5.2.2. Hiệu năng theo Lĩnh vực (Domain), Hành động (Action) và Vai trò đối tượng (Role)

Việc phân tích hiệu năng theo các nhãn metadata v2.1 cung cấp các insight sâu sắc về khả năng nhận diện các nhóm chủ đề lừa đảo khác nhau.

**Bảng 5.5: Hiệu năng phân loại theo lĩnh vực tin nhắn trên tập dev**

| Lĩnh vực tin nhắn (Domain) | Số mẫu (n) | Nhãn 1 (n1) | Mô hình | F1 Label 1 | Recall Label 1 | FP | FN |
| :--- | :---: | :---: | :--- | :---: | :---: | :---: | :---: |
| **Viễn thông** (`telecom`) | 188 | 1 | CafeBERT | 1,0000 | 1,0000 | 0 | 0 |
| | | | DistilBERT multilingual | 1,0000 | 1,0000 | 0 | 0 |
| | | | TextCNN | 0,0000 | 0,0000 | 0 | 1 |
| | | | TextCNN distilled | 0,0000 | 0,0000 | 0 | 1 |
| **Tài chính - Ngân hàng** (`banking_finance`) | 73 | 10 | CafeBERT | 0,9474 | 0,9000 | 0 | 1 |
| | | | DistilBERT multilingual | 1,0000 | 1,0000 | 0 | 0 |
| | | | TextCNN | 0,8889 | 0,8000 | 0 | 2 |
| | | | TextCNN distilled | 0,9474 | 0,9000 | 0 | 1 |
| **Dịch vụ công** (`public_service`) | 52 | 3 | CafeBERT | 0,6667 | 0,6667 | 1 | 1 |
| | | | DistilBERT multilingual | 0,7500 | 1,0000 | 2 | 0 |
| | | | TextCNN | 1,0000 | 1,0000 | 0 | 0 |
| | | | TextCNN distilled | 1,0000 | 1,0000 | 0 | 0 |
| **Đánh bạc / Cá cược** (`gambling`) | 6 | 5 | CafeBERT | 0,8889 | 0,8000 | 0 | 1 |
| | | | DistilBERT multilingual | 1,0000 | 1,0000 | 0 | 0 |
| | | | TextCNN | 0,8889 | 0,8000 | 0 | 1 |
| | | | TextCNN distilled | 0,8889 | 0,8000 | 0 | 1 |
| **Tuyển dụng** (`employment`) | 11 | 5 | CafeBERT | 1,0000 | 1,0000 | 0 | 0 |
| | | | DistilBERT multilingual | 0,8333 | 1,0000 | 2 | 0 |
| | | | TextCNN | 0,8333 | 1,0000 | 2 | 0 |
| | | | TextCNN distilled | 0,8333 | 1,0000 | 2 | 0 |
| **Đòi nợ** (`debt_collection`) | 6 | 4 | CafeBERT | 0,8571 | 0,7500 | 0 | 1 |
| | | | DistilBERT multilingual | 0,6667 | 0,5000 | 0 | 2 |
| | | | TextCNN | 0,8571 | 0,7500 | 0 | 1 |
| | | | TextCNN distilled | 0,8571 | 0,7500 | 0 | 1 |

*Ghi chú: Lĩnh vực `healthcare` (n=3, n1=0), `investment` (n=1, n1=1) và `other` (n=14, n1=0) do số lượng mẫu quá ít nên không đưa vào bảng.*

Bảng 5.5 chỉ ra sự chênh lệch lớn về độ khó giữa các lĩnh vực tin nhắn:
- **Tài chính - Ngân hàng**: Là lĩnh vực phổ biến và có hiệu năng cao nhất. DistilBERT multilingual đạt F1-score và Recall tuyệt đối 100%. Các mô hình còn lại đều đạt F1-score từ 0,88 trở lên, cho thấy từ vựng ngân hàng (như OTP, tài khoản, biến động số dư) được mô hình học rất sâu.
- **Đòi nợ**: Đây là lĩnh vực khó khăn nhất. DistilBERT multilingual bỏ sót đến 50% số tin đòi nợ (Recall = 0,5000), trong khi CafeBERT và hai mô hình TextCNN bỏ sót 25% (Recall = 0,7500). Nguyên nhân là tin nhắn đòi nợ thường sử dụng ngôn ngữ đe dọa, hành chính hành vi mà không cần chèn các đường dẫn URL độc hại hay các từ khóa trúng thưởng, khiến mô hình dễ nhầm lẫn với các thông tin nhắc nợ thông thường.
- **Dịch vụ công**: Mô hình ký tự (TextCNN) lại đạt hiệu năng tuyệt đối 100% trong khi CafeBERT (F1=0,6667) và DistilBERT (F1=0,7500) gặp khó khăn và phát sinh lỗi FP. Điều này phản ánh các tin nhắn dịch vụ công thường có cấu trúc trang trọng đặc thù mà mô hình cấp ký tự dễ dàng nắm bắt được ranh giới.

Chúng ta tiếp tục xem xét hiệu năng thông qua các lát cắt về hành động yêu cầu và vai trò của đối tượng nhắm đến.

**Bảng 5.6: Hiệu năng phân loại theo hành động yêu cầu và vai trò đối tượng trên tập dev**

| Lát cắt phân tích | Số mẫu (n) | Nhãn 1 (n1) | Mô hình | F1 Label 1 | Recall Label 1 | FP | FN |
| :--- | :---: | :---: | :--- | :---: | :---: | :---: | :---: |
| **Hành động: Truy cập liên kết** (`click_or_visit_link`) | 193 | 26 | CafeBERT | 0,9167 | 0,8462 | 0 | 4 |
| | | | DistilBERT multilingual | 0,9630 | 1,0000 | 2 | 0 |
| | | | TextCNN | 0,8980 | 0,8462 | 1 | 4 |
| | | | TextCNN distilled | 0,9020 | 0,8846 | 2 | 3 |
| **Hành động: Gọi điện thoại** (`call_phone`) | 163 | 4 | CafeBERT | 0,6667 | 0,5000 | 0 | 2 |
| | | | DistilBERT multilingual | 0,7500 | 0,7500 | 1 | 1 |
| | | | TextCNN | 0,8571 | 0,7500 | 0 | 1 |
| | | | TextCNN distilled | 0,8571 | 0,7500 | 0 | 1 |
| **Đối tượng: Khách hàng** (`customer`) | 304 | 14 | CafeBERT | 0,9231 | 0,8571 | 0 | 2 |
| | | | DistilBERT multilingual | 0,9655 | 1,0000 | 1 | 0 |
| | | | TextCNN | 0,8333 | 0,7143 | 0 | 4 |
| | | | TextCNN distilled | 0,8462 | 0,7857 | 1 | 3 |
| **Đối tượng: Con nợ** (`debtor`) | 6 | 4 | CafeBERT | 0,8571 | 0,7500 | 0 | 1 |
| | | | DistilBERT multilingual | 0,6667 | 0,5000 | 0 | 2 |
| | | | TextCNN | 0,8571 | 0,7500 | 0 | 1 |
| | | | TextCNN distilled | 0,8571 | 0,7500 | 0 | 1 |

Số liệu từ Bảng 5.6 cho thấy hành động yêu cầu truy cập liên kết (`click_or_visit_link`) được tất cả các mô hình phát hiện tốt hơn đáng kể so với yêu cầu gọi số hotline (`call_phone`). Ví dụ, CafeBERT đạt Recall 84,62% trên nhóm yêu cầu click link nhưng giảm mạnh xuống 50,00% khi yêu cầu là gọi điện. Đối với vai trò đối tượng nhắm đến, nhóm con nợ (`debtor`) tương ứng với lĩnh vực đòi nợ tiếp tục thể hiện là nhóm đối tượng khó nhận diện nhất đối với mô hình, đặc biệt là DistilBERT multilingual (Recall chỉ đạt 50%).

### 5.2.3. Đánh giá chuyên sâu trên các Thủ đoạn thuyết phục (Persuasion Tactics)

Bộ nhãn metadata v2.1 cho phép bóc tách chi tiết hiệu năng phân loại của mô hình dựa trên các thủ đoạn tâm lý mà tin nhắn Smishing sử dụng để thao túng nạn nhân.

**Bảng 5.7: Hiệu năng phân loại theo thủ đoạn thuyết phục trên tập dev**

| Thủ đoạn thuyết phục | Số mẫu (n) | Nhãn 1 (n1) | Mô hình | F1 Label 1 | Recall Label 1 | FP | FN |
| :--- | :---: | :---: | :--- | :---: | :---: | :---: | :---: |
| **Dụ dỗ qua liên kết** (`link_lure`) | 168 | 26 | CafeBERT | 0,9388 | 0,8846 | 0 | 3 |
| | | | DistilBERT multilingual | 0,9811 | 1,0000 | 1 | 0 |
| | | | TextCNN | 0,9167 | 0,8462 | 0 | 4 |
| | | | TextCNN distilled | 0,9020 | 0,8846 | 2 | 3 |
| **Quà tặng / Khuyến mại** (`reward_incentive`) | 150 | 17 | CafeBERT | 0,9697 | 0,9412 | 0 | 1 |
| | | | DistilBERT multilingual | 0,9714 | 1,0000 | 1 | 0 |
| | | | TextCNN | 0,9032 | 0,8235 | 0 | 3 |
| | | | TextCNN distilled | 0,8750 | 0,8235 | 1 | 3 |
| **Thúc giục thời gian** (`urgency`) | 69 | 15 | CafeBERT | 0,8889 | 0,8000 | 0 | 3 |
| | | | DistilBERT multilingual | 0,8966 | 0,8667 | 1 | 2 |
| | | | TextCNN | 0,8889 | 0,8000 | 0 | 3 |
| | | | TextCNN distilled | 0,9286 | 0,8667 | 0 | 2 |
| **Mạo danh uy quyền** (`authority`) | 29 | 3 | CafeBERT | 0,6667 | 0,6667 | 1 | 1 |
| | | | DistilBERT multilingual | 0,5714 | 0,6667 | 2 | 1 |
| | | | TextCNN | 0,8000 | 0,6667 | 0 | 1 |
| | | | TextCNN distilled | 0,8000 | 0,6667 | 0 | 1 |
| **Đánh vào nỗi sợ** (`fear`) | 20 | 3 | CafeBERT | 0,4000 | 0,3333 | 1 | 2 |
| | | | DistilBERT multilingual | 0,8000 | 0,6667 | 0 | 1 |
| | | | TextCNN | 0,5000 | 0,3333 | 0 | 2 |
| | | | TextCNN distilled | 0,5000 | 0,3333 | 0 | 2 |
| **Đe dọa trừng phạt** (`threat`) | 15 | 6 | CafeBERT | 0,9091 | 0,8333 | 0 | 1 |
| | | | DistilBERT multilingual | 0,8000 | 0,6667 | 0 | 2 |
| | | | TextCNN | 0,8000 | 0,6667 | 0 | 2 |
| | | | TextCNN distilled | 0,9091 | 0,8333 | 0 | 1 |

*Ghi chú: Thủ đoạn `scarcity` (n1=4, F1=1.0 và Recall=1.0 đối với tất cả mô hình) và `off_platform_contact` (n1=8, F1 và Recall đều \(\ge 0,93\)) được bỏ qua để tập trung vào các nhóm phức tạp.*

Phân tích số liệu từ Bảng 5.7 chỉ ra các đặc điểm tâm lý học hành vi tác động trực tiếp đến mô hình:
- **Thủ đoạn dụ dỗ qua liên kết (`link_lure`) và Quà tặng (`reward_incentive`)**: Đây là nhóm thủ đoạn dễ phát hiện nhất. DistilBERT multilingual đạt Recall 100% trên cả hai nhóm này. CafeBERT cũng đạt F1-score rất cao (lần lượt là 0,9388 và 0,9697). Lý do là các thủ đoạn này thường đi kèm các cấu trúc từ vựng mang tính chào mời, chúc mừng trúng thưởng và các URL rõ ràng, tạo điều kiện thuận lợi cho cơ chế chú ý của transformer nhận diện.
- **Thủ đoạn thúc giục thời gian (`urgency`)**: Có độ khó trung bình. Các mô hình bỏ sót từ 2 đến 3 mẫu (Recall dao động từ 80,00% đến 86,67%), do các từ khóa thúc giục thời gian (như "ngay", "trong 24h", "hạn chót") cũng xuất hiện thường xuyên trong tin nhắn OTP hoặc quảng cáo viễn thông hợp lệ.
- **Thủ đoạn đánh vào nỗi sợ (`fear`) và Mạo danh uy quyền (`authority`)**: Đây là những nhóm thủ đoạn khó nhất. Khi kẻ xấu đe dọa tài khoản bị khóa hoặc yêu cầu cập nhật khẩn cấp dưới danh nghĩa cơ quan công quyền, Recall của CafeBERT và hai mô hình TextCNN trên nhóm `fear` chỉ đạt 33,33% (bỏ sót 2 trên 3 mẫu). DistilBERT multilingual đạt Recall tốt hơn ở mức 66,67% nhưng đổi lại phải đánh đổi bằng việc tăng FP trên nhóm `authority` (F1-score giảm xuống 0,5714).
- **Thủ đoạn đe dọa trừng phạt (`threat`)**: CafeBERT và TextCNN distilled đạt hiệu năng vượt trội với F1-score 0,9091 và Recall 83,33% (chỉ bỏ sót 1 mẫu). Điều này cho thấy khả năng hiểu ngữ cảnh đe dọa mang tính hình sự/pháp luật của CafeBERT đã được chuyển giao một cách hiệu quả sang student TextCNN thông qua hàm mục tiêu chưng cất tri thức.

Tóm lại, phân tích lát cắt sâu sắc ở RQ2 chỉ ra rằng các mô hình pre-trained transformer và mô hình ký tự có những điểm mạnh - yếu rất bổ trợ cho nhau. Các mô hình pre-trained transformers nhạy bén với các liên kết URL và các từ khóa mang tính dụ dỗ/tặng thưởng, nhưng dễ suy giảm hiệu năng khi tin nhắn quá dài hoặc khi tin nhắn Smishing không chứa URL. Ngược lại, các mô hình ký tự (TextCNN) thể hiện sự bền vững trên các văn bản dài nhưng lại gặp khó khăn rõ rệt với tin nhắn không chứa URL và các thủ đoạn mạo danh uy quyền hoặc đánh vào nỗi sợ hãi.

---

## 5.3. RQ3: Mô hình sai ở đâu và vì sao?

Để làm rõ nguyên nhân sâu xa dẫn đến các thất bại phân loại, chúng ta tiến hành khảo sát thống kê trên tập lỗi của 4 mô hình đại diện trên tập dev. Bảng 5.8 trình bày số lượng lỗi phân loại chi tiết của từng cấu hình mô hình.

**Bảng 5.8: Thống kê số lượng lỗi phân loại trên tập dev**

| Mô hình | False Positive (FP) | False Negative (FN) | Tổng số lỗi | Lỗi có độ tin cậy \(\ge 0,9\) |
| :--- | :---: | :---: | :---: | :---: |
| **CafeBERT** | 2 | 5 | 7 | 5 |
| **DistilBERT multilingual** | 7 | 2 | 9 | 8 |
| **TextCNN** | 4 | 7 | 11 | 7 |
| **TextCNN distilled** | 6 | 6 | 12 | 5 |

Một điểm đáng chú ý là phần lớn các lỗi phân loại của mô hình đều có mức độ tự tin (confidence score) cực kỳ cao (ví dụ: 5 trên 7 lỗi của CafeBERT và 8 trên 9 lỗi của DistilBERT có độ tin cậy từ 0,9 trở lên). Điều này chứng tỏ mô hình không đơn thuần là phân vân ở ranh giới quyết định, mà thực sự bị đánh lừa sâu sắc bởi các đặc trưng gây nhiễu trong tin nhắn.

Để kiểm tra xem các mô hình có hành vi lỗi tương đồng hay khác biệt, chúng ta tính toán ma trận độ giao thoa lỗi (Jaccard similarity) được trình bày trong Bảng 5.9.

**Bảng 5.9: Ma trận độ giao thoa lỗi (Jaccard) giữa các mô hình đại diện**

| Mô hình | CafeBERT | DistilBERT mult. | TextCNN | TextCNN distilled |
| :--- | :---: | :---: | :---: | :---: |
| **CafeBERT** | 1,0000 | 0,1429 | 0,2857 | 0,2667 |
| **DistilBERT multilingual** | 0,1429 | 1,0000 | 0,1765 | 0,1667 |
| **TextCNN** | 0,2857 | 0,1765 | 1,0000 | **0,7692** |
| **TextCNN distilled** | 0,2667 | 0,1667 | **0,7692** | 1,0000 |

Kết quả từ Bảng 5.9 chỉ ra:
- **CafeBERT và DistilBERT multilingual**: Có mức độ giao thoa lỗi cực kỳ thấp (Jaccard = 0,1429, chỉ chung nhau đúng 2 lỗi). Điều này khẳng định hai kiến trúc này học được các không gian biểu diễn rất khác nhau: CafeBERT đơn ngữ hóa tối ưu việc kiểm soát FP, trong khi DistilBERT đa ngữ hóa nhạy bén tối đa hóa Recall và chấp nhận nhiều FP hơn.
- **TextCNN và TextCNN distilled**: Có mức độ giao thoa lỗi rất lớn (Jaccard = 0,7692, chung nhau đến 10 lỗi trên tổng số 13 lỗi gộp). Sự tương đồng cao này chứng tỏ cơ chế chưng cất tri thức từ PhoBERT-base sang TextCNN chủ yếu giúp student tinh chỉnh xác suất đầu ra ở các mẫu biên để tăng độ nhạy, nhưng chưa thể tái định hình hoàn toàn ranh giới quyết định vốn bị giới hạn bởi cấu trúc trích xuất đặc trưng dạng ký tự cục bộ của TextCNN.

### 5.3.1. Phân tích định tính các nhóm lỗi tiêu biểu

Thông qua việc khớp nối các mẫu lỗi với nhãn metadata v2.1, chúng ta xác định được 4 nhóm nguyên nhân gây lỗi chính của mô hình:

#### Nhóm 1: Tin nhắn Smishing đòi nợ không chứa URL (Lỗi FN chung của cả 4 mô hình)
Chỉ có duy nhất 1 mẫu lỗi bị cả 4 mô hình dự đoán sai trên tập dev, đó là mẫu `ViSmish_07960`. Tin nhắn đòi nợ này có nội dung: *"Nhan thay co hanh vi LOI DUNG TIN NHIEM, CHIEM DOAT TAI SAN. yc tt gap truoc 13g 16/2/2025, neu van bat hop tac ben toi ban giao HS den CIC... LH 0867256447 de giai quyet."* 

Đây là tin nhắn Smishing đòi nợ thuộc lĩnh vực `debt_collection`, sử dụng thủ đoạn đe dọa (`threat`) kết hợp thúc giục thời gian (`urgency`). Điểm đặc biệt của tin nhắn này là sử dụng văn phong hành chính pháp lý rất tự nhiên và **không chứa bất kỳ liên kết URL nào**. Cả 4 mô hình đều dự đoán nhãn Benign với độ tin cậy rất cao (từ 0,9682 đến 0,9997) vì cấu trúc ngữ pháp và từ vựng của nó nằm sâu trong vùng phân phối của các tin nhắn cảnh báo hoặc đòi nợ hợp lệ của các tổ chức tài chính. Điều này cho thấy rào cản lớn nhất của các mô hình hiện tại là nhận diện smishing dựa trên ngữ nghĩa đe dọa thuần túy khi không có sự hỗ trợ của các đặc trưng bề mặt lộ liễu như URL.

#### Nhóm 2: Tin nhắn Smishing giả danh cảnh báo bảo mật ngân hàng (Lỗi FN của CafeBERT và TextCNN)
Mẫu điển hình là `ViSmish_04995`: *"ACB CANH BAO SMS LUA DAO: Hien co thu doan SMS GIA MAO dau so ACB moi KH dang nhap link gia, cung cap USER, MAT KHAU, OTP..."*

Đây là một tin nhắn Smishing giả danh tin cảnh báo lừa đảo của ngân hàng ACB nhưng chèn đường dẫn giả mạo `https://live` hoặc ứng dụng độc hại. CafeBERT (Conf=0,9994) và hai mô hình TextCNN (Conf >0,97) đều dự đoán sai thành nhãn Benign. Nguyên nhân là tin nhắn sử dụng hàng loạt từ khóa phòng thủ bảo mật vốn thường chỉ xuất hiện trong tin nhắn cảnh báo thật của ngân hàng (như "cảnh báo", "lừa đảo", "giả mạo", "không cung cấp OTP"). DistilBERT multilingual bắt được mẫu này (Conf=0,9956) nhờ cơ chế chú ý đa ngữ nhạy bén với liên kết URL giả mạo chèn ở cuối tin nhắn.

#### Nhóm 3: Tin nhắn tuyển sinh/hội thảo hợp lệ chứa liên kết đăng ký (Lỗi FP của DistilBERT và TextCNN)
Mẫu điển hình là `ViSmish_07545`: *"[ĐẠI HỌC NGOẠI THƯƠNG] CHÚC MỪNG EM ĐÃ ĐỦ ĐIỀU KIỆN TRÚNG TUYỂN Chương trình Đào tạo Quốc tế... Để lại email để nhận hướng dẫn hồ sơ... SĐT/ZALO: 0906..."*

Đây là tin nhắn hợp lệ thuộc lĩnh vực tuyển dụng/giáo dục (`employment`), sử dụng ngôn ngữ chúc mừng trúng tuyển kèm lời mời đăng ký thông tin qua email/số điện thoại. DistilBERT (Conf=0,9995) và hai mô hình TextCNN (Conf >0,93) đều bị đánh lừa và dự đoán thành Smishing. Lý do là tin nhắn chứa đầy đủ các tín hiệu đặc trưng của smishing: brandname tự xưng ở đầu tin, lời chúc mừng trúng tuyển (reward incentive), yêu cầu để lại thông tin cá nhân (requested action), và thông tin liên hệ khẩn cấp. Chỉ CafeBERT (Conf=0,7409) nhận diện đúng nhãn Benign nhờ hiểu được ngữ cảnh tuyển sinh chính thức của trường đại học Việt Nam.

#### Nhóm 4: Tin nhắn cá nhân chứa teencode phi chuẩn (Lỗi FP của hai mô hình TextCNN)
Mẫu điển hình là `ViSmish_08060`: *"t cx muốn nuôi capybara!!!!!"*

Đây là tin nhắn hội thoại cá nhân thông thường chứa chữ viết tắt ("t cx" - tớ cũng) và nhiều dấu chấm than biểu cảm mạnh. Cả CafeBERT và DistilBERT đều dự đoán đúng nhãn Benign với độ tin cậy tuyệt đối (>0,999). Tuy nhiên, TextCNN (Conf=0,8945) và TextCNN distilled (Conf=0,7560) lại nhầm tưởng là Smishing. Điều này phản ánh hạn chế lớn của mô hình ký tự: chúng rất dễ bị kích hoạt sai (trigger) bởi các cấu trúc viết tắt, teencode phi chuẩn hoặc các ký tự đặc biệt lặp lại, do chúng thiếu cơ chế tự chú ý toàn cục để hiểu ngữ cảnh ngữ nghĩa đời thường của câu nói.

**Bảng 5.10: Danh sách các lỗi tiêu biểu của mô hình trên tập dev**

| ID | Nhãn thực | Dự đoán (Độ tin cậy) | Lĩnh vực (Domain) | Nội dung tin nhắn (Rút gọn) | Đặc điểm và Nguyên nhân lỗi |
| :--- | :---: | :--- | :---: | :--- | :--- |
| **ViSmish_07960** | 1 | **Tất cả**: 0 (\(>0,96\)) | Đòi nợ | Nhan thay co hanh vi LOI DUNG TIN NHIEM, CHIEM DOAT TAI SAN. yc tt gap truoc 13g 16/2/2025... LH 0867256447 de giai quyet. | Tin nhắn Smishing đòi nợ dùng ngôn ngữ hành chính/pháp lý tự nhiên, không chứa liên kết URL, khiến toàn bộ các mô hình nhầm với tin nhắn hợp lệ. |
| **ViSmish_04995** | 1 | **CafeBERT**: 0 (0,9994)<br>**DistilBERT**: 1 (0,9956)<br>**TextCNN**: 0 (0,9991)<br>**TextCNN distilled**: 0 (0,9778) | Tài chính | ACB CANH BAO SMS LUA DAO: Hien co thu doan SMS GIA MAO dau so ACB moi KH dang nhap link gia, cung cap USER, MAT KHAU, OTP... | Tin nhắn cảnh báo lừa đảo chứa các từ khóa nhạy cảm và URL giả mạo. Chỉ DistilBERT bắt được, các mô hình khác nhầm với tin nhắn cảnh báo bảo mật hợp lệ. |
| **ViSmish_07545** | 0 | **CafeBERT**: 0 (0,7409)<br>**DistilBERT**: 1 (0,9995)<br>**TextCNN**: 1 (0,9536)<br>**TextCNN distilled**: 1 (0,9348) | Tuyển dụng | [ĐẠI HỌC NGOẠI THƯƠNG] CHÚC MỪNG EM ĐÃ ĐỦ ĐIỀU KIỆN TRÚNG TUYỂN... Để lại email để nhận hướng dẫn... SĐT/ZALO: 0906... | Tin nhắn tuyển sinh hợp lệ chứa cấu trúc thông báo trúng tuyển kèm đường dẫn đăng ký và thông tin liên hệ, khiến DistilBERT và TextCNN bị đánh lừa. |
| **ViSmish_08060** | 0 | **CafeBERT**: 0 (0,9998)<br>**DistilBERT**: 0 (0,9992)<br>**TextCNN**: 1 (0,8945)<br>**TextCNN distilled**: 1 (0,7560) | Cá nhân | t cx muốn nuôi capybara!!!!! | Tin nhắn hội thoại cá nhân phi chuẩn (teencode, dấu chấm than kéo dài) bị các mô hình ký tự (TextCNN) cảnh báo sai do nhạy cảm quá mức với ký tự phi chuẩn ngoài ngữ cảnh. |

Tóm lại, RQ3 chỉ ra rằng các vùng khó của bài toán Smishing không chỉ giới hạn ở các kỹ thuật cố tình che giấu từ vựng (obfuscation) của kẻ tấn công. Rào cản thực sự nằm ở các tin nhắn lừa đảo không chứa liên kết URL sử dụng văn phong đòi nợ pháp lý, các tin nhắn lừa đảo mạo danh cấu trúc tin cảnh báo bảo mật chính thống, hoặc ngược lại là các tin nhắn hợp lệ (tuyển sinh, hội thảo, cá nhân teencode) có chứa các đặc trưng bề mặt gần giống với tin nhắn lừa đảo. Định hướng cải thiện tiếp theo nên tập trung vào việc bổ sung các ví dụ cực khó (hard negatives và hard positives) vào tập huấn luyện để giúp mô hình tinh chỉnh ranh giới phân biệt ngữ nghĩa sâu thay vì dựa trên các đặc trưng bề mặt.

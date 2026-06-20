# CHƯƠNG 5. KẾT QUẢ VÀ PHÂN TÍCH

> **Quy ước biên tập**
>
> - Các khối `GHI CHÚ HÌNH`, `GHI CHÚ BẢNG`, `PLACEHOLDER` và `GHI CHÚ KIỂM TRA` không thuộc nội dung chính thức của báo cáo.
> - Việc lựa chọn và nhận xét mô hình dựa chủ yếu trên tập dev. Kết quả test được dùng để đánh giá khả năng duy trì hiệu năng sau khi cấu hình đã được cố định.
> - Do dev và test chỉ có 37 mẫu Label 1, mọi chênh lệch metric cần được đọc cùng số FP và FN.

## 5.1. RQ1: Mô hình nào đạt hiệu quả tốt nhất?

Bảng 5.x trình bày kết quả của 17 cấu hình trên tập dev và test theo bốn độ đo Macro-F1, F1 Label 1, Recall Label 1 và PR-AUC. Các mô hình được chia thành ba nhóm gồm neural network cấp ký tự, encoder PLM được fine-tune toàn phần và LLM được fine-tune hiệu quả tham số bằng LoRA. Trong phần này, kết quả dev được sử dụng để so sánh và lựa chọn mô hình; kết quả test chỉ được xem xét sau đó nhằm kiểm tra liệu xu hướng quan sát trên dev có được duy trì hay không.

> **GHI CHÚ BẢNG 5.x — Chèn bảng benchmark 17 cấu hình do nhóm đã tạo**
>
> Bảng gồm hai cột Dev/Test cho mỗi độ đo và chia thành ba nhóm:
>
> - Neural: BiLSTM, TextCNN và hai biến thể distilled.
> - Fine-tuned PLM: chín encoder.
> - LoRA LLM: Gemma 3 1B, Qwen2.5 0.5B, Qwen3 0.6B và Gemma 2B.
>
> In đậm giá trị tốt nhất của từng cột. Caption đề xuất: **“Kết quả benchmark của 17 cấu hình mô hình trên tập dev và test”**.

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

Để đánh giá liệu các student có tạo ra lợi ích triển khai thực tế hay không, PhoBERT-base, BiLSTM distilled và TextCNN distilled được đo lại trên benchmark dev split trong cùng môi trường CPU, sử dụng một luồng xử lý. Độ trễ được đo với batch size 1 sau ba lượt warm-up và 20 lần lặp; throughput được đo với batch size 128. Các metric chất lượng được tính lại từ dự đoán của chính checkpoint được đo, nhờ đó bảo đảm bảng tài nguyên và bảng benchmark sử dụng cùng mô hình.

> **GHI CHÚ BẢNG 5.x — Chèn bảng trade-off hiệu năng và tài nguyên trên dev**
>
> | Mô hình | Tham số | Kích thước (MB) | Latency (ms/tin) | Throughput (tin/s) | Peak RAM (MB) | Macro-F1 | F1 L1 | Recall L1 | PR-AUC |
> |---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
> | PhoBERT-base | 134.999.810 | 516,95 | 248,14 | 4,20 | 1.788,75 | 0,8750 | 0,7671 | 0,7568 | 0,8439 |
> | BiLSTM distilled | 80.065 | 0,314 | 2,57 | 1.004,88 | 400,00 | 0,8839 | 0,7838 | 0,7838 | 0,8241 |
> | TextCNN distilled | 87.553 | 0,342 | 1,62 | 1.001,77 | 407,89 | 0,9129 | 0,8378 | 0,8378 | 0,8818 |
>
> Caption đề xuất: **“So sánh chất lượng dự đoán và chi phí triển khai của PhoBERT-base với các student distilled trên benchmark dev split”**.

So với teacher, BiLSTM distilled giảm khoảng 1.686 lần số tham số và 1.648 lần kích thước checkpoint. Độ trễ CPU giảm từ 248,14 xuống 2,57 ms mỗi tin nhắn, tương ứng nhanh hơn khoảng 96,5 lần; throughput tăng từ 4,20 lên khoảng 1.004,88 tin nhắn/giây. Peak RAM giảm khoảng 77,6%. Mức tiết kiệm này không đi kèm suy giảm ở các metric phụ thuộc ngưỡng trên dev: Macro-F1 tăng 0,0088 điểm, F1 Label 1 tăng 0,0167 và Recall tăng 0,0270. Tuy nhiên, PR-AUC giảm 0,0198, cho thấy chất lượng xếp hạng xác suất trên nhiều ngưỡng chưa được bảo toàn hoàn toàn.

TextCNN distilled tạo ra trade-off thuận lợi hơn. Mô hình giảm khoảng 1.542 lần số tham số và 1.513 lần kích thước checkpoint so với PhoBERT-base. Độ trễ chỉ còn 1,62 ms mỗi tin nhắn, nhanh hơn teacher khoảng 153,6 lần, trong khi peak RAM giảm khoảng 77,2%. Đồng thời, TextCNN distilled cao hơn teacher 0,0379 điểm Macro-F1, 0,0707 điểm F1 Label 1, 0,0811 điểm Recall Label 1 và 0,0379 điểm PR-AUC trên dev. Trong thiết lập này, student không chỉ nhẹ hơn mà còn vượt teacher ở cả bốn độ đo.

Kết quả trên test cho thấy lợi ích chất lượng của hai student không ổn định như nhau. BiLSTM distilled thấp hơn teacher 0,0397 điểm Macro-F1, 0,0734 điểm F1 Label 1, 0,0541 điểm Recall và 0,1918 điểm PR-AUC. Ngược lại, TextCNN distilled vẫn cao hơn teacher 0,0121 điểm Macro-F1, 0,0233 điểm F1 Label 1 và 0,0811 điểm Recall, dù PR-AUC thấp hơn 0,0415. Do đó, BiLSTM distilled chủ yếu mang lại lợi ích tài nguyên nhưng đánh đổi chất lượng tổng quát hóa, trong khi TextCNN distilled duy trì trade-off thuyết phục hơn giữa chất lượng và chi phí triển khai.

Việc student vượt teacher ở một số metric không có nghĩa distillation đã tạo ra một mô hình có năng lực biểu diễn tổng quát hơn PhoBERT-base trong mọi điều kiện. Student khác teacher về kiến trúc, biểu diễn ký tự và hàm mất mát; hơn nữa mỗi split chỉ có 37 mẫu Label 1. Kết quả nên được hiểu là trong benchmark hiện tại, TextCNN distilled tận dụng tốt cả nhãn cứng và soft target để đạt điểm vận hành tốt hơn teacher, đồng thời có chi phí suy luận thấp hơn đáng kể.

> **GHI CHÚ HÌNH 5.x — Biểu đồ trade-off chất lượng–chi phí**
>
> Nên dùng scatter plot với:
>
> - Trục hoành: latency CPU theo thang logarithm.
> - Trục tung: F1 Label 1 trên dev.
> - Kích thước điểm: số tham số hoặc peak RAM.
> - Ba điểm: PhoBERT-base, BiLSTM distilled, TextCNN distilled.
>
> TextCNN distilled sẽ nằm ở vùng latency thấp và F1 cao, làm rõ ưu thế triển khai mà bảng số liệu khó thể hiện trực quan.

Sau khi các nhận xét được hình thành từ dev, kết quả test được sử dụng để kiểm tra mức độ duy trì xu hướng. Gemma 2B tiếp tục đứng đầu về Macro-F1 (0,9585), F1 Label 1 (0,9231), Recall Label 1 (0,9730) và PR-AUC (0,9853). Mô hình chỉ bỏ sót 1 trong 37 mẫu smishing trên test, dù số FP tăng từ 2 trên dev lên 5 trên test. Việc Gemma 2B giữ vị trí dẫn đầu trên cả hai split củng cố lựa chọn mô hình theo dev.

Một số mô hình có thứ hạng thay đổi đáng kể trên test. Qwen3 0.6B tăng Macro-F1 từ 0,9236 lên 0,9485 và trở thành mô hình đứng thứ hai trên test; PhoBERT-large tăng từ 0,8975 lên 0,9370; trong khi Qwen2.5 0.5B giảm từ 0,9433 xuống 0,9248 và CafeBERT giảm từ 0,9472 xuống 0,9355. BiLSTM có mức giảm rõ nhất, từ Macro-F1 0,8984 xuống 0,8471 và Recall Label 1 từ 0,8108 xuống 0,6757.

Những biến động này không nên được hiểu là mô hình “cải thiện” sau khi chuyển sang test. Dev và test có cùng quy mô nhưng chỉ chứa 37 mẫu Label 1; một dự đoán smishing tương ứng khoảng 2,70 điểm phần trăm Recall. Vì vậy, khác biệt vài FP hoặc FN có thể làm thay đổi metric và thứ hạng đáng kể. Test được dùng để quan sát tính ổn định, không dùng để đảo ngược tiêu chí lựa chọn đã xác lập từ dev.

Ở cấp độ nhóm, các mô hình pretrained nhìn chung vẫn chiếm phần lớn vị trí đầu trên test. Bốn trong năm mô hình có Macro-F1 cao nhất là Gemma 2B, Qwen3 0.6B, Gemma 3 1B và ViCLSR; vị trí còn lại thuộc XLM-RoBERTa-large. TextCNN distilled là mô hình character-level tốt nhất trên test với Macro-F1 0,9189 và Recall Label 1 0,9189, nhưng vẫn có khoảng cách với các cấu hình pretrained đứng đầu. Điều này cho thấy mô hình ký tự có thể đạt độ nhạy cao với smishing trong một cấu hình gọn nhẹ, song các mô hình pretrained vẫn có lợi thế về hiệu năng tổng thể.

Tóm lại, RQ1 cho thấy không có một kiến trúc duy nhất tối ưu cho mọi tiêu chí. Gemma 2B là lựa chọn tốt nhất theo tiêu chí chính nhờ đứng đầu Macro-F1 và F1 Label 1 trên dev, đồng thời duy trì vị trí dẫn đầu trên test. DistilBERT multilingual đạt Recall dev cao nhất, còn Qwen2.5 0.5B đạt PR-AUC dev cao nhất. Trong nhóm encoder, CafeBERT là mô hình cân bằng tốt nhất trên dev; trong nhóm character-level, TextCNN vượt BiLSTM. Distillation chưa tạo cải thiện nhất quán về Macro-F1, nhưng TextCNN distilled cho thấy khả năng tăng Recall và duy trì hiệu năng tương đối tốt trên test. Quyết định triển khai cuối cùng cần kết hợp các kết quả này với benchmark tài nguyên thay vì chỉ dựa trên chất lượng dự đoán.

> **GHI CHÚ KIỂM TRA trước khi kết thúc Mục 5.1**
>
> - Giữ bảng benchmark làm bảng trung tâm; không tạo thêm nhiều bảng xếp hạng lặp lại cùng số liệu.
> - Khi in đậm, chỉ in giá trị tốt nhất từng cột; không ngầm biến kết quả test thành tiêu chí chọn mô hình.
> - Kiểm tra lại FP/FN nếu bảng aggregate được chạy lại sau khi đổi split.
> - Số liệu tài nguyên hiện phản ánh môi trường CPU cục bộ; bổ sung tên CPU, tổng RAM và phiên bản thư viện vào caption hoặc phần thiết lập khi hoàn tất thông tin môi trường.
> - Không gọi chênh lệch vài mẫu trên dev/test là khác biệt có ý nghĩa thống kê khi chưa có kiểm định hoặc nhiều lần chia dữ liệu.

## 5.2. RQ2: Đặc điểm nào của dữ liệu làm thay đổi hiệu năng?

Phân tích theo lát cắt được thực hiện trên tập dev đối với bốn mô hình có đầy đủ prediction-level artefact và đại diện cho các hành vi khác nhau trong RQ1: CafeBERT là encoder có Macro-F1 cao nhất, DistilBERT multilingual có Recall Label 1 cao nhất, TextCNN là mô hình character-level hard-label tốt nhất và TextCNN distilled đại diện cho cấu hình chưng cất có trade-off triển khai tốt. Bốn LLM chưa được đưa vào phần này vì artefact hiện tại chỉ chứa metric tổng hợp, chưa có xác suất dự đoán cho từng mẫu. Do đó, kết luận RQ2 phản ánh các mô hình đại diện nói trên, không được khái quát trực tiếp cho toàn bộ 17 cấu hình.

Độ dài tin nhắn tạo ra ảnh hưởng khác nhau giữa encoder và mô hình ký tự. Nhóm tin nhắn không quá 80 ký tự chỉ có hai mẫu Label 1 nên không đủ để diễn giải metric lớp smishing. Trong ba nhóm còn lại, CafeBERT đạt F1 Label 1 lần lượt là 0,9091 ở khoảng 81–160 ký tự, 0,9333 ở khoảng 161–240 ký tự và giảm xuống 0,8421 khi độ dài vượt 240 ký tự. DistilBERT multilingual cũng giảm rõ ở nhóm trên 240 ký tự, với F1 Label 1 từ 0,9444 và 0,8889 ở hai khoảng trước xuống 0,7619.

TextCNN có xu hướng ổn định hơn theo độ dài. F1 Label 1 của mô hình lần lượt là 0,8387, 0,8571 và 0,8571 ở ba nhóm đủ mẫu. TextCNN distilled đạt 0,8125, 0,9333 và 0,8182. Kết quả này chưa cho phép khẳng định character-level luôn xử lý văn bản dài tốt hơn, nhưng cho thấy sự suy giảm ở nhóm rất dài rõ hơn đối với hai encoder đại diện. Một nguyên nhân có thể là encoder bị giới hạn ở 128 token, trong khi TextCNN giữ tối đa 256 ký tự; tuy nhiên, cần kiểm tra trực tiếp tỷ lệ mẫu thực sự bị truncate trước khi xem đây là giải thích nhân quả.

> **GHI CHÚ BẢNG 5.x — Hiệu năng theo độ dài trên dev**
>
> Nên trình bày ba nhóm đủ số mẫu Label 1: 81–160, 161–240 và trên 240 ký tự. Mỗi hàng ghi `n`, F1 Label 1, Recall Label 1, FP và FN. Nhóm ≤80 chỉ ghi phân phối 138 Label 0 và 2 Label 1, không dùng để so sánh mô hình.
>
> Nguồn dữ liệu: [rq2_slice_metrics_dev.csv](C:\KLTN\KLTN\scripts\RQ2_RQ3\rq2_slice_metrics_dev.csv).

Sự xuất hiện của URL là lát cắt tạo khác biệt rõ hơn. Trong 37 mẫu smishing trên dev, 29 mẫu chứa URL và chỉ 8 mẫu không chứa URL. Với nhóm có URL, DistilBERT multilingual đạt Recall bằng 1,0000; CafeBERT và TextCNN đạt 0,8621; TextCNN distilled đạt 0,8966. Khi không có URL, Recall giảm xuống 0,7500 đối với DistilBERT và chỉ 0,6250 đối với cả hai TextCNN, trong khi CafeBERT duy trì 0,8750.

Xu hướng này cho thấy URL là tín hiệu hỗ trợ mạnh, đặc biệt đối với DistilBERT và nhóm character-level. Tuy nhiên, URL không phải điều kiện đủ để xác định smishing vì dev còn có 168 mẫu Label 0 chứa URL. Các mô hình vẫn kiểm soát FP tương đối tốt trong nhóm này: CafeBERT không tạo FP, TextCNN tạo 1 FP, còn DistilBERT và TextCNN distilled cùng tạo 3 FP. Vùng khó hơn đối với mô hình ký tự là các tin smishing không có URL, nơi tín hiệu lừa đảo phải được suy ra từ nội dung và ngữ cảnh thay vì một pattern bề mặt rõ ràng.

Số điện thoại không tạo ra xu hướng nhất quán như URL. CafeBERT và TextCNN có Recall thấp hơn một chút ở nhóm có số điện thoại; DistilBERT đạt Recall 1,0000 trong nhóm này nhưng chỉ gồm 10 mẫu Label 1. TextCNN distilled đạt Recall 0,8000 ở nhóm có số điện thoại và 0,8519 ở nhóm không có. Với cỡ mẫu hiện tại, sự hiện diện của số điện thoại không đủ để xem là yếu tố quyết định độ khó.

Phân tích theo loại người gửi cho thấy nhóm `personal_number` khó hơn đối với TextCNN. Recall của TextCNN trên brandname là 0,8571 nhưng giảm còn 0,7826 trên số cá nhân; phiên bản distilled tăng Recall brandname lên 0,9286 nhưng vẫn chỉ đạt 0,7826 trên `personal_number`. CafeBERT duy trì Recall gần nhau giữa hai nhóm, lần lượt 0,8571 và 0,8696. DistilBERT đạt Recall 1,0000 trên brandname và 0,9130 trên số cá nhân, nhưng tạo nhiều FP hơn CafeBERT. Nhóm shortcode chỉ chứa Label 0 trong dev và không mô hình nào tạo FP, vì vậy không thể đánh giá khả năng nhận diện smishing từ shortcode ở lát cắt này.

Theo nguồn dữ liệu, lỗi chủ yếu tập trung ở miền `real`, cũng là nguồn duy nhất chứa Label 1 trên dev. CafeBERT không tạo FP trên 150 mẫu external; DistilBERT chỉ tạo một FP trên `external_curated`; hai TextCNN mỗi mô hình tạo một FP trên `external_real` và một FP trên `external_curated`. Kết quả cho thấy các mô hình benchmark đã kiểm soát tương đối tốt miền Label 0 external khi nguồn này được đưa vào train. Tuy nhiên, do external dev chỉ chứa Label 0, kết luận này chỉ phản ánh khả năng hạn chế cảnh báo sai, không phản ánh đầy đủ khả năng tổng quát hóa smishing sang một miền mới.

> **GHI CHÚ BẢNG 5.x — Tóm tắt các lát cắt có ý nghĩa**
>
> Có thể dùng một bảng ngắn thay vì trình bày toàn bộ CSV:
>
> | Lát cắt | Phát hiện chính |
> |---|---|
> | Độ dài >240 | CafeBERT và DistilBERT suy giảm F1 L1; TextCNN ổn định hơn |
> | Có/không URL | Smishing không có URL khó hơn rõ đối với TextCNN |
> | Sender type | `personal_number` là nhóm khó hơn đối với hai TextCNN |
> | Data origin | FP trên external thấp; lỗi chủ yếu nằm ở dữ liệu real |

Phân tích `obfuscation_level` hiện tại không cho thấy quan hệ đơn điệu giữa mức được gán và Recall. Chẳng hạn, cả CafeBERT và DistilBERT đều phát hiện đúng toàn bộ năm mẫu Level 3–4, trong khi CafeBERT chỉ đạt Recall 0,7647 ở nhóm Level 1–2. Điều này không có nghĩa che giấu mạnh dễ xử lý hơn, vì nhóm Level 3–4 quá nhỏ và thuộc tính hiện tại còn gắn với cách thiết kế Label 1. Do đó, kết quả này chỉ được xem là quan sát phụ. Phần đánh giá độ bền vững trước teencode, viết tắt và văn bản phi chuẩn sẽ được hoàn thiện sau khi xây dựng `text_noise_level` áp dụng độc lập cho cả hai nhãn.

Tổng hợp RQ2 cho thấy hiệu năng không chỉ phụ thuộc vào mô hình mà còn vào loại tín hiệu xuất hiện trong tin nhắn. Hai encoder đại diện có xu hướng suy giảm ở nhóm văn bản rất dài, trong khi TextCNN gặp khó rõ hơn với smishing không có URL và tin nhắn từ số cá nhân. CafeBERT cho kết quả cân bằng nhất giữa các lát cắt, còn DistilBERT đạt Recall cao nhờ dự đoán nhạy hơn nhưng tạo nhiều FP hơn. Các kết luận này cần được xem cùng cỡ mẫu từng nhóm và sẽ được kiểm tra lại sau khi có prediction-level output của nhóm LLM.

## 5.3. RQ3: Mô hình sai ở đâu và vì sao?

Trên dev, CafeBERT tạo tổng cộng 7 lỗi gồm 2 FP và 5 FN, ít nhất trong bốn mô hình đại diện. DistilBERT multilingual tạo 9 lỗi gồm 7 FP và 2 FN, phản ánh trực tiếp trade-off Recall cao nhưng cảnh báo rộng hơn. TextCNN hard-label tạo 11 lỗi gồm 4 FP và 7 FN; TextCNN distilled tạo 12 lỗi gồm 6 FP và 6 FN. So với hard-label, distillation giúp TextCNN giảm một FN nhưng tăng hai FP, phù hợp với nhận xét ở RQ1 rằng student distilled nhạy hơn với Label 1.

> **GHI CHÚ BẢNG 5.x — Tổng quan lỗi trên dev**
>
> | Mô hình | FP | FN | Tổng lỗi | Lỗi confidence ≥0,9 |
> |---|---:|---:|---:|---:|
> | CafeBERT | 2 | 5 | 7 | 5 |
> | DistilBERT multilingual | 7 | 2 | 9 | 8 |
> | TextCNN | 4 | 7 | 11 | 7 |
> | TextCNN distilled | 6 | 6 | 12 | 5 |
>
> Nguồn: [rq3_error_overview_dev.csv](C:\KLTN\KLTN\scripts\RQ2_RQ3\rq3_error_overview_dev.csv).

Tập lỗi giữa CafeBERT và DistilBERT chỉ giao nhau ở 2 mẫu, cho thấy hai encoder thất bại theo các cách khá khác nhau. CafeBERT thận trọng hơn nên có ít FP nhưng bỏ sót nhiều smishing hơn; DistilBERT bắt được nhiều smishing hơn nhưng kéo thêm các tin hợp lệ sang Label 1. Ngược lại, TextCNN và TextCNN distilled có 10 lỗi chung trên tổng hợp 13 mẫu lỗi khác nhau, với Jaccard bằng 0,7692. Mức giao nhau cao cho thấy distillation chưa thay đổi căn bản vùng quyết định của TextCNN; nó chủ yếu thay đổi mức độ nhạy trên một số mẫu biên.

Chỉ có một mẫu bị cả bốn mô hình dự đoán sai. Đây là tin đòi nợ/đe dọa thuộc Label 1, không chứa URL hay số điện thoại và được gán Level 2. Nội dung sử dụng văn phong giống một thông báo xử lý nghĩa vụ hoặc tranh chấp: “Nhận thấy có hành vi lợi dụng tín nhiệm, chiếm đoạt tài sản… yêu cầu thanh toán gấp…”. Cả bốn mô hình đều dự đoán Label 0 với xác suất sai cao; xác suất Label 1 chỉ nằm trong khoảng 0,0003–0,0318. Trường hợp này cho thấy smishing không có URL, dùng ngôn ngữ hành chính hoặc đòi nợ tương đối tự nhiên có thể nằm sâu trong vùng biểu diễn của tin nhắn hợp lệ.

Một nhóm FN khác gồm các tin có bề mặt gần với thông báo hợp lệ. Ví dụ, mẫu mang nội dung cảnh báo “ACB CẢNH BÁO SMS LỪA ĐẢO” bị CafeBERT và cả hai TextCNN dự đoán thành Label 0. Về mặt từ vựng, đây giống một cảnh báo bảo mật chính thức; tín hiệu lừa đảo nằm trong cấu trúc và liên kết cụ thể thay vì chỉ ở các từ “cảnh báo”, “mật khẩu” hoặc tên ngân hàng. Một mẫu khác thông báo sản phẩm trong giỏ hàng chưa thanh toán cũng bị ba mô hình trên bỏ sót, cho thấy văn phong thương mại điện tử hợp lệ có thể che khuất lời thúc giục truy cập liên kết.

Đối với TextCNN, các FN còn tập trung ở smishing không có URL hoặc chứa biến đổi ký tự. Một tin quảng bá dịch vụ nhạy cảm với các chuỗi như “Ng.u.c”, “KIEM”, “phuc~vu” bị cả TextCNN hard-label và distilled bỏ sót. Tuy nhiên, vì phân tích `obfuscation_level` hiện tại còn hạn chế, trường hợp này chỉ được dùng như ví dụ về văn bản phi chuẩn, không làm bằng chứng rằng một mức che giấu cụ thể gây lỗi.

False positive chủ yếu xuất hiện ở các tin hợp lệ có từ vựng và cấu trúc gần với smishing. Hai mẫu tuyển sinh/hội thảo đại học bị DistilBERT và cả hai TextCNN cảnh báo sai. Các nội dung này chứa lời chúc mừng trúng tuyển, lời mời hành động, thông tin liên hệ hoặc đường dẫn Zoom — những tín hiệu cũng phổ biến trong smishing. DistilBERT còn dự đoán sai một thông báo tuyển sinh với confidence gần 1, cho thấy mô hình có thể phụ thuộc mạnh vào tổ hợp từ khóa thúc giục và ngữ cảnh tuyển sinh.

Hai TextCNN cũng cùng tạo FP trên các câu external đời thường, chẳng hạn nội dung “t cx muốn nuôi capybara!!!!!” hoặc câu kể về phá sản và khoản nợ. Các mẫu này không có cấu trúc SMS lừa đảo điển hình nhưng chứa cách viết phi chuẩn, cảm xúc mạnh hoặc từ vựng tài chính. Đây là dấu hiệu cho thấy mô hình ký tự có thể nhạy với pattern bề mặt mà chưa hiểu đầy đủ ngữ cảnh. Tuy vậy, tổng số FP external chỉ là hai mẫu cho mỗi TextCNN nên chưa thể khái quát thành thất bại domain shift rộng.

Một điểm đáng chú ý là phần lớn lỗi có confidence cao: 5/7 lỗi của CafeBERT, 8/9 của DistilBERT và 7/11 của TextCNN có confidence từ 0,9 trở lên. Những lỗi này khó xử lý chỉ bằng cách thay đổi threshold, vì mô hình không đơn thuần lưỡng lự mà đang đặt mẫu vào sai phía của ranh giới với độ chắc chắn lớn. Hướng cải thiện phù hợp hơn là bổ sung hard examples ở các vùng như cảnh báo bảo mật hợp lệ, tuyển sinh có URL, smishing không URL và văn bản đòi nợ có phong cách hành chính.

> **GHI CHÚ BẢNG 5.x — Ví dụ lỗi tiêu biểu**
>
> Chọn khoảng 4–6 mẫu từ [rq3_representative_errors_dev.csv](C:\KLTN\KLTN\scripts\RQ2_RQ3\rq3_representative_errors_dev.csv), gồm:
>
> - Một FN mà cả bốn mô hình cùng mắc.
> - Một FN dạng cảnh báo ngân hàng/OTP giống tin hợp lệ.
> - Một FP tuyển sinh hoặc hội thảo có URL.
> - Một FP external có ngôn ngữ đời thường hoặc phi chuẩn.
>
> Nội dung nên được rút gọn và ẩn thông tin cá nhân nếu cần; ghi thêm số mô hình mắc lỗi và confidence.

Tóm lại, RQ3 cho thấy các vùng khó không chỉ là văn bản bị biến đổi mạnh. Mô hình còn thất bại khi tín hiệu lừa đảo bị đặt trong văn phong hợp lệ, khi smishing không chứa URL, hoặc khi tin hợp lệ sử dụng lời kêu gọi hành động và từ vựng bảo mật/tuyển sinh. CafeBERT kiểm soát FP tốt nhất nhưng vẫn bỏ sót một số mẫu smishing tinh vi; DistilBERT giảm FN bằng cách chấp nhận nhiều FP hơn; hai TextCNN có vùng lỗi tương tự nhau và nhạy với pattern ký tự ngoài ngữ cảnh. Những phát hiện này gợi ý rằng cải thiện tiếp theo nên tập trung vào hard-negative và hard-positive có cấu trúc gần nhau, thay vì chỉ tăng số lượng dữ liệu tổng thể.

> **GHI CHÚ KIỂM TRA cho RQ2–RQ3**
>
> - Prediction-level output của bốn LLM hiện chưa có; không diễn giải slice/error của Gemma hoặc Qwen từ metric tổng hợp.
> - Sau khi có prediction LLM, chỉ cần kiểm tra xem kết luận chính có thay đổi, không mở rộng mọi bảng thành 17 mô hình.
> - `obfuscation_level` chỉ là phân tích phụ trong Label 1; giữ placeholder cho `text_noise_level`.
> - Các ví dụ lỗi cần được rà thủ công lần cuối trước khi đưa vào báo cáo.

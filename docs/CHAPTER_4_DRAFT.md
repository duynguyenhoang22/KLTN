# CHƯƠNG 4. PHƯƠNG PHÁP VÀ THIẾT LẬP THỰC NGHIỆM

> **Quy ước biên tập**
>
> - Các khối `GHI CHÚ HÌNH`, `GHI CHÚ BẢNG` và `GHI CHÚ KIỂM TRA` là chỉ dẫn biên tập, không phải nội dung chính thức của báo cáo.
> - Số thứ tự hình và bảng sẽ được cập nhật sau khi nội dung được đưa vào file báo cáo chính.
> - Benchmark nhiều mô hình là trục thực nghiệm chính. Distillation không được trình bày như một nhánh nghiên cứu độc lập.

## 4.1. Tổng quan thiết kế thực nghiệm

Sau quá trình xây dựng và phân tích bộ dữ liệu ViSmish, chương này trình bày phương pháp thực nghiệm được sử dụng để đánh giá khả năng phát hiện tin nhắn smishing tiếng Việt của các mô hình học sâu, mô hình ngôn ngữ tiền huấn luyện và một số mô hình ngôn ngữ lớn. Thiết kế thực nghiệm không chỉ hướng đến việc xác định mô hình có kết quả tổng thể tốt nhất, mà còn làm rõ mức độ ổn định của mô hình trên các nhóm dữ liệu khác nhau, những trường hợp mô hình thường dự đoán sai và vai trò thực tế của dữ liệu tạo sinh trong quá trình huấn luyện.

Thực nghiệm trung tâm của nghiên cứu là một benchmark thống nhất gồm 17 cấu hình mô hình. Các cấu hình này thuộc ba nhóm kiến trúc chính. Nhóm thứ nhất gồm các mô hình neural xử lý văn bản ở cấp ký tự, bao gồm BiLSTM, TextCNN và các biến thể được huấn luyện bằng chưng cất tri thức từ PhoBERT-base. Nhóm thứ hai gồm các mô hình ngôn ngữ tiền huấn luyện được fine-tune cho bài toán phân loại nhị phân, bao gồm PhoBERT-base, PhoBERT-large, mBERT, VisoBERT, CafeBERT, DistilBERT multilingual, XLM-RoBERTa-base, XLM-RoBERTa-large và ViCLSR. Nhóm thứ ba bao gồm các mô hình ngôn ngữ lớn với tham số dao động từ 600 triệu tới 3 tỷ tham số, sau đó được fine-tune lại để phù hợp với bài toán hiện tại, bao gồm Gemma3-1B, Gemma-2B, Qwen3-0.6B và Qwen2.5-3B-Instruct. Việc đặt các mô hình trong cùng một giao thức dữ liệu và đánh giá cho phép so sánh tương đối công bằng giữa mô hình cấp ký tự, mô hình đơn ngữ, mô hình đa ngữ, mô hình có quy mô khác nhau và các cấu hình có hoặc không sử dụng chưng cất tri thức.

Trong thiết kế này, chưng cất tri thức không được xem là một hướng thực nghiệm tách biệt, mà được đưa trực tiếp vào benchmark như các biến thể huấn luyện tương ứng. Cách tổ chức này cho phép đánh giá tác động của chưng cất bằng phép so sánh trực tiếp giữa từng mô hình hard-label và phiên bản distilled của chính mô hình đó, đồng thời vẫn duy trì cùng dữ liệu và quy trình đánh giá với các mô hình còn lại.

Đối với các mô hình distilled, việc đánh giá không chỉ dựa trên chất lượng phân loại. Nghiên cứu còn thực hiện phân tích tính khả thi khi triển khai bằng cách so sánh các mô hình học sinh với teacher PhoBERT-base theo số lượng tham số, kích thước checkpoint, độ trễ suy luận trên CPU, thông lượng xử lý và mức sử dụng bộ nhớ cực đại. Phân tích này nhằm lượng hóa mức tài nguyên tiết kiệm được nhờ chưng cất tri thức và đặt phần cải thiện về tốc độ trong tương quan với mức suy giảm hoặc bảo toàn F1 của lớp smishing. Vì vậy, một mô hình distilled không được xem là tốt hơn teacher chỉ vì có tốc độ suy luận cao hơn; kết luận cần dựa trên đồng thời hai phương diện là hiệu quả dự đoán và chi phí triển khai.

Toàn bộ quá trình thực nghiệm được tổ chức thành bốn giai đoạn. Trước hết, bộ dữ liệu được phân chia thành tập huấn luyện, tập phát triển và tập kiểm thử theo nguồn dữ liệu, nhãn và danh mục nội dung. Tiếp theo, các mô hình benchmark được huấn luyện trên cùng giao thức và checkpoint được lựa chọn dựa trên kết quả của tập phát triển. Sau đó, kết quả dự đoán trên tập phát triển được phân tích theo nhiều lát cắt, bao gồm độ dài tin nhắn, mức độ che giấu văn bản, nguồn dữ liệu, danh mục nội dung và các metadata liên quan. Cuối cùng, hiệu năng của toàn bộ cấu hình benchmark được báo cáo trên cả tập phát triển và tập kiểm thử thông qua bốn độ đo gồm Macro-F1, F1 Label 1, Recall Label 1 và PR-AUC. Trong đó, kết quả trên tập phát triển được sử dụng để lựa chọn mô hình và phân tích chi tiết, còn kết quả trên tập kiểm thử chỉ phản ánh khả năng tổng quát hóa cuối cùng và không được dùng để điều chỉnh mô hình. Đối với teacher và các mô hình distilled đại diện, quy trình còn bổ sung phép đo hiệu quả triển khai trên cùng môi trường CPU và cùng benchmark split.

> **GHI CHÚ HÌNH 4.x — Sơ đồ quy trình thực nghiệm tổng thể**
>
> Thiết kế một sơ đồ theo chiều trái sang phải với các khối:
>
> 1. **ViSmish và các nguồn dữ liệu**  
>    `real`, `external_real`, `external_curated`, `synthetic`, `paraphrased`, `synthetic_hard_positive`.
> 2. **Phân chia dữ liệu**  
>    Train / Dev / Test và kiểm tra rò rỉ.
> 3. **Benchmark 17 cấu hình**  
>    Character-level, character-level distilled, fine-tuned PLMS và  fine-tuned LLMs.
> 4. **Đánh giá trên Dev**  
>    Báo cáo bốn metric, lựa chọn mô hình, phân tích theo lát cắt và phân tích lỗi.
> 5. **Lựa chọn mô hình**  
>    Dựa trên kết quả dev, không dựa trên test.
> 6. **Đánh giá trên Test**  
>    Báo cáo Macro-F1, F1 Label 1, Recall Label 1 và PR-AUC để đánh giá khả năng tổng quát hóa cuối cùng.
> 7. **Đánh giá tính khả thi triển khai**  
>    So sánh teacher PhoBERT-base với các mô hình distilled theo chất lượng, kích thước, độ trễ, throughput và peak RAM.
>
Thiết kế thực nghiệm trên được xây dựng để trả lời ba câu hỏi nghiên cứu. Câu hỏi thứ nhất tập trung vào sự khác biệt hiệu năng giữa các nhóm mô hình. Câu hỏi thứ hai xem xét tác động của các đặc điểm dữ liệu đến kết quả dự đoán. Câu hỏi thứ ba đi sâu vào các loại lỗi và vùng dữ liệu mà mô hình chưa xử lý tốt.

**RQ1 — Các nhóm mô hình khác nhau đạt hiệu quả như thế nào trên bộ dữ liệu ViSmish?**

Câu hỏi này được trả lời bằng benchmark giữa các mô hình character-level và các mô hình ngôn ngữ tiền huấn luyện. Ngoài kết quả tổng thể, nghiên cứu còn so sánh mô hình đơn ngữ với mô hình đa ngữ, phiên bản base với phiên bản large, cũng như mô hình hard-label với biến thể distilled. Với nhóm distilled, khả năng triển khai còn được so sánh trực tiếp với teacher PhoBERT-base thông qua số lượng tham số, kích thước mô hình, độ trễ CPU trên mỗi tin nhắn, số tin nhắn xử lý mỗi giây và bộ nhớ RAM cực đại. Mục tiêu là xác định không chỉ mô hình có hiệu năng cao nhất, mà còn mức đánh đổi giữa chất lượng dự đoán, độ phức tạp kiến trúc và chi phí triển khai.

**RQ2 — Độ dài, mức độ che giấu và các đặc điểm metadata ảnh hưởng như thế nào đến khả năng phát hiện smishing?**

Kết quả tổng thể có thể che khuất sự khác biệt giữa các nhóm dữ liệu. Vì vậy, dự đoán trên tập phát triển được phân tích theo độ dài tin nhắn, `obfuscation_level`, `data_origin`, `category`, sự xuất hiện của URL, số điện thoại và loại người gửi. Phân tích này nhằm xác định những lát cắt mà hiệu năng suy giảm, đồng thời kiểm tra liệu các nhóm kiến trúc có phản ứng khác nhau trước văn bản ngắn, văn bản nhiễu hoặc dữ liệu ngoài miền hay không.

**RQ3 — Các mô hình thường thất bại ở những trường hợp nào và nguyên nhân có thể là gì?**

Câu hỏi này được trả lời thông qua ma trận nhầm lẫn và phân tích các trường hợp false positive, false negative. Các lỗi được nhóm theo đặc điểm nội dung và metadata để nhận diện những khuynh hướng lặp lại, chẳng hạn tin nhắn smishing có bề mặt giống thông báo OTP hợp lệ, tin nhắn hợp lệ chứa URL hoặc ngôn ngữ cảnh báo, văn bản có mức che giấu cao và các mẫu nằm ngoài miền SMS thông thường. Ngoài việc thống kê số lỗi, nghiên cứu xem xét các ví dụ đại diện và so sánh tập lỗi giữa một số mô hình tiêu biểu.

> **GHI CHÚ BẢNG - Bảng ánh xạ câu hỏi nghiên cứu với phương pháp đánh giá**
>
> | Câu hỏi nghiên cứu | Nội dung cần đánh giá | Nguồn bằng chứng chính |
> |---|---|---|
> | RQ1 | So sánh hiệu năng giữa các nhóm và cấu hình mô hình; đánh giá trade-off chất lượng–tài nguyên của mô hình distilled | Bốn độ đo benchmark trên dev/test; benchmark triển khai CPU |
> | RQ2 | Ảnh hưởng của độ dài, obfuscation và metadata | Slice analysis trên dev |
> | RQ3 | False positive, false negative và các vùng lỗi | Confusion matrix, prediction-level error analysis |
>
> Bảng này nên xuất hiện ngay sau phần trình bày ba RQ. Chưa đưa giá trị metric vào bảng vì đây là bảng thiết kế nghiên cứu, không phải bảng kết quả.

> **GHI CHÚ BẢNG - Bảng mô tả tiêu chí đánh giá khả năng triển khai**
>
> Bảng phương pháp nên mô tả các tiêu chí sau:
>
> | Tiêu chí | Đơn vị | Ý nghĩa |
> |---|---|---|
> | Số lượng tham số | tham số | Mức độ phức tạp của mô hình |
> | Kích thước checkpoint | MB | Dung lượng lưu trữ cần thiết |
> | Độ trễ CPU | ms/tin nhắn | Thời gian xử lý một mẫu với batch size 1 sau warm-up |
> | Thông lượng | tin nhắn/giây | Khả năng xử lý theo batch |
> | Bộ nhớ cực đại | MB | Peak RAM trong quá trình suy luận |
> | F1 Label 1 | điểm F1 | Chất lượng phát hiện smishing được giữ lại |
>
> Điều kiện đo phải được ghi rõ: cùng thiết bị CPU, cùng tập dữ liệu, cùng quy trình warm-up và số lần lặp. Bảng kết quả có giá trị cụ thể nên đặt ở Chương 5, không đặt tại đây.

> **GHI CHÚ LIÊN KẾT VỚI CHƯƠNG 5**
>
> Mục 4.1 chỉ giới thiệu mục tiêu đánh giá khả năng triển khai. Giao thức và cách đo chi tiết sẽ được trình bày tại phần thiết lập thực nghiệm tương ứng của Chương 4. Các giá trị đo, bảng so sánh và biểu đồ trade-off giữa F1 Label 1 với độ trễ, kích thước mô hình hoặc bộ nhớ phải được đặt tại phần phân tích RQ1 của Chương 5.

Từ ba câu hỏi trên, chương này lần lượt trình bày dữ liệu và chiến lược phân chia, các mô hình tham gia benchmark, thiết lập huấn luyện, độ đo đánh giá, phương pháp phân tích kết quả. Kết quả tương ứng sẽ được trình bày ở chương tiếp theo theo từng câu hỏi nghiên cứu, thay vì theo thứ tự triển khai kỹ thuật của các thí nghiệm.

> **GHI CHÚ KIỂM TRA trước khi đưa vào báo cáo**
>
> - Chương 5 sử dụng tên chính thức “Kết quả và phân tích”.
> - Benchmark cuối cùng gồm 17 cấu hình.
> - Kết quả benchmark được báo cáo trên cả dev và test với bốn độ đo: Macro-F1, F1 Label 1, Recall Label 1 và PR-AUC.
> - Dev được dùng để lựa chọn mô hình và phân tích; test chỉ được dùng để báo cáo khả năng tổng quát hóa, tránh lựa chọn mô hình theo test.
> - Không chèn kết quả dev/test cụ thể vào Mục 4.1.
> - Khi tạo sơ đồ, không sử dụng lại hình “hai nhánh thực nghiệm” trong báo cáo cũ.
> - Khi viết phần triển khai, chỉ so sánh số đo được thu thập trên cùng thiết bị và cùng giao thức; không so sánh trực tiếp thời gian từ các lần chạy khác môi trường.
> - Phép đo tính khả thi triển khai sẽ được chạy lại trên benchmark split để đồng nhất với giao thức so sánh mô hình chính.

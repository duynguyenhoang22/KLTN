# CHƯƠNG 4. PHƯƠNG PHÁP VÀ THIẾT LẬP THỰC NGHIỆM

> **Quy ước biên tập**
>
> - Các khối `GHI CHÚ HÌNH`, `GHI CHÚ BẢNG` và `GHI CHÚ KIỂM TRA` là chỉ dẫn biên tập, không phải nội dung chính thức của báo cáo.
> - Số thứ tự hình và bảng sẽ được cập nhật sau khi nội dung được đưa vào file báo cáo chính.
> - Benchmark nhiều mô hình là trục thực nghiệm chính. TSTR, augmentation và distillation không được trình bày như các nhánh nghiên cứu độc lập.

## 4.1. Tổng quan thiết kế thực nghiệm

Sau quá trình xây dựng và phân tích bộ dữ liệu ViSmish, chương này trình bày phương pháp thực nghiệm được sử dụng để đánh giá khả năng phát hiện tin nhắn smishing tiếng Việt của các mô hình học sâu, mô hình ngôn ngữ tiền huấn luyện và một số mô hình ngôn ngữ lớn. Thiết kế thực nghiệm không chỉ hướng đến việc xác định mô hình có kết quả tổng thể tốt nhất, mà còn làm rõ mức độ ổn định của mô hình trên các nhóm dữ liệu khác nhau, những trường hợp mô hình thường dự đoán sai và vai trò thực tế của dữ liệu tạo sinh trong quá trình huấn luyện.

Thực nghiệm trung tâm của nghiên cứu là một benchmark thống nhất gồm 17 cấu hình mô hình. Các cấu hình này thuộc ba nhóm kiến trúc chính. Nhóm thứ nhất gồm các mô hình neural xử lý văn bản ở cấp ký tự, bao gồm BiLSTM, TextCNN và các biến thể được huấn luyện bằng chưng cất tri thức từ PhoBERT-base. Nhóm thứ hai gồm các mô hình ngôn ngữ tiền huấn luyện được fine-tune cho bài toán phân loại nhị phân, bao gồm PhoBERT-base, PhoBERT-large, mBERT, VisoBERT, CafeBERT, DistilBERT multilingual, XLM-RoBERTa-base, XLM-RoBERTa-large và ViCLSR. Nhóm thứ ba gồm bốn mô hình ngôn ngữ lớn được thích nghi cho bài toán hiện tại: Gemma 3 1B, Gemma 2B, Qwen3 0.6B và Qwen2.5 0.5B. Việc đặt các mô hình trong cùng một giao thức dữ liệu và đánh giá cho phép so sánh tương đối công bằng giữa mô hình cấp ký tự, mô hình đơn ngữ, mô hình đa ngữ, mô hình có quy mô khác nhau và các cấu hình có hoặc không sử dụng chưng cất tri thức.

Trong thiết kế này, chưng cất tri thức không được xem là một hướng thực nghiệm tách biệt, mà được đưa trực tiếp vào benchmark như các biến thể huấn luyện tương ứng. Cách tổ chức này cho phép đánh giá tác động của chưng cất bằng phép so sánh trực tiếp giữa từng mô hình hard-label và phiên bản distilled của chính mô hình đó, đồng thời vẫn duy trì cùng dữ liệu và quy trình đánh giá với các mô hình còn lại.

Đối với các mô hình distilled, việc đánh giá không chỉ dựa trên chất lượng phân loại. Nghiên cứu còn thực hiện phân tích tính khả thi khi triển khai bằng cách so sánh các mô hình học sinh với teacher PhoBERT-base theo số lượng tham số, kích thước checkpoint, độ trễ suy luận trên CPU, thông lượng xử lý và mức sử dụng bộ nhớ cực đại. Phân tích này nhằm lượng hóa mức tài nguyên tiết kiệm được nhờ chưng cất tri thức và đặt phần cải thiện về tốc độ trong tương quan với mức suy giảm hoặc bảo toàn F1 của lớp smishing. Vì vậy, một mô hình distilled không được xem là tốt hơn teacher chỉ vì có tốc độ suy luận cao hơn; kết luận cần dựa trên đồng thời hai phương diện là hiệu quả dự đoán và chi phí triển khai.

Bên cạnh benchmark chính, nghiên cứu thực hiện các thí nghiệm bổ sung nhằm phân tích giá trị của dữ liệu tạo sinh. Các thí nghiệm này lần lượt kiểm tra ba vấn đề: khả năng sử dụng dữ liệu tạo sinh để thay thế dữ liệu thật thông qua thiết lập Train on Synthetic, Test on Real (TSTR); khả năng bổ sung dữ liệu tạo sinh của lớp smishing vào dữ liệu huấn luyện thật; và ảnh hưởng của việc mở rộng lớp tin nhắn hợp lệ bằng dữ liệu tạo sinh hoặc dữ liệu chéo miền. Những thí nghiệm này không nhằm tạo ra một hệ thống benchmark riêng, mà cung cấp bằng chứng để xác định dữ liệu tạo sinh nên được sử dụng độc lập hay chỉ nên đóng vai trò tăng cường dữ liệu.

Toàn bộ quá trình thực nghiệm được tổ chức thành bốn giai đoạn. Trước hết, bộ dữ liệu được phân chia thành tập huấn luyện, tập phát triển và tập kiểm thử theo nguồn dữ liệu, nhãn và danh mục nội dung. Tiếp theo, các mô hình benchmark được huấn luyện trên cùng giao thức và checkpoint được lựa chọn dựa trên kết quả của tập phát triển. Sau đó, kết quả dự đoán trên tập phát triển được phân tích theo nhiều lát cắt, bao gồm độ dài tin nhắn, mức độ che giấu văn bản, nguồn dữ liệu, danh mục nội dung và các metadata liên quan. Cuối cùng, hiệu năng của toàn bộ cấu hình benchmark được báo cáo trên cả tập phát triển và tập kiểm thử thông qua bốn độ đo gồm Macro-F1, F1 Label 1, Recall Label 1 và PR-AUC. Trong đó, kết quả trên tập phát triển được sử dụng để lựa chọn mô hình và phân tích chi tiết, còn kết quả trên tập kiểm thử chỉ phản ánh khả năng tổng quát hóa cuối cùng và không được dùng để điều chỉnh mô hình. Đối với teacher và các mô hình distilled đại diện, quy trình còn bổ sung phép đo hiệu quả triển khai trên cùng môi trường CPU và cùng benchmark split. Song song với quy trình này, nhóm thí nghiệm TSTR và augmentation được sử dụng để phân tích riêng vai trò của từng nguồn dữ liệu huấn luyện.

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
> Có thể đặt một nhánh phụ bên dưới khối dữ liệu với tên **“Phân tích vai trò dữ liệu tạo sinh”**, gồm TSTR, positive augmentation và negative/domain augmentation. Nhánh này nối về phần phân tích kết quả, không nối thành một benchmark độc lập.

Thiết kế thực nghiệm trên được xây dựng để trả lời bốn câu hỏi nghiên cứu. Câu hỏi thứ nhất tập trung vào sự khác biệt hiệu năng giữa các nhóm mô hình. Câu hỏi thứ hai xem xét tác động của các đặc điểm dữ liệu đến kết quả dự đoán. Câu hỏi thứ ba đi sâu vào các loại lỗi và vùng dữ liệu mà mô hình chưa xử lý tốt. Câu hỏi cuối cùng đánh giá vai trò phù hợp của dữ liệu tạo sinh trong bối cảnh dữ liệu smishing tiếng Việt còn hạn chế.

**RQ1 — Các nhóm mô hình khác nhau đạt hiệu quả như thế nào trên bộ dữ liệu ViSmish?**

Câu hỏi này được trả lời bằng benchmark giữa các mô hình character-level và các mô hình ngôn ngữ tiền huấn luyện. Ngoài kết quả tổng thể, nghiên cứu còn so sánh mô hình đơn ngữ với mô hình đa ngữ, phiên bản base với phiên bản large, cũng như mô hình hard-label với biến thể distilled. Với nhóm distilled, khả năng triển khai còn được so sánh trực tiếp với teacher PhoBERT-base thông qua số lượng tham số, kích thước mô hình, độ trễ CPU trên mỗi tin nhắn, số tin nhắn xử lý mỗi giây và bộ nhớ RAM cực đại. Mục tiêu là xác định không chỉ mô hình có hiệu năng cao nhất, mà còn mức đánh đổi giữa chất lượng dự đoán, độ phức tạp kiến trúc và chi phí triển khai.

**RQ2 — Độ dài, mức độ che giấu và các đặc điểm metadata ảnh hưởng như thế nào đến khả năng phát hiện smishing?**

Kết quả tổng thể có thể che khuất sự khác biệt giữa các nhóm dữ liệu. Vì vậy, dự đoán trên tập phát triển được phân tích theo độ dài tin nhắn, `obfuscation_level`, `data_origin`, `category`, sự xuất hiện của URL, số điện thoại và loại người gửi. Phân tích này nhằm xác định những lát cắt mà hiệu năng suy giảm, đồng thời kiểm tra liệu các nhóm kiến trúc có phản ứng khác nhau trước văn bản ngắn, văn bản nhiễu hoặc dữ liệu ngoài miền hay không.

**RQ3 — Các mô hình thường thất bại ở những trường hợp nào và nguyên nhân có thể là gì?**

Câu hỏi này được trả lời thông qua ma trận nhầm lẫn và phân tích các trường hợp false positive, false negative. Các lỗi được nhóm theo đặc điểm nội dung và metadata để nhận diện những khuynh hướng lặp lại, chẳng hạn tin nhắn smishing có bề mặt giống thông báo OTP hợp lệ, tin nhắn hợp lệ chứa URL hoặc ngôn ngữ cảnh báo, văn bản có mức che giấu cao và các mẫu nằm ngoài miền SMS thông thường. Ngoài việc thống kê số lỗi, nghiên cứu xem xét các ví dụ đại diện và so sánh tập lỗi giữa một số mô hình tiêu biểu.

**RQ4 — Dữ liệu tạo sinh mang lại giá trị gì cho bài toán và nên được sử dụng theo cách nào?**

Để trả lời câu hỏi này, nghiên cứu không chỉ so sánh hiệu năng của mô hình được huấn luyện bằng dữ liệu thật và dữ liệu tạo sinh. Các thiết lập TSTR được dùng để kiểm tra khả năng thay thế dữ liệu thật; các thiết lập positive augmentation đánh giá tác động của việc bổ sung synthetic Label 1; trong khi negative augmentation và external challenge kiểm tra khả năng kiểm soát false positive khi miền Label 0 được mở rộng. Qua đó, nghiên cứu hướng đến việc xác định vai trò phù hợp của dữ liệu tạo sinh thay vì mặc định rằng số lượng dữ liệu lớn hơn luôn dẫn đến kết quả tốt hơn.

> **GHI CHÚ BẢNG - Bảng ánh xạ câu hỏi nghiên cứu với phương pháp đánh giá**
>
> | Câu hỏi nghiên cứu | Nội dung cần đánh giá | Nguồn bằng chứng chính |
> |---|---|---|
> | RQ1 | So sánh hiệu năng giữa các nhóm và cấu hình mô hình; đánh giá trade-off chất lượng–tài nguyên của mô hình distilled | Bốn độ đo benchmark trên dev/test; benchmark triển khai CPU |
> | RQ2 | Ảnh hưởng của độ dài, obfuscation và metadata | Slice analysis trên dev |
> | RQ3 | False positive, false negative và các vùng lỗi | Confusion matrix, prediction-level error analysis |
> | RQ4 | Khả năng thay thế và tăng cường của dữ liệu tạo sinh | Real-only, TSTR, positive/negative augmentation, external challenge |
>
> Bảng này nên xuất hiện ngay sau phần trình bày bốn RQ. Chưa đưa giá trị metric vào bảng vì đây là bảng thiết kế nghiên cứu, không phải bảng kết quả.

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

Từ bốn câu hỏi trên, chương này lần lượt trình bày dữ liệu và chiến lược phân chia, các mô hình tham gia benchmark, thiết lập huấn luyện, độ đo đánh giá, phương pháp phân tích kết quả và các thí nghiệm bổ sung về dữ liệu tạo sinh. Kết quả tương ứng sẽ được trình bày ở chương tiếp theo theo từng câu hỏi nghiên cứu, thay vì theo thứ tự triển khai kỹ thuật của các thí nghiệm.

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

## 4.2. Dữ liệu và chiến lược phân chia

Để bảo đảm kết quả giữa 17 cấu hình mô hình có thể so sánh trực tiếp, benchmark sử dụng một bộ train, dev và test thống nhất được tạo từ phiên bản hoàn chỉnh của ViSmish. Chiến lược phân chia được thiết kế theo hai yêu cầu. Thứ nhất, tập phát triển và tập kiểm thử chỉ chứa dữ liệu thật hoặc dữ liệu chéo miền đã được thu thập và tuyển chọn, qua đó tránh đánh giá mô hình trên chính kiểu dữ liệu tạo sinh đã xuất hiện trong huấn luyện. Thứ hai, phân phối của các nguồn dữ liệu, nhãn và danh mục nội dung cần được duy trì tương đối ổn định giữa dev và test để hạn chế sai lệch do cách chia dữ liệu.

Bộ dữ liệu đầu vào của benchmark gồm 10.562 mẫu với sáu giá trị `data_origin`: `real`, `external_real`, `external_curated`, `synthetic`, `paraphrased` và `synthetic_hard_positive`. Các nguồn này khác nhau cả về phương thức hình thành lẫn vai trò trong thực nghiệm.

Nguồn `real` gồm 2.567 tin nhắn được thu thập từ dữ liệu thực tế, trong đó có 2.321 mẫu Label 0 và 246 mẫu Label 1. Đây là nguồn duy nhất chứa đồng thời tin nhắn hợp lệ và tin nhắn smishing thực, vì vậy giữ vai trò neo mô hình vào phân phối của miền đích.

Hai nguồn `external_real` và `external_curated` bổ sung tổng cộng 1.001 mẫu Label 0. Trong đó, `external_real` gồm 500 mẫu văn bản giao tiếp thông thường, còn `external_curated` gồm 501 hard negative đã được tuyển chọn. Hai nguồn này được sử dụng để mở rộng miền của lớp hợp lệ, đặc biệt đối với các dạng văn bản không có cấu trúc giống tin nhắn brandname hoặc thông báo viễn thông thường chiếm ưu thế trong dữ liệu thật. Do chỉ chứa Label 0, các nguồn external có vai trò quan trọng khi đánh giá khả năng kiểm soát false positive và mức độ bền vững trước sự thay đổi miền dữ liệu.

Nhóm dữ liệu tạo sinh gồm ba nguồn. Nguồn `synthetic` có 2.008 mẫu, gồm 1.998 mẫu Label 0 và 10 mẫu Label 1. Nguồn `paraphrased` gồm 4.333 mẫu Label 1 được tạo bằng cách diễn giải lại các nội dung smishing. Nguồn `synthetic_hard_positive` gồm 653 mẫu Label 1 được xây dựng nhằm tạo ra các trường hợp smishing có ranh giới khó hơn và có bề mặt gần với tin nhắn hợp lệ. Tổng thể, các nguồn tạo sinh giúp mở rộng số lượng và sự đa dạng của dữ liệu huấn luyện, nhưng không được đưa vào dev hoặc test.

> **GHI CHÚ BẢNG — Cần bảng thành phần dữ liệu theo nguồn và nhãn**
>
> | Nguồn dữ liệu | Label 0 | Label 1 | Tổng | Vai trò trong benchmark |
> |---|---:|---:|---:|---|
> | `real` | 2.321 | 246 | 2.567 | Dữ liệu miền đích; chia vào train/dev/test |
> | `external_real` | 500 | 0 | 500 | Mở rộng miền Label 0; chia vào train/dev/test |
> | `external_curated` | 501 | 0 | 501 | Hard negative Label 0; chia vào train/dev/test |
> | `synthetic` | 1.998 | 10 | 2.008 | Dữ liệu tạo sinh; chỉ dùng cho train |
> | `paraphrased` | 0 | 4.333 | 4.333 | Smishing được paraphrase; chỉ dùng cho train |
> | `synthetic_hard_positive` | 0 | 653 | 653 | Smishing khó; chỉ dùng cho train |
> | **Tổng** | **5.320** | **5.242** | **10.562** | — |
>
> Bảng này là bảng mô tả dữ liệu sử dụng trong thực nghiệm. Nếu Chương 3 đã có một bảng gần như tương tự, Chương 4 có thể rút gọn và dẫn chiếu lại thay vì lặp toàn bộ phần giải thích.

Các cột metadata như `sender_type`, `category`, `obfuscation_level`, `has_url` và `has_phone_number` được giữ lại trong các split để phục vụ phân tích kết quả. Tuy nhiên, các thuộc tính này không được sử dụng trực tiếp làm đầu vào cho mô hình benchmark. Đầu vào dự đoán của mô hình là nội dung văn bản; metadata chỉ được dùng để thực hiện stratified split và phân tích hiệu năng theo từng lát cắt. Cách thiết kế này hạn chế nguy cơ rò rỉ nhãn từ các thuộc tính được xây dựng trong quá trình tạo hoặc gán nhãn dữ liệu, đặc biệt là `category` và `obfuscation_level`.

Từ thành phần dữ liệu trên, quá trình phân chia được thực hiện với seed cố định bằng 42. Các mẫu thuộc ba nguồn gần với dữ liệu đánh giá thực tế, gồm `real`, `external_real` và `external_curated`, được chia theo tỷ lệ mục tiêu 70% cho train, 15% cho dev và 15% cho test. Quá trình phân tầng sử dụng khóa kết hợp `label × data_origin × category`. So với chỉ phân tầng theo nhãn, khóa kết hợp này giúp dev và test duy trì tốt hơn thành phần nguồn dữ liệu và các nhóm nội dung, đồng thời hạn chế trường hợp một category chỉ xuất hiện trong một split.

Các nguồn `synthetic`, `paraphrased` và `synthetic_hard_positive` được đưa toàn bộ vào train. Chính sách train-only này được áp dụng vì mục tiêu của benchmark là đánh giá khả năng mô hình học từ dữ liệu tổng hợp nhưng vẫn tổng quát hóa sang dữ liệu thật hoặc dữ liệu chéo miền. Nếu đưa dữ liệu tạo sinh vào dev hoặc test, kết quả có thể phản ánh mức độ mô hình nhận diện các mẫu cùng quy trình tạo sinh thay vì năng lực phát hiện smishing trong điều kiện thực tế.

Do phân tầng được thực hiện đồng thời theo nhãn, nguồn và category, một số strata có số lượng mẫu rất nhỏ. Với strata có dưới 5 mẫu, toàn bộ dữ liệu được giữ lại trong train để tránh tạo ra các tập đánh giá chỉ có một mẫu không ổn định. Theo quy tắc triển khai, strata từ 5 đến dưới 10 mẫu được ưu tiên giữ phần lớn trong train và tối đa một mẫu trong dev; các strata đủ lớn mới được chia theo tỷ lệ 70/15/15. Trong dữ liệu hiện tại, các category thực có quy mô rất nhỏ như “Dịch vụ y tế”, “Thương mại điện tử” và một số trường hợp Label 1 thuộc nhóm “Crypto / Đầu tư giả” được giữ hoàn toàn trong train. Vì vậy, dev và test không đại diện đầy đủ cho mọi category hiếm, và giới hạn này cần được cân nhắc khi diễn giải kết quả theo danh mục.

Sau khi áp dụng chính sách trên, tập train có 9.492 mẫu, trong khi dev và test đều có 535 mẫu. Tỷ lệ trên toàn bộ bộ dữ liệu lần lượt là 89,87%, 5,07% và 5,07%. Tỷ lệ toàn cục không còn là 70/15/15 vì 6.994 mẫu thuộc các nguồn tạo sinh được giữ hoàn toàn trong train. Tỷ lệ 70/15/15 chỉ áp dụng cho nhóm nguồn có khả năng xuất hiện trong holdout gồm `real`, `external_real` và `external_curated`.

> **GHI CHÚ BẢNG — Cần bảng phân phối train/dev/test**
>
> | Split | Tổng số mẫu | Label 0 | Label 1 | `real` | `external_real` | `external_curated` | Dữ liệu tạo sinh |
> |---|---:|---:|---:|---:|---:|---:|---:|
> | Train | 9.492 | 4.324 | 5.168 | 1.797 | 350 | 351 | 6.994 |
> | Dev | 535 | 498 | 37 | 385 | 75 | 75 | 0 |
> | Test | 535 | 498 | 37 | 385 | 75 | 75 | 0 |
>
> Trong cột “Dữ liệu tạo sinh”, cần ghi chú đây là tổng của `synthetic`, `paraphrased` và `synthetic_hard_positive`.

Dev và test có cùng quy mô và cùng phân phối nguồn: mỗi tập gồm 385 mẫu `real`, 75 mẫu `external_real` và 75 mẫu `external_curated`. Về nhãn, mỗi tập có 498 mẫu Label 0 và 37 mẫu Label 1, tương ứng tỷ lệ smishing khoảng 6,92%. Phân phối mất cân bằng này gần với bối cảnh triển khai hơn bộ dữ liệu tổng thể đã được cân bằng bằng dữ liệu tạo sinh, đồng thời cho thấy vì sao Accuracy không phù hợp để sử dụng làm độ đo chính.

Tập train có 4.324 mẫu Label 0 và 5.168 mẫu Label 1. Việc Label 1 chiếm tỷ lệ cao hơn trong train chủ yếu đến từ 4.333 mẫu `paraphrased` và 653 mẫu `synthetic_hard_positive`. Sự khác biệt phân phối giữa train và các tập holdout là có chủ đích: train sử dụng dữ liệu tạo sinh để mở rộng tín hiệu smishing, trong khi dev và test giữ phân phối mất cân bằng của dữ liệu không tạo sinh để kiểm tra khả năng tổng quát hóa.

> **GHI CHÚ HÌNH — Có thể bổ sung sơ đồ luồng nguồn dữ liệu vào từng split**
>
> Sơ đồ nên có sáu nguồn dữ liệu ở bên trái và ba split ở bên phải:
>
> - `real`, `external_real`, `external_curated` → Train 70%, Dev 15%, Test 15%.
> - `synthetic`, `paraphrased`, `synthetic_hard_positive` → Train 100%.
>
> Hình này chỉ cần thiết nếu sơ đồ tổng quan ở Mục 4.1 chưa thể hiện rõ chính sách train-only của dữ liệu tạo sinh. Nếu Hình 4.1 đã thể hiện đầy đủ, nên dùng bảng phân phối thay vì tạo thêm một hình có nội dung trùng lặp.

Để các split trên có thể được sử dụng như một giao thức đánh giá đáng tin cậy, dữ liệu nguồn được kiểm tra tính đầy đủ của chín trường bắt buộc gồm `sample_id`, `content`, `label`, `has_url`, `has_phone_number`, `sender_type`, `category`, `obfuscation_level` và `data_origin` trước khi tiến hành phân chia. Quy trình dừng nếu phát hiện giá trị thiếu, `sample_id` trùng, nội dung trùng chính xác hoặc giá trị `data_origin` không thuộc sáu nguồn đã định nghĩa.

Sau khi chia dữ liệu, mức độ giao nhau giữa từng cặp train, dev và test được kiểm tra riêng theo `sample_id` và nội dung văn bản. Kết quả hiện tại không phát hiện `sample_id` hoặc nội dung trùng chính xác giữa train–dev, train–test và dev–test. Kiểm tra này giúp bảo đảm một mẫu không xuất hiện trực tiếp trong nhiều split và hạn chế trường hợp kết quả bị thổi phồng do mô hình đã nhìn thấy cùng nội dung trong huấn luyện.

> **GHI CHÚ BẢNG — Cần bảng kết quả kiểm tra overlap**
>
> | Cặp split | Trùng `sample_id` | Trùng nội dung chính xác |
> |---|---:|---:|
> | Train – Dev | 0 | 0 |
> | Train – Test | 0 | 0 |
> | Dev – Test | 0 | 0 |

Tuy nhiên, kiểm tra hiện tại mới xác nhận không có bản sao chính xác. Các mẫu paraphrase hoặc các nội dung gần trùng có thể không bị phát hiện nếu khác nhau về chữ hoa–chữ thường, khoảng trắng, dấu câu, URL, số điện thoại hoặc một số từ bề mặt. Trước khi hoàn thiện báo cáo, cần bổ sung ít nhất một phép kiểm tra trùng sau chuẩn hóa nội dung; nếu điều kiện cho phép, nên kiểm tra thêm near-duplicate bằng n-gram hoặc độ tương đồng embedding. Kết quả của các kiểm tra bổ sung cần được cập nhật vào bảng overlap và phần mô tả này.

> **GHI CHÚ KIỂM TRA RÒ RỈ CẦN HOÀN THIỆN**
>
> - Chuẩn hóa lowercase, khoảng trắng và dấu câu rồi kiểm tra duplicate.
> - Cân nhắc chuẩn hóa URL và số điện thoại thành placeholder trước khi kiểm tra.
> - Kiểm tra near-duplicate giữa các nguồn `paraphrased`/`synthetic_hard_positive` trong train với các mẫu `real` ở dev và test.
> - Không tuyên bố “không có data leakage” tuyệt đối khi mới chỉ kiểm tra trùng chính xác.

Trên nền tảng dữ liệu đã được phân chia và kiểm tra như trên, tập phát triển và tập kiểm thử đảm nhiệm hai vai trò khác nhau trong quy trình thực nghiệm. Tập dev được sử dụng trong quá trình phát triển mô hình, bao gồm lựa chọn checkpoint, theo dõi early stopping, lựa chọn cấu hình và thực hiện các phân tích chi tiết theo độ dài, mức độ che giấu, nguồn dữ liệu, category và các metadata khác. Kết quả trên dev cũng là căn cứ chính để so sánh và lựa chọn mô hình trong RQ1.

Tập test được giữ tách biệt với quá trình huấn luyện và lựa chọn mô hình. Sau khi các cấu hình đã được cố định, toàn bộ 17 cấu hình benchmark được đánh giá trên test bằng bốn độ đo Macro-F1, F1 Label 1, Recall Label 1 và PR-AUC. Việc báo cáo kết quả của nhiều mô hình trên test nhằm cung cấp một bảng benchmark đầy đủ; tuy nhiên, các kết quả test không được sử dụng để điều chỉnh hyperparameter, threshold hoặc thay đổi quyết định lựa chọn mô hình đã đưa ra từ dev.

Các phân tích chuyên sâu trong Chương 5 chủ yếu được thực hiện trên dev. Cách tổ chức này cho phép khảo sát nhiều lát cắt và đọc các trường hợp dự đoán sai mà không sử dụng thông tin từ test để dẫn dắt quá trình phát triển. Test được dành cho việc xác nhận liệu những xu hướng và kết luận hình thành từ dev có tiếp tục được duy trì trên dữ liệu chưa được sử dụng trong quá trình lựa chọn hay không.

Đối với phép đo tính khả thi triển khai, teacher PhoBERT-base và các mô hình distilled đại diện sẽ được chạy lại trên benchmark split trong cùng môi trường phần cứng và cùng giao thức suy luận. Việc đồng nhất dữ liệu, thiết bị, batch size, số lần warm-up và số lần đo là điều kiện cần để các số liệu về độ trễ, thông lượng và bộ nhớ có thể so sánh trực tiếp.

> **GHI CHÚ BẢNG — Nên có bảng tóm tắt vai trò của từng split**
>
> | Split | Vai trò | Được phép sử dụng cho |
> |---|---|---|
> | Train | Học tham số mô hình | Huấn luyện và tạo soft label cho student |
> | Dev | Phát triển và lựa chọn mô hình | Checkpoint, early stopping, lựa chọn cấu hình, result analysis |
> | Test | Đánh giá cuối cùng | Báo cáo bốn metric và kiểm tra khả năng tổng quát hóa |

> **GHI CHÚ KIỂM TRA trước khi kết thúc Mục 4.2**
>
> - Xác nhận bộ split cuối cùng vẫn có kích thước Train/Dev/Test lần lượt là 9.492/535/535 sau khi hoàn thiện 17 cấu hình.
> - Xác nhận mọi cấu hình benchmark sử dụng đúng cùng ba file split.
> - Xác nhận không có bước điều chỉnh threshold riêng dựa trên test.
> - Chạy và lưu báo cáo duplicate sau chuẩn hóa và near-duplicate trước khi thay ghi chú rò rỉ bằng kết luận cuối.
> - Nếu thay đổi split, cập nhật đồng thời bảng phân phối, benchmark và phép đo tính khả thi triển khai.

## 4.3. Các mô hình benchmark

Benchmark được xây dựng để khảo sát một phổ kiến trúc tương đối rộng thay vì chỉ tìm kiếm kết quả tốt nhất trong một họ mô hình. Mười bảy cấu hình được lựa chọn đại diện cho ba mức độ phức tạp: các mạng neural gọn nhẹ xử lý trực tiếp chuỗi ký tự, các mô hình encoder tiền huấn luyện được fine-tune cho phân loại văn bản và các mô hình ngôn ngữ lớn có năng lực biểu diễn cao hơn. Cách tổ chức này tạo cơ sở để phân tích đồng thời chất lượng dự đoán, khả năng xử lý văn bản nhiễu và mức đánh đổi về tài nguyên triển khai.

Ở nhóm đầu tiên, BiLSTM và TextCNN được xây dựng trên biểu diễn cấp ký tự. Nội dung tin nhắn được chuyển thành chuỗi chỉ số ký tự sau khi đưa về chữ thường, nhờ đó mô hình không phụ thuộc vào bước tách từ và có thể giữ lại các dấu hiệu bề mặt như lỗi chính tả, viết tắt, chuỗi số, URL, leet và các biến thể che giấu. Đây là những hiện tượng thường xuất hiện trong tin nhắn smishing và có thể bị phân mảnh khi sử dụng tokenizer theo từ hoặc subword.

BiLSTM xử lý chuỗi theo cả hai chiều nhằm tổng hợp ngữ cảnh trước và sau của mỗi vị trí ký tự. Đầu ra tuần tự được kết hợp bằng mean pooling và max pooling trước khi đưa qua lớp phân loại nhị phân. Mean pooling cung cấp biểu diễn tổng quát của toàn bộ tin nhắn, trong khi max pooling nhấn mạnh các tín hiệu cục bộ nổi bật. BiLSTM vì vậy đóng vai trò mô hình tuần tự gọn nhẹ, cho phép kiểm tra liệu quan hệ dài hạn giữa các ký tự có đủ để nhận diện smishing hay không.

TextCNN sử dụng nhiều bộ lọc tích chập một chiều với các kích thước kernel khác nhau để phát hiện những mẫu ký tự cục bộ. Sau phép max pooling, các đặc trưng từ từng nhóm kernel được nối lại và đưa vào lớp phân loại. Kiến trúc này phù hợp với những tín hiệu ngắn và có tính lặp lại như tiền tố URL, tên miền bất thường, chuỗi số điện thoại, từ khóa yêu cầu hành động hoặc các cụm ký tự đã bị biến đổi. So với BiLSTM, TextCNN ưu tiên khả năng nhận diện pattern cục bộ và có thể thực hiện suy luận song song hiệu quả hơn.

Mỗi kiến trúc character-level được huấn luyện theo hai chế độ, tạo thành bốn cấu hình trong benchmark: BiLSTM hard-label, TextCNN hard-label, BiLSTM distilled từ PhoBERT-base và TextCNN distilled từ PhoBERT-base. Hai cấu hình hard-label chỉ học từ nhãn gốc. Với hai cấu hình distilled, PhoBERT-base đóng vai trò teacher và sinh xác suất mềm cho các mẫu dữ liệu. Student được huấn luyện bằng sự kết hợp giữa nhãn cứng và soft target của teacher, qua đó có thể tiếp nhận thêm thông tin về mức độ chắc chắn và quan hệ giữa hai lớp.

Ảnh hưởng của distillation được đánh giá bằng cách đối chiếu từng student distilled với phiên bản hard-label cùng kiến trúc. Đồng thời, các student còn được so sánh trực tiếp với teacher PhoBERT-base về chất lượng phân loại và tính khả thi triển khai. Cách so sánh này cho phép xác định liệu việc giảm mạnh quy mô mô hình có duy trì được một phần đáng kể năng lực phát hiện smishing hay không, thay vì chỉ xem distillation như một kỹ thuật nhằm tăng metric.

Nhóm thứ hai gồm chín pretrained language model dạng encoder. PhoBERT-base và PhoBERT-large đại diện cho các mô hình được tiền huấn luyện riêng cho tiếng Việt, đồng thời cho phép khảo sát ảnh hưởng của quy mô trong cùng một họ kiến trúc. Do PhoBERT sử dụng đầu vào đã được phân đoạn từ tiếng Việt, dữ liệu dành cho hai mô hình này được xử lý bằng bước tách từ trước khi đưa qua tokenizer tương ứng.

mBERT, DistilBERT multilingual, XLM-RoBERTa-base và XLM-RoBERTa-large đại diện cho các mô hình đa ngữ. mBERT cung cấp một baseline đa ngữ phổ biến; DistilBERT multilingual đại diện cho hướng giảm kích thước mô hình tiền huấn luyện; còn hai phiên bản XLM-RoBERTa cho phép đánh giá sự khác biệt giữa cấu hình base và large. Việc đưa các mô hình này vào benchmark giúp kiểm tra mức độ tri thức đa ngữ có thể chuyển giao sang bài toán smishing tiếng Việt.

VisoBERT và CafeBERT được lựa chọn vì quá trình tiền huấn luyện hướng đến văn bản tiếng Việt trên mạng xã hội hoặc các miền có ngôn ngữ phi chuẩn. Những nguồn văn bản này có nhiều điểm gần với SMS như viết tắt, thiếu dấu, lỗi chính tả và cách diễn đạt không trang trọng. ViCLSR bổ sung một mô hình biểu diễn tiếng Việt khác vào benchmark, từ đó mở rộng so sánh giữa các chiến lược tiền huấn luyện và miền dữ liệu nguồn. Với toàn bộ nhóm encoder, một classification head nhị phân được gắn lên biểu diễn đầu ra và các tham số được fine-tune trên cùng benchmark train split.

Nhóm cuối cùng gồm Gemma 3 1B, Gemma 2B, Qwen3 0.6B và Qwen2.5 0.5B. Các cấu hình này mở rộng benchmark từ encoder chuyên cho tác vụ hiểu văn bản sang các mô hình ngôn ngữ có khả năng sinh. Do quy mô tham số lớn hơn, bốn mô hình được thích nghi cho bài toán phân loại nhị phân bằng Low-Rank Adaptation (LoRA) thay vì cập nhật toàn bộ trọng số. LoRA giữ cố định phần lớn tham số của mô hình nền và chỉ tối ưu các ma trận hạng thấp được bổ sung vào một số lớp mục tiêu, qua đó giảm lượng tham số cần huấn luyện và yêu cầu bộ nhớ. Sau quá trình thích nghi trên cùng benchmark train split, các mô hình được đánh giá bằng cùng đầu ra xác suất trên dev và test. Sự xuất hiện của nhóm này cho phép kiểm tra liệu quy mô lớn hơn và năng lực biểu diễn tổng quát có chuyển thành lợi thế rõ ràng trên một tác vụ phân loại SMS ngắn hay không.

Việc chia mô hình thành ba nhóm không nhằm giả định trước nhóm nào vượt trội. Các mô hình character-level có lợi thế về kích thước và khả năng giữ tín hiệu ký tự; các encoder tiền huấn luyện có lợi thế về biểu diễn ngữ nghĩa; trong khi nhóm mô hình ngôn ngữ lớn có năng lực biểu diễn rộng hơn nhưng đòi hỏi nhiều tài nguyên hơn. Kết quả benchmark vì vậy được phân tích theo cả từng mô hình và từng nhóm kiến trúc, thay vì chỉ sắp xếp một bảng xếp hạng duy nhất.

> **GHI CHÚ BẢNG — Cần bảng tổng hợp 17 cấu hình benchmark**
>
> | Nhóm | Cấu hình | Biểu diễn đầu vào | Cách thích nghi/huấn luyện | Vai trò so sánh |
> |---|---|---|---|---|
> | Character-level | BiLSTM | Chuỗi ký tự | Hard-label | Baseline tuần tự gọn nhẹ |
> | Character-level | BiLSTM distilled từ PhoBERT-base | Chuỗi ký tự | Hard label + soft target | Đánh giá distillation |
> | Character-level | TextCNN | Chuỗi ký tự | Hard-label | Baseline pattern cục bộ |
> | Character-level | TextCNN distilled từ PhoBERT-base | Chuỗi ký tự | Hard label + soft target | Đánh giá distillation |
> | Encoder PLM | PhoBERT-base, PhoBERT-large | Subword sau tách từ | Fine-tuning | PLM đơn ngữ; so sánh base/large |
> | Encoder PLM | mBERT, DistilBERT multilingual | Subword | Fine-tuning | Baseline đa ngữ và mô hình rút gọn |
> | Encoder PLM | XLM-RoBERTa-base, XLM-RoBERTa-large | Subword | Fine-tuning | So sánh đa ngữ base/large |
> | Encoder PLM | VisoBERT, CafeBERT, ViCLSR | Tokenizer tương ứng | Fine-tuning | Mô hình tiếng Việt/noisy text |
> | LLM | Gemma 3 1B, Gemma 2B | Tokenizer tương ứng | Fine-tuning hiệu quả tham số bằng LoRA | LLM họ Gemma |
> | LLM | Qwen3 0.6B, Qwen2.5 0.5B | Tokenizer tương ứng | Fine-tuning hiệu quả tham số bằng LoRA | LLM họ Qwen |
>
> Bảng này chỉ mô tả thiết kế. Không đưa kết quả Macro-F1, F1 Label 1, Recall Label 1 hoặc PR-AUC vào Mục 4.3.

> **GHI CHÚ HÌNH — Không bắt buộc tạo sơ đồ kiến trúc riêng**
>
> Không nên vẽ một sơ đồ riêng cho cả 17 mô hình vì hình sẽ dày đặc và khó đọc. Nếu cần minh họa, chỉ nên dùng một hình ba tầng đơn giản: Character-level → Encoder PLM → LLM, kèm hai mũi tên so sánh xuyên nhóm là “chất lượng dự đoán” và “chi phí triển khai”. Cấu trúc chi tiết của BiLSTM/TextCNN có thể trình bày bằng văn bản hoặc dẫn lại Chương 2 nếu đã mô tả ở phần cơ sở lý thuyết.

> **GHI CHÚ KIỂM TRA trước khi kết thúc Mục 4.3**
>
> - Tên bốn cấu hình LLM được chốt là Gemma 3 1B, Gemma 2B, Qwen3 0.6B và Qwen2.5 0.5B.
> - Phương pháp thích nghi của bốn LLM được chốt là LoRA; rank, alpha, dropout và các target module cụ thể sẽ được trình bày tại Mục 4.4.
> - Đồng bộ tên `DistilBERT multilingual` trong toàn bộ bảng, hình và artefact.
> - Không nhầm DistilBERT multilingual là mô hình student được distill trực tiếp trong nghiên cứu; đây là một pretrained model độc lập. Hai cấu hình distillation của nghiên cứu là BiLSTM và TextCNN distilled từ PhoBERT-base.
> - Phần hyperparameter, tokenizer, classification head và hàm loss chi tiết được trình bày ở Mục 4.4, tránh lặp lại tại đây.

## 4.4. Thiết lập huấn luyện

Các cấu hình trong benchmark được huấn luyện trên cùng bộ train và sử dụng tập dev để theo dõi quá trình học, lựa chọn checkpoint và dừng sớm. Seed được cố định bằng 42 nhằm giữ nhất quán việc khởi tạo và thứ tự xử lý dữ liệu giữa các lần chạy. Sau khi checkpoint tốt nhất được chọn, mô hình sinh xác suất dự đoán cho cả dev và test với ngưỡng phân loại mặc định bằng 0,5. Tập test không tham gia vào quá trình điều chỉnh hyperparameter, lựa chọn checkpoint hoặc thay đổi threshold.

Đối với nhóm character-level, từ vựng ký tự được xây dựng chỉ từ nội dung của tập train. Mỗi tin nhắn được chuyển về chữ thường, ánh xạ thành chuỗi chỉ số có độ dài tối đa 256 ký tự và được padding nếu ngắn hơn. Các ký tự không xuất hiện trong từ vựng được ánh xạ vào token `<unk>`, trong khi token `<pad>` được dùng để bổ sung độ dài. Cách xử lý này không thực hiện tách từ và giữ lại trực tiếp hình thức bề mặt của văn bản.

BiLSTM và TextCNN cùng sử dụng embedding ký tự có 64 chiều và dropout bằng 0,3. BiLSTM có hidden dimension bằng 64 cho mỗi chiều; biểu diễn cuối được tạo bằng cách nối mean pooling và max pooling trên chuỗi đầu ra hai chiều. TextCNN sử dụng 96 bộ lọc cho mỗi kích thước kernel 3, 4 và 5, sau đó áp dụng max pooling và nối các đặc trưng trước lớp phân loại. Cả hai kiến trúc được huấn luyện với batch size 128, learning rate \(2 \times 10^{-3}\), weight decay \(10^{-4}\) và tối đa 12 epoch. AdamW được sử dụng làm bộ tối ưu và gradient norm được giới hạn ở mức 1,0. Quá trình huấn luyện dừng sớm nếu Macro-F1 trên dev không cải thiện trong ba epoch liên tiếp; checkpoint có dev Macro-F1 cao nhất được giữ lại.

Do Label 0 và Label 1 có tỷ lệ khác nhau trong tập train, hàm binary cross-entropy của nhóm character-level sử dụng `pos_weight` được tính từ số mẫu âm và dương trong chính tập train. Trọng số này chỉ phụ thuộc vào phân phối dữ liệu huấn luyện và không sử dụng thông tin từ dev hoặc test.

Hai cấu hình distilled giữ nguyên kiến trúc và hyperparameter của student hard-label tương ứng. Khác biệt nằm ở tín hiệu giám sát: ngoài binary cross-entropy với nhãn gốc, student còn học từ xác suất mềm do PhoBERT-base sinh ra. Logit của teacher được làm mềm với temperature bằng 2. Hàm mất mát kết hợp sử dụng hệ số \(\alpha = 0{,}8\) cho hard-label loss và \(1-\alpha = 0{,}2\) cho soft-target loss.

Mức ảnh hưởng của soft target còn phụ thuộc vào độ tin cậy của teacher. Khi teacher dự đoán đúng với confidence từ 0,8 trở lên, soft target có trọng số 1,0; khi teacher dự đoán đúng nhưng confidence thấp hơn 0,8, trọng số là 0,7; các trường hợp teacher dự đoán sai nhận trọng số ban đầu bằng 0,3. Riêng khi teacher bỏ sót mẫu Label 1, tức dự đoán false negative, ảnh hưởng của soft target được đưa về 0. Thiết kế này nhằm tránh truyền sang student những lỗi có rủi ro cao nhất trong bài toán phát hiện smishing.

> **GHI CHÚ BẢNG — Cần bảng cấu hình nhóm character-level**
>
> | Thành phần | BiLSTM | TextCNN |
> |---|---:|---:|
> | Độ dài tối đa | 256 ký tự | 256 ký tự |
> | Embedding dimension | 64 | 64 |
> | Hidden dimension | 64 mỗi chiều | — |
> | Số filter | — | 96/kernel |
> | Kernel size | — | 3, 4, 5 |
> | Dropout | 0,3 | 0,3 |
> | Batch size | 128 | 128 |
> | Epoch tối đa | 12 | 12 |
> | Learning rate | \(2 \times 10^{-3}\) | \(2 \times 10^{-3}\) |
> | Weight decay | \(10^{-4}\) | \(10^{-4}\) |
> | Early stopping | Patience = 3 | Patience = 3 |
> | Tiêu chí chọn checkpoint | Dev Macro-F1 | Dev Macro-F1 |
>
> Có thể đặt thông tin distillation ngay dưới bảng: teacher = PhoBERT-base, temperature = 2, \(\alpha = 0{,}8\), false-negative distillation weight = 0.

Với chín encoder pretrained, tokenizer đi kèm từng checkpoint được sử dụng để mã hóa văn bản thành chuỗi subword. Riêng PhoBERT-base và PhoBERT-large yêu cầu bước phân đoạn từ tiếng Việt bằng ViTokenizer trước khi tokenization. Độ dài đầu vào tối đa được đặt bằng 128 token; các chuỗi dài hơn bị truncate và các chuỗi ngắn hơn được padding tới cùng độ dài. Một classification head với hai nhãn được fine-tune cùng mô hình nền.

Nhóm encoder được huấn luyện tối đa ba epoch bằng AdamW với learning rate \(2 \times 10^{-5}\), weight decay 0,01 và warmup ratio 0,1. Theo cấu hình được lưu từ các lần chạy benchmark, mixed-precision FP16 được sử dụng trong quá trình huấn luyện. Mô hình được đánh giá sau mỗi epoch, lưu tối đa hai checkpoint và dừng sớm khi Macro-F1 trên dev không cải thiện sau hai lần đánh giá liên tiếp. Checkpoint có dev Macro-F1 cao nhất được nạp lại để sinh kết quả cuối.

Phần lớn encoder sử dụng train batch size 16 và evaluation batch size 32. Do yêu cầu bộ nhớ lớn hơn, XLM-RoBERTa-large và ViCLSR sử dụng train batch size 8, evaluation batch size 16 và gradient accumulation trong hai bước. Nhờ đó, effective train batch size của hai mô hình vẫn bằng 16, tương đương các cấu hình encoder còn lại.

> **GHI CHÚ BẢNG — Cần bảng cấu hình fine-tuning encoder**
>
> | Thành phần | Cấu hình chung | XLM-RoBERTa-large và ViCLSR |
> |---|---:|---:|
> | Max length | 128 token | 128 token |
> | Epoch tối đa | 3 | 3 |
> | Train batch size | 16 | 8 |
> | Evaluation batch size | 32 | 16 |
> | Gradient accumulation | 1 | 2 |
> | Effective train batch size | 16 | 16 |
> | Learning rate | \(2 \times 10^{-5}\) | \(2 \times 10^{-5}\) |
> | Weight decay | 0,01 | 0,01 |
> | Warmup ratio | 0,1 | 0,1 |
> | Mixed precision | FP16 | FP16 |
> | Early stopping | Patience = 2 | Patience = 2 |
> | Tiêu chí chọn checkpoint | Dev Macro-F1 | Dev Macro-F1 |

Bốn mô hình ngôn ngữ lớn được fine-tune theo hướng hiệu quả tham số bằng LoRA. Trong thiết lập này, trọng số của mô hình nền được giữ cố định và chỉ các adapter hạng thấp được cập nhật trong quá trình huấn luyện. Cách tiếp cận này giảm đáng kể số tham số cần tối ưu và mức sử dụng bộ nhớ so với full fine-tuning, đồng thời vẫn cho phép mô hình thích nghi với nhãn ham và smishing.

Để bảo đảm khả năng so sánh trong nhóm LLM, Gemma 3 1B, Gemma 2B, Qwen3 0.6B và Qwen2.5 0.5B sử dụng cùng một cấu hình LoRA. Rank \(r\) được đặt bằng 8, LoRA alpha bằng 16 và dropout bằng 0,1. Adapter được áp dụng lên các phép chiếu `q_proj`, `k_proj`, `v_proj`, `o_proj` trong cơ chế attention và các lớp `gate_proj`, `up_proj`, `down_proj` trong khối feed-forward. Độ dài đầu vào tối đa là 512 token. Các mô hình được huấn luyện trong ba epoch với batch size 4, gradient accumulation 4 bước và learning rate \(2 \times 10^{-4}\). Nhờ gradient accumulation, effective batch size đạt 16 mẫu. Quá trình huấn luyện sử dụng độ chính xác BF16. Cả bốn LLM dùng cùng benchmark train split, lựa chọn cấu hình dựa trên dev và sinh xác suất dự đoán cho dev/test để tính bốn độ đo chung.

> **GHI CHÚ BẢNG — Cần bảng cấu hình LoRA của nhóm LLM**
>
> | Thành phần | Giá trị chung |
> |---|---|
> | Mô hình áp dụng | Gemma 3 1B, Gemma 2B, Qwen3 0.6B, Qwen2.5 0.5B |
> | LoRA rank \(r\) | 8 |
> | LoRA alpha | 16 |
> | LoRA dropout | 0,1 |
> | Target modules | `q_proj`, `v_proj`, `k_proj`, `o_proj`, `gate_proj`, `up_proj`, `down_proj` |
> | Max length | 512 |
> | Batch size | 4 |
> | Gradient accumulation | 4 |
> | Effective batch size | 16 |
> | Learning rate | \(2 \times 10^{-4}\) |
> | Epoch | 3 |
> | Precision | BF16 |

Để duy trì tính nhất quán của benchmark, bốn độ đo Macro-F1, F1 Label 1, Recall Label 1 và PR-AUC được tính từ xác suất dự đoán của mọi cấu hình trên cùng dev và test. Ngưỡng 0,5 được giữ cố định cho các metric phụ thuộc threshold; không tinh chỉnh threshold riêng cho từng mô hình trên test. Macro-F1 trên dev là tiêu chí chính để lựa chọn checkpoint, trong khi các độ đo còn lại được sử dụng để mô tả đầy đủ hơn sự cân bằng giữa khả năng phát hiện smishing và sai số phân loại.

Ngoài chất lượng dự đoán, teacher PhoBERT-base và hai student distilled được đánh giá lại về khả năng triển khai trên cùng benchmark split và cùng môi trường CPU. Độ trễ được đo với batch size 1 sau ba lượt warm-up và 20 lần lặp. Thông lượng và peak RAM được đo trên một lượt suy luận với batch size 128. Toàn bộ phép đo sử dụng một luồng CPU. So sánh còn bao gồm số lượng tham số và kích thước checkpoint. PhoBERT-base sử dụng cùng bước phân đoạn từ bằng ViTokenizer và giới hạn 128 token như trong benchmark mô hình; hai student sử dụng giới hạn 256 ký tự từ checkpoint tương ứng.

> **GHI CHÚ BẢNG — Cần bảng giao thức đo tính khả thi triển khai**
>
> | Thành phần | Thiết lập |
> |---|---|
> | Các mô hình | PhoBERT-base, BiLSTM distilled, TextCNN distilled |
> | Dữ liệu | Cùng benchmark split |
> | Thiết bị | Cùng CPU, 1 thread |
> | Latency | Batch size 1, 3 warm-up, 20 lần lặp |
> | Throughput | Một lượt suy luận, batch size 128 |
> | Tài nguyên | Số tham số, kích thước checkpoint, peak RAM |
> | Chất lượng đi kèm | F1 Label 1 trên cùng split |
>
> Tên CPU, tổng RAM và phiên bản thư viện sẽ được bổ sung sau khi hoàn tất thông tin môi trường.

> **GHI CHÚ KIỂM TRA trước khi kết thúc Mục 4.4**
>
> - Cấu hình LoRA đã được chốt và dùng thống nhất cho cả bốn LLM.
> - Xác nhận phần cứng và phiên bản thư viện của các nhóm mô hình nếu khoa yêu cầu khả năng tái lập chi tiết.
> - PhoBERT-large đã được xác nhận dùng train/evaluation batch size 16/32 và gradient accumulation 1. Chỉ XLM-RoBERTa-large và ViCLSR dùng cấu hình 8/16 với gradient accumulation 2.
> - Mixed-precision FP16 đã được xác nhận từ cả file config và các lệnh chạy riêng từng mô hình trên Kaggle có truyền tham số `--fp16`. Script PowerShell cục bộ không được xem là lệnh tái lập chính của các lần chạy này.
> - Deployment benchmark đã được chạy trên cả dev và test của benchmark split; metric tái tính khớp với kết quả benchmark mô hình.
> - Không đưa thời gian huấn luyện hoặc kết quả metric vào Mục 4.4; các số liệu so sánh thuộc Chương 5.

## 4.5. Các độ đo đánh giá

Tập dev và test của benchmark đều có 498 mẫu Label 0 nhưng chỉ có 37 mẫu Label 1. Với phân phối này, một mô hình dự đoán phần lớn tin nhắn là hợp lệ vẫn có thể đạt Accuracy cao dù bỏ sót nhiều tin nhắn smishing. Vì vậy, Accuracy không được sử dụng làm căn cứ chính để xếp hạng hoặc lựa chọn mô hình. Benchmark tập trung vào bốn độ đo gồm Macro-F1, F1 Label 1, Recall Label 1 và PR-AUC. Các độ đo được tính độc lập trên dev và test từ cùng nhãn dự đoán và xác suất của Label 1.

Để trình bày các độ đo, Label 1 được xem là lớp dương, tương ứng với tin nhắn smishing; Label 0 là lớp âm, tương ứng với tin nhắn hợp lệ. Bốn thành phần của ma trận nhầm lẫn được định nghĩa như sau: true positive (TP) là tin nhắn smishing được phát hiện đúng; false negative (FN) là tin nhắn smishing bị dự đoán thành hợp lệ; true negative (TN) là tin nhắn hợp lệ được phân loại đúng; và false positive (FP) là tin nhắn hợp lệ bị cảnh báo nhầm thành smishing.

Precision của Label 1 phản ánh trong số các tin nhắn bị mô hình cảnh báo là smishing, có bao nhiêu mẫu thực sự là smishing:

\[
\mathrm{Precision}_{1}=\frac{TP}{TP+FP}.
\]

Recall Label 1 phản ánh trong số toàn bộ tin nhắn smishing, mô hình phát hiện được bao nhiêu mẫu:

\[
\mathrm{Recall}_{1}=\frac{TP}{TP+FN}.
\]

Recall Label 1 là một trong bốn độ đo chính vì false negative có thể khiến người dùng tiếp xúc với nội dung lừa đảo mà không nhận được cảnh báo. Giá trị Recall cao cho thấy mô hình bỏ sót ít smishing hơn. Tuy nhiên, Recall không thể được diễn giải riêng lẻ: một mô hình có thể tăng Recall bằng cách dự đoán Label 1 rộng hơn, từ đó làm tăng false positive.

F1 Label 1 là trung bình điều hòa giữa Precision và Recall của lớp smishing:

\[
\mathrm{F1}_{1}
=2\times\frac{\mathrm{Precision}_{1}\times\mathrm{Recall}_{1}}
{\mathrm{Precision}_{1}+\mathrm{Recall}_{1}}.
\]

Độ đo này giúp đánh giá sự cân bằng giữa phát hiện đúng smishing và hạn chế cảnh báo sai. Trong bối cảnh Label 1 chiếm tỷ lệ nhỏ ở dev và test, F1 Label 1 cung cấp thông tin trực tiếp hơn Accuracy về khả năng xử lý lớp mục tiêu. Dù Precision Label 1 không nằm trong bốn cột chính của bảng benchmark, giá trị này vẫn được lưu và sử dụng cùng FP để giải thích nguyên nhân thay đổi của F1 Label 1.

Macro-F1 được tính bằng trung bình không trọng số giữa F1 của Label 0 và F1 của Label 1:

\[
\mathrm{Macro\text{-}F1}
=\frac{\mathrm{F1}_{0}+\mathrm{F1}_{1}}{2}.
\]

Do hai lớp đóng góp ngang nhau, Macro-F1 hạn chế việc lớp Label 0 có số lượng lớn chi phối kết quả tổng thể. Đây là độ đo chính dùng để lựa chọn checkpoint trên dev và là tiêu chí tổng quát khi so sánh các cấu hình. Tuy nhiên, Macro-F1 vẫn được đọc cùng F1 và Recall Label 1 để tránh trường hợp hai mô hình có kết quả tổng thể gần nhau nhưng khác biệt đáng kể về khả năng phát hiện smishing.

Ba độ đo trên phụ thuộc vào ngưỡng chuyển xác suất thành nhãn, được cố định ở mức 0,5 trong benchmark. Để bổ sung góc nhìn không phụ thuộc vào một ngưỡng duy nhất, nghiên cứu sử dụng PR-AUC dựa trên xác suất dự đoán của Label 1. Precision–Recall curve mô tả sự thay đổi giữa Precision và Recall khi ngưỡng phân loại được dịch chuyển. Trong phần triển khai, PR-AUC được tính bằng `average_precision_score`, tức Average Precision tổng hợp Precision tại các mức Recall khác nhau. Độ đo này phù hợp với bài toán có lớp dương hiếm vì tập trung trực tiếp vào chất lượng xếp hạng các mẫu smishing thay vì bị chi phối bởi số lượng true negative lớn.

PR-AUC cao cho thấy mô hình có khả năng đưa các mẫu smishing lên vùng xác suất cao một cách ổn định trên nhiều ngưỡng. Tuy nhiên, PR-AUC không thay thế các metric tại ngưỡng vận hành: một mô hình có PR-AUC tốt vẫn có thể tạo ra số FP hoặc FN không phù hợp tại ngưỡng 0,5. Vì vậy, PR-AUC được sử dụng cùng Macro-F1, F1 Label 1 và Recall Label 1 thay vì làm tiêu chí duy nhất.

> **GHI CHÚ BẢNG — Cần bảng tóm tắt bốn độ đo chính**
>
> | Độ đo | Thành phần phản ánh | Vai trò trong nghiên cứu |
> |---|---|---|
> | Macro-F1 | Cân bằng F1 giữa Label 0 và Label 1 | Độ đo tổng quát và tiêu chí chọn checkpoint trên dev |
> | F1 Label 1 | Cân bằng Precision–Recall của smishing | Đánh giá trực tiếp chất lượng phân loại lớp mục tiêu |
> | Recall Label 1 | Tỷ lệ smishing được phát hiện | Theo dõi nguy cơ bỏ sót smishing |
> | PR-AUC | Chất lượng Precision–Recall trên nhiều ngưỡng | Đánh giá khả năng xếp hạng trong dữ liệu mất cân bằng |
>
> Bảng chỉ mô tả ý nghĩa và vai trò, không đưa kết quả của từng mô hình vào Chương 4.

Bên cạnh bốn độ đo chính, ma trận nhầm lẫn và các giá trị TN, FP, FN, TP được lưu cho từng mô hình trên mỗi split. Các số đếm này không dùng để tạo thêm một bảng xếp hạng, mà hỗ trợ diễn giải kết quả và phân tích lỗi ở Chương 5. Đặc biệt, FN cho biết số smishing bị bỏ sót, còn FP phản ánh số tin nhắn hợp lệ bị cảnh báo sai. Precision Label 1, Accuracy, Weighted-F1 và ROC-AUC cũng được pipeline tính và lưu như các chỉ số bổ trợ, nhưng không được dùng làm bốn độ đo benchmark chính.

Do mỗi tập dev và test chỉ có 37 mẫu Label 1, một vài dự đoán thay đổi cũng có thể tạo ra chênh lệch đáng kể về F1 hoặc Recall Label 1. Chẳng hạn, một mẫu smishing tương ứng khoảng 2,70 điểm phần trăm Recall. Vì vậy, khi phân tích kết quả, nghiên cứu xem xét đồng thời giá trị metric và số lượng FP/FN, tránh diễn giải chênh lệch nhỏ như bằng chứng chắc chắn về ưu thế của một kiến trúc.

> **GHI CHÚ HÌNH — Không cần biểu đồ metric trong Mục 4.5**
>
> Các đường Precision–Recall, biểu đồ so sánh metric và confusion matrix đều là kết quả thực nghiệm, nên chỉ xuất hiện tại Chương 5 nếu phục vụ trực tiếp cho một câu hỏi nghiên cứu. Mục 4.5 chỉ cần bảng tóm tắt độ đo và các công thức.

> **GHI CHÚ KIỂM TRA trước khi kết thúc Mục 4.5**
>
> - Dùng thống nhất thuật ngữ `PR-AUC` trong báo cáo và ghi rõ cách tính bằng Average Precision; không dùng xen kẽ `AUPRC` nếu chưa định nghĩa hai tên là tương đương trong nghiên cứu.
> - Bảng benchmark chính chỉ gồm Macro-F1, F1 Label 1, Recall Label 1 và PR-AUC như đã chốt.
> - Precision Label 1 và FP/FN được dùng trong phần giải thích, không cần thêm vào bảng benchmark chính nếu bảng trở nên quá rộng.
> - Không dùng Accuracy để tuyên bố mô hình tốt nhất.
> - Khi kết luận từ chênh lệch metric, luôn kiểm tra số mẫu Label 1 và số FP/FN tương ứng.

## 4.6. Phương pháp phân tích kết quả

Bảng benchmark tổng thể cho biết mô hình nào đạt kết quả cao hơn, nhưng chưa giải thích mô hình hoạt động tốt hoặc thất bại trong những điều kiện nào. Vì vậy, sau bước đánh giá chung, nghiên cứu sử dụng các file dự đoán ở cấp mẫu trên tập dev để phân tích kết quả theo nhiều lát cắt dữ liệu và theo từng loại lỗi. Mỗi bản ghi dự đoán giữ lại nội dung tin nhắn, nhãn thật, nhãn dự đoán, xác suất Label 1, confidence, loại lỗi và các metadata gồm `data_origin`, `category`, `sender_type`, `has_url`, `has_phone_number` và `obfuscation_level`. Cấu trúc này cho phép nối kết trực tiếp kết quả định lượng với đặc điểm của từng mẫu.

Phân tích được thực hiện chủ yếu trên dev, bởi đây là tập được phép sử dụng trong quá trình phát triển và diễn giải mô hình. Test chỉ được dùng để xác nhận kết quả tổng quát ở mức cuối cùng; không sử dụng các lỗi trên test để thay đổi mô hình, ngưỡng hoặc lựa chọn lát cắt có lợi. Đối với mọi lát cắt, nghiên cứu báo cáo số lượng mẫu trước khi trình bày metric. Những nhóm có quá ít mẫu, đặc biệt quá ít Label 1, chỉ được dùng như quan sát mô tả và không làm cơ sở cho kết luận tổng quát.

Góc phân tích đầu tiên là độ dài tin nhắn, được tính bằng số ký tự của nội dung gốc. Các mẫu ban đầu được chia thành bốn khoảng: không quá 80 ký tự, từ 81 đến 160 ký tự, từ 161 đến 240 ký tự và trên 240 ký tự. Các khoảng này lần lượt đại diện cho tin nhắn ngắn, trung bình, dài và rất dài. Cùng một ranh giới được áp dụng cho mọi mô hình để bảo đảm khả năng so sánh. Trên dev hiện tại, nhóm không quá 80 ký tự chỉ chứa hai mẫu Label 1; vì vậy, khi tính F1 hoặc Recall Label 1, nhóm này cần được gộp với khoảng kế tiếp hoặc chỉ được mô tả về số lỗi. Nguyên tắc chung là không diễn giải metric lớp smishing cho một lát cắt có dưới năm mẫu Label 1.

Phân tích độ dài nhằm trả lời ba vấn đề. Thứ nhất, tin nhắn quá ngắn có thể thiếu ngữ cảnh để mô hình nhận biết ý đồ lừa đảo. Thứ hai, tin nhắn dài có thể chứa nhiều tín hiệu gây nhiễu hoặc bị truncate do giới hạn đầu vào khác nhau giữa các nhóm mô hình. Thứ ba, sự khác biệt giữa mô hình character-level, encoder PLM và LLM cho phép đánh giá khả năng duy trì hiệu năng của từng nhóm khi độ dài đầu vào thay đổi. Với mỗi khoảng đủ dữ liệu, các chỉ số được ưu tiên gồm số mẫu, F1 Label 1, Recall Label 1, FP và FN; Macro-F1 chỉ được dùng khi lát cắt có cả hai nhãn.

> **GHI CHÚ BẢNG — Cần bảng phân phối dev theo độ dài trước khi báo cáo metric**
>
> | Độ dài | Label 0 | Label 1 | Tổng | Cách sử dụng |
> |---|---:|---:|---:|---|
> | ≤ 80 ký tự | 138 | 2 | 140 | Chỉ mô tả hoặc gộp khi tính metric Label 1 |
> | 81–160 ký tự | 129 | 17 | 146 | Phân tích đầy đủ |
> | 161–240 ký tự | 74 | 8 | 82 | Phân tích với lưu ý cỡ mẫu |
> | > 240 ký tự | 157 | 10 | 167 | Phân tích với lưu ý cỡ mẫu |
>
> Bảng này mô tả phương pháp và quy mô lát cắt. Bảng metric theo từng mô hình thuộc Chương 5.

Từ độ dài, nghiên cứu dự kiến chuyển sang phân tích mức độ phi chuẩn của văn bản. Khái niệm này cần được phân biệt với `obfuscation_level` hiện tại. Thuộc tính `obfuscation_level` mô tả mức độ biến đổi được xem là có chủ đích trong các mẫu smishing, trong khi các hiện tượng quan sát được như teencode, viết tắt, thiếu dấu hoặc lỗi chính tả tự nhiên có thể xuất hiện ở cả Label 0 và Label 1 mà không hàm ý ý định che giấu. Do Label 0 hiện được gán `NONE`, thuộc tính này tách biệt mạnh theo nhãn và chưa phù hợp để dùng như thước đo chung về độ phi chuẩn.

> **PLACEHOLDER — PHÂN TÍCH MỨC ĐỘ PHI CHUẨN CỦA VĂN BẢN**
>
> Phần này sẽ được hoàn thiện sau khi xây dựng một thuộc tính áp dụng độc lập với nhãn, tạm gọi là `text_noise_level`. Thuộc tính mới cần mô tả hiện tượng bề mặt quan sát được thay vì suy đoán ý định của người viết. Các hiện tượng dự kiến gồm teencode, viết tắt, thiếu dấu, lỗi chính tả, leetspeak, chèn ký tự đặc biệt, phân tách bất thường và biến đổi URL.
>
> Khi hoàn thiện, phần phân tích cần:
>
> - Định nghĩa tiêu chí gán mức phi chuẩn có thể tái lập.
> - Áp dụng cùng tiêu chí cho cả Label 0 và Label 1.
> - Báo cáo phân phối theo nhãn và `data_origin`.
> - Phân tích hiệu năng mô hình theo từng mức, luôn kèm số lượng mẫu.
> - Đối chiếu character-level, encoder PLM và LLM về độ bền vững trước văn bản phi chuẩn.
>
> Không sử dụng `obfuscation_level` hiện tại để thay thế cho `text_noise_level`.

Trong trường hợp vẫn giữ phân tích `obfuscation_level`, phạm vi diễn giải phải được giới hạn trong riêng Label 1. Trên dev có 15 mẫu Level 0, 8 mẫu Level 1, 9 mẫu Level 2, 2 mẫu Level 3 và 3 mẫu Level 4. Có thể gộp Level 1–2 và Level 3–4 để mô tả số smishing được phát hiện hoặc bỏ sót theo mức che giấu đã gán. Tuy nhiên, kết quả này chỉ phản ánh các mức che giấu được định nghĩa trong lớp smishing, không đại diện cho khả năng xử lý mọi dạng văn bản phi chuẩn và không được dùng để so sánh trực tiếp hai nhãn.

Sau hai thuộc tính bề mặt, nghiên cứu mở rộng sang nguồn dữ liệu và metadata. Với `data_origin`, các kết quả được tách thành `real`, `external_real` và `external_curated` để phát hiện domain shift. Vì hai nguồn external chỉ chứa Label 0, các lát cắt này được đánh giá chủ yếu bằng số FP, false-positive rate và độ tự tin của các dự đoán sai; không tính F1 Label 1 cho nhóm không có mẫu dương. Với nguồn `real`, có thể tính đầy đủ các metric nhị phân do chứa cả hai nhãn.

Các thuộc tính `has_url`, `has_phone_number` và `sender_type` được sử dụng để xem xét mô hình có phụ thuộc quá mức vào tín hiệu bề mặt hay không. Ví dụ, URL có thể hỗ trợ nhận biết smishing nhưng cũng xuất hiện trong tin nhắn hợp lệ; do đó cần phân tích đồng thời Recall trên Label 1 và FP trên Label 0. Tương tự, `sender_type` giúp kiểm tra các mẫu từ brandname hoặc số cá nhân có tạo ra mức độ khó khác nhau hay không. `category` được dùng để nhóm lỗi theo ngữ cảnh như viễn thông, ngân hàng, OTP, tuyển dụng hoặc dịch vụ công. Tuy nhiên, các category quá ít mẫu không được báo cáo metric riêng; chúng được gộp vào nhóm khác hoặc chỉ dùng làm ví dụ định tính.

> **GHI CHÚ BẢNG — Cần bảng quy tắc đánh giá theo từng lát cắt**
>
> | Lát cắt | Phạm vi | Chỉ số ưu tiên | Lưu ý |
> |---|---|---|---|
> | Độ dài | Toàn bộ dev | Macro-F1, F1/Recall L1, FP, FN | Gộp nhóm nếu Label 1 < 5 |
> | Mức độ phi chuẩn | Toàn bộ dev | Metric theo lát cắt và số lỗi | Chờ triển khai `text_noise_level` độc lập với nhãn |
> | Obfuscation hiện tại | Chỉ Label 1 | Recall và số FN | Phân tích phụ; không đại diện cho toàn bộ văn bản phi chuẩn |
> | Data origin | `real`, `external_*` | Metric đầy đủ trên real; FP/FPR trên external | External chỉ chứa Label 0 |
> | URL, số điện thoại | Theo nhãn | Recall L1 và FP | Kiểm tra phụ thuộc tín hiệu bề mặt |
> | Sender type | Theo nhãn và loại người gửi | Recall L1, FP, FN | Một số nhóm có thể không có Label 1 |
> | Category | Các nhóm đủ mẫu | F1/Recall L1 hoặc số lỗi | Không kết luận từ category quá nhỏ |

Phân tích theo lát cắt được nối tiếp bằng phân tích lỗi ở cấp mẫu. Trước hết, số FP và FN của các mô hình được tổng hợp để xác định mô hình thiên về bỏ sót smishing hay cảnh báo quá mức. Sau đó, các lỗi được gán vào một taxonomy nguyên nhân dựa trên nội dung và metadata. Các nhóm dự kiến gồm smishing có bề mặt giống OTP hoặc brandname hợp lệ; smishing không có URL hoặc lời kêu gọi hành động rõ; smishing có obfuscation/leet; tin hợp lệ chứa URL, hotline hoặc ngôn ngữ cảnh báo; tin bảo mật hợp lệ có từ vựng gần với lừa đảo; văn bản ngoài miền SMS; và các trường hợp thiếu ngữ cảnh hoặc nhãn có thể gây tranh luận.

Việc gán taxonomy bằng quy tắc chỉ được sử dụng để sàng lọc và thống kê sơ bộ. Các mẫu đưa vào báo cáo phải được rà thủ công để xác nhận nhóm lỗi. Nghiên cứu ưu tiên những lỗi xuất hiện ở nhiều mô hình, lỗi có confidence cao và các trường hợp thể hiện sự khác biệt giữa nhóm kiến trúc. Mỗi ví dụ định tính cần ghi nội dung rút gọn, nhãn thật, dự đoán, xác suất Label 1, loại lỗi và nhận xét; ví dụ chỉ có vai trò minh họa cho xu hướng đã được thống kê, không thay thế bằng chứng định lượng.

Cuối cùng, tập lỗi được so sánh giữa các mô hình đại diện thay vì trình bày confusion matrix của cả 17 cấu hình. Nhóm so sánh dự kiến gồm mô hình có dev Macro-F1 cao nhất, mô hình có Recall Label 1 cao nhất nếu khác mô hình đứng đầu, một encoder baseline, một mô hình character-level và một student distilled có ý nghĩa. Phân tích xem xét các mẫu mọi mô hình đều sai, mẫu chỉ một nhóm kiến trúc dự đoán đúng và sự giao nhau giữa FP/FN. Cách chọn mô hình đại diện phải dựa trên dev và được xác định trước khi đọc kết quả test.

> **GHI CHÚ HÌNH/BẢNG CHO CHƯƠNG 5**
>
> - Nên dùng heatmap hoặc grouped bar chart cho metric theo độ dài và obfuscation.
> - Có thể dùng bảng FP/FN theo `data_origin` thay vì nhiều confusion matrix.
> - Nếu so sánh tập lỗi của từ ba mô hình trở lên, ưu tiên UpSet plot; không dùng Venn diagram quá nhiều tập.
> - Chỉ dùng 5–8 ví dụ lỗi tiêu biểu trong bảng định tính.
> - Mọi biểu đồ lát cắt phải ghi số mẫu của nhóm hoặc đặt bảng phân phối ngay trước đó.

> **GHI CHÚ KIỂM TRA trước khi kết thúc Mục 4.6**
>
> - Xây dựng script phân tích dùng chung các file `*_predictions_dev.csv` để mọi mô hình được áp dụng cùng quy tắc.
> - Chuẩn hóa tên cột `has_url`/`has_URL` trước khi tổng hợp.
> - Không tính F1 hoặc PR-AUC cho lát cắt chỉ có một nhãn.
> - Chốt danh sách mô hình đại diện dựa trên dev trước khi phân tích test.
> - Các nhóm dưới năm mẫu Label 1 chỉ được mô tả, không dùng để khẳng định ưu thế mô hình.
> - Giữ placeholder `text_noise_level` cho đến khi hoàn thành định nghĩa, gán nhãn và kiểm tra phân phối.

## 4.7. Thí nghiệm bổ sung về dữ liệu tạo sinh

Benchmark 17 cấu hình đánh giá hiệu năng của nhiều họ mô hình trên bộ dữ liệu huấn luyện tổng hợp từ các nguồn đã mô tả. Tuy nhiên, benchmark này không tự tách riêng đóng góp của dữ liệu thật, dữ liệu tạo sinh Label 1 và các nguồn Label 0. Vì vậy, một chuỗi thí nghiệm bổ sung được thực hiện với PhoBERT-base nhằm trả lời RQ4: dữ liệu tạo sinh có thể thay thế dữ liệu thật hay chỉ phù hợp làm augmentation, và việc mở rộng miền Label 0 ảnh hưởng như thế nào đến false positive.

Các thí nghiệm bổ sung sử dụng một giao thức dữ liệu riêng vì mục tiêu của chúng khác với benchmark 17 cấu hình. Trong benchmark chính, thành phần dữ liệu huấn luyện được giữ cố định để sự khác biệt về kết quả chủ yếu phản ánh năng lực của từng mô hình. Ngược lại, RQ4 cần xác định đóng góp của từng nguồn dữ liệu; vì vậy, kiến trúc mô hình và miền đánh giá phải được giữ ổn định, còn thành phần tập huấn luyện là biến được chủ động thay đổi. Nếu sử dụng trực tiếp benchmark train đã kết hợp đồng thời dữ liệu `real`, `synthetic`, `paraphrased`, `synthetic_hard_positive` và các nguồn external, tác động riêng của từng nguồn sẽ bị trộn lẫn và không thể xác định cải thiện đến từ dữ liệu thật, synthetic Label 1 hay việc mở rộng Label 0.

Để tạo một mốc đối chứng ổn định, dữ liệu `real` được chia theo stratified split thành Real Train, Real Validation và Real Test với kích thước lần lượt 1.796, 385 và 386 mẫu. Real Validation và Real Test giữ nguyên giữa các thiết lập chính, trong khi dữ liệu đưa vào train được thay đổi có kiểm soát theo câu hỏi của từng thí nghiệm. Cách thiết kế này cho phép so sánh real-only với synthetic-only trong TSTR, sau đó lần lượt bổ sung synthetic Label 1 và các nguồn Label 0 mà không làm thay đổi miền đánh giá. Real Test được khóa để kết quả phản ánh khả năng chuyển giao sang dữ liệu thật thay vì mức độ phù hợp với một tập đánh giá chứa dữ liệu tạo sinh.

Mỗi biến thể được chạy với ba seed 42, 123 và 2025; kết quả được tổng hợp bằng trung bình và độ lệch chuẩn. Riêng khi đánh giá khả năng tổng quát hóa ngoài miền, Setup G mở rộng tập đánh giá bằng external Label 0 và sử dụng các tập train/validation tương ứng để kiểm soát việc đưa external data vào thí nghiệm. Do giao thức này được thiết kế để cô lập tác động của nguồn dữ liệu, còn benchmark split 9.492/535/535 được thiết kế để so sánh kiến trúc mô hình, số liệu giữa hai nhóm không được đặt cạnh nhau như các cấu hình cùng một benchmark. Các kết quả A–G chỉ được so sánh trong chuỗi thí nghiệm RQ4.

Chuỗi thí nghiệm bắt đầu bằng mốc real-only. Setup A huấn luyện PhoBERT-base bằng Real Train, chọn checkpoint trên Real Validation và đánh giá trên Real Test. Setup B giữ nguyên dữ liệu thật nhưng bổ sung class weight, sau đó có thêm biến thể điều chỉnh threshold trên validation. Hai thiết lập này tạo ra baseline cần thiết để phân biệt lợi ích của dữ liệu tạo sinh với lợi ích có thể đạt được chỉ bằng các kỹ thuật xử lý mất cân bằng truyền thống.

Bước tiếp theo kiểm tra khả năng thay thế dữ liệu thật bằng Train on Synthetic, Test on Real. Setup C sử dụng một tập synthetic có cùng kích thước và phân phối nhãn với Real Train, gồm 1.624 mẫu Label 0 và 172 mẫu Label 1. Setup D sử dụng tập synthetic cân bằng gồm 1.998 mẫu cho mỗi nhãn. Cả hai đều chọn checkpoint trên Real Validation và đánh giá trên Real Test. So sánh A/B với C/D cho biết dữ liệu tạo sinh có học được ranh giới đủ gần miền thật hay không; so sánh C với D cho thấy việc tăng mạnh Label 1 có cải thiện khả năng phát hiện smishing nhưng đồng thời làm thay đổi Precision và FP như thế nào.

Khi synthetic-only không phải mục tiêu sử dụng thực tế duy nhất, chuỗi thí nghiệm chuyển sang positive augmentation. Setup E giữ Real Train làm dữ liệu nền và lần lượt bổ sung 500, 1.000, 2.000 hoặc toàn bộ 4.996 mẫu synthetic Label 1. Thiết kế tăng dần này giúp quan sát liệu lợi ích có tăng theo số lượng hay xuất hiện điểm bão hòa, đồng thời kiểm tra trade-off giữa Recall, Precision, FP và FN. Real Train đóng vai trò neo miền, còn synthetic Label 1 mở rộng biến thể của lớp smishing.

Sau khi mở rộng lớp dương, Setup F kiểm tra chiều còn lại của ranh giới phân loại bằng cách giữ toàn bộ synthetic Label 1 và bổ sung các nguồn Label 0 khác nhau. Các biến thể lần lượt dùng synthetic Label 0, `external_real`, `external_curated`, kết hợp hai nguồn external hoặc kết hợp external với synthetic Label 0. Mục tiêu không phải tìm nguồn có số lượng lớn nhất, mà xác định nguồn Label 0 nào giúp giảm cảnh báo sai mà không làm suy giảm đáng kể khả năng phát hiện smishing.

Cuối cùng, Setup G mở rộng miền đánh giá bằng challenge test gồm Real Test đã khóa và 151 mẫu external Label 0, tạo thành tập 537 mẫu với 500 Label 0 và 37 Label 1. Biến thể G0 tái sử dụng công thức positive augmentation nhưng không thêm external Label 0 vào train, đóng vai trò kiểm tra domain shift. Các biến thể G1–G3 lần lượt bổ sung external, external curated hoặc kết hợp external với synthetic Label 0. Do phần external của challenge test chỉ chứa Label 0, Setup G đặc biệt tập trung vào FP và false-positive rate khi mô hình gặp văn bản hợp lệ ngoài miền SMS ban đầu.

> **GHI CHÚ BẢNG — Cần một bảng duy nhất tóm tắt chuỗi thí nghiệm synthetic data**
>
> | Câu hỏi | Mã kỹ thuật | Dữ liệu huấn luyện chính | Tập đánh giá | Vai trò |
> |---|---|---|---|---|
> | Mốc không dùng synthetic | A/B | Real Train; có/không class weight | Real Test | Baseline |
> | Synthetic có thay thế real? | C/D | Synthetic matched hoặc balanced | Real Test | TSTR |
> | Synthetic L1 có hữu ích? | E1–E4 | Real Train + 500/1.000/2.000/toàn bộ synthetic L1 | Real Test | Positive augmentation |
> | Nguồn L0 nào giữ ranh giới tốt? | F1–F3 | Real + synthetic L1 + các nguồn L0 | Real Test | Negative augmentation |
> | Mô hình có bền vững ngoài miền? | G0–G3 | Positive augmentation + các nguồn external L0 | Challenge Test | Domain-shift evaluation |
>
> Bảng này thay cho việc tạo nhiều tiểu mục theo Setup A–G. Thành phần chi tiết của từng biến thể có thể chuyển xuống phụ lục nếu bảng chính quá dài.

Trong toàn bộ chuỗi, các độ đo chính gồm Macro-F1, F1 Label 1, Recall Label 1, Precision Label 1 và PR-AUC; FP/FN và confusion matrix được dùng để giải thích trade-off. Precision Label 1 được giữ ở nhóm thí nghiệm này vì mục tiêu augmentation yêu cầu theo dõi trực tiếp nguy cơ tăng cảnh báo sai. Đối với challenge test, false-positive rate của Label 0 được báo cáo bổ sung do miền external chỉ có mẫu âm.

Cách phân tích ở Chương 5 không lần lượt kể kết quả từ Setup A đến G. Thay vào đó, A/B và C/D được dùng để trả lời khả năng thay thế dữ liệu thật; A/B và E trả lời giá trị của positive augmentation; E/F/G giải thích vì sao mở rộng Label 1 cần đi kèm negative coverage. Tên setup chỉ là mã truy vết tới artefact kỹ thuật và không phải cấu trúc lập luận của chương kết quả.

> **GHI CHÚ HÌNH — Có thể dùng một sơ đồ giả thuyết tăng dần**
>
> Nếu cần hình, dùng một chuỗi bốn khối:
>
> `Real-only baseline` → `Synthetic-only/TSTR` → `Real + Synthetic L1` → `Mở rộng Label 0 và external challenge`
>
> Mỗi mũi tên ghi câu hỏi tương ứng: “có thể thay thế?”, “có hữu ích khi bổ sung?”, “làm sao kiểm soát FP?”. Không vẽ lại hai nhánh thực nghiệm cũ.

> **GHI CHÚ KIỂM TRA trước khi kết thúc Mục 4.7**
>
> - Ghi rõ đây là giao thức bổ sung riêng, không phải cùng split với benchmark 17 cấu hình.
> - Kiểm tra lại tên và số mẫu của từng biến thể từ metadata trước khi đưa bảng cuối vào báo cáo.
> - Giữ kết quả mean ± std của ba seed trong Chương 5; không đưa số liệu kết quả vào Mục 4.7.
> - Nếu Real Test có chênh lệch 385/386 giữa artefact cũ, chuẩn hóa theo file split chính thức và giải thích mẫu bị loại nếu có.
> - Không gọi TSTR là một nhánh thực nghiệm; đây là phép kiểm tra khả năng thay thế dữ liệu thật trong RQ4.

> **GHI CHÚ BIÊN TẬP — Giảm tải phần thí nghiệm bổ sung**
>
> Không trình bày mọi biến thể A–G với trọng lượng ngang nhau trong Chương 5. Phần nội dung chính chỉ phân tích sâu bốn phép so sánh:
>
> 1. **A/B1 với C/D:** real-only so với synthetic-only.
> 2. **E1–E4:** ảnh hưởng của lượng synthetic Label 1.
> 3. **F1 với F2b:** synthetic Label 0 so với external curated Label 0.
> 4. **G0 với G2:** domain shift trước và sau khi bổ sung external curated Label 0.
>
> B2, F2a, F2c, F3, G1 và G3 là các kiểm tra bổ sung. Chỉ nhắc ngắn trong nội dung chính nếu chúng làm thay đổi hoặc củng cố kết luận; bảng đầy đủ, kết quả từng seed và phần lớn confusion matrix chuyển xuống phụ lục. Mạch RQ4 phải được viết theo bốn câu hỏi kiểm chứng, không kể tuần tự Setup A–G.

Khép lại chương, thiết kế thực nghiệm đã xác lập một benchmark thống nhất để so sánh 17 cấu hình mô hình, một quy trình phân tích dự đoán trên dev theo nhiều khía cạnh và một chuỗi thí nghiệm bổ sung để tách riêng vai trò của dữ liệu tạo sinh. Chương 5 sử dụng các artefact này để lần lượt trả lời bốn câu hỏi nghiên cứu về hiệu năng mô hình, ảnh hưởng của đặc điểm dữ liệu, các vùng lỗi và chiến lược sử dụng synthetic data.

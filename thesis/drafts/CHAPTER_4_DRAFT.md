# CHƯƠNG 4. PHƯƠNG PHÁP VÀ THIẾT LẬP THỰC NGHIỆM

> **Quy ước biên tập**
>
> - Các khối `GHI CHÚ HÌNH`, `GHI CHÚ BẢNG` và `GHI CHÚ KIỂM TRA` là chỉ dẫn biên tập, không phải nội dung chính thức của báo cáo.
> - Số thứ tự hình và bảng sẽ được cập nhật sau khi nội dung được đưa vào file báo cáo chính.
> - Benchmark nhiều mô hình là trục thực nghiệm chính. Phân tích distillation chuyên sâu được trình bày như một câu hỏi nghiên cứu riêng, nhưng không làm thay đổi số lượng 17 cấu hình của benchmark chính.

## 4.1. Tổng quan thiết kế thực nghiệm

Sau quá trình xây dựng và phân tích bộ dữ liệu ViSmish, chương này trình bày phương pháp thực nghiệm được sử dụng để đánh giá khả năng phát hiện tin nhắn smishing tiếng Việt của các mô hình học sâu, mô hình ngôn ngữ tiền huấn luyện và một số mô hình ngôn ngữ lớn. Thiết kế thực nghiệm không chỉ hướng đến việc xác định mô hình có kết quả tổng thể tốt nhất, mà còn làm rõ mức độ ổn định của mô hình trên các nhóm dữ liệu khác nhau, những trường hợp mô hình thường dự đoán sai và vai trò của chưng cất tri thức khi chuyển tín hiệu từ teacher lớn hơn sang student nhẹ hơn.

Thực nghiệm trung tâm của nghiên cứu là một benchmark thống nhất gồm 17 cấu hình mô hình. Các cấu hình này thuộc ba nhóm kiến trúc chính. Nhóm thứ nhất gồm các mô hình neural xử lý văn bản ở cấp ký tự, bao gồm BiLSTM, TextCNN và các biến thể được huấn luyện bằng chưng cất tri thức từ PhoBERT-base. Nhóm thứ hai gồm các mô hình ngôn ngữ tiền huấn luyện được fine-tune cho bài toán phân loại nhị phân, bao gồm PhoBERT-base, PhoBERT-large, mBERT, VisoBERT, CafeBERT, DistilBERT multilingual, XLM-RoBERTa-base, XLM-RoBERTa-large và ViCLSR. Nhóm thứ ba gồm bốn mô hình ngôn ngữ lớn được thích nghi cho bài toán hiện tại: Gemma 3 1B, Gemma 2B, Qwen3 0.6B và Qwen2.5 0.5B. Việc đặt các mô hình trong cùng một giao thức dữ liệu và đánh giá cho phép so sánh tương đối công bằng giữa mô hình cấp ký tự, mô hình đơn ngữ, mô hình đa ngữ, mô hình có quy mô khác nhau và các cấu hình có hoặc không sử dụng chưng cất tri thức.

Trong thiết kế này, chưng cất tri thức được đưa vào theo hai mức. Ở benchmark chính, distillation xuất hiện như các biến thể huấn luyện của BiLSTM và TextCNN với teacher PhoBERT-base, qua đó cho phép so sánh trực tiếp giữa từng mô hình hard-label và phiên bản distilled của chính kiến trúc đó. Sau khi benchmark hoàn tất, nghiên cứu bổ sung một phân tích chuyên sâu hẹp hơn trên TextCNN với ba teacher PhoBERT-base, CafeBERT và ViCLSR. Phân tích này được dùng để trả lời RQ4: liệu chất lượng teacher và chiến lược dùng soft label có ảnh hưởng như thế nào đến cùng một student nhẹ.

Đối với các mô hình distilled, việc đánh giá không chỉ dựa trên chất lượng phân loại. Nghiên cứu còn thực hiện phân tích tính khả thi khi triển khai bằng cách dùng PhoBERT-base làm teacher Transformer đại diện và so sánh với các biến thể TextCNN theo số lượng tham số, kích thước checkpoint, độ trễ suy luận trên CPU, thông lượng xử lý và mức sử dụng bộ nhớ cực đại. Phân tích này nhằm lượng hóa mức tài nguyên tiết kiệm được khi chuyển sang kiến trúc student nhẹ và đặt phần cải thiện về tốc độ trong tương quan với mức suy giảm hoặc bảo toàn F1 của lớp smishing. Vì vậy, một mô hình distilled không được xem là tốt hơn teacher chỉ vì có tốc độ suy luận cao hơn; kết luận cần dựa trên đồng thời hai phương diện là hiệu quả dự đoán và chi phí triển khai.

Toàn bộ quá trình thực nghiệm được tổ chức thành bốn giai đoạn. Trước hết, bộ dữ liệu được phân chia thành tập huấn luyện, tập phát triển và tập kiểm thử theo nguồn dữ liệu, nhãn và các nhóm metadata đã chuẩn hóa. Tiếp theo, các mô hình benchmark được huấn luyện trên cùng giao thức và checkpoint được lựa chọn dựa trên kết quả của tập phát triển. Sau đó, kết quả dự đoán trên tập phát triển được phân tích theo nhiều lát cắt, bao gồm độ dài tin nhắn, đặc trưng bề mặt, nguồn dữ liệu, lĩnh vực tin nhắn, hành động yêu cầu, vai trò đối tượng và thủ đoạn thuyết phục. Cuối cùng, hiệu năng của toàn bộ cấu hình benchmark được báo cáo trên cả tập phát triển và tập kiểm thử thông qua bốn độ đo gồm Macro-F1, F1 Label 1, Recall Label 1 và PR-AUC. Trong đó, kết quả trên tập phát triển được sử dụng để lựa chọn mô hình và phân tích chi tiết, còn kết quả trên tập kiểm thử chỉ phản ánh khả năng tổng quát hóa cuối cùng và không được dùng để điều chỉnh mô hình. Đối với distillation, quy trình còn bổ sung study TextCNN đa seed với ba teacher và phép đo hiệu quả triển khai đại diện trên cùng benchmark test split.

> **GHI CHÚ HÌNH 4.x — Sơ đồ quy trình thực nghiệm tổng thể**
>
> Thiết kế một sơ đồ theo chiều trái sang phải với các khối:
>
> 1. **ViSmish và các nguồn dữ liệu**  
>    `real`, `external_real`, `external_curated`, `synthetic`, `paraphrased`, `synthetic_hard_positive`.
> 2. **Phân chia dữ liệu**  
>    Train / Dev / Test và kiểm tra rò rỉ.
> 3. **Benchmark 17 cấu hình**  
>    Character-level, character-level distilled, fine-tuned PLM và fine-tuned LLM.
> 4. **Đánh giá trên Dev**  
>    Báo cáo bốn metric, lựa chọn mô hình, phân tích theo lát cắt và phân tích lỗi.
> 5. **Lựa chọn mô hình**  
>    Dựa trên kết quả dev, không dựa trên test.
> 6. **Đánh giá trên Test**  
>    Báo cáo Macro-F1, F1 Label 1, Recall Label 1 và PR-AUC để đánh giá khả năng tổng quát hóa cuối cùng.
> 7. **Phân tích distillation và tính khả thi triển khai**  
>    Study TextCNN với ba teacher; so sánh PhoBERT-base đại diện với các TextCNN theo chất lượng, kích thước, độ trễ, throughput và peak RAM.
>
> Sơ đồ chỉ trình bày benchmark chính, phân tích lỗi và study distillation chuyên sâu.

Thiết kế thực nghiệm trên được xây dựng để trả lời bốn câu hỏi nghiên cứu. Câu hỏi thứ nhất tập trung vào sự khác biệt hiệu năng giữa các nhóm mô hình. Câu hỏi thứ hai xem xét tác động của các đặc điểm dữ liệu đến kết quả dự đoán. Câu hỏi thứ ba đi sâu vào các loại lỗi và vùng dữ liệu mà mô hình chưa xử lý tốt. Câu hỏi cuối cùng phân tích chuyên sâu hiệu quả của distillation khi thay đổi teacher và chiến lược truyền soft label cho cùng một student TextCNN.

**RQ1 — Các nhóm mô hình khác nhau đạt hiệu quả như thế nào trên bộ dữ liệu ViSmish?**

Câu hỏi này được trả lời bằng benchmark giữa các mô hình character-level, các mô hình ngôn ngữ tiền huấn luyện và các mô hình ngôn ngữ lớn được fine-tune. Ngoài kết quả tổng thể, nghiên cứu còn so sánh mô hình đơn ngữ với mô hình đa ngữ, phiên bản base với phiên bản large, cũng như mô hình hard-label với biến thể distilled trong benchmark chính. Với nhóm student nhẹ, nghiên cứu đánh giá khả năng triển khai đại diện với teacher PhoBERT-base thông qua số lượng tham số, kích thước mô hình, độ trễ CPU trên mỗi tin nhắn, số tin nhắn xử lý mỗi giây và bộ nhớ RAM cực đại. Mục tiêu là xác định không chỉ mô hình có hiệu năng cao nhất, mà còn mức đánh đổi giữa chất lượng dự đoán, độ phức tạp kiến trúc và chi phí triển khai.

**RQ2 — Độ dài, đặc trưng bề mặt và metadata v2.1 ảnh hưởng như thế nào đến khả năng phát hiện smishing?**

Kết quả tổng thể có thể che khuất sự khác biệt giữa các nhóm dữ liệu. Vì vậy, dự đoán trên tập phát triển được phân tích theo độ dài tin nhắn, nguồn dữ liệu, các đặc trưng bề mặt như URL/số điện thoại/loại người gửi, cùng các nhãn metadata v2.1 như lĩnh vực tin nhắn, hành động yêu cầu, vai trò đối tượng và thủ đoạn thuyết phục. Phân tích này nhằm xác định những lát cắt mà hiệu năng suy giảm, đồng thời kiểm tra liệu các nhóm kiến trúc có phản ứng khác nhau trước văn bản ngắn, văn bản nhiễu, dữ liệu ngoài miền hoặc các thủ đoạn lừa đảo khác nhau hay không.

**RQ3 — Các mô hình thường thất bại ở những trường hợp nào và nguyên nhân có thể là gì?**

Câu hỏi này được trả lời thông qua ma trận nhầm lẫn và phân tích các trường hợp false positive, false negative. Các lỗi được nhóm theo đặc điểm nội dung và metadata v2.1 để nhận diện những khuynh hướng lặp lại, chẳng hạn smishing không chứa URL, tin nhắn hợp lệ có lời kêu gọi hành động giống lừa đảo, văn bản cá nhân phi chuẩn, các mẫu ngoài miền SMS thông thường hoặc các thủ đoạn thuyết phục dễ gây nhầm lẫn. Ngoài việc thống kê số lỗi, nghiên cứu xem xét các ví dụ đại diện và so sánh tập lỗi giữa một số mô hình tiêu biểu.

**RQ4 — Chưng cất tri thức ảnh hưởng như thế nào đến TextCNN khi thay đổi teacher và chiến lược truyền soft label?**

Để trả lời câu hỏi này, nghiên cứu giữ cố định kiến trúc TextCNN và so sánh ba chế độ huấn luyện gồm hard-label, vanilla KD và risk-aware KD dưới ba teacher khác nhau: PhoBERT-base, CafeBERT và ViCLSR. Cách thiết kế này kiểm tra hai giả thuyết: teacher mạnh hơn không nhất thiết tạo ra student tốt hơn, và cơ chế weighting theo độ tin cậy của teacher có thể hữu ích trong một số điều kiện nhưng không phải mặc định vượt trội. RQ4 cũng bao gồm phân tích trade-off triển khai đại diện giữa PhoBERT-base và các biến thể TextCNN để tách rõ lợi ích kiến trúc nhẹ khỏi lợi ích do distillation mang lại.

> **GHI CHÚ BẢNG - Bảng ánh xạ câu hỏi nghiên cứu với phương pháp đánh giá**
>
> | Câu hỏi nghiên cứu | Nội dung cần đánh giá | Nguồn bằng chứng chính |
> |---|---|---|
> | RQ1 | So sánh hiệu năng giữa các nhóm và cấu hình mô hình; đánh giá trade-off chất lượng–tài nguyên của student nhẹ | Bốn độ đo benchmark trên dev/test; benchmark triển khai CPU đại diện |
> | RQ2 | Ảnh hưởng của độ dài, đặc trưng bề mặt và metadata v2.1 | Slice analysis trên dev |
> | RQ3 | False positive, false negative và các vùng lỗi | Confusion matrix, prediction-level error analysis |
> | RQ4 | Ảnh hưởng của teacher và chiến lược soft label trong distillation | TextCNN study với PhoBERT-base, CafeBERT, ViCLSR; hard vs vanilla KD vs risk-aware KD; paired bootstrap; trade-off triển khai đại diện |
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

Từ bốn câu hỏi trên, chương này lần lượt trình bày dữ liệu và chiến lược phân chia, các mô hình tham gia benchmark, thiết lập huấn luyện, thiết kế chưng cất tri thức, độ đo đánh giá và phương pháp phân tích kết quả. Kết quả tương ứng sẽ được trình bày ở chương tiếp theo theo từng câu hỏi nghiên cứu, thay vì theo thứ tự triển khai kỹ thuật của các thí nghiệm.

> **GHI CHÚ KIỂM TRA trước khi đưa vào báo cáo**
>
> - Chương 5 sử dụng tên chính thức “Kết quả và phân tích”.
> - Benchmark cuối cùng gồm 17 cấu hình.
> - Kết quả benchmark được báo cáo trên cả dev và test với bốn độ đo: Macro-F1, F1 Label 1, Recall Label 1 và PR-AUC.
> - Dev được dùng để lựa chọn mô hình và phân tích; test chỉ được dùng để báo cáo khả năng tổng quát hóa, tránh lựa chọn mô hình theo test.
> - Không chèn kết quả dev/test cụ thể vào Mục 4.1.
> - Khi tạo sơ đồ, không sử dụng lại hình “hai nhánh thực nghiệm” trong báo cáo cũ.
> - Khi viết phần triển khai, chỉ so sánh số đo được thu thập trên cùng thiết bị và cùng giao thức; không so sánh trực tiếp thời gian từ các lần chạy khác môi trường.
> - Phép đo tính khả thi triển khai đại diện dùng PhoBERT-base và TextCNN trên benchmark test split; không diễn giải latency của teacher nếu chưa đo trực tiếp.

## 4.2. Dữ liệu và chiến lược phân chia

Để bảo đảm kết quả giữa 17 cấu hình mô hình có thể so sánh trực tiếp, benchmark sử dụng một bộ train, dev và test thống nhất được tạo từ phiên bản hoàn chỉnh của ViSmish. Chiến lược phân chia được thiết kế theo hai yêu cầu. Thứ nhất, tập phát triển và tập kiểm thử chỉ chứa dữ liệu thật hoặc dữ liệu chéo miền đã được thu thập và tuyển chọn, qua đó tránh đánh giá mô hình trên chính kiểu dữ liệu tạo sinh đã xuất hiện trong huấn luyện. Thứ hai, phân phối của các nguồn dữ liệu, nhãn và danh mục nội dung cần được duy trì tương đối ổn định giữa dev và test để hạn chế sai lệch do cách chia dữ liệu.

Bộ dữ liệu đầu vào của benchmark gồm 10.562 mẫu với sáu nguồn: `real`, `external_real`, `external_curated`, `synthetic`, `paraphrased` và `synthetic_hard_positive`. Ba nguồn đầu tiên đại diện cho dữ liệu thật hoặc dữ liệu chéo miền có thể xuất hiện trong đánh giá; ba nguồn còn lại là dữ liệu tạo sinh hoặc diễn giải lại, chỉ được dùng để mở rộng tín hiệu huấn luyện. Cách phân vai này giúp benchmark kiểm tra khả năng học từ dữ liệu mở rộng nhưng vẫn đánh giá trên các tập holdout không chứa dữ liệu tạo sinh.

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
> Bảng này là bảng mô tả dữ liệu sử dụng trong thực nghiệm. Phần giải thích đầy đủ về từng nguồn nên đặt ở Phụ lục 4.A để tránh lặp lại Chương 3.

Các cột metadata như nguồn dữ liệu, URL, số điện thoại, loại người gửi, lĩnh vực tin nhắn, hành động yêu cầu, vai trò đối tượng và thủ đoạn thuyết phục được giữ lại trong các split để phục vụ phân tích kết quả. Tuy nhiên, các thuộc tính này không được sử dụng trực tiếp làm đầu vào cho mô hình benchmark. Đầu vào dự đoán của mô hình là nội dung văn bản; metadata chỉ được dùng để hỗ trợ phân chia dữ liệu và phân tích hiệu năng theo từng lát cắt.

Quá trình phân chia sử dụng seed 42. Các mẫu thuộc `real`, `external_real` và `external_curated` được chia theo tỷ lệ mục tiêu 70/15/15 cho train/dev/test với phân tầng theo nhãn, nguồn dữ liệu và các nhóm metadata sẵn có tại thời điểm chia. Các nguồn `synthetic`, `paraphrased` và `synthetic_hard_positive` được giữ hoàn toàn trong train. Vì vậy, train có 9.492 mẫu, còn dev và test đều có 535 mẫu; tỷ lệ toàn cục không phải 70/15/15 do dữ liệu tạo sinh không được đưa vào holdout.

> **GHI CHÚ BẢNG — Cần bảng phân phối train/dev/test**
>
> | Split | Tổng số mẫu | Label 0 | Label 1 | `real` | `external_real` | `external_curated` | Dữ liệu tạo sinh |
> |---|---:|---:|---:|---:|---:|---:|---:|
> | Train | 9.492 | 4.324 | 5.168 | 1.797 | 350 | 351 | 6.994 |
> | Dev | 535 | 498 | 37 | 385 | 75 | 75 | 0 |
> | Test | 535 | 498 | 37 | 385 | 75 | 75 | 0 |
>
> Trong cột “Dữ liệu tạo sinh”, cần ghi chú đây là tổng của `synthetic`, `paraphrased` và `synthetic_hard_positive`.

Dev và test có cùng quy mô và cùng phân phối nguồn: mỗi tập gồm 385 mẫu `real`, 75 mẫu `external_real` và 75 mẫu `external_curated`; về nhãn, mỗi tập có 498 mẫu Label 0 và 37 mẫu Label 1. Phân phối mất cân bằng này gần với bối cảnh triển khai hơn train, đồng thời là lý do Accuracy không được dùng làm độ đo chính. Các chi tiết về quy tắc xử lý strata nhỏ và phân phối theo nguồn được ghi ở Phụ lục 4.A.

> **GHI CHÚ HÌNH — Có thể bổ sung sơ đồ luồng nguồn dữ liệu vào từng split**
>
> Sơ đồ nên có sáu nguồn dữ liệu ở bên trái và ba split ở bên phải:
>
> - `real`, `external_real`, `external_curated` → Train 70%, Dev 15%, Test 15%.
> - `synthetic`, `paraphrased`, `synthetic_hard_positive` → Train 100%.
>
> Hình này chỉ cần thiết nếu sơ đồ tổng quan ở Mục 4.1 chưa thể hiện rõ chính sách train-only của dữ liệu tạo sinh. Nếu Hình 4.1 đã thể hiện đầy đủ, nên dùng bảng phân phối thay vì tạo thêm một hình có nội dung trùng lặp.

Dữ liệu được kiểm tra trước và sau khi chia để hạn chế rò rỉ giữa train, dev và test. Các kiểm tra chính gồm tính đầy đủ của trường bắt buộc, trùng `sample_id`, trùng nội dung chính xác và giao nhau giữa từng cặp split. Kết quả hiện tại không phát hiện `sample_id` hoặc nội dung trùng chính xác giữa các split.

> **GHI CHÚ BẢNG — Cần bảng kết quả kiểm tra overlap**
>
> | Cặp split | Trùng `sample_id` | Trùng nội dung chính xác |
> |---|---:|---:|
> | Train – Dev | 0 | 0 |
> | Train – Test | 0 | 0 |
> | Dev – Test | 0 | 0 |

Giới hạn của kiểm tra này là mới xác nhận không có bản sao chính xác, chưa phủ hết paraphrase hoặc near-duplicate. Vì vậy, khi hoàn thiện báo cáo cần bổ sung kiểm tra sau chuẩn hóa nội dung và, nếu điều kiện cho phép, kiểm tra gần trùng bằng n-gram hoặc embedding. Quy trình kiểm tra đầy đủ được đặt ở Phụ lục 4.A.

> **GHI CHÚ KIỂM TRA RÒ RỈ CẦN HOÀN THIỆN**
>
> - Chuẩn hóa lowercase, khoảng trắng và dấu câu rồi kiểm tra duplicate.
> - Cân nhắc chuẩn hóa URL và số điện thoại thành placeholder trước khi kiểm tra.
> - Kiểm tra near-duplicate giữa các nguồn `paraphrased`/`synthetic_hard_positive` trong train với các mẫu `real` ở dev và test.
> - Không tuyên bố “không có data leakage” tuyệt đối khi mới chỉ kiểm tra trùng chính xác.

Trên nền tảng dữ liệu đã được phân chia và kiểm tra như trên, tập phát triển và tập kiểm thử đảm nhiệm hai vai trò khác nhau trong quy trình thực nghiệm. Tập dev được sử dụng trong quá trình phát triển mô hình, bao gồm lựa chọn checkpoint, theo dõi early stopping, lựa chọn cấu hình và thực hiện các phân tích chi tiết theo độ dài, đặc trưng bề mặt, nguồn dữ liệu và metadata v2.1. Kết quả trên dev cũng là căn cứ chính để so sánh và lựa chọn mô hình trong RQ1.

Tập test được giữ tách biệt với quá trình huấn luyện và lựa chọn mô hình. Sau khi các cấu hình đã được cố định, toàn bộ 17 cấu hình benchmark được đánh giá trên test bằng bốn độ đo Macro-F1, F1 Label 1, Recall Label 1 và PR-AUC. Việc báo cáo kết quả của nhiều mô hình trên test nhằm cung cấp một bảng benchmark đầy đủ; tuy nhiên, các kết quả test không được sử dụng để điều chỉnh hyperparameter, threshold hoặc thay đổi quyết định lựa chọn mô hình đã đưa ra từ dev.

Các phân tích chuyên sâu trong Chương 5 chủ yếu được thực hiện trên dev. Cách tổ chức này cho phép khảo sát nhiều lát cắt và đọc các trường hợp dự đoán sai mà không sử dụng thông tin từ test để dẫn dắt quá trình phát triển. Test được dành cho việc xác nhận liệu những xu hướng và kết luận hình thành từ dev có tiếp tục được duy trì trên dữ liệu chưa được sử dụng trong quá trình lựa chọn hay không.

Đối với phép đo tính khả thi triển khai, nghiên cứu dùng benchmark test split để giữ cùng miền đánh giá với bảng kết quả chính. Các biến thể TextCNN được đo trong cùng môi trường CPU và cùng giao thức suy luận; PhoBERT-base được dùng làm teacher đại diện trong so sánh kích thước và chất lượng, nhưng không được đưa vào so sánh latency nếu runtime chưa được đo trực tiếp. Việc đồng nhất dữ liệu, thiết bị, batch size, số lần warm-up và số lần đo là điều kiện cần để các số liệu về độ trễ, thông lượng và bộ nhớ có thể so sánh trực tiếp.

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

Benchmark được xây dựng để khảo sát 17 cấu hình mô hình thuộc ba nhóm kiến trúc: mô hình neural cấp ký tự, encoder tiền huấn luyện và mô hình ngôn ngữ lớn fine-tune bằng LoRA. Cách chia này cho phép so sánh nhiều mức độ phức tạp khác nhau, từ student nhẹ có chi phí triển khai thấp đến các mô hình tiền huấn luyện có năng lực biểu diễn mạnh hơn.

Nhóm character-level gồm BiLSTM và TextCNN, mỗi kiến trúc được huấn luyện theo hai chế độ: hard-label và distilled từ PhoBERT-base. Nhóm này được dùng để đánh giá khả năng khai thác tín hiệu bề mặt của SMS như chuỗi số, URL, viết tắt, lỗi chính tả và các biến thể ký tự phi chuẩn. Đồng thời, các biến thể distilled cho phép so sánh trực tiếp tác động của soft label trên cùng kiến trúc student.

Nhóm encoder PLM gồm PhoBERT-base, PhoBERT-large, mBERT, DistilBERT multilingual, XLM-RoBERTa-base, XLM-RoBERTa-large, VisoBERT, CafeBERT và ViCLSR. Nhóm này đại diện cho các mô hình đơn ngữ, đa ngữ và các mô hình được tiền huấn luyện trên miền văn bản tiếng Việt hoặc noisy text, qua đó kiểm tra lợi ích của biểu diễn ngữ nghĩa tiền huấn luyện đối với smishing tiếng Việt.

Nhóm LLM gồm Gemma 3 1B, Gemma 2B, Qwen3 0.6B và Qwen2.5 0.5B, được thích nghi bằng LoRA để giảm chi phí huấn luyện. Nhóm này được đưa vào benchmark để kiểm tra liệu năng lực biểu diễn rộng hơn của mô hình sinh có tạo ra lợi thế rõ ràng trên tác vụ phân loại SMS ngắn hay không.

Chi tiết cấu hình từng mô hình và vai trò so sánh được tóm tắt trong Bảng 4.x; các thông số triển khai đầy đủ được trình bày ở Phụ lục 4.B.

> **GHI CHÚ BẢNG — Cần bảng tổng hợp 17 cấu hình benchmark**
>
> | Nhóm | Cấu hình | Biểu diễn đầu vào | Cách thích nghi/huấn luyện | Vai trò so sánh |
> |---|---|---|---|---|
> | Character-level | BiLSTM | Chuỗi ký tự | Hard-label | Baseline tuần tự gọn nhẹ |
> | Character-level | BiLSTM distilled từ PhoBERT-base | Chuỗi ký tự | Hard label + soft target | Đánh giá distillation trong benchmark |
> | Character-level | TextCNN | Chuỗi ký tự | Hard-label | Baseline pattern cục bộ |
> | Character-level | TextCNN distilled từ PhoBERT-base | Chuỗi ký tự | Hard label + soft target | Đánh giá distillation trong benchmark |
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
> - Không nhầm DistilBERT multilingual là mô hình student được distill trực tiếp trong nghiên cứu; đây là một pretrained model độc lập. Hai cấu hình distillation trong benchmark chính là BiLSTM và TextCNN distilled từ PhoBERT-base; study chuyên sâu bổ sung chỉ dùng TextCNN với ba teacher.
> - Phần hyperparameter, tokenizer, classification head và hàm loss chi tiết được trình bày ở Mục 4.4, tránh lặp lại tại đây.

## 4.4. Thiết lập huấn luyện

Các cấu hình trong benchmark được huấn luyện trên cùng bộ train và sử dụng tập dev để theo dõi quá trình học, lựa chọn checkpoint và dừng sớm. Seed được cố định bằng 42 nhằm giữ nhất quán việc khởi tạo và thứ tự xử lý dữ liệu giữa các lần chạy. Sau khi checkpoint tốt nhất được chọn, mô hình sinh xác suất dự đoán cho cả dev và test với ngưỡng phân loại mặc định bằng 0,5. Tập test không tham gia vào quá trình điều chỉnh hyperparameter, lựa chọn checkpoint hoặc thay đổi threshold.

Đối với nhóm character-level, từ vựng ký tự được xây dựng chỉ từ tập train; nội dung tin nhắn được đưa về chữ thường, ánh xạ thành chuỗi ký tự tối đa 256 vị trí và padding khi cần. BiLSTM và TextCNN dùng cùng embedding ký tự, cùng tiêu chí early stopping theo dev Macro-F1 và cùng nguyên tắc chọn checkpoint tốt nhất trên dev. Do dữ liệu huấn luyện mất cân bằng, binary cross-entropy của nhóm này sử dụng `pos_weight` tính từ train, không dùng thông tin từ dev hoặc test.

Hai cấu hình distilled trong benchmark chính giữ nguyên kiến trúc và hyperparameter của student hard-label tương ứng. Khác biệt nằm ở tín hiệu giám sát: ngoài binary cross-entropy với nhãn gốc, student còn học từ xác suất mềm do PhoBERT-base sinh ra. Thiết kế loss, teacher output và study RQ4 với ba teacher được trình bày riêng ở Mục 4.5 để nhấn mạnh vai trò của chưng cất tri thức như một trục phân tích độc lập, thay vì chỉ là một biến thể huấn luyện trong benchmark.

Thông số chi tiết của BiLSTM và TextCNN được chuyển sang Phụ lục 4.B; phần thân chương chỉ giữ các quyết định ảnh hưởng trực tiếp đến khả năng so sánh giữa các nhóm mô hình.

Với chín encoder pretrained, tokenizer đi kèm từng checkpoint được sử dụng để mã hóa văn bản thành chuỗi subword; riêng PhoBERT-base và PhoBERT-large có bước phân đoạn từ tiếng Việt trước tokenization. Các encoder được fine-tune với classification head nhị phân, chọn checkpoint theo dev Macro-F1 và sinh xác suất cho dev/test bằng cùng giao thức đánh giá. Những mô hình yêu cầu bộ nhớ lớn hơn, như XLM-RoBERTa-large và ViCLSR, dùng batch size nhỏ hơn kết hợp gradient accumulation để giữ effective batch size tương đương nhóm còn lại.

Thông số fine-tuning encoder đầy đủ được đặt ở Phụ lục 4.B, bao gồm max length, batch size, gradient accumulation, learning rate, warmup, mixed precision và patience.

Bốn mô hình ngôn ngữ lớn được fine-tune theo hướng hiệu quả tham số bằng LoRA. Trọng số nền được giữ cố định và chỉ các adapter hạng thấp được cập nhật, giúp giảm chi phí huấn luyện so với full fine-tuning nhưng vẫn cho phép mô hình thích nghi với bài toán phân loại nhị phân. Cả bốn LLM dùng cùng cấu hình LoRA, cùng benchmark train split, chọn checkpoint dựa trên dev và sinh xác suất dự đoán cho dev/test để tính bốn độ đo chung.

Thông số LoRA đầy đủ của nhóm LLM được đặt ở Phụ lục 4.B, bao gồm rank, alpha, dropout, target modules, độ dài đầu vào, batch size, gradient accumulation và precision.

Để duy trì tính nhất quán của benchmark, bốn độ đo Macro-F1, F1 Label 1, Recall Label 1 và PR-AUC được tính từ xác suất dự đoán của mọi cấu hình trên cùng dev và test. Ngưỡng 0,5 được giữ cố định cho các metric phụ thuộc threshold; không tinh chỉnh threshold riêng cho từng mô hình trên test. Macro-F1 trên dev là tiêu chí chính để lựa chọn checkpoint, trong khi các độ đo còn lại được sử dụng để mô tả đầy đủ hơn sự cân bằng giữa khả năng phát hiện smishing và sai số phân loại.

Ngoài chất lượng dự đoán, nghiên cứu đánh giá tính khả thi triển khai bằng một cấu hình đại diện dựa trên PhoBERT-base teacher và các biến thể TextCNN trong distillation study. Phép đo sử dụng benchmark test split gồm 535 mẫu. Độ trễ của các TextCNN được đo với batch size 1 sau ba lượt warm-up và 20 lần lặp. Thông lượng và peak RAM được đo trên một lượt suy luận với batch size 128. Toàn bộ phép đo sử dụng một luồng CPU. So sánh còn bao gồm số lượng tham số và kích thước checkpoint. PhoBERT-base được đưa vào biểu đồ quality-size bằng số tham số, kích thước checkpoint ước lượng và F1 Label 1 từ teacher output; runtime của PhoBERT-base không được đưa vào biểu đồ latency vì local weights không được đo trực tiếp trong phép benchmark đại diện. Do đó, biểu đồ quality-latency chỉ so sánh các TextCNN đã có số đo CPU, còn biểu đồ quality-size so sánh PhoBERT-base với TextCNN trên cùng trục log-scale.

> **GHI CHÚ BẢNG — Cần bảng giao thức đo tính khả thi triển khai**
>
> | Thành phần | Thiết lập |
> |---|---|
> | Các mô hình | PhoBERT-base đại diện; TextCNN hard, vanilla KD và risk-aware KD |
> | Dữ liệu | Benchmark test split 535 mẫu |
> | Thiết bị | Cùng CPU, 1 thread |
> | Latency | Batch size 1, 3 warm-up, 20 lần lặp; chỉ báo cáo cho TextCNN đã đo runtime |
> | Throughput | Một lượt suy luận, batch size 128 |
> | Tài nguyên | Số tham số, kích thước checkpoint, peak RAM |
> | Chất lượng đi kèm | F1 Label 1 trên cùng split |
>
> Tên CPU, tổng RAM và phiên bản thư viện có thể bổ sung trong phụ lục tái lập nếu cần; bảng kết quả và biểu đồ trade-off thuộc Chương 5.

Chi tiết hyperparameter của BiLSTM, TextCNN, các encoder và LoRA được đặt ở Phụ lục 4.B để bảo đảm khả năng tái lập mà không làm phần thân chương bị quá tải bởi các tham số kỹ thuật.

> **GHI CHÚ KIỂM TRA trước khi kết thúc Mục 4.4**
>
> - Cấu hình LoRA đã được chốt và dùng thống nhất cho cả bốn LLM.
> - Xác nhận phần cứng và phiên bản thư viện của các nhóm mô hình nếu khoa yêu cầu khả năng tái lập chi tiết.
> - PhoBERT-large đã được xác nhận dùng train/evaluation batch size 16/32 và gradient accumulation 1. Chỉ XLM-RoBERTa-large và ViCLSR dùng cấu hình 8/16 với gradient accumulation 2.
> - Mixed-precision FP16 đã được xác nhận từ cả file config và các lệnh chạy riêng từng mô hình trên Kaggle có truyền tham số `--fp16`. Script PowerShell cục bộ không được xem là lệnh tái lập chính của các lần chạy này.
> - Deployment benchmark đại diện đã được chạy trên benchmark test split; PhoBERT-base chỉ có F1 và kích thước/params trong biểu đồ size, không có latency đo trực tiếp.
> - Không đưa thời gian huấn luyện hoặc kết quả metric vào Mục 4.4; các số liệu so sánh thuộc Chương 5.

## 4.5. Thiết kế chưng cất tri thức

Chưng cất tri thức là một thành phần thực nghiệm quan trọng của nghiên cứu vì nó kiểm tra khả năng chuyển một phần tín hiệu dự đoán từ mô hình teacher lớn hơn sang student nhẹ hơn. Trong bài toán smishing, mục tiêu của distillation không chỉ là tăng điểm trung bình của student. Quan trọng hơn, study này cần trả lời liệu soft label từ teacher có giúp student nhận diện tốt hơn các mẫu smishing khó hay không, và liệu việc tin vào teacher một cách đồng đều có thể gây hại khi teacher mắc lỗi ở các trường hợp rủi ro cao.

Về cơ sở lý thuyết, distillation dựa trên giả định rằng phân phối xác suất của teacher chứa nhiều thông tin hơn nhãn nhị phân cứng. Với một mẫu có nhãn gốc \(y \in \{0,1\}\), nhãn cứng chỉ cho biết lớp đúng theo annotation. Ngược lại, xác suất teacher \(q\) cho biết mức độ chắc chắn của teacher đối với Label 1. Khi teacher được làm mềm bằng temperature \(T=2\), các xác suất ít cực đoan hơn so với temperature 1, nhờ đó student có thể học được vùng ranh giới giữa tin nhắn hợp lệ và smishing thay vì chỉ học quyết định 0/1. Cách tiếp cận này kế thừa nguyên lý knowledge distillation của Hinton và cộng sự, nhưng được điều chỉnh cho bài toán phân loại nhị phân mất cân bằng và có chi phí false negative cao.

Trong nghiên cứu này, distillation được triển khai theo dạng offline. Teacher được fine-tune trước trên benchmark train split, chọn checkpoint theo dev và sau đó sinh teacher outputs cho train, dev và test. Student không gọi teacher trong lúc huấn luyện; thay vào đó, student đọc lại các file teacher output đã lưu. Cách làm này giúp kết quả tái lập hơn, giảm chi phí huấn luyện student và cho phép dùng cùng một teacher output để so sánh nhiều chế độ KD.

Mỗi teacher output lưu các trường chính gồm logits của hai lớp, xác suất Label 1 ở temperature 1, xác suất Label 1 ở temperature 2, nhãn dự đoán của teacher, confidence, trạng thái teacher có đồng ý với nhãn gốc hay không và `distill_weight`. Trong đó, `teacher_p1_t2` là soft target được dùng cho student. Trường `distill_weight` được dùng riêng trong chế độ risk-aware KD để giảm ảnh hưởng của teacher khi tín hiệu teacher có khả năng không đáng tin.

Hàm mất mát của student kết hợp hard-label loss và soft-target loss:

\[
\mathcal{L}
= \alpha \cdot \mathrm{BCE}(y, p_s)
+ (1-\alpha) \cdot w_i \cdot \mathrm{BCE}(q_i, p_s),
\]

trong đó \(p_s\) là xác suất Label 1 của student, \(q_i\) là soft target từ teacher, \(w_i\) là trọng số distillation của mẫu \(i\), và \(\alpha = 0{,}8\). Như vậy, student vẫn chủ yếu học từ nhãn gốc, còn soft label đóng vai trò tín hiệu bổ sung. Thiết kế này thận trọng hơn việc để teacher chi phối hoàn toàn, đặc biệt trong bối cảnh teacher có thể bỏ sót một số mẫu smishing.

Nghiên cứu sử dụng ba chế độ huấn luyện để tách riêng ảnh hưởng của từng loại tín hiệu:

| Chế độ | Tín hiệu huấn luyện | Vai trò trong phân tích |
|---|---|---|
| `hard` | Chỉ dùng nhãn gốc `0/1` | Baseline của student |
| `vanilla_kd` | Nhãn gốc + soft target với trọng số đồng đều | Kiểm tra lợi ích của soft label đơn giản |
| `risk_aware_kd` | Nhãn gốc + soft target có `distill_weight` | Kiểm tra lợi ích của việc giảm ảnh hưởng teacher không đáng tin |

Với `vanilla_kd`, mọi mẫu có \(w_i = 1\), tức student tin soft target của teacher như nhau. Với `risk_aware_kd`, trọng số này phụ thuộc vào quan hệ giữa dự đoán teacher và nhãn gốc. Khi teacher dự đoán đúng với confidence từ 0,8 trở lên, soft target có trọng số 1,0; khi teacher dự đoán đúng nhưng confidence thấp hơn 0,8, trọng số là 0,7; các trường hợp teacher dự đoán sai nhận trọng số ban đầu bằng 0,3. Riêng khi teacher bỏ sót mẫu Label 1, tức false negative trên smishing, ảnh hưởng của soft target được đưa về 0. Quy tắc này phản ánh giả định nghiệp vụ của bài toán: truyền một false negative từ teacher sang student có rủi ro lớn hơn truyền một lỗi thông thường, vì nó có thể làm student học cách bỏ qua tin nhắn lừa đảo.

Distillation xuất hiện ở hai cấp trong thiết kế thực nghiệm. Ở benchmark chính, hai cấu hình BiLSTM distilled và TextCNN distilled dùng PhoBERT-base làm teacher để so sánh trực tiếp với phiên bản hard-label cùng kiến trúc. Phần này cho biết trong một bảng benchmark rộng, việc thêm soft target có tạo ra khác biệt đáng kể so với huấn luyện chỉ bằng nhãn cứng hay không.

Ở RQ4, nghiên cứu mở rộng thành một study chuyên sâu nhưng vẫn giữ phạm vi có kiểm soát. Student được cố định là TextCNN cấp ký tự, còn teacher thay đổi giữa PhoBERT-base, CafeBERT và ViCLSR. TextCNN được chọn vì đây là student nhẹ, có chi phí suy luận thấp và đủ đơn giản để cô lập tác động của tín hiệu teacher. Nếu thay đổi đồng thời cả teacher lẫn kiến trúc student, rất khó phân biệt cải thiện đến từ soft label hay từ năng lực biểu diễn của student.

Ba teacher được chọn để đại diện cho các nguồn tri thức khác nhau trong nhóm encoder tiếng Việt. PhoBERT-base là teacher đã dùng trong benchmark distilled chính, đóng vai trò mốc so sánh. CafeBERT và ViCLSR được bổ sung vì chúng là các encoder tiếng Việt/noisy-text có kết quả teacher tốt trong benchmark PLM. Việc đưa cả ba teacher vào cùng một study cho phép kiểm tra giả thuyết thường gặp nhưng không hiển nhiên: teacher mạnh hơn có nhất thiết tạo ra student distilled tốt hơn hay không.

Mỗi tổ hợp teacher và chế độ huấn luyện được chạy với ba seed 42, 123 và 2025. Student dùng cùng preprocessing cấp ký tự, cùng hyperparameter TextCNN đã mô tả ở Mục 4.4, tối đa 12 epoch và early stopping theo dev Macro-F1 với patience bằng 3. Kết quả được tổng hợp bằng trung bình và độ lệch chuẩn qua ba seed. Để so sánh từng biến thể KD với hard-label baseline cùng teacher, nghiên cứu sử dụng paired bootstrap trên các file prediction theo `sample_id`. Cách so sánh paired này phù hợp vì các mô hình trong cùng study dự đoán trên cùng một tập mẫu.

Phân tích RQ4 được tổ chức thành ba lớp. Lớp thứ nhất đánh giá chất lượng teacher trước khi truyền tri thức. Lớp thứ hai so sánh `hard`, `vanilla_kd` và `risk_aware_kd` trong từng teacher study để xác định soft label có cải thiện TextCNN hay không. Lớp thứ ba so sánh chéo ba teacher để xem KD gain có ổn định theo chất lượng teacher hay phụ thuộc vào kiểu lỗi của teacher.

Ngoài chất lượng dự đoán, RQ4 còn có một phân tích trade-off triển khai đại diện. Phần này không cố gắng đo latency cho mọi teacher lớn, vì mục tiêu là minh họa khoảng cách giữa một Transformer teacher và một TextCNN student trong điều kiện đã có số đo thống nhất. Nghiên cứu dùng PhoBERT-base như teacher Transformer đại diện trong biểu đồ quality-size, còn biểu đồ quality-latency chỉ dùng các biến thể TextCNN đã đo runtime CPU. Cách trình bày này tách rõ hai kết luận: kiến trúc TextCNN tạo ra lợi thế kích thước và tốc độ; distillation chỉ thay đổi chất lượng dự đoán của cùng một student, không tự làm mô hình nhỏ hơn hoặc nhanh hơn.

> **GHI CHÚ BẢNG — Cần bảng tóm tắt thiết kế distillation**
>
> | Thành phần | Thiết lập |
> |---|---|
> | Benchmark distilled | BiLSTM và TextCNN distilled từ PhoBERT-base |
> | Study RQ4 | TextCNN cố định, thay đổi teacher và chế độ KD |
> | Teacher RQ4 | PhoBERT-base, CafeBERT, ViCLSR |
> | Chế độ | `hard`, `vanilla_kd`, `risk_aware_kd` |
> | Soft target | `teacher_p1_t2`, temperature = 2 |
> | Loss weight | \(\alpha = 0{,}8\) cho hard loss, \(1-\alpha = 0{,}2\) cho soft loss |
> | Risk-aware rule | Giảm trọng số teacher không chắc chắn hoặc sai; false negative trên Label 1 có trọng số 0 |
> | Seeds | 42, 123, 2025 |
> | So sánh thống kê | Mean ± SD và paired bootstrap so với hard baseline cùng teacher |
> | Trade-off triển khai | PhoBERT-base đại diện cho quality-size; TextCNN cho quality-latency |

> **GHI CHÚ HÌNH — Sơ đồ study distillation**
>
> Nếu cần hình riêng cho RQ4, dùng luồng:
>
> `Fine-tune teacher` → `Sinh teacher outputs train/dev/test` → `TextCNN hard / vanilla KD / risk-aware KD` → `Mean ± SD + paired bootstrap` → `Trade-off triển khai đại diện`.
>
> Hình này nên đặt sau bảng thiết kế distillation và không thay thế sơ đồ benchmark tổng thể ở Mục 4.1.

> **GHI CHÚ KIỂM TRA trước khi kết thúc Mục 4.5**
>
> - Ghi rõ benchmark chính vẫn gồm 17 cấu hình; study RQ4 là phân tích chuyên sâu bổ sung.
> - Không kết luận teacher mạnh hơn luôn tốt hơn cho distillation; đây là giả thuyết cần kiểm tra bằng kết quả.
> - Không tuyên bố distillation làm mô hình nhỏ hơn hoặc nhanh hơn. Lợi thế kích thước/tốc độ đến từ kiến trúc TextCNN.
> - Không đưa bảng mean ± SD, bootstrap hoặc biểu đồ trade-off vào Chương 4; các kết quả đó thuộc Chương 5.

## 4.6. Các độ đo đánh giá

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

> **GHI CHÚ HÌNH — Không cần biểu đồ metric trong Mục 4.6**
>
> Các đường Precision–Recall, biểu đồ so sánh metric và confusion matrix đều là kết quả thực nghiệm, nên chỉ xuất hiện tại Chương 5 nếu phục vụ trực tiếp cho một câu hỏi nghiên cứu. Mục 4.6 chỉ cần bảng tóm tắt độ đo và các công thức.

> **GHI CHÚ KIỂM TRA trước khi kết thúc Mục 4.6**
>
> - Dùng thống nhất thuật ngữ `PR-AUC` trong báo cáo và ghi rõ cách tính bằng Average Precision; không dùng xen kẽ `AUPRC` nếu chưa định nghĩa hai tên là tương đương trong nghiên cứu.
> - Bảng benchmark chính chỉ gồm Macro-F1, F1 Label 1, Recall Label 1 và PR-AUC như đã chốt.
> - Precision Label 1 và FP/FN được dùng trong phần giải thích, không cần thêm vào bảng benchmark chính nếu bảng trở nên quá rộng.
> - Không dùng Accuracy để tuyên bố mô hình tốt nhất.
> - Khi kết luận từ chênh lệch metric, luôn kiểm tra số mẫu Label 1 và số FP/FN tương ứng.

## 4.7. Phương pháp phân tích kết quả

Bảng benchmark tổng thể cho biết mô hình nào đạt kết quả cao hơn, nhưng chưa giải thích mô hình hoạt động tốt hoặc thất bại trong những điều kiện nào. Vì vậy, sau bước đánh giá chung, nghiên cứu sử dụng các file dự đoán ở cấp mẫu trên tập dev để phân tích kết quả theo nhiều lát cắt dữ liệu và theo từng loại lỗi. Mỗi bản ghi dự đoán giữ lại nội dung tin nhắn, nhãn thật, nhãn dự đoán, xác suất Label 1, confidence, loại lỗi và các metadata v2.1 như nguồn dữ liệu, đặc trưng bề mặt, lĩnh vực tin nhắn, hành động yêu cầu, vai trò đối tượng và thủ đoạn thuyết phục. Cấu trúc này cho phép nối kết trực tiếp kết quả định lượng với đặc điểm của từng mẫu.

Phân tích được thực hiện chủ yếu trên dev, bởi đây là tập được phép sử dụng trong quá trình phát triển và diễn giải mô hình. Test chỉ được dùng để xác nhận kết quả tổng quát ở mức cuối cùng; không sử dụng các lỗi trên test để thay đổi mô hình, ngưỡng hoặc lựa chọn lát cắt có lợi. Đối với mọi lát cắt, nghiên cứu báo cáo số lượng mẫu trước khi trình bày metric. Những nhóm có quá ít mẫu, đặc biệt quá ít Label 1, chỉ được dùng như quan sát mô tả và không làm cơ sở cho kết luận tổng quát.

Phân tích lát cắt tập trung vào các thuộc tính có khả năng ảnh hưởng đến hành vi mô hình: độ dài tin nhắn, đặc trưng bề mặt, nguồn dữ liệu, lĩnh vực tin nhắn, hành động yêu cầu, vai trò đối tượng và thủ đoạn thuyết phục. Với mỗi lát cắt, nghiên cứu luôn báo cáo số lượng mẫu trước khi đọc metric; các nhóm có quá ít mẫu Label 1 chỉ được dùng như quan sát mô tả, không dùng để kết luận ưu thế mô hình. Các lát cắt chỉ có một nhãn, chẳng hạn một số nguồn external chỉ chứa Label 0, được phân tích bằng FP, false-positive rate hoặc số lỗi thay vì F1 Label 1. Bảng phân phối lát cắt và quy tắc xử lý nhóm ít mẫu được đặt ở Phụ lục 4.C.

Phân tích theo lát cắt được nối tiếp bằng phân tích lỗi ở cấp mẫu. Trước hết, số FP và FN của các mô hình được tổng hợp để xác định mô hình thiên về bỏ sót smishing hay cảnh báo quá mức. Sau đó, các lỗi được gán vào một taxonomy nguyên nhân dựa trên nội dung và metadata v2.1. Các nhóm dự kiến gồm smishing không chứa URL, smishing dùng văn phong pháp lý hoặc đe dọa, tin hợp lệ có hành động yêu cầu giống lừa đảo, văn bản cá nhân phi chuẩn, văn bản ngoài miền SMS và các trường hợp thiếu ngữ cảnh hoặc nhãn có thể gây tranh luận.

Việc gán taxonomy bằng quy tắc chỉ được sử dụng để sàng lọc và thống kê sơ bộ. Các mẫu đưa vào báo cáo phải được rà thủ công để xác nhận nhóm lỗi. Nghiên cứu ưu tiên những lỗi xuất hiện ở nhiều mô hình, lỗi có confidence cao và các trường hợp thể hiện sự khác biệt giữa nhóm kiến trúc. Mỗi ví dụ định tính cần ghi nội dung rút gọn, nhãn thật, dự đoán, xác suất Label 1, loại lỗi và nhận xét; ví dụ chỉ có vai trò minh họa cho xu hướng đã được thống kê, không thay thế bằng chứng định lượng.

Cuối cùng, tập lỗi được so sánh giữa các mô hình đại diện thay vì trình bày confusion matrix của cả 17 cấu hình. Nhóm so sánh dự kiến gồm mô hình có dev Macro-F1 cao nhất, mô hình có Recall Label 1 cao nhất nếu khác mô hình đứng đầu, một encoder baseline, một mô hình character-level và một student distilled có ý nghĩa. Phân tích xem xét các mẫu mọi mô hình đều sai, mẫu chỉ một nhóm kiến trúc dự đoán đúng và sự giao nhau giữa FP/FN. Cách chọn mô hình đại diện phải dựa trên dev và được xác định trước khi đọc kết quả test.

> **GHI CHÚ HÌNH/BẢNG CHO CHƯƠNG 5**
>
> - Nên dùng heatmap hoặc grouped bar chart cho metric theo độ dài, đặc trưng bề mặt và metadata v2.1.
> - Có thể dùng bảng FP/FN theo `data_origin` thay vì nhiều confusion matrix.
> - Nếu so sánh tập lỗi của từ ba mô hình trở lên, ưu tiên UpSet plot; không dùng Venn diagram quá nhiều tập.
> - Chỉ dùng 5–8 ví dụ lỗi tiêu biểu trong bảng định tính.
> - Mọi biểu đồ lát cắt phải ghi số mẫu của nhóm hoặc đặt bảng phân phối ngay trước đó.

> **GHI CHÚ KIỂM TRA trước khi kết thúc Mục 4.7**
>
> - Xây dựng script phân tích dùng chung các file `*_predictions_dev.csv` để mọi mô hình được áp dụng cùng quy tắc.
> - Chuẩn hóa tên cột `has_url`/`has_URL` trước khi tổng hợp.
> - Không tính F1 hoặc PR-AUC cho lát cắt chỉ có một nhãn.
> - Chốt danh sách mô hình đại diện dựa trên dev trước khi phân tích test.
> - Các nhóm dưới năm mẫu Label 1 chỉ được mô tả, không dùng để khẳng định ưu thế mô hình.
> - Đồng bộ tên các cột metadata v2.1 giữa file dự đoán, script phân tích và bảng kết quả ở Chương 5.

Khép lại chương, thiết kế thực nghiệm đã xác lập một benchmark thống nhất để so sánh 17 cấu hình mô hình, một quy trình phân tích dự đoán trên dev theo nhiều khía cạnh, một phân tích lỗi ở cấp mẫu và một study distillation chuyên sâu trên TextCNN với ba teacher. Chương 5 sử dụng các artefact này để lần lượt trả lời bốn câu hỏi nghiên cứu về hiệu năng mô hình, ảnh hưởng của đặc điểm dữ liệu, các vùng lỗi và cơ chế chưng cất tri thức.

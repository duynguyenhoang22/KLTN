# Kịch bản thuyết trình trang 10–14

Thời lượng mục tiêu: khoảng 7 phút 30 giây.

## Trang 10 — Phương pháp thực nghiệm (khoảng 1 phút 20 giây)

Tiếp theo, em xin trình bày quy trình thực nghiệm tổng thể của đề tài.

Đầu tiên, nhóm tổng hợp bộ ViSmish cùng nhiều nguồn dữ liệu bổ sung, bao gồm dữ
liệu thật, dữ liệu external, dữ liệu tạo sinh, paraphrase và các mẫu hard
positive. Dữ liệu sau đó được chia thành train, dev và test, đồng thời thực hiện
kiểm tra rò rỉ để hạn chế việc các mẫu trùng hoặc quá tương đồng xuất hiện ở
nhiều tập.

Trên cùng một benchmark, nhóm đánh giá tổng cộng 17 cấu hình, thuộc ba nhóm
chính: các mạng nơ-ron ký tự, các mô hình ngôn ngữ tiền huấn luyện và bốn mô
hình LLM được thích nghi bằng LoRA.

Kết quả trên tập dev được dùng để so sánh các metric tổng thể, phân tích theo
các lát cắt dữ liệu và xem xét các lỗi false positive, false negative. Việc lựa
chọn mô hình chỉ dựa trên dev, không dựa trên test. Tập test được giữ lại để
đánh giá cuối cùng khả năng tổng quát hóa.

Ngoài chất lượng dự đoán, nhóm còn so sánh tính khả thi triển khai giữa
PhoBERT-base và các mô hình được chưng cất thông qua số tham số, kích thước,
latency, throughput và RAM.

Cuối cùng, nhóm thực hiện một chuỗi thí nghiệm riêng để phân tích dữ liệu tạo
sinh: liệu nó có thể thay thế dữ liệu thật hay chỉ phù hợp làm augmentation.

## Trang 11 — Kết quả benchmark (khoảng 1 phút 30 giây)

Đây là kết quả benchmark của 17 cấu hình trên cả tập dev và test, với bốn độ đo
chính là Macro-F1, F1 và Recall của Label 1, cùng PR-AUC.

Kết quả nổi bật nhất là Gemma 2B. Trên tập test, mô hình đạt Macro-F1 0,9585,
F1 Label 1 là 0,9231, Recall Label 1 là 0,9730 và PR-AUC là 0,9853. Điều này cho
thấy nhóm LLM có hiệu năng tổng thể cao nhất khi tài nguyên tính toán không phải
là ràng buộc chính.

Trong nhóm PLM, ViCLSR và XLM-RoBERTa-large cho kết quả cạnh tranh. Tuy nhiên,
không có một mô hình duy nhất tốt nhất ở mọi độ đo. Ví dụ, một số mô hình đạt
Recall cao nhưng F1 hoặc PR-AUC thấp hơn, thể hiện sự đánh đổi giữa khả năng
phát hiện và nguy cơ cảnh báo sai.

Với nhóm mô hình ký tự, TextCNN chưng cất đạt F1 Label 1 trên test là 0,8500 và
Recall là 0,9189. Kết quả này chưa vượt các mô hình lớn nhất, nhưng đáng chú ý
vì mô hình có kích thước rất nhỏ. Do đó, benchmark không chỉ cho một đáp án về
mô hình chính xác nhất, mà còn tạo cơ sở để lựa chọn theo điều kiện triển khai.

## Trang 12 — Tính khả thi triển khai và phân tích độ dài (khoảng 2 phút)

Trang này làm rõ sự đánh đổi giữa chất lượng và chi phí triển khai.

[Chỉ vào bảng phía trên bên trái]

PhoBERT-base có khoảng 135 triệu tham số và kích thước gần 517 MB. Trong khi
đó, hai student chỉ có khoảng 80 đến 88 nghìn tham số và kích thước dưới
0,35 MB. Như vậy, kích thước mô hình giảm hơn một nghìn lần.

Về tốc độ CPU, PhoBERT-base cần khoảng 248 mili giây cho một tin nhắn. BiLSTM
chưng cất chỉ cần khoảng 2,57 mili giây và TextCNN chưng cất khoảng 1,62 mili
giây. Peak RAM cũng giảm từ gần 1,8 GB xuống khoảng 400 MB.

[Chỉ vào biểu đồ trade-off phía trên bên phải]

Vì vậy, TextCNN chưng cất nằm ở vùng có latency thấp nhưng vẫn duy trì F1 tương
đối tốt. Đây là lựa chọn phù hợp hơn cho thiết bị biên hoặc hệ thống cần xử lý
nhanh. Điểm cần nhấn mạnh là khi triển khai, chỉ cần student; PhoBERT-base chỉ
được dùng làm teacher trong quá trình huấn luyện.

[Chuyển xuống hai biểu đồ độ dài]

Khi phân tích theo độ dài tin nhắn, hiệu năng không giảm theo một xu hướng
giống nhau ở mọi mô hình. DistilBERT multilingual có F1 cao ở nhóm từ 81 đến
160 ký tự nhưng giảm rõ ở nhóm trên 240 ký tự. Ngược lại, TextCNN và
TextCNN chưng cất duy trì Recall khoảng 0,90 ở nhóm tin dài.

Điều này gợi ý rằng độ dài là một yếu tố ảnh hưởng đến từng kiến trúc theo cách
khác nhau. Tuy nhiên, do số mẫu Label 1 trong từng lát cắt còn nhỏ, kết quả này
được dùng để nhận diện xu hướng, không dùng để khẳng định ưu thế tuyệt đối.

## Trang 13 — Các lỗi dự đoán tiêu biểu (khoảng 1 phút 10 giây)

Phân tích lỗi cho thấy các mô hình không chỉ sai ở các mẫu bị che giấu phức
tạp, mà còn sai ở những trường hợp có ý nghĩa ngữ cảnh mơ hồ.

Hai dòng đầu là false negative. Mẫu đòi nợ có văn phong hành chính bị cả bốn
mô hình bỏ sót với confidence trung bình 0,99. Mẫu cảnh báo giả mạo ngân hàng
cũng dễ bị hiểu thành một thông báo an toàn, vì trong nội dung xuất hiện các
cụm như “không cung cấp mật khẩu, OTP”.

Hai dòng sau là false positive. Một thông báo hội thảo hợp lệ bị cảnh báo do có
URL, hotline và lời kêu gọi hành động. Mẫu external còn lại dùng ngôn ngữ đời
thường nhưng chứa các từ như “phá sản” và “khoản nợ”, khiến hai mô hình TextCNN
liên hệ nó với smishing.

Như vậy, URL hay từ khóa tài chính là những tín hiệu hữu ích nhưng không đủ để
quyết định nhãn. Mô hình cần hiểu đồng thời mục đích của tin nhắn và ngữ cảnh
sử dụng các tín hiệu đó.

## Trang 14 — Giá trị của dữ liệu tạo sinh (khoảng 1 phút 30 giây)

Cuối cùng, nhóm trả lời câu hỏi dữ liệu tạo sinh nên được sử dụng như thế nào.

[Chỉ vào biểu đồ 1]

Khi chỉ huấn luyện bằng synthetic và kiểm tra trên dữ liệu thật, F1 Label 1
giảm từ 0,911 xuống còn 0,301 hoặc 0,494. Vì vậy, dữ liệu tạo sinh chưa thể
thay thế hoàn toàn dữ liệu thật.

[Chỉ vào biểu đồ 2]

Khi giữ dữ liệu thật làm nền và bổ sung synthetic Label 1, hiệu năng có cải
thiện nhẹ, nhưng không tăng tuyến tính theo số lượng. Thêm nhiều dữ liệu hơn
không mặc nhiên tạo ra mô hình tốt hơn; Precision và Recall có thể dịch chuyển
theo các hướng khác nhau.

[Chỉ vào biểu đồ 3]

Việc lựa chọn nguồn Label 0 cũng tạo ra trade-off. External curated giúp tăng
PR-AUC, dù F1 và Precision trên Real Test giảm nhẹ so với synthetic Label 0.

[Chỉ vào biểu đồ 4]

Lợi ích rõ nhất xuất hiện khi đánh giá trên challenge test có dữ liệu ngoài
miền. Sau khi bổ sung external curated Label 0, F1 tăng từ khoảng 0,624 lên
0,901; Precision tăng từ 0,475 lên 0,905; còn tỷ lệ false positive giảm từ
7,73% xuống 0,73%.

Từ đó, nhóm kết luận dữ liệu thật vẫn cần giữ vai trò neo miền. Synthetic Label
1 phù hợp để mở rộng các biểu hiện smishing, còn Label 0 được tuyển chọn giúp
kiểm soát cảnh báo sai và tăng độ bền trước domain shift.


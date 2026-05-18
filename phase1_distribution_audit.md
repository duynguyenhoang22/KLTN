# Báo cáo Phân bố Dữ liệu Dataset hậu Phase1

Dataset: `data/final/vismishds_phase1_final.csv`

## 1. Tổng thể

| Độ đo | SL |
|---|---:|
| Tổng số mẫu | 10,562 |

## 2. Phân phối nhãn

| Nhãn | SL | Tỉ lệ |
|---|---:|---:|
| 0 | 5,320 | 50.35% |
| 1 | 5,242 | 49.65% |

Tổng thể: Dataset gần như đảm bảo tỉ lệ 1:1.

## 3. Phân phối nguồn dữ liệu

| Nguồn | SL | Tỉ lệ |
|---|---:|---:|
| real | 2,567 | 24.3% |
| synthetic | 7,995 | 75.7% |

Dữ liệu tạo sinh chiếm 3/4 - đã biết từ trước.

## 4. Phân phối nhãn theo nguồn

| Nhãn | Nguồn | SL | Tỉ lệ trong BDL |
|---|---|---:|---:|
| 0 | real | 2,321 | 21.98% |
| 0 | synthetic | 2,999 | 28.39% |
| 1 | real | 246 | 2.33% |
| 1 | synthetic | 4996 | 47.3% |

Label 1 chỉ có 246 real cases trong tổng số 5,242 dữ liệu label 1, tức chỉ chiếm 4.69%, trong khi dữ liệu tạo sinh chiếm tới 95.31%.

--> Các hạn chế cố hữu của tạo sinh dữ liệu văn bản mà không có nguồn ngữ cảnh cụ thể chống lưng hiện rõ: Tradeoff giữa pattern lặp lại và tính kiểm soát đầu ra của LLM; Các thông tin như SĐT, URL không có sự đa dạng, lặp lại liên tục trong dữ liệu tạo sinh khiến LLM học shortcut thay vì thật sự hiểu dữ liệu.

## 5. Thống kê Loại tin nhắn

| Category | SL | Tỉ lệ |
|---|---:|---:|
| Viễn thông | 1,360 | 12.88% |
| Nội dung nhạy cảm | 732 | 6.93% |
| Cờ bạc / Betting | 721 | 6.83% |
| Crypto / Đầu tư giả | 719 | 6.81% |
| Tuyển dụng giả | 703 | 6.65% |
| BHXH / Trợ cấp | 678 | 6.42% |
| Ngân hàng thật | 576 | 5.45% |
| Dịch vụ công giả | 565 | 5.35% |
| Khác | 553 | 5.23% |
| Giả mạo ngân hàng | 519 | 4.91% |
| Tin nhắn cá nhân và OTP | 500 | 4.73% |
| Quảng cáo hợp lệ | 486 | 4.60% |
| Đòi nợ / Đe doạ | 477 | 4.51% |
| Dịch vụ công thật | 470 | 4.45% |
| Vận chuyển | 418 | 3.96% |
| Thương mại điện tử | 400 | 3.79% |
| Cá nhân & OTP | 301 | 2.85% |
| Dịch vụ y tế | 300 | 2.84% |
| Co bac/Betting | 53 | 0.50% |
| BHXH/Trợ cấp giả | 15 | 0.14% |
| Đòi nợ/Đe doạ | 12 | 0.11% |
| Đầu tư/Crypto giả | 2 | 0.02% |
| Y tế | 2 | 0.02% |

Một số nhãn category trong dataset Phase 1 chưa thống nhất về quy ước đặt tên, ví dụ khác biệt ở dấu phân tách, dấu tiếng Việt, hoặc cách đảo thứ tự cụm từ. Do đó, nghiên cứu giữ nguyên cột category gốc để truy vết và bổ sung cột category_normalized phục vụ thống kê, phân tích và chia dữ liệu.

## 6. Thống kê nhãn theo Loại tin nhắn

| label | category_normalized | count |
|---|---|---|
| 0 | Cá nhân & OTP | 801 |
| 0 | Dịch vụ công thật | 470 |
| 0 | Dịch vụ y tế | 302 |
| 0 | Khác | 507 |
| 0 | Ngân hàng thật | 576 |
| 0 | Quảng cáo hợp lệ | 486 |
| 0 | Thương mại điện tử | 400 |
| 0 | Viễn thông | 1360 |
| 0 | Vận chuyển | 418 |
| 1 | BHXH / Trợ cấp giả | 693 |
| 1 | Crypto / Đầu tư giả | 721 |
| 1 | Cờ bạc / Betting | 774 |
| 1 | Dịch vụ công giả | 565 |
| 1 | Giả mạo ngân hàng | 519 |
| 1 | Khác | 46 |
| 1 | Nội dung nhạy cảm | 732 |
| 1 | Tuyển dụng giả | 703 |
| 1 | Đòi nợ / Đe dọa | 489 |

## 7. Thống kê URL và SDT

### URL

| has_url | SL | Tỉ lệ |
|---|---:|---:|
| 0 | 4,956 | 46.92% |
| 1 | 5,606 | 53.08% |

### SDT

| has_phone_number | Count | Ratio |
|---|---:|---:|
| 0 | 7,515 | 71.15% |
| 1 | 3,047 | 28.85% |

### Thống kê URL và SDT theo nhãn

| Label | has_url | has_phone_number | Count |
|---|---:|---:|---:|
| 0 | 0 | 0 | 2,739 |
| 0 | 0 | 1 | 913 |
| 0 | 1 | 0 | 987 |
| 0 | 1 | 1 | 681 |
| 1 | 0 | 0 | 634 |
| 1 | 0 | 1 | 670 |
| 1 | 1 | 0 | 3,155 |
| 1 | 1 | 1 | 783 |

Nhãn 1 chứa nhiều tin nhắn có URl hơn nhiều so với nhãn 0. Sự xuất hiện của URL trên thực tế đúng là một dấu hiệu mạnh của một tin nhắn lừa đảo, tuy nhiên điều này cũng là một con dao hai lưỡi nếu các mẫu URL có cấu trúc TÊN.ĐUÔI lặp lại nhiều lần xuyên suốt dữ liệu tạo sinh.

**Đây là điều bộ dữ liệu hiện tại đang gặp phải**

## 8. Thống kê độ dài tin nhắn theo nhãn và nguồn

| Label | Data origin | SL | Avg length | Min | P50 | P90 | Max |
|---|---|---:|---:|---:|---:|---:|---:|
| 0 | real | 2,321 | 228.9 | 2 | 227 | 362 | 916 |
| 0 | synthetic | 2,999 | 112.3 | 23 | 110 | 162 | 219 |
| 1 | real | 246 | 194.1 | 49 | 156 | 349 | 920 |
| 1 | synthetic | 4,996 | 117.5 | 12 | 110 | 182 | 298 |

Các tin nhắn tạo sinh có độ dài trung bình ngắn hơn cũng như phân phối độ dài tin nhắn hẹp hơn so với các mẩu tin nhắn thật. **Đây cũng là một shortcut tiềm năng khiến mô hình hiểu sai.**

## 10. Kết luận rút ra

1. Bộ dữ liệu nhìn chung đã cân bằng về nhãn, tuy nhiên tạo sinh dữ liệu dẫn đến mất cân bằng nghiêm trọng về nguồn. Điều này khiến độ cân bằng nhãn tổng thể trở nên dễ gây hiểu nhầm: dataset cân bằng về `label`, nhưng không cân bằng về bản chất dữ liệu.

2. Dữ liệu nhãn 1 phụ thuộc gần như hoàn toàn vào dữ liệu tạo sinh: chỉ 246/5,246 mẫu label 1 là dữ liệu thật, tương đương 4.69%. Do đó, mô hình huấn luyện trên random split có nguy cơ học đặc trưng của dữ liệu tạo sinh label 1 thay vì học đặc trưng tổng quát của tin nhắn lừa đảo.

3. Tập real label 1 quá nhỏ để đại diện đầy đủ cho không gian positive class. Điều này làm cho các kết quả đánh giá trên validation/test trộn synthetic có thể cao nhưng chưa đủ chứng minh khả năng tổng quát hóa trên dữ liệu thật.

4. Các mẫu tạo sinh có độ dài ngắn hơn và phân phối độ dài hẹp hơn nhiều so với mẫu thật ở cả hai nhãn. Đây là một shortcut tiềm năng: mô hình có thể học khác biệt về độ dài hoặc phong cách sinh dữ liệu thay vì nội dung ngữ nghĩa.

5. Sự xuất hiện của URL có liên hệ mạnh với nhãn 1, đặc biệt là trong dữ liệu tạo sinh: 3,760/5,000 mẫu synthetic label 1 có URL. URL là tín hiệu hợp lý trong bài toán phát hiện lừa đảo, nhưng nếu tên miền/cú pháp URL bị lặp nhiều thì nó sẽ là artifact của quá trình tạo sinh.

6. Nhãn 0 có tỷ lệ real cao hơn nhiều so với nhãn 1: 2,321/5,320 mẫu label 0 là real, tương đương 43.63%. Vì vậy, có thể tồn tại sự khác biệt không mong muốn giữa hai nhãn: label 0 mang nhiều đặc trưng real hơn, còn label 1 mang nhiều đặc trưng synthetic hơn. Đây là một dạng confounding giữa `label` và `data_origin`.

7. Một số category positive có số lượng rất đều nhau, ví dụ `Nội dung nhạy cảm`, `Cờ bạc / Betting`, `Crypto / Đầu tư giả`, `Tuyển dụng giả`, `BHXH / Trợ cấp`. Sự đều đặn này phản ảnh việc dữ liệu được tạo theo quota/prompt template.

8. Category `Khác` không cân bằng giữa hai nhãn: label 0 có 507 mẫu, trong khi label 1 chỉ có 46 mẫu. Điều này cho thấy label 1 được tổ chức theo các nhóm lừa đảo cụ thể hơn, còn label 0 có vùng nội dung rộng và phân tán hơn. --> **Do số lượng dữ liệu thật ban đầu đã có sự chênh lệch rất lớn (tỉ lệ xấp xỉ 1:8)**

9. Category label 0 và label 1 gần như tách biệt về mặt tên gọi: label 0 gồm các nhóm hợp lệ như `Ngân hàng thật`, `Dịch vụ công thật`, `Vận chuyển`, `Thương mại điện tử`; label 1 gồm các nhóm rủi ro như `Giả mạo ngân hàng`, `Cờ bạc / Betting`, `Tuyển dụng giả`. Nếu category hoặc dấu hiệu category bị phản ánh quá trực tiếp trong câu chữ, mô hình có thể học phân biệt domain/category thay vì học hành vi lừa đảo ở mức sâu hơn. **Cân xem xét kĩ hơn**

10. Đã phát hiện sự không nhất quán trong cách gọi tên category, ví dụ khác biệt dấu phân tách, dấu tiếng Việt, hoặc cách đảo thứ tự cụm từ. Việc tạo cột `category_normalized` là cần thiết để thống kê, phân tích và chia dữ liệu ổn định hơn, đồng thời vẫn giữ cột `category` gốc để truy vết. **Đã xử lý**

11. Từ các dấu hiệu trên, random split không nên được dùng làm phương thức đánh giá chính. Các kết quả từ random split chỉ nên được xem như baseline nội bộ hoặc diagnostic, vì train/validation có khả năng cùng chia sẻ đặc trưng tạo sinh.

12. Phương thức đánh giá chính nên bổ sung ít nhất hai thiết lập: real-only evaluation để đo khả năng tổng quát hóa trên dữ liệu thật, và template-holdout evaluation để kiểm tra mô hình có phụ thuộc vào pattern/template của dữ liệu tạo sinh hay không.

**Đã thử triển khai real-only evalutaion**
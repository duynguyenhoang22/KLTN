# RQ4: Knowledge distillation có giúp TextCNN nhẹ hơn đạt trade-off tốt hơn không?

RQ4 đánh giá liệu soft label từ các teacher Transformer có giúp cùng một student TextCNN cải thiện so với hard-label baseline hay không. Ba teacher được khảo sát gồm PhoBERT-base, CafeBERT và ViCLSR. Với mỗi teacher, TextCNN được huấn luyện theo ba chế độ: `hard`, `vanilla_kd` và `risk_aware_kd`. Kết quả được tổng hợp qua ba seed và so sánh bằng paired bootstrap trên tập test.

## 1. Hiệu quả distillation phụ thuộc vào teacher và chiến lược dùng soft label

Bảng RQ4.1 tóm tắt chênh lệch trên test giữa từng cấu hình KD và TextCNN hard baseline trong cùng teacher study. Vì mục tiêu của smishing detection là giảm bỏ sót tin lừa đảo, Recall Label 1 được dùng làm tiêu điểm phân tích.

**Bảng RQ4.1: Chênh lệch Recall Label 1 trên test so với TextCNN hard baseline**

| Teacher | Chế độ KD | Delta Recall Label 1 | Diễn giải |
| :--- | :--- | :---: | :--- |
| PhoBERT-base | Vanilla KD | +0,0093 | Tăng rất nhẹ, chưa đủ rõ. |
| PhoBERT-base | Risk-aware KD | **+0,0900** | Tăng recall rõ nhất; CI 95% nằm trên 0. |
| CafeBERT | Vanilla KD | +0,0185 | Có xu hướng cải thiện nhẹ. |
| CafeBERT | Risk-aware KD | **-0,0723** | Làm giảm recall rõ rệt. |
| ViCLSR | Vanilla KD | **-0,0898** | Làm giảm recall. |
| ViCLSR | Risk-aware KD | **-0,0633** | Vẫn thấp hơn hard baseline. |

Với PhoBERT-base, `vanilla_kd` gần như không cải thiện Recall Label 1, trong khi `risk_aware_kd` tăng recall khoảng +0,09 trên test. Đây là kết quả có ý nghĩa nhất trong RQ4 vì CI 95% của delta recall nằm hoàn toàn trên 0. Cách diễn giải hợp lý là PhoBERT-base không phải teacher mạnh nhất, nên dùng soft label đồng đều dễ truyền cả tín hiệu sai sang student. Khi áp dụng risk-aware weighting, các mẫu teacher không đáng tin được giảm ảnh hưởng, giúp TextCNN giữ hard-label supervision làm neo chính và chỉ tận dụng soft signal ở những trường hợp phù hợp.

Với CafeBERT, xu hướng ngược lại xuất hiện. CafeBERT là teacher mạnh nhất trong ba teacher, nhưng `risk_aware_kd` lại làm giảm Recall Label 1 khoảng -0,0723. Trong khi đó, `vanilla_kd` cho xu hướng cải thiện nhẹ. Kết quả này cho thấy risk-aware weighting không phải lúc nào cũng tốt: nếu teacher đủ mạnh và soft label chứa thông tin hữu ích về decision boundary, việc giảm trọng số theo heuristic có thể làm mất tín hiệu cần thiết cho student.

ViCLSR là trường hợp phản chứng quan trọng. Mặc dù ViCLSR có chất lượng teacher output không thấp, cả `vanilla_kd` và `risk_aware_kd` đều làm giảm Recall Label 1 so với hard baseline. Điều này cho thấy chất lượng teacher là điều kiện cần nhưng không đủ; soft label còn phải tương thích với kiến trúc student, loss và phân phối lỗi. Vì vậy, không thể suy luận rằng teacher tốt hơn sẽ luôn tạo student distilled tốt hơn.

Từ phân tích này, kết luận chính là distillation không phải một cải thiện mặc định. Với PhoBERT-base, risk-aware KD là lựa chọn tốt nhất; với CafeBERT, vanilla KD phù hợp hơn; với ViCLSR, hard-label TextCNN ổn định hơn cả hai biến thể KD.

## 2. Trade-off triển khai: TextCNN nhẹ là do kiến trúc, KD chỉ thay đổi chất lượng dự đoán

Để đánh giá ý nghĩa triển khai, cấu hình PhoBERT-base được dùng làm đại diện vì đã có phép đo CPU cho các TextCNN student. Bảng RQ4.2 trình bày kích thước, latency và F1 Label 1 của các cấu hình liên quan.

**Bảng RQ4.2: Trade-off triển khai của PhoBERT-base và các TextCNN student**

| Mô hình | Tham số | Kích thước (MB) | Latency CPU (ms/tin) | Throughput (tin/s) | F1 Label 1 |
| :--- | :---: | :---: | :---: | :---: | :---: |
| PhoBERT-base | 134.999.810 | 514,98 | N/A | N/A | 0,8267 |
| TextCNN hard | 87.553 | 0,342 | 2,19 | 566,46 | 0,8378 |
| TextCNN vanilla KD | 87.553 | 0,342 | 2,43 | 602,23 | 0,7692 |
| TextCNN risk-aware KD | 87.553 | 0,342 | 1,42 | 902,58 | 0,8500 |

Kết quả này cần được diễn giải tách bạch giữa hai nguồn lợi ích. TextCNN nhỏ và nhanh hơn PhoBERT-base là do kiến trúc cấp ký tự, không phải do distillation. Distillation không làm giảm số tham số, vì cả ba cấu hình TextCNN đều có cùng số tham số xấp xỉ 87,5 nghìn và kích thước khoảng 0,342 MB. Nói cách khác, KD chỉ thay đổi chất lượng dự đoán của cùng một student, còn lợi thế triển khai đến từ việc chọn student nhẹ.

Trong cấu hình đại diện này, TextCNN risk-aware KD đạt F1 Label 1 cao nhất trong nhóm đo deployment (0,8500), đồng thời có latency CPU khoảng 1,42 ms/tin. TextCNN hard cũng đã có F1 Label 1 cao hơn PhoBERT-base trong phép đo này (0,8378 so với 0,8267), cho thấy student nhẹ có thể cạnh tranh tốt nếu dữ liệu và huấn luyện phù hợp. Ngược lại, TextCNN vanilla KD là phản ví dụ quan trọng: cùng kiến trúc nhẹ nhưng F1 Label 1 giảm xuống 0,7692. Điều này củng cố kết luận rằng chiến lược dùng soft label quyết định chất lượng của student distilled.

Tóm lại, RQ4 cho thấy knowledge distillation là một kỹ thuật có điều kiện. Nó có thể giúp TextCNN nhẹ cải thiện recall và giữ chi phí suy luận thấp khi teacher và chiến lược KD phù hợp, nhưng cũng có thể làm giảm hiệu năng nếu soft target không tương thích với student. Vì vậy, mọi mô hình distilled cần được so sánh trực tiếp với hard-label baseline cùng kiến trúc, đặc biệt theo Recall Label 1 và F1 Label 1 thay vì chỉ theo Accuracy hoặc Macro-F1.

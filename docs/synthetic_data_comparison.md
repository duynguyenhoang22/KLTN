# So sánh dữ liệu tạo sinh Phase 1 và Phase 2

Tài liệu này đánh giá liệu các điều chỉnh ở Phase 2 có làm giảm những hạn chế
đã được phát hiện trong dữ liệu Phase 1 hay không. Phạm vi đánh giá tập trung vào
ba vấn đề mục tiêu:

1. mật độ leet và biến dạng ký tự quá cao trong dữ liệu smishing tạo sinh;
2. mức độ tương đồng và lặp kịch bản cao giữa các mẫu;
3. nguồn và miền nội dung của dữ liệu Label 0 còn hạn chế.

Hai phiên bản dữ liệu được sử dụng là:

1. [Phase 1](../data/reference/phase1/vismishds_phase1_final.csv);
2. [Phase 2](../data/reference/phase2/vismish_phase2_final.csv).

Phase 2 là phiên bản được tái cấu trúc có chủ đích từ Phase 1, không phải một
lần tạo sinh độc lập. Vì vậy, các kết quả dưới đây được diễn giải như bằng chứng
đánh giá hiệu quả của từng biện pháp điều chỉnh, không phải như một phép so sánh
hai bộ dữ liệu độc lập.

## 1. Các thay đổi từ Phase 1 sang Phase 2

| Can thiệp | Quy mô và kết quả |
|---|---:|
| Paraphrase dữ liệu Label 1 | 4.343 mẫu đầu vào |
| Paraphrase thành công | 4.333 mẫu |
| Mẫu không thay đổi sau paraphrase | 10 mẫu |
| Thay nhóm synthetic Label 1 cũ bằng hard-positive thuộc kịch bản mới | khoảng 650 mẫu cũ được thay bằng 653 mẫu mới |
| Loại bớt synthetic Label 0 | 1.001 mẫu |
| Bổ sung dữ liệu Label 0 từ ViLexNorm | 1.001 mẫu |
| Tổng số mẫu của mỗi phiên bản | 10.562 mẫu |

Thành phần Label 1 có nguồn gốc tạo sinh trong Phase 2 gồm 4.333 mẫu
`paraphrased`, 653 mẫu `synthetic_hard_positive` và 10 mẫu `synthetic` không
thay đổi sau paraphrase. Tổng số mẫu của nhóm này vẫn là 4.996, bằng với số mẫu
synthetic Label 1 trong Phase 1.

Thành phần Label 0 thay đổi từ 2.999 mẫu synthetic trong Phase 1 thành 1.998
mẫu synthetic và 1.001 mẫu dữ liệu bổ sung từ ViLexNorm trong Phase 2. Số mẫu
real Label 0 được giữ nguyên ở mức 2.321.

## 2. Giảm leet và biến dạng ký tự quá mức

Quan sát Phase 1 cho thấy leet xuất hiện với mật độ cao và thường được áp dụng
trên nhiều token trong cùng một tin nhắn. Điều này có thể tạo ra dấu hiệu bề mặt
quá rõ giữa dữ liệu smishing và dữ liệu hợp lệ, làm tăng nguy cơ mô hình học lối
tắt thay vì học hành vi lừa đảo.

| Chỉ số trên nhóm Label 1 có nguồn gốc tạo sinh | Phase 1 | Phase 2 | Thay đổi |
|---|---:|---:|---:|
| Tỷ lệ mẫu có leet | 82,45% | 72,78% | -9,67 điểm phần trăm |
| Tỷ lệ token leet | 18,87% | 4,91% | -13,96 điểm phần trăm |
| Mật độ leet trung bình | 0,2700 | 0,0671 | -0,2029 |

Tỷ lệ token leet giảm tương đối khoảng 73,98%, trong khi tỷ lệ mẫu có ít nhất
một dấu hiệu leet chỉ giảm 9,67 điểm phần trăm. Chênh lệch này cho thấy Phase 2
không loại bỏ hoàn toàn leet mà chủ yếu làm giảm cường độ biến dạng trong từng
tin nhắn. Kết quả phù hợp với mục tiêu giữ lại các trường hợp che giấu có kiểm
soát nhưng hạn chế hiện tượng nhiều token bị biến dạng một cách dày đặc.

Các chỉ số này mô tả tần suất biểu hiện bề mặt. Chúng không tự xác định liệu một
biến đổi ký tự có thật sự được thực hiện với chủ ý che giấu hay chỉ là hiện tượng
văn bản phi chuẩn.

## 3. Giảm mức độ tương đồng và lặp kịch bản

Để đánh giá hiện tượng nhiều mẫu có nội dung gần nhau, hai nhóm chỉ số được sử
dụng:

- độ tương đồng cosine với láng giềng gần nhất trong không gian embedding;
- mức lặp của các chuỗi 5-gram và 6-gram.

| Chỉ số trên nhóm Label 1 có nguồn gốc tạo sinh | Phase 1 | Phase 2 | Thay đổi |
|---|---:|---:|---:|
| Mean nearest-neighbor similarity | 0,9533 | 0,9273 | -0,0260 |
| Median nearest-neighbor similarity | 0,9621 | 0,9288 | -0,0333 |
| Tỷ lệ NN similarity ≥ 0,90 | 92,73% | 76,68% | -16,05 điểm phần trăm |
| Tỷ lệ NN similarity ≥ 0,95 | 63,17% | 27,48% | -35,69 điểm phần trăm |
| Mức lặp 5-gram | 0,6008 | 0,4873 | -0,1135 |
| Mức lặp 6-gram | 0,5202 | 0,3951 | -0,1251 |

Sau khi paraphrase và thay thế nhóm hard-positive, cả độ tương đồng
nearest-neighbor lẫn mức lặp n-gram dài đều giảm. Đáng chú ý, tỷ lệ mẫu có láng
giềng gần nhất với similarity từ 0,95 trở lên giảm từ 63,17% xuống 27,48%.
Kết quả này cho thấy Phase 2 có ít cặp mẫu gần trùng nhau hơn và ít tái sử dụng
các chuỗi từ dài hơn Phase 1.

Các chỉ số trên cung cấp bằng chứng rằng mức độ lặp bề mặt và mức tập trung của
các mẫu trong không gian embedding đã giảm. Tuy nhiên, chúng không chứng minh
rằng mọi mẫu Phase 2 đều có kịch bản độc lập, cũng không trực tiếp đo tính đúng
nhãn, tính hợp lý hoặc mức độ chân thực của nội dung.

## 4. Đa dạng hóa nguồn dữ liệu Label 0

| Nguồn Label 0 | Phase 1 | Phase 2 |
|---|---:|---:|
| Real | 2.321 | 2.321 |
| Synthetic | 2.999 | 1.998 |
| ViLexNorm/external | 0 | 1.001 |
| Tổng | 5.320 | 5.320 |

Việc thay 1.001 mẫu synthetic Label 0 bằng dữ liệu ViLexNorm làm giảm tỷ trọng
dữ liệu tạo sinh và bổ sung một nguồn văn bản bên ngoài vào lớp hợp lệ. Thay đổi
này trực tiếp làm đa dạng nguồn gốc và hiện tượng văn bản của Label 0.

Do ViLexNorm không hoàn toàn tương đương với phân phối SMS hợp lệ thực tế, kết
quả không được diễn giải thành bằng chứng rằng Phase 2 đã gần dữ liệu SMS thật
hơn. Lợi ích chính được ghi nhận ở đây là giảm sự phụ thuộc vào một nguồn tạo
sinh duy nhất và mở rộng phạm vi các biến thể văn bản phi chuẩn.

## 5. Kết luận

Phase 2 được xây dựng để xử lý ba hạn chế cụ thể của Phase 1: leet quá dày đặc,
mức lặp cao trong dữ liệu smishing tạo sinh và sự phụ thuộc lớn vào dữ liệu
synthetic ở Label 0.

Kết quả định lượng cho thấy:

1. tỷ lệ token leet giảm từ 18,87% xuống 4,91%;
2. tỷ lệ nearest-neighbor similarity từ 0,95 trở lên giảm từ 63,17% xuống
   27,48%;
3. mức lặp 5-gram giảm từ 0,6008 xuống 0,4873 và mức lặp 6-gram giảm từ
   0,5202 xuống 0,3951;
4. 1.001 mẫu synthetic Label 0 được thay bằng dữ liệu ViLexNorm;
5. khoảng 650 mẫu synthetic Label 1 cũ được thay bằng 653 hard-positive thuộc
   các kịch bản mới.

Những kết quả này cung cấp bằng chứng mô tả rằng các hạn chế mục tiêu của Phase
1 đã được giảm bớt trong Phase 2. Phạm vi kết luận không bao gồm khẳng định
Phase 2 tốt hơn trên mọi chiều, có chất lượng hoàn hảo hoặc chắc chắn cải thiện
hiệu năng mô hình.
# Phân tích lỗi FP/FN cho các setup A, B, E và G

## Mục tiêu

Phân tích lỗi thủ công được thực hiện nhằm bổ sung diễn giải định tính cho các kết quả định lượng của nhóm thí nghiệm TSTR/augmentation. Thay vì chỉ báo cáo Macro-F1, F1 Label 1, Precision, Recall và AUPRC, phần này xem xét các trường hợp mô hình dự đoán sai để trả lời ba câu hỏi:

1. Baseline real-only thường sai ở loại tin nhắn nào?
2. Việc thêm synthetic Label 1 có làm thay đổi pattern FP/FN trên Real Test hay không?
3. Khi miền Label 0 được mở rộng trong Setup G, vì sao G0 tạo nhiều false positive và vì sao G2 cải thiện rõ rệt?

Phân tích sử dụng các file prediction-level được sinh sau khi chạy lại Setup A, B, E và G. Mỗi dòng lỗi có `true_label`, `pred_label`, `prob_label1`, `error_type`, metadata và nội dung SMS. Các file tổng hợp nằm tại `setup_results/manual_error_analysis/`.

## Cách thực hiện

Toàn bộ các file `*_errors.csv` được gom lại thành `all_errors_labeled.csv`. Mỗi lỗi được gán thêm một nhãn nguyên nhân sơ bộ (`suggested_reason`) bằng rule dựa trên nội dung và metadata, ví dụ: tin hợp lệ có URL, tin hợp lệ giống tuyển sinh/tuyển dụng, tin hợp lệ dạng khuyến mãi/quà tặng, smishing bị viết giống OTP hoặc có obfuscation/leet.

Các nhãn này không được xem là ground truth tuyệt đối. Chúng đóng vai trò hỗ trợ review thủ công và giúp phát hiện pattern lỗi. Các mẫu cần đọc tay được lưu trong `manual_review_candidates.csv`; các lỗi lặp lại qua nhiều seed được lưu trong `stable_error_cases.csv`.

## Tổng quan số lỗi

| Setup / variant | Seed 42 | Seed 123 | Seed 2025 | Nhận xét |
|---|---:|---:|---:|---|
| A_real_only | 3 FN, 3 FP | 3 FN, 4 FP | 3 FN, 4 FP | Baseline ổn định, lỗi ít nhưng vẫn có các case khó lặp qua nhiều seed |
| B1_class_weight_default | 3 FN, 4 FP | 3 FN, 3 FP | 2 FN, 5 FP | Class weight không làm thay đổi pattern lỗi lớn |
| B2_class_weight_threshold | 3 FN, 6 FP | 3 FN, 3 FP | 2 FN, 7 FP | Threshold làm tăng FP ở một số seed |
| E4_all | 3 FN, 5 FP | 3 FN, 1 FP | 5 FN, 1 FP | Augmentation Label 1 giữ số lỗi thấp, nhưng trade-off giữa FP/FN dao động theo seed |
| G0_E4_champion | 4 FN, 44 FP | 2 FN, 45 FP | 3 FN, 27 FP | Lỗi chính là FP, đặc biệt trên external Label 0 |
| G2_external_curated | 5 FN, 1 FP | 3 FN, 4 FP | 3 FN, 6 FP | Giảm mạnh FP trên external; lỗi còn lại nằm ở real subset |

## Nhận xét theo nhóm setup

### Setup A/B: baseline real-only và class weighting

Setup A có số lỗi thấp trên Real Test, nhưng các lỗi lặp lại qua nhiều seed cho thấy một số mẫu vẫn nằm ở vùng khó của bài toán. Các FN ổn định thường là smishing có bề mặt giống tin hợp lệ hoặc không chứa tín hiệu lừa đảo rõ theo cách mô hình đã học. Ví dụ, một tin trúng thưởng qua shortcode Mobifone bị dự đoán là hợp lệ ở cả 3 seed; một tin OTP TNEX có URL bất thường cũng bị dự đoán là hợp lệ ở nhiều seed.

Các FP của Setup A thường rơi vào tin hợp lệ nhưng có bề mặt dễ giống smishing: tin tuyển sinh FPT có link Zoom và hotline, tin Google khôi phục tài khoản, tin ngân hàng/brandname có cảnh báo bảo mật hoặc mật khẩu khởi tạo. Điều này cho thấy mô hình không chỉ học nội dung lừa đảo, mà còn nhạy với các tín hiệu bề mặt như URL, hotline, brandname và thông báo bảo mật.

Setup B1 và B2 không tạo ra một pattern lỗi hoàn toàn mới. B1 giữ số lỗi gần với A. B2 có xu hướng tăng FP ở một số seed do threshold làm mô hình nhạy hơn với Label 1. Vì vậy, class weight/threshold có thể cải thiện recall nhưng cần được kiểm soát bằng precision và false positive rate.

### Setup E: Real Train + synthetic Label 1

Setup E4 là variant dùng toàn bộ synthetic Label 1 để augmentation. Số lỗi trên Real Test vẫn thấp, cho thấy việc thêm synthetic Label 1 không làm mô hình sụp đổ trên real distribution. Tuy nhiên, các lỗi còn lại cho thấy hai pattern đáng chú ý.

Thứ nhất, một số FN vẫn rất ổn định qua cả ba seed: tin OTP TNEX có URL bất thường, tin trúng thưởng Mobifone qua shortcode, và tin có obfuscation/leet như `MU0N KIEM`, `Tjen`, `ZAL0`. Đây là các mẫu mà ngay cả augmentation Label 1 vẫn chưa giúp mô hình nhận diện chắc chắn.

Thứ hai, FP của E4 chủ yếu là các tin hợp lệ có dấu hiệu bề mặt giống smishing: tuyển sinh/nhập học có hotline, link trường đại học, thông báo Google khôi phục tài khoản, hoặc tin dịch vụ viễn thông. Điều này phù hợp với trade-off của augmentation Label 1: mô hình được tăng độ nhạy với tín hiệu smishing, nhưng các tin hợp lệ có URL/hotline/brandname vẫn có thể bị kéo về Label 1.

### Setup G: external challenge và mở rộng miền Label 0

Setup G là phần có giá trị giải thích lỗi mạnh nhất. G0_E4_champion giữ recall Label 1 cao nhưng tạo rất nhiều FP trên challenge test: 44, 45 và 27 FP ở ba seed. Phần lớn FP của G0 nằm ở external Label 0, đặc biệt `external_curated` và `external_real`. Đây là bằng chứng định tính rõ cho vấn đề domain shift: mô hình đã học tốt smishing trong miền Real Test nhưng chưa đủ tiếp xúc với miền Label 0 mới.

Một điểm thú vị là nhiều FP external của G0 không phải SMS truyền thống, mà là các câu văn bản đời thường hoặc bình luận ngắn có số tiền, từ ngữ cảm xúc, hoặc cấu trúc khác với SMS brandname. Ví dụ các câu nói về vay tiền, lương, khách sạn, tiền học hoặc tranh chấp cá nhân bị dự đoán là smishing với xác suất rất cao. Điều này cho thấy G0 không chỉ nhạy với URL/hotline, mà còn thiếu ranh giới âm tính đủ rộng cho các dạng văn bản ngoài miền SMS hợp lệ ban đầu.

Khi chuyển sang G2_external_curated, các lỗi trên external subset biến mất ở cả ba seed; lỗi còn lại chỉ nằm ở real subset. Điều này là bằng chứng mạnh cho luận điểm augmentation cần đi theo hai phía: thêm synthetic Label 1 để tăng miền smishing, đồng thời thêm Label 0 đa dạng/curated để mô hình học ranh giới âm tính rộng hơn. Nói cách khác, synthetic Label 1 hữu ích, nhưng nếu không mở rộng miền Label 0 thì precision trên dữ liệu ngoài miền có thể giảm mạnh.

## Ví dụ lỗi tiêu biểu

Các ví dụ dưới đây được lấy trực tiếp từ `manual_review_candidates.csv`. Mục tiêu là minh họa pattern lỗi, không phải thay thế thống kê tổng hợp.

### False negative trên Real Test: smishing có bề mặt giống tin hợp lệ

Một lỗi FN ổn định ở nhiều setup là tin trúng thưởng qua shortcode Mobifone:

```text
Chuc mung ban da nhan duoc 1 chiec dien thoai E770i tu chuong trinh Quay So Ngau Nhien cua Mobifone. SoanTin: XU E770i31 va gui 4 lan den 6769 de xem chi tiet
```

Mẫu này bị dự đoán là Label 0 ở cả 3 seed của A, E4, G0 và G2. Đây là ví dụ điển hình cho smishing có bề mặt giống tin khuyến mãi/tổng đài hợp lệ: có thương hiệu quen thuộc, shortcode và không có URL độc hại rõ ràng. Mô hình vì vậy dễ xem nó là tin hợp lệ.

Một FN khác là tin OTP TNEX:

```text
TNEX Ma OTP cua ban 632900, se het han sau 2 phut. Vui long KHONG chia se ma cho bat ky ai voi bat ky ly do nao https//vi.ecmjJ7U4frh
```

Mẫu này cũng bị sai ổn định ở E4, G0 và G2. Về mặt nội dung, câu đầu giống hoàn toàn cảnh báo OTP hợp lệ; tín hiệu bất thường nằm ở phần URL bị viết thiếu chuẩn (`https//...`). Điều này cho thấy mô hình vẫn gặp khó với các mẫu smishing “núp” dưới văn phong bảo mật/OTP hợp lệ.

Một nhóm FN khác là tin có obfuscation/leet:

```text
Em la nu sinh vien 21 tuoi MU0N KIEM chut Tjen trang TRAI CU0C S0NG EM C0 the den lam tinh khu vuc nao cung DU0C GIA CA Uu DAI Add ZAL0 e: 0367891234 QkR
```

Mẫu này bị sai ở cả 3 seed của E4 và G2, và 2/3 seed của G0. Đây là lỗi đáng chú ý vì dữ liệu synthetic đã có obfuscation, nhưng mô hình vẫn có thể bỏ sót khi nội dung nằm ngoài các template smishing quen thuộc hoặc có cách viết quá nhiễu.

### False positive trên Real Test: tin hợp lệ có URL, hotline hoặc brandname

Một FP lặp lại qua nhiều setup là thông báo khôi phục tài khoản Google:

```text
Bạn đã yêu cầu Google khôi phục quyền truy cập cho duyj4f2004@gmail.com? Nếu không phải thì hãy kiểm tra email để tìm hiểu cách DỪNG yêu cầu này.
```

Mẫu này bị dự đoán là smishing ở cả 3 seed của A, E4, G0 và G2. Đây là tin hợp lệ nhưng có các đặc điểm giống cảnh báo bảo mật: tài khoản email, hành động khôi phục quyền truy cập và lời nhắc dừng yêu cầu. Với dữ liệu smishing, các tín hiệu “tài khoản”, “khôi phục”, “bảo mật” thường gần với ngữ cảnh lừa đảo, nên mô hình bị kéo sang Label 1.

Một FP khác trong Setup A là tin tuyển sinh FPT có link Zoom và hotline:

```text
Chao Quy PH-HS da dang ky tham gia Hoi thao Hoi&Dap Tuyen sinh 2022 - Dai hoc FPT. Chuong trinh se bat dau luc 19:00 toi nay. Moi Quy PH-HS tham du bang duong link: https://us02web.zoom.us/j/84853187652 hoac Zoom ID: 848 5318 7652. Mat khau vao phong: FPT. Hotline (028) 7300 5588.
```

Mẫu này bị FP ở cả 3 seed của A và 2/3 seed của G2. Đây là ví dụ rõ cho tin hợp lệ nhưng có tổ hợp tín hiệu dễ gây nhầm: URL, hotline, mã phòng, mật khẩu và brandname FPT. Những tín hiệu này cũng thường xuất hiện trong tin lừa đảo, nên mô hình khó phân biệt nếu không có đủ negative examples tương tự.

### False positive trên external Label 0 trong G0

G0_E4_champion tạo nhiều FP nhất trên external Label 0. Đáng chú ý, nhiều lỗi không phải SMS brandname truyền thống mà là câu đời thường/bình luận ngắn:

```text
mỗi tháng 20 trẹo: 5 trẹo lương cứng , 15 trẹo lương tâm
```

```text
Chơi vs nhau từ lơpd 3 đến khi lấy vợ, hơn 20 năm mà có 50tr bạn cũng đánh đổi
```

```text
Ko cho vay thì ngại cho vay oy tới lúc đòi thì sợ giận mà ko đòi ngta cg ko có suy nghĩ muốn trả mà kb lm tn
```

Các mẫu này bị G0 dự đoán là Label 1 ở cả 3 seed với xác suất rất cao. Chúng không chứa URL hoặc hotline theo kiểu SMS lừa đảo, nhưng có số tiền, từ ngữ đời thường, viết tắt/không chuẩn và nội dung liên quan đến vay tiền/lương/tranh chấp. Điều này cho thấy G0 thiếu negative coverage cho miền văn bản ngoài SMS hợp lệ ban đầu, nên ranh giới Label 0 quá hẹp.

Sau khi thêm external curated Label 0 trong G2, các lỗi external này biến mất ở cả 3 seed. Đây là ví dụ định tính mạnh nhất cho vai trò của Label 0 augmentation: không chỉ thêm positive synthetic, mà còn cần mở rộng miền negative để mô hình không đánh đồng mọi văn bản “bất thường” với smishing.

## Kết luận cho khóa luận

Phân tích FP/FN củng cố kết luận định lượng của Setup G: mô hình G0 đạt recall cao nhưng precision thấp trên challenge vì nhiều external Label 0 bị kéo sang Label 1. Việc bổ sung external curated Label 0 trong G2 giúp giảm mạnh false positive trên miền external, cho thấy vấn đề không nằm ở synthetic Label 1 một cách đơn lẻ, mà ở sự mất cân bằng miền giữa positive augmentation và negative coverage.

Với Setup A/B/E, lỗi trên Real Test ít về số lượng nên chỉ nên được dùng như phân tích minh họa. Các case lặp qua nhiều seed cho thấy các vùng khó gồm: smishing có bề mặt giống OTP/brandname/khuyến mãi hợp lệ, tin hợp lệ có URL/hotline/brandname, và tin có obfuscation/leet hoặc cách viết không chuẩn.

Do đó, kết luận thực nghiệm nên được trình bày như sau: dữ liệu tạo sinh có giá trị augmentation cho Label 1, nhưng cần được sử dụng có kiểm soát cùng với mở rộng miền Label 0. Phân tích lỗi cho thấy nếu chỉ tăng positive synthetic mà không bổ sung negative coverage tương ứng, mô hình có thể trở nên quá nhạy với các tín hiệu bề mặt và tạo nhiều false positive trên dữ liệu ngoài miền.

## Artefact đi kèm

- `all_errors_labeled.csv`: toàn bộ lỗi FP/FN của A/B/E/G kèm nhãn nguyên nhân sơ bộ.
- `stable_error_cases.csv`: các lỗi gộp theo nội dung/mẫu và số seed mắc lỗi.
- `manual_review_candidates.csv`: danh sách mẫu ưu tiên để đọc thủ công và chọn ví dụ đưa vào báo cáo.
- `error_summary_by_setup_seed.csv`: số FP/FN theo setup, variant, seed và subset.
- `error_summary_by_reason.csv`: số lỗi theo nhóm nguyên nhân gợi ý.
- `key_variant_error_counts.csv`: bảng tóm tắt lỗi cho các variant trọng tâm.

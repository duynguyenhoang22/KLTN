# Kết quả vòng Scope Challenge P0.1

Ngày phân tích: 2026-06-21  
Số mẫu: 50 real messages  
Annotator: 2, làm việc độc lập

## Kết quả agreement

| Độ đo | Kết quả |
|---|---:|
| Scope-decision agreement | 86,0% |
| Scope-decision Cohen's Kappa | 0,451 |
| Effective-outcome agreement | 76,0% |
| Effective-outcome Cohen's Kappa | 0,581 |
| Số mẫu cả hai cùng accept | 40 |
| Label agreement trong nhóm cùng accept | 87,5% |
| Label Cohen's Kappa trong nhóm cùng accept | 0,684 |
| Mẫu cần adjudication/review | 26 |
| Outcome disagreement trực tiếp | 12 |

`effective outcome` kết hợp quyết định phạm vi và label, ví dụ
`accepted_label_0`, `accepted_label_1`, `excluded_*` hoặc
`needs_adjudication`.

## Diễn giải

Hai annotator áp dụng khá nhất quán quyết định accept/exclude/adjudicate, nhưng
chưa đạt quality gate P0.1. Kappa label 0,684 trong nhóm cùng accept nằm sát
ngưỡng mục tiêu 0,70; effective-outcome Kappa 0,581 cho thấy policy vẫn còn
điểm dễ hiểu khác nhau.

Không sửa annotation độc lập ban đầu để tăng điểm. Các file đó là bằng chứng
về mức rõ ràng thực tế của guideline.

## Bất đồng có tính hệ thống

### 1. Có URL và chỉ có URL

Một annotator đã áp dụng quy tắc “chỉ có URL → Label 1” cho các thông báo đầy
đủ câu chữ nhưng có kèm URL. Điều này tạo bất đồng ở nhiều thông báo giao dịch,
gia hạn hoặc dịch vụ.

Scope đã được sửa thành RC2:

- toàn bộ nội dung chỉ là URL → Label 1;
- nội dung có câu chữ kèm URL → đánh giá toàn bộ nội dung;
- URL không tự động quyết định nhãn.

### 2. Đòi nợ và thông báo thanh toán

Heuristic tìm candidate ban đầu dùng tín hiệu tài chính quá rộng, làm một số
thông báo gia hạn/thanh toán rơi vào nhóm stress-test đòi nợ. Đây không phải
lỗi annotation, nhưng bộc lộ nhu cầu làm rõ:

- chỉ quy về Label 1 khi nội dung thực sự đòi nợ và có đe dọa/cưỡng ép;
- thông báo thanh toán, gia hạn hoặc giao dịch bình thường không áp dụng.

Heuristic đã được siết cho các lần lấy mẫu sau.

### 3. Malicious ngoài phạm vi và smishing

Nhóm quảng cáo cờ bạc/dịch vụ nhạy cảm có agreement thấp nhất. Hai cách hiểu
chính:

- quảng cáo malicious nhưng chưa có bằng chứng fraud → out of scope;
- mọi quảng cáo cờ bạc có hứa thưởng/link → Label 1.

Theo quyết định đã khóa của nhóm, chỉ malicious/non-fraud phải đi
`excluded_out_of_scope_malicious`. Buổi adjudication phải kiểm từng content xem
có bằng chứng gian dối/chiếm đoạt hay chỉ quảng cáo hoạt động malicious.

### 4. Không sử dụng kiến thức ngoài content

Một số reason dựa vào giả định “thương hiệu hợp pháp” hoặc “link không có
brandname”. Hai cách này đều có nguy cơ dùng kiến thức ngoài nội dung.

Annotator không được xác minh domain/thương hiệu bên ngoài. Chỉ cấu trúc,
ngữ nghĩa và hành động thể hiện trong `content` được dùng để quyết định.

## Lỗi định dạng cần sửa

Annotator A có:

- 7 mẫu thiếu confidence;
- 3 trong số đó đồng thời thiếu reason.

Các ô này phải được bổ sung trước hoặc trong adjudication. Không thay đổi quyết
định độc lập ban đầu.

## Kết luận P0.1

Trạng thái cuối: **đã khóa ngày 2026-06-21**.

Adjudication đã có quyết định cuối cho đủ 26 mẫu:

- 17 `accepted` gồm 12 Label 0 và 5 Label 1;
- 8 `excluded_out_of_scope_malicious`;
- 1 `excluded_language_scope`.

Hai policy note phát sinh đều đã được phản ánh trong scope RC2:

- đánh giá toàn bộ ngữ cảnh, không auto-label theo brandname;
- có URL không đồng nghĩa Label 1.

Sau xác nhận của Annotator A:

- 7 confidence bị bỏ trống đã được khôi phục thành `high`;
- 6 rationale trống được ghi rõ là mẫu được đưa vào queue để thảo luận thêm,
  sau đó đã thống nhất quyết định cuối.

Validator cuối:

- 26/26 dòng adjudication hợp lệ;
- 0 lỗi quality gate;
- 2 policy note, đều đã được phản ánh trong scope RC2.

Scope được chuyển sang `2.0.0-locked`. Annotation độc lập ban đầu vẫn được giữ
nguyên để báo cáo agreement; việc bổ sung provenance chỉ diễn ra trong
adjudication sheet.

# Protocol adjudication — Scope Challenge P0.1

Đầu vào:

- `data/annotations/scope_challenge_adjudication.csv`
- `data/processed/scope_challenge_agreement_report.md`
- `docs/dataset_scope.md` phiên bản dùng khi adjudication: `2.0.0-rc2`

Trạng thái: hoàn tất; kết quả đã được dùng để khóa scope `2.0.0-locked`.

## Trước buổi adjudication

1. Annotator A bổ sung các ô `confidence` và `reason` còn trống.
2. Cả hai đọc phần làm rõ quy tắc URL/SĐT và đòi nợ trong scope RC2.
3. Không mở legacy label/category như căn cứ quyết định.

## Cách xử lý queue

Hai người cùng xem từng dòng và điền:

- `final_scope_decision`
- `final_label`
- `adjudication_reason`
- `scope_policy_change_required`

`final_label` chỉ điền `0` hoặc `1` khi final decision là `accepted`.

`scope_policy_change_required`:

- `0`: scope RC2 đã đủ để quyết định;
- `1`: cần bổ sung/sửa policy trước khi chốt mẫu.

## Thứ tự thảo luận

1. 12 mẫu có `outcome_disagreement`.
2. Mẫu một trong hai annotator đánh dấu `needs_discussion=1`.
3. Mẫu confidence thấp hoặc thiếu.

Không quyết định theo đa số hay confidence cao hơn. Hai người phải chỉ ra quy
tắc scope và evidence trong `content`.

## Điểm cần kiểm tra đặc biệt

- “Chỉ có URL” không đồng nghĩa “có chứa URL”.
- Thông báo thanh toán/gia hạn không đồng nghĩa đòi nợ đe dọa.
- Không xác minh thương hiệu/domain bằng kiến thức ngoài `content`.
- Quảng cáo cờ bạc/dịch vụ nhạy cảm chỉ vào Label 1 khi có bằng chứng lừa đảo
  theo scope; nếu chỉ malicious/non-fraud thì out of scope.
- Nội dung không giải mã chắc chắn không được đoán nhãn từ category cũ.

## Điều kiện kết thúc

- Mọi dòng queue có quyết định cuối.
- Mọi quyết định có reason.
- Các dòng yêu cầu policy change đã được phản ánh vào scope.
- Chạy lại comparison/adjudication validator.
- Kappa/percent agreement được báo cáo lại sau adjudication, nhưng không được
  sửa annotation độc lập ban đầu để làm đẹp agreement.

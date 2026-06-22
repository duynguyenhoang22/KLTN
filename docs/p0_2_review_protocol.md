# Protocol review taxonomy P0.2

File:

- Reviewer A: `data/annotations/p0_2_taxonomy_review_a.csv`
- Reviewer B: `data/annotations/p0_2_taxonomy_review_b.csv`

Tài liệu tham chiếu:

- `docs/dataset_scope.md`
- `docs/annotation_guidelines.md`
- `docs/metadata_data_dictionary.md`
- `docs/p0_2_human_review_checklist.md`

## Cách review

Hai người làm độc lập. Với mỗi field/value, chọn đúng một `decision`:

- `accept`: giữ nguyên;
- `rename`: đổi tên nhưng giữ khái niệm;
- `merge`: nhập vào value khác;
- `split`: cần chia thành nhiều value;
- `remove`: không có giá trị phân tích hoặc không gán ổn định.

Nếu không `accept`, bắt buộc điền:

- `proposed_value_or_target`;
- `comment`.

Không yêu cầu điền ví dụ hoặc phản ví dụ trong review độc lập. Các ranh giới
khó và cách hiểu khác nhau sẽ được thảo luận ở bước adjudication sau khi so
sánh hai sheet.

## Câu hỏi review

1. Hai người có thể phân biệt value chỉ từ `content` không?
2. Value có độc lập với label không?
3. Value có đủ số mẫu tiềm năng để phân tích không?
4. Value có trùng hoặc bao hàm value khác không?
5. Value có yêu cầu suy diễn demographic không được phép không?
6. `unknown`, `other`, `not_applicable` có dùng đúng ý nghĩa không?

Không cần cố giải quyết mọi ca biên trong file review. Nếu một value có vẻ khó
gán nhưng chưa chắc cần đổi, chọn decision phù hợp nhất và ghi ngắn trong
`comment`; hệ thống sẽ đưa bất đồng A/B vào queue thảo luận.

## Sau review

Không sửa trực tiếp taxonomy trước khi so sánh hai sheet. Bước tiếp theo sẽ:

- tổng hợp tất cả non-accept decisions;
- phát hiện A/B bất đồng;
- tạo taxonomy adjudication sheet;
- thảo luận thêm định nghĩa và ví dụ chỉ cho các value bất đồng;
- cập nhật taxonomy/schema/guideline cùng lúc;
- chạy contract audit trước khi khóa.

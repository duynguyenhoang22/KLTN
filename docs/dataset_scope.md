# Phạm vi và chính sách nhãn của ViSmishDS v2

Phiên bản: `2.0.0-draft`  
Ngày ban hành bản nháp: 2026-06-20  
Trạng thái: P0.1 — cần human review trước khi khóa

## 1. Mục đích của tài liệu

Tài liệu này là hợp đồng phạm vi của ViSmishDS v2. Nó xác định:

- dataset đại diện cho loại dữ liệu nào;
- một bản ghi và một nhãn có ý nghĩa gì;
- mẫu nào được nhận, loại hoặc giữ lại để adjudication;
- cách xử lý dữ liệu thiếu ngữ cảnh và mơ hồ;
- vai trò không thể thay thế của con người;
- những kết luận nào không được suy rộng từ dataset.

Mọi annotation guideline, prompt, pipeline, split và thí nghiệm phải tuân theo
tài liệu này. Nếu định nghĩa thay đổi, phải tăng phiên bản và đánh giá lại các
mẫu đã gán.

## 2. Phát biểu phạm vi

ViSmishDS v2 là bộ dữ liệu phục vụ nghiên cứu phát hiện **tin nhắn văn bản
tiếng Việt có dấu hiệu smishing hoặc lừa đảo trực tiếp qua nội dung tin nhắn**.

Dataset tập trung vào nội dung ngắn tương tự SMS, gồm:

- SMS gửi từ số cá nhân, shortcode hoặc brandname;
- nội dung quảng bá/lừa đảo có hình thức tương tự SMS;
- văn bản tiếng Việt chuẩn hoặc phi chuẩn;
- tin nhắn có thể chứa URL, tên miền, số điện thoại hoặc lời kêu gọi chuyển
  sang nền tảng khác;
- tin nhắn hợp lệ có bề mặt gần với smishing để làm negative/hard negative.

Dataset không nhằm đại diện đầy đủ cho:

- mọi hình thức lừa đảo trực tuyến;
- email phishing dài;
- hội thoại mạng xã hội nhiều lượt;
- cuộc gọi lừa đảo, hình ảnh, mã QR hoặc tệp đính kèm nếu không có phần văn bản;
- toàn bộ dân số, vùng miền hoặc phương ngữ Việt Nam;
- ý định thật của người gửi khi nội dung không cung cấp đủ bằng chứng.

## 3. Đơn vị phân tích

### 3.1. Đơn vị chính

Một bản ghi là **một thông điệp văn bản độc lập** được đưa cho mô hình tại thời
điểm dự đoán.

Mỗi bản ghi có:

- một `sample_id` ổn định;
- một trường `content`;
- một nhãn nhị phân;
- provenance nguồn;
- metadata được gán từ chính nội dung và thông tin nguồn hợp lệ.

### 3.2. Tin nhắn nhiều đoạn

Nhiều dòng vẫn được xem là một bản ghi nếu chúng thuộc cùng một lần gửi hoặc
cùng một thông điệp gốc.

Không ghép các tin nhắn rời thành một mẫu chỉ để tạo thêm ngữ cảnh.

### 3.3. Hội thoại

Đoạn hội thoại nhiều lượt không thuộc phạm vi release chính. Nếu chỉ một lượt
được giữ lại, annotator phải đánh giá dựa trên lượt đó và không tự tưởng tượng
các lượt bị thiếu.

Nếu nhãn chỉ xác định được nhờ hội thoại ngoài bản ghi, mẫu phải được:

- giữ ở tập review với lý do `insufficient_context`; hoặc
- loại khỏi release phân loại một tin nhắn độc lập.

## 4. Định nghĩa nhãn

## 4.1. Label 1 — Smishing/lừa đảo

Gán Label 1 khi nội dung có đủ bằng chứng cho thấy thông điệp đang thực hiện
hoặc dẫn dắt một hành vi lừa đảo, chiếm đoạt, đánh cắp thông tin hoặc thao túng
người nhận thực hiện hành động gây rủi ro.

Các dấu hiệu có thể gồm:

- giả mạo cá nhân, thương hiệu hoặc cơ quan;
- yêu cầu cung cấp OTP, mật khẩu, thông tin định danh hoặc thông tin tài chính;
- dẫn đến website/kênh liên hệ đáng ngờ để xác thực, nhận thưởng hoặc xử lý sự cố;
- yêu cầu chuyển tiền, nạp tiền hoặc thanh toán bằng lý do gian dối;
- hứa việc làm, lợi nhuận, trợ cấp hoặc phần thưởng bất thường để dẫn dụ;
- đe dọa, gây sợ hãi hoặc tạo cấp bách nhằm ép hành động;
- tuyển mộ vào quy trình task scam, đầu tư giả hoặc hành vi chiếm đoạt tương tự.

Không yêu cầu mọi mẫu Label 1 phải có URL, số điện thoại, obfuscation hoặc lỗi
chính tả.

## 4.2. Label 0 — Không phải smishing

Gán Label 0 khi nội dung không thực hiện hành vi lừa đảo theo định nghĩa trên
và có đủ ngữ cảnh để xem là thông điệp hợp lệ hoặc không gây hại trong phạm vi
bài toán.

Label 0 có thể gồm:

- OTP hoặc cảnh báo bảo mật hợp lệ;
- thông báo ngân hàng, viễn thông, vận chuyển hoặc dịch vụ công hợp lệ;
- quảng cáo hợp lệ;
- tin nhắn cá nhân;
- tin chứa URL, hotline, deadline hoặc ngôn ngữ cảnh báo nhưng không có bằng
  chứng lừa đảo;
- hard negative có bề mặt giống smishing.

Label 0 không đồng nghĩa với “văn bản sạch”, “không có URL” hoặc “không có
obfuscation/noise”.

## 4.3. Không tạo Label 2 cho ca mơ hồ

Nhãn mô hình vẫn là nhị phân. Tuy nhiên, pipeline quản trị phải có trường quyết
định riêng:

- `accepted_label_0`;
- `accepted_label_1`;
- `needs_adjudication`;
- `excluded_insufficient_context`;
- `excluded_invalid_record`;
- `excluded_privacy_or_safety`;
- `excluded_duplicate`.

Ca mơ hồ không được ép vào Label 0 chỉ vì chưa chứng minh được Label 1.

## 5. Quy tắc ra quyết định nhãn

Annotator thực hiện theo thứ tự:

1. Nội dung có đủ để hiểu thông điệp đang yêu cầu/đề nghị điều gì không?
2. Có bằng chứng trực tiếp về hành vi lừa đảo hoặc dẫn dắt đến rủi ro không?
3. Bằng chứng đó nằm trong nội dung/provenance được phép sử dụng hay đến từ suy
   đoán bên ngoài?
4. Có cách giải thích hợp lệ và hợp lý ngang bằng với cách giải thích lừa đảo
   không?
5. Nếu hai cách giải thích vẫn cạnh tranh, chuyển adjudication thay vì ép nhãn.

Các tín hiệu sau **không đủ một mình** để gán Label 1:

- có URL hoặc tên miền lạ;
- có số điện thoại;
- viết hoa, sai chính tả, bỏ dấu, teencode hoặc leetspeak;
- tạo cảm giác cấp bách;
- đề cập ngân hàng, tiền, OTP, trúng thưởng hoặc cơ quan nhà nước;
- được sinh bởi LLM;
- category cũ mang chữ “giả”;
- model/judge dự đoán Label 1 với confidence cao.

## 6. Inclusion policy

Một mẫu được đưa vào candidate pool khi:

- có nội dung văn bản đọc được ở mức tối thiểu;
- có provenance nguồn;
- phù hợp hình thức SMS hoặc short-message;
- chủ yếu là tiếng Việt, hoặc code-switching nhưng tiếng Việt vẫn có vai trò
  đủ lớn để phân tích;
- nhãn có thể được đánh giá từ thông tin được phép sử dụng;
- không phải exact duplicate của mẫu đã chọn;
- không vi phạm chính sách dữ liệu nhạy cảm của dự án.

Synthetic chỉ được xem là **candidate data**, không tự động là ground truth.

## 7. Exclusion policy

Loại khỏi release chính khi:

- nội dung rỗng, hỏng encoding hoặc chỉ gồm ký tự không thể diễn giải;
- là email dài, bài đăng dài hoặc hội thoại nhiều lượt ngoài phạm vi;
- nhãn phụ thuộc hoàn toàn vào ngữ cảnh không có trong bản ghi;
- không xác định được provenance tối thiểu;
- exact duplicate hoặc bản sao chỉ khác khoảng trắng;
- chứa thông tin cá nhân nhạy cảm không thể khử định danh an toàn;
- synthetic bị lỗi logic, mâu thuẫn, placeholder hoặc artifact nghiêm trọng;
- văn bản không có đủ thành phần tiếng Việt cho mục tiêu nghiên cứu;
- có tranh chấp nhãn không thể adjudicate với bằng chứng hiện có.

Mẫu bị loại vẫn phải có exclusion record; không xóa im lặng.

## 8. Xử lý ca mơ hồ và thiếu ngữ cảnh

### 8.1. `unknown`, `general`, `other` và `not_applicable`

- `unknown`: thuộc tính có thể tồn tại nhưng không đủ bằng chứng để xác định.
- `general`: nội dung rõ ràng hướng đến công chúng hoặc mọi người.
- `other`: xác định được giá trị nhưng taxonomy hiện tại không bao phủ.
- `not_applicable`: thuộc tính không có ý nghĩa đối với mẫu đó.

Không dùng `unknown` để che lỗi guideline hoặc tránh đưa ra quyết định có đủ
bằng chứng.

### 8.2. Ca biên bắt buộc adjudication

- thông báo đòi nợ có ngôn ngữ đe dọa nhưng chưa rõ gian dối;
- quảng cáo cờ bạc/dịch vụ nhạy cảm nhưng chưa thể hiện hành vi chiếm đoạt;
- tuyển dụng thu nhập cao nhưng không có bước dẫn dụ rõ;
- thông báo thương hiệu có URL lạ nhưng không thể xác minh nguồn;
- tin nhắn chỉ có link hoặc số điện thoại;
- nội dung có thể là spam nhưng chưa phải smishing;
- mẫu synthetic ghi Label 1 nhưng nội dung không thực hiện hành vi lừa đảo.

Spam, nội dung phi pháp hoặc nội dung khó chịu không tự động đồng nghĩa với
smishing. Nếu khóa luận muốn mở rộng Label 1 thành “malicious SMS” rộng hơn,
đó là thay đổi bài toán và phải ban hành phiên bản scope mới.

## 9. Phạm vi metadata nhóm đối tượng

Metadata nhóm đối tượng mô tả **đối tượng được nội dung biểu đạt là đang hướng
đến**, không mô tả chắc chắn người đã nhận tin.

Chỉ gán nhóm cụ thể khi có evidence trong nội dung, ví dụ:

- “sinh viên năm cuối” → trạng thái `student`;
- “người đã nghỉ hưu” → trạng thái `retired`, có thể hỗ trợ age group;
- “chị em phụ nữ” → gender `female`;
- “chủ shop” → occupation/life status phù hợp.

Không được suy diễn:

- tuyển dụng → người trẻ;
- trợ cấp → người cao tuổi;
- ngân hàng → người trưởng thành;
- cờ bạc → nam giới;
- nội dung nhạy cảm → một giới cụ thể;
- teencode → thanh thiếu niên.

Nếu thông điệp dùng “quý khách”, “bạn” hoặc không nêu nhóm cụ thể:

- dùng `general` nếu lời mời rõ ràng áp dụng rộng;
- dùng `unknown` nếu không thể xác định phạm vi;
- không tự gán nhóm tuổi/nghề nghiệp.

## 10. Vai trò của con người

## 10.1. Vì sao con người là bắt buộc

ViSmishDS xử lý các khái niệm có tính ngữ cảnh và chuẩn tắc:

- đâu là lừa đảo thay vì quảng cáo/spam;
- một biến đổi văn bản có phải cố ý che giấu hay chỉ là lỗi tự nhiên;
- bằng chứng có đủ để suy luận nhóm đối tượng hay không;
- một synthetic sample có hợp lý và trung thực với bối cảnh Việt Nam hay không;
- ca mơ hồ nên nhận nhãn nào hoặc nên bị loại.

Các quyết định này không thể được xác lập chỉ bằng regex, model confidence hoặc
đa số phiếu của LLM. Con người chịu trách nhiệm cuối cùng về ground truth.

## 10.2. Công việc con người không được giao hoàn toàn cho LLM

Con người bắt buộc:

1. Phê duyệt scope, label policy, taxonomy và guideline.
2. Gán độc lập pilot để kiểm tra khả năng áp dụng định nghĩa.
3. Adjudicate mọi bất đồng nhãn cốt lõi.
4. Review toàn bộ real Label 1 trong release đầu tiên.
5. Review mẫu thiếu ngữ cảnh, confidence thấp và judge bất đồng.
6. Quyết định giữ, sửa, loại hoặc tái sinh synthetic.
7. Phê duyệt evidence cho target audience cụ thể.
8. Phê duyệt exclusion vì privacy/safety.
9. Khóa dataset release và test split.
10. Chịu trách nhiệm về các kết luận được viết trong luận văn.

LLM không được tự nâng annotation của mình thành `human_reviewed` hoặc
`adjudicated`.

## 10.3. Việc LLM và công cụ tự động được hỗ trợ

LLM/công cụ có thể:

- đề xuất metadata và evidence span;
- phát hiện mẫu nghi ngờ, contradiction hoặc artifact;
- nhóm duplicate/near-duplicate;
- tạo review queue theo confidence;
- làm hai judge độc lập cho synthetic;
- kiểm schema và consistency;
- tính agreement và thống kê phân phối.

Mọi output tự động phải lưu:

- model/tool ID và version;
- prompt/rule version;
- timestamp;
- confidence;
- raw output hoặc checksum;
- trạng thái đã/chưa được con người duyệt.

## 10.4. Vai trò cụ thể trong quy trình

### Người thiết kế dữ liệu

- duy trì scope, schema và guideline;
- không tự ý thay định nghĩa sau khi xem kết quả benchmark;
- phân tích bias và coverage.

### Annotator

- gán dựa trên nội dung, không dựa category/level cũ;
- ghi evidence và uncertainty;
- chuyển ca không chắc sang adjudication.

### Adjudicator

- xem hai annotation độc lập và bằng chứng;
- đưa ra quyết định cuối hoặc loại mẫu;
- ghi lý do quyết định;
- đề xuất sửa guideline khi bất đồng có tính hệ thống.

### Người kiểm định synthetic

- review judge disagreement và high-severity failure;
- kiểm tra mẫu both-pass ngẫu nhiên;
- không sửa nội dung rồi giữ nguyên provenance như chưa từng thay đổi.

### Release owner

- kiểm quality gate;
- khóa manifest/checksum;
- bảo đảm không còn record chưa duyệt;
- ký xác nhận phiên bản dùng cho thí nghiệm và luận văn.

Một người có thể đảm nhiệm nhiều vai trò trong nhóm nhỏ, nhưng không nên tự gán
và tự adjudicate toàn bộ cùng một mẫu mà không có kiểm tra chéo.

## 10.5. Quy tắc hai người

Tối thiểu cần hai người tham gia ở các điểm:

- annotation pilot;
- thay đổi định nghĩa Label 0/1;
- adjudication ca biên có khả năng làm thay đổi guideline;
- khóa taxonomy;
- phê duyệt Dataset Release v2.

Nếu hai người vẫn bất đồng:

1. ghi lại hai lập luận;
2. kiểm tra bằng chứng nguồn;
3. tham vấn người thứ ba/cán bộ hướng dẫn nếu có;
4. nếu vẫn không giải quyết được, loại mẫu khỏi release chính.

## 11. Synthetic data policy

Synthetic không được dùng để định nghĩa thế nào là smishing. Định nghĩa phải
đến từ scope, dữ liệu thực, tài liệu chuyên môn và quyết định của con người.

Một mẫu synthetic chỉ được nhận khi:

- phù hợp label policy;
- qua schema validation;
- qua hai judge độc lập;
- qua human audit theo protocol;
- không thuộc family/template bị rò rỉ sang test;
- có provenance generator, prompt và version.

Nhãn/metadata do generator trả về là `generated claim`, không phải verified
ground truth.

## 12. Privacy và đạo đức dữ liệu

Con người phải kiểm tra các trường hợp chứa:

- số điện thoại cá nhân;
- tên và định danh cá nhân;
- số tài khoản, CCCD/CMND;
- địa chỉ hoặc thông tin người bị đòi nợ;
- nội dung nhạy cảm có thể gây hại khi công bố.

Quyết định khử định danh phải giữ được tín hiệu nghiên cứu cần thiết nhưng
không giữ thông tin nhận dạng không cần thiết.

Dataset không được dùng để:

- tạo hoặc tối ưu tin nhắn lừa đảo triển khai thực tế;
- nhắm mục tiêu nhóm dễ tổn thương;
- khẳng định đặc điểm nhân khẩu học thật của người nhận;
- tự động cáo buộc cá nhân/tổ chức là lừa đảo mà không có xác minh phù hợp.

## 13. Nguồn dữ liệu trong phạm vi hiện tại

### Nguồn bất biến

- real Label 0 do dự án thu thập;
- real Label 1 do dự án thu thập;
- raw ViLexNorm dùng làm external candidate;
- snapshot Phase 1 dùng để migration và truy vết.

### Chưa phải release v2

- mọi synthetic Phase 1;
- metadata category/obfuscation legacy;
- external candidate chưa review;
- hard negative hoặc normalization output lịch sử.

Các nguồn “chưa phải release” chỉ được nhập lại thông qua pipeline v2.

## 14. Giới hạn diễn giải

Kết quả trên ViSmishDS v2 không tự động chứng minh:

- hiệu quả trên mọi SMS tại Việt Nam;
- hiệu quả trên mọi vùng miền, nhóm tuổi hoặc nghề nghiệp;
- khả năng phát hiện email phishing, cuộc gọi hoặc hình ảnh;
- quan hệ nhân quả giữa metadata và lỗi mô hình;
- tỷ lệ smishing ngoài đời thực;
- đặc điểm nhân khẩu học thật của nạn nhân.

Mọi lát cắt phải báo cáo số mẫu. Nhóm quá nhỏ chỉ được mô tả như quan sát hoặc
được gộp theo quy tắc công bố trước.

## 15. Quality gate để khóa P0.1

P0.1 chỉ hoàn thành khi:

- [ ] Hai thành viên đã đọc và phê duyệt scope.
- [ ] Có ít nhất 10 ví dụ Label 0, 10 ví dụ Label 1 và 10 ca biên.
- [ ] Hai người gán độc lập 50 ca khó bằng chính sách này.
- [ ] Mọi bất đồng được ghi và adjudicate.
- [ ] Định nghĩa spam, malicious SMS và smishing không còn nhập nhằng.
- [ ] Quy tắc `unknown/general/other/not_applicable` được đồng ý.
- [ ] Quy trình privacy/exclusion có người chịu trách nhiệm.
- [ ] Tài liệu được tăng từ `draft` sang phiên bản khóa.

## 16. Các quyết định con người cần chốt

Trước pilot chính thức, nhóm phải trả lời:

1. Quảng cáo cờ bạc hoặc dịch vụ nhạy cảm không có dấu hiệu chiếm đoạt có thuộc
   Label 1 không, hay nằm ngoài bài toán smishing?
2. Tin đòi nợ có đe dọa nhưng có thể đến từ chủ nợ thật được xử lý thế nào?
3. Spam thương mại gây khó chịu nhưng hợp pháp có luôn là Label 0 không?
4. Tin chỉ chứa một URL/số liên hệ có được giữ khi không đủ ngữ cảnh không?
5. Có cho phép sử dụng thông tin nguồn ngoài `content` để xác định nhãn không?
   Nếu có, chính xác những trường nguồn nào được phép?
6. External social-text khác hình thức SMS được dùng cho train, challenge hay
   chỉ phân tích domain shift?
7. Ngưỡng nào khiến một mẫu tiếng Việt pha tiếng Anh nằm ngoài phạm vi?

Các câu trả lời phải được ghi vào phiên bản khóa, không để annotator tự quyết
khác nhau.

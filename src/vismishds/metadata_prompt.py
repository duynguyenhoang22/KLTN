from __future__ import annotations

import json
from typing import Iterable

from .metadata_contract import metadata_output_schema
from .taxonomy import load_taxonomy


def build_system_prompt() -> str:
    taxonomy = load_taxonomy()
    allowed = {
        field: taxonomy[field]
        for field in (
            "message_domain",
            "text_phenomena",
            "target_age_group",
            "target_gender",
            "target_roles",
            "obfuscation_techniques",
            "persuasion_tactics",
            "requested_actions",
        )
    }
    return f"""
Bạn là annotator metadata cho tin nhắn tiếng Việt ViSmishDS.
Chỉ sử dụng content. Không xem label, nguồn dữ liệu, metadata cũ, hoặc tra cứu
tính xác thực của thương hiệu/domain.

## 1. Quy tắc output

- Trả duy nhất JSON object dạng {{"items": [...]}} đúng schema.
- Mỗi input sample_id có đúng một output; không bỏ sót, thêm hoặc đổi sample_id.
- Chỉ dùng enum đúng chính tả trong ALLOWED_ENUMS; không tự tạo value.
- Evidence là đoạn ngắn xuất hiện nguyên văn trong content đã mask.
- Placeholder <PHONE_n>, <EMAIL_n>, <IDENTIFIER_n>, <PERSON_NAME_n> không phải
  text noise hay obfuscation.
- Không gán sender_type, label, has_url hoặc has_phone_number.

## 2. Message domain — chọn hoạt động chính, không chọn campaign owner

Ưu tiên domain nghiệp vụ chuyên biệt hơn marketing_promotion:
- data, gói cước, thuê bao, nạp thẻ nhà mạng → telecom;
- tài khoản, thẻ, OTP tài chính, ví, giao dịch, hóa đơn tài chính → banking_finance;
- mua bán sản phẩm/dịch vụ → commerce;
- vận đơn, giao/nhận hàng → logistics;
- thuế, pháp luật, công an, BHXH, hành chính → public_service;
- tuyển dụng/công việc → employment;
- crypto, forex, trading, đầu tư vốn/lợi nhuận → investment;
- khoản vay/thu hồi nợ → debt_collection;
- casino, slot, cá cược, game bài, nạp-rút/thưởng gắn trò chơi → gambling;
- dịch vụ tình dục, gái xinh, body, massage/hẹn hò thương mại → adult_service.

Chỉ dùng marketing_promotion khi thông điệp là quảng cáo/ưu đãi chung và không
có domain chuyên biệt. Không đổi adult_service hoặc gambling thành
marketing_promotion chỉ vì content mang hình thức quảng cáo. Dùng other khi
nội dung hiểu được nhưng thật sự ngoài taxonomy; dùng unknown khi không đủ nội
dung để biết domain.

## 3. Text phenomena và noise — phân loại mọi lỗi chính tả và xác định mức độ nhiễu

- **Danh sách hiện tượng bề mặt (text_phenomena):** Gán mọi hiện tượng quan sát được trong văn bản. Không tự động quy kết lỗi chính tả là che giấu (obfuscation).
  + Bắt buộc gán `diacritic_omission` nếu văn bản viết tiếng Việt không dấu (ví dụ: `tai khoan cua ban`, `quy khach`).
  + Bắt buộc gán `abbreviation` nếu văn bản chứa bất kỳ từ viết tắt nào, kể cả các từ thông dụng: `QK` (Quý khách), `LH` (liên hệ), `CSKH` (chăm sóc khách hàng), `TB` (thông báo), `QC` (quảng cáo), `TK` (tài khoản), `GD` (giao dịch), `OTP`, `VND`, `SMS`, `KM` (khuyến mãi), `KHTT`, `APP`, `gplx`...
  + Bắt buộc gán `irregular_casing` nếu văn bản viết hoa toàn bộ từ để nhấn mạnh (ví dụ: `CHỈ 5K`, `ĐẶC BIỆT`, `ĐĂNG KÝ`) hoặc dùng kiểu chữ xen kẽ hoa thường trong tên thương hiệu/dịch vụ (`ViettelPay`, `MyViettel`, `VinaPhone`, `Messenger`).
  + Bắt buộc gán `teencode` cho các từ chat thông dụng: `ko`, `k`, `j`, `zậy`, `ae` (anh em)...
  + Nếu văn bản được viết hoàn toàn bằng tiếng Việt chuẩn có dấu đầy đủ, không có từ viết tắt nào, và không viết hoa bất thường $\rightarrow$ Gán duy nhất giá trị "none" (không để trống).

- **Quy tắc gán chỉ số nhiễu (text_noise_score):**
  + **Gán 0 (Chuẩn/Gần chuẩn):** Chỉ dùng khi văn bản viết bằng tiếng Việt chuẩn hoàn toàn có dấu, không có từ viết tắt, không có lỗi chính tả và không có chữ hoa bất thường.
  + **Gán 1 (Nhẹ):** Dùng ngay khi văn bản viết tiếng Việt không dấu (`diacritic_omission`) hoặc có từ viết tắt thông dụng (`abbreviation`) nhưng vẫn đọc hiểu bình thường ngay lập tức.
  + **Gán 2 (Trung bình):** Nhiều hiện tượng teencode, viết tắt, hoặc chèn ký tự xen kẽ nhưng nghĩa vẫn rõ ràng.
  + **Gán 3 (Nặng):** Độ nhiễu cao, chen dấu/khoảng trắng phức tạp hoặc viết tắt quá nhiều, cần khôi phục đáng kể để hiểu nghĩa.
  + **Gán 4 (Cực đoan):** Bị biến đổi cực đoan, hầu như không thể đọc hiểu bình thường.

## 4. Target audience — gán nhãn dựa trên ngữ cảnh giao tiếp và cách xưng hô trong tin nhắn

Target audience mô tả nhóm người nhận mà nội dung hướng tới, dựa trên ngữ cảnh giao tiếp, xưng hô và bằng chứng (evidence) cụ thể trong văn bản. Phải tuân thủ nghiêm ngặt quy trình quyết định và các quy tắc cưỡng chế sau:

### Quy trình quyết định 2 bước:
- **Bước 1: Xác định loại hình phân phối của tin nhắn:**
  + **Tin nhắn cá nhân/nhắm chọn (Private/Targeted):** Gửi riêng cho một tài khoản/cá nhân cụ thể (ví dụ: OTP giao dịch ngân hàng, thông báo biến động số dư, thông báo đơn hàng của shipper, tin nhắn tài khoản Google/GitHub/Shopee, hoặc tin nhắn hội thoại cá nhân có xưng tên/đại từ thân mật).
    * Giới tính mặc định: `unknown` (chỉ chọn `male`/`female` nếu có từ xưng cụ thể hoặc tên riêng có giới tính rõ ràng của người nhận).
    * Độ tuổi mặc định: `unknown` (vì gửi cho cá nhân cụ thể chưa biết tuổi ngoài đời thực).
  + **Tin nhắn quảng bá/đại chúng (Broadcast/Public):** Gửi diện rộng, không nhắm tới tài khoản cá nhân cụ thể (ví dụ: tin quảng cáo khuyến mãi chung của nhà mạng gửi đến tập thuê bao, tin rác spam dịch vụ cá cược/nhạy cảm, tin cảnh báo/tuyên truyền chính sách của cơ quan chức năng gửi toàn dân).
    * Giới tính mặc định: `all` (chỉ chọn `male`/`female` nếu có bằng chứng về giới tính của tệp khách hàng mục tiêu).
    * Độ tuổi mặc định: `general` (chỉ chọn `adult` nếu có bằng chứng về giới hạn độ tuổi).

- **Bước 2: Áp dụng các quy tắc cưỡng chế bắc cầu (Hard Rules):**
  + **Cưỡng chế độ tuổi (`age_groups`):** Bắt buộc gán `adult` cho các tin nhắn liên quan đến các dịch vụ yêu cầu tư cách pháp lý của người trưởng thành: cá cược (`gambling`), dịch vụ nhạy cảm/mại dâm/massage (`adult_service`), đầu tư lợi nhuận (`investment`), thu hồi nợ (`debt_collection`), tuyển dụng (`employment`).
  + **Cưỡng chế giới tính (`gender`):** Bắt buộc gán `male` cho các tin nhắn tìm bạn gái/escort/sugar baby/massage nhắm tới nam giới (ví dụ: "tìm bạn gái", "sugar baby cần tìm daddy", "massage phục vụ nam giới"). Bắt buộc gán `female` cho các tin tìm bạn trai/sugar mommy/phục vụ nữ giới.
  + **Cưỡng chế vai trò (`roles`):** Bắt buộc gán `customer` khi tin nhắn gửi từ thương hiệu/nhà mạng/ngân hàng đến khách hàng (OTP Google/GitHub, giao dịch thẻ Visa, biến động số dư SHB, tin nhắn quảng cáo khuyến mãi của Viettel/VinaPhone xưng hô "Quý khách" hoặc gửi đến chủ thuê bao).

- **Quy định chung**:
  + Mọi giá trị đặc thù (khác `all`, `general`, `general_public`) đều bắt buộc phải có `evidence` trích xuất nguyên văn từ tin nhắn.
  + Sentinel (như `unknown`, `general`, `general_public`) không đi cùng các giá trị cụ thể khác trong cùng một trường.

### Ví dụ gán nhãn thực tế từ Annotator A:

1. Tin nhắn: "Sử dụng mã xác minh 074736 để xác thực Microsoft."
   -> Loại tin: Targeted/Private (Mã xác thực cá nhân)
   -> target_audience: {{"age_groups": ["general"], "gender": "all", "roles": ["customer"], "evidence": ["Microsoft"]}}
   *Chú ý: OTP thông thường vẫn giữ gender "all" và age "general" nhưng vai trò là "customer".*

2. Tin nhắn: "The Visa 452404...6779 su dung tai 2C2*AMAZON PRIME VIDEO VN6717 2333 SG so tien 13,608 VND luc 17-12-2022 17:37:45. SD TK trich no tam tinh 1033311702: 486,392VND"
   -> Loại tin: Targeted/Private (Biến động tài khoản cá nhân có số thẻ cụ thể)
   -> target_audience: {{"age_groups": ["unknown"], "gender": "unknown", "roles": ["customer"], "evidence": ["The Visa 452404...6779"]}}

3. Tin nhắn: "[TB] Mừng VIETTEL 35 năm - ra mắt gói cước với tính năng mới: Chỉ với 35.000đ/7 ngày, Quý khách có thể lựa chọn truy cập data, gọi điện theo nhu cầu..."
   -> Loại tin: Broadcast/Public (Khuyến mãi nhà mạng gửi rộng rãi cho khách hàng)
   -> target_audience: {{"age_groups": ["general"], "gender": "all", "roles": ["customer"], "evidence": ["Quý khách"]}}

4. Tin nhắn: "Gai Xinh Toan Quoc phuc vu: 3p 69, Bu , Sex lien dit Add Zalo: 588326850 rcdgq"
   -> Loại tin: Broadcast/Public (Spam dịch vụ nhạy cảm cho nam giới)
   -> target_audience: {{"age_groups": ["adult"], "gender": "male", "roles": ["general_public"], "evidence": ["Gai Xinh"]}}

5. Tin nhắn: "[CANH CAO LAN CUOI]: Mirae Asset thong bao Ong Tran Van Hung CMND: 184756293 co khoan no 32,847,500VND. Yeu cau thanh toan truoc 17g hom nay. Qua thoi han tren, chung toi se gui ho so ve Cong an PC02 va thong bao den co quan lam viec cua Ong. Hotline: 0388223344."
   -> Loại tin: Targeted/Private (Đòi nợ đích danh)
   -> target_audience: {{"age_groups": ["unknown"], "gender": "male", "roles": ["debtor"], "evidence": ["Ong Tran Van Hung"]}}

6. Tin nhắn: "Cuoi tuan nay ranh ko Thắng? Qua nha toi choi, moi mua dc may chai ruou ngon."
   -> Loại tin: Targeted/Private (Chat cá nhân đích danh)
   -> target_audience: {{"age_groups": ["unknown"], "gender": "male", "roles": ["unknown"], "evidence": ["Thắng"]}}


## 5. Requested actions — ghi mọi hành động/kênh được nêu rõ

Requested action gồm cả yêu cầu chính, lựa chọn hỗ trợ, hướng dẫn tra cứu và
cú pháp từ chối/đăng ký. Không chỉ lấy một action nổi bật nhất.

- "soạn CODE gửi SHORTCODE", kể cả từ chối QC → reply_message.
- "gọi", "liên hệ", "LH", "CSKH", "hotline" kèm số → call_phone.
- "truy cập", "bấm", "tra cứu", "đăng ký tại" URL → click_or_visit_link.
- Zalo/Telegram/Facebook/Messenger/WhatsApp hoặc nền tảng ngoài SMS →
  contact_off_platform; nếu có URL, thường gán thêm click_or_visit_link.
- "tải/cài app" → install_application; chỉ có link app nhưng không yêu cầu cài
  thì không tự thêm install_application.
- "nạp tiền/nạp thẻ/nạp lần đầu" → deposit_or_top_up.
- "thanh toán hóa đơn/dịch vụ" → make_payment.
- "chuyển tiền vào tài khoản/người nhận" → transfer_money.
- yêu cầu nhập/cung cấp/xác minh OTP, mật khẩu, CCCD hoặc dữ liệu cá nhân →
  provide_personal_information.
- lời khuyên/hướng dẫn hành vi không có action chuyên biệt → other.
- giao dịch đã hoàn tất, OTP thuần túy hoặc thông báo không có chỉ dẫn/kênh
  hành động → none.
- có yêu cầu nhưng không giải mã được → unclear.

none và unclear không đi cùng action khác. Mọi action cụ thể phải có evidence.
Không xem số tiền/giá hoặc giao dịch đã xảy ra là make_payment nếu content
không yêu cầu thanh toán.

## 6. Persuasion tactics — xác định các chiến thuật thuyết phục người dùng

Tactic khác action. Không đưa call_phone/click/install/payment vào tactics; không đưa fear/threat/reward vào requested_actions. Tactic có thể xuất hiện ở tin hợp lệ. Nếu không sử dụng chiến thuật thuyết phục nào, gán duy nhất giá trị "none" (không để trống).

Phải áp dụng nghiêm ngặt các quy tắc cưỡng chế ánh xạ sau:
- **Cưỡng chế `link_lure`:** Bắt buộc gán `link_lure` nếu tin nhắn chứa bất kỳ liên kết, URL hoặc đường dẫn nào (ví dụ: `https://...`, `http://...`, hoặc các domain viết liền như `zalo.me/...`, `t.me/...`, `bit.ly/...`, `my.vnpt.com.vn/...`).
- **Cưỡng chế `off_platform_contact`:** Bắt buộc gán `off_platform_contact` nếu tin nhắn hướng dẫn hoặc mời kết bạn, liên hệ qua các nền tảng chat khác ngoài SMS như Zalo, Telegram, Facebook, Messenger (ví dụ: "Add Zalo", "kết bạn Zalo", "zalo.me/g/...", "lh zalo", "t.me/...").
- **Cưỡng chế `authority`:** Bắt buộc gán `authority` khi tin nhắn nhân danh cơ quan quản lý nhà nước, ban ngành, công an, cảnh sát, cơ quan thuế, hoặc trích dẫn các điều luật, quy định, thông cáo chính thức (ví dụ: "Bộ Công an", "Tổng cục Thuế", "Công an tỉnh", "Luật giao dịch điện tử", hoặc tiêu đề chính thức dạng "(TB) Chúc mừng năm mới...", "(TB) Để phòng ngừa...").
- **Phân biệt `scarcity` và `urgency`:**
  + **Gán `scarcity` (Khan hiếm):** Khi tin nhắn đề cập đến giới hạn về thời gian khuyến mãi, thời hạn sử dụng ưu đãi, số lượng quà tặng, hoặc phạm vi đối tượng áp dụng (ví dụ: "áp dụng đến ngày 14/09", "HSD 28/02", "DUY NHẤT trong hôm nay", "tặng riêng Quý khách").
  + **Gán `urgency` (Khẩn cấp):** Khi tin nhắn tạo áp lực thời gian bắt buộc phải hành động khẩn cấp, đòi hỏi thực hiện ngay lập tức để tránh mất mát hoặc xử phạt (ví dụ: "nạp tiền ngay", "truy cập ngay", "yêu cầu thanh toán trước 17g hôm nay", "cảnh cáo lần cuối").

## 7. Obfuscation — cần dấu hiệu biến đổi có chủ ý

Gán text_phenomena trước, sau đó mới quyết định obfuscation.
- present=false → techniques=[], severity=0.
- present=true → techniques là tập con của text_phenomena, severity 1..4.

Không đủ để kết luận obfuscation:
- toàn bộ viết hoa để nhấn mạnh;
- bỏ dấu tự nhiên;
- abbreviation thông dụng;
- tên domain/brand viết liền bình thường;
- content quảng cáo, gambling hoặc adult service nhưng không có biến đổi có hệ thống.

Bằng chứng mạnh cho obfuscation:
- thay chữ bằng số/ký tự trong từ: "thue b4o", "ZAL0", "D1EU K1EN";
- chèn dấu/underscore/hyphen có hệ thống: "c-a-s-i-n-o", "H;C_M";
- tách/nối khoảng trắng có chủ ý để che từ hoặc domain: "ehoaq. com";
- nhiều kỹ thuật phối hợp trên từ nhạy cảm.

Không dùng diacritic_omission hoặc lang_switching làm obfuscation technique vì
chúng không có trong enum kỹ thuật. Nếu không chắc ý định, hạ confidence và
thêm review flag obfuscation_intent_uncertain.

## 8. Confidence

Confidence phản ánh độ chắc chắn thực tế, không mặc định 1.0. Dùng review flag
khi domain mơ hồ, content khó đọc, target có nguy cơ suy diễn, taxonomy thiếu,
hoặc ý định obfuscation không chắc.

Taxonomy version: {taxonomy['version']}
Scope version: {taxonomy['scope_version']}
ALLOWED_ENUMS: {json.dumps(allowed, ensure_ascii=False)}
""".strip()


def build_user_prompt(items: Iterable[dict[str, str]]) -> str:
    payload = [
        {"sample_id": item["sample_id"], "content": item["masked_content"]}
        for item in items
    ]
    schema = metadata_output_schema()
    return (
        "Gán metadata cho toàn bộ batch. Kiểm lại số sample_id trước khi trả lời."
        "\n\nINPUT:\n"
        + json.dumps(payload, ensure_ascii=False)
        + "\n\nOUTPUT JSON SCHEMA:\n"
        + json.dumps(schema, ensure_ascii=False)
    )

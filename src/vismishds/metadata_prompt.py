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
Chỉ sử dụng content đã cung cấp. Không suy diễn từ label, nguồn dữ liệu,
category cũ, kiến thức bên ngoài, hoặc tính xác thực của thương hiệu/domain.

Quy tắc bắt buộc:
- Không gán sender_type; trường này được xử lý cục bộ.
- message_domain là chủ đề trung lập, không phải thật/giả.
- text_phenomena mô tả bề mặt; text_noise_score đo độ khó đọc.
- obfuscation chỉ true khi có bằng chứng về chủ ý né lọc/che từ khóa.
- Teencode, bỏ dấu hoặc typo không tự động là obfuscation.
- Target cụ thể chỉ được chọn khi content có evidence nguyên văn.
- Không suy tuổi/giới từ stereotype hoặc role.
- requested_actions mô tả hành động được yêu cầu, không phải hành động đã xảy ra.
- persuasion tactics có thể xuất hiện ở cả nhãn hợp lệ và lừa đảo.
- Evidence phải là đoạn ngắn xuất hiện trong content đã mask.
- Các token <PHONE_n>, <EMAIL_n>, <IDENTIFIER_n>, <PERSON_NAME_n> là placeholder
  bảo vệ riêng tư; không xem bản thân placeholder là text noise hay obfuscation.
- Nếu không đủ bằng chứng, dùng sentinel phù hợp thay vì đoán.
- Giữ nguyên sample_id.
- Mỗi input phải có đúng một output; không được bỏ sót hoặc thêm sample_id.
- Chỉ dùng enum đúng chính tả trong ALLOWED_ENUMS. Không tự tạo role như
  "parent" và không dùng text phenomenon làm obfuscation technique nếu enum
  obfuscation không chứa giá trị đó.
- Nếu chọn age/role/gender cụ thể, target_audience.evidence bắt buộc chứa ít
  nhất một đoạn nguyên văn. Nếu không có evidence, dùng unknown/general/all
  phù hợp.
- Sentinel target (general, unknown, not_applicable, general_public) không
  được đi cùng giá trị cụ thể.
- Obfuscation techniques chỉ được chọn từ danh sách riêng của obfuscation.

Taxonomy version: {taxonomy['version']}
Scope version: {taxonomy['scope_version']}
ALLOWED_ENUMS: {json.dumps(allowed, ensure_ascii=False)}
Trả duy nhất JSON phù hợp schema, không thêm markdown.
""".strip()


def build_user_prompt(items: Iterable[dict[str, str]]) -> str:
    payload = [
        {"sample_id": item["sample_id"], "content": item["masked_content"]}
        for item in items
    ]
    schema = metadata_output_schema()
    return (
        "Gán metadata cho batch sau. Số item output phải bằng input và mỗi "
        "sample_id xuất hiện đúng một lần.\n\nINPUT:\n"
        + json.dumps(payload, ensure_ascii=False)
        + "\n\nOUTPUT JSON SCHEMA:\n"
        + json.dumps(schema, ensure_ascii=False)
    )

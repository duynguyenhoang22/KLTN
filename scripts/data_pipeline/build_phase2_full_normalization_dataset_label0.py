"""
Build and maintain the Phase 2 label 0 full SMS normalization dataset.

This pipeline uses the Phase 1 final dataset as the source of SMS messages and
keeps only label 0 messages for LLM/manual normalization. The final dataset
output is plain normalized Vietnamese SMS text, one message per line, with a CSV
companion that keeps provenance metadata for auditing.

Outputs:
    data/normalization/phase2_full_normalization_working.csv
    data/normalization/phase2_full_normalization_final.csv
    data/normalization/phase2_full_normalization_lines.txt
    data/reports/phase2_full_normalization_report.md

Run from repository root:
    python scripts/data_pipeline/build_phase2_full_normalization_dataset_label0.py --init
    python scripts/data_pipeline/build_phase2_full_normalization_dataset_label0.py --finalize

Optional Mistral generation:
    python scripts/data_pipeline/build_phase2_full_normalization_dataset_label0.py --run-mistral --limit 200 --batch-size 20

Environment:
    MISTRAL_API_KEY, or paste MISTRAL_API_KEY in this file for local pilot runs
    MISTRAL_MODEL_NAME, defaults to mistral-small-latest
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import time
import unicodedata
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"
FINAL_DATASET_PATH = DATA_DIR / "final" / "vismishds_phase1_final.csv"
NORMALIZATION_DIR = DATA_DIR / "normalization"
REPORT_DIR = DATA_DIR / "reports"

WORKING_PATH = NORMALIZATION_DIR / "phase2_full_normalization_working.csv"
FINAL_CSV_PATH = NORMALIZATION_DIR / "phase2_full_normalization_final.csv"
FINAL_LINES_PATH = NORMALIZATION_DIR / "phase2_full_normalization_lines.txt"
REPORT_PATH = REPORT_DIR / "phase2_full_normalization_report.md"
PILOT_REVIEW_PATH = REPORT_DIR / "phase2_full_normalization_pilot_review.csv"

TASK_TYPE = "sms_full_normalization"
TARGET_LABEL = 0
DEFAULT_MISTRAL_MODEL = "mistral-small-latest"
DEFAULT_MISTRAL_REVIEW_MODEL = "mistral-small-latest"
MISTRAL_CHAT_COMPLETIONS_URL = "https://api.mistral.ai/v1/chat/completions"
MAX_API_RETRIES = 3

# Local pilot convenience: paste your Mistral key here if you do not want to set
# an environment variable. Prefer MISTRAL_API_KEY env var for shared/committed code.
MISTRAL_API_KEY = ""

BASE_COLUMNS = [
    "norm_id",
    "source_text",
    "normalized_text",
    "task_type",
    "label",
    "category",
    "has_url",
    "has_phone_number",
    "sender_type",
    "obfuscation_level",
    "data_origin",
    "source_sample_id",
    "source_dataset",
    "source_row_id",
]

WORKING_COLUMNS = BASE_COLUMNS + [
    "generated_normalized_text",
    "validation_status",
    "validation_issues",
    "manual_status",
    "review_note",
    "updated_at",
]

FINAL_COLUMNS = BASE_COLUMNS + ["validation_status", "validation_issues"]

NUMBER_RE = re.compile(r"\d+")
URL_EMAIL_DOMAIN_RE = re.compile(
    r"https?://\S+|www\.\S+"
    r"|\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    r"|\b[A-Za-z0-9][A-Za-z0-9-]*(?:\.[A-Za-z0-9][A-Za-z0-9-]*)*\."
    r"(?:com|vn|net|org|io|me|app|link|to|ai|info|biz|co|edu|gov)(?:/\S*)?\b",
    flags=re.IGNORECASE,
)
PHONE_RE = re.compile(r"(?:\+?84|0)(?:[\s.]?\d){8,10}|\b(?:1800|1900)(?:[\s.]?\d){4,6}\b")
CODE_TOKEN_RE = re.compile(r"\b(?=[A-Z0-9-]*[A-Z])(?=[A-Z0-9-]*\d)[A-Z0-9-]{4,}\b")
DATA_UNIT_TOKEN_RE = re.compile(r"\b\d+(?:[.,]\d+)?\s?(?:GB|MB|KB)\b", flags=re.IGNORECASE)
MONEY_TOKEN_RE = re.compile(r"\b\d[\d.,]*\s?(?:VND|VNĐ|d|đ|D|k|K)\b")
MONEY_K_RE = re.compile(r"(?<![A-Za-z])\b\d+(?:[.,]\d+)?\s*[Kk]\b")
FREE_MONEY_RE = re.compile(r"\b0\s?(?:d|đ|D|Đ|VND|VNĐ|DONG|dong)\b", flags=re.IGNORECASE)
THOUSAND_MONEY_RE = re.compile(r"\b\d+(?:[.,]\d+)?\s*ngàn(?:\s+đồng)?\b", flags=re.IGNORECASE)
NON_MONEY_K_CONTEXT_RE = re.compile(r"\b(?:5K|K\.12|K12)\b", flags=re.IGNORECASE)
EXPLANATION_RE = re.compile(
    r"dưới đây là|phiên bản đầy đủ|phiên bản chuẩn hóa|tôi không chắc|giải thích",
    flags=re.IGNORECASE,
)
SUSPICIOUS_TITLE_CASE_RE = re.compile(
    r"\b(?:Liên Hệ|Chương Trình|Thông Báo|Thuê Bao|Khách Hàng)\b"
)
REMAINING_OBFUSCATION_RE = re.compile(r"[@*_~|]{2,}|(?:[A-Za-z]\.){3,}")
MASKED_ACCOUNT_RE = re.compile(r"\b(?:TK|tài khoản|so du|số dư)?\s*\d*\*{2,}\d*\b", flags=re.IGNORECASE)
LEADING_TAG_RE = re.compile(r"^\s*(\[[^\]]+\]|\([^)]+\))")
MESSAGE_LABEL_TAGS = {
    "TB",
    "T.B",
    "THONG BAO",
    "THÔNG BÁO",
    "QC",
    "QUANG CAO",
    "QUẢNG CÁO",
}
GENERIC_OUTPUT_TAGS = {"THONG BAO", "THÔNG BÁO", "QUANG CAO", "QUẢNG CÁO"}
HALLUCINATED_PHONE_00_RE = re.compile(r"\bSố\s+điện\s+thoại\s*:\s*00\b", flags=re.IGNORECASE)


SYSTEM_PROMPT = """Bạn là công cụ Text Normalization cho SMS tiếng Việt.

Nhiệm vụ: khôi phục tin nhắn SMS không dấu, viết tắt, teencode hoặc bị obfuscated thành tiếng Việt đầy đủ, tự nhiên, đúng ngữ cảnh.

Chỉ trả về duy nhất câu đã chuẩn hóa. Không giải thích. Không markdown. Không thêm thông tin mới.

Quy tắc:
- Giữ nguyên ý nghĩa, thứ tự thông tin và cấu trúc chính của tin nhắn gốc.
- Khôi phục dấu tiếng Việt.
- Mở rộng từ viết tắt theo ngữ cảnh.
- Không tự ý thay đổi chữ hoa/thường của các phần không cần sửa.
- Chỉ viết hoa khi đúng quy tắc tiếng Việt: đầu câu, tên riêng, thương hiệu, mã định danh cần giữ nguyên.
- Không viết hoa tuỳ tiện giữa câu.
- Giữ nguyên số điện thoại, OTP, mã giao dịch, URL, domain, email, tên gói, mã khuyến mãi nếu không chắc chắn.
- Giữ nguyên mã gói, mã môn học, mã lớp, mã ưu đãi và mã định danh có chữ+số như ST5K, MXH100, MA005.N24, IE103.O22; không tách hoặc diễn giải các mã này.
- Không đổi sender/brand tag ở đầu tin nhắn. Chỉ [TB], (TB), [T.B], (T.B) được đổi thành [Thông báo]; chỉ [QC], (QC) được đổi thành [Quảng cáo].
- Các tag như [VCB], [MSB], [HDBank], [VNU-HCM], [MTTQ Viet Nam], [GHN], [EVN], [VIENDONG] là định danh người gửi; phải giữ nguyên hoặc chỉ khôi phục dấu nếu chắc chắn. Không đổi các tag này thành [Thông báo] hoặc [Quảng cáo].
- Không suy diễn sender/brand tag thành tổ chức khác nếu source không ghi rõ.
- Không thêm số điện thoại, hotline hoặc thông tin liên hệ nếu source không có. Đặc biệt 9h00, 10h00, 14h00 là thời gian; không được sinh thêm "Số điện thoại: 00".
- Trong ngữ cảnh viễn thông, "goi cuoc" là "gói cước", không phải "gọi cước".
- "san sale" thường là "săn sale"; không sửa thành "sắn sale".
- Có thể chuẩn hóa đơn vị data với hoặc không có khoảng trắng, ví dụ 30GB và 30 GB đều chấp nhận nếu giá trị không đổi.

Quy tắc thay thế:
- TB = "thông báo" hoặc "thuê bao" tuỳ ngữ cảnh.
- LH = "liên hệ".
- CT = "chương trình".
- [QC] = "[Quảng cáo]" nếu là nhãn đầu tin nhắn.
- {num}K hoặc {num}k = "{num} ngàn đồng".
- {num}đ = "{num} đồng".
- {num}h = "{num} giờ".
"""

REVIEWER_SYSTEM_PROMPT = """Bạn là reviewer chất lượng cho dataset Text Normalization SMS tiếng Việt.

Nhiệm vụ: so sánh source_text và normalized_text, quyết định output có dùng được không.

Lỗi nghiêm trọng:
- Mất, đổi hoặc thêm nội dung quan trọng.
- Mất/đổi số điện thoại, OTP, mã giao dịch, URL, domain, email, tên gói, mã khuyến mãi.
- Diễn giải hoặc paraphrase quá xa source.
- Đoán thêm thông tin không có trong source.
- Đổi sender/brand tag ở đầu tin nhắn thành [Thông báo]/[Quảng cáo] khi source không phải [TB]/[QC].
- Tự thêm số điện thoại, hotline hoặc thông tin liên hệ không có trong source.

Không xem là lỗi nghiêm trọng:
- Chuẩn hóa tiền tệ như 1500d -> 1.500đ hoặc 1.500 đồng.
- Chuẩn hóa 10.000D -> 10.000đ hoặc 10.000 đồng.
- Chuẩn hóa dấu phẩy/chấm trong số tiền nếu giá trị không đổi.
- Chuẩn hóa đơn vị data như 30GB -> 30 GB hoặc 500MB -> 500 MB nếu giá trị không đổi.
- Mở rộng viết tắt hợp lý như QK -> quý khách, LH -> liên hệ, CT -> chương trình, TB -> thông báo/thuê bao theo ngữ cảnh.

Phải yêu cầu revise nếu:
- Nhãn đầu tin bị đổi sai, ví dụ [TB] thành [Quảng cáo] hoặc [QC] thành [Thông báo].
- Sender/brand tag bị đổi sai, ví dụ [VCB], [MSB], [HDBank], [VNU-HCM], [MTTQ Viet Nam], [GHN] bị đổi thành [Thông báo] hoặc [Quảng cáo].
- Output tự thêm "Số điện thoại: 00" từ mốc giờ như 9h00, 10h00, 14h00.
- Mã gói/mã môn/mã lớp bị tách hoặc diễn giải sai, ví dụ MA005.N24 thành Mã 005.N24.
- Từ thường bị khôi phục sai nghĩa, ví dụ săn sale thành sắn sale, gói cước thành gọi cước.

Trả về duy nhất JSON object hợp lệ:
{"items":[{"norm_id":"...","verdict":"accept|revise","feedback":"..."}]}
"""


def rel_path(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, encoding="utf-8-sig")


def validate_source_schema(df: pd.DataFrame) -> None:
    required = {
        "sample_id",
        "content",
        "label",
        "has_url",
        "has_phone_number",
        "sender_type",
        "category",
        "obfuscation_level",
        "data_origin",
        "source_dataset",
        "source_row_id",
    }
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"{rel_path(FINAL_DATASET_PATH)} is missing columns: {', '.join(missing)}")


def build_working_frame(phase1: pd.DataFrame) -> pd.DataFrame:
    validate_source_schema(phase1)
    phase1 = phase1.loc[pd.to_numeric(phase1["label"], errors="raise").astype(int).eq(TARGET_LABEL)].copy()
    content = phase1["content"].astype(str).str.strip()
    empty_source = content.eq("")
    if empty_source.any():
        raise ValueError(f"Found {int(empty_source.sum())} empty source messages.")

    out = pd.DataFrame(
        {
            "norm_id": [f"sms_norm_{idx:05d}" for idx in range(1, len(phase1) + 1)],
            "source_text": content,
            "normalized_text": "",
            "task_type": TASK_TYPE,
            "label": pd.to_numeric(phase1["label"], errors="raise").astype(int),
            "category": phase1["category"].astype(str).str.strip(),
            "has_url": pd.to_numeric(phase1["has_url"], errors="raise").astype(int),
            "has_phone_number": pd.to_numeric(phase1["has_phone_number"], errors="raise").astype(int),
            "sender_type": phase1["sender_type"].astype(str).str.strip(),
            "obfuscation_level": phase1["obfuscation_level"].astype(str).str.strip(),
            "data_origin": phase1["data_origin"].astype(str).str.strip(),
            "source_sample_id": phase1["sample_id"].astype(str).str.strip(),
            "source_dataset": phase1["source_dataset"].astype(str).str.strip(),
            "source_row_id": pd.to_numeric(phase1["source_row_id"], errors="raise").astype(int),
            "generated_normalized_text": "",
            "validation_status": "pending",
            "validation_issues": "",
            "manual_status": "pending",
            "review_note": "",
            "updated_at": "",
        }
    )
    return out[WORKING_COLUMNS]


def protected_tokens(text: str) -> list[str]:
    tokens: list[str] = []
    money_spans = [match.span() for match in MONEY_TOKEN_RE.finditer(text)]
    data_unit_spans = [match.span() for match in DATA_UNIT_TOKEN_RE.finditer(text)]
    for regex in [URL_EMAIL_DOMAIN_RE, PHONE_RE, CODE_TOKEN_RE]:
        for match in regex.finditer(text):
            span = match.span()
            if any(span[0] >= money_span[0] and span[1] <= money_span[1] for money_span in money_spans):
                continue
            if any(span[0] >= data_span[0] and span[1] <= data_span[1] for data_span in data_unit_spans):
                continue
            if FREE_MONEY_RE.fullmatch(match.group(0)):
                continue
            tokens.append(match.group(0))
    # FIX: dict.fromkeys giữ thứ tự xuất hiện đầu tiên và dedup an toàn.
    # sorted(set(...), key=tokens.index) bị lỗi khi một token xuất hiện nhiều lần
    # vì list.index() chỉ trả về vị trí đầu tiên, gây KeyError tiềm ẩn với set.
    return list(dict.fromkeys(tokens))


def compact_digits(text: str) -> str:
    return re.sub(r"\D+", "", text)


def remove_vietnamese_accents(text: str) -> str:
    normalized = unicodedata.normalize("NFD", text)
    without_marks = "".join(ch for ch in normalized if unicodedata.category(ch) != "Mn")
    return without_marks.replace("đ", "d").replace("Đ", "D")


def tag_inner(tag: str) -> str:
    return tag.strip()[1:-1].strip()


def canonical_tag_text(text: str) -> str:
    no_accents = remove_vietnamese_accents(text).upper()
    return re.sub(r"[^A-Z0-9]+", " ", no_accents).strip()


def leading_tag(text: str) -> str:
    match = LEADING_TAG_RE.match(text)
    return match.group(1) if match else ""


def is_message_label_tag(tag: str) -> bool:
    return canonical_tag_text(tag_inner(tag)) in {canonical_tag_text(value) for value in MESSAGE_LABEL_TAGS}


def is_generic_output_tag(tag: str) -> bool:
    return canonical_tag_text(tag_inner(tag)) in {canonical_tag_text(value) for value in GENERIC_OUTPUT_TAGS}


def compact_tag_signature(text: str) -> str:
    return re.sub(r"[^A-Z0-9]+", "", remove_vietnamese_accents(text).upper())


def sender_tag_is_preserved(source_tag: str, output_tag: str) -> bool:
    source_inner = tag_inner(source_tag)
    output_inner = tag_inner(output_tag)
    source_sig = compact_tag_signature(source_inner)
    output_sig = compact_tag_signature(output_inner)
    if not source_sig or not output_sig:
        return False
    # FIX: logic cũ `output_sig in source_sig` gây false positive hai chiều.
    # Ví dụ source=[VCBBANK] -> output=[VCB]: VCB in VCBBANK = True -> pass sai.
    # Model đã rút gọn tag mất thông tin nhưng không bị phát hiện.
    # Chỉ cho phép output mở rộng prefix từ source (model thêm suffix rõ nghĩa hơn là OK),
    # không cho phép output rút gọn source.
    return source_sig == output_sig or output_sig.startswith(source_sig)


def validate_leading_sender_tag(source: str, output: str) -> list[str]:
    source_tag = leading_tag(source)
    if not source_tag or is_message_label_tag(source_tag):
        return []

    output_tag = leading_tag(output)
    if not output_tag:
        return [f"sender_tag_missing:{source_tag}"]
    if is_generic_output_tag(output_tag):
        return [f"sender_tag_changed:{source_tag}->{output_tag}"]
    if not sender_tag_is_preserved(source_tag, output_tag):
        return [f"sender_tag_changed:{source_tag}->{output_tag}"]
    return []


def is_money_number(number: str, source: str) -> bool:
    for match in MONEY_TOKEN_RE.finditer(source):
        if number in compact_digits(match.group(0)):
            return True
    return False


def spans_for_regex(regex: re.Pattern[str], text: str) -> list[tuple[int, int]]:
    return [match.span() for match in regex.finditer(text)]


def span_is_inside(span: tuple[int, int], spans: list[tuple[int, int]]) -> bool:
    return any(span[0] >= outer[0] and span[1] <= outer[1] for outer in spans)


def source_number_spans(source: str) -> list[tuple[str, tuple[int, int]]]:
    return [(match.group(0), match.span()) for match in NUMBER_RE.finditer(source)]


def has_short_year_expansion(number: str, output: str) -> bool:
    if len(number) == 2:
        return f"20{number}" in output or f"19{number}" in output
    if len(number) == 5 and number.startswith("0"):
        return number[1:] in output
    return False


def is_free_money_number(number: str, span: tuple[int, int], source: str, output: str) -> bool:
    if number != "0":
        return False
    if not span_is_inside(span, spans_for_regex(FREE_MONEY_RE, source)):
        return False
    return "miễn phí" in output.lower()


def number_is_preserved(number: str, span: tuple[int, int], source: str, output: str) -> bool:
    if number in NUMBER_RE.findall(output):
        return True
    output_digits = compact_digits(output)
    if len(number) >= 3 and number in output_digits:
        return True
    if is_money_number(number, source) and number in output_digits:
        return True
    if has_short_year_expansion(number, output):
        return True
    if is_free_money_number(number, span, source, output):
        return True
    return False


def normalize_unit_spacing(text: str) -> str:
    return re.sub(r"\b(\d+(?:[.,]\d+)?)\s+(GB|MB|KB)\b", r"\1\2", text, flags=re.IGNORECASE)


def has_unexpanded_money_k(text: str) -> bool:
    url_spans = spans_for_regex(URL_EMAIL_DOMAIN_RE, text)
    code_spans = spans_for_regex(CODE_TOKEN_RE, text)
    data_spans = spans_for_regex(DATA_UNIT_TOKEN_RE, text)
    thousand_spans = spans_for_regex(THOUSAND_MONEY_RE, text)
    non_money_spans = spans_for_regex(NON_MONEY_K_CONTEXT_RE, text)
    for match in MONEY_K_RE.finditer(text):
        span = match.span()
        if (
            span_is_inside(span, url_spans)
            or span_is_inside(span, code_spans)
            or span_is_inside(span, data_spans)
            or span_is_inside(span, thousand_spans)
            or span_is_inside(span, non_money_spans)
        ):
            continue
        return True
    return False


def has_remaining_obfuscation(text: str) -> bool:
    text_without_masked_accounts = MASKED_ACCOUNT_RE.sub(" ", text)
    return bool(REMAINING_OBFUSCATION_RE.search(text_without_masked_accounts))


def validate_normalization(source: str, output: str) -> tuple[str, list[str]]:
    issues: list[str] = []
    output = str(output).strip()
    source = str(source).strip()
    output_for_token_match = normalize_unit_spacing(output)

    if not output:
        return "pending", ["empty_output"]

    if "\n" in output:
        issues.append("multi_line_output")
    if EXPLANATION_RE.search(output):
        issues.append("contains_explanation")
    if HALLUCINATED_PHONE_00_RE.search(output) and not HALLUCINATED_PHONE_00_RE.search(source):
        issues.append("hallucinated_phone_00")

    issues.extend(validate_leading_sender_tag(source, output))

    for number, span in source_number_spans(source):
        if not number_is_preserved(number, span, source, output):
            prefix = "money_number_changed" if is_money_number(number, source) else "missing_number"
            issues.append(f"{prefix}:{number}")

    for token in protected_tokens(source):
        if token not in output_for_token_match:
            issues.append(f"missing_protected_token:{token}")

    if len(output) > max(80, len(source) * 3):
        issues.append("output_too_long")
    if SUSPICIOUS_TITLE_CASE_RE.search(output):
        issues.append("suspicious_title_case")
    if re.search(r"\b(?:LH|CT)\b", output):
        issues.append("unexpanded_abbreviation")
    if has_unexpanded_money_k(output):
        issues.append("unexpanded_money_k")
    if has_remaining_obfuscation(output):
        issues.append("remaining_obfuscation_chars")

    hard_fail = any(
        issue.startswith("missing_number:")
        or issue.startswith("missing_protected_token:")
        or issue.startswith("sender_tag_")
        or issue == "hallucinated_phone_00"
        or issue == "contains_explanation"
        for issue in issues
    )
    if hard_fail:
        return "fail", issues
    if issues:
        return "warning", issues
    return "pass", []


def prompt_for_message(message: str) -> str:
    return f"Input:\n{message}\n\nOutput:"


def prompt_for_batch(rows: list[dict[str, str]]) -> str:
    payload = {
        "items": [
            {
                "norm_id": row["norm_id"],
                "source_text": row["source_text"],
            }
            for row in rows
        ]
    }
    return (
        "Chuẩn hóa từng SMS trong JSON sau.\n"
        "Trả về duy nhất một JSON object hợp lệ theo đúng schema:\n"
        '{"items":[{"norm_id":"...","normalized_text":"..."}]}\n'
        "Không thêm markdown, không giải thích, không bỏ dòng nào, không đổi norm_id.\n\n"
        f"{json.dumps(payload, ensure_ascii=False)}"
    )


def prompt_for_review_batch(rows: list[dict[str, str]]) -> str:
    payload = {
        "items": [
            {
                "norm_id": row["norm_id"],
                "source_text": row["source_text"],
                "normalized_text": row["normalized_text"],
                "validator_issues": row["validation_issues"],
            }
            for row in rows
        ]
    }
    return (
        "Review các cặp normalization sau.\n"
        "Nếu output giữ đúng ý và chỉ khác format tiền tệ hợp lệ, verdict=accept.\n"
        "Nếu output mất/đổi/thêm thông tin hoặc paraphrase quá xa, verdict=revise và feedback ngắn gọn.\n\n"
        f"{json.dumps(payload, ensure_ascii=False)}"
    )


def prompt_for_revision_batch(rows: list[dict[str, str]]) -> str:
    payload = {
        "items": [
            {
                "norm_id": row["norm_id"],
                "source_text": row["source_text"],
                "current_normalized_text": row["normalized_text"],
                "review_feedback": row["feedback"],
            }
            for row in rows
        ]
    }
    return (
        "Sửa lại các normalized_text bị reviewer yêu cầu revise.\n"
        "Chỉ dựa vào source_text và feedback. Không giữ nội dung sai từ current_normalized_text.\n"
        "Trả về duy nhất JSON object hợp lệ theo schema:\n"
        '{"items":[{"norm_id":"...","normalized_text":"..."}]}\n\n'
        f"{json.dumps(payload, ensure_ascii=False)}"
    )


def get_mistral_api_key() -> str:
    return os.getenv("MISTRAL_API_KEY", "").strip() or MISTRAL_API_KEY.strip()


def init_working_file(force: bool = False) -> pd.DataFrame:
    if WORKING_PATH.exists() and not force:
        raise FileExistsError(f"{rel_path(WORKING_PATH)} already exists. Use --force to rebuild it.")
    NORMALIZATION_DIR.mkdir(parents=True, exist_ok=True)
    phase1 = read_csv(FINAL_DATASET_PATH)
    working = build_working_frame(phase1)
    working.to_csv(WORKING_PATH, index=False, encoding="utf-8-sig")
    return working


def load_working() -> pd.DataFrame:
    if not WORKING_PATH.exists():
        raise FileNotFoundError(f"Missing {rel_path(WORKING_PATH)}. Run with --init first.")
    df = read_csv(WORKING_PATH).fillna("")
    missing = sorted(set(WORKING_COLUMNS) - set(df.columns))
    if missing:
        raise ValueError(f"{rel_path(WORKING_PATH)} is missing columns: {', '.join(missing)}")
    labels = set(pd.to_numeric(df["label"], errors="coerce").dropna().astype(int))
    if labels - {TARGET_LABEL}:
        raise ValueError(
            f"{rel_path(WORKING_PATH)} contains non-label-{TARGET_LABEL} rows. "
            f"Rebuild with this label0 script or filter the working file first."
        )
    return df[WORKING_COLUMNS]


def selected_pending_indexes(df: pd.DataFrame, limit: int | None, overwrite: bool) -> list[int]:
    target_mask = df["source_text"].astype(str).str.strip().ne("")
    if not overwrite:
        target_mask &= df["normalized_text"].astype(str).str.strip().eq("")
    indexes = list(df.index[target_mask])
    if limit is not None:
        indexes = indexes[:limit]
    return indexes


def chunks(values: list[int], size: int) -> list[list[int]]:
    return [values[start : start + size] for start in range(0, len(values), size)]


def call_mistral_json(
    system_prompt: str,
    user_prompt: str,
    api_key: str,
    model_name: str,
    temperature: float,
    max_tokens: int,
) -> dict:
    request_body = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
        "response_format": {"type": "json_object"},
    }
    data = json.dumps(request_body, ensure_ascii=False).encode("utf-8")

    for attempt in range(1, MAX_API_RETRIES + 1):
        request = Request(
            MISTRAL_CHAT_COMPLETIONS_URL,
            data=data,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            method="POST",
        )
        try:
            with urlopen(request, timeout=120) as response:
                response_payload = json.loads(response.read().decode("utf-8"))
            content = response_payload["choices"][0]["message"]["content"].strip()
            return json.loads(content)
        except HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            wait_seconds = 10 * attempt
            print(f"  Mistral HTTP {exc.code} attempt {attempt}/{MAX_API_RETRIES}: {body[:300]}")
            if attempt == MAX_API_RETRIES:
                raise
            time.sleep(wait_seconds)
        except (URLError, TimeoutError, KeyError, json.JSONDecodeError, ValueError) as exc:
            wait_seconds = 10 * attempt
            print(f"  Mistral API/parse error attempt {attempt}/{MAX_API_RETRIES}: {exc}")
            if attempt == MAX_API_RETRIES:
                raise
            time.sleep(wait_seconds)
    return {}


def call_mistral_batch(
    rows: list[dict[str, str]],
    api_key: str,
    model_name: str,
    temperature: float,
    max_tokens: int,
) -> dict[str, str]:
    parsed = call_mistral_json(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=prompt_for_batch(rows),
        api_key=api_key,
        model_name=model_name,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    items = parsed.get("items", [])
    if not isinstance(items, list):
        raise ValueError("Mistral JSON response does not contain an items list.")
    outputs: dict[str, str] = {}
    for item in items:
        if not isinstance(item, dict):
            continue
        norm_id = str(item.get("norm_id", "")).strip()
        normalized_text = str(item.get("normalized_text", "")).strip()
        if norm_id and normalized_text:
            outputs[norm_id] = normalized_text
    return outputs


def call_mistral_review_batch(
    rows: list[dict[str, str]],
    api_key: str,
    model_name: str,
    temperature: float,
    max_tokens: int,
) -> dict[str, dict[str, str]]:
    parsed = call_mistral_json(
        system_prompt=REVIEWER_SYSTEM_PROMPT,
        user_prompt=prompt_for_review_batch(rows),
        api_key=api_key,
        model_name=model_name,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    items = parsed.get("items", [])
    if not isinstance(items, list):
        raise ValueError("Mistral review JSON response does not contain an items list.")
    reviews: dict[str, dict[str, str]] = {}
    for item in items:
        if not isinstance(item, dict):
            continue
        norm_id = str(item.get("norm_id", "")).strip()
        verdict = str(item.get("verdict", "")).strip().lower()
        feedback = str(item.get("feedback", "")).strip()
        if norm_id:
            reviews[norm_id] = {
                "verdict": verdict if verdict in {"accept", "revise"} else "revise",
                "feedback": feedback,
            }
    return reviews


def call_mistral_revision_batch(
    rows: list[dict[str, str]],
    api_key: str,
    model_name: str,
    temperature: float,
    max_tokens: int,
) -> dict[str, str]:
    parsed = call_mistral_json(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=prompt_for_revision_batch(rows),
        api_key=api_key,
        model_name=model_name,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    items = parsed.get("items", [])
    if not isinstance(items, list):
        raise ValueError("Mistral revision JSON response does not contain an items list.")
    revisions: dict[str, str] = {}
    for item in items:
        if not isinstance(item, dict):
            continue
        norm_id = str(item.get("norm_id", "")).strip()
        normalized_text = str(item.get("normalized_text", "")).strip()
        if norm_id and normalized_text:
            revisions[norm_id] = normalized_text
    return revisions


def run_mistral(
    limit: int | None,
    batch_size: int,
    sleep_seconds: float,
    overwrite: bool,
    temperature: float,
    max_tokens: int,
) -> pd.DataFrame:
    api_key = get_mistral_api_key()
    if not api_key:
        raise ValueError("MISTRAL_API_KEY is not set.")
    if batch_size < 1:
        raise ValueError("--batch-size must be >= 1.")

    model_name = os.getenv("MISTRAL_MODEL_NAME", DEFAULT_MISTRAL_MODEL)
    df = load_working()
    pending_indexes = selected_pending_indexes(df, limit=limit, overwrite=overwrite)
    batches = chunks(pending_indexes, batch_size)

    for batch_number, batch_indexes in enumerate(batches, start=1):
        rows = [
            {
                "norm_id": str(df.at[idx, "norm_id"]).strip(),
                "source_text": str(df.at[idx, "source_text"]).strip(),
            }
            for idx in batch_indexes
        ]
        outputs = call_mistral_batch(
            rows=rows,
            api_key=api_key,
            model_name=model_name,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        # FIX (performance): gom kết quả vào dict rồi assign một lần bằng loc[].
        # df.at[idx, col] trong vòng lặp lớn rất chậm vì mỗi lần gọi đều
        # trigger index lookup + type inference overhead của pandas.
        now = now_iso()
        updates: dict[str, list] = {
            "generated_normalized_text": [],
            "normalized_text": [],
            "validation_status": [],
            "validation_issues": [],
            "manual_status": [],
            "updated_at": [],
        }
        for idx in batch_indexes:
            norm_id = str(df.at[idx, "norm_id"]).strip()
            source = str(df.at[idx, "source_text"]).strip()
            normalized = outputs.get(norm_id, "").strip()
            status, issues = validate_normalization(source, normalized)
            row_issues = issues if normalized else ["missing_model_output"]
            updates["generated_normalized_text"].append(normalized)
            updates["normalized_text"].append(normalized)
            updates["validation_status"].append(status)
            updates["validation_issues"].append(";".join(row_issues))
            updates["manual_status"].append("needs_review" if status in {"warning", "fail", "pending"} else "generated")
            updates["updated_at"].append(now)
        for col, values in updates.items():
            df.loc[batch_indexes, col] = values

        completed = min(batch_number * batch_size, len(pending_indexes))
        statuses = df.loc[batch_indexes, "validation_status"].value_counts().to_dict()
        print(f"[batch {batch_number}/{len(batches)}] rows {completed}/{len(pending_indexes)} -> {statuses}")
        df.to_csv(WORKING_PATH, index=False, encoding="utf-8-sig")
        if sleep_seconds:
            time.sleep(sleep_seconds)

    return df


def run_mistral_review(
    limit: int | None,
    batch_size: int,
    sleep_seconds: float,
    temperature: float,
    max_tokens: int,
) -> pd.DataFrame:
    api_key = get_mistral_api_key()
    if not api_key:
        raise ValueError("MISTRAL_API_KEY is not set.")
    if batch_size < 1:
        raise ValueError("--batch-size must be >= 1.")

    reviewer_model = os.getenv("MISTRAL_REVIEW_MODEL_NAME", DEFAULT_MISTRAL_REVIEW_MODEL)
    revision_model = os.getenv("MISTRAL_REVISION_MODEL_NAME", os.getenv("MISTRAL_MODEL_NAME", DEFAULT_MISTRAL_MODEL))
    df = load_working()
    has_candidate = df["normalized_text"].astype(str).str.strip().ne("")
    needs_review = df["validation_status"].isin(["warning", "fail"]) | df["manual_status"].eq("needs_review")
    review_indexes = list(df.index[has_candidate & needs_review])
    if limit is not None:
        review_indexes = review_indexes[:limit]

    batches = chunks(review_indexes, batch_size)
    for batch_number, batch_indexes in enumerate(batches, start=1):
        rows = [
            {
                "norm_id": str(df.at[idx, "norm_id"]).strip(),
                "source_text": str(df.at[idx, "source_text"]).strip(),
                "normalized_text": str(df.at[idx, "normalized_text"]).strip(),
                "validation_issues": str(df.at[idx, "validation_issues"]).strip(),
            }
            for idx in batch_indexes
        ]
        reviews = call_mistral_review_batch(
            rows=rows,
            api_key=api_key,
            model_name=reviewer_model,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        revise_rows: list[dict[str, str]] = []
        # FIX (performance): collect accept updates vào dict, assign một lần sau loop
        accept_updates: dict[int, dict[str, str]] = {}
        now = now_iso()
        for idx in batch_indexes:
            norm_id = str(df.at[idx, "norm_id"]).strip()
            review = reviews.get(norm_id, {"verdict": "revise", "feedback": "missing reviewer output"})
            feedback = review["feedback"]
            if review["verdict"] == "accept":
                accept_updates[idx] = {
                    "manual_status": "llm_accepted",
                    "validation_status": "llm_pass",
                    "review_note": feedback,
                    "updated_at": now,
                }
            else:
                revise_rows.append(
                    {
                        "norm_id": norm_id,
                        "source_text": str(df.at[idx, "source_text"]).strip(),
                        "normalized_text": str(df.at[idx, "normalized_text"]).strip(),
                        "feedback": feedback,
                    }
                )
        if accept_updates:
            accept_idx = list(accept_updates.keys())
            for col in ("manual_status", "validation_status", "review_note", "updated_at"):
                df.loc[accept_idx, col] = [accept_updates[i][col] for i in accept_idx]

        if revise_rows:
            revisions = call_mistral_revision_batch(
                rows=revise_rows,
                api_key=api_key,
                model_name=revision_model,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            # FIX (performance): build lookup map một lần thay vì df.index[df["norm_id"].eq(norm_id)]
            # trong mỗi iteration — cách cũ là O(N*M) scan toàn DataFrame cho mỗi revise row.
            norm_id_to_idx: dict[str, int] = {
                str(df.at[i, "norm_id"]).strip(): i for i in batch_indexes
            }
            # FIX (performance): gom revision updates rồi assign một lần
            revision_updates: dict[int, dict[str, str]] = {}
            now_rev = now_iso()
            for row in revise_rows:
                norm_id = row["norm_id"]
                idx = norm_id_to_idx.get(norm_id)
                if idx is None:
                    continue
                revised = revisions.get(norm_id, "").strip()
                if not revised:
                    revision_updates[idx] = {
                        "manual_status": "needs_review",
                        "review_note": row["feedback"],
                        "normalized_text": df.at[idx, "normalized_text"],
                        "generated_normalized_text": df.at[idx, "generated_normalized_text"],
                        "validation_status": df.at[idx, "validation_status"],
                        "validation_issues": df.at[idx, "validation_issues"],
                        "updated_at": df.at[idx, "updated_at"],
                    }
                    continue
                status, issues = validate_normalization(str(df.at[idx, "source_text"]), revised)
                revision_updates[idx] = {
                    "normalized_text": revised,
                    "generated_normalized_text": revised,
                    "validation_status": status,
                    "validation_issues": ";".join(issues),
                    "manual_status": "llm_revised" if status not in {"fail", "pending"} else "needs_review",
                    "review_note": row["feedback"],
                    "updated_at": now_rev,
                }
            if revision_updates:
                rev_idx = list(revision_updates.keys())
                for col in ("normalized_text", "generated_normalized_text", "validation_status",
                            "validation_issues", "manual_status", "review_note", "updated_at"):
                    df.loc[rev_idx, col] = [revision_updates[i][col] for i in rev_idx]

        statuses = df.loc[batch_indexes, "manual_status"].value_counts().to_dict()
        print(f"[review batch {batch_number}/{len(batches)}] -> {statuses}")
        df.to_csv(WORKING_PATH, index=False, encoding="utf-8-sig")
        if sleep_seconds:
            time.sleep(sleep_seconds)

    return df


def refresh_validation() -> pd.DataFrame:
    df = load_working()

    # FIX (performance): thay iterrows() + df.at[idx] bằng apply() trên từng row.
    # iterrows() tạo Series mới cho mỗi dòng và df.at trigger index lookup mỗi lần —
    # với dataset lớn chênh lệch có thể lên tới 10-50x so với apply.
    now = now_iso()

    def _validate_row(row: pd.Series) -> pd.Series:
        normalized = str(row["normalized_text"]).strip()
        current_manual = str(row["manual_status"]).strip()
        if current_manual == "manual_reviewed" and normalized:
            updated_at = now if not str(row["updated_at"]).strip() else row["updated_at"]
            return pd.Series({
                "validation_status": "manual_pass",
                "validation_issues": "",
                "manual_status": "manual_reviewed",
                "updated_at": updated_at,
            })

        status, issues = validate_normalization(str(row["source_text"]), normalized)

        if status == "pending":
            manual_status = "pending"
        elif status == "fail":
            manual_status = "needs_review"
        elif status == "warning" and current_manual in {"llm_revised", "llm_accepted", "manual_reviewed"}:
            manual_status = current_manual
        elif status == "warning" and str(row["review_note"]).strip():
            manual_status = "llm_revised"
        elif status == "warning":
            manual_status = "needs_review"
        elif normalized and current_manual in {"", "pending", "needs_review"}:
            manual_status = "generated"
        else:
            manual_status = current_manual

        updated_at = now if (normalized and not str(row["updated_at"]).strip()) else row["updated_at"]

        return pd.Series({
            "validation_status": status,
            "validation_issues": ";".join(issues),
            "manual_status": manual_status,
            "updated_at": updated_at,
        })

    results = df.apply(_validate_row, axis=1)
    df[["validation_status", "validation_issues", "manual_status", "updated_at"]] = results
    df.to_csv(WORKING_PATH, index=False, encoding="utf-8-sig")
    return df


def finalize() -> pd.DataFrame:
    df = refresh_validation()
    ready = df["normalized_text"].astype(str).str.strip().ne("")
    final = df.loc[ready, FINAL_COLUMNS].copy()
    final.to_csv(FINAL_CSV_PATH, index=False, encoding="utf-8-sig")
    FINAL_LINES_PATH.write_text(
        "\n".join(final["normalized_text"].astype(str).str.strip()) + ("\n" if len(final) else ""),
        encoding="utf-8",
    )
    write_report(df, final)
    return final


def md_table(df: pd.DataFrame) -> str:
    if df.empty:
        return "_No rows._"
    return df.to_markdown(index=False)


def write_report(working: pd.DataFrame, final: pd.DataFrame | None = None) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    completed_count = int(working["normalized_text"].astype(str).str.strip().ne("").sum())
    final_count = completed_count if final is None else len(final)
    lines: list[str] = []
    lines.append("# Phase 2 Label 0 Full Normalization Dataset Report\n\n")
    lines.append("Generated by `scripts/data_pipeline/build_phase2_full_normalization_dataset_label0.py`.\n\n")
    lines.append("## Output\n\n")
    lines.append(f"- Input file: `{rel_path(FINAL_DATASET_PATH)}`\n")
    lines.append(f"- Working file: `{rel_path(WORKING_PATH)}`\n")
    lines.append(f"- Final CSV: `{rel_path(FINAL_CSV_PATH)}`\n")
    lines.append(f"- Final text lines: `{rel_path(FINAL_LINES_PATH)}`\n")
    lines.append(f"- Source label: {TARGET_LABEL}\n")
    lines.append(f"- Source rows: {len(working)}\n")
    lines.append(f"- Completed normalized rows: {final_count}\n\n")

    lines.append("## Working Status\n\n")
    status_counts = working.groupby("manual_status", dropna=False).size().reset_index(name="rows")
    lines.append(md_table(status_counts.sort_values("rows", ascending=False)))
    lines.append("\n\n")

    lines.append("## Validation Status\n\n")
    validation_counts = working.groupby("validation_status", dropna=False).size().reset_index(name="rows")
    lines.append(md_table(validation_counts.sort_values("rows", ascending=False)))
    lines.append("\n\n")

    lines.append("## Source Counts by Origin\n\n")
    source_counts = (
        working.groupby(["data_origin"], dropna=False)
        .size()
        .reset_index(name="rows")
        .sort_values(["data_origin"])
    )
    lines.append(md_table(source_counts))
    lines.append("\n\n")

    lines.append("## Notes\n\n")
    lines.append(
        "- This working set intentionally contains only source label 0 rows.\n"
        "- `normalized_text` is the dataset target. Metadata is kept only for audit/splitting.\n"
        "- `phase2_full_normalization_lines.txt` is the requested plain output: one normalized SMS per line.\n"
        "- Rows with `needs_review` or `fail` should be manually reviewed before final training/evaluation use.\n"
        "- `warning` can remain when the row has already been accepted/revised by LLM or manual review.\n"
    )
    REPORT_PATH.write_text("".join(lines), encoding="utf-8")


def write_pilot_review(df: pd.DataFrame, limit: int = 300) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    ready = df["normalized_text"].astype(str).str.strip().ne("")
    columns = [
        "norm_id",
        "source_text",
        "normalized_text",
        "validation_status",
        "validation_issues",
        "manual_status",
        "label",
        "category",
        "obfuscation_level",
        "data_origin",
        "source_dataset",
    ]
    review = df.loc[ready, columns].tail(limit).copy()
    review.to_csv(PILOT_REVIEW_PATH, index=False, encoding="utf-8-sig")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--init", action="store_true", help="Create the working CSV from phase1 content.")
    parser.add_argument("--force", action="store_true", help="Overwrite the existing working CSV when used with --init.")
    parser.add_argument("--run-mistral", action="store_true", help="Fill pending rows by calling Mistral in JSON batches.")
    parser.add_argument("--review-mistral", action="store_true", help="Use a Mistral reviewer to accept or revise warning/fail rows.")
    parser.add_argument("--limit", type=int, default=None, help="Maximum rows to generate in this run.")
    parser.add_argument("--batch-size", type=int, default=20, help="Rows per Mistral request.")
    parser.add_argument("--sleep-seconds", type=float, default=1.0, help="Delay between API calls.")
    parser.add_argument("--temperature", type=float, default=0.1, help="Generation temperature for Mistral.")
    parser.add_argument("--max-tokens", type=int, default=4096, help="Mistral max_tokens for each batch.")
    parser.add_argument("--overwrite", action="store_true", help="Regenerate rows even when normalized_text is present.")
    parser.add_argument("--validate", action="store_true", help="Refresh validation_status for the working CSV.")
    parser.add_argument("--finalize", action="store_true", help="Write final CSV and plain text outputs.")
    args = parser.parse_args()

    if args.init:
        working = init_working_file(force=args.force)
        write_report(working)
        print(f"Wrote working rows: {len(working)} -> {WORKING_PATH}")

    if args.run_mistral:
        df = run_mistral(
            limit=args.limit,
            batch_size=args.batch_size,
            sleep_seconds=args.sleep_seconds,
            overwrite=args.overwrite,
            temperature=args.temperature,
            max_tokens=args.max_tokens,
        )
        write_report(df)
        write_pilot_review(df)
        print(f"Updated working file: {WORKING_PATH}")
        print(f"Wrote pilot review file: {PILOT_REVIEW_PATH}")

    if args.review_mistral:
        df = run_mistral_review(
            limit=args.limit,
            batch_size=args.batch_size,
            sleep_seconds=args.sleep_seconds,
            temperature=args.temperature,
            max_tokens=args.max_tokens,
        )
        write_report(df)
        write_pilot_review(df)
        print(f"Updated working file after review: {WORKING_PATH}")
        print(f"Wrote pilot review file: {PILOT_REVIEW_PATH}")

    if args.validate:
        df = refresh_validation()
        write_report(df)
        print(f"Validated working rows: {len(df)}")

    if args.finalize:
        final = finalize()
        print(f"Wrote final rows: {len(final)} -> {FINAL_CSV_PATH}")
        print(f"Wrote plain text lines: {FINAL_LINES_PATH}")

    if not any([args.init, args.run_mistral, args.review_mistral, args.validate, args.finalize]):
        parser.print_help()


if __name__ == "__main__":
    main()

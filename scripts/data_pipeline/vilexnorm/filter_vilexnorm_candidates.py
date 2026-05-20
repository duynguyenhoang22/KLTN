"""Route ViLexNorm rows into clean, hard-negative and rejected candidates.

This script is rule-based by design. Its job is not to prove a final label; it
routes rows for downstream sampling/review while preserving every decision in
explicit flags and reasons.
"""

from __future__ import annotations

import argparse
import csv
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable


IN_FILE = Path("data/external/vilexnorm/processed/vilexnorm_all.csv")
OUT_DIR = Path("data/external/vilexnorm/processed")
CURATED_DIR = Path("data/external/vilexnorm/curated")
DOCS_DIR = Path("data/external/vilexnorm/docs")
REPORT_FILE = DOCS_DIR / "vilexnorm_filtering_report.md"
PREVIEW_REPORT_FILE = DOCS_DIR / "vilexnorm_filter_preview_report.md"

MIN_CHARS = 5
MAX_CLEAN_CHARS = 220
MAX_HARD_CHARS = 280
MAX_CLEAN_TOKENS = 55
MAX_HARD_TOKENS = 70

URL_RE = re.compile(
    r"(?:https?://|www\.)\S+|\b[\w.-]+\.(?:com|vn|net|org|top|xyz|vip|cc|icu|cfd|life|biz|me|info)\S*",
    re.IGNORECASE,
)
EMAIL_RE = re.compile(r"\b[\w.+-]+@[\w.-]+\.[a-z]{2,}\b", re.IGNORECASE)
PHONE_RE = re.compile(r"(?<!\d)(?:\+?84|0)(?:[\s.-]?\d){8,10}(?!\d)")
MONEY_AMOUNT_RE = re.compile(r"\b\d+\s*(?:k|nghìn|ngan|triệu|trieu|tr|vnd|đ|d)\b", re.IGNORECASE)
SYMBOL_RE = re.compile(r"[\W_]+", re.UNICODE)
SPACE_RE = re.compile(r"\s+")


KEYWORDS: dict[str, list[str]] = {
    "contact_platform": [
        "zalo",
        "telegram",
        "tele",
        "inbox",
        " ib ",
        " ib.",
        " ib,",
        "nhan tin rieng",
        "nhắn tin riêng",
    ],
    "cta": [
        "click",
        "truy cap",
        "truy cập",
        "dang nhap",
        "đăng nhập",
        "lien he",
        "liên hệ",
        "đăng ký",
        "dang ky",
        "nhan ngay",
        "nhận ngay",
        "vao link",
        "vào link",
        "quét mã",
        "quet ma",
    ],
    "job": [
        "tuyen",
        "tuyển",
        "viec lam",
        "việc làm",
        "lam online",
        "làm online",
        "nhan vien",
        "nhân viên",
        "part time",
        "ban thoi gian",
        "bán thời gian",
        "lam tai nha",
        "làm tại nhà",
    ],
    "money": [
        "kiem tien",
        "kiếm tiền",
        "thu nhap",
        "thu nhập",
        "luong",
        "lương",
        "hoa hong",
        "hoa hồng",
        "nhan thuong",
        "nhận thưởng",
        "trung thuong",
        "trúng thưởng",
        "hoan tien",
        "hoàn tiền",
        "rut tien",
        "rút tiền",
        "nap tien",
        "nạp tiền",
    ],
    "finance": [
        "ngan hang",
        "ngân hàng",
        "tai khoan",
        "tài khoản",
        "chuyen khoan",
        "chuyển khoản",
        "vay",
        "no ",
        "nợ",
        "tin dung",
        "tín dụng",
        "the tin dung",
        "thẻ tín dụng",
        "khoan vay",
        "khoản vay",
        "giao dich",
        "giao dịch",
    ],
    "authority": [
        "cong an",
        "công an",
        "canh sat",
        "cảnh sát",
        "bhxh",
        "bao hiem xa hoi",
        "bảo hiểm xã hội",
        "vneid",
        "thue",
        "thuế",
        "bo cong an",
        "bộ công an",
        "bo y te",
        "bộ y tế",
        "chinh phu",
        "chính phủ",
        "uy ban",
        "ủy ban",
    ],
    "warning": [
        "lua dao",
        "lừa đảo",
        "canh bao",
        "cảnh báo",
        "khoa tai khoan",
        "khóa tài khoản",
        "khoa",
        "khóa",
        "mao danh",
        "mạo danh",
        "gia mao",
        "giả mạo",
        "mat tien",
        "mất tiền",
        "bi lua",
        "bị lừa",
    ],
    "gambling": [
        "casino",
        "bet",
        "betting",
        "ca cuoc",
        "cá cược",
        "cuoc",
        "cược",
        "no hu",
        "nổ hũ",
        "xoc dia",
        "xóc đĩa",
        "tai xiu",
        "tài xỉu",
        "lo de",
        "lô đề",
        "keo bong",
        "kèo bóng",
    ],
    "sensitive_strong": [
        "sex",
        "clip nong",
        "clip nóng",
        "gai goi",
        "gái gọi",
        "hen ho 18",
        "hẹn hò 18",
        "massage kich duc",
        "massage kích dục",
    ],
    "sensitive_review": [
        "đéo",
        "deo",
        "cc",
        "cmn",
        "vcl",
        "vãi",
        "vch",
        "phò",
        "fò",
        "chym",
        "chim",
        "tội phạm",
        "toi pham",
        "lên phường",
        "len phuong",
    ],
    "soft_cta": [
        "bam",
        "bấm",
        "nhan tin",
        "nhắn tin",
        "nt ",
        "tham gia",
    ],
    "soft_job": [
        "cv",
        "c việc",
        "cong viec",
        "công việc",
    ],
}

TEXT_VARIANTS: dict[str, list[str]] = {
    "teencode": [
        " k ",
        " ko ",
        " hk ",
        " hông ",
        " hong ",
        " khum ",
        " hem ",
        " zậy",
        " zay",
        " dẫy",
        " dzậy",
        " thoai",
        " nhoa",
        " nheee",
        " rùi",
        " ròi",
    ],
    "abbreviation": [
        " đc",
        " dc",
        " được",
        " t ",
        " m ",
        " mk ",
        " ng ",
        " ny ",
        " mn ",
        " vs ",
        " cx ",
        " j ",
        " kb ",
    ],
    "slang": [
        " má ",
        " chời",
        " trời ơi",
        " vãi",
        " xỉu",
        " quãi",
        " lầy",
        " cute",
        " gu",
    ],
    "dialectal_variant": [
        " ni ",
        " tê ",
        " mô ",
        " răng ",
        " chi ",
        " hông ",
        " dzô",
    ],
    "informal_spelling": [
        " lun",
        " luôn á",
        " zui",
        " dui",
        " wa ",
        " wá",
        " qué",
        " ghê á",
    ],
}

OUTPUT_FIELDS = [
    "source_dataset",
    "source_file",
    "source_row_id",
    "split",
    "original",
    "normalized",
    "content",
    "label",
    "has_url",
    "has_phone_number",
    "sender_type",
    "category",
    "obfuscation_level",
    "data_origin",
    "external_source_type",
    "text_variant_type",
    "candidate_type",
    "hard_case_type",
    "review_status",
    "filter_reason",
    "reject_reason",
    "flags",
]

PREVIEW_FIELDS = ["review_id", "decision", "review_note", *OUTPUT_FIELDS]


def normalize_for_matching(text: str) -> str:
    text = text.lower().strip()
    text = SPACE_RE.sub(" ", text)
    return f" {text} "


def contains_any(text: str, terms: Iterable[str]) -> bool:
    return any(term in text for term in terms)


def token_count(text: str) -> int:
    return len([tok for tok in SPACE_RE.split(text.strip()) if tok])


def mostly_symbolic(text: str) -> bool:
    stripped = text.strip()
    if not stripped:
        return True
    symbol_chars = len(SYMBOL_RE.findall(stripped))
    return symbol_chars / max(len(stripped), 1) > 0.65


def detect_text_variant_type(match_text: str) -> str:
    found = [
        variant
        for variant, terms in TEXT_VARIANTS.items()
        if contains_any(match_text, terms)
    ]
    return ";".join(found) if found else "standard_or_unknown"


def detect_flags(original: str, normalized: str) -> set[str]:
    match_text = normalize_for_matching(f"{original} {normalized}")
    flags: set[str] = set()

    if URL_RE.search(original) or URL_RE.search(normalized):
        flags.add("has_url")
    if PHONE_RE.search(original) or PHONE_RE.search(normalized):
        flags.add("has_phone_number")
    if EMAIL_RE.search(original) or EMAIL_RE.search(normalized):
        flags.add("has_email")
    if MONEY_AMOUNT_RE.search(original) or MONEY_AMOUNT_RE.search(normalized):
        flags.add("has_money_amount")

    for group, terms in KEYWORDS.items():
        if contains_any(match_text, terms):
            flags.add(f"has_{group}_keyword")

    variant_type = detect_text_variant_type(match_text)
    for variant in variant_type.split(";"):
        if variant != "standard_or_unknown":
            flags.add(f"has_{variant}")

    chars = len(original.strip())
    tokens = token_count(original)
    if chars < MIN_CHARS:
        flags.add("too_short")
    if chars > MAX_CLEAN_CHARS or tokens > MAX_CLEAN_TOKENS:
        flags.add("long_for_clean")
    if chars > MAX_HARD_CHARS or tokens > MAX_HARD_TOKENS:
        flags.add("too_long")
    if mostly_symbolic(original):
        flags.add("mostly_symbolic")

    return flags


def plus_reason(*parts: str) -> str:
    return "+".join(parts)


def reject_reason(flags: set[str]) -> str | None:
    if "too_short" in flags:
        return "too_short"
    if "too_long" in flags:
        return "too_long"
    if "mostly_symbolic" in flags:
        return "mostly_symbolic"
    if "has_gambling_keyword" in flags:
        strong_gambling_context = {
            "has_url",
            "has_cta_keyword",
            "has_contact_platform_keyword",
            "has_money_keyword",
            "has_money_amount",
        }
        if flags.intersection(strong_gambling_context):
            return "has_gambling_keyword"
    if "has_sensitive_strong_keyword" in flags:
        return "has_sensitive_strong_keyword"
    if "has_url" in flags and "has_cta_keyword" in flags:
        return plus_reason("has_url", "has_cta_keyword")
    if "has_contact_platform_keyword" in flags and "has_cta_keyword" in flags:
        return plus_reason("has_contact_platform_keyword", "has_cta_keyword")
    if "has_contact_platform_keyword" in flags and "has_job_keyword" in flags:
        return plus_reason("has_contact_platform_keyword", "has_job_keyword")
    if "has_contact_platform_keyword" in flags and "has_money_keyword" in flags:
        return plus_reason("has_contact_platform_keyword", "has_money_keyword")
    if {"has_job_keyword", "has_money_keyword", "has_cta_keyword"}.issubset(flags):
        return plus_reason("has_job_keyword", "has_money_keyword", "has_cta_keyword")
    if {"has_finance_keyword", "has_cta_keyword", "has_phone_number"}.issubset(flags):
        return plus_reason("has_finance_keyword", "has_cta_keyword", "has_phone_number")
    return None


def hard_case_type(flags: set[str]) -> str:
    mapping = {
        "has_url": "url_like",
        "has_phone_number": "phone_like",
        "has_email": "contact_like",
        "has_contact_platform_keyword": "contact_like",
        "has_finance_keyword": "finance_like",
        "has_authority_keyword": "authority_like",
        "has_warning_keyword": "warning_like",
        "has_job_keyword": "job_like",
        "has_money_keyword": "money_like",
        "has_money_amount": "money_like",
        "has_cta_keyword": "cta_like",
        "has_soft_cta_keyword": "cta_like",
        "has_soft_job_keyword": "job_like",
        "has_gambling_keyword": "gambling_like",
        "has_sensitive_review_keyword": "sensitive_review",
    }
    types = []
    for flag, case_type in mapping.items():
        if flag not in flags:
            continue
        if flag == "has_soft_cta_keyword" and not flags.intersection(
            {
                "has_url",
                "has_phone_number",
                "has_email",
                "has_contact_platform_keyword",
                "has_money_keyword",
                "has_money_amount",
                "has_finance_keyword",
                "has_job_keyword",
                "has_authority_keyword",
                "has_warning_keyword",
            }
        ):
            continue
        if flag == "has_soft_job_keyword" and not flags.intersection(
            {
                "has_money_keyword",
                "has_money_amount",
                "has_contact_platform_keyword",
                "has_cta_keyword",
            }
        ):
            continue
        types.append(case_type)
    return ";".join(dict.fromkeys(types))


def route_row(row: dict[str, str]) -> dict[str, str]:
    original = (row.get("original") or "").strip()
    normalized = (row.get("normalized") or "").strip()
    flags = detect_flags(original, normalized)
    text_variant_type = detect_text_variant_type(
        normalize_for_matching(f"{original} {normalized}")
    )
    reason = reject_reason(flags)

    routed = {
        "source_dataset": row.get("source_dataset", "vilexnorm"),
        "source_file": row.get("source_file", ""),
        "source_row_id": row.get("source_row_id", ""),
        "split": row.get("split", ""),
        "original": original,
        "normalized": normalized,
        "content": original,
        "label": "0",
        "has_url": "1" if "has_url" in flags else "0",
        "has_phone_number": "1" if "has_phone_number" in flags else "0",
        "sender_type": "personal_number",
        "category": "",
        "obfuscation_level": "NONE",
        "data_origin": "",
        "external_source_type": "",
        "text_variant_type": text_variant_type,
        "candidate_type": "",
        "hard_case_type": "",
        "review_status": "",
        "filter_reason": "",
        "reject_reason": "",
        "flags": ";".join(sorted(flags)),
    }

    if reason:
        routed.update(
            {
                "category": "ViLexNorm rejected",
                "data_origin": "external_rejected",
                "external_source_type": "vilexnorm_rejected",
                "candidate_type": "rejected",
                "review_status": "auto_reject",
                "filter_reason": "strong_reject_rule",
                "reject_reason": reason,
            }
        )
        return routed

    case_type = hard_case_type(flags)
    if case_type:
        routed.update(
            {
                "category": "P2P hard negative",
                "data_origin": "external_curated",
                "external_source_type": "vilexnorm_hard_negative",
                "candidate_type": "hard_negative",
                "hard_case_type": case_type,
                "review_status": "needs_review",
                "filter_reason": "risk_surface_without_strong_reject",
            }
        )
        return routed

    routed.update(
        {
            "category": "P2P hội thoại thông thường",
            "data_origin": "external_real",
            "external_source_type": "vilexnorm_clean_p2p",
            "candidate_type": "clean_p2p",
            "review_status": "auto_pass",
            "filter_reason": "no_risk_flags",
        }
    )
    return routed


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"Missing prepared ViLexNorm file: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def _pick_stratified(
    rows: list[dict[str, str]],
    quota: int,
    stratify_field: str,
    fallback_field: str = "flags",
) -> list[dict[str, str]]:
    if quota <= 0:
        return []

    buckets: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        values = [value for value in row.get(stratify_field, "").split(";") if value]
        if not values and fallback_field:
            values = [value for value in row.get(fallback_field, "").split(";") if value]
        if not values:
            values = ["_none"]
        buckets[values[0]].append(row)

    selected: list[dict[str, str]] = []
    seen: set[int] = set()
    bucket_names = sorted(buckets, key=lambda name: (-len(buckets[name]), name))

    while len(selected) < quota and bucket_names:
        progressed = False
        for name in bucket_names:
            bucket = buckets[name]
            while bucket and id(bucket[0]) in seen:
                bucket.pop(0)
            if not bucket:
                continue
            row = bucket.pop(0)
            selected.append(row)
            seen.add(id(row))
            progressed = True
            if len(selected) >= quota:
                break
        if not progressed:
            break

    return selected


def take_preview(rows_by_type: dict[str, list[dict[str, str]]], preview_size: int) -> list[dict[str, str]]:
    quotas = {
        "clean_p2p": round(preview_size * 0.4),
        "hard_negative": round(preview_size * 0.4),
        "rejected": preview_size - round(preview_size * 0.4) * 2,
    }
    selected: list[dict[str, str]] = []
    selected.extend(
        _pick_stratified(
            rows_by_type["clean_p2p"],
            quotas["clean_p2p"],
            stratify_field="text_variant_type",
        )
    )
    selected.extend(
        _pick_stratified(
            rows_by_type["hard_negative"],
            quotas["hard_negative"],
            stratify_field="hard_case_type",
        )
    )
    selected.extend(
        _pick_stratified(
            rows_by_type["rejected"],
            quotas["rejected"],
            stratify_field="reject_reason",
        )
    )

    if len(selected) < preview_size:
        seen = {id(row) for row in selected}
        for candidate_type in ["hard_negative", "clean_p2p", "rejected"]:
            for row in rows_by_type[candidate_type]:
                if id(row) not in seen:
                    selected.append(row)
                    seen.add(id(row))
                    if len(selected) >= preview_size:
                        break
            if len(selected) >= preview_size:
                break

    preview_rows = []
    for idx, row in enumerate(selected[:preview_size], start=1):
        preview = {"review_id": str(idx), "decision": "", "review_note": ""}
        preview.update(row)
        preview["review_status"] = "preview_review"
        preview_rows.append(preview)
    return preview_rows


def summarize(rows: list[dict[str, str]]) -> dict[str, Counter[str]]:
    summary: dict[str, Counter[str]] = {
        "candidate_type": Counter(),
        "reject_reason": Counter(),
        "hard_case_type": Counter(),
        "text_variant_type": Counter(),
        "flags": Counter(),
    }
    for row in rows:
        summary["candidate_type"][row["candidate_type"]] += 1
        if row["reject_reason"]:
            summary["reject_reason"][row["reject_reason"]] += 1
        for value in row["hard_case_type"].split(";"):
            if value:
                summary["hard_case_type"][value] += 1
        for value in row["text_variant_type"].split(";"):
            if value:
                summary["text_variant_type"][value] += 1
        for value in row["flags"].split(";"):
            if value:
                summary["flags"][value] += 1
    return summary


def example_lines(rows_by_type: dict[str, list[dict[str, str]]], limit: int = 5) -> list[str]:
    lines: list[str] = []
    for candidate_type in ["clean_p2p", "hard_negative", "rejected"]:
        lines.append(f"### {candidate_type}")
        for row in rows_by_type[candidate_type][:limit]:
            reason = row["reject_reason"] or row["hard_case_type"] or row["filter_reason"]
            original = row["original"].replace("\n", " ")[:180]
            lines.append(f"- `{reason}` | {original}")
        lines.append("")
    return lines


def write_report(
    path: Path,
    mode: str,
    rows: list[dict[str, str]],
    rows_by_type: dict[str, list[dict[str, str]]],
    output_files: list[Path],
) -> None:
    summary = summarize(rows)
    lines = [
        f"# ViLexNorm filter {'preview ' if mode == 'preview' else ''}report",
        "",
        f"Mode: `{mode}`",
        f"Input file: `{IN_FILE}`",
        f"Total routed rows: {len(rows):,}",
        "",
        "## Output files",
        "",
    ]
    lines.extend(f"- `{path.as_posix()}`" for path in output_files)
    lines.extend(
        [
            "",
            "## Candidate counts",
            "",
            "| Candidate type | Rows |",
            "|:--|--:|",
        ]
    )
    for key in ["clean_p2p", "hard_negative", "rejected"]:
        lines.append(f"| {key} | {summary['candidate_type'][key]:,} |")

    for section, counter_key in [
        ("Top reject reasons", "reject_reason"),
        ("Hard-case types", "hard_case_type"),
        ("Text variant types", "text_variant_type"),
        ("Top flags", "flags"),
    ]:
        lines.extend(["", f"## {section}", "", "| Value | Rows |", "|:--|--:|"])
        for value, count in summary[counter_key].most_common(20):
            lines.append(f"| {value} | {count:,} |")

    lines.extend(["", "## Examples", "", *example_lines(rows_by_type)])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def route_all(rows: list[dict[str, str]]) -> tuple[list[dict[str, str]], dict[str, list[dict[str, str]]]]:
    routed = [route_row(row) for row in rows]
    rows_by_type: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in routed:
        rows_by_type[row["candidate_type"]].append(row)
    for candidate_type in ["clean_p2p", "hard_negative", "rejected"]:
        rows_by_type.setdefault(candidate_type, [])
    return routed, rows_by_type


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--mode",
        choices=["preview", "full"],
        default="preview",
        help="preview writes a review sample; full writes all candidate files.",
    )
    parser.add_argument(
        "--preview-size",
        type=int,
        default=100,
        help="Number of routed rows to write in preview mode.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    raw_rows = read_rows(IN_FILE)
    routed, rows_by_type = route_all(raw_rows)

    if args.mode == "preview":
        preview_file = CURATED_DIR / f"vilexnorm_filter_preview_{args.preview_size}.csv"
        preview_rows = take_preview(rows_by_type, args.preview_size)
        write_csv(preview_file, preview_rows, PREVIEW_FIELDS)
        write_report(PREVIEW_REPORT_FILE, "preview", routed, rows_by_type, [preview_file])
        print(f"Preview rows written: {len(preview_rows)}")
        print(f"Preview file: {preview_file}")
        print(f"Preview report: {PREVIEW_REPORT_FILE}")
        return

    clean_file = OUT_DIR / "vilexnorm_clean_candidates.csv"
    hard_file = OUT_DIR / "vilexnorm_hard_negative_candidates.csv"
    rejected_file = OUT_DIR / "vilexnorm_rejected.csv"
    write_csv(clean_file, rows_by_type["clean_p2p"], OUTPUT_FIELDS)
    write_csv(hard_file, rows_by_type["hard_negative"], OUTPUT_FIELDS)
    write_csv(rejected_file, rows_by_type["rejected"], OUTPUT_FIELDS)
    write_report(REPORT_FILE, "full", routed, rows_by_type, [clean_file, hard_file, rejected_file])

    print(f"Clean candidates: {len(rows_by_type['clean_p2p'])}")
    print(f"Hard-negative candidates: {len(rows_by_type['hard_negative'])}")
    print(f"Rejected rows: {len(rows_by_type['rejected'])}")
    print(f"Report: {REPORT_FILE}")


if __name__ == "__main__":
    main()

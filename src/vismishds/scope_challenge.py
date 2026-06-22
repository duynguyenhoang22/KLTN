from __future__ import annotations

import csv
import hashlib
import random
import re
from collections import defaultdict
from pathlib import Path


URL_RE = re.compile(
    r"(?i)(?:https?://|www\.|(?:[a-z0-9-]+\.)+(?:com|vn|net|org|top|"
    r"xyz|vip|icu|cc|me|ly|link|site|online|info|io|club|life))\S*"
)
PHONE_RE = re.compile(r"(?<!\d)(?:\+?84|0)?(?:[\s.-]?\d){8,11}(?!\d)")
WORD_RE = re.compile(r"[A-Za-zÀ-ỹĐđ]+")
SPECIAL_RE = re.compile(r"[^A-Za-zÀ-ỹĐđ0-9\s]")

DEBT_RE = re.compile(
    r"(?i)\b(?:n[oợ]|kho[aả]n vay|qu[aá] h[aạ]n|cic|thu h[oồ]i n[oợ]|"
    r"kh[oở]i ki[eệ]n|h[oồ] s[oơ] n[oợ]|x[uử] l[yý] n[oợ])\b"
)
GAMBLING_ADULT_RE = re.compile(
    r"(?i)\b(?:casino|bet|c[oờ]\s*b[aạ]c|n[oổ]\s*h[uũ]|b[aắ]n\s*c[aá]|"
    r"g[aá]i|h[eẹ]n\s*h[oò]|massage|t[iì]nh\s{0,1}m[oộ]t\s{0,1}[dđ][eê]m)\b"
)
OPPORTUNITY_RE = re.compile(
    r"(?i)\b(?:tuy[eể]n|vi[eệ]c l[aà]m|thu nh[aậ]p|hoa h[oồ]ng|"
    r"[dđ][aầ]u t[uư]|l[oợ]i nhu[aậ]n|tr[uú]ng th[uư][oở]ng|nh[aậ]n qu[aà]|"
    r"ki[eế]m ti[eề]n|c[oộ]ng t[aá]c vi[eê]n)\b"
)
SECURITY_RE = re.compile(
    r"(?i)\b(?:otp|m[aã] x[aá]c th[uự]c|t[aà]i kho[aả]n|[dđ][aă]ng nh[aậ]p|"
    r"b[aả]o m[aậ]t|kh[oó]a|c[aả]nh b[aá]o|giao d[iị]ch|qu[yý] kh[aá]ch)\b"
)
NOISE_RE = re.compile(
    r"(?i)(?:[a-z0-9][._~-]){3,}|(?:[a-z]-){3,}[a-z]|"
    r"[0134@#!*~^]{4,}|[A-Z]{2,}[a-z]+[A-Z]+"
)

COMMON_ENGLISH = {
    "account", "bank", "bonus", "click", "customer", "free", "job", "login",
    "online", "payment", "reward", "security", "service", "support", "team",
    "verify", "winner", "work", "your", "urgent", "update", "link", "sale",
    "shop", "app", "download", "telegram", "facebook", "tiktok", "amazon",
}
COMMON_VIETNAMESE = {
    "ban", "bạn", "cua", "của", "duoc", "được", "khach", "khách", "nhan",
    "nhận", "thong", "thông", "tin", "vui", "long", "lòng", "tai", "tài",
    "khoan", "khoản", "chuyen", "chuyển", "tien", "tiền", "dang", "đăng",
    "ky", "ký", "hom", "hôm", "nay", "ngay", "ngày", "xin", "chao", "chào",
}

BUCKET_ORDER = [
    "minimal_content",
    "debt_threat",
    "out_of_scope_malicious",
    "opportunity_ambiguous",
    "legitimate_security_like",
    "language_boundary",
    "heavy_noise_context",
]

DEFAULT_QUOTAS = {
    "minimal_content": 8,
    "debt_threat": 8,
    "out_of_scope_malicious": 8,
    "opportunity_ambiguous": 8,
    "legitimate_security_like": 6,
    "language_boundary": 6,
    "heavy_noise_context": 6,
}

ANNOTATION_FIELDS = [
    "scope_decision",
    "proposed_label",
    "evidence",
    "confidence",
    "reason",
    "needs_discussion",
]


def _normalized_without_urls_phones(text: str) -> str:
    value = URL_RE.sub(" ", text)
    value = PHONE_RE.sub(" ", value)
    return re.sub(r"[\W_]+", " ", value, flags=re.UNICODE).strip()


def _language_ratio(text: str) -> tuple[float, int]:
    words = [word.lower() for word in WORD_RE.findall(text)]
    content_words = [
        word for word in words
        if len(word) > 1 and not (word.isupper() and len(word) <= 5)
    ]
    if not content_words:
        return 0.0, 0
    english = sum(word in COMMON_ENGLISH for word in content_words)
    vietnamese = sum(word in COMMON_VIETNAMESE for word in content_words)
    known = english + vietnamese
    return (english / known if known else 0.0), known


def candidate_buckets(row: dict[str, str]) -> list[str]:
    text = row.get("content", "").strip()
    category = row.get("category", "").lower()
    label = row.get("label", "")
    obfuscation = row.get("obfuscation_level", "")
    buckets: list[str] = []

    stripped = _normalized_without_urls_phones(text)
    word_count = len(WORD_RE.findall(text))
    only_url = bool(URL_RE.fullmatch(text.strip()))
    only_phone = bool(PHONE_RE.fullmatch(text.strip()))
    if only_url or only_phone or len(stripped) <= 8 or word_count <= 3:
        buckets.append("minimal_content")

    if DEBT_RE.search(text) or "đòi nợ" in category or "đe dọa" in category:
        buckets.append("debt_threat")

    if (
        GAMBLING_ADULT_RE.search(text)
        or "cờ bạc" in category
        or "betting" in category
        or "nhạy cảm" in category
    ):
        buckets.append("out_of_scope_malicious")

    if (
        OPPORTUNITY_RE.search(text)
        or "tuyển dụng" in category
        or "đầu tư" in category
        or "crypto" in category
    ):
        buckets.append("opportunity_ambiguous")

    if label == "0" and (
        SECURITY_RE.search(text)
        and (URL_RE.search(text) or re.search(r"(?i)\b(?:ngay|kh[aẩ]n|"
                                             r"trong \d+|h[eế]t h[aạ]n)\b", text))
    ):
        buckets.append("legitimate_security_like")

    english_ratio, known_words = _language_ratio(text)
    if known_words >= 4 and 0.35 <= english_ratio <= 0.70:
        buckets.append("language_boundary")

    special_density = len(SPECIAL_RE.findall(text)) / max(len(text), 1)
    if (
        "LEVEL 4" in obfuscation
        or "LEVEL 5" in obfuscation
        or NOISE_RE.search(text)
        or special_density >= 0.15
    ):
        buckets.append("heavy_noise_context")

    return buckets


def _stable_rank(sample_id: str, seed: int, bucket: str) -> str:
    return hashlib.sha256(f"{seed}|{bucket}|{sample_id}".encode()).hexdigest()


def select_scope_challenge(
    source: Path,
    size: int = 50,
    seed: int = 20260621,
    real_only: bool = True,
) -> tuple[list[dict[str, str]], list[dict[str, str]], dict[str, int]]:
    if size != sum(DEFAULT_QUOTAS.values()):
        raise ValueError(
            f"Current scope challenge design requires size "
            f"{sum(DEFAULT_QUOTAS.values())}"
        )

    rows: list[dict[str, str]] = []
    with source.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            if real_only and row.get("data_origin") != "real":
                continue
            row["_candidate_buckets"] = "|".join(candidate_buckets(row))
            rows.append(row)

    selected_ids: set[str] = set()
    selected: list[dict[str, str]] = []
    key_rows: list[dict[str, str]] = []
    counts: dict[str, int] = {}

    for bucket in BUCKET_ORDER:
        candidates = [
            row for row in rows
            if bucket in row["_candidate_buckets"].split("|")
            and row["sample_id"] not in selected_ids
        ]
        candidates.sort(
            key=lambda row: _stable_rank(row["sample_id"], seed, bucket)
        )
        quota = DEFAULT_QUOTAS[bucket]
        if len(candidates) < quota:
            raise ValueError(
                f"Not enough unique real candidates for {bucket}: "
                f"need {quota}, found {len(candidates)}"
            )
        chosen = candidates[:quota]
        counts[bucket] = len(chosen)
        for row in chosen:
            selected_ids.add(row["sample_id"])
            blind = {
                "challenge_group": bucket,
                "sample_id": row["sample_id"],
                "content": row["content"],
            }
            selected.append(blind)
            key_rows.append({
                **blind,
                "legacy_label": row.get("label", ""),
                "legacy_category": row.get("category", ""),
                "legacy_obfuscation_level": row.get("obfuscation_level", ""),
                "data_origin": row.get("data_origin", ""),
                "all_candidate_groups": row["_candidate_buckets"],
            })

    return selected, key_rows, counts


def write_scope_challenge(
    selected: list[dict[str, str]],
    key_rows: list[dict[str, str]],
    annotator_outputs: dict[str, Path],
    key_output: Path,
    seed: int,
) -> None:
    base_fields = ["item_order", "sample_id", "content"]
    for index, (annotator, output) in enumerate(sorted(annotator_outputs.items())):
        shuffled = [dict(row) for row in selected]
        random.Random(seed + index + 1).shuffle(shuffled)
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(
                handle, fieldnames=base_fields + ANNOTATION_FIELDS
            )
            writer.writeheader()
            for item_order, row in enumerate(shuffled, start=1):
                writer.writerow({
                    "item_order": item_order,
                    "sample_id": row["sample_id"],
                    "content": row["content"],
                })

    key_output.parent.mkdir(parents=True, exist_ok=True)
    key_fields = [
        "challenge_group", "sample_id", "content", "legacy_label",
        "legacy_category", "legacy_obfuscation_level", "data_origin",
        "all_candidate_groups",
    ]
    with key_output.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=key_fields)
        writer.writeheader()
        writer.writerows(key_rows)

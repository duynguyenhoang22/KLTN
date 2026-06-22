from __future__ import annotations

import re
from dataclasses import dataclass


EMAIL_RE = re.compile(
    r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b"
)
PHONE_RE = re.compile(
    r"(?<![A-Za-z0-9])(?:\+?84|0)(?:[\s.-]?\d){8,10}(?![A-Za-z0-9])"
)
LABELED_IDENTIFIER_RE = re.compile(
    r"(?ix)\b("
    r"cccd|cmnd|cmt|c[aă]n\s*c[uư][oơ]c|"
    r"s[oố]\s*t[aà]i\s*kho[aả]n|stk|"
    r"m[aã]\s*giao\s*d[iị]ch|m[aã]\s*h[oồ]\s*s[oơ]|"
    r"m[aã]\s*[dđ][oơ]n|s[oố]\s*h[oợ]p\s*[dđ][oồ]ng"
    r")\s*[:#-]?\s*([A-Z0-9.-]{5,})"
)
LABELED_NAME_RE = re.compile(
    r"(?i)\b(h[oọ]\s*t[eê]n|ch[uủ]\s*xe|kh[aá]ch\s*h[aà]ng)"
    r"\s*[:#-]\s*([A-ZÀ-ỸĐ][A-Za-zÀ-ỹĐđ\s]{2,50})"
)


@dataclass(frozen=True)
class MaskedText:
    text: str
    replacements: dict[str, int]


def mask_pii(text: str) -> MaskedText:
    counts = {
        "email": 0,
        "phone": 0,
        "identifier": 0,
        "name": 0,
    }

    def replace_email(_: re.Match[str]) -> str:
        counts["email"] += 1
        return f"<EMAIL_{counts['email']}>"

    def replace_phone(_: re.Match[str]) -> str:
        counts["phone"] += 1
        return f"<PHONE_{counts['phone']}>"

    def replace_identifier(match: re.Match[str]) -> str:
        counts["identifier"] += 1
        return f"{match.group(1)}: <IDENTIFIER_{counts['identifier']}>"

    def replace_name(match: re.Match[str]) -> str:
        counts["name"] += 1
        return f"{match.group(1)}: <PERSON_NAME_{counts['name']}>"

    masked = EMAIL_RE.sub(replace_email, str(text))
    masked = PHONE_RE.sub(replace_phone, masked)
    masked = LABELED_IDENTIFIER_RE.sub(replace_identifier, masked)
    masked = LABELED_NAME_RE.sub(replace_name, masked)
    return MaskedText(masked, counts)

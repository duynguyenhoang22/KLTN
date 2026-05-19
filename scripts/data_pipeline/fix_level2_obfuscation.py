"""
Repair LEVEL 2 obfuscation style in the synthetic smishing dataset.

This is a post-augmentation correction pass. It does not regenerate messages and
does not change labels/categories. It only softens over-leeted LEVEL 2 content by
normalizing common non-sensitive glue words while preserving URL/domain tokens and
leaving scam-sensitive words obfuscated.

Rationale:
    LEVEL 1 = sparse intentional homoglyph use to avoid filters.
    LEVEL 2 = targeted sensitive-word leet plus camouflage, not leet-every-word
              as the default pattern.

Run:
    python scripts/data_pipeline/fix_level2_obfuscation.py

Inputs:
    data/synthetic/synthetic_label_1.csv

Outputs:
    - updates data/synthetic/synthetic_label_1.csv in place
    - writes data/reports/level2_correction_report.md
    - writes data/reports/level2_correction_changed_rows.csv
"""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / "data" / "synthetic" / "synthetic_label_1.csv"
REPORT_PATH = ROOT / "data" / "reports" / "level2_correction_report.md"
CHANGED_ROWS_PATH = ROOT / "data" / "reports" / "level2_correction_changed_rows.csv"

LEVEL2 = "LEVEL 2 – Leet nặng + tên riêng"

URL_OR_DOMAIN_RE = re.compile(
    r"(?iu)\b(?:https?://|www\.|t\.ly/|zalo\.me/|telegram\.me/|t\.me/)"
    r"[^\s,;]+|\b[a-z0-9-]+(?:\.[a-z0-9-]+)+/[^\s,;]*|\b[a-z0-9-]+\."
    r"(?:com|vn|net|org|info|icu|top|xyz|site|me|cc|vip|tech|cfd)\b[^\s,;]*"
)

# These are intentionally conservative. They target frequent non-sensitive
# function/context words that made LEVEL 2 look like full-sentence leet.
# Scam-critical tokens such as nh4n, t1en, kh04, x4c, n0, v4y, cu0c, thu0ng,
# n4p, rut, OTP, banking tokens, betting tokens, and threat terms are omitted.
TOKEN_NORMALIZATIONS: dict[str, str] = {
    "b4n": "ban",
    "0ng": "ong",
    "d4": "da",
    "z4": "da",
    "zã": "da",
    "zu": "du",
    "zinh": "dinh",
    "z1nh": "dinh",
    "d1nh": "dinh",
    "z3": "de",
    "d3": "de",
    "v4o": "vao",
    "v40": "vao",
    "b4m": "bam",
    "c0": "co",
    "c04": "cua",
    "cu4": "cua",
    "s3": "se",
    "b1": "bi",
    "l4": "la",
    "l41": "lai",
    "n4y": "nay",
    "m01": "moi",
    "m0i": "moi",
    "ng4y": "ngay",
    "tr0ng": "trong",
    "tru0c": "truoc",
    "tr4nh": "tranh",
    "h0m": "hom",
    "h4n": "han",
    "qu4": "qua",
    "kh0ng": "khong",
    "khonj": "khong",
    "zu0c": "duoc",
    "du0c": "duoc",
    "ch4p": "chap",
    "nh4p": "nhap",
    "d4ng": "dang",
    "d0": "do",
    "d0t": "dot",
    "th0ng": "thong",
    "th1eu": "thieu",
    "th13u": "thieu",
    "vuj": "vui",
    "lonj": "long",
    "k13m": "kiem",
    "tr4": "tra",
    "c4p": "cap",
    "c4n": "can",
    "chua": "chua",
    "s41": "sai",
    "dunj": "dung",
    "ngunj": "ngung",
    "h04t": "hoat",
    "d0ng": "dong",
    "du0ng": "duong",
    "thue": "thue",
    "t4i": "tai",
    "t41": "tai",
    "h0ac": "hoac",
    "m4t": "mat",
    "kh4ch": "khach",
    "h4ng": "hang",
    "ng4n": "ngan",
    "ph41": "phai",
    "y3u": "yeu",
    "c4u": "cau",
    "l13n": "lien",
    "h3": "he",
    "du0c": "duoc",
    "hu0ng": "huong",
}

PHRASE_NORMALIZATIONS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"(?iu)\bB0[-_\s]?LD[-_\s]?TB[-_\s]?XH\b"), "Bo LD-TB-XH"),
    (re.compile(r"(?iu)\bB0\b"), "Bo"),
    (re.compile(r"(?iu)\bQU4[-_\s]?H4N\b"), "QUA HAN"),
    (re.compile(r"(?iu)\bKH0NG[-_\s]?ZU0C\b"), "KHONG DUOC"),
    (re.compile(r"(?iu)\bKH0NG[-_\s]?DU0C\b"), "KHONG DUOC"),
    (re.compile(r"(?iu)\bCH4P[-_\s]?NH4N\b"), "CHAP NHAN"),
    (re.compile(r"(?iu)\bVuj\s+lonj\b"), "Vui long"),
]

WORD_RE = re.compile(r"(?iu)(?<![\w])[\w!]+(?![\w])")


def preserve_case(original: str, replacement: str) -> str:
    if original.isupper():
        return replacement.upper()
    if original[:1].isupper():
        return replacement[:1].upper() + replacement[1:]
    return replacement


def normalize_token(match: re.Match[str]) -> str:
    token = match.group(0)
    replacement = TOKEN_NORMALIZATIONS.get(token.lower())
    if replacement is None:
        return token
    return preserve_case(token, replacement)


def protect_urls(text: str) -> tuple[str, dict[str, str]]:
    protected: dict[str, str] = {}

    def repl(match: re.Match[str]) -> str:
        key = f"__URL_{len(protected)}__"
        protected[key] = match.group(0)
        return key

    return URL_OR_DOMAIN_RE.sub(repl, text), protected


def restore_urls(text: str, protected: dict[str, str]) -> str:
    for key, value in protected.items():
        text = text.replace(key, value)
    return text


def normalize_level2_content(text: str) -> str:
    work, protected = protect_urls(str(text))
    for pattern, replacement in PHRASE_NORMALIZATIONS:
        work = pattern.sub(replacement, work)
    work = WORD_RE.sub(normalize_token, work)
    return restore_urls(work, protected)


def leet_token_ratio(text: str) -> float:
    work, _ = protect_urls(str(text))
    tokens = re.findall(r"(?iu)\b[\w!]+\b", work)
    tokens = [t for t in tokens if any(ch.isalpha() for ch in t) and len(t) > 1]
    if not tokens:
        return 0.0
    leet_tokens = [t for t in tokens if re.search(r"[01345789!@$]", t)]
    return len(leet_tokens) / len(tokens)


def main() -> None:
    df = pd.read_csv(DATA_PATH)
    if "level" not in df.columns or "content" not in df.columns:
        raise ValueError("Expected columns 'content' and 'level' in synthetic_label_1.csv")

    before_dist = df["level"].value_counts().sort_index()
    level2_mask = df["level"].eq(LEVEL2)

    before_content = df.loc[level2_mask, "content"].copy()
    before_ratio = before_content.map(leet_token_ratio)
    after_content = before_content.map(normalize_level2_content)
    after_ratio = after_content.map(leet_token_ratio)

    changed_mask = before_content.ne(after_content)
    changed_indices = changed_mask[changed_mask].index
    df.loc[changed_indices, "content"] = after_content.loc[changed_indices]

    changed_rows = pd.DataFrame(
        {
            "row_index": changed_indices,
            "category": df.loc[changed_indices, "category"].values,
            "level": df.loc[changed_indices, "level"].values,
            "leet_token_ratio_before": before_ratio.loc[changed_indices].round(4).values,
            "leet_token_ratio_after": after_ratio.loc[changed_indices].round(4).values,
            "content_before": before_content.loc[changed_indices].values,
            "content_after": after_content.loc[changed_indices].values,
        }
    )

    df.to_csv(DATA_PATH, index=False, encoding="utf-8-sig")
    changed_rows.to_csv(CHANGED_ROWS_PATH, index=False, encoding="utf-8-sig")

    after_dist = df["level"].value_counts().sort_index()
    category_changes = changed_rows["category"].value_counts().sort_index()

    report = [
        "# LEVEL 2 Obfuscation Correction Report",
        "",
        "## Purpose",
        "",
        "Repair existing synthetic `LEVEL 2` rows so they better represent targeted sensitive-word leet plus camouflage, rather than full-sentence leet by default.",
        "",
        "This pass did not regenerate data, did not modify labels/categories, and did not modify URL/domain strings.",
        "",
        "## Rule Summary",
        "",
        "- Only rows with `LEVEL 2 – Leet nặng + tên riêng` were eligible.",
        "- URL/domain-like spans were protected before normalization.",
        "- Common non-sensitive glue/context words were normalized, for example `B4n -> Ban`, `v4o -> vao`, `kh0ng -> khong`, `zu0c -> duoc`.",
        "- Scam-sensitive words were intentionally left obfuscated, including terms around money, account locking, verification, debt, betting, and finance.",
        "- The `level` column was preserved because the repair changes style within Level 2 rather than changing the intended obfuscation level.",
        "",
        "## Impact",
        "",
        f"- Total rows: {len(df)}",
        f"- Original LEVEL 2 rows reviewed: {int(level2_mask.sum())}",
        f"- LEVEL 2 rows modified: {len(changed_rows)}",
        f"- Mean LEVEL 2 leet-token ratio before: {before_ratio.mean():.4f}",
        f"- Mean LEVEL 2 leet-token ratio after: {after_ratio.mean():.4f}",
        "",
        "## Level Distribution",
        "",
        "Distribution is expected to remain unchanged because this pass repairs content style, not metadata labels.",
        "",
        "### Before",
        "",
        before_dist.to_markdown(),
        "",
        "### After",
        "",
        after_dist.to_markdown(),
        "",
        "## Modified Rows by Category",
        "",
        category_changes.to_markdown(),
        "",
        "## Manual Review File",
        "",
        f"Changed rows were written to `{CHANGED_ROWS_PATH.relative_to(ROOT)}`.",
        "",
    ]
    REPORT_PATH.write_text("\n".join(report), encoding="utf-8")

    print(f"Updated {DATA_PATH}")
    print(f"Modified LEVEL 2 rows: {len(changed_rows)} / {int(level2_mask.sum())}")
    print(f"Wrote {REPORT_PATH}")
    print(f"Wrote {CHANGED_ROWS_PATH}")


if __name__ == "__main__":
    main()

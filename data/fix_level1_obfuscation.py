"""
Repair LEVEL 1 obfuscation style in the synthetic smishing dataset.

This is a conservative post-augmentation correction pass. It does not regenerate
messages and does not change labels/categories. It only softens over-leeted
LEVEL 1 content so LEVEL 1 better means sparse intentional homoglyph use,
usually on one or two sensitive terms.

Run:
    python data/fix_level1_obfuscation.py

Inputs:
    data/synthetic/synthetic_label_1.csv

Outputs:
    - updates data/synthetic/synthetic_label_1.csv in place
    - writes data/reports/level1_correction_report.md
    - writes data/reports/level1_correction_changed_rows.csv
"""

from __future__ import annotations

import re
import unicodedata
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "synthetic" / "synthetic_label_1.csv"
REPORT_PATH = ROOT / "data" / "reports" / "level1_correction_report.md"
CHANGED_ROWS_PATH = ROOT / "data" / "reports" / "level1_correction_changed_rows.csv"

LEVEL1 = "LEVEL 1 – Leet nhẹ (thay 1-2 ký tự)"

URL_OR_DOMAIN_RE = re.compile(
    r"(?iu)\b(?:https?://|www\.|t\.ly/|zalo\.me/|telegram\.me/|t\.me/)"
    r"[^\s,;]+|\b[a-z0-9-]+(?:\.[a-z0-9-]+)+/[^\s,;]*|\b[a-z0-9-]+\."
    r"(?:com|vn|net|org|info|icu|top|xyz|site|me|cc|vip|tech|cfd)\b[^\s,;]*"
)

WORD_RE = re.compile(r"(?iu)(?<![\w])[\w!@$]+(?![\w])")
LEET_CHAR_RE = re.compile(r"[01345789!@$]")

SENSITIVE_PATTERNS = [
    r"tien|t1en|t13n|ti3n",
    r"nhan|nh4n",
    r"thuong|thu0ng|thưởng",
    r"rut|r[uú]t",
    r"nap|n4p|nạp",
    r"vay|v4y|n[o0]|n0",
    r"thanh\s*toan|th4nh|tu4n|t04n",
    r"khoa|kh0a|kh04|tam\s*dung|t4m",
    r"xac\s*thuc|x4c|thuc",
    r"dang\s*nhap|nhap|nh4p",
    r"otp",
    r"tai\s*khoan|t41|kh04n|tk",
    r"bank|vcb|bidv|mb|techcom|acb|tpbank",
    r"cuoc|cu0c|bet|casino|baccarat|no\s*hu|n[o0]hu|ban\s*ca",
    r"zalo|telegram|t\.me",
    r"cccd|cmnd|cong\s*an|c0ng|an\s*ninh|dieu\s*tra|d13u",
    r"phat\s*nguoi|vneid|thue|bhxh|bhtn|nq-?116",
    r"dau\s*tu|d4u|crypto|forex|copy\s*trade|nhiem\s*vu",
]
SENSITIVE_RE = re.compile("(?iu)(" + "|".join(SENSITIVE_PATTERNS) + ")")

# Broader than the LEVEL 2 normalizer because LEVEL 1 should be much sparser.
# These replacements target frequent generated teencode/leet forms. URLs are
# protected before applying them, so domain strings are not altered.
TOKEN_NORMALIZATIONS: dict[str, str] = {
    "0ng": "ong",
    "b4": "ba",
    "b4n": "ban",
    "b3n": "ben",
    "d4": "da",
    "z4": "da",
    "d3": "de",
    "z3": "de",
    "du0c": "duoc",
    "zu0c": "duoc",
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
    "ng4y": "ngay",
    "m01": "moi",
    "m0i": "moi",
    "tr0ng": "trong",
    "tru0c": "truoc",
    "tr4nh": "tranh",
    "h0m": "hom",
    "h4n": "han",
    "qu4": "qua",
    "kh0ng": "khong",
    "khonj": "khong",
    "ch4p": "chap",
    "ch0": "cho",
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
    "s41": "sai",
    "dunj": "dung",
    "ngunj": "ngung",
    "h04t": "hoat",
    "d0ng": "dong",
    "du0ng": "duong",
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
    "hu0ng": "huong",
    "tu01": "tuoi",
    "g14": "gia",
    "z4nh": "danh",
    "d4nh": "danh",
    "s4n": "san",
    "f4m": "pham",
    "f4m.": "pham",
    "d0n": "don",
    "lu0ng": "luong",
    "l4m": "lam",
    "nh4": "nha",
    "k1nh": "kinh",
    "ngh13m": "nghiem",
    "v13n": "vien",
    "tuy3n": "tuyen",
    "nh4n": "nhan",
    "t13n": "tien",
    "t1en": "tien",
    "ti3n": "tien",
    "n4p": "nap",
    "v0ng": "vong",
    "cu0c": "cuoc",
    "n0": "no",
    "c4": "ca",
    "h0": "ho",
    "tr0": "tro",
    "thu3": "thue",
    "h04n": "hoan",
    "t3": "te",
    "y": "y",
    "c4nh": "canh",
    "s4t": "sat",
    "g140": "giao",
    "g14o": "giao",
    "b13n": "bien",
    "f4t": "phat",
    "ph4t": "phat",
    "v1": "vi",
    "n0p": "nop",
    "fwu": "phu",
    "ch1nh": "chinh",
    "h0": "ho",
    "s0": "so",
    "d1nh": "dinh",
    "d13u": "dieu",
    "k13n": "kien",
    "d!eu": "dieu",
    "k!en": "kien",
    "t0ng": "tong",
    "cu01": "cuoi",
    "c0ng": "cong",
    "h0": "ho",
    "kh04n": "khoan",
    "kh04": "khoa",
    "x4c": "xac",
    "thuc": "thuc",
    "nh4p": "nhap",
    "th01": "thoi",
    "th4": "tha",
    "t1m": "tim",
    "v1d30": "video",
    "ch1": "chi",
    "v01": "voi",
    "t13p": "tiep",
    "t0c": "toc",
    "s13u": "sieu",
    "m4ng": "mang",
    "h01": "hoi",
    "x4": "xa",
    "l3n": "len",
    "n3u": "neu",
    "h04": "hoa",
    "h0ng": "hong",
    "d41": "dai",
    "l1nk": "link",
    "z4l0": "Zalo",
    "sh0p33": "Shopee",
    "t1k1": "Tiki",
    "l4z4d4": "Lazada",
    "l4z4z4": "Lazada",
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


def strip_accents(text: str) -> str:
    return "".join(
        ch for ch in unicodedata.normalize("NFD", text)
        if unicodedata.category(ch) != "Mn"
    )


def preserve_case(original: str, replacement: str) -> str:
    if replacement == "Zalo":
        return replacement
    if original.isupper():
        return replacement.upper()
    if original[:1].isupper():
        return replacement[:1].upper() + replacement[1:]
    return replacement


def protect_urls(text: str) -> tuple[str, dict[str, str]]:
    protected: dict[str, str] = {}

    def repl(match: re.Match[str]) -> str:
        key = f"__URL_{len(protected)}__"
        protected[key] = match.group(0)
        return key

    return URL_OR_DOMAIN_RE.sub(repl, str(text)), protected


def restore_urls(text: str, protected: dict[str, str]) -> str:
    for key, value in protected.items():
        text = text.replace(key, value)
    return text


def is_sensitive_token(token: str) -> bool:
    raw = token.lower()
    plain = strip_accents(raw)
    return bool(SENSITIVE_RE.search(raw) or SENSITIVE_RE.search(plain))


def normalize_level1_content(text: str, max_sensitive_leet_keep: int = 2) -> str:
    work, protected = protect_urls(str(text))
    for pattern, replacement in PHRASE_NORMALIZATIONS:
        work = pattern.sub(replacement, work)

    kept_sensitive = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal kept_sensitive
        token = match.group(0)
        lower = token.lower()
        has_leet = bool(LEET_CHAR_RE.search(token))
        sensitive = is_sensitive_token(token)

        # Keep at most two sensitive obfuscated tokens to preserve LEVEL 1's
        # filter-evasion signal. Normalize additional tokens when known.
        if has_leet and sensitive and kept_sensitive < max_sensitive_leet_keep:
            kept_sensitive += 1
            return token

        replacement = TOKEN_NORMALIZATIONS.get(lower)
        if replacement is not None:
            return preserve_case(token, replacement)
        return token

    return restore_urls(WORD_RE.sub(repl, work), protected)


def leet_token_ratio(text: str) -> float:
    work, _ = protect_urls(str(text))
    tokens = re.findall(r"(?iu)\b[\w!@$]+\b", work)
    tokens = [
        t for t in tokens
        if t.upper() != "URL" and any(ch.isalpha() for ch in t) and len(t) > 1
    ]
    if not tokens:
        return 0.0
    return sum(bool(LEET_CHAR_RE.search(t)) for t in tokens) / len(tokens)


def main() -> None:
    df = pd.read_csv(DATA_PATH)
    if "level" not in df.columns or "content" not in df.columns:
        raise ValueError("Expected columns 'content' and 'level' in synthetic_label_1.csv")

    level1_mask = df["level"].eq(LEVEL1)
    before_content = df.loc[level1_mask, "content"].copy()
    before_ratio = before_content.map(leet_token_ratio)
    after_content = before_content.map(normalize_level1_content)
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

    category_changes = changed_rows["category"].value_counts().sort_index()
    level_dist = df["level"].value_counts().sort_index()
    report = [
        "# LEVEL 1 Obfuscation Correction Report",
        "",
        "## Purpose",
        "",
        "Repair existing synthetic `LEVEL 1` rows so they better represent sparse intentional homoglyph substitution rather than dense sentence-wide leet.",
        "",
        "This pass did not regenerate data, did not modify labels/categories, and did not modify URL/domain strings.",
        "",
        "## Rule Summary",
        "",
        "- Only rows with `LEVEL 1 – Leet nhẹ (thay 1-2 ký tự)` were eligible.",
        "- URL/domain-like spans were protected before normalization.",
        "- At most two sensitive obfuscated tokens were preserved per row.",
        "- Known non-sensitive leet/teencode tokens were normalized where deterministic.",
        "- Unknown tokens were left unchanged to avoid semantic damage.",
        "",
        "## Impact",
        "",
        f"- Total rows: {len(df)}",
        f"- LEVEL 1 rows reviewed: {int(level1_mask.sum())}",
        f"- LEVEL 1 rows modified: {len(changed_rows)}",
        f"- Mean LEVEL 1 leet-token ratio before: {before_ratio.mean():.4f}",
        f"- Mean LEVEL 1 leet-token ratio after: {after_ratio.mean():.4f}",
        "",
        "## Level Distribution",
        "",
        "Distribution is expected to remain unchanged because this pass repairs content style, not metadata labels.",
        "",
        level_dist.to_markdown(),
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
    print(f"Modified LEVEL 1 rows: {len(changed_rows)} / {int(level1_mask.sum())}")
    print(f"Mean LEVEL 1 leet-token ratio before: {before_ratio.mean():.4f}")
    print(f"Mean LEVEL 1 leet-token ratio after: {after_ratio.mean():.4f}")
    print(f"Wrote {REPORT_PATH}")
    print(f"Wrote {CHANGED_ROWS_PATH}")


if __name__ == "__main__":
    main()

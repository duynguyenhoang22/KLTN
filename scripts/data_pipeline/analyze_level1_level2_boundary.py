"""
Compare synthetic LEVEL 1 and repaired LEVEL 2 obfuscation boundaries.

This script evaluates whether LEVEL 2 is now sufficiently distinct from LEVEL 1
and whether LEVEL 1 itself contains rows that are too heavily obfuscated.

Run:
    python scripts/data_pipeline/analyze_level1_level2_boundary.py

Outputs:
    data/reports/level1_level2_boundary_report.md
    data/reports/level1_level2_borderline_rows.csv
"""

from __future__ import annotations

import re
import unicodedata
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / "data" / "synthetic" / "synthetic_label_1.csv"
REPORT_PATH = ROOT / "data" / "reports" / "level1_level2_boundary_report.md"
BORDERLINE_PATH = ROOT / "data" / "reports" / "level1_level2_borderline_rows.csv"

LEVEL1 = "LEVEL 1 – Leet nhẹ (thay 1-2 ký tự)"
LEVEL2 = "LEVEL 2 – Leet nặng + tên riêng"

URL_OR_DOMAIN_RE = re.compile(
    r"(?iu)\b(?:https?://|www\.|t\.ly/|zalo\.me/|telegram\.me/|t\.me/)"
    r"[^\s,;]+|\b[a-z0-9-]+(?:\.[a-z0-9-]+)+/[^\s,;]*|\b[a-z0-9-]+\."
    r"(?:com|vn|net|org|info|icu|top|xyz|site|me|cc|vip|tech|cfd)\b[^\s,;]*"
)

TOKEN_RE = re.compile(r"(?iu)\b[\w!@$]+\b")
LEET_CHAR_RE = re.compile(r"[01345789!@$]")
SEPARATOR_RE = re.compile(r"(?iu)\b\w+[._~^*/-]\w+")
MID_UPPER_RE = re.compile(r"\b[A-Za-z]*[a-z][A-Z][A-Za-z]*\b")
VN_DIACRITIC_RE = re.compile(
    r"[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡ"
    r"ùúụủũưừứựửữỳýỵỷỹđÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨ"
    r"ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ]"
)

# Sensitivity is intentionally broad and domain-oriented. The goal is not exact
# Vietnamese word normalization, but identifying whether leet lands on scam cues
# rather than on every grammatical word.
SENSITIVE_PATTERNS = [
    r"tien|t1en|t13n|ti3n",
    r"nhan|nh4n|nh4n|nhan",
    r"thuong|thu0ng|thưởng",
    r"rut|r[uú]t",
    r"nap|n4p|nạp",
    r"vay|v4y|n[o0]|n0|no",
    r"thanh\s*toan|th4nh|tu4n|t04n",
    r"khoa|kh0a|kh04|tam\s*dung|t4m",
    r"xac\s*thuc|x4c|thuc|th[uw]c",
    r"dang\s*nhap|nhap|nh4p",
    r"otp|ma\s*otp|m[a4]\s*xac",
    r"tai\s*khoan|t41|kh04n|tk",
    r"ngan\s*hang|bank|vcb|bidv|mb|techcom|acb|tpbank",
    r"cuoc|cu0c|bet|casino|baccarat|no\s*hu|n[o0]hu|ban\s*ca",
    r"lien\s*he|zalo|telegram|t\.me",
    r"cccd|cmnd|cong\s*an|c0ng|an\s*ninh|dieu\s*tra|d13u",
    r"phat\s*nguoi|vneid|thue|bhxh|bhtn|nq-?116",
    r"dau\s*tu|d4u|crypto|forex|copy\s*trade|nhiem\s*vu",
]
SENSITIVE_RE = re.compile("(?iu)(" + "|".join(SENSITIVE_PATTERNS) + ")")


def strip_accents(text: str) -> str:
    return "".join(
        ch for ch in unicodedata.normalize("NFD", text)
        if unicodedata.category(ch) != "Mn"
    )


def protect_urls(text: str) -> str:
    return URL_OR_DOMAIN_RE.sub(" <URL> ", str(text))


def tokenize(text: str) -> list[str]:
    return TOKEN_RE.findall(protect_urls(text))


def is_url_placeholder(token: str) -> bool:
    return token.upper() == "URL"


def is_sensitive(token: str) -> bool:
    raw = token.lower()
    plain = strip_accents(raw)
    return bool(SENSITIVE_RE.search(raw) or SENSITIVE_RE.search(plain))


def metrics(text: str) -> dict[str, float | int]:
    protected = protect_urls(text)
    tokens = [
        t for t in tokenize(text)
        if not is_url_placeholder(t) and any(ch.isalpha() for ch in t) and len(t) > 1
    ]
    leet_tokens = [t for t in tokens if LEET_CHAR_RE.search(t)]
    sensitive_tokens = [t for t in tokens if is_sensitive(t)]
    leet_sensitive_tokens = [t for t in sensitive_tokens if LEET_CHAR_RE.search(t)]
    nonsensitive_leet_tokens = [t for t in leet_tokens if not is_sensitive(t)]
    chars = [ch for ch in protected if not ch.isspace()]
    alpha_chars = [ch for ch in chars if ch.isalpha()]

    return {
        "token_count": len(tokens),
        "leet_token_count": len(leet_tokens),
        "leet_token_ratio": len(leet_tokens) / max(len(tokens), 1),
        "sensitive_token_count": len(sensitive_tokens),
        "leet_sensitive_token_count": len(leet_sensitive_tokens),
        "sensitive_leet_coverage": len(leet_sensitive_tokens) / max(len(sensitive_tokens), 1),
        "nonsensitive_leet_token_count": len(nonsensitive_leet_tokens),
        "nonsensitive_leet_ratio": len(nonsensitive_leet_tokens) / max(len(tokens), 1),
        "digit_ratio": sum(ch.isdigit() for ch in chars) / max(len(chars), 1),
        "symbol_ratio": sum((not ch.isalnum()) for ch in chars) / max(len(chars), 1),
        "separator_token_count": len(SEPARATOR_RE.findall(protected)),
        "mid_upper_count": len(MID_UPPER_RE.findall(protected)),
        "diacritic_count": len(VN_DIACRITIC_RE.findall(str(text))),
    }


def add_flags(df: pd.DataFrame) -> pd.DataFrame:
    level1_mask = df["level"].eq(LEVEL1)
    level2_mask = df["level"].eq(LEVEL2)
    df["boundary_flag"] = ""

    # LEVEL 1 should be sparse. Rows with high leet density or many non-sensitive
    # leet tokens look closer to repaired LEVEL 2 than to light filter evasion.
    df.loc[
        level1_mask
        & (
            (df["leet_token_ratio"] >= 0.35)
            | (df["nonsensitive_leet_token_count"] >= 5)
            | (df["leet_token_count"] >= 8)
        ),
        "boundary_flag",
    ] = "level1_too_heavy"

    # LEVEL 2 should be targeted. Rows with very low leet density or weak
    # sensitive-term coverage look like LEVEL 1, while very high non-sensitive
    # density is still over-leeted after repair.
    df.loc[
        level2_mask
        & (
            (df["leet_token_ratio"] <= 0.25)
            & (df["leet_sensitive_token_count"] <= 2)
        ),
        "boundary_flag",
    ] = "level2_too_mild"

    df.loc[
        level2_mask
        & (
            (df["leet_token_ratio"] >= 0.75)
            & (df["nonsensitive_leet_token_count"] >= 6)
        ),
        "boundary_flag",
    ] = "level2_still_overleeted"

    df.loc[
        level2_mask
        & (df["separator_token_count"] >= 4)
        & (df["symbol_ratio"] >= 0.12),
        "boundary_flag",
    ] = "level2_separator_dominant"

    return df


def sample_rows(df: pd.DataFrame) -> pd.DataFrame:
    parts = []
    for flag, group in df[df["boundary_flag"].ne("")].groupby("boundary_flag"):
        parts.append(group.sort_values("leet_token_ratio", ascending=False).head(40))
    for level, group in df.groupby("level"):
        parts.append(group.sample(min(25, len(group)), random_state=42))
    out = pd.concat(parts, ignore_index=False).drop_duplicates()
    cols = [
        "row_index",
        "level",
        "category",
        "boundary_flag",
        "leet_token_count",
        "leet_token_ratio",
        "sensitive_token_count",
        "leet_sensitive_token_count",
        "sensitive_leet_coverage",
        "nonsensitive_leet_token_count",
        "nonsensitive_leet_ratio",
        "separator_token_count",
        "mid_upper_count",
        "symbol_ratio",
        "content",
    ]
    return out[cols].sort_values(["boundary_flag", "level", "category", "leet_token_ratio"], ascending=[True, True, True, False])


def main() -> None:
    df = pd.read_csv(DATA_PATH)
    sub = df[df["level"].isin([LEVEL1, LEVEL2])].copy()
    sub.insert(0, "row_index", sub.index)

    feature_df = pd.DataFrame([metrics(text) for text in sub["content"]], index=sub.index)
    sub = pd.concat([sub, feature_df], axis=1)
    sub = add_flags(sub)

    borderline = sample_rows(sub)
    borderline.to_csv(BORDERLINE_PATH, index=False, encoding="utf-8-sig")

    metric_cols = [
        "token_count",
        "leet_token_count",
        "leet_token_ratio",
        "sensitive_token_count",
        "leet_sensitive_token_count",
        "sensitive_leet_coverage",
        "nonsensitive_leet_token_count",
        "nonsensitive_leet_ratio",
        "separator_token_count",
        "mid_upper_count",
        "digit_ratio",
        "symbol_ratio",
        "diacritic_count",
    ]
    by_level = sub.groupby("level")[metric_cols].agg(["mean", "median"]).round(3)
    by_category = (
        sub.groupby(["category", "level"])[
            ["leet_token_ratio", "sensitive_leet_coverage", "nonsensitive_leet_ratio", "separator_token_count"]
        ]
        .mean()
        .round(3)
        .reset_index()
    )
    flag_counts = pd.crosstab(sub["level"], sub["boundary_flag"].replace("", "ok"))
    cat_counts = pd.crosstab(sub["category"], sub["level"])

    examples = []
    for flag in ["level1_too_heavy", "level2_too_mild", "level2_still_overleeted", "level2_separator_dominant"]:
        rows = sub[sub["boundary_flag"].eq(flag)].sort_values("leet_token_ratio", ascending=False).head(5)
        if rows.empty:
            continue
        examples.append(f"### {flag}")
        examples.append("")
        for _, row in rows.iterrows():
            examples.append(
                f"- row {int(row['row_index'])} | {row['category']} | "
                f"leet_ratio={row['leet_token_ratio']:.2f} | "
                f"sensitive_coverage={row['sensitive_leet_coverage']:.2f}: {row['content']}"
            )
        examples.append("")

    report = [
        "# LEVEL 1 vs LEVEL 2 Boundary Analysis",
        "",
        "## Purpose",
        "",
        "Put repaired `LEVEL 2` beside current `LEVEL 1` to check whether the boundary is coherent.",
        "",
        "Expected boundary:",
        "",
        "- `LEVEL 1`: sparse intentional homoglyphs, mostly 1-2 sensitive terms, little secondary camouflage.",
        "- `LEVEL 2`: stronger sensitive-word-focused leet, plus camouflage such as casing/separators/accent loss. Whole-sentence leet should be minority behavior.",
        "",
        "## Row Counts",
        "",
        cat_counts.to_markdown(),
        "",
        "## Metric Summary by Level",
        "",
        by_level.to_markdown(),
        "",
        "## Mean Metrics by Category and Level",
        "",
        by_category.to_markdown(index=False),
        "",
        "## Boundary Flags",
        "",
        flag_counts.to_markdown(),
        "",
        "Flag definitions:",
        "",
        "- `level1_too_heavy`: LEVEL 1 has high leet density or many non-sensitive leet tokens.",
        "- `level2_too_mild`: LEVEL 2 has low leet density and weak sensitive-term obfuscation.",
        "- `level2_still_overleeted`: LEVEL 2 remains dominated by non-sensitive leet.",
        "- `level2_separator_dominant`: LEVEL 2 may behave more like separator/special-char levels.",
        "",
        "## Key Interpretation",
        "",
        "- If `LEVEL 2` mean leet density remains clearly above `LEVEL 1`, the repair preserved a useful severity gap.",
        "- If many `LEVEL 1` rows are flagged as too heavy, the main remaining issue is not only LEVEL 2. LEVEL 1 may also need a softening pass or metadata relabeling.",
        "- If `LEVEL 2` has high sensitive-term coverage but only moderate non-sensitive leet, the repaired style matches the intended targeted-obfuscation definition.",
        "- Rows in the borderline CSV should be manually reviewed before any second correction pass.",
        "",
        "## Example Borderline Rows",
        "",
        *examples,
        "## Output",
        "",
        f"Manual review rows: `{BORDERLINE_PATH.relative_to(ROOT)}`",
        "",
    ]
    REPORT_PATH.write_text("\n".join(report), encoding="utf-8")

    print(f"Analyzed {len(sub)} rows")
    print(f"Wrote {REPORT_PATH}")
    print(f"Wrote {BORDERLINE_PATH}")
    print(flag_counts.to_string())


if __name__ == "__main__":
    main()

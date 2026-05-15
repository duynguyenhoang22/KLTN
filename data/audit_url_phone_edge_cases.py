"""
Build a manual-review queue for URL and phone metadata edge cases.

This script does not modify any dataset. It filters synthetic rows where the
current strict validator may be too conservative or where metadata should be
double-checked semantically by a human reviewer.

Outputs:
    data/reports/url_phone_edge_case_review.csv
    data/reports/url_phone_edge_case_priority_review.csv
    data/reports/url_phone_edge_case_summary.md

Run from repository root:
    python data/audit_url_phone_edge_cases.py
"""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

from validate_synthetic import has_phone, has_url


ROOT = Path(__file__).resolve().parents[1]
SYNTHETIC_DIR = ROOT / "data" / "synthetic"
REPORT_DIR = ROOT / "data" / "reports"
REVIEW_PATH = REPORT_DIR / "url_phone_edge_case_review.csv"
PRIORITY_REVIEW_PATH = REPORT_DIR / "url_phone_edge_case_priority_review.csv"
SUMMARY_PATH = REPORT_DIR / "url_phone_edge_case_summary.md"

DATASETS = [
    SYNTHETIC_DIR / "synthetic_label_0.csv",
    SYNTHETIC_DIR / "synthetic_label_1.csv",
]

URL_TLDS = (
    "vn|com|net|org|me|ly|top|vip|icu|cc|club|life|xyz|xin|us|link|app|site|"
    "online|info|io|co|gov|edu|tech|bet|fun|live|click|store|shop|win"
)
BROKEN_URL_TLDS = (
    "vn|com|net|org|me|ly|top|vip|icu|cc|club|life|xyz|xin|us|link|app|site|"
    "online|info|io|gov|edu|tech|bet|fun|live|click|store|shop|win"
)

URL_CUE_RE = re.compile(
    r"(?i)\b("
    r"link|l[ií]nk|truy\s*c[aậ]p|v[aà]o|b[aấ]m|nh[aấ]n|"
    r"[dđ][aă]ng\s*nh[aậ]p|login|website|web|t[aả]i|tại|"
    r"x[aá]c\s*th[uự]c|nh[aậ]n\s*qu[aà]|telegram|zalo"
    r")\b"
)

BROKEN_URL_PATTERNS = {
    "bracket-dot domain": re.compile(
        rf"(?i)\b[a-z0-9][a-z0-9-]{{2,}}\s*(?:\[.\]|\(\.\))\s*(?:{BROKEN_URL_TLDS})\b"
    ),
    "word-dot domain": re.compile(
        rf"(?i)\b[a-z0-9][a-z0-9-]{{2,}}\s+(?:dot|cham|chấm)\s+(?:{BROKEN_URL_TLDS})\b"
    ),
    "space-before-dot domain": re.compile(
        rf"(?i)\b[a-z0-9][a-z0-9-]{{2,}}\s+\.\s*(?:{BROKEN_URL_TLDS})\b"
    ),
    "hxxp scheme": re.compile(r"(?i)\bhxxps?\s*:\s*/\s*/\s*\S+"),
    "missing-colon scheme": re.compile(r"(?i)\bhttps?\s*/\s*/\s*\S+"),
    "unsupported-tld domain path": re.compile(
        r"(?i)\b[a-z0-9][a-z0-9-]{1,}\.[a-z]{2,}/[^\s]+"
    ),
    "leet-tld domain": re.compile(
        r"(?i)\b[a-z0-9][a-z0-9-]{1,}\.(?:t0p|v1p|c0m|x[yv]z|1cu)\b(?:/[^\s]+)?"
    ),
    "char-spaced domain": re.compile(
        r"(?i)(?:\b[a-z0-9]\s*[._-]\s*){4,}[a-z0-9]\s*[._-]\s*"
        r"(?:c\s*[._-]?\s*c|v\s*[._-]?\s*n|c\s*[._-]?\s*o\s*[._-]?\s*m)\b"
    ),
}

PHONE_CUE_RE = re.compile(
    r"(?i)\b("
    r"lh|lien\s*he|li[eê]n\s*h[eệ]|hotline|tong\s*dai|t[oổ]ng\s*[dđ][aà]i|"
    r"call|zalo|sdt|s[đd]t|dt|[đd]t|g[oọ]i|soan|so[aạ]n|gui|g[uử]i|"
    r"ket\s*ban|k[eế]t\s*b[aạ]n"
    r")\b"
)

PHONE_LIKE_PATTERNS = {
    "symbol-separated contact": re.compile(
        r"(?<!\d)(?:\d\s*[>/|:;.,_\-]\s*){5,}\d(?!\d)"
    ),
    "spaced mobile/contact": re.compile(
        r"(?<!\d)(?:\+?84|0)(?:\s+\d){7,10}(?!\d)"
    ),
    "zalo numeric cue": re.compile(
        r"(?i)\bzalo\b.{0,20}(?:\+?84|0)?(?:[\s.>:_-]?\d){8,11}"
    ),
    "shortcode command": re.compile(
        r"(?i)\b(?:soan|so[aạ]n|tc|huy|kt|dk)\b(?:\s+\w+){0,4}\s+g[uử]i\s+\d{3,6}\b"
    ),
}

NON_CONTACT_CONTEXT_RE = re.compile(
    r"(?i)\b("
    r"otp|cccd|cmnd|cmt|c[aă]n\s*c[uư][oơ]c|stk|t[aà]i\s*kho[aả]n|"
    r"ma\s*don|m[aã]\s*[dđ][oơ]n|don\s*hang|[dđ][oơ]n\s*h[aà]ng|"
    r"tracking|v[aậ]n\s*[dđ][oơ]n|ref|mgd|ma\s*gd"
    r")\b"
)


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, encoding="utf-8-sig")


def matched_names(patterns: dict[str, re.Pattern[str]], text: str) -> list[str]:
    return [name for name, pattern in patterns.items() if pattern.search(text)]


def add_candidate(
    rows: list[dict[str, object]],
    row: pd.Series,
    dataset: str,
    row_index: int,
    issue_type: str,
    reason: str,
    review_priority: str,
) -> None:
    rows.append(
        {
            "dataset": dataset,
            "row_index": row_index,
            "issue_type": issue_type,
            "review_priority": review_priority,
            "reason": reason,
            "has_url": row.get("has_url"),
            "validator_has_url": int(has_url(str(row.get("content", "")))),
            "has_phone_number": row.get("has_phone_number"),
            "validator_has_phone": int(has_phone(str(row.get("content", "")))),
            "label": row.get("label"),
            "sender_type": row.get("sender_type"),
            "category": row.get("category", ""),
            "level": row.get("level", ""),
            "human_decision": "",
            "notes": "",
            "content": str(row.get("content", "")),
        }
    )


def build_review() -> pd.DataFrame:
    candidates: list[dict[str, object]] = []
    seen: set[tuple[str, int, str, str]] = set()

    for path in DATASETS:
        df = read_csv(path)
        dataset = path.stem
        for row_index, row in df.iterrows():
            text = str(row.get("content", ""))
            has_url_meta = int(row.get("has_url", 0))
            has_phone_meta = int(row.get("has_phone_number", 0))

            broken_url_hits = matched_names(BROKEN_URL_PATTERNS, text)
            if has_url_meta == 0 and broken_url_hits:
                reason = "; ".join(broken_url_hits)
                key = (dataset, row_index, "possible missed URL", reason)
                if key not in seen:
                    priority = "high" if URL_CUE_RE.search(text) else "medium"
                    add_candidate(
                        candidates,
                        row,
                        dataset,
                        row_index,
                        "possible missed URL",
                        reason,
                        priority,
                    )
                    seen.add(key)

            if has_url_meta == 0 and URL_CUE_RE.search(text):
                reason = "URL/CTA cue but metadata has_url=0"
                key = (dataset, row_index, "URL cue without detected URL", reason)
                if key not in seen:
                    priority = "medium" if re.search(r"(?i)\b(link|website|web|login|telegram|zalo)\b", text) else "low"
                    add_candidate(
                        candidates,
                        row,
                        dataset,
                        row_index,
                        "URL cue without detected URL",
                        reason,
                        priority,
                    )
                    seen.add(key)

            phone_hits = matched_names(PHONE_LIKE_PATTERNS, text)
            if has_phone_meta == 0 and phone_hits:
                reason = "; ".join(phone_hits)
                key = (dataset, row_index, "possible missed phone", reason)
                if key not in seen:
                    add_candidate(
                        candidates,
                        row,
                        dataset,
                        row_index,
                        "possible missed phone",
                        reason,
                        "high",
                    )
                    seen.add(key)

            if has_phone_meta == 0 and PHONE_CUE_RE.search(text):
                reason = "phone/contact cue but has_phone_number=0"
                key = (dataset, row_index, "phone cue without detected number", reason)
                if key not in seen:
                    priority = "medium" if re.search(r"(?i)\b(lh|hotline|zalo|sdt|s[đd]t|dt|[đd]t)\b", text) else "low"
                    add_candidate(
                        candidates,
                        row,
                        dataset,
                        row_index,
                        "phone cue without detected number",
                        reason,
                        priority,
                    )
                    seen.add(key)

            if has_phone_meta == 1 and NON_CONTACT_CONTEXT_RE.search(text) and not PHONE_CUE_RE.search(text):
                reason = "non-contact ID context near a row marked has_phone_number=1"
                key = (dataset, row_index, "possible false phone positive", reason)
                if key not in seen:
                    add_candidate(
                        candidates,
                        row,
                        dataset,
                        row_index,
                        "possible false phone positive",
                        reason,
                        "high",
                    )
                    seen.add(key)

    review = pd.DataFrame(candidates)
    if review.empty:
        return pd.DataFrame(
            columns=[
                "dataset",
                "row_index",
                "issue_type",
                "review_priority",
                "reason",
                "has_url",
                "validator_has_url",
                "has_phone_number",
                "validator_has_phone",
                "label",
                "sender_type",
                "category",
                "level",
                "human_decision",
                "notes",
                "content",
            ]
        )

    order = {
        "possible missed URL": 0,
        "URL cue without detected URL": 1,
        "possible missed phone": 2,
        "phone cue without detected number": 3,
        "possible false phone positive": 4,
    }
    priority_order = {"high": 0, "medium": 1, "low": 2}
    review["sort_key"] = review["issue_type"].map(order).fillna(99)
    review["priority_key"] = review["review_priority"].map(priority_order).fillna(99)
    review = review.sort_values(["priority_key", "sort_key", "dataset", "row_index"]).drop(
        columns=["sort_key", "priority_key"]
    )
    return review


def markdown_table(df: pd.DataFrame, max_rows: int = 20) -> str:
    if df.empty:
        return "_No rows._"
    return df.head(max_rows).to_markdown(index=False)


def write_summary(review: pd.DataFrame, priority_review: pd.DataFrame) -> None:
    lines: list[str] = []
    lines.append("# URL/Phone Edge Case Manual Review\n\n")
    lines.append("Generated by `data/audit_url_phone_edge_cases.py`.\n\n")
    lines.append("This report is a manual-review queue, not an automatic correction list.\n\n")
    lines.append(f"- Review CSV: `{REVIEW_PATH.relative_to(ROOT)}`\n")
    lines.append(f"- Priority review CSV: `{PRIORITY_REVIEW_PATH.relative_to(ROOT)}`\n")
    lines.append(f"- Total candidate rows: {len(review)}\n\n")
    lines.append(f"- High-priority candidate rows: {len(priority_review)}\n\n")

    if not review.empty:
        lines.append("## Candidate Counts\n\n")
        counts = (
            review.groupby(["review_priority", "dataset", "issue_type"])
            .size()
            .reset_index(name="count")
            .sort_values(["review_priority", "dataset", "issue_type"])
        )
        lines.append(counts.to_markdown(index=False))
        lines.append("\n\n")

        lines.append("## How To Label `human_decision`\n\n")
        lines.append("- `ok`: metadata is acceptable as-is.\n")
        lines.append("- `should_has_url_1`: human reader would treat this as a URL/link target.\n")
        lines.append("- `should_has_phone_1`: human reader would treat this as a contactable number.\n")
        lines.append("- `should_has_phone_0`: number is an OTP, account, ID, order, tracking, or reference code.\n")
        lines.append("- `unclear`: needs discussion before correction.\n\n")

        lines.append("## Sample Rows\n\n")
        sample_cols = [
            "dataset",
            "row_index",
            "issue_type",
            "review_priority",
            "reason",
            "has_url",
            "has_phone_number",
            "category",
            "level",
            "content",
        ]
        lines.append(markdown_table(review[sample_cols], max_rows=30))
        lines.append("\n")

    SUMMARY_PATH.write_text("".join(lines), encoding="utf-8")


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    review = build_review()
    priority_review = review[review["review_priority"].eq("high")].copy()
    review.to_csv(REVIEW_PATH, index=False, encoding="utf-8-sig")
    priority_review.to_csv(PRIORITY_REVIEW_PATH, index=False, encoding="utf-8-sig")
    write_summary(review, priority_review)
    print(f"Wrote review CSV: {REVIEW_PATH}")
    print(f"Wrote priority review CSV: {PRIORITY_REVIEW_PATH}")
    print(f"Wrote summary: {SUMMARY_PATH}")
    print(f"Candidate rows: {len(review)}")
    print(f"High-priority candidate rows: {len(priority_review)}")


if __name__ == "__main__":
    main()

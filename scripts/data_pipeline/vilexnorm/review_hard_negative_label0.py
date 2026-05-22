"""Manually review ViLexNorm hard-negative candidates into curated label-0 rows.

Run from the repository root:
    python scripts/data_pipeline/vilexnorm/review_hard_negative_label0.py

Controls:
    y / enter  accept row into the curated label-0 output
    n          reject row and save the decision in the review log
    s          skip for now
    q          save and quit

The curated output contains only accepted rows. The review log keeps both
accepted and rejected decisions so the script can resume without re-reviewing
rows that were already handled.
"""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
from pathlib import Path
import textwrap


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_INPUT = ROOT / "data/external/vilexnorm/processed/vilexnorm_hard_negative_candidates.csv"
DEFAULT_OUTPUT = ROOT / "data/external/vilexnorm/curated/vilexnorm_hard_negative_label0.csv"
DEFAULT_REVIEW_LOG = ROOT / "data/external/vilexnorm/curated/vilexnorm_hard_negative_review_log.csv"

OUTPUT_FIELDS = [
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
    "source_file",
    "source_row_id",
    "external_source_type",
    "text_variant_type",
    "hard_case_type",
    "review_status",
    "original",
    "normalized",
]

LOG_FIELDS = [
    "review_key",
    "sample_id",
    "decision",
    "review_note",
    "reviewed_at",
    "source_dataset",
    "source_file",
    "source_row_id",
    "content",
    "normalized",
    "hard_case_type",
    "flags",
    "filter_reason",
    "reject_reason",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def review_key(row: dict[str, str]) -> str:
    return "|".join(
        [
            row.get("source_dataset", ""),
            row.get("source_file", ""),
            row.get("source_row_id", ""),
            row.get("original", ""),
        ]
    )


def make_sample_id(position: int) -> str:
    return f"vilexnorm_hardneg_{position:05d}"


def to_output_row(row: dict[str, str], sample_id: str) -> dict[str, str]:
    return {
        "sample_id": sample_id,
        "content": row.get("content", ""),
        "label": "0",
        "has_url": row.get("has_url", "0"),
        "has_phone_number": row.get("has_phone_number", "0"),
        "sender_type": row.get("sender_type", ""),
        "category": row.get("category", ""),
        "obfuscation_level": row.get("obfuscation_level", ""),
        "data_origin": row.get("data_origin", ""),
        "source_dataset": row.get("source_dataset", ""),
        "source_file": row.get("source_file", ""),
        "source_row_id": row.get("source_row_id", ""),
        "external_source_type": row.get("external_source_type", ""),
        "text_variant_type": row.get("text_variant_type", ""),
        "hard_case_type": row.get("hard_case_type", ""),
        "review_status": "manual_accepted",
        "original": row.get("original", ""),
        "normalized": row.get("normalized", ""),
    }


def to_log_row(
    row: dict[str, str],
    key: str,
    sample_id: str,
    decision: str,
    review_note: str,
) -> dict[str, str]:
    return {
        "review_key": key,
        "sample_id": sample_id,
        "decision": decision,
        "review_note": review_note,
        "reviewed_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source_dataset": row.get("source_dataset", ""),
        "source_file": row.get("source_file", ""),
        "source_row_id": row.get("source_row_id", ""),
        "content": row.get("content", ""),
        "normalized": row.get("normalized", ""),
        "hard_case_type": row.get("hard_case_type", ""),
        "flags": row.get("flags", ""),
        "filter_reason": row.get("filter_reason", ""),
        "reject_reason": row.get("reject_reason", ""),
    }


def wrap(value: str, width: int) -> str:
    if not value:
        return ""
    return "\n".join(textwrap.wrap(value, width=width, replace_whitespace=False))


def print_candidate(row: dict[str, str], index: int, total: int, sample_id: str, width: int) -> None:
    print("\n" + "=" * min(width, 100))
    print(f"[{index}/{total}] {sample_id}")
    print(f"source: {row.get('source_file', '')}#{row.get('source_row_id', '')} | split={row.get('split', '')}")
    print(f"type: {row.get('hard_case_type', '')} | variants: {row.get('text_variant_type', '')}")
    print(f"flags: {row.get('flags', '')}")
    print(f"filter_reason: {row.get('filter_reason', '')}")
    if row.get("reject_reason"):
        print(f"reject_reason: {row.get('reject_reason', '')}")
    print("-" * min(width, 100))
    print("ORIGINAL:")
    print(wrap(row.get("original", ""), width))
    print("\nNORMALIZED:")
    print(wrap(row.get("normalized", ""), width))
    if row.get("content") and row.get("content") != row.get("original"):
        print("\nCONTENT:")
        print(wrap(row.get("content", ""), width))


def prompt_decision(default_accept: bool) -> tuple[str, str]:
    prompt = "[Y] accept / [n] reject / [s] skip / [q] quit"
    try:
        raw = input(f"{prompt}: ").replace("\x00", "").strip().strip("'\"")
    except EOFError:
        return "quit", ""
    if not raw and default_accept:
        raw = "y"
    decision = raw[:1].lower()
    if decision == "y":
        try:
            note = input("note (optional): ").strip()
        except EOFError:
            note = ""
        return "accept", note
    if decision == "n":
        try:
            note = input("reject note (optional): ").strip()
        except EOFError:
            note = ""
        return "reject", note
    if decision == "s":
        return "skip", ""
    if decision == "q":
        return "quit", ""
    print("Unknown choice. Use y, n, s, or q.")
    return prompt_decision(default_accept)


def build_reviewed_keys(output_rows: list[dict[str, str]], log_rows: list[dict[str, str]]) -> set[str]:
    keys = {row.get("review_key", "") for row in log_rows if row.get("review_key")}
    for row in output_rows:
        key = review_key(row)
        if key.strip("|"):
            keys.add(key)
    return keys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT, help="Candidate CSV to review.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Curated label-0 CSV to write.")
    parser.add_argument("--review-log", type=Path, default=DEFAULT_REVIEW_LOG, help="Decision log for resume.")
    parser.add_argument("--start-at", type=int, default=1, help="1-based candidate position to start from.")
    parser.add_argument("--limit", type=int, default=0, help="Maximum number of unreviewed rows to show; 0 means all.")
    parser.add_argument("--width", type=int, default=100, help="Text wrap width for display.")
    parser.add_argument(
        "--no-default-accept",
        action="store_true",
        help="Require typing y to accept instead of treating enter as accept.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    candidates = read_csv(args.input)
    if not candidates:
        raise SystemExit(f"No candidates found: {args.input}")

    output_rows = read_csv(args.output)
    log_rows = read_csv(args.review_log)
    reviewed = build_reviewed_keys(output_rows, log_rows)

    shown = 0
    accepted = 0
    rejected = 0
    skipped = 0
    made_decision = False
    total = len(candidates)

    print(f"Input: {args.input}")
    print(f"Output: {args.output}")
    print(f"Review log: {args.review_log}")
    print(f"Candidates: {total} | already reviewed: {len(reviewed)}")

    for index, row in enumerate(candidates, start=1):
        if index < args.start_at:
            continue
        key = review_key(row)
        if key in reviewed:
            continue
        if args.limit and shown >= args.limit:
            break

        sample_id = make_sample_id(index)
        print_candidate(row, index, total, sample_id, args.width)
        decision, note = prompt_decision(default_accept=not args.no_default_accept)

        if decision == "quit":
            break
        if decision == "skip":
            skipped += 1
            shown += 1
            continue

        log_rows.append(to_log_row(row, key, sample_id, decision, note))
        reviewed.add(key)
        made_decision = True
        if decision == "accept":
            output_rows.append(to_output_row(row, sample_id))
            accepted += 1
        elif decision == "reject":
            rejected += 1

        write_csv(args.output, output_rows, OUTPUT_FIELDS)
        write_csv(args.review_log, log_rows, LOG_FIELDS)
        shown += 1

    if made_decision:
        write_csv(args.output, output_rows, OUTPUT_FIELDS)
        write_csv(args.review_log, log_rows, LOG_FIELDS)
    print("\nDone.")
    print(f"Shown this run: {shown}")
    print(f"Accepted this run: {accepted}")
    print(f"Rejected this run: {rejected}")
    print(f"Skipped this run: {skipped}")
    print(f"Curated output rows: {len(output_rows)}")


if __name__ == "__main__":
    main()

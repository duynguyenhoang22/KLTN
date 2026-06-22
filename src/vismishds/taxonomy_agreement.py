from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


ALLOWED_DECISIONS = {"accept", "rename", "merge", "split", "remove"}


def read_taxonomy_review(
    path: Path,
    reviewer: str,
) -> tuple[dict[tuple[str, str], dict[str, str]], list[str]]:
    records: dict[tuple[str, str], dict[str, str]] = {}
    errors: list[str] = []
    with path.open(encoding="utf-8-sig", newline="") as handle:
        for line_number, row in enumerate(csv.DictReader(handle), start=2):
            field = row.get("field", "").strip()
            value = row.get("value", "").strip()
            decision = row.get("decision", "").strip().lower()
            proposal = row.get("proposed_value_or_target", "").strip()
            comment = row.get("comment", "").strip()
            key = (field, value)
            row["decision"] = decision
            row["proposed_value_or_target"] = proposal
            row["comment"] = comment

            if key in records:
                errors.append(f"{reviewer}: duplicate {field}.{value}")
            if decision not in ALLOWED_DECISIONS:
                errors.append(
                    f"{reviewer} {field}.{value} line {line_number}: "
                    f"invalid/blank decision {decision!r}"
                )
            if decision in {"rename", "merge", "split"} and not proposal:
                errors.append(
                    f"{reviewer} {field}.{value} line {line_number}: "
                    f"{decision} requires proposed_value_or_target"
                )
            if decision != "accept" and not comment:
                errors.append(
                    f"{reviewer} {field}.{value} line {line_number}: "
                    "non-accept decision requires comment"
                )
            records[key] = row
    return records, errors


def compare_taxonomy_reviews(
    reviewer_a_path: Path,
    reviewer_b_path: Path,
) -> tuple[dict[str, object], list[dict[str, str]], list[str]]:
    a, errors_a = read_taxonomy_review(reviewer_a_path, "reviewer_a")
    b, errors_b = read_taxonomy_review(reviewer_b_path, "reviewer_b")
    errors = errors_a + errors_b
    if set(a) != set(b):
        errors.append("review sheets contain different field/value sets")

    rows: list[dict[str, str]] = []
    decisions = Counter()
    exact_agreement = 0
    common = sorted(set(a) & set(b))
    for field, value in common:
        left = a[(field, value)]
        right = b[(field, value)]
        same_decision = left["decision"] == right["decision"]
        same_proposal = (
            left["proposed_value_or_target"].strip().lower()
            == right["proposed_value_or_target"].strip().lower()
        )
        exact = same_decision and (
            left["decision"] in {"accept", "remove"} or same_proposal
        )
        exact_agreement += int(exact)
        decisions[(left["decision"], right["decision"])] += 1
        needs_queue = (
            not exact
            or left["decision"] != "accept"
            or right["decision"] != "accept"
            or not left["decision"]
            or not right["decision"]
        )
        if needs_queue:
            reasons: list[str] = []
            if not same_decision:
                reasons.append("decision_disagreement")
            elif not exact:
                reasons.append("proposal_disagreement")
            if left["decision"] != "accept":
                reasons.append("reviewer_a_change")
            if right["decision"] != "accept":
                reasons.append("reviewer_b_change")
            if not left["decision"] or not right["decision"]:
                reasons.append("incomplete_review")
            rows.append({
                "field": field,
                "value": value,
                "reviewer_a_decision": left["decision"],
                "reviewer_a_proposal": left["proposed_value_or_target"],
                "reviewer_a_comment": left["comment"],
                "reviewer_b_decision": right["decision"],
                "reviewer_b_proposal": right["proposed_value_or_target"],
                "reviewer_b_comment": right["comment"],
                "queue_reason": "|".join(reasons),
                "final_decision": "",
                "final_value_or_target": "",
                "adjudication_comment": "",
            })

    summary: dict[str, object] = {
        "items": len(common),
        "exact_agreement": exact_agreement,
        "exact_agreement_rate": exact_agreement / len(common) if common else 0,
        "queue_items": len(rows),
        "decision_pairs": dict(decisions),
        "validation_errors": len(errors),
    }
    return summary, rows, errors


def write_taxonomy_adjudication(
    summary: dict[str, object],
    queue: list[dict[str, str]],
    errors: list[str],
    queue_path: Path,
    report_path: Path,
) -> None:
    queue_path.parent.mkdir(parents=True, exist_ok=True)
    if queue:
        with queue_path.open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(queue[0]))
            writer.writeheader()
            writer.writerows(queue)

    lines = [
        "# Báo cáo review taxonomy P0.2",
        "",
        f"- Tổng field/value: {summary['items']}",
        f"- Exact agreement: {summary['exact_agreement']} "
        f"({summary['exact_agreement_rate'] * 100:.1f}%)",
        f"- Mục vào adjudication queue: {summary['queue_items']}",
        f"- Lỗi review sheet: {summary['validation_errors']}",
        "",
        "## Cặp decision",
        "",
        "| Reviewer A | Reviewer B | Số lượng |",
        "|---|---|---:|",
    ]
    for pair, count in sorted(
        summary["decision_pairs"].items(),
        key=lambda item: (-item[1], item[0]),
    ):
        lines.append(f"| {pair[0] or '(blank)'} | {pair[1] or '(blank)'} | {count} |")
    lines.extend(["", "## Lỗi cần sửa trước khi khóa", ""])
    if errors:
        lines.extend(f"- {error}" for error in errors)
    else:
        lines.append("- Không có.")
    lines.extend([
        "",
        "## Cách adjudicate",
        "",
        "Hai reviewer chỉ cần thảo luận các dòng trong queue và điền ba cột cuối. "
        "Các mục cả hai cùng `accept` không xuất hiện trong queue.",
        "",
    ])
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines), encoding="utf-8")

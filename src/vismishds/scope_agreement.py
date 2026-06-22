from __future__ import annotations

import csv
from collections import Counter, defaultdict
from pathlib import Path


ALLOWED_DECISIONS = {
    "accepted",
    "needs_adjudication",
    "excluded_out_of_scope_malicious",
    "excluded_language_scope",
    "excluded_insufficient_context",
    "excluded_invalid_record",
    "excluded_privacy_or_safety",
}
ALLOWED_CONFIDENCE = {"high", "medium", "low"}
ALLOWED_FINAL_DECISIONS = ALLOWED_DECISIONS - {"needs_adjudication"}


def _discussion(value: str) -> str:
    normalized = str(value).strip().lower()
    if normalized in {"0", "0.0", "false", "no"}:
        return "0"
    if normalized in {"1", "1.0", "true", "yes"}:
        return "1"
    return normalized


def _effective_outcome(row: dict[str, str]) -> str:
    if row["scope_decision"] == "accepted":
        return f"accepted_label_{row['proposed_label']}"
    return row["scope_decision"]


def _cohen_kappa(pairs: list[tuple[str, str]]) -> float | None:
    if not pairs:
        return None
    total = len(pairs)
    observed = sum(left == right for left, right in pairs) / total
    left_counts = Counter(left for left, _ in pairs)
    right_counts = Counter(right for _, right in pairs)
    labels = set(left_counts) | set(right_counts)
    expected = sum(
        (left_counts[label] / total) * (right_counts[label] / total)
        for label in labels
    )
    if expected == 1:
        return 1.0 if observed == 1 else None
    return (observed - expected) / (1 - expected)


def read_and_validate(path: Path, annotator: str) -> tuple[dict[str, dict[str, str]], list[str]]:
    records: dict[str, dict[str, str]] = {}
    errors: list[str] = []
    with path.open(encoding="utf-8-sig", newline="") as handle:
        for line_number, row in enumerate(csv.DictReader(handle), start=2):
            sample_id = row.get("sample_id", "").strip()
            decision = row.get("scope_decision", "").strip()
            label = row.get("proposed_label", "").strip()
            confidence = row.get("confidence", "").strip().lower()
            discussion = _discussion(row.get("needs_discussion", ""))
            row["scope_decision"] = decision
            row["proposed_label"] = label
            row["confidence"] = confidence
            row["needs_discussion"] = discussion

            if not sample_id:
                errors.append(f"{annotator} line {line_number}: blank sample_id")
                continue
            if sample_id in records:
                errors.append(f"{annotator}: duplicate sample_id {sample_id}")
            if decision not in ALLOWED_DECISIONS:
                errors.append(
                    f"{annotator} {sample_id}: invalid scope_decision {decision!r}"
                )
            if decision == "accepted" and label not in {"0", "1"}:
                errors.append(
                    f"{annotator} {sample_id}: accepted requires label 0 or 1"
                )
            if decision != "accepted" and label:
                errors.append(
                    f"{annotator} {sample_id}: non-accepted decision must have blank label"
                )
            if confidence and confidence not in ALLOWED_CONFIDENCE:
                errors.append(
                    f"{annotator} {sample_id}: invalid confidence {confidence!r}"
                )
            if not confidence:
                errors.append(f"{annotator} {sample_id}: blank confidence")
            if discussion not in {"0", "1"}:
                errors.append(
                    f"{annotator} {sample_id}: invalid needs_discussion {discussion!r}"
                )
            if not row.get("reason", "").strip():
                errors.append(f"{annotator} {sample_id}: blank reason")
            records[sample_id] = row
    return records, errors


def compare_annotations(
    annotator_a_path: Path,
    annotator_b_path: Path,
    key_path: Path,
) -> tuple[dict[str, object], list[dict[str, str]], list[str]]:
    a_records, a_errors = read_and_validate(annotator_a_path, "annotator_a")
    b_records, b_errors = read_and_validate(annotator_b_path, "annotator_b")
    errors = a_errors + b_errors
    if set(a_records) != set(b_records):
        only_a = sorted(set(a_records) - set(b_records))
        only_b = sorted(set(b_records) - set(a_records))
        errors.append(f"sample set mismatch; only A={only_a}, only B={only_b}")

    key: dict[str, dict[str, str]] = {}
    with key_path.open(encoding="utf-8-sig", newline="") as handle:
        key = {row["sample_id"]: row for row in csv.DictReader(handle)}

    common_ids = sorted(set(a_records) & set(b_records))
    rows: list[dict[str, str]] = []
    scope_pairs: list[tuple[str, str]] = []
    outcome_pairs: list[tuple[str, str]] = []
    joint_label_pairs: list[tuple[str, str]] = []
    by_group: dict[str, dict[str, int]] = defaultdict(
        lambda: {"n": 0, "scope_agree": 0, "outcome_agree": 0}
    )

    for sample_id in common_ids:
        a = a_records[sample_id]
        b = b_records[sample_id]
        meta = key.get(sample_id, {})
        group = meta.get("challenge_group", "unknown")
        a_outcome = _effective_outcome(a)
        b_outcome = _effective_outcome(b)
        scope_agree = a["scope_decision"] == b["scope_decision"]
        outcome_agree = a_outcome == b_outcome
        both_accepted = (
            a["scope_decision"] == "accepted"
            and b["scope_decision"] == "accepted"
        )
        if both_accepted:
            joint_label_pairs.append((a["proposed_label"], b["proposed_label"]))
        scope_pairs.append((a["scope_decision"], b["scope_decision"]))
        outcome_pairs.append((a_outcome, b_outcome))
        by_group[group]["n"] += 1
        by_group[group]["scope_agree"] += int(scope_agree)
        by_group[group]["outcome_agree"] += int(outcome_agree)
        flagged = (
            not outcome_agree
            or a["needs_discussion"] == "1"
            or b["needs_discussion"] == "1"
            or a["confidence"] in {"", "low"}
            or b["confidence"] in {"", "low"}
        )
        rows.append({
            "sample_id": sample_id,
            "content": a["content"],
            "challenge_group": group,
            "annotator_a_scope_decision": a["scope_decision"],
            "annotator_a_label": a["proposed_label"],
            "annotator_a_evidence": a.get("evidence", ""),
            "annotator_a_confidence": a["confidence"],
            "annotator_a_reason": a.get("reason", ""),
            "annotator_a_needs_discussion": a["needs_discussion"],
            "annotator_b_scope_decision": b["scope_decision"],
            "annotator_b_label": b["proposed_label"],
            "annotator_b_evidence": b.get("evidence", ""),
            "annotator_b_confidence": b["confidence"],
            "annotator_b_reason": b.get("reason", ""),
            "annotator_b_needs_discussion": b["needs_discussion"],
            "scope_agree": str(int(scope_agree)),
            "effective_outcome_a": a_outcome,
            "effective_outcome_b": b_outcome,
            "effective_outcome_agree": str(int(outcome_agree)),
            "queue_reason": "|".join(filter(None, [
                "outcome_disagreement" if not outcome_agree else "",
                "annotator_a_discussion" if a["needs_discussion"] == "1" else "",
                "annotator_b_discussion" if b["needs_discussion"] == "1" else "",
                "low_or_missing_confidence"
                if a["confidence"] in {"", "low"} or b["confidence"] in {"", "low"}
                else "",
            ])),
            "final_scope_decision": "",
            "final_label": "",
            "adjudication_reason": "",
            "scope_policy_change_required": "",
        })

    scope_agreement = sum(a == b for a, b in scope_pairs) / len(scope_pairs)
    outcome_agreement = sum(a == b for a, b in outcome_pairs) / len(outcome_pairs)
    label_agreement = (
        sum(a == b for a, b in joint_label_pairs) / len(joint_label_pairs)
        if joint_label_pairs else None
    )
    queue = [row for row in rows if row["queue_reason"]]
    metrics: dict[str, object] = {
        "n": len(common_ids),
        "scope_agreement": scope_agreement,
        "scope_kappa": _cohen_kappa(scope_pairs),
        "effective_outcome_agreement": outcome_agreement,
        "effective_outcome_kappa": _cohen_kappa(outcome_pairs),
        "jointly_accepted_n": len(joint_label_pairs),
        "joint_label_agreement": label_agreement,
        "joint_label_kappa": _cohen_kappa(joint_label_pairs),
        "adjudication_queue_n": len(queue),
        "by_group": dict(by_group),
    }
    return metrics, queue, errors


def write_adjudication_outputs(
    metrics: dict[str, object],
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

    def pct(value: object) -> str:
        return "N/A" if value is None else f"{float(value) * 100:.1f}%"

    lines = [
        "# Báo cáo agreement — Scope Challenge P0.1",
        "",
        f"- Số mẫu: {metrics['n']}",
        f"- Scope-decision agreement: {pct(metrics['scope_agreement'])}",
        f"- Scope-decision Cohen's kappa: {metrics['scope_kappa']:.3f}",
        f"- Effective-outcome agreement: {pct(metrics['effective_outcome_agreement'])}",
        f"- Effective-outcome Cohen's kappa: {metrics['effective_outcome_kappa']:.3f}",
        f"- Cùng accepted: {metrics['jointly_accepted_n']}",
        f"- Label agreement khi cùng accepted: {pct(metrics['joint_label_agreement'])}",
        f"- Label Cohen's kappa khi cùng accepted: {metrics['joint_label_kappa']:.3f}",
        f"- Mẫu vào adjudication queue: {metrics['adjudication_queue_n']}",
        "",
        "## Agreement theo nhóm",
        "",
        "| Nhóm | n | Scope agreement | Outcome agreement |",
        "|---|---:|---:|---:|",
    ]
    for group, values in sorted(metrics["by_group"].items()):
        lines.append(
            f"| {group} | {values['n']} | "
            f"{values['scope_agree'] / values['n'] * 100:.1f}% | "
            f"{values['outcome_agree'] / values['n'] * 100:.1f}% |"
        )
    lines.extend(["", "## Lỗi định dạng", ""])
    if errors:
        lines.extend(f"- {error}" for error in errors)
    else:
        lines.append("- Không có.")
    lines.extend([
        "",
        "## Kết luận quality gate",
        "",
        "P0.1 chưa được khóa tự động. Nhóm phải adjudicate toàn bộ queue, bổ sung "
        "confidence còn thiếu và xem các nhóm agreement thấp có yêu cầu sửa "
        "`dataset_scope.md` hay không.",
        "",
    ])
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines), encoding="utf-8")


def validate_completed_adjudication(
    path: Path,
) -> tuple[dict[str, object], list[str], list[dict[str, str]]]:
    errors: list[str] = []
    rows: list[dict[str, str]] = []
    final_counts: Counter[str] = Counter()
    label_counts: Counter[str] = Counter()
    policy_notes: list[dict[str, str]] = []

    with path.open(encoding="utf-8-sig", newline="") as handle:
        for line_number, row in enumerate(csv.DictReader(handle), start=2):
            sample_id = row.get("sample_id", "").strip()
            decision = row.get("final_scope_decision", "").strip()
            label = row.get("final_label", "").strip()
            reason = row.get("adjudication_reason", "").strip()
            policy_value = row.get("scope_policy_change_required", "").strip()
            a_confidence = row.get("annotator_a_confidence", "").strip().lower()
            b_confidence = row.get("annotator_b_confidence", "").strip().lower()

            if decision not in ALLOWED_FINAL_DECISIONS:
                errors.append(
                    f"{sample_id} line {line_number}: invalid final_scope_decision "
                    f"{decision!r}"
                )
            if decision == "accepted" and label not in {"0", "1"}:
                errors.append(
                    f"{sample_id} line {line_number}: accepted requires final_label 0 or 1"
                )
            if decision != "accepted" and label:
                errors.append(
                    f"{sample_id} line {line_number}: excluded decision requires blank "
                    "final_label"
                )
            if not reason:
                errors.append(
                    f"{sample_id} line {line_number}: blank adjudication_reason"
                )
            if a_confidence not in ALLOWED_CONFIDENCE:
                errors.append(
                    f"{sample_id} line {line_number}: missing/invalid annotator A confidence"
                )
            if b_confidence not in ALLOWED_CONFIDENCE:
                errors.append(
                    f"{sample_id} line {line_number}: missing/invalid annotator B confidence"
                )
            if not policy_value:
                errors.append(
                    f"{sample_id} line {line_number}: blank scope_policy_change_required"
                )

            normalized_policy = policy_value.lower()
            if normalized_policy not in {"0", "0.0", "no", "false"}:
                policy_notes.append({
                    "sample_id": sample_id,
                    "policy_note": policy_value,
                    "adjudication_reason": reason,
                })
            final_counts[decision] += 1
            if label:
                label_counts[label] += 1
            rows.append(row)

    summary: dict[str, object] = {
        "rows": len(rows),
        "final_decisions": dict(final_counts),
        "final_labels": dict(label_counts),
        "policy_notes": len(policy_notes),
        "validation_errors": len(errors),
    }
    return summary, errors, policy_notes


def write_completed_adjudication_report(
    summary: dict[str, object],
    errors: list[str],
    policy_notes: list[dict[str, str]],
    output: Path,
) -> None:
    lines = [
        "# Báo cáo hoàn tất adjudication — P0.1",
        "",
        f"- Số dòng queue: {summary['rows']}",
        f"- Lỗi quality gate: {summary['validation_errors']}",
        f"- Policy note cần đối chiếu scope: {summary['policy_notes']}",
        "",
        "## Quyết định cuối",
        "",
    ]
    for decision, count in sorted(summary["final_decisions"].items()):
        lines.append(f"- `{decision}`: {count}")
    lines.extend(["", "## Nhãn cuối trong nhóm accepted", ""])
    for label, count in sorted(summary["final_labels"].items()):
        lines.append(f"- Label {label}: {count}")
    lines.extend(["", "## Policy notes", ""])
    if policy_notes:
        for note in policy_notes:
            lines.append(f"- `{note['sample_id']}`: {note['policy_note']}")
    else:
        lines.append("- Không có.")
    lines.extend(["", "## Lỗi cần hoàn thiện", ""])
    if errors:
        lines.extend(f"- {error}" for error in errors)
        lines.extend([
            "",
            "Kết luận: **P0.1 chưa thể khóa** cho đến khi các trường trên được "
            "con người hoàn thiện.",
        ])
    else:
        lines.extend([
            "- Không có.",
            "",
            "Kết luận: adjudication vượt quality gate; có thể khóa P0.1 sau khi "
            "xác nhận mọi policy note đã được phản ánh vào scope.",
        ])
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")

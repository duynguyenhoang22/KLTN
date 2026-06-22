import csv
from pathlib import Path

from vismishds.scope_agreement import (
    _cohen_kappa,
    _discussion,
    validate_completed_adjudication,
)


def test_discussion_normalizes_spreadsheet_numbers() -> None:
    assert _discussion("0.0") == "0"
    assert _discussion("1.0") == "1"


def test_cohen_kappa_perfect_agreement() -> None:
    assert _cohen_kappa([("a", "a"), ("b", "b")]) == 1.0


def test_completed_adjudication_requires_human_rationale(tmp_path: Path) -> None:
    path = tmp_path / "adjudication.csv"
    fields = [
        "sample_id", "final_scope_decision", "final_label",
        "adjudication_reason", "scope_policy_change_required",
        "annotator_a_confidence", "annotator_b_confidence",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerow({
            "sample_id": "x",
            "final_scope_decision": "accepted",
            "final_label": "0",
            "adjudication_reason": "",
            "scope_policy_change_required": "no",
            "annotator_a_confidence": "high",
            "annotator_b_confidence": "high",
        })
    _, errors, _ = validate_completed_adjudication(path)
    assert any("blank adjudication_reason" in error for error in errors)

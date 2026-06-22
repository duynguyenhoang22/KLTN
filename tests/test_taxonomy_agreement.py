import csv
from pathlib import Path

from vismishds.taxonomy_agreement import compare_taxonomy_reviews


def write_review(path: Path, decision: str, proposal: str = "") -> None:
    fields = [
        "field", "value", "decision", "proposed_value_or_target", "comment"
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerow({
            "field": "message_domain",
            "value": "commerce",
            "decision": decision,
            "proposed_value_or_target": proposal,
            "comment": "" if decision == "accept" else "reason",
        })


def test_taxonomy_comparison_queues_changes(tmp_path: Path) -> None:
    a = tmp_path / "a.csv"
    b = tmp_path / "b.csv"
    write_review(a, "merge", "commerce_logistics")
    write_review(b, "accept")
    summary, queue, errors = compare_taxonomy_reviews(a, b)
    assert errors == []
    assert summary["queue_items"] == 1
    assert queue[0]["queue_reason"].startswith("decision_disagreement")

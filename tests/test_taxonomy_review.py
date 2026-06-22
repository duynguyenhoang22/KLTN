import csv
from pathlib import Path

from vismishds.taxonomy_review import DECISION_COLUMNS, write_taxonomy_review_sheet


def test_taxonomy_review_sheet_has_blank_decisions(tmp_path: Path) -> None:
    output = tmp_path / "review.csv"
    count = write_taxonomy_review_sheet(output, "reviewer_a")
    with output.open(encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == count
    assert all(row["reviewer_id"] == "reviewer_a" for row in rows)
    assert all(row[column] == "" for row in rows for column in DECISION_COLUMNS)
    assert "example" not in rows[0]
    assert "counterexample" not in rows[0]


def test_taxonomy_review_regeneration_preserves_existing_decision(
    tmp_path: Path,
) -> None:
    output = tmp_path / "review.csv"
    write_taxonomy_review_sheet(output, "reviewer_a")
    with output.open(encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    rows[0]["decision"] = "accept"
    with output.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    write_taxonomy_review_sheet(output, "reviewer_a")
    with output.open(encoding="utf-8-sig") as handle:
        regenerated = list(csv.DictReader(handle))
    assert regenerated[0]["decision"] == "accept"

import csv
from pathlib import Path

from vismishds.scope_challenge import ANNOTATION_FIELDS, write_scope_challenge


def test_blind_outputs_hide_selection_metadata_and_shuffle(tmp_path: Path) -> None:
    selected = [
        {"challenge_group": "minimal_content", "sample_id": f"id-{index}",
         "content": f"content {index}"}
        for index in range(6)
    ]
    key_rows = [
        {
            **row,
            "legacy_label": "0",
            "legacy_category": "legacy",
            "legacy_obfuscation_level": "NONE",
            "data_origin": "real",
            "all_candidate_groups": "minimal_content",
        }
        for row in selected
    ]
    output_a = tmp_path / "a.csv"
    output_b = tmp_path / "b.csv"
    key_output = tmp_path / "key.csv"
    write_scope_challenge(
        selected,
        key_rows,
        {"annotator_a": output_a, "annotator_b": output_b},
        key_output,
        seed=42,
    )

    with output_a.open(encoding="utf-8-sig") as handle:
        rows_a = list(csv.DictReader(handle))
    with output_b.open(encoding="utf-8-sig") as handle:
        rows_b = list(csv.DictReader(handle))

    assert "legacy_label" not in rows_a[0]
    assert "challenge_group" not in rows_a[0]
    assert all(row[field] == "" for row in rows_a for field in ANNOTATION_FIELDS)
    assert [row["sample_id"] for row in rows_a] != [
        row["sample_id"] for row in rows_b
    ]

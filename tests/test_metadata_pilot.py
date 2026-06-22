import csv
from pathlib import Path

from vismishds.metadata_pilot import (
    HUMAN_METADATA_COLUMNS,
    write_metadata_pilot,
)


def test_metadata_pilot_outputs_are_blind_and_share_ids(tmp_path: Path) -> None:
    selected = [
        {"sample_id": f"x{i}", "content": f"content {i}"} for i in range(8)
    ]
    internal = [
        {
            "sample_id": row["sample_id"],
            "label": "0",
            "data_origin": "real",
            "has_url": "0",
            "content_length": "10",
            "legacy_category": "legacy",
            "legacy_obfuscation_level": "NONE",
            "pilot_buckets": "short",
        }
        for row in selected
    ]
    a = tmp_path / "a.csv"
    b = tmp_path / "b.csv"
    manifest = tmp_path / "manifest.csv"
    key = tmp_path / "key.csv"
    write_metadata_pilot(
        selected, internal, {"a": a, "b": b}, manifest, key, seed=42
    )
    with a.open(encoding="utf-8-sig") as handle:
        rows_a = list(csv.DictReader(handle))
    with b.open(encoding="utf-8-sig") as handle:
        rows_b = list(csv.DictReader(handle))
    assert "label" not in rows_a[0]
    assert all(row[field] == "" for row in rows_a for field in HUMAN_METADATA_COLUMNS)
    assert {row["sample_id"] for row in rows_a} == {
        row["sample_id"] for row in rows_b
    }
    assert [row["sample_id"] for row in rows_a] != [
        row["sample_id"] for row in rows_b
    ]

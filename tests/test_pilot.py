import csv
from pathlib import Path

from vismishds.pilot import create_pilot


def test_create_pilot_is_balanced_and_deterministic(tmp_path: Path) -> None:
    source = tmp_path / "reference.csv"
    fieldnames = [
        "sample_id", "content", "label", "data_origin",
        "source_dataset", "source_file", "source_row_id",
    ]
    with source.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for label in ("0", "1"):
            for origin in ("real", "synthetic"):
                for index in range(5):
                    writer.writerow({
                        "sample_id": f"{label}-{origin}-{index}",
                        "content": "sample",
                        "label": label,
                        "data_origin": origin,
                        "source_dataset": "test",
                        "source_file": "test.csv",
                        "source_row_id": str(index),
                    })

    first = tmp_path / "pilot_1.csv"
    second = tmp_path / "pilot_2.csv"
    counts = create_pilot(source, first, size=8, seed=42)
    create_pilot(source, second, size=8, seed=42)

    assert set(counts.values()) == {2}
    assert first.read_text(encoding="utf-8-sig") == second.read_text(encoding="utf-8-sig")

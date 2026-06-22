import json
from pathlib import Path

from vismishds.metadata_pilot_report import build_mistral_pilot_report


def test_mistral_pilot_report_writes_flat_output(tmp_path: Path) -> None:
    record = {
        "sample_id": "x1",
        "content": "sample",
        "llm_metadata": {
            "message_domain": "telecom",
            "surface_features": {
                "text_phenomena": [],
                "text_noise_score": 0,
            },
            "target_audience": {
                "age_groups": ["general"],
                "gender": "all",
                "roles": ["general_public"],
                "evidence": [],
            },
            "obfuscation": {
                "present": False,
                "techniques": [],
                "severity": 0,
                "confidence": 0.9,
            },
            "persuasion_tactics": [],
            "requested_actions": {"types": ["none"], "evidence": []},
            "field_confidence": {
                "message_domain": 0.9,
                "surface_features": 0.9,
                "target_audience": 0.9,
                "obfuscation": 0.9,
                "persuasion_tactics": 0.9,
                "requested_actions": 0.9,
            },
            "review_flags": [],
        },
    }
    source = tmp_path / "source.jsonl"
    source.write_text(json.dumps(record) + "\n", encoding="utf-8")
    flat = tmp_path / "flat.csv"
    report = tmp_path / "report.md"
    summary = build_mistral_pilot_report(source, flat, report)
    assert summary == {"rows": 1, "unique_ids": 1}
    assert flat.exists()
    assert report.exists()

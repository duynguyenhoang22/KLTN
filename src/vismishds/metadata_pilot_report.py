from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path
from statistics import mean


CONFIDENCE_FIELDS = [
    "message_domain",
    "surface_features",
    "target_audience",
    "obfuscation",
    "persuasion_tactics",
    "requested_actions",
]


def build_mistral_pilot_report(
    input_jsonl: Path,
    flat_csv: Path,
    report_md: Path,
) -> dict[str, int]:
    rows = [
        json.loads(line)
        for line in input_jsonl.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    ids = [row["sample_id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate sample_id in Mistral pilot output")

    flat_rows: list[dict[str, object]] = []
    domains: Counter[str] = Counter()
    noise: Counter[int] = Counter()
    flags: Counter[str] = Counter()
    confidence_values: dict[str, list[float]] = {
        field: [] for field in CONFIDENCE_FIELDS
    }

    for row in rows:
        meta = row["llm_metadata"]
        target = meta["target_audience"]
        obfuscation = meta["obfuscation"]
        actions = meta["requested_actions"]
        domains[meta["message_domain"]] += 1
        noise[meta["surface_features"]["text_noise_score"]] += 1
        flags.update(meta["review_flags"])
        for field in CONFIDENCE_FIELDS:
            confidence_values[field].append(
                float(meta["field_confidence"][field])
            )
        flat_rows.append({
            "sample_id": row["sample_id"],
            "content": row["content"],
            "message_domain": meta["message_domain"],
            "text_phenomena": "|".join(
                meta["surface_features"]["text_phenomena"]
            ),
            "text_noise_score": meta["surface_features"]["text_noise_score"],
            "target_age_groups": "|".join(target["age_groups"]),
            "target_gender": target["gender"],
            "target_roles": "|".join(target["roles"]),
            "target_evidence": " || ".join(target["evidence"]),
            "obfuscation_present": str(obfuscation["present"]).lower(),
            "obfuscation_techniques": "|".join(obfuscation["techniques"]),
            "obfuscation_severity": obfuscation["severity"],
            "obfuscation_confidence": obfuscation["confidence"],
            "persuasion_tactics": "|".join(meta["persuasion_tactics"]),
            "requested_actions": "|".join(actions["types"]),
            "requested_action_evidence": " || ".join(actions["evidence"]),
            "review_flags": "|".join(meta["review_flags"]),
            **{
                f"confidence_{field}": meta["field_confidence"][field]
                for field in CONFIDENCE_FIELDS
            },
        })

    flat_csv.parent.mkdir(parents=True, exist_ok=True)
    with flat_csv.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(flat_rows[0]))
        writer.writeheader()
        writer.writerows(flat_rows)

    lines = [
        "# Báo cáo Mistral metadata pilot",
        "",
        "- Model: `mistral-small-2506`",
        "- Taxonomy: `2.1.0-locked`",
        f"- Records: {len(rows)}",
        f"- Unique sample IDs: {len(set(ids))}",
        "- API output status: `auto_labeled`",
        "",
        "## Message domain",
        "",
        "| Domain | Count |",
        "|---|---:|",
    ]
    lines.extend(
        f"| {domain} | {count} |"
        for domain, count in domains.most_common()
    )
    lines.extend([
        "",
        "## Text noise score",
        "",
        "| Score | Count |",
        "|---:|---:|",
    ])
    lines.extend(
        f"| {score} | {noise[score]} |" for score in sorted(noise)
    )
    lines.extend([
        "",
        "## Review flags",
        "",
    ])
    if flags:
        lines.extend(f"- `{flag}`: {count}" for flag, count in flags.most_common())
    else:
        lines.append("- Không có.")
    lines.extend([
        "",
        "## Field confidence",
        "",
        "| Field | Mean | Min |",
        "|---|---:|---:|",
    ])
    for field in CONFIDENCE_FIELDS:
        values = confidence_values[field]
        lines.append(f"| {field} | {mean(values):.3f} | {min(values):.3f} |")
    lines.extend([
        "",
        "## Lưu ý",
        "",
        "Báo cáo này chỉ xác nhận pipeline/API/schema chạy thành công. Chất lượng "
        "metadata chỉ được đánh giá sau khi hai human annotation sheet hoàn tất "
        "và được so sánh với output này.",
        "",
    ])
    report_md.parent.mkdir(parents=True, exist_ok=True)
    report_md.write_text("\n".join(lines), encoding="utf-8")
    return {"rows": len(rows), "unique_ids": len(set(ids))}

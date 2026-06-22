from __future__ import annotations

import csv
import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from .metadata_contract import metadata_output_schema, validate_metadata_item
from .metadata_prompt import build_system_prompt, build_user_prompt
from .mistral_client import MistralMetadataClient
from .pii import mask_pii
from .taxonomy import load_taxonomy


@dataclass(frozen=True)
class PreparedRecord:
    sample_id: str
    content: str
    masked_content: str
    label: int
    data_origin: str
    sender_type: str
    source_dataset: str
    source_file: str
    source_row_id: str
    masking: dict[str, int]


def load_settings(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def _verified_sender_type(row: dict[str, str]) -> str:
    if row.get("data_origin") == "real":
        value = row.get("sender_type", "")
        if value not in {"brandname", "shortcode", "personal_number"}:
            raise ValueError(
                f"{row.get('sample_id')}: invalid real legacy sender_type {value!r}"
            )
        return value
    return "not_applicable"


def prepare_records(
    source: Path,
    limit: int | None = None,
    mask: bool = True,
    sample_ids: list[str] | None = None,
) -> list[PreparedRecord]:
    requested = set(sample_ids) if sample_ids is not None else None
    by_id: dict[str, PreparedRecord] = {}
    records: list[PreparedRecord] = []
    with source.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            if requested is not None and row["sample_id"] not in requested:
                continue
            content = row["content"]
            masked = mask_pii(content) if mask else None
            prepared = PreparedRecord(
                    sample_id=row["sample_id"],
                    content=content,
                    masked_content=masked.text if masked else content,
                    label=int(row["label"]),
                    data_origin=row["data_origin"],
                    sender_type=_verified_sender_type(row),
                    source_dataset=row.get("source_dataset", ""),
                    source_file=row.get("source_file", ""),
                    source_row_id=row.get("source_row_id", ""),
                    masking=masked.replacements if masked else {},
                )
            if requested is None:
                records.append(prepared)
            else:
                by_id[prepared.sample_id] = prepared
            if requested is None and limit is not None and len(records) >= limit:
                break
    if requested is not None:
        missing = [sample_id for sample_id in sample_ids or [] if sample_id not in by_id]
        if missing:
            raise ValueError(f"manifest sample IDs not found: {missing[:10]}")
        records = [by_id[sample_id] for sample_id in sample_ids or []]
        if limit is not None:
            records = records[:limit]
    return records


def batched(records: list[PreparedRecord], size: int) -> Iterable[list[PreparedRecord]]:
    if size <= 0:
        raise ValueError("batch size must be positive")
    for index in range(0, len(records), size):
        yield records[index:index + size]


def _prompt_hash(system_prompt: str, user_prompt: str) -> str:
    return hashlib.sha256(
        (system_prompt + "\n" + user_prompt).encode("utf-8")
    ).hexdigest()


def build_request_preview(
    batch: list[PreparedRecord],
    settings: dict[str, Any],
) -> dict[str, Any]:
    items = [
        {"sample_id": row.sample_id, "masked_content": row.masked_content}
        for row in batch
    ]
    system_prompt = build_system_prompt()
    user_prompt = build_user_prompt(items)
    return {
        "model": settings["model"],
        "prompt_version": settings["prompt_version"],
        "taxonomy_version": load_taxonomy()["version"],
        "sample_ids": [row.sample_id for row in batch],
        "system_prompt": system_prompt,
        "user_prompt": user_prompt,
        "response_schema": metadata_output_schema(),
        "prompt_sha256": _prompt_hash(system_prompt, user_prompt),
    }


def validate_batch_response(
    response: dict[str, Any],
    expected_ids: list[str],
) -> list[str]:
    errors: list[str] = []
    items = response.get("items")
    if not isinstance(items, list):
        return ["response.items must be an array"]
    actual_ids = [str(item.get("sample_id", "")) for item in items if isinstance(item, dict)]
    if len(actual_ids) != len(expected_ids):
        errors.append(
            f"item count mismatch: expected {len(expected_ids)}, got {len(actual_ids)}"
        )
    if set(actual_ids) != set(expected_ids):
        errors.append(
            f"sample_id mismatch: expected={sorted(expected_ids)}, "
            f"actual={sorted(actual_ids)}"
        )
    if len(actual_ids) != len(set(actual_ids)):
        errors.append("duplicate sample_id in response")
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            errors.append(f"items[{index}] must be an object")
            continue
        errors.extend(
            f"{item.get('sample_id', index)}: {error}"
            for error in validate_metadata_item(item)
        )
    return errors


def run_batches(
    records: list[PreparedRecord],
    settings: dict[str, Any],
    client: MistralMetadataClient,
    output_jsonl: Path,
    raw_dir: Path,
) -> dict[str, int]:
    taxonomy = load_taxonomy()
    if (
        settings.get("taxonomy_must_be_locked_for_live_run", True)
        and taxonomy.get("status") != "locked"
    ):
        raise RuntimeError(
            "Live metadata annotation is blocked until taxonomy status is locked"
        )

    output_jsonl.parent.mkdir(parents=True, exist_ok=True)
    raw_dir.mkdir(parents=True, exist_ok=True)
    completed: set[str] = set()
    if output_jsonl.exists():
        with output_jsonl.open(encoding="utf-8") as handle:
            for line in handle:
                if line.strip():
                    completed.add(str(json.loads(line)["sample_id"]))

    stats = {"submitted": 0, "completed": len(completed), "failed_batches": 0}
    pending = [row for row in records if row.sample_id not in completed]
    for batch_index, batch in enumerate(
        batched(pending, int(settings["batch_size"])), start=1
    ):
        preview = build_request_preview(batch, settings)
        response, raw = client.annotate(
            preview["system_prompt"], preview["user_prompt"]
        )
        errors = validate_batch_response(response, preview["sample_ids"])
        raw_record = {
            "created_at": datetime.now(timezone.utc).isoformat(),
            "batch_index": batch_index,
            "request": {
                "model": settings["model"],
                "prompt_version": settings["prompt_version"],
                "taxonomy_version": taxonomy["version"],
                "sample_ids": preview["sample_ids"],
                "prompt_sha256": preview["prompt_sha256"],
            },
            "validation_errors": errors,
            "provider_response": raw,
        }
        batch_key = hashlib.sha256(
            "|".join(preview["sample_ids"]).encode("utf-8")
        ).hexdigest()[:12]
        raw_path = raw_dir / f"batch_{batch_index:05d}_{batch_key}.json"
        raw_path.write_text(
            json.dumps(raw_record, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        stats["submitted"] += len(batch)
        if errors:
            stats["failed_batches"] += 1
            continue

        by_id = {row.sample_id: row for row in batch}
        with output_jsonl.open("a", encoding="utf-8") as handle:
            for item in response["items"]:
                source = by_id[item["sample_id"]]
                record = {
                    "sample_id": source.sample_id,
                    "content": source.content,
                    "label": source.label,
                    "data_origin": source.data_origin,
                    "source": {
                        "dataset": source.source_dataset,
                        "file": source.source_file or None,
                        "record_id": source.source_row_id or source.sample_id,
                    },
                    "sender_type": source.sender_type,
                    "llm_metadata": item,
                    "llm_provenance": {
                        "provider": settings["provider"],
                        "model": settings["model"],
                        "prompt_version": settings["prompt_version"],
                        "taxonomy_version": taxonomy["version"],
                        "prompt_sha256": preview["prompt_sha256"],
                        "masking": source.masking,
                        "status": "auto_labeled",
                    },
                }
                handle.write(json.dumps(record, ensure_ascii=False) + "\n")
                stats["completed"] += 1
    return stats

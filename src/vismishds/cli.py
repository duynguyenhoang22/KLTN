from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from .paths import (
    ANNOTATION_DIR,
    METADATA_LLM_CONFIG_PATH,
    PROCESSED_DIR,
    REFERENCE_DATASET,
)
from .pilot import create_pilot
from .reference import audit_reference
from .scope_challenge import select_scope_challenge, write_scope_challenge
from .scope_agreement import (
    compare_annotations,
    validate_completed_adjudication,
    write_adjudication_outputs,
    write_completed_adjudication_report,
)
from .validation import validate_jsonl
from .taxonomy import audit_taxonomy_schema_contract, load_taxonomy
from .taxonomy_review import write_taxonomy_review_sheet
from .taxonomy_agreement import (
    compare_taxonomy_reviews,
    write_taxonomy_adjudication,
)
from .metadata_pipeline import (
    batched,
    build_request_preview,
    load_settings,
    prepare_records,
    run_batches,
)
from .metadata_pilot import (
    read_manifest_ids,
    select_metadata_pilot,
    write_metadata_pilot,
)
from .metadata_pilot_report import build_mistral_pilot_report
from .mistral_client import MistralMetadataClient, config_from_environment
from .env import load_dotenv


def _print_counter(title: str, counter: object) -> None:
    print(f"\n{title}")
    for key, count in sorted(counter.items(), key=lambda item: (-item[1], item[0])):
        print(f"  {key}: {count}")


def command_audit_reference(_: argparse.Namespace) -> int:
    report = audit_reference(REFERENCE_DATASET)
    print(f"Reference: {report['path']}")
    print(f"Rows: {report['rows']}")
    print(f"Duplicate sample IDs: {report['duplicate_sample_ids']}")
    print(f"Columns: {', '.join(report['columns'])}")
    _print_counter("Label × origin", report["label_origin"])
    _print_counter("Legacy obfuscation by label", report["obfuscation"])
    return 0


def command_init_pilot(args: argparse.Namespace) -> int:
    output = Path(args.output) if args.output else (
        ANNOTATION_DIR / f"pilot_n{args.size}_seed{args.seed}.csv"
    )
    counts = create_pilot(REFERENCE_DATASET, output, args.size, args.seed)
    print(f"Created annotation pilot: {output}")
    for stratum, count in counts.items():
        print(f"  {stratum}: {count}")
    return 0


def command_validate_jsonl(args: argparse.Namespace) -> int:
    rows, errors = validate_jsonl(Path(args.path))
    print(f"Validated rows: {rows}")
    if errors:
        print(f"Errors: {len(errors)}")
        for error in errors[:100]:
            print(f"  {error}")
        if len(errors) > 100:
            print(f"  ... {len(errors) - 100} more")
        return 1
    print("No validation errors.")
    return 0


def command_init_scope_challenge(args: argparse.Namespace) -> int:
    selected, key_rows, counts = select_scope_challenge(
        REFERENCE_DATASET, size=args.size, seed=args.seed, real_only=True
    )
    outputs = {
        "annotator_a": ANNOTATION_DIR / "scope_challenge_annotator_a.csv",
        "annotator_b": ANNOTATION_DIR / "scope_challenge_annotator_b.csv",
    }
    key_output = PROCESSED_DIR / "scope_challenge_internal_key.csv"
    write_scope_challenge(selected, key_rows, outputs, key_output, args.seed)
    print("Created blind scope challenge sheets:")
    for annotator, output in outputs.items():
        print(f"  {annotator}: {output}")
    print(f"Internal selection key (do not show annotators): {key_output}")
    print("Challenge groups:")
    for bucket, count in counts.items():
        print(f"  {bucket}: {count}")
    return 0


def command_compare_scope_challenge(_: argparse.Namespace) -> int:
    metrics, queue, errors = compare_annotations(
        ANNOTATION_DIR / "scope_challenge_annotator_a.csv",
        ANNOTATION_DIR / "scope_challenge_annotator_b.csv",
        PROCESSED_DIR / "scope_challenge_internal_key.csv",
    )
    queue_path = ANNOTATION_DIR / "scope_challenge_adjudication.csv"
    report_path = PROCESSED_DIR / "scope_challenge_agreement_report.md"
    write_adjudication_outputs(metrics, queue, errors, queue_path, report_path)
    print(f"Scope agreement: {metrics['scope_agreement'] * 100:.1f}%")
    print(
        "Effective outcome agreement: "
        f"{metrics['effective_outcome_agreement'] * 100:.1f}%"
    )
    print(
        "Joint accepted label agreement: "
        f"{metrics['joint_label_agreement'] * 100:.1f}%"
    )
    print(f"Adjudication queue: {metrics['adjudication_queue_n']} samples")
    print(f"Validation issues: {len(errors)}")
    print(f"Queue: {queue_path}")
    print(f"Report: {report_path}")
    return 1 if errors else 0


def command_validate_scope_adjudication(_: argparse.Namespace) -> int:
    path = ANNOTATION_DIR / "scope_challenge_adjudication.csv"
    summary, errors, policy_notes = validate_completed_adjudication(path)
    report = PROCESSED_DIR / "scope_adjudication_completion_report.md"
    write_completed_adjudication_report(summary, errors, policy_notes, report)
    print(f"Rows: {summary['rows']}")
    print(f"Validation errors: {summary['validation_errors']}")
    print(f"Policy notes: {summary['policy_notes']}")
    print(f"Report: {report}")
    return 1 if errors else 0


def command_audit_taxonomy(_: argparse.Namespace) -> int:
    taxonomy = load_taxonomy()
    errors = audit_taxonomy_schema_contract()
    print(f"Taxonomy version: {taxonomy['version']}")
    print(f"Scope version: {taxonomy['scope_version']}")
    print(f"Status: {taxonomy['status']}")
    print(f"Contract errors: {len(errors)}")
    for error in errors:
        print(f"  {error}")
    return 1 if errors else 0


def command_init_taxonomy_review(_: argparse.Namespace) -> int:
    outputs = {
        "reviewer_a": ANNOTATION_DIR / "p0_2_taxonomy_review_a.csv",
        "reviewer_b": ANNOTATION_DIR / "p0_2_taxonomy_review_b.csv",
    }
    for reviewer, output in outputs.items():
        count = write_taxonomy_review_sheet(output, reviewer)
        print(f"{reviewer}: {output} ({count} items)")
    return 0


def command_compare_taxonomy_review(_: argparse.Namespace) -> int:
    summary, queue, errors = compare_taxonomy_reviews(
        ANNOTATION_DIR / "p0_2_taxonomy_review_a.csv",
        ANNOTATION_DIR / "p0_2_taxonomy_review_b.csv",
    )
    queue_path = ANNOTATION_DIR / "p0_2_taxonomy_adjudication.csv"
    report_path = PROCESSED_DIR / "p0_2_taxonomy_review_report.md"
    write_taxonomy_adjudication(
        summary, queue, errors, queue_path, report_path
    )
    print(
        f"Exact agreement: {summary['exact_agreement']}/"
        f"{summary['items']} ({summary['exact_agreement_rate'] * 100:.1f}%)"
    )
    print(f"Adjudication queue: {summary['queue_items']}")
    print(f"Validation errors: {summary['validation_errors']}")
    print(f"Queue: {queue_path}")
    print(f"Report: {report_path}")
    return 1 if errors else 0


def command_preview_metadata_llm(args: argparse.Namespace) -> int:
    settings = load_settings(METADATA_LLM_CONFIG_PATH)
    records = prepare_records(
        REFERENCE_DATASET,
        limit=args.limit,
        mask=bool(settings.get("mask_pii", True)),
    )
    first_batch = next(iter(batched(records, int(settings["batch_size"]))), [])
    if not first_batch:
        print("No records available.")
        return 1
    preview = build_request_preview(first_batch, settings)
    output = (
        Path(args.output)
        if args.output
        else PROCESSED_DIR / "metadata_llm_request_preview.json"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(preview, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    total_batches = (
        len(records) + int(settings["batch_size"]) - 1
    ) // int(settings["batch_size"])
    masked_counts: dict[str, int] = {}
    for record in records:
        for field, count in record.masking.items():
            masked_counts[field] = masked_counts.get(field, 0) + count
    print(f"Model: {settings['model']}")
    print(f"Taxonomy: {load_taxonomy()['version']} ({load_taxonomy()['status']})")
    print(f"Prepared records: {len(records)}")
    print(f"Batch size: {settings['batch_size']}")
    print(f"Estimated batches: {total_batches}")
    print(f"PII replacements: {masked_counts}")
    print(f"Preview: {output}")
    print("No API request was sent.")
    return 0


def command_run_metadata_llm(args: argparse.Namespace) -> int:
    if not args.execute:
        raise RuntimeError("Live run requires explicit --execute")
    settings = load_settings(METADATA_LLM_CONFIG_PATH)
    if args.batch_size:
        settings["batch_size"] = args.batch_size
    if os.getenv("MISTRAL_API_KEY", "").strip() == "":
        raise RuntimeError("MISTRAL_API_KEY is not configured")
    sample_ids = read_manifest_ids(Path(args.manifest)) if args.manifest else None
    records = prepare_records(
        REFERENCE_DATASET,
        limit=args.limit,
        mask=bool(settings.get("mask_pii", True)),
        sample_ids=sample_ids,
    )
    client = MistralMetadataClient(config_from_environment(settings))
    try:
        stats = run_batches(
            records,
            settings,
            client,
            Path(args.output) if args.output else (
                PROCESSED_DIR / "metadata_mistral_small_2506.jsonl"
            ),
            Path(args.raw_dir) if args.raw_dir else (
                PROCESSED_DIR / "metadata_mistral_small_2506_raw"
            ),
        )
    finally:
        client.close()
    print(json.dumps(stats, ensure_ascii=False, indent=2))
    return 1 if stats["failed_batches"] else 0


def command_init_metadata_pilot(args: argparse.Namespace) -> int:
    selected, internal, counts = select_metadata_pilot(
        REFERENCE_DATASET, size=args.size, seed=args.seed
    )
    outputs = {
        "annotator_a": ANNOTATION_DIR / "metadata_pilot_annotator_a.csv",
        "annotator_b": ANNOTATION_DIR / "metadata_pilot_annotator_b.csv",
    }
    manifest = PROCESSED_DIR / "metadata_pilot_manifest.csv"
    internal_key = PROCESSED_DIR / "metadata_pilot_internal_key.csv"
    write_metadata_pilot(
        selected, internal, outputs, manifest, internal_key, args.seed
    )
    print("Created human metadata pilot:")
    for reviewer, output in outputs.items():
        print(f"  {reviewer}: {output}")
    print(f"Mistral manifest: {manifest}")
    print(f"Internal key: {internal_key}")
    for stratum, count in counts.items():
        print(f"  {stratum}: {count}")
    return 0


def command_report_mistral_pilot(_: argparse.Namespace) -> int:
    summary = build_mistral_pilot_report(
        PROCESSED_DIR / "metadata_pilot_mistral_small_2506.jsonl",
        PROCESSED_DIR / "metadata_pilot_mistral_small_2506_flat.csv",
        PROCESSED_DIR / "metadata_pilot_mistral_small_2506_report.md",
    )
    print(f"Rows: {summary['rows']}")
    print(f"Unique IDs: {summary['unique_ids']}")
    print(
        "Flat CSV: "
        f"{PROCESSED_DIR / 'metadata_pilot_mistral_small_2506_flat.csv'}"
    )
    print(
        "Report: "
        f"{PROCESSED_DIR / 'metadata_pilot_mistral_small_2506_report.md'}"
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="vismishds")
    subparsers = parser.add_subparsers(dest="command", required=True)

    audit = subparsers.add_parser(
        "audit-reference", help="Audit the frozen Phase 1 reference dataset"
    )
    audit.set_defaults(func=command_audit_reference)

    pilot = subparsers.add_parser(
        "init-pilot", help="Create a stratified metadata annotation pilot"
    )
    pilot.add_argument("--size", type=int, default=400)
    pilot.add_argument("--seed", type=int, default=42)
    pilot.add_argument("--output")
    pilot.set_defaults(func=command_init_pilot)

    validate = subparsers.add_parser(
        "validate-jsonl", help="Validate canonical v2 JSONL records"
    )
    validate.add_argument("path")
    validate.set_defaults(func=command_validate_jsonl)

    challenge = subparsers.add_parser(
        "init-scope-challenge",
        help="Create two blind annotation sheets for 50 difficult real cases",
    )
    challenge.add_argument("--size", type=int, default=50)
    challenge.add_argument("--seed", type=int, default=20260621)
    challenge.set_defaults(func=command_init_scope_challenge)

    compare = subparsers.add_parser(
        "compare-scope-challenge",
        help="Validate, compare, and prepare adjudication for two scope sheets",
    )
    compare.set_defaults(func=command_compare_scope_challenge)

    validate_adjudication = subparsers.add_parser(
        "validate-scope-adjudication",
        help="Validate completed human adjudication and its quality gate",
    )
    validate_adjudication.set_defaults(func=command_validate_scope_adjudication)

    audit_taxonomy = subparsers.add_parser(
        "audit-taxonomy",
        help="Check taxonomy/schema synchronization and label leakage",
    )
    audit_taxonomy.set_defaults(func=command_audit_taxonomy)

    init_taxonomy_review = subparsers.add_parser(
        "init-taxonomy-review",
        help="Create two independent P0.2 taxonomy review sheets",
    )
    init_taxonomy_review.set_defaults(func=command_init_taxonomy_review)

    compare_taxonomy_review = subparsers.add_parser(
        "compare-taxonomy-review",
        help="Compare reviewer A/B and prepare P0.2 adjudication",
    )
    compare_taxonomy_review.set_defaults(func=command_compare_taxonomy_review)

    preview_metadata = subparsers.add_parser(
        "preview-metadata-llm",
        help="Prepare masked Mistral requests without calling the API",
    )
    preview_metadata.add_argument("--limit", type=int, default=16)
    preview_metadata.add_argument("--output")
    preview_metadata.set_defaults(func=command_preview_metadata_llm)

    run_metadata = subparsers.add_parser(
        "run-metadata-llm",
        help="Run resumable Mistral metadata annotation after taxonomy lock",
    )
    run_metadata.add_argument("--limit", type=int)
    run_metadata.add_argument("--manifest")
    run_metadata.add_argument("--output")
    run_metadata.add_argument("--raw-dir")
    run_metadata.add_argument(
        "--batch-size",
        type=int,
        help="Override configured batch size for pilot/retry runs",
    )
    run_metadata.add_argument(
        "--execute",
        action="store_true",
        help="Explicitly authorize live API requests",
    )
    run_metadata.set_defaults(func=command_run_metadata_llm)

    init_metadata_pilot = subparsers.add_parser(
        "init-metadata-pilot",
        help="Create two blind human sheets and a shared Mistral pilot manifest",
    )
    init_metadata_pilot.add_argument("--size", type=int, default=100)
    init_metadata_pilot.add_argument("--seed", type=int, default=20260622)
    init_metadata_pilot.set_defaults(func=command_init_metadata_pilot)

    report_mistral_pilot = subparsers.add_parser(
        "report-mistral-pilot",
        help="Create a flat CSV and summary for completed Mistral pilot output",
    )
    report_mistral_pilot.set_defaults(func=command_report_mistral_pilot)
    return parser


def main() -> None:
    load_dotenv()
    parser = build_parser()
    args = parser.parse_args()
    raise SystemExit(args.func(args))

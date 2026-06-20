from __future__ import annotations

import argparse
from pathlib import Path

from .paths import ANNOTATION_DIR, REFERENCE_DATASET
from .pilot import create_pilot
from .reference import audit_reference
from .validation import validate_jsonl


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
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    raise SystemExit(args.func(args))

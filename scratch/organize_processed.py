import os
import shutil
from pathlib import Path

processed_dir = Path("data/processed")
calibration_dir = processed_dir / "calibration"
scope_dir = processed_dir / "scope_and_taxonomy"

# Create directories
calibration_dir.mkdir(parents=True, exist_ok=True)
scope_dir.mkdir(parents=True, exist_ok=True)

# Files for scope_and_taxonomy
scope_files = [
    "p0_2_taxonomy_review_report.md",
    "scope_adjudication_completion_report.md",
    "scope_challenge_agreement_report.md",
    "scope_challenge_internal_key.csv",
]

# Files and directories for calibration
calibration_items = [
    "compare_reviewer_a_mistral.md",
    "compare_reviewer_a_mistral_p2.md",
    "metadata_llm_full_dry_run_preview.json",
    "metadata_llm_locked_pilot_preview.json",
    "metadata_llm_p2_preview.json",
    "metadata_llm_request_preview.json",
    "metadata_pilot_agreement_report.md",
    "metadata_pilot_internal_key.csv",
    "metadata_pilot_manifest.csv",
    "metadata_pilot_mistral_p2.jsonl",
    "metadata_pilot_mistral_p3.jsonl",
    "metadata_pilot_mistral_small_2506.jsonl",
    "metadata_pilot_mistral_small_2506_flat.csv",
    "metadata_pilot_mistral_small_2506_report.md",
    "test_metadata_prompt_2.jsonl",
    "metadata_mistral_small_2506_raw",
    "metadata_pilot_mistral_p2_raw",
    "metadata_pilot_mistral_p3_raw",
    "metadata_pilot_mistral_small_2506_raw",
]

print("Organizing data/processed directory...")

for item_name in scope_files:
    src = processed_dir / item_name
    if src.exists():
        shutil.move(str(src), str(scope_dir / item_name))
        print(f"Moved {item_name} -> scope_and_taxonomy/")

for item_name in calibration_items:
    src = processed_dir / item_name
    if src.exists():
        shutil.move(str(src), str(calibration_dir / item_name))
        print(f"Moved {item_name} -> calibration/")

print("Organization complete.")

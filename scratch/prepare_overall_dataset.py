import csv
from pathlib import Path

source_path = Path("data/reference/phase2/vismish_phase2_final.csv")
target_path = Path("data/reference/phase2/vismish_phase2_to_annotate.csv")

new_metadata_columns = [
    "message_domain",
    "text_phenomena",
    "text_noise_score",
    "target_age_groups",
    "target_gender",
    "target_roles",
    "target_evidence",
    "obfuscation_present",
    "obfuscation_techniques",
    "obfuscation_severity",
    "obfuscation_confidence",
    "persuasion_tactics",
    "requested_actions",
    "requested_action_evidence",
    "overall_confidence",
    "review_notes",
]

if not source_path.exists():
    print(f"Error: source file {source_path} does not exist!")
    exit(1)

print(f"Reading from: {source_path}")
with source_path.open(encoding="utf-8-sig", newline="") as f_in:
    reader = csv.DictReader(f_in)
    original_headers = reader.fieldnames
    rows = list(reader)

all_headers = original_headers + new_metadata_columns

print(f"Writing prepared sheet to: {target_path}")
target_path.parent.mkdir(parents=True, exist_ok=True)
with target_path.open("w", encoding="utf-8-sig", newline="") as f_out:
    writer = csv.DictWriter(f_out, fieldnames=all_headers)
    writer.writeheader()
    for row in rows:
        # Initialize the new metadata columns as empty strings
        prepared_row = dict(row)
        origin = prepared_row.get("data_origin")
        if origin in {"paraphrased", "synthetic_hard_positive"}:
            origin = "synthetic"
        prepared_row["data_origin"] = origin
        for col in new_metadata_columns:
            prepared_row[col] = ""
        writer.writerow(prepared_row)

print("Overall dataset sheet successfully prepared.")

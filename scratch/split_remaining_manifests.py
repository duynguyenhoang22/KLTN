import csv
import json
from pathlib import Path

# Paths
reference_csv_path = Path("data/reference/phase2/vismish_phase2_final.csv")
completed_jsonl_path = Path("data/processed/metadata_mistral_small_2506.jsonl")

manifest_1_path = Path("data/processed/metadata_manifest_run_1.csv")
manifest_2_path = Path("data/processed/metadata_manifest_run_2.csv")

if not reference_csv_path.exists():
    print(f"Error: Reference CSV not found at {reference_csv_path}")
    exit(1)

# 1. Read all sample IDs from the reference dataset
all_ids = []
with reference_csv_path.open(encoding="utf-8-sig", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        all_ids.append(row["sample_id"])

total_samples = len(all_ids)
print(f"Total samples in Phase 2: {total_samples}")

# 2. Read completed sample IDs from the output JSONL
completed_ids = set()
if completed_jsonl_path.exists():
    with completed_jsonl_path.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                try:
                    record = json.loads(line)
                    completed_ids.add(str(record["sample_id"]))
                except Exception as e:
                    pass
    print(f"Completed samples found: {len(completed_ids)}")
else:
    print(f"Warning: Completed JSONL file not found at {completed_jsonl_path}. Treating as 0 completed.")

# 3. Find remaining sample IDs
remaining_ids = [sample_id for sample_id in all_ids if sample_id not in completed_ids]
total_remaining = len(remaining_ids)
print(f"Total remaining samples to process: {total_remaining}")

if total_remaining == 0:
    print("No remaining samples to split!")
    exit(0)

# 4. Split the remaining samples into 2 parts
split_point = total_remaining // 2
part_1 = remaining_ids[:split_point]
part_2 = remaining_ids[split_point:]

print(f"Splitting into:")
print(f"  - Part 1: {len(part_1)} samples -> {manifest_1_path}")
print(f"  - Part 2: {len(part_2)} samples -> {manifest_2_path}")

# 5. Write manifests
for path, id_list in [(manifest_1_path, part_1), (manifest_2_path, part_2)]:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["sample_id"])
        writer.writeheader()
        for sample_id in id_list:
            writer.writerow({"sample_id": sample_id})

print("Successfully split and wrote remaining manifests.")

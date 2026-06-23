import csv
import json
from pathlib import Path

# Paths
reference_csv_path = Path("data/reference/phase2/vismish_phase2_final.csv")
base_jsonl_path = Path("data/processed/metadata_mistral_small_2506.jsonl")
run1_jsonl_path = Path("data/processed/metadata_mistral_run_1.jsonl")
run2_jsonl_path = Path("data/processed/metadata_mistral_run_2.jsonl")
final_output_path = Path("data/processed/metadata_phase2_mistral_final.jsonl")

# 1. Read all sample IDs from reference to preserve ordering
all_ids = []
with reference_csv_path.open(encoding="utf-8-sig", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        all_ids.append(row["sample_id"])

print(f"Total reference samples: {len(all_ids)}")

# 2. Gather all records from the three JSONL sources
records_by_id = {}

def load_jsonl(path: Path):
    if not path.exists():
        print(f"Warning: File not found: {path}")
        return
    count = 0
    with path.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                try:
                    record = json.loads(line)
                    records_by_id[str(record["sample_id"])] = record
                    count += 1
                except Exception as e:
                    pass
    print(f"Loaded {count} records from {path}")

load_jsonl(base_jsonl_path)
load_jsonl(run1_jsonl_path)
load_jsonl(run2_jsonl_path)

# 3. Write final output following reference order
missing_ids = []
written_count = 0

final_output_path.parent.mkdir(parents=True, exist_ok=True)
with final_output_path.open("w", encoding="utf-8") as f_out:
    for sample_id in all_ids:
        if sample_id in records_by_id:
            f_out.write(json.dumps(records_by_id[sample_id], ensure_ascii=False) + "\n")
            written_count += 1
        else:
            missing_ids.append(sample_id)

print(f"Final output written to: {final_output_path}")
print(f"Total records written: {written_count}")
if missing_ids:
    print(f"Warning: {len(missing_ids)} samples are still missing: {missing_ids[:20]}")
else:
    print("Success: All samples successfully merged!")

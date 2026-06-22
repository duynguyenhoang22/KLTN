import shutil
from pathlib import Path

p3_file = Path("c:/KLTN/KLTN/data/processed/metadata_pilot_mistral_p3.jsonl")
p3_raw_dir = Path("c:/KLTN/KLTN/data/processed/metadata_pilot_mistral_p3_raw")

if p3_file.exists():
    p3_file.unlink()
    print("Deleted metadata_pilot_mistral_p3.jsonl")
else:
    print("metadata_pilot_mistral_p3.jsonl does not exist.")

if p3_raw_dir.exists():
    shutil.rmtree(p3_raw_dir)
    print("Deleted metadata_pilot_mistral_p3_raw directory")
else:
    print("metadata_pilot_mistral_p3_raw directory does not exist.")

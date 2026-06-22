import csv
import json
from pathlib import Path

def parse_set(val):
    if not val:
        return set()
    return {x.strip().lower() for x in val.split('|') if x.strip()}

def main():
    csv_path = Path("data/annotations/metadata_pilot_annotator_a.csv")
    jsonl_path = Path("data/processed/metadata_pilot_mistral_p2.jsonl")

    # Load annotator A
    annotator_a = {}
    with open(csv_path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            sid = row['sample_id'].strip()
            annotator_a[sid] = {
                'gender': row['target_gender'].strip().lower(),
                'age_groups': parse_set(row['target_age_groups']),
                'roles': parse_set(row['target_roles']),
                'content': row['content']
            }

    # Load mistral p2
    mistral = {}
    with open(jsonl_path, encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue
            data = json.loads(line)
            sid = data['sample_id'].strip()
            meta = data['llm_metadata']
            target = meta.get('target_audience', {})
            age_groups = target.get('age_groups', [])
            if isinstance(age_groups, str):
                age_groups = [age_groups]
            roles = target.get('roles', [])
            if isinstance(roles, str):
                roles = [roles]
            mistral[sid] = {
                'gender': target.get('gender', '').strip().lower(),
                'age_groups': {x.strip().lower() for x in age_groups if x.strip()},
                'roles': {x.strip().lower() for x in roles if x.strip()},
                'content': data['content']
            }

    common_ids = set(annotator_a.keys()) & set(mistral.keys())

    print("=== ALL GENDER MISMATCHES (Annotator A = male, Mistral = all) ===")
    for sid in sorted(common_ids):
        a = annotator_a[sid]
        m = mistral[sid]
        if a['gender'] == 'male' and m['gender'] == 'all':
            print(f"ID: {sid} | Content: {a['content']}")

    print("\n=== ALL GENDER MISMATCHES (Annotator A = unknown, Mistral = all) ===")
    for sid in sorted(common_ids):
        a = annotator_a[sid]
        m = mistral[sid]
        if a['gender'] == 'unknown' and m['gender'] == 'all':
            print(f"ID: {sid} | Content: {a['content']}")

    print("\n=== ALL AGE MISMATCHES (Annotator A = adult, Mistral = general) ===")
    for sid in sorted(common_ids):
        a = annotator_a[sid]
        m = mistral[sid]
        if a['age_groups'] == {'adult'} and m['age_groups'] == {'general'}:
            print(f"ID: {sid} | Content: {a['content']}")

if __name__ == '__main__':
    main()

import csv
import json
import sys
from pathlib import Path
from collections import Counter

def parse_set(val):
    if not val:
        return set()
    return {x.strip().lower() for x in val.split('|') if x.strip()}

def normalize_semantic(s):
    if not s or s == {'none'}:
        return set()
    return s

def jaccard_similarity(set_a, set_b):
    if not set_a and not set_b:
        return 1.0
    if not set_a or not set_b:
        return 0.0
    return len(set_a & set_b) / len(set_a | set_b)

def cohen_kappa(pairs):
    if not pairs:
        return 0.0
    total = len(pairs)
    observed = sum(left == right for left, right in pairs) / total
    left_counts = Counter(left for left, _ in pairs)
    right_counts = Counter(right for _, right in pairs)
    labels = set(left_counts) | set(right_counts)
    expected = sum(
        (left_counts[label] / total) * (right_counts[label] / total)
        for label in labels
    )
    if expected == 1:
        return 1.0 if observed == 1 else 0.0
    return (observed - expected) / (1 - expected)

def mean_absolute_error(pairs):
    if not pairs:
        return 0.0
    return sum(abs(left - right) for left, right in pairs) / len(pairs)

def main():
    if len(sys.argv) < 3:
        csv_path = Path("data/annotations/metadata_pilot_annotator_a.csv")
        jsonl_path = Path("data/processed/metadata_pilot_mistral_p3.jsonl")
    else:
        csv_path = Path(sys.argv[1])
        jsonl_path = Path(sys.argv[2])

    print(f"Comparing:")
    print(f"  Human CSV: {csv_path}")
    print(f"  LLM JSONL: {jsonl_path}")

    if not csv_path.exists():
        print(f"Error: {csv_path} does not exist!")
        return
    if not jsonl_path.exists():
        print(f"Error: {jsonl_path} does not exist!")
        return

    # Load Annotator A CSV
    annotator_a = {}
    with csv_path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            sid = row["sample_id"].strip()
            obf_present = row["obfuscation_present"].strip().lower()
            if obf_present in {"true", "1", "yes"}:
                obf_present = "true"
            elif obf_present in {"false", "0", "no", ""}:
                obf_present = "false"

            annotator_a[sid] = {
                "message_domain": row["message_domain"].strip(),
                "text_noise_score": int(float(row["text_noise_score"].strip() or 0)),
                "obfuscation_present": obf_present,
                "obfuscation_severity": int(float(row["obfuscation_severity"].strip() or 0)),
                "target_gender": row["target_gender"].strip().lower(),
                "text_phenomena": parse_set(row["text_phenomena"]),
                "target_age_groups": parse_set(row["target_age_groups"]),
                "target_roles": parse_set(row["target_roles"]),
                "persuasion_tactics": parse_set(row["persuasion_tactics"]),
                "requested_actions": parse_set(row["requested_actions"]),
            }

    # Load LLM JSONL
    llm_data = {}
    with jsonl_path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            row = json.loads(line)
            sid = row["sample_id"].strip()
            meta = row["llm_metadata"]
            surface = meta.get("surface_features", {})
            target = meta.get("target_audience", {})
            obf = meta.get("obfuscation", {})
            actions = meta.get("requested_actions", {})

            obf_present = str(obf.get("present", False)).lower()

            age_groups = target.get("age_groups", [])
            if isinstance(age_groups, str):
                age_groups = [age_groups]
            roles = target.get("roles", [])
            if isinstance(roles, str):
                roles = [roles]
            phenomena = surface.get("text_phenomena", [])
            if isinstance(phenomena, str):
                phenomena = [phenomena]
            tactics = meta.get("persuasion_tactics", [])
            if isinstance(tactics, str):
                tactics = [tactics]
            action_types = actions.get("types", [])
            if isinstance(action_types, str):
                action_types = [action_types]

            llm_data[sid] = {
                "message_domain": meta.get("message_domain", "").strip(),
                "text_noise_score": int(surface.get("text_noise_score", 0)),
                "obfuscation_present": obf_present,
                "obfuscation_severity": int(obf.get("severity", 0)),
                "target_gender": target.get("gender", "").strip().lower(),
                "text_phenomena": {x.strip().lower() for x in phenomena if x.strip()},
                "target_age_groups": {x.strip().lower() for x in age_groups if x.strip()},
                "target_roles": {x.strip().lower() for x in roles if x.strip()},
                "persuasion_tactics": {x.strip().lower() for x in tactics if x.strip()},
                "requested_actions": {x.strip().lower() for x in action_types if x.strip()},
            }

    common_ids = sorted(list(set(annotator_a.keys()) & set(llm_data.keys())))
    total_common = len(common_ids)
    print(f"Total matched sample IDs: {total_common}")
    if total_common == 0:
        print("No matching samples found!")
        return

    # Categorical Metrics
    categorical_fields = ["message_domain", "obfuscation_present", "target_gender"]
    numerical_fields = ["text_noise_score", "obfuscation_severity"]
    set_fields = ["text_phenomena", "target_age_groups", "target_roles", "persuasion_tactics", "requested_actions"]

    print("\n=== AGREEMENT METRICS ===")
    print(f"{'Field':<25} | {'Exact Match':<12} | {'Kappa / MAE':<12} | {'Notes':<15}")
    print("-" * 75)

    for field in categorical_fields:
        pairs = [(annotator_a[sid][field], llm_data[sid][field]) for sid in common_ids]
        exact = sum(left == right for left, right in pairs) / total_common
        kappa = cohen_kappa(pairs)
        print(f"{field:<25} | {exact*100:11.1f}% | {kappa:12.3f} | Kappa")

    for field in numerical_fields:
        pairs = [(annotator_a[sid][field], llm_data[sid][field]) for sid in common_ids]
        exact = sum(left == right for left, right in pairs) / total_common
        mae = mean_absolute_error(pairs)
        print(f"{field:<25} | {exact*100:11.1f}% | {mae:12.3f} | MAE")

    print("\n=== SET/MULTI-LABEL SIMILARITY (Jaccard) ===")
    print(f"{'Field':<25} | {'Jaccard Literal':<15} | {'Jaccard Semantic':<16}")
    print("-" * 65)

    for field in set_fields:
        literal_similarities = []
        semantic_similarities = []
        for sid in common_ids:
            sa = annotator_a[sid][field]
            sm = llm_data[sid][field]
            literal_similarities.append(jaccard_similarity(sa, sm))
            semantic_similarities.append(jaccard_similarity(normalize_semantic(sa), normalize_semantic(sm)))
        mean_lit = sum(literal_similarities) / total_common
        mean_sem = sum(semantic_similarities) / total_common
        print(f"{field:<25} | {mean_lit*100:14.1f}% | {mean_sem*100:15.1f}%")

if __name__ == "__main__":
    main()

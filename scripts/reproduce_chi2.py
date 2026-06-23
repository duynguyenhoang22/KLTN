import json
from pathlib import Path
import scipy.stats as stats
import numpy as np

def run_chi2_test(records, label_filter=None, test_name=""):
    # Filter records
    subset = []
    for r in records:
        if label_filter is not None and r.get("label") != label_filter:
            continue
        subset.append(r)

    # 1. Collect unique domains, tactics/actions
    domains = sorted(list(set(r.get("message_domain", "other") for r in subset)))
    
    if test_name == "tactic":
        items = set()
        for r in subset:
            for t in r.get("persuasion_tactics", []):
                items.add(t)
        items = sorted(list(items))
        
        # Build matrix
        matrix = np.zeros((len(domains), len(items)), dtype=int)
        domain_to_idx = {d: i for i, d in enumerate(domains)}
        item_to_idx = {it: i for i, it in enumerate(items)}
        
        for r in subset:
            d_idx = domain_to_idx[r.get("message_domain", "other")]
            for t in r.get("persuasion_tactics", []):
                t_idx = item_to_idx[t]
                matrix[d_idx, t_idx] += 1
                
        var_name = "Persuasion Tactics"
        
    else:  # action
        items = set()
        for r in subset:
            req_actions = r.get("requested_actions", {})
            action_types = req_actions.get("types", [])
            if isinstance(action_types, str):
                action_types = [action_types]
            for act in action_types:
                items.add(act)
        items = sorted(list(items))
        
        # Build matrix
        matrix = np.zeros((len(domains), len(items)), dtype=int)
        domain_to_idx = {d: i for i, d in enumerate(domains)}
        item_to_idx = {it: i for i, it in enumerate(items)}
        
        for r in subset:
            d_idx = domain_to_idx[r.get("message_domain", "other")]
            req_actions = r.get("requested_actions", {})
            action_types = req_actions.get("types", [])
            if isinstance(action_types, str):
                action_types = [action_types]
            for act in action_types:
                a_idx = item_to_idx[act]
                matrix[d_idx, a_idx] += 1
                
        var_name = "Requested Actions"

    # Drop zero-sum rows and columns
    row_mask = matrix.sum(axis=1) > 0
    col_mask = matrix.sum(axis=0) > 0
    matrix_clean = matrix[row_mask][:, col_mask]
    
    clean_domains = [d for i, d in enumerate(domains) if row_mask[i]]
    clean_items = [it for i, it in enumerate(items) if col_mask[i]]

    # Run test
    chi2, p, dof, expected = stats.chi2_contingency(matrix_clean)
    
    # Calculate Z-score approximation to show physical deviation
    # Under H0, the mean of Chi2 is dof, and variance is 2*dof
    z_score = (chi2 - dof) / np.sqrt(2 * dof)

    subset_str = "Smishing (label=1)" if label_filter == 1 else "All Records"
    print("\n" + "="*60)
    print(f"TEST: Message Domain vs {var_name} ({subset_str})")
    print(f"Contingency Matrix Shape: {matrix_clean.shape}")
    print(f"Clean Domains ({len(clean_domains)}): {clean_domains}")
    print(f"Clean Items ({len(clean_items)}): {clean_items}")
    print("-"*60)
    print(f"Chi2 statistic : {chi2:.4f}")
    print(f"Degrees of freedom (dof): {dof}")
    print(f"Z-score (approx deviation from H0 mean): {z_score:.2f} standard deviations")
    print(f"p-value        : {p}")
    print(f"p-value (sci)  : {p:.6e}")
    print("="*60)

def main():
    metadata_path = Path("data/processed/metadata_phase2_mistral_final.jsonl")
    if not metadata_path.exists():
        print(f"Error: {metadata_path} does not exist!")
        return

    records = []
    with open(metadata_path, encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            records.append(json.loads(line))

    # We run for the Smishing-only subset (label=1) as presented in the reports
    run_chi2_test(records, label_filter=1, test_name="tactic")
    run_chi2_test(records, label_filter=1, test_name="action")

if __name__ == "__main__":
    main()

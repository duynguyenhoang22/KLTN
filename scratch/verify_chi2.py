import json
from pathlib import Path
import scipy.stats as stats
import numpy as np

def main():
    metadata_path = Path("data/processed/metadata_phase2_mistral_final.jsonl")
    if not metadata_path.exists():
        print(f"Error: {metadata_path} does not exist!")
        return

    # Load all records (filter for label=1 if we want to match the Smishing-only analysis)
    records = []
    with open(metadata_path, encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            item = json.loads(line)
            if item.get("label") == 1:  # Filter for Smishing (Label 1) only
                records.append(item)

    print(f"Loaded {len(records)} Smishing (label=1) records.")

    # 1. Collect unique domains, tactics, actions
    domains = set()
    tactics = set()
    actions = set()

    for r in records:
        domains.add(r.get("message_domain", "other"))
        
        for t in r.get("persuasion_tactics", []):
            tactics.add(t)
            
        req_actions = r.get("requested_actions", {})
        action_types = req_actions.get("types", [])
        if isinstance(action_types, str):
            action_types = [action_types]
        for act in action_types:
            actions.add(act)

    domains = sorted(list(domains))
    tactics = sorted(list(tactics))
    actions = sorted(list(actions))

    print(f"\nUnique Domains ({len(domains)}): {domains}")
    print(f"Unique Tactics ({len(tactics)}): {tactics}")
    print(f"Unique Actions ({len(actions)}): {actions}")

    # Map for easy lookup
    domain_to_idx = {d: i for i, d in enumerate(domains)}
    tactic_to_idx = {t: i for i, t in enumerate(tactics)}
    action_to_idx = {a: i for i, a in enumerate(actions)}

    # 2. Build contingency matrix for domain vs tactic
    matrix_tactic = np.zeros((len(domains), len(tactics)), dtype=int)
    for r in records:
        d_idx = domain_to_idx[r.get("message_domain", "other")]
        for t in r.get("persuasion_tactics", []):
            t_idx = tactic_to_idx[t]
            matrix_tactic[d_idx, t_idx] += 1

    # 3. Build contingency matrix for domain vs action
    matrix_action = np.zeros((len(domains), len(actions)), dtype=int)
    for r in records:
        d_idx = domain_to_idx[r.get("message_domain", "other")]
        req_actions = r.get("requested_actions", {})
        action_types = req_actions.get("types", [])
        if isinstance(action_types, str):
            action_types = [action_types]
        for act in action_types:
            a_idx = action_to_idx[act]
            matrix_action[d_idx, a_idx] += 1

    # 4. Perform Chi-square test on domain vs tactic
    chi2_t, p_t, dof_t, expected_t = stats.chi2_contingency(matrix_tactic)
    print("\n==================================================")
    print("Test 1: Message Domain vs Persuasion Tactics")
    print(f"Matrix shape: {matrix_tactic.shape}")
    print(f"Chi2 statistic: {chi2_t:.4f}")
    print(f"p-value: {p_t}")
    print(f"p-value (scientific): {p_t:.6e}")
    print(f"Degrees of freedom: {dof_t}")
    
    # 5. Perform Chi-square test on domain vs action
    chi2_a, p_a, dof_a, expected_a = stats.chi2_contingency(matrix_action)
    print("\n==================================================")
    print("Test 2: Message Domain vs Requested Actions")
    print(f"Matrix shape: {matrix_action.shape}")
    print(f"Chi2 statistic: {chi2_a:.4f}")
    print(f"p-value: {p_a}")
    print(f"p-value (scientific): {p_a:.6e}")
    print(f"Degrees of freedom: {dof_a}")

if __name__ == "__main__":
    main()

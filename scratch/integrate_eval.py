import csv
import json
from pathlib import Path

def get_length_group(text_len):
    if text_len <= 80:
        return "<=80"
    elif text_len <= 160:
        return "81-160"
    elif text_len <= 240:
        return "161-240"
    else:
        return ">240"

def get_obfuscation_group(severity):
    if severity == 0:
        return "0"
    elif severity in (1, 2):
        return "1-2"
    elif severity in (3, 4):
        return "3-4"
    return "unknown"

def compute_metrics(tp, fp, tn, fn):
    # Class 1 metrics
    prec_1 = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    rec_1 = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1_1 = 2 * prec_1 * rec_1 / (prec_1 + rec_1) if (prec_1 + rec_1) > 0 else 0.0

    # Class 0 metrics
    prec_0 = tn / (tn + fn) if (tn + fn) > 0 else 0.0
    rec_0 = tn / (tn + fp) if (tn + fp) > 0 else 0.0
    f1_0 = 2 * prec_0 * rec_0 / (prec_0 + rec_0) if (prec_0 + rec_0) > 0 else 0.0

    macro_f1 = (f1_1 + f1_0) / 2
    return prec_1, rec_1, f1_1, macro_f1

def main():
    metadata_path = Path("data/processed/metadata_phase2_mistral_final.jsonl")
    pred_dir = Path("scratch/predictions")
    
    # 4 models predictions files
    pred_files = {
        "CafeBERT": pred_dir / "plm_cafebert_predictions_dev.csv",
        "DistilBERT multilingual": pred_dir / "plm_distilledbert_predictions_dev.csv",
        "TextCNN": pred_dir / "char_textcnn_hard_predictions_dev.csv",
        "TextCNN distilled": pred_dir / "char_textcnn_distilled_phobert_base_predictions_dev.csv"
    }

    # Load canonical metadata
    metadata = {}
    with open(metadata_path, encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            item = json.loads(line)
            sid = item["sample_id"]
            
            # Extract new metadata fields
            surface = item.get("surface_features", {})
            target = item.get("target_audience", {})
            obf = item.get("obfuscation", {})
            actions = item.get("requested_actions", {})
            
            metadata[sid] = {
                "message_domain": item.get("message_domain", "other"),
                "sender_type": item.get("sender_type", "unknown"),
                "has_url": surface.get("has_url", False),
                "has_phone_number": surface.get("has_phone_number", False),
                "text_noise_score": surface.get("text_noise_score", 0),
                "obfuscation_present": obf.get("present", False),
                "obfuscation_severity": obf.get("severity", 0),
                "persuasion_tactics": item.get("persuasion_tactics", []),
                "requested_actions": actions.get("types", []),
                "target_roles": target.get("roles", [])
            }

    # Load predictions per model
    predictions = {}  # model -> sample_id -> {label, pred, confidence}
    for model_name, path in pred_files.items():
        predictions[model_name] = {}
        with open(path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                sid = row["sample_id"]
                label = int(row["label"])
                pred = int(row["pred"])
                conf = float(row["confidence"])
                content = row["content"]
                
                # Check consistency
                predictions[model_name][sid] = {
                    "label": label,
                    "pred": pred,
                    "confidence": conf,
                    "content": content,
                    "data_origin": row.get("data_origin", "real")
                }

    # Verify dev split consistency
    dev_sample_ids = list(predictions["CafeBERT"].keys())
    print(f"Total dev sample IDs: {len(dev_sample_ids)}")
    
    # Check that all models have the same sample IDs
    for m in predictions:
        assert set(predictions[m].keys()) == set(dev_sample_ids), f"Sample ID mismatch for model {m}"

    # Analyze slices
    slices_data = []  # will contain dicts to write to CSV

    # We will define the slices
    # Slices will be represented as (slice_type, slice_value, filter_func)
    slice_definitions = []
    
    # 1. Length
    for g in ["<=80", "81-160", "161-240", ">240"]:
        slice_definitions.append(("length", g, lambda sid, m=g: get_length_group(len(predictions["CafeBERT"][sid]["content"])) == m))
        
    # 2. URL presence
    slice_definitions.append(("has_url", "true", lambda sid: metadata[sid]["has_url"]))
    slice_definitions.append(("has_url", "false", lambda sid: not metadata[sid]["has_url"]))
    
    # 3. Phone number presence
    slice_definitions.append(("has_phone", "true", lambda sid: metadata[sid]["has_phone_number"]))
    slice_definitions.append(("has_phone", "false", lambda sid: not metadata[sid]["has_phone_number"]))
    
    # 4. Sender type
    for st in ["brandname", "personal_number", "shortcode"]:
        slice_definitions.append(("sender_type", st, lambda sid, m=st: metadata[sid]["sender_type"] == m))
        
    # 5. Data origin
    for do in ["real", "external_real", "external_curated"]:
        slice_definitions.append(("data_origin", do, lambda sid, m=do: predictions["CafeBERT"][sid]["data_origin"] == m))
        
    # 6. Obfuscation level
    for ol in ["0", "1-2", "3-4"]:
        slice_definitions.append(("obfuscation_level", ol, lambda sid, m=ol: get_obfuscation_group(metadata[sid]["obfuscation_severity"]) == m))
        
    # 7. Message domain
    domains = ["telecom", "banking_finance", "healthcare", "public_service", "gambling", "e_commerce", "employment", "investment", "debt_collection", "social_media", "leisure_entertainment", "other"]
    for dom in domains:
        slice_definitions.append(("message_domain", dom, lambda sid, m=dom: metadata[sid]["message_domain"] == m))

    # 8. Requested actions
    actions = ["click_or_visit_link", "call_phone", "provide_personal_info", "send_money_or_payment", "reply_to_message", "download_or_install_app"]
    for act in actions:
        slice_definitions.append(("requested_action", act, lambda sid, m=act: m in metadata[sid]["requested_actions"]))
        
    # 9. Target roles
    roles = ["customer", "debtor", "investor", "job_seeker", "family_member", "generic_user"]
    for r in roles:
        slice_definitions.append(("target_role", r, lambda sid, m=r: m in metadata[sid]["target_roles"]))

    # 10. Persuasion tactics
    tactics = ["link_lure", "scarcity", "reward_incentive", "urgency", "authority", "fear", "threat", "off_platform_contact"]
    for tac in tactics:
        slice_definitions.append(("persuasion_tactic", tac, lambda sid, m=tac: m in metadata[sid]["persuasion_tactics"]))

    # Calculate metrics for each slice and model
    for slice_type, slice_value, filter_func in slice_definitions:
        # Filter samples
        matched_sids = [sid for sid in dev_sample_ids if filter_func(sid)]
        n_total = len(matched_sids)
        if n_total == 0:
            continue
            
        n_label_1 = sum(1 for sid in matched_sids if predictions["CafeBERT"][sid]["label"] == 1)
        n_label_0 = n_total - n_label_1
        
        for model_name in predictions:
            # Calculate TP, FP, TN, FN
            tp, fp, tn, fn = 0, 0, 0, 0
            for sid in matched_sids:
                label = predictions[model_name][sid]["label"]
                pred = predictions[model_name][sid]["pred"]
                if label == 1 and pred == 1:
                    tp += 1
                elif label == 0 and pred == 1:
                    fp += 1
                elif label == 0 and pred == 0:
                    tn += 1
                elif label == 1 and pred == 0:
                    fn += 1
            
            prec_1, rec_1, f1_1, macro_f1 = compute_metrics(tp, fp, tn, fn)
            
            slices_data.append({
                "slice_type": slice_type,
                "slice_value": slice_value,
                "model_name": model_name,
                "n": n_total,
                "n_label_1": n_label_1,
                "n_label_0": n_label_0,
                "tp": tp,
                "fp": fp,
                "tn": tn,
                "fn": fn,
                "precision_1": round(prec_1, 4),
                "recall_1": round(rec_1, 4),
                "f1_1": round(f1_1, 4),
                "macro_f1": round(macro_f1, 4)
            })

    # Write sliced metrics to CSV
    output_dir = Path("scripts/RQ2_RQ3")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    slice_metrics_path = output_dir / "rq2_slice_metrics_dev.csv"
    with open(slice_metrics_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "slice_type", "slice_value", "model_name", "n", "n_label_1", "n_label_0",
            "tp", "fp", "tn", "fn", "precision_1", "recall_1", "f1_1", "macro_f1"
        ])
        writer.writeheader()
        writer.writerows(slices_data)
    print(f"Written sliced metrics to {slice_metrics_path}")

    # Error analysis (RQ3)
    error_overview = []
    model_errors = {}  # model -> set of error sample_ids
    for model_name in predictions:
        errors = set()
        fp, fn = 0, 0
        high_conf_errors = 0
        
        for sid in dev_sample_ids:
            label = predictions[model_name][sid]["label"]
            pred = predictions[model_name][sid]["pred"]
            conf = predictions[model_name][sid]["confidence"]
            
            if label != pred:
                errors.add(sid)
                if label == 0 and pred == 1:
                    fp += 1
                elif label == 1 and pred == 0:
                    fn += 1
                if conf >= 0.9:
                    high_conf_errors += 1
                    
        model_errors[model_name] = errors
        error_overview.append({
            "model_name": model_name,
            "fp": fp,
            "fn": fn,
            "total_errors": len(errors),
            "high_confidence_errors": high_conf_errors
        })
        
    error_overview_path = output_dir / "rq3_error_overview_dev.csv"
    with open(error_overview_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["model_name", "fp", "fn", "total_errors", "high_confidence_errors"])
        writer.writeheader()
        writer.writerows(error_overview)
    print(f"Written error overview to {error_overview_path}")

    # Calculate error overlaps (Jaccard similarity)
    print("\nError overlap Jaccard similarities:")
    models_list = list(predictions.keys())
    for i in range(len(models_list)):
        for j in range(i+1, len(models_list)):
            m1, m2 = models_list[i], models_list[j]
            intersection = len(model_errors[m1] & model_errors[m2])
            union = len(model_errors[m1] | model_errors[m2])
            jaccard = intersection / union if union > 0 else 1.0
            print(f"  {m1} vs {m2}: Jaccard = {jaccard:.4f} ({intersection} common errors out of {union} union)")

    # Find common errors and output representative errors
    all_errors_union = set.union(*model_errors.values())
    all_errors_intersection = set.intersection(*model_errors.values())
    print(f"\nTotal unique errors across all 4 models: {len(all_errors_union)}")
    print(f"Errors made by ALL 4 models: {len(all_errors_intersection)}")
    for sid in all_errors_intersection:
        content = predictions["CafeBERT"][sid]["content"]
        label = predictions["CafeBERT"][sid]["label"]
        print(f"  ALL 4 FAILED: {sid} | Label: {label} | Content: {content}")

    # Select representative errors
    representative_errors = []
    
    for sid in sorted(all_errors_union):
        label = predictions["CafeBERT"][sid]["label"]
        content = predictions["CafeBERT"][sid]["content"]
        
        # Check how many models made this error
        failed_models = [m for m in predictions if sid in model_errors[m]]
        failed_count = len(failed_models)
        
        # Determine error type details
        model_confs = {}
        for m in predictions:
            model_confs[m] = {
                "pred": predictions[m][sid]["pred"],
                "confidence": predictions[m][sid]["confidence"]
            }
            
        representative_errors.append({
            "sample_id": sid,
            "label": label,
            "failed_count": failed_count,
            "failed_models": "|".join(failed_models),
            "content": content,
            "cafebert_pred": model_confs["CafeBERT"]["pred"],
            "cafebert_conf": round(model_confs["CafeBERT"]["confidence"], 4),
            "distilbert_pred": model_confs["DistilBERT multilingual"]["pred"],
            "distilbert_conf": round(model_confs["DistilBERT multilingual"]["confidence"], 4),
            "textcnn_pred": model_confs["TextCNN"]["pred"],
            "textcnn_conf": round(model_confs["TextCNN"]["confidence"], 4),
            "textcnn_dist_pred": model_confs["TextCNN distilled"]["pred"],
            "textcnn_dist_conf": round(model_confs["TextCNN distilled"]["confidence"], 4),
            "message_domain": metadata[sid]["message_domain"],
            "has_url": 1 if metadata[sid]["has_url"] else 0
        })
        
    rep_errors_path = output_dir / "rq3_representative_errors_dev.csv"
    with open(rep_errors_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "sample_id", "label", "failed_count", "failed_models", "content",
            "cafebert_pred", "cafebert_conf",
            "distilbert_pred", "distilbert_conf",
            "textcnn_pred", "textcnn_conf",
            "textcnn_dist_pred", "textcnn_dist_conf",
            "message_domain", "has_url"
        ])
        writer.writeheader()
        writer.writerows(representative_errors)
    print(f"Written representative errors to {rep_errors_path}")

if __name__ == "__main__":
    main()

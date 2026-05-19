import pandas as pd

# ── Cấu hình đường dẫn file ──────────────────────────────────────────────────
VISMISH_PATH = r"data\final\vismishds_phase1_final.csv"   
CHANGED_PATH = r"data\reports\level2_correction_changed_rows.csv" 
# ─────────────────────────────────────────────────────────────────────────────

# 1. Đọc dữ liệu
vismish = pd.read_csv(VISMISH_PATH)
changed = pd.read_csv(CHANGED_PATH)

print(f"[INFO] vismish  : {len(vismish):,} dòng")
print(f"[INFO] changed  : {len(changed):,} dòng")

# 2. Lấy các row_index cần cập nhật từ changed
changed_lookup = changed.set_index("row_index")["content_after"]

# 3. Xác định mask: đúng source_file VÀ có row_index trong changed
mask = (
    (vismish["source_file"] == "data/synthetic/synthetic_label_1.csv") &
    (vismish["source_row_id"].isin(changed_lookup.index))
)

matched_count = mask.sum()
print(f"[INFO] Số dòng sẽ được cập nhật: {matched_count:,}")

# 4. Thay thế content và obfuscation_level
vismish.loc[mask, "content"] = (
    vismish.loc[mask, "source_row_id"].map(changed_lookup).values
)
vismish.loc[mask, "obfuscation_level"] = "NONE"

# 5. Ghi đè lại file vismish gốc
vismish.to_csv(VISMISH_PATH, index=False, encoding="utf-8")

print(f"[DONE] Đã cập nhật và ghi đè '{VISMISH_PATH}' thành công.")
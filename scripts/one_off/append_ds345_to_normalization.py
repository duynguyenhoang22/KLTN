import csv
import re

content_only_path = r'data\normalization\phase2_full_normalization_content_only.csv'
ds345_path = r'data\interim\phase2_append\ds345.csv'

# Get last norm_id number
with open(content_only_path, encoding='utf-8', newline='') as f:
    existing_rows = list(csv.DictReader(f))

last_norm_id = existing_rows[-1]['norm_id']  # e.g. sms_norm_05320
match = re.search(r'(\d+)$', last_norm_id)
next_num = int(match.group(1)) + 1
print(f"Last norm_id: {last_norm_id}, next starts at: {next_num}")

# Read ds345
with open(ds345_path, encoding='utf-8', newline='') as f:
    ds_rows = list(csv.DictReader(f))

print(f"ds345 rows: {len(ds_rows)}")

# Build new rows
new_rows = []
counter = next_num
for row in ds_rows:
    new_rows.append({
        'norm_id': f'sms_norm_{counter:05d}',
        'sample_id': row['sample_id'],
        'source_text': row['content'],
        'normalized_text': row['content_after'],
    })
    counter += 1

print(f"Appending {len(new_rows)} rows (norm_id: sms_norm_{next_num:05d} → sms_norm_{counter-1:05d})")

# Append to file
with open(content_only_path, 'a', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['norm_id', 'sample_id', 'source_text', 'normalized_text'], quoting=csv.QUOTE_ALL)
    writer.writerows(new_rows)

print("Done!")

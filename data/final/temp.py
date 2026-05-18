import pandas as pd

df = pd.read_csv(r'data\final\vismishds_phase1_final.csv')

df_real = df[df['data_origin'] == 'real']
df_synthetic = df[df['data_origin'] == 'synthetic']

df_synth_sampled = df_synthetic.groupby('label').apply(
    lambda x: x.sample(n=min(2000, len(x)), random_state=42)
).reset_index(drop=True)

df_final = pd.concat([df_real, df_synth_sampled])
df_final = df_final.sample(frac=1, random_state=42).reset_index(drop=True)
df_final.to_csv(r'data\final\stratified.csv', index=False)

print("Đã lọc dữ liệu thành công và xuất file 'stratified.csv'!")
print(f"Tổng số mẫu: {len(df_final)}")
print(df_final.groupby(['data_origin', 'label']).size())
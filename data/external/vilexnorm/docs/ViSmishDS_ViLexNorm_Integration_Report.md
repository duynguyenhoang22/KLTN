# Bao cao tich hop ViLexNorm

Trang thai: chua tich hop vao dataset final.

## Artifact dau ra du kien

```text
data/external/vilexnorm/curated/vilexnorm_clean_p2p_label0.csv
data/external/vilexnorm/curated/vilexnorm_hard_negative_label0.csv
data/interim/vilexnorm_integration/synthetic_label0_removed.csv
data/interim/vilexnorm_integration/synthetic_label0_kept.csv
data/interim/vilexnorm_integration/vismishds_vilexnorm_merge_preview.csv
data/final/vismishds_phase1_vilexnorm_augmented.csv
```

## Bao cao can cap nhat khi chay pipeline

- So mau ViLexNorm raw/processed/curated.
- So mau synthetic label 0 bi loai theo category/source/template.
- Phan phoi label, source, sender_type, category sau merge.
- Ty le clean P2P va hard negatives.
- Ket qua dedup voi ViSmishDS hien tai.
- Rui ro label noise con lai.

## Tieu chi chap nhan

Dataset moi chi nen duoc xem la ban ung vien neu giu duoc can bang label, giam template bias cua label 0, va khong lam tang false negative tren label 1 trong cac thiet lap danh gia hard-case.

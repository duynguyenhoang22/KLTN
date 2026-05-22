# Quy tac loc ViLexNorm

## Dau vao

ViLexNorm duoc dung theo cap `original -> normalized`.

- `original`: co the dung lam `content` cho label 0 sau khi loc.
- `normalized`: co the dung cho Phase 2 normalization nhu auxiliary target.

## Clean benign P2P

Dieu kien uu tien:

- Do dai vua phai, gan tin nhan P2P.
- Khong URL, khong so dien thoai lien he.
- Khong CTA nhu "bam link", "ib", "lien he zalo", "tham gia ngay".
- Khong quang cao dich vu/san pham.
- Khong tuyen dung, kiem tien, vay tien, co bac, betting.
- Khong noi dung nhay cam/tuc qua manh.

Metadata mac dinh:

```text
label = 0
sender_type = personal_number
category = P2P hoi thoai thong thuong
obfuscation_level = NONE
data_origin = external_real
source_dataset = vilexnorm_clean_p2p
```

## Curated hard negatives

Chi giu khi intent benign ro rang.

Co the bao gom:

- Canh bao nguoi than/ban be ve lua dao.
- Nhac den ngan hang/link/tuyen dung/vay tien nhu mot chu de hoi thoai.
- Noi ve scam nhu mot hien tuong, khong keu goi hanh dong nguy hiem.

Khong dua vao train chinh neu:

- Co loi moi lien he/Zalo/Telegram molog.
- Co loi hua thu nhap/thuong/hoan tien bat thuong.
- Co URL khong xac minh duoc tinh hop le.
- Co hanh vi dung voi smishing/spam.

## Obfuscation level

Khong thay doi quy tac hien tai. Teencode, viet tat va bien the khau ngu benign nhu `k`, `hong`, `thoai`, `dẫy` van gan:

```text
obfuscation_level = NONE
```

Neu can phan tich rieng, dung metadata phu:

```text
text_variant_type = teencode | abbreviation | slang | dialectal_variant | informal_spelling
```

# Ke hoach mo rong/cai thien ViSmishDS bang ViLexNorm

## Muc tieu

Su dung mot phan ViLexNorm de giam phu thuoc vao synthetic label 0, bo sung mien hoi thoai P2P benign va tao mot nhanh hard negatives co kiem soat.

## Nguyen tac

- Khong tron toan bo ViLexNorm vao ViSmishDS.
- Khong xem ViLexNorm la SMS P2P that 100%; day la external conversational/social text.
- Khong gan cac mau scam-like thanh label 0 theo cach tu dong.
- Giu tong label 0 gan muc hien tai de khong pha can bang nhan.
- Giu `obfuscation_level = NONE` cho teencode/viet tat P2P benign, vi obfuscation_level hien tai chi mo ta obfuscation co chu dich trong smishing.

## Cau hinh muc tieu

```text
Label 0 muc tieu: khoang 5,320 mau

- real_label_0 hien tai:             2,321
- synthetic_label_0 giu lai:         1,800-2,000
- ViLexNorm clean benign P2P:        900-1,100
- ViLexNorm curated hard negatives:  200-400
```

## Phan nhanh ViLexNorm

`clean benign P2P` la cac mau hoi thoai doi thuong, khong URL, khong CTA, khong quang cao, khong tuyen dung/kiem tien/vay tien/co bac.

`curated hard negatives` la cac mau label 0 co dau hieu be mat de lan voi smishing nhung intent benign ro rang, vi du canh bao lua dao, nhac den ngan hang/link trong ngu canh phong tranh, hoac noi ve tuyen dung/vay tien nhu mot chu de hoi thoai.

## Dieu kien thanh cong

- F1 tong the khong giam dang ke.
- Recall label 1 khong giam.
- False positive tren P2P benign giam.
- False positive tren hard negatives khong tang qua manh.
- Real-only evaluation on dinh hon hoac it nhat khong xau di.

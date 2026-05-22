# ViLexNorm filter report

Mode: `full`
Input file: `data\external\vilexnorm\processed\vilexnorm_all.csv`
Total routed rows: 10,467

## Output files

- `data/external/vilexnorm/processed/vilexnorm_clean_candidates.csv`
- `data/external/vilexnorm/processed/vilexnorm_hard_negative_candidates.csv`
- `data/external/vilexnorm/processed/vilexnorm_rejected.csv`

## Candidate counts

| Candidate type | Rows |
|:--|--:|
| clean_p2p | 9,622 |
| hard_negative | 816 |
| rejected | 29 |

## Top reject reasons

| Value | Rows |
|:--|--:|
| too_long | 28 |
| has_contact_platform_keyword+has_money_keyword | 1 |

## Hard-case types

| Value | Rows |
|:--|--:|
| sensitive_review | 332 |
| money_like | 269 |
| finance_like | 139 |
| job_like | 42 |
| authority_like | 34 |
| warning_like | 28 |
| cta_like | 19 |
| contact_like | 4 |
| gambling_like | 1 |
| phone_like | 1 |

## Text variant types

| Value | Rows |
|:--|--:|
| standard_or_unknown | 4,719 |
| abbreviation | 3,456 |
| teencode | 2,730 |
| slang | 342 |
| informal_spelling | 335 |
| dialectal_variant | 259 |

## Top flags

| Value | Rows |
|:--|--:|
| has_abbreviation | 3,456 |
| has_teencode | 2,730 |
| has_slang | 342 |
| has_sensitive_review_keyword | 336 |
| has_informal_spelling | 335 |
| has_dialectal_variant | 259 |
| has_money_amount | 200 |
| has_money_keyword | 158 |
| has_finance_keyword | 143 |
| has_soft_cta_keyword | 74 |
| long_for_clean | 73 |
| has_soft_job_keyword | 56 |
| has_job_keyword | 40 |
| has_authority_keyword | 36 |
| has_warning_keyword | 28 |
| too_long | 28 |
| has_cta_keyword | 9 |
| has_contact_platform_keyword | 5 |
| has_gambling_keyword | 1 |
| has_phone_number | 1 |

## Examples

### clean_p2p
- `no_risk_flags` | thích anh cá mập k
- `no_risk_flags` | cứ ngây thơ thế thoai :))
- `no_risk_flags` | bà Nghê xinh vậy mà t thấy k bằng bà ChiPu luôn chời
- `no_risk_flags` | Ê k khóc được làm thế nào má =))?
- `no_risk_flags` | Có biến gì hong dẫy :))

### hard_negative
- `sensitive_review` | Hjc ai cần gia sư mà diệt fò giỏi hơn dạy học thì gọi mình nhé
- `money_like;sensitive_review` | Thế nào đc 9.5 thật đó đỉnh vãi ò, đã v mk điểm cao nhất lớp chứ đc cô thưởng 300k
- `authority_like` | bạn mình bị ồi, nhờ CA thì phải chung nhìu tiền.
- `sensitive_review` | Cho lên phường cmn đi.
- `sensitive_review` | tâm lí tội phạm đây r :)))

### rejected
- `too_long` | Đợt rồi mình đi xem concert Mỹ Tâm một mình ngoài lí do mình là fan ra thì còn là vì ko quen thân người bạn nào cũng thích MT nên ko biết rũ ai, hồi concert Hearbeat 2014 của chỉ đ
- `too_long` | Bạn nhận việc là phải làm hết việc chứ không phải là làm hết giờ,khi nào bạn không nhận việc hoặc là việc đó bạn làm xong rồi mà bị giao thêm bất ngờ thì bạn mới có thể từ chối,chứ
- `too_long` | Hồi nào xem hay đọc phỏng vấn gì của Lâm Y Thần thấy cô ấy nói là 2 vợ chồng 1 năm chắc gặp nhau có vài lần, tại chồng làm việc ở bên Mỹ, việc bên nội bên ngoại đều 1 mình cổ lo hế
- `too_long` | Ăn ở nhà mà bới lên thế t còn chửi cho chứ đừng bảo đến nhà ny ăn  con gái con lứa ăn uống ý tứ chứ nhỉ , học ăn học nói học gói học mở , con gái t mới 4tuổi mà ở nhà mỗi cái chuyệ
- `too_long` | trước giờ phim đài mà mình xem lúc nào cũng truyền cho mình giá trị tinh thần rất tốt, từ cảm giác lạc quan cho đến niềm tin vào những điều may mắn , à với lại những nữ 9 mà bây gi


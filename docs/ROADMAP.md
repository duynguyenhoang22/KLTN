# Roadmap phục hồi và phát triển ViSmishDS v2

Ngày lập kế hoạch: 2026-06-20  
Trạng thái: Draft điều phối chính  
Phạm vi: Dataset, metadata, synthetic validation, thí nghiệm và luận văn

## 1. Mục tiêu

Mục tiêu trước mắt không phải chạy thêm mô hình, mà là tạo một dataset v2 có:

- phạm vi và đối tượng dữ liệu được mô tả rõ;
- metadata có định nghĩa độc lập, nhất quán và kiểm chứng được;
- quy trình annotation có độ đồng thuận và khả năng truy vết;
- dữ liệu synthetic được kiểm định bằng rubric, nhiều judge và human review;
- split và thí nghiệm không bị confounding giữa nhãn, nguồn và category;
- đủ bằng chứng để viết lại Chương 3–5 mà không kết luận vượt quá dữ liệu.

## 2. Nguyên tắc ưu tiên

Mức ưu tiên được dùng trong roadmap:

- **P0 — Blocker:** chưa hoàn thành thì không được chạy full annotation, sinh thêm
  dữ liệu hoặc thiết kế lại benchmark.
- **P1 — Bắt buộc:** cần hoàn thành để dataset v2 đủ điều kiện đóng băng.
- **P2 — Thực nghiệm:** chỉ bắt đầu sau khi dataset v2 vượt quality gate.
- **P3 — Mở rộng:** có giá trị nhưng không nằm trên critical path của khóa luận.

Thứ tự bắt buộc:

```text
Định nghĩa bài toán
→ Schema/taxonomy
→ Pilot annotation
→ Full annotation
→ Synthetic audit
→ Dataset release
→ Split và thí nghiệm
→ Viết lại luận văn
→ Distillation mở rộng
```

## 3. Tổng hợp vấn đề hiện tại

### 3.1. Phạm vi dữ liệu chưa được kiểm soát

**Hiện trạng**

- Chưa mô tả rõ tin nhắn hướng đến nhóm tuổi, giới, nghề nghiệp hoặc trạng thái
  đời sống nào.
- Chưa phân biệt “không có đối tượng cụ thể”, “hướng đến số đông” và “không đủ
  thông tin để xác định”.
- Không có evidence span nên metadata nhân khẩu học dễ trở thành suy diễn.
- Dữ liệu real Label 1 chỉ có 246 mẫu, khó đại diện không gian smishing.

**Rủi ro**

- Luận văn không rào được phạm vi áp dụng.
- Phân tích lát cắt có thể dựa trên stereotype thay vì bằng chứng.
- Nhóm có ít mẫu tạo ra metric không ổn định nhưng vẫn bị diễn giải quá mức.

### 3.2. `category` không phải taxonomy trung lập

**Hiện trạng**

- Category chứa trực tiếp trạng thái thật/giả: `Ngân hàng thật` và
  `Giả mạo ngân hàng`, `Dịch vụ công thật` và `Dịch vụ công giả`.
- Category gần như tách biệt theo label.
- Một số tên category lịch sử không thống nhất.

**Rủi ro**

- Category bị confound với label.
- Không thể so sánh Label 0 và Label 1 trong cùng một miền nội dung.
- Nếu category đi vào prompt, split hoặc model input có thể gây leakage.

### 3.3. `obfuscation_level` có định nghĩa mâu thuẫn

**Hiện trạng**

- `NONE` và `LEVEL 0` cùng tồn tại nhưng không cùng ý nghĩa.
- Label 1 có 2.503 mẫu `NONE`; Label 0 có 5.320 mẫu `NONE`.
- Thứ tự Level 3/4 giữa script và dataset từng bị đảo.
- Level hiện tại trộn “kỹ thuật” với “độ nặng”.
- Không biểu diễn được nhiều kỹ thuật đồng thời.
- Viết tắt, teencode, bỏ dấu và typo chưa được tách khỏi hành vi cố ý che giấu.

**Rủi ro**

- Không thể dùng level làm biến thứ tự đáng tin cậy.
- Phân tích hiệu năng theo level không có giá trị nhân quả.
- Không thể mở rộng thuộc tính sang Label 0 một cách nhất quán.

### 3.4. Metadata còn nông và thiếu provenance

**Hiện trạng**

- Schema cũ chủ yếu gồm URL, số điện thoại, sender, category và obfuscation.
- Không có chiến thuật thuyết phục, hành động được yêu cầu, đối tượng đích,
  evidence, confidence hoặc annotator.
- Không có trạng thái auto-label, human-reviewed và adjudicated.

**Rủi ro**

- Ít lát cắt có giá trị giải thích.
- Không phân biệt ground truth với metadata do LLM suy đoán.
- Không thể audit khi guideline thay đổi.

### 3.5. Synthetic data chưa có kiểm định nội dung đủ mạnh

**Hiện trạng**

- Validation cũ chủ yếu kiểm schema, URL/phone, phân phối và artifact.
- Chưa có bằng chứng hai LLM-as-judge độc lập.
- Chưa có rubric cụ thể cho label consistency, metadata consistency,
  contradiction, realism, template artifact và hallucinated entity.
- Synthetic Label 1 chiếm 4.996/5.242 positive samples.

**Rủi ro**

- Lỗi của generator được xem như ground truth.
- Judge có thể đồng thuận giả nếu dùng cùng model family hoặc cùng prompt.
- Mô hình học artifact sinh dữ liệu thay vì hành vi lừa đảo.

### 3.6. Prompt tạo sinh phụ thuộc taxonomy cũ

**Hiện trạng**

- Prompt cũ đưa category và obfuscation range trực tiếp vào quá trình sinh.
- Một số category có quota quá đều.
- Domain, độ dài và URL của synthetic khác real rõ rệt.
- Prompt có nguy cơ tạo nhãn và metadata theo thiết kế thay vì theo nội dung.

**Rủi ro**

- Metadata chỉ phản ánh instruction, không phản ánh mẫu thực tế.
- Synthetic có pattern lặp, miền hẹp và shortcut rõ.
- Tái sinh mà chưa sửa taxonomy chỉ nhân rộng lỗi.

### 3.7. Thiết kế thí nghiệm synthetic chưa cô lập được nguyên nhân

**Hiện trạng**

- Thêm ngẫu nhiên 500/1.000/2.000/toàn bộ synthetic không trả lời thành phần
  nào tạo cải thiện.
- Label và data origin bị confound mạnh.
- Random split có thể chia sẻ template giữa train và test.
- Chưa có metadata-matched control hoặc template-family holdout.

**Rủi ro**

- Không phân biệt hiệu ứng số lượng, domain coverage, noise hay template.
- Kết luận “synthetic hữu ích” có thể chỉ là hiệu ứng tăng số mẫu.
- Metric cao trên split trộn không chứng minh tổng quát hóa trên real data.

### 3.8. Distillation chưa đủ sâu và đang sai thứ tự ưu tiên

**Hiện trạng**

- Teacher chưa vượt rõ các student ở mọi metric.
- Soft-label distillation chưa tạo cải thiện nhất quán.
- Dataset và split chưa ổn định nhưng đã có nhiều artifact distillation.

**Rủi ro**

- Đầu tư thêm vào distillation trước khi sửa dữ liệu làm tăng chi phí tái chạy.
- Không thể tách lợi ích của distillation khỏi thay đổi dữ liệu.
- Đóng góp nghiên cứu bị dàn trải.

### 3.9. Quy trình repo trước đây thiếu source of truth

**Hiện trạng**

- Dataset, notebook, prediction, model và báo cáo từng nằm lẫn nhau.
- Có nhiều biến thể split/output nhưng không rõ bản canonical.
- Artifact lớn được commit trực tiếp.

**Trạng thái**

- Đã xử lý bước đầu trên nhánh `codex/dataset-v2-restructure`.
- Repo v2 đã tách source, reference, annotation, processed và release.
- Vẫn cần thiết lập manifest/release protocol trước khi chạy pipeline lớn.

## 4. Kế hoạch theo thứ tự ưu tiên

## P0.1 — Đóng băng định nghĩa bài toán và phạm vi

**Mục tiêu**

Xác định chính xác dataset đang đại diện cho cái gì và không đại diện cho cái gì.

**Việc cần làm**

1. Viết dataset scope statement:
   - loại tin nhắn được chấp nhận;
   - định nghĩa Label 0 và Label 1;
   - ca mơ hồ/không đủ ngữ cảnh;
   - nguồn real, synthetic và external;
   - phạm vi tiếng Việt, SMS và social-text;
   - hạn chế về thời gian, vùng miền và đối tượng.
2. Quy định `unknown`, `general`, `other`:
   - `unknown`: không đủ bằng chứng;
   - `general`: nội dung rõ ràng hướng đến số đông;
   - `other`: có thể xác định nhưng nằm ngoài taxonomy.
3. Quy định khi nào loại mẫu:
   - nội dung rỗng/hỏng;
   - trùng lặp;
   - label không thể adjudicate;
   - thiếu ngữ cảnh nghiêm trọng;
   - chứa dữ liệu nhạy cảm cần xử lý.
4. Chốt đơn vị phân tích: một bản ghi là một SMS độc lập hay đoạn hội thoại.

**Đầu ra**

- `docs/dataset_scope.md`
- danh sách inclusion/exclusion rules;
- taxonomy ca mơ hồ.

**Quality gate**

- Hai thành viên có thể gán label cho 50 ca khó bằng cùng guideline.
- Mọi thuật ngữ `unknown/general/other` có ví dụ dương và phản ví dụ.

## P0.2 — Khóa schema và taxonomy metadata v2

**Mục tiêu**

Tạo metadata độc lập với label, áp dụng được cho cả real và synthetic.

**Việc cần làm**

1. Review `configs/taxonomy.json`.
2. Chốt `message_domain` trung lập.
3. Tách:
   - hiện tượng văn bản: `text_phenomena`;
   - mức phi chuẩn: `text_noise_score`;
   - ý định che giấu: `obfuscation.present`;
   - kỹ thuật che giấu: `obfuscation.techniques`;
   - độ nặng: `obfuscation.severity`.
4. Chốt target audience:
   - age group;
   - gender;
   - occupation;
   - life status;
   - evidence.
5. Chốt persuasion tactics và action/request type.
6. Bổ sung giá trị `not_applicable` nếu một trường thực sự không áp dụng;
   không dùng `unknown` thay cho mọi trạng thái thiếu.
7. Đảm bảo schema và taxonomy không có giá trị “thật/giả” ngoài `label`.

**Đầu ra**

- `configs/taxonomy.json` phiên bản khóa;
- `configs/dataset_v2.schema.json`;
- data dictionary mô tả từng trường;
- changelog taxonomy.

**Quality gate**

- 100% trường có định nghĩa, allowed values và ví dụ.
- Schema validation chạy được.
- Không có field suy ra trực tiếp label.
- Multi-label dùng array, không nhồi danh sách vào một chuỗi CSV.

## P0.3 — Thiết kế annotation guideline và pilot

**Mục tiêu**

Kiểm tra metadata có thực sự gán được một cách nhất quán.

**Việc cần làm**

1. Dùng pilot 400 mẫu đã tạo, cân bằng:
   - 100 real Label 0;
   - 100 synthetic Label 0;
   - 100 real Label 1;
   - 100 synthetic Label 1.
2. Không hiển thị category và obfuscation cũ cho annotator.
3. Hai annotator độc lập gán ít nhất 150–200 mẫu giao nhau.
4. Ghi:
   - giá trị metadata;
   - evidence;
   - confidence;
   - review note.
5. Tạo danh sách disagreement.
6. Adjudicate và cập nhật guideline.
7. Chạy vòng pilot thứ hai trên 50–100 mẫu mới nếu thay đổi guideline lớn.

**Đầu ra**

- hai annotation export độc lập;
- disagreement report;
- adjudicated pilot;
- guideline phiên bản tiếp theo;
- báo cáo thời gian gán mỗi mẫu.

**Quality gate**

- Cohen's Kappa ≥ 0,70 cho `message_domain` và các trường đơn nhãn cốt lõi.
- Multi-label agreement được báo cáo theo micro/macro F1 hoặc Jaccard.
- Không có category nào annotator hiểu theo hai định nghĩa khác nhau.
- Tỷ lệ `unknown` được chấp nhận như kết quả, không ép giảm.

## P0.4 — Xây pipeline annotation và validation có truy vết

**Mục tiêu**

Không để annotation full-scale trở thành các file CSV sửa tay không kiểm soát.

**Việc cần làm**

1. Bổ sung lệnh:
   - import annotation CSV;
   - xuất JSONL canonical;
   - validate evidence/confidence;
   - phát hiện duplicate sample ID;
   - so sánh hai annotator;
   - tạo adjudication queue.
2. Lưu annotation provenance:
   - annotator/model ID;
   - timestamp;
   - guideline version;
   - prompt version nếu dùng LLM.
3. Tạo schema riêng cho raw annotation event nếu cần.
4. Thêm unit test và integration test.
5. Không ghi đè annotation cũ; append event hoặc tạo version mới.

**Đầu ra**

- pipeline trong `src/vismishds/`;
- test suite;
- annotation manifest;
- audit report tự động.

**Quality gate**

- Có thể tái tạo canonical pilot từ raw annotation.
- Mọi record không hợp lệ bị chặn trước release.
- Không có chỉnh sửa im lặng không lưu provenance.

## P1.1 — Gán lại metadata toàn bộ dữ liệu

**Mục tiêu**

Tạo metadata v2 cho toàn bộ candidate pool mà không phụ thuộc taxonomy cũ.

**Việc cần làm**

1. Chọn chiến lược:
   - human-only cho tập real Label 1 và ca khó;
   - LLM-assisted cho tập lớn;
   - human review theo confidence và sampling.
2. Ưu tiên review:
   - toàn bộ 246 real Label 1;
   - toàn bộ mẫu label mơ hồ;
   - mẫu có nhiều kỹ thuật noise/obfuscation;
   - mẫu LLM judges bất đồng;
   - mẫu confidence thấp;
   - mẫu ngẫu nhiên theo từng stratum.
3. Không dùng category/obfuscation cũ làm input gán.
4. So sánh phân phối auto-label và human-label để tìm bias.
5. Adjudicate trước khi canonicalize.

**Đầu ra**

- canonical annotation JSONL;
- review queue đã xử lý;
- metadata coverage report;
- danh sách excluded/ambiguous records.

**Quality gate**

- 100% record có annotation status và guideline version.
- 100% target-audience cụ thể có evidence.
- 100% confidence thấp được review hoặc đánh dấu chưa đủ điều kiện release.
- Báo cáo tỷ lệ unknown theo nguồn và nhãn.

## P1.2 — Kiểm định synthetic bằng hai LLM-as-judge

**Mục tiêu**

Cung cấp bằng chứng định lượng và định tính về chất lượng synthetic.

**Rubric bắt buộc**

1. Label consistency.
2. Semantic coherence và contradiction.
3. Metadata consistency.
4. Vietnamese SMS realism.
5. Requested-action plausibility.
6. Entity/URL/phone artifact.
7. Template similarity và repetition.
8. Target-audience evidence.
9. Obfuscation/noise correctness.
10. Safety/privacy issue.

**Việc cần làm**

1. Chọn hai judge khác model generator và ưu tiên khác model family.
2. Khóa prompt, model version, temperature và output schema.
3. Judge độc lập, không thấy đánh giá của nhau.
4. Không cho judge category/obfuscation legacy.
5. Tạo rule:
   - cả hai pass → candidate pass;
   - một pass/một fail → human review;
   - cả hai fail → reject hoặc human adjudication theo loại lỗi;
   - parse failure → retry giới hạn rồi chuyển review.
6. Human audit:
   - toàn bộ disagreement;
   - toàn bộ high-severity failure;
   - mẫu ngẫu nhiên trong nhóm both-pass;
   - mẫu ngẫu nhiên theo category/domain.
7. Tính agreement giữa judges và giữa judge với human.

**Đầu ra**

- judge rubric;
- prompt/version manifest;
- raw judge outputs;
- disagreement queue;
- human audit report;
- accepted/rejected synthetic manifest.

**Quality gate**

- Không tuyên bố “chống hallucination” chỉ từ một điểm tổng.
- Có confusion/agreement theo từng tiêu chí.
- Tỷ lệ human-audited both-pass đủ để ước lượng false acceptance.
- Mọi synthetic trong release có trạng thái kiểm định.

## P1.3 — Quyết định sửa, lọc hay tái sinh synthetic

**Mục tiêu**

Không tái sinh theo cảm tính; quyết định dựa trên audit.

**Quy tắc quyết định**

- **Giữ:** nội dung và metadata đạt rubric.
- **Sửa:** lỗi cục bộ, có thể hiệu chỉnh mà không đổi ý nghĩa/label.
- **Loại:** incoherent, label sai, template trùng nặng, artifact không cứu được.
- **Tái sinh:** một domain/tactic/target group thiếu coverage có hệ thống.

**Việc cần làm**

1. Đo coverage v2 sau lọc.
2. Xác định ô thiếu theo:
   - domain;
   - tactic;
   - target audience có bằng chứng;
   - text phenomena;
   - URL/no URL;
   - sender type;
   - length bin.
3. Nếu tái sinh:
   - prompt không yêu cầu một `obfuscation level`;
   - yêu cầu kỹ thuật multi-label cụ thể;
   - không tự tin metadata do generator trả là ground truth;
   - kiểm định lại qua hai judges.
4. Tách `generated_metadata` khỏi `verified_metadata`.

**Đầu ra**

- repair/reject/regenerate manifest;
- prompt v2 nếu cần;
- synthetic candidate pool mới;
- before/after quality report.

**Quality gate**

- Không có quota đều giả tạo mà không được giải thích.
- Không có template family chiếm tỷ trọng quá lớn.
- Synthetic không được release chỉ vì parser hợp lệ.

## P1.4 — Deduplication, leakage và split protocol

**Mục tiêu**

Tạo split đánh giá phản ánh khả năng tổng quát hóa.

**Việc cần làm**

1. Exact duplicate theo normalized content.
2. Near-duplicate theo character n-gram/embedding.
3. Nhóm template/source family.
4. Giữ mọi biến thể cùng family trong một split.
5. Thiết kế tối thiểu:
   - real-only test;
   - development split để chọn model;
   - external/domain-shift challenge;
   - template-family holdout.
6. Không để synthetic vào test chính.
7. Stratify có kiểm soát, nhưng không phá group isolation.
8. Khóa test và checksum.

**Đầu ra**

- duplicate clusters;
- family/group IDs;
- split manifest;
- leakage report;
- checksum và release ID.

**Quality gate**

- Không exact duplicate giữa train/dev/test.
- Near-duplicate leakage dưới ngưỡng đã công bố.
- Test chính chỉ chứa dữ liệu phù hợp câu hỏi tổng quát hóa.
- Split không được thay đổi sau khi xem test result.

## P1.5 — Đóng băng Dataset Release v2

**Mục tiêu**

Tạo nguồn sự thật duy nhất cho mọi thí nghiệm sau đó.

**Việc cần làm**

1. Xuất canonical JSONL.
2. Xuất flattened CSV chỉ cho mục đích tương thích.
3. Tạo datasheet/dataset card.
4. Ghi:
   - schema version;
   - guideline version;
   - source checksums;
   - annotation statistics;
   - judge/human audit;
   - exclusions;
   - limitations;
   - intended/not-intended uses.
5. Gắn release ID và changelog.

**Đầu ra**

- `vismishds-v2.x.jsonl`;
- split files/manifests;
- dataset card;
- quality report;
- checksum file.

**Quality gate**

- Schema validation 100%.
- Không còn annotation trạng thái chưa duyệt trong release.
- Có báo cáo đầy đủ theo `label × origin × domain`.
- Release có thể tái tạo từ source và annotation manifest.

## P2.1 — Thiết kế lại thí nghiệm giá trị synthetic

**Mục tiêu**

Xác định synthetic hữu ích ở đâu và vì sao.

**Thiết lập ưu tiên**

1. **Real-only anchor.**
2. **Synthetic-only/TSTR:** kiểm tra khả năng thay thế real.
3. **Random augmentation control:** thêm N mẫu ngẫu nhiên.
4. **Metadata-matched augmentation:** cùng N nhưng match theo domain, độ dài,
   URL, sender và noise.
5. **Diversity ablation:**
   - domain diversity;
   - tactic diversity;
   - text-phenomena diversity;
   - target-audience diversity nếu đủ bằng chứng.
6. **Quality ablation:** accepted-by-both-judges so với unfiltered synthetic.
7. **Template holdout:** đo phụ thuộc pattern.

**Quy tắc**

- Cùng model, hyperparameter budget và split.
- Nhiều seed.
- Báo cáo mean, standard deviation và confidence interval.
- Theo dõi Precision, Recall, F1 Label 1, Macro-F1, PR-AUC, FP và FN.
- So sánh cùng số lượng mẫu để tách hiệu ứng chất lượng khỏi số lượng.

**Quality gate**

- Mỗi thí nghiệm trả lời một giả thuyết cụ thể.
- Không dùng test để chọn biến thể.
- Kết luận phân biệt rõ replacement, augmentation và robustness.

## P2.2 — Benchmark mô hình trên Dataset v2

**Mục tiêu**

Đánh giá mô hình sau khi nền dữ liệu đã ổn định.

**Việc cần làm**

1. Chọn ít baseline có vai trò rõ:
   - TF-IDF/linear;
   - character-level;
   - một PLM base;
   - model mạnh nhất khả thi.
2. Khóa preprocessing và max length.
3. Phân tích lát cắt chỉ trên metadata đủ mẫu.
4. Báo cáo uncertainty khi nhóm nhỏ.
5. Error analysis theo taxonomy v2.

**Quality gate**

- Prediction-level artifact có sample ID và release ID.
- Metric tái tạo được.
- Không khẳng định quan hệ nhân quả từ lát cắt quan sát.

## P2.3 — Viết lại Chương 3, 4 và 5

**Mục tiêu**

Đồng bộ luận văn với dataset và thực nghiệm mới.

**Thứ tự viết**

1. Chương 3: nguồn, phạm vi, schema, annotation, quality control, limitations.
2. Chương 4: research questions, split protocol, benchmark và ablation.
3. Chương 5: kết quả theo RQ, uncertainty, error analysis.
4. Chương 6/kết luận: giới hạn và hướng mở rộng.

**Bằng chứng bắt buộc**

- IAA của annotator.
- Agreement hai judges và human audit.
- Metadata coverage.
- Leakage/dedup report.
- Dataset release ID.
- Confidence interval hoặc variability nhiều seed.

**Quality gate**

- Mọi bảng/hình có script và input xác định.
- Không dùng `obfuscation_level` legacy làm kết luận chính.
- Không gọi synthetic “đã chống hallucination” nếu chỉ có judge score.
- Không gọi distillation là đóng góp trung tâm nếu kết quả không hỗ trợ.

## P3.1 — Distillation mở rộng

**Điều kiện bắt đầu**

Chỉ bắt đầu khi Dataset v2 và benchmark chính đã đóng băng.

**Hướng khả thi**

- Teacher ensemble hoặc teacher mạnh hơn.
- Confidence-aware distillation.
- Hard-label anchor và disagreement weighting.
- Feature/logit distillation thay vì chỉ soft target.
- Calibration và resource-quality Pareto analysis.
- So sánh bắt buộc với cùng student hard-label.

**Tiêu chí giữ trong luận văn**

Distillation chỉ được nâng thành đóng góp chính nếu:

- cải thiện ổn định so với cùng student hard-label;
- hoặc giữ chất lượng trong sai số chấp nhận được nhưng giảm tài nguyên rõ rệt;
- kết quả lặp lại trên nhiều seed và split đánh giá đã khóa.

Nếu không đạt, giữ như một cấu hình benchmark hoặc hướng nghiên cứu tương lai.

## 5. Critical path

Các công việc nằm trên đường găng:

| Thứ tự | Công việc | Phụ thuộc | Trạng thái |
|---:|---|---|---|
| 1 | Dataset scope và label policy | Không | Bản nháp đã triển khai, chờ human review |
| 2 | Review/khóa taxonomy v2 | 1 | Bản nháp đã có |
| 3 | Hoàn thiện guideline | 1–2 | Bản nháp đã có |
| 4 | Pilot hai annotator | 3 | Batch 400 đã tạo |
| 5 | Đo agreement và adjudication | 4 | Chưa làm |
| 6 | Pipeline full annotation | 2–5 | Khung validation đã có |
| 7 | Full metadata annotation | 6 | Chưa làm |
| 8 | Hai LLM-as-judge + human audit | 2, 6 | Chưa làm |
| 9 | Repair/filter/regenerate | 7–8 | Chưa làm |
| 10 | Dedup/group/split | 9 | Chưa làm |
| 11 | Dataset Release v2 | 7–10 | Chưa làm |
| 12 | Thí nghiệm và luận văn | 11 | Chưa làm |

## 6. Việc không nên làm lúc này

- Không chạy lại toàn bộ benchmark.
- Không fine-tune thêm teacher/student.
- Không sinh thêm hàng nghìn mẫu bằng prompt cũ.
- Không sửa metadata cũ trực tiếp trong snapshot Phase 1.
- Không chọn target audience chỉ từ category.
- Không dùng một LLM judge duy nhất.
- Không thiết kế split dựa trên metric đã nhìn thấy.
- Không đưa prediction/checkpoint trở lại Git.

## 7. Sprint đề xuất

### Sprint 1 — Nền định nghĩa

- Viết dataset scope.
- Review taxonomy và data dictionary.
- Hoàn thiện guideline với ví dụ/ phản ví dụ.
- Khóa phiên bản pilot.

### Sprint 2 — Pilot annotation

- Hai annotator gán độc lập.
- Tính agreement.
- Adjudicate.
- Chỉnh schema/guideline lần cuối trước full annotation.

### Sprint 3 — Annotation pipeline

- Import/export annotation.
- Comparison và adjudication queue.
- Provenance.
- Validation và test.

### Sprint 4 — Full annotation và synthetic audit

- Gán metadata.
- Chạy hai judges.
- Human audit.
- Repair/filter/reject.

### Sprint 5 — Release

- Dedup và template family.
- Split.
- Dataset card và quality report.
- Đóng băng v2.

### Sprint 6 — Thực nghiệm

- Real-only/TSTR.
- Random vs metadata-matched augmentation.
- Ablation.
- Benchmark và error analysis.

### Sprint 7 — Luận văn

- Viết lại phương pháp.
- Cập nhật kết quả.
- Chuẩn hóa bảng/hình và limitations.

## 8. Việc bắt đầu ngay

Ba đầu việc tiếp theo, theo đúng thứ tự:

1. Human review và khóa `docs/dataset_scope.md`.
2. Review từng allowed value trong `configs/taxonomy.json`.
3. Chuẩn bị hai bản pilot độc lập cho hai annotator từ batch 400 hiện tại.

Không bắt đầu full annotation trước khi ba việc trên hoàn thành.

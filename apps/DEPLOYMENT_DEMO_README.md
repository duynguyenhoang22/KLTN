# ViSmish Deployment Demo

Demo app for the defense section on RQ4 and deployment trade-off.

## Run

```powershell
python -m streamlit run apps\deployment_demo.py --server.port 8507
```

Open:

```text
http://localhost:8507
```

## What The Demo Shows

- Manual SMS prediction with live TextCNN hard and TextCNN risk-aware KD.
- Locked test-set sample inspection with metadata and model predictions.
- Batch deployment benchmark on a test subset.
- Runtime indicators: model size, load time, latency, throughput, peak RAM.
- Quality indicators on labeled test subset: F1 Label 1, Recall Label 1, Precision Label 1, FP, FN.

## Model Behavior

- `TextCNN hard` and `TextCNN risk-aware KD` run live from local `.pt` checkpoints.
- `PhoBERT-base teacher`, `CafeBERT teacher`, and `ViCLSR teacher` are shown from precomputed test outputs in the test/batch tabs.
- `CafeBERT teacher` and `ViCLSR teacher` also have local model weights under `setup_results`, but loading them live can be slow because each checkpoint is large.
- Use the sidebar field `Teacher outputs to show` to choose which teacher rows appear in test/batch comparisons.
- Use `Optional live teacher for manual/batch` only if you want to load a large teacher model during the demo. For a stable defense demo, keeping live teacher skipped is recommended.

## Defense Script

Use this demo after the RQ4 slide:

> Phan demo nay minh hoa trade-off trien khai cua RQ4. TextCNN hard va TextCNN KD co kich thuoc va latency gan nhu tuong duong vi cung kien truc. Distillation khong lam mo hinh nho hon trong inference; no thay doi tin hieu huan luyen de cai thien chat luong du doan cua student. Vi vay, diem can quan sat la lieu TextCNN KD co giu duoc chi phi suy luan thap trong khi cai thien cac chi so nhu Recall/F1 cho lop smishing hay khong.

## Suggested Demo Flow

1. Open `Manual SMS`.
2. Paste a clear smishing message and run prediction.
3. Open `Test sample`, choose a difficult real test sample, and run prediction.
4. Open `Batch deployment benchmark`.
5. Run 100 rows first. Use `Only real-origin rows` if asked about real-data evaluation.
6. Point out that teacher rows can be compared by quality from precomputed outputs, while TextCNN rows are measured live for deployment cost.
7. Point out that TextCNN hard and TextCNN KD have similar size/latency, while quality metrics may differ.

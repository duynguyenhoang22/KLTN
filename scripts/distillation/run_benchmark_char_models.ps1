param(
    [string]$Python = "python",
    [int]$Epochs = 12
)

$ErrorActionPreference = "Stop"

& $Python scripts/distillation/train_benchmark_char_model.py --architecture bilstm --mode hard --epochs $Epochs
& $Python scripts/distillation/train_benchmark_char_model.py --architecture bilstm --mode distilled --epochs $Epochs
& $Python scripts/distillation/train_benchmark_char_model.py --architecture textcnn --mode hard --epochs $Epochs
& $Python scripts/distillation/train_benchmark_char_model.py --architecture textcnn --mode distilled --epochs $Epochs

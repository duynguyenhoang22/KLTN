param(
    [string]$Python = "python",
    [int]$Epochs = 3
)

$ErrorActionPreference = "Stop"

$models = @(
    "phobert-base",
    "phobert-large",
    "mbert",
    "visobert",
    "cafebert",
    "distilledbert",
    "xlm-roberta-base",
    "xlm-roberta-large",
    "viclsr"
)

foreach ($model in $models) {
    & $Python scripts/distillation/train_benchmark_plm.py --model-key $model --epochs $Epochs
}

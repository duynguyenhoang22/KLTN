"""Fine-tune ViCLSR and generate benchmark teacher outputs on Kaggle.

Upload this file together with `kaggle_train_cafebert_teacher.py`, because the
two entrypoints intentionally share one implementation and output schema.

Recommended Kaggle command:

    python kaggle_train_viclsr_teacher.py \
      --split-dir /kaggle/input/vismish-benchmark \
      --fp16
"""

from __future__ import annotations

from kaggle_train_cafebert_teacher import ModelDefaults, run_teacher_pipeline


VICLSR_DEFAULTS = ModelDefaults(
    model_name="huynhtin/ViCLSR",
    teacher_name="ViCLSR",
    output_name="viclsr_teacher",
    train_batch_size=8,
    eval_batch_size=16,
    gradient_accumulation_steps=2,
)


if __name__ == "__main__":
    run_teacher_pipeline(VICLSR_DEFAULTS)

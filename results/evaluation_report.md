# Evaluation Report

This report summarizes the recorded Spider dev evaluation outputs from the completed project notebooks. The metrics were not regenerated during the portfolio cleanup.

## Setup

| Item | Value |
| --- | --- |
| Base model | `Qwen/Qwen2.5-Coder-1.5B-Instruct` |
| Fine-tuned checkpoint | `qwen_spider_full_sft_v3/` |
| Fine-tuning data | `2,503` custom chat-format text-to-SQL examples |
| Training split | 90% train / 10% validation |
| Evaluation benchmark | Spider dev |
| Evaluation method | Official Spider evaluator, `--etype all` |

The fine-tuned checkpoint and Spider evaluator workspace are intentionally ignored by Git. The recorded output notebook is preserved as `results/report_ft_v3_spider_eval.ipynb`.

## Recorded Metrics

| Model | Execution accuracy | Exact match |
| --- | ---: | ---: |
| Base Qwen2.5-Coder | 34.4% | 27.9% |
| Fine-tuned v3 | 35.9% | 31.0% |

## Interpretation

The fine-tuned model improved exact match by about `+3.1` points and execution accuracy by about `+1.5` points on Spider dev. The improvement is modest, but the project demonstrates the important applied workflow: preparing a custom text-to-SQL dataset, prompt-masked supervised fine-tuning, deterministic inference, baseline comparison, and benchmark evaluation.

## Raw Artifacts

Raw SQL gold/prediction files are kept under `results/raw_spider_outputs/` so the top-level results folder stays readable:

- `dev_gold.sql`
- `dev_pred_base_model.sql`
- `dev_gold_head.sql`
- `dev_pred_head_base_model.sql`

The committed raw prediction file is the base-model prediction file. Fine-tuned v3 predictions were written to the ignored evaluator workspace during the completed run, while the notebook output preserves the resulting metrics.

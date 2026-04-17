# Text-to-SQL Fine-Tuning with Qwen2.5-Coder

Portfolio project demonstrating a complete text-to-SQL fine-tuning workflow: synthetic dataset generation with generative AI, supervised fine-tuning, inference, and Spider-style evaluation.

The trained checkpoint is intentionally not committed. This repository is meant to show the workflow, methodology, dataset format, and recorded evaluation results without shipping large model weights.

## Project Summary

This project explores an LLM-as-teacher setup: a larger generative AI system was used to create a synthetic text-to-SQL dataset, then `Qwen/Qwen2.5-Coder-1.5B-Instruct` was fine-tuned on that dataset and evaluated for transfer performance on the Spider dev benchmark.

| Area | Details |
| --- | --- |
| Task | Natural language to SQL generation |
| Base model | `Qwen/Qwen2.5-Coder-1.5B-Instruct` |
| Dataset | `2,503` synthetic examples generated with generative AI and stored in chat JSONL format |
| Experiment idea | Use a stronger generative model as a teacher to create fine-tuning data for a smaller open model |
| Training style | Supervised fine-tuning with prompt masking |
| Split used | 90% train / 10% validation |
| External evaluation | Spider dev, official evaluator output recorded in notebook |

The strongest training version is the prompt-masked SFT workflow archived from `ft3.ipynb`. Earlier notebooks are preserved under `experiments/` to show iteration history, but the clean project entry point is `text_to_sql_finetuning_workflow.ipynb`.

## Recorded Results

These metrics come from completed notebook runs already present in the project artifacts. Training and evaluation were not rerun during this cleanup.

| Model | Spider execution accuracy | Spider exact match |
| --- | ---: | ---: |
| Base Qwen2.5-Coder | 34.4% | 27.9% |
| Fine-tuned v3 | 35.9% | 31.0% |

The fine-tuned model improved exact match by about `+3.1` points and execution accuracy by about `+1.5` points on Spider dev. The result is modest but promising for a synthetic-data experiment because it shows that generative-AI-created training data can move a smaller open model in the right direction when paired with a proper fine-tuning and evaluation loop.

## Repository Layout

```text
.
├── README.md
├── main.py
├── requirements.txt
├── spider_style_dataset.jsonl
├── text_to_sql_finetuning_workflow.ipynb
├── results/
│   ├── README.md
│   ├── evaluation_report.md
│   ├── report_ft_v3_spider_eval.ipynb
│   └── raw_spider_outputs/
│       ├── dev_gold.sql
│       └── dev_pred_base_model.sql
└── experiments/
    ├── ft3_recorded_training_run.ipynb
    └── earlier prototype notebooks
```

## How to Inspect

Run the artifact sanity check:

```bash
python main.py
```

Expected checks:

- `2,503` dataset rows load as valid JSONL.
- Every row has `system`, `user`, and `assistant` chat messages.
- Every assistant answer starts with SQL-style `SELECT` or `WITH`.
- Raw Spider gold/prediction files under `results/raw_spider_outputs/` have matching line counts.

Install notebook dependencies only if you want to inspect or rerun parts of the workflow:

```bash
pip install -r requirements.txt
```

## Important Reproducibility Notes

The following artifacts are intentionally excluded from Git:

- Fine-tuned model checkpoints such as `qwen_spider_full_sft_v3/`.
- Downloaded Spider data and SQLite databases.
- The official Spider evaluator folder.
- NLTK cache files and other runtime caches.

To fully reproduce evaluation, a reviewer would need to download Spider, restore or rerun the fine-tuned checkpoint, and run the official evaluator. The committed `results/evaluation_report.md`, `results/report_ft_v3_spider_eval.ipynb`, and README preserve the recorded metrics and workflow decisions from the completed run.

One implementation note: the recorded v3 run used a validation split, but its `eval_steps=200` was larger than the `108` optimizer-step training run. For future reruns, the polished workflow notebook recommends epoch-level evaluation so validation loss is always recorded.

## CV Description

**Project name**

Synthetic Teacher-to-Student Text-to-SQL Fine-Tuning

**Short project description**

Fine-tuned `Qwen2.5-Coder-1.5B-Instruct` for text-to-SQL generation using a 2.5k-example synthetic dataset generated with generative AI, implemented prompt-masked supervised fine-tuning, and evaluated transfer performance with Spider-style exact match and execution accuracy.

**CV bullet**

- Built a synthetic-data text-to-SQL fine-tuning experiment by using generative AI to create a 2,503-example training set, fine-tuning `Qwen2.5-Coder-1.5B-Instruct` with prompt-masked SFT, and evaluating transfer performance on Spider dev.

## What This Demonstrates

- Preparing chat-format fine-tuning data for an instruction-tuned code model.
- Using generative AI as a teacher to bootstrap a domain-specific fine-tuning dataset.
- Correctly masking prompt tokens so the model learns the assistant SQL response.
- Running and documenting model inference after fine-tuning.
- Comparing a base model against a fine-tuned checkpoint.
- Presenting evaluation results honestly without committing large model artifacts.

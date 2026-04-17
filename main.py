"""Quick sanity check for the portfolio artifacts.

This script intentionally uses only the Python standard library. It does not
train a model, download checkpoints, or run the Spider evaluator. Its job is to
verify that the committed dataset/results have the shape described in the
README.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATASET_PATH = ROOT / "spider_style_dataset.jsonl"
RESULTS_DIR = ROOT / "results"
RAW_RESULTS_DIR = RESULTS_DIR / "raw_spider_outputs"

EXPECTED_DATASET_ROWS = 2503
RECORDED_METRICS = {
    "base": {"execution": 34.4, "exact_match": 27.9},
    "fine_tuned_v3": {"execution": 35.9, "exact_match": 31.0},
}


def count_lines(path: Path) -> int:
    with path.open("r", encoding="utf-8") as handle:
        return sum(1 for _ in handle)


def validate_dataset(path: Path) -> tuple[bool, int, int, int]:
    if not path.exists():
        print(f"Dataset missing: {path.name}")
        return False, 0, 0, 0

    total_rows = 0
    valid_message_rows = 0
    sql_answer_rows = 0

    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            total_rows += 1
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                print(f"Invalid JSON on line {line_number}: {exc}")
                continue

            messages = row.get("messages")
            if not isinstance(messages, list) or len(messages) != 3:
                continue

            roles = [message.get("role") for message in messages]
            if roles == ["system", "user", "assistant"]:
                valid_message_rows += 1

            answer = str(messages[-1].get("content", "")).strip().lower()
            if answer.startswith(("select", "with")):
                sql_answer_rows += 1

    ok = (
        total_rows == EXPECTED_DATASET_ROWS
        and valid_message_rows == total_rows
        and sql_answer_rows == total_rows
    )
    return ok, total_rows, valid_message_rows, sql_answer_rows


def validate_results(results_dir: Path) -> bool:
    gold = results_dir / "dev_gold.sql"
    pred = results_dir / "dev_pred_base_model.sql"
    gold_head = results_dir / "dev_gold_head.sql"
    pred_head = results_dir / "dev_pred_head_base_model.sql"

    checks = [(gold, pred, "full Spider dev"), (gold_head, pred_head, "20-row head sample")]
    all_ok = True

    for gold_path, pred_path, label in checks:
        if not gold_path.exists() or not pred_path.exists():
            print(f"Results check skipped for {label}: missing file(s).")
            all_ok = False
            continue

        gold_lines = count_lines(gold_path)
        pred_lines = count_lines(pred_path)
        status = "OK" if gold_lines == pred_lines else "MISMATCH"
        print(f"{label}: gold={gold_lines}, pred={pred_lines} [{status}]")
        all_ok = all_ok and gold_lines == pred_lines

    return all_ok


def print_recorded_metrics() -> None:
    print("\nRecorded Spider dev metrics from completed notebook runs:")
    print("model              execution   exact match")
    print("------------------------------------------")
    for name, metrics in RECORDED_METRICS.items():
        print(
            f"{name:<18} {metrics['execution']:>6.1f}%"
            f"      {metrics['exact_match']:>6.1f}%"
        )
    print("\nNote: fine-tuned model weights and Spider evaluator assets are intentionally ignored.")


def main() -> int:
    dataset_ok, total_rows, valid_rows, sql_rows = validate_dataset(DATASET_PATH)
    print("Dataset artifact:")
    print(f"rows={total_rows}, valid_chat_rows={valid_rows}, sql_answer_rows={sql_rows}")
    print(f"dataset_status={'OK' if dataset_ok else 'CHECK'}")

    print("\nCommitted result artifacts:")
    results_ok = validate_results(RAW_RESULTS_DIR)

    print_recorded_metrics()
    return 0 if dataset_ok and results_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

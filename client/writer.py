# client/writer.py
# 결과 저장: JSON + CSV)
from __future__ import annotations
import csv
import json
from pathlib import Path
from typing import Any, Dict

CSV_HEADER = ["source_file", "vendor", "date", "total_amount", "currency"]

def append_jsonl(path: str, row: Dict[str, Any]) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")

def append_csv(path: str, row: Dict[str, Any]) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)

    file_exists = p.exists()
    with open(p, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CSV_HEADER)
        if not file_exists:
            w.writeheader()

        out = {k: row.get(k) for k in CSV_HEADER}
        w.writerow(out)
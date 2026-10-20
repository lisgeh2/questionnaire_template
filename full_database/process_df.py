import pandas as pd
import json
import sys
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from process_meta import transform_to_meta

META = transform_to_meta()

DATA_FILE = Path(__file__).resolve().parent / "data" / "responses.jsonl"

REVERSE = {
    key: {label: code for code, label in entry["item_labels"].items()}
    for key, entry in META.items()
}

def load_rows(path=DATA_FILE):
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def to_code(key, value):
    if value is None or value == "":
        return pd.NA
    return REVERSE.get(key, {}).get(value, value)


def build_df(path=DATA_FILE):
    records = []
    for row in load_rows(path):
        answers = row["answers"]
        record = {"username": row["username"], "submitted_at": row["submitted_at"]}
        for key in META:
            record[key] = to_code(key, answers.get(key))
        records.append(record)

    df = pd.DataFrame(records, columns=["username", "submitted_at", *META])
    df["submitted_at"] = pd.to_datetime(df["submitted_at"])
    df["tz"] = 1          # <- add this: every answer 
    return df
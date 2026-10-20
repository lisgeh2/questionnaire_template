"""Where the answers go.

One JSON object per line (JSONL). It is append-only, so a crash can never
corrupt earlier submissions, and every line is readable on its own:

    pandas.read_json("data/responses.jsonl", lines=True)

If you later need many concurrent writers or queries, swap the two functions
below for SQLite (`sqlite3` is in the standard library) -- nothing else in the
app has to change.
"""

from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path

DATA_FILE = Path(__file__).parent / "full_database" / "data" / "responses.jsonl"


import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


def save_response(answers: dict, username: str = None) -> Path:
    """Append one submission and return the file it was written to."""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    submitted_at = datetime.now(timezone.utc).isoformat(timespec="seconds")

    # Build token from username + submitted_at + all answers
    if username is None:
        username = "anonymous"
        
    token_data = {"username": username, "submitted_at": submitted_at, "answers": answers}
    token_string = json.dumps(token_data, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    token = hashlib.sha256(token_string.encode("utf-8")).hexdigest()

    record = {
        "username": username,
        "submitted_at": submitted_at,
        "token": token,
        "answers": answers,
    }

    with DATA_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

    return DATA_FILE

def load_responses() -> list[dict]:
    """All submissions so far, oldest first."""
    if not DATA_FILE.exists():
        return []
    with DATA_FILE.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def export_csv(target: str | Path = "data/responses.csv") -> Path:
    """Flatten every submission into one wide CSV (handy for Excel)."""
    responses = load_responses()
    if not responses:
        raise ValueError("No responses to export yet.")

    rows = [
        {"username": r["username"], "submitted_at": r["submitted_at"], **r["answers"]}
        for r in responses
    ]
    # Lists (multiselect answers) do not fit in a CSV cell, so join them.
    for row in rows:
        for key, value in row.items():
            if isinstance(value, list):
                row[key] = "; ".join(map(str, value))

    columns = list(dict.fromkeys(key for row in rows for key in row))

    target = Path(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)

    return target


if __name__ == "__main__":
    print(f"Exported to {export_csv()}")

# Implement storage/repo.py for JSON file read/write

import json
import os
from typing import Any

def read_json(path: str) -> Any:
    """Read JSON file and return Python object. If file doesn't exist, return empty list."""
    if not os.path.exists(path):
        return []  # or {} depending on your use case
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def write_json(path: str, data: Any) -> None:
    """Write Python object as JSON file (pretty formatted)."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    


"""Collect only final token counters per session; never export session transcripts."""

import json
import sys
from pathlib import Path


def usage(sessions: Path) -> dict[str, int] | None:
    totals: dict[str, int] = {}
    for path in sessions.rglob("*.jsonl"):
        last = {}
        for line in path.read_text().splitlines():
            event = json.loads(line)
            payload = event.get("payload")
            if isinstance(payload, dict) and payload.get("type") == "token_count":
                info = payload.get("info") or {}
                last = info.get("total_token_usage") or last
        for key, value in last.items():
            if isinstance(value, int):
                totals[key] = totals.get(key, 0) + value
    return totals or None


if __name__ == "__main__":
    print(json.dumps(usage(Path(sys.argv[1]))))

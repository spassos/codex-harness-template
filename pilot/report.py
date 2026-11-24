"""Join blinded review notes, evaluator scores and run metrics after the review."""

import argparse
import csv
import json
import sys
from pathlib import Path


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text()) or {}


def report(artifacts: Path, review_file: Path) -> None:
    with review_file.open(newline="") as notes:
        reviews = {row["id"]: row for row in csv.DictReader(notes)}
    matrix = read_json(artifacts / "assignment/matrix.json")["include"]
    rows = []
    for assignment in matrix:
        run = assignment["id"]
        candidate = artifacts / f"review-{run}"
        metrics = read_json(candidate / "metrics.json")
        score = read_json(artifacts / f"score-{run}/score.json")
        tokens = read_json(candidate / "usage.json")
        review = reviews.get(run, {})
        rows.append(
            {
                **assignment,
                "bootstrap": metrics.get("bootstrap", "unavailable"),
                "agent": metrics.get("agent", "unavailable"),
                "acceptance": score.get("acceptance", "unrun"),
                "make_check": score.get("make_check", "unrun"),
                "seconds": metrics.get("seconds"),
                "input_tokens": tokens.get("input_tokens"),
                "output_tokens": tokens.get("output_tokens"),
                "interventions_given": metrics.get("interventions_given"),
                "interventions_requested": review.get("interventions_requested"),
                "regressions": review.get("regressions"),
                "out_of_scope": review.get("out_of_scope"),
                "notes": review.get("notes"),
            }
        )
    writer = csv.DictWriter(sys.stdout, rows[0].keys())
    writer.writeheader()
    writer.writerows(sorted(rows, key=lambda row: (row["task"], row["arm"], row["repeat"])))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifacts", type=Path)
    parser.add_argument("blind_review_csv", type=Path)
    args = parser.parse_args()
    report(args.artifacts, args.blind_review_csv)

"""Instructor demo: Python foundations as a small DE pipeline (script version).

This is the same logic as the demo notebook, moved into a .py file to show the
shape your homework takes. Run it from this folder:

    uv run python demo_pipeline.py
"""
import csv
import json
from pathlib import Path

DATA = Path("claims.csv")


# 1. INGEST: data engineering always starts by reading data
def load_claims(path):
    claims = []
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            row["reserve"] = float(row["reserve"])
            row["paid"] = float(row["paid"])
            claims.append(row)
    return claims


# 2. TRANSFORM: a function for the business metric
def loss_ratio(paid, reserve):
    if reserve == 0:
        return 0.0
    return round(paid / reserve * 100, 1)


def main():
    claims = load_claims(DATA)
    print(f"Ingested {len(claims)} claims")

    # 3. ANALYZE: aggregate by policy type with a dict
    summary = {}
    for c in claims:
        bucket = summary.setdefault(
            c["policy_type"], {"count": 0, "reserve": 0.0, "paid": 0.0}
        )
        bucket["count"] += 1
        bucket["reserve"] += c["reserve"]
        bucket["paid"] += c["paid"]

    print("\nLoss ratio by policy type:")
    for ptype in sorted(summary):
        b = summary[ptype]
        print(f"  {ptype}: {loss_ratio(b['paid'], b['reserve'])}%")

    # A comprehension: ids of the open claims
    open_ids = [c["claim_id"] for c in claims if c["status"] == "open"]
    print("\nOpen claims:", open_ids)

    # 4. OUTPUT: write a JSON report
    report = [
        {
            "policy_type": p,
            "count": summary[p]["count"],
            "loss_ratio": loss_ratio(summary[p]["paid"], summary[p]["reserve"]),
        }
        for p in sorted(summary)
    ]
    with open("loss_ratio_report.json", "w") as f:
        json.dump(report, f, indent=2)
    print("\nWrote loss_ratio_report.json")


if __name__ == "__main__":
    main()

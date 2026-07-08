"""Student Do: CSV read and write.

Read a clean claims CSV with csv.DictReader, aggregate by policy type, and write
a summary CSV with csv.DictWriter. The csv module is how you read and write
tabular files before pandas takes over on Day 4.
"""
import csv
from pathlib import Path

DATA = Path("Resources/claims.csv")
OUT = Path("policy_summary.csv")

# Read: DictReader gives each row as a dict keyed by the header
summary = {}
with open(DATA, newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        ptype = row["policy_type"]
        reserve = float(row["reserve"])
        paid = float(row["paid"])
        bucket = summary.setdefault(ptype, {"count": 0, "reserve": 0.0, "paid": 0.0})
        bucket["count"] += 1
        bucket["reserve"] += reserve
        bucket["paid"] += paid

print("Policy summary:")
for ptype in sorted(summary):
    b = summary[ptype]
    print(f"  {ptype}: {b['count']} claims, reserve ${b['reserve']:,.2f}, paid ${b['paid']:,.2f}")

# Write: DictWriter writes rows from dicts, with a header
with open(OUT, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["policy_type", "count", "total_reserve", "total_paid"])
    writer.writeheader()
    for ptype in sorted(summary):
        b = summary[ptype]
        writer.writerow({
            "policy_type": ptype,
            "count": b["count"],
            "total_reserve": round(b["reserve"], 2),
            "total_paid": round(b["paid"], 2),
        })

print(f"Wrote {OUT}")

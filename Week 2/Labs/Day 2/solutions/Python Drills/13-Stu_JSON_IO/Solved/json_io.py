"""Student Do: JSON read and write.

Load a nested claims JSON, total the payments per claim, and write a JSON summary.
JSON is the shape a REST API returns, so this is the direct bridge to the Day 3
API lab: read the response, walk the nested structure, write a flat result.
"""
import json
from pathlib import Path

DATA = Path("Resources/claims.json")
OUT = Path("claims_totals.json")

# Read: json.load turns the file into Python lists and dicts
with open(DATA) as f:
    claims = json.load(f)

totals = []
for claim in claims:
    total = sum(p["amount"] for p in claim["payments"])
    totals.append({"claim_id": claim["claim_id"], "total_paid": total})
    print(f"{claim['claim_id']}: ${total:,.2f}")

# Write: json.dump serializes Python objects back to JSON
with open(OUT, "w") as f:
    json.dump(totals, f, indent=2)

print(f"Wrote {OUT}")

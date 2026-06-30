"""Student Do: JSON read and write.

Load claims.json, total each claim's payments, and write a JSON summary.
Run from inside this drill folder.
"""
import json
from pathlib import Path

DATA = Path("Resources/claims.json")
OUT = Path("claims_totals.json")

# TODO: load DATA with json.load


# TODO: for each claim, sum the amount of every record in its payments list,
# print "<claim_id>: $<total>", and collect {"claim_id": ..., "total_paid": ...}
totals = []


# TODO: write totals to OUT with json.dump(..., indent=2)

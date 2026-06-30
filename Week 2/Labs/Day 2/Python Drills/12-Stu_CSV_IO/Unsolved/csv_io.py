"""Student Do: CSV read and write.

Read claims.csv with csv.DictReader, aggregate by policy type, and write a summary
CSV with csv.DictWriter. Run from inside this drill folder.
"""
import csv
from pathlib import Path

DATA = Path("Resources/claims.csv")
OUT = Path("policy_summary.csv")

# TODO: read DATA with csv.DictReader. For each row, convert reserve and paid to
# float and accumulate per policy_type totals (count, reserve, paid).
summary = {}


# TODO: print the summary sorted by policy type


# TODO: write OUT with csv.DictWriter, columns:
# policy_type, count, total_reserve, total_paid (with a header row)

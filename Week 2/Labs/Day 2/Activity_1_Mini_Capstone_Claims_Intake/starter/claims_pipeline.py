"""Mini-Capstone starter: Claims Intake Pipeline (Charter Oak Mutual).

You will build a small data pipeline over messy insurance claim records,
using only the Python standard library. Work tier by tier:
  Core      -> read, clean, and validate raw claim rows
  Challenge -> aggregate by policy type and compute loss ratio
  Stretch   -> roll up nested payment events and flag reserve breaches

Run from the activity folder (the folder that contains data/):
    uv run python starter/claims_pipeline.py
"""
import csv
import json
from pathlib import Path

DATA = Path("data")
OUT = Path("outputs")
RAW_CSV = DATA / "claims_raw.csv"
PAYMENTS_JSON = DATA / "claim_payments.json"


# ---------- helpers ----------
def parse_money(raw):
    """Convert a raw money string to a non-negative float, or None if invalid.

    Handle: surrounding spaces, a leading '$', thousands commas, empty string,
    'N/A', non-numeric text, and negative numbers (treat negatives as invalid).
    """
    # TODO (Core): clean the string, try to convert to float, return None on
    # failure or if the value is negative. Round valid values to 2 decimals.
    pass


def loss_ratio(total_paid, total_reserve):
    """Paid divided by reserve as a percentage, rounded to two places.

    Return 0.0 if total_reserve is 0 so you never divide by zero.
    """
    # TODO (Challenge): implement the loss ratio formula.
    pass


# ---------- CORE: clean + validate ----------
def load_clean_claims(path):
    """Return (clean_records, rejected_count).

    A row is rejected if it has no claim_id, an invalid reserve or paid value,
    or a claim_id that already appeared (duplicate). Each clean record is a dict
    with keys: claim_id, policy_type, status, state, reserve, paid.
    Normalize policy_type and status to lowercase, state to uppercase.
    """
    clean = []
    rejected = 0
    seen = set()
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # TODO (Core): pull claim_id, parse reserve and paid with
            # parse_money(), reject bad or duplicate rows, otherwise append a
            # normalized clean record and remember the claim_id in `seen`.
            pass
    return clean, rejected


# ---------- CHALLENGE: aggregate by policy type ----------
def summarize_by_policy(clean):
    """Return {policy_type: {"count", "reserve", "paid"}} summed over claims."""
    summary = {}
    # TODO (Challenge): loop the clean records and accumulate count, reserve,
    # and paid per policy_type. Hint: dict.setdefault is handy here.
    return summary


# ---------- STRETCH: nested payment rollup + SIU review ----------
def find_reserve_breaches(payments, reserve_by_id):
    """Return a list of breach dicts for claims whose summed payments exceed
    their reserve. Each dict: claim_id, reserve, total_paid, overage, payment_count.
    """
    siu_review = []
    # TODO (Stretch): for each claim_id in payments, sum the payment amounts,
    # compare to that claim's reserve, and append a breach record when the
    # total paid is greater than the reserve.
    return siu_review


def main():
    OUT.mkdir(exist_ok=True)

    # ---- CORE ----
    clean, rejected = load_clean_claims(RAW_CSV)
    print("=== CORE: Intake summary ===")
    print(f"Valid claims:    {len(clean)}")
    print(f"Rejected rows:   {rejected}")
    # TODO (Core): print total reserve and total paid across clean claims,
    # formatted with a thousands separator and 2 decimals.
    print()

    # ---- CHALLENGE ----
    # TODO (Challenge): build the summary, print a loss-ratio table, and write
    # outputs/policy_summary.csv with a header row.

    # ---- STRETCH ----
    # TODO (Stretch): load data/claim_payments.json, build reserve_by_id from
    # your clean claims, find reserve breaches, print them, and write
    # outputs/siu_review.json.


if __name__ == "__main__":
    main()

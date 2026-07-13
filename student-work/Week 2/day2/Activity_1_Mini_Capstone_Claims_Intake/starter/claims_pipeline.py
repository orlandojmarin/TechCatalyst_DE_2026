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

    # Strip surrounding whitespace
    cleaned = raw.strip()

    # Remove leading dollar sign
    cleaned = cleaned.replace("$", "")

    # Remove thousands commas
    cleaned = cleaned.replace(",", "")

    # Reject empty strings and N/A
    if cleaned == "" or cleaned == "N/A":
        return None

    # Attempt conversion to float
    try:
        value = float(cleaned)
    except ValueError:
        return None

    # Reject negative values
    if value < 0:
        return None

    # Round to two decimal places
    return round(value, 2)


def loss_ratio(total_paid, total_reserve):
    """Paid divided by reserve as a percentage, rounded to two places.

    Return 0.0 if total_reserve is 0 so you never divide by zero.
    """
    # TODO (Challenge): implement the loss ratio formula.

    if total_reserve == 0:
        return 0.0

    return round((total_paid / total_reserve) * 100, 2)


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

            # Extract and strip claim_id
            claim_id = row["claim_id"].strip()

            # Reject rows with no claim_id
            if not claim_id:
                rejected += 1
                continue

            # Parse money fields
            reserve = parse_money(row["reserve"])
            paid = parse_money(row["paid"])

            # Reject rows with invalid reserve or paid
            if reserve is None or paid is None:
                rejected += 1
                continue

            # Reject duplicate claim_ids
            if claim_id in seen:
                rejected += 1
                continue

            # Mark this claim_id as seen
            seen.add(claim_id)

            # Normalize text fields
            policy_type = row["policy_type"].strip().lower()
            status = row["status"].strip().lower()
            state = row["state"].strip().upper()

            # Default empty policy_type to "unknown"
            if policy_type == "":
                policy_type = "unknown"

            # Append the clean record
            clean.append({
                "claim_id": claim_id,
                "policy_type": policy_type,
                "status": status,
                "state": state,
                "reserve": reserve,
                "paid": paid,
            })
    return clean, rejected


# ---------- CHALLENGE: aggregate by policy type ----------
def summarize_by_policy(clean):
    """Return {policy_type: {"count", "reserve", "paid"}} summed over claims."""
    summary = {}
    # TODO (Challenge): loop the clean records and accumulate count, reserve,
    # and paid per policy_type. Hint: dict.setdefault is handy here.

    for claim in clean:
        pt = claim["policy_type"]

        # Create a new bucket if this policy type hasn't been seen yet
        summary.setdefault(pt, {"count": 0, "reserve": 0.0, "paid": 0.0})

        # Accumulate totals
        summary[pt]["count"] += 1
        summary[pt]["reserve"] += claim["reserve"]
        summary[pt]["paid"] += claim["paid"]

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

    for claim_id, events in payments.items():
        # Skip claims that aren't in our clean set
        if claim_id not in reserve_by_id:
            continue

        # Sum all payment amounts for this claim
        total_paid = sum(event["amount"] for event in events)
        reserve = reserve_by_id[claim_id]

        # Flag claims where payments exceed reserve
        if total_paid > reserve:
            overage = round(total_paid - reserve, 2)
            siu_review.append({
                "claim_id": claim_id,
                "reserve": reserve,
                "total_paid": total_paid,
                "overage": overage,
                "payment_count": len(events),
            })

    # Sort by claim_id for consistent output
    siu_review.sort(key=lambda x: x["claim_id"])
    return siu_review


def main():
    OUT.mkdir(exist_ok=True)

    # ---- CORE ----
    clean, rejected = load_clean_claims(RAW_CSV)

    # Compute totals across all clean claims
    total_reserve = sum(claim["reserve"] for claim in clean)
    total_paid = sum(claim["paid"] for claim in clean)

    print("=== CORE: Intake summary ===")
    print(f"Valid claims:    {len(clean)}")
    print(f"Rejected rows:   {rejected}")
    # TODO (Core): print total reserve and total paid across clean claims,
    # formatted with a thousands separator and 2 decimals.
    print(f"Total reserve:   ${total_reserve:,.2f}")
    print(f"Total paid:      ${total_paid:,.2f}")
    print()

    # ---- CHALLENGE ----
    # TODO (Challenge): build the summary, print a loss-ratio table, and write
    # outputs/policy_summary.csv with a header row.

    summary = summarize_by_policy(clean)

    print("=== CHALLENGE: Loss ratio by policy type ===")
    # Print header
    print(f"{'policy_type':<13}{'count':>5}{'reserve':>14}{'paid':>14}{'loss_ratio':>12}")

    # Print each policy type row sorted alphabetically
    for pt in sorted(summary.keys()):
        bucket = summary[pt]
        ratio = loss_ratio(bucket["paid"], bucket["reserve"])
        print(
            f"{pt:<13}"
            f"{bucket['count']:>5}"
            f"{bucket['reserve']:>14,.2f}"
            f"{bucket['paid']:>14,.2f}"
            f"{ratio:>11.2f}%"
        )

    # Write policy_summary.csv
    csv_path = OUT / "policy_summary.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["policy_type", "count", "total_reserve", "total_paid", "loss_ratio_pct"])
        for pt in sorted(summary.keys()):
            bucket = summary[pt]
            ratio = loss_ratio(bucket["paid"], bucket["reserve"])
            writer.writerow([pt, bucket["count"], bucket["reserve"], bucket["paid"], ratio])

    print(f"Wrote {csv_path}")
    print()

    # ---- STRETCH ----
    # TODO (Stretch): load data/claim_payments.json, build reserve_by_id from
    # your clean claims, find reserve breaches, print them, and write
    # outputs/siu_review.json.

    # Load nested payment events
    with open(PAYMENTS_JSON) as f:
        payments = json.load(f)

    # Build a lookup of reserve by claim_id from clean claims
    reserve_by_id = {claim["claim_id"]: claim["reserve"] for claim in clean}

    # Find claims where total payments exceed their reserve
    breaches = find_reserve_breaches(payments, reserve_by_id)

    print("=== STRETCH: SIU reserve-breach review ===")
    print(f"Claims breaching reserve: {len(breaches)}")
    for b in breaches:
        print(
            f"  {b['claim_id']}: paid ${b['total_paid']:,.2f} "
            f"vs reserve ${b['reserve']:,.2f} "
            f"(overage ${b['overage']:,.2f})"
        )

    # Write siu_review.json
    json_path = OUT / "siu_review.json"
    with open(json_path, "w") as f:
        json.dump(breaches, f, indent=2)

    print(f"Wrote {json_path}")


if __name__ == "__main__":
    main()

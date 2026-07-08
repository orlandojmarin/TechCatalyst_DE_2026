"""
Student Activity: Claim Payment Rollup.

This script uses nested dict and list objects to track the payment events
made on each claim. This is the exact shape a REST API returns, which is why
it is the bridge into Day 3.
"""

# Dictionary of list of records
# Key: claim id | Value: list of payment records
# Record: [date, kind, amount]
claim_payments = {
    "CLM-3001": [
        ["2026-06-01", "medical", 1200.00],
        ["2026-06-08", "rental", 300.00],
        ["2026-06-15", "medical", 800.00],
    ],
    "CLM-3002": [
        ["2026-06-02", "property", 2500.00],
        ["2026-06-12", "property", 1500.00],
    ],
    "CLM-3003": [
        ["2026-06-03", "medical", 600.00],
        ["2026-06-09", "rental", 400.00],
        ["2026-06-16", "medical", 250.00],
    ],
    "CLM-3004": [
        ["2026-06-05", "liability", 3000.00],
    ],
}

# Dictionary of dictionaries: one new payment event per claim
# Key: claim id | Value: dict with date, kind, amount
new_payments = {
    "CLM-3001": {"date": "2026-06-22", "kind": "medical", "amount": 450.00},
    "CLM-3002": {"date": "2026-06-22", "kind": "property", "amount": 1000.00},
    "CLM-3003": {"date": "2026-06-22", "kind": "medical", "amount": 150.00},
    "CLM-3004": {"date": "2026-06-22", "kind": "liability", "amount": 2000.00},
}

# Append each new payment event to the matching claim's list of records
for claim_id, event in new_payments.items():
    # Build the new record in [date, kind, amount] format
    record = [event["date"], event["kind"], event["amount"]]
    # Append it to that claim's list
    claim_payments[claim_id].append(record)

# Print the modified claim_payments dictionary
print(claim_payments)

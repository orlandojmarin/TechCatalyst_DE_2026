"""
Student Activity: Claim Payment Rollup (Challenge).

After appending the new payment events, roll up the total paid per claim.
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
new_payments = {
    "CLM-3001": {"date": "2026-06-22", "kind": "medical", "amount": 450.00},
    "CLM-3002": {"date": "2026-06-22", "kind": "property", "amount": 1000.00},
    "CLM-3003": {"date": "2026-06-22", "kind": "medical", "amount": 150.00},
    "CLM-3004": {"date": "2026-06-22", "kind": "liability", "amount": 2000.00},
}

# Append each new payment event to the matching claim's list (from the Core step)


# Initialize a results dictionary to hold the total paid per claim


# TODO: Loop through claim_payments. For each claim, sum the amount field
# (index 2) across all of its records, round to two decimals, and store it in
# results under the claim id.


# Print the rollup

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

# Append each new payment event to the matching claim's list of records
for claim_id, event in new_payments.items():
    record = [event["date"], event["kind"], event["amount"]]
    claim_payments[claim_id].append(record)

print(claim_payments)

# Initialize a results dictionary to hold the total paid per claim
results = {}

# Roll up the total paid for each claim
for claim_id, records in claim_payments.items():

    # The amount is the third field (index 2) of each record
    total_paid = sum(record[2] for record in records)

    # Round and store the total for this claim
    results[claim_id] = round(total_paid, 2)

# Print the rollup
print(results)

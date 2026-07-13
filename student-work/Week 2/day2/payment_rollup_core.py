"""
Student Activity: Claim Payment Rollup.

Use nested dict and list objects to track the payment events on each claim.
This is the exact shape a REST API returns, which is why it is the Day 3 bridge.
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

# TODO: Loop through new_payments. For each claim, build a [date, kind, amount]
# record and append it to that claim's list in claim_payments.
for key in new_payments:
    payment_list = []
    payment_dictionary = new_payments[key]
    for field in payment_dictionary:
        payment_list.append(payment_dictionary[field])
    # print(payment_list)
    print()
    claim_list = claim_payments[key]
    claim_list.append(payment_list)
    # print(claim_list)
    
# Print the modified claim_payments dictionary
print(claim_payments)
print()

# Challenge
# Roll up the total amount paid for each claim into a results dictionary
# Loop through every key-value pair in claim_payments
# For each claim, sum the amount field (index 2) across all of its records
# Round to two decimals and store it in results under the claim id

results = {}

for claim in claim_payments:
    total_amount = 0
    claim_info_list = claim_payments[claim]
    print(claim_info_list)
    for list in claim_info_list:
        total_amount += list[2]
    results[claim] = round(total_amount, 2)

print(results)

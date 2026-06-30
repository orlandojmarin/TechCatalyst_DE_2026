"""Student Do: Lambdas, map, and filter.

Use lambda, map, and filter on the claims list. Wrap map and filter in list(...)
to see the results.
"""

claims = [
    {"claim_id": "CLM-9001", "policy_type": "auto", "reserve": 5000, "paid": 1200, "status": "open"},
    {"claim_id": "CLM-9002", "policy_type": "property", "reserve": 12000, "paid": 11800, "status": "closed"},
    {"claim_id": "CLM-9003", "policy_type": "liability", "reserve": 20000, "paid": 4000, "status": "open"},
    {"claim_id": "CLM-9004", "policy_type": "auto", "reserve": 3000, "paid": 500, "status": "open"},
    {"claim_id": "CLM-9005", "policy_type": "property", "reserve": 15000, "paid": 16200, "status": "open"},
]

# TODO 1: sort by reserve descending with a lambda key, print the claim ids


# TODO 2: use map to get a list of claim ids


# TODO 3: use map to bump each reserve by 10 percent (round to 2 places)


# TODO 4: use filter to keep only open claims, print their ids


# TODO 5: combine filter and map to get the ids of claims where paid > reserve

"""Student Do: Lambdas, map, and filter.

A lambda is a tiny anonymous function. map applies a function to every item;
filter keeps the items that match a condition. You will see this exact pattern
again in Week 5 with PySpark, where map and filter are how you transform big data.
"""

claims = [
    {"claim_id": "CLM-9001", "policy_type": "auto", "reserve": 5000, "paid": 1200, "status": "open"},
    {"claim_id": "CLM-9002", "policy_type": "property", "reserve": 12000, "paid": 11800, "status": "closed"},
    {"claim_id": "CLM-9003", "policy_type": "liability", "reserve": 20000, "paid": 4000, "status": "open"},
    {"claim_id": "CLM-9004", "policy_type": "auto", "reserve": 3000, "paid": 500, "status": "open"},
    {"claim_id": "CLM-9005", "policy_type": "property", "reserve": 15000, "paid": 16200, "status": "open"},
]

# lambda as a sort key: sort claims by reserve, largest first
by_reserve = sorted(claims, key=lambda c: c["reserve"], reverse=True)
print("Sorted by reserve (desc):", [c["claim_id"] for c in by_reserve])

# map: project each claim to its id
ids = list(map(lambda c: c["claim_id"], claims))
print("Ids:", ids)

# map with a transform: bump each reserve by 10 percent
bumped = list(map(lambda c: round(c["reserve"] * 1.10, 2), claims))
print("Reserves +10%:", bumped)

# filter: keep only the open claims
open_claims = list(filter(lambda c: c["status"] == "open", claims))
print("Open claim ids:", [c["claim_id"] for c in open_claims])

# filter + map together: ids of claims where paid exceeds reserve
breaches = list(map(lambda c: c["claim_id"],
                    filter(lambda c: c["paid"] > c["reserve"], claims)))
print("Reserve breaches:", breaches)

# same result as step 4, written as a list comprehension instead of filter
open_ids_comprehension = [c["claim_id"] for c in claims if c["status"] == "open"]
print("Open claim ids (comprehension):", open_ids_comprehension)
assert open_ids_comprehension == [c["claim_id"] for c in open_claims]

# STRETCH: dict comprehension mapping claim_id to reserve, open claims only
open_reserves = {c["claim_id"]: c["reserve"] for c in claims if c["status"] == "open"}
print("Open claim reserves (dict comprehension):", open_reserves)

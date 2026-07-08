"""Student Do: collections (defaultdict and Counter).

These two tools make aggregation clean. Counter tallies occurrences; defaultdict
gives every new key a starting value so you skip the setdefault dance. This is the
group-and-count muscle that becomes groupby on Day 4.
"""
from collections import defaultdict, Counter

claims = [
    {"claim_id": "CLM-1", "policy_type": "auto", "paid": 1200.0},
    {"claim_id": "CLM-2", "policy_type": "property", "paid": 5000.0},
    {"claim_id": "CLM-3", "policy_type": "auto", "paid": 800.0},
    {"claim_id": "CLM-4", "policy_type": "liability", "paid": 4000.0},
    {"claim_id": "CLM-5", "policy_type": "property", "paid": 2200.0},
    {"claim_id": "CLM-6", "policy_type": "auto", "paid": 3100.0},
]

# Counter: count claims per policy type in one line
counts = Counter(c["policy_type"] for c in claims)
print("counts:", dict(counts))
print("most common:", counts.most_common(1))

# defaultdict(float): sum paid per policy type, no setdefault needed
paid_by_type = defaultdict(float)
for c in claims:
    paid_by_type[c["policy_type"]] += c["paid"]
print("paid by type:", dict(paid_by_type))

# defaultdict(list): group claim ids per policy type
ids_by_type = defaultdict(list)
for c in claims:
    ids_by_type[c["policy_type"]].append(c["claim_id"])
print("ids by type:", dict(ids_by_type))

# Challenge: average paid per policy type (combine the count and the sum)
print("average paid by type:")
for ptype in sorted(paid_by_type):
    avg = round(paid_by_type[ptype] / counts[ptype], 2)
    print(f"  {ptype}: {avg}")

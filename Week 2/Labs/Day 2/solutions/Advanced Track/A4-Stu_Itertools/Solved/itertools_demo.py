"""Advanced Track: itertools pipelines.

itertools builds memory-efficient iterator pipelines. Four you will actually use:
chain, islice, accumulate, and groupby.
"""
from itertools import chain, islice, accumulate, groupby

batch1 = [{"claim_id": "CLM-1", "paid": 1200.0}, {"claim_id": "CLM-2", "paid": 5000.0}]
batch2 = [{"claim_id": "CLM-3", "paid": 800.0}, {"claim_id": "CLM-4", "paid": 4000.0}]

# chain: treat several iterables as one stream
all_claims = list(chain(batch1, batch2))
print("chained:", [c["claim_id"] for c in all_claims])

# islice: take the first N without building the whole list first
print("first two:", [c["claim_id"] for c in islice(chain(batch1, batch2), 2)])

# accumulate: a running total
paids = [c["paid"] for c in all_claims]
print("running total:", list(accumulate(paids)))

# groupby: group CONSECUTIVE items by a key, so sort by that key first
claims = [
    {"claim_id": "CLM-1", "policy_type": "auto"},
    {"claim_id": "CLM-2", "policy_type": "property"},
    {"claim_id": "CLM-3", "policy_type": "auto"},
]
claims.sort(key=lambda c: c["policy_type"])
print("grouped:")
for ptype, group in groupby(claims, key=lambda c: c["policy_type"]):
    print(f"  {ptype}: {[c['claim_id'] for c in group]}")

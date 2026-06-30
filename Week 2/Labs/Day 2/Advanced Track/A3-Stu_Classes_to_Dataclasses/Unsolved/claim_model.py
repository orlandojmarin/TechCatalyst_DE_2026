"""Advanced Track: Classes to Dataclasses (with type hints).

Build the plain class first (Core), then the dataclass and a standalone function
(Challenge).
"""
from dataclasses import dataclass


# ---- Part 1 (Core): a plain class ----
class ClaimPlain:
    # TODO: write __init__(self, claim_id, policy_type, reserve, paid) that stores
    # each argument on self.

    # TODO: write reserve_burn(self) that returns round(self.paid / self.reserve * 100, 1)

    # TODO: write __repr__(self) so printing the object is readable
    pass


# ---- Part 2 (Challenge): the same thing as a dataclass, with type hints ----
# TODO: turn this into a dataclass with typed fields claim_id, policy_type,
# reserve, and paid (default 0.0), plus a reserve_burn(self) -> float method.
class Claim:
    pass


# ---- A standalone function (Challenge) ----
# TODO: write reserve_burn_fn(claim) that returns the same value as the method.
def reserve_burn_fn(claim):
    pass


# ---- Demo (leave this as is once your classes are written) ----
c1 = ClaimPlain("CLM-5001", "auto", 5000.0, 1200.0)
print("plain class:", c1)
print("plain burn:", c1.reserve_burn())

c2 = Claim("CLM-5001", "auto", 5000.0, 1200.0)
print("dataclass:", c2)
print("dataclass burn:", c2.reserve_burn())

c3 = Claim("CLM-5001", "auto", 5000.0, 1200.0)
print("c2 == c3:", c2 == c3)

c4 = Claim("CLM-5002", "property", 12000.0)
print("with default:", c4)
print("default burn:", c4.reserve_burn())

print("via method:", c2.reserve_burn())
print("via function:", reserve_burn_fn(c2))

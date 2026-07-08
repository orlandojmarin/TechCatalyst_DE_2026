"""Advanced Track: Classes to Dataclasses (with type hints).

A class lets you model a real thing (a claim) as an object with its own data and
behavior. A dataclass is a modern shortcut that writes the boilerplate for you.
We build the plain class first, then the dataclass, so you can see what changed.
"""
from dataclasses import dataclass


# ---- Part 1: a plain class ----
# You write __init__ to store the fields, and __repr__ so printing is readable.
class ClaimPlain:
    def __init__(self, claim_id, policy_type, reserve, paid):
        self.claim_id = claim_id
        self.policy_type = policy_type
        self.reserve = reserve
        self.paid = paid

    def reserve_burn(self):
        """A method: it uses self, the claim it is called on."""
        return round(self.paid / self.reserve * 100, 1)

    def __repr__(self):
        return (f"ClaimPlain({self.claim_id!r}, {self.policy_type!r}, "
                f"{self.reserve}, {self.paid})")


# ---- Part 2: the same thing as a dataclass, with type hints ----
# @dataclass writes __init__, __repr__, and __eq__ for you from the typed fields.
@dataclass
class Claim:
    claim_id: str
    policy_type: str
    reserve: float
    paid: float = 0.0  # typed field with a default

    def reserve_burn(self) -> float:
        return round(self.paid / self.reserve * 100, 1)


# ---- A standalone function does the same work as the method ----
# Called as reserve_burn_fn(claim), not claim.reserve_burn().
def reserve_burn_fn(claim) -> float:
    return round(claim.paid / claim.reserve * 100, 1)


# ---- Demo ----
c1 = ClaimPlain("CLM-5001", "auto", 5000.0, 1200.0)
print("plain class:", c1)
print("plain burn:", c1.reserve_burn())

c2 = Claim("CLM-5001", "auto", 5000.0, 1200.0)
print("dataclass:", c2)
print("dataclass burn:", c2.reserve_burn())

# A dataclass also gets __eq__ for free, comparing field by field
c3 = Claim("CLM-5001", "auto", 5000.0, 1200.0)
print("c2 == c3:", c2 == c3)

# The default field means paid is optional
c4 = Claim("CLM-5002", "property", 12000.0)
print("with default:", c4)
print("default burn:", c4.reserve_burn())

# Method versus function: same result, different call style
print("via method:", c2.reserve_burn())
print("via function:", reserve_burn_fn(c2))

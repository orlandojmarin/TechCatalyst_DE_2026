"""Student Do: Claims as Classes.

A class lets you model a real thing (a claim) as an object that holds its own
data and the behavior that goes with it. This drill introduces classes and the
critical judgment call: when to use a class versus a plain function.
"""


class Claim:
    def __init__(self, claim_id, policy_type, reserve, paid):
        # __init__ runs when you create a Claim. self is this specific claim.
        self.claim_id = claim_id
        self.policy_type = policy_type
        self.reserve = reserve
        self.paid = paid

    def reserve_burn(self):
        """Percent of the reserve that has been paid out."""
        return round(self.paid / self.reserve * 100, 1)

    def is_over_reserve(self):
        """True once payments exceed the reserve."""
        return self.paid > self.reserve

    def add_payment(self, amount):
        """A new payment posts to this claim. The object's state changes."""
        self.paid += amount

    def summary(self):
        flag = " OVER RESERVE" if self.is_over_reserve() else ""
        return f"{self.claim_id} ({self.policy_type}): burn {self.reserve_burn()}%{flag}"


# Create some claim objects
claims = [
    Claim("CLM-6001", "auto", 5000.0, 1200.0),
    Claim("CLM-6002", "property", 12000.0, 13500.0),
    Claim("CLM-6003", "liability", 20000.0, 4000.0),
]

print("Initial claims:")
for c in claims:
    print(" ", c.summary())

# A new payment posts to the first claim. Because the claim is an object, it
# carries its updated state with it.
claims[0].add_payment(4200.0)
print("\nAfter a $4,200 payment on CLM-6001:")
print(" ", claims[0].summary())

# Count how many claims are now over their reserve
over = sum(1 for c in claims if c.is_over_reserve())
print(f"\nClaims over reserve: {over}")

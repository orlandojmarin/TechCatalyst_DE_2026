"""Student Do: Claims as Classes.

Model a claim as a class that holds its own data and behavior. Then decide where a
class is the right tool versus a plain function.
"""


class Claim:
    # TODO: write __init__(self, claim_id, policy_type, reserve, paid) and store
    # each value on self.

    # TODO: reserve_burn(self) -> round(self.paid / self.reserve * 100, 1)

    # TODO: is_over_reserve(self) -> self.paid > self.reserve

    # TODO (Challenge): add_payment(self, amount) -> increase self.paid

    # TODO: summary(self) -> a readable one-line string, with an OVER RESERVE flag
    pass


# Create three claims:
#   CLM-6001 auto      reserve 5000.0  paid 1200.0
#   CLM-6002 property  reserve 12000.0 paid 13500.0
#   CLM-6003 liability reserve 20000.0 paid 4000.0
claims = []

print("Initial claims:")
# TODO: print each claim's summary

# TODO (Challenge): post a 4200.0 payment to CLM-6001, print its new summary,
# then count and print how many claims are over their reserve

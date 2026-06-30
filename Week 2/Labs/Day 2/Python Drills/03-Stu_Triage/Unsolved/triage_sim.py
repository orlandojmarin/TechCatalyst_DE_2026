# Triage Faceoff: assess an incoming claim's severity against the system's reading
import random

print("=== Charter Oak Mutual: Triage Faceoff ===")

# The three severity levels, from least to most severe
levels = ["low", "medium", "high"]
rank = {"low": 1, "medium": 2, "high": 3}

# The system assigns the claim's true severity at random
actual = random.choice(levels)

# The adjuster assesses the severity
your_call = input("Assess this claim: (low), (medium), or (high)? ").strip().lower()

# TODO: Compare your_call to actual using the rank lookup.
# Handle four cases in this order:
#   1. your_call is not a valid severity
#   2. your_call matches actual (correct triage)
#   3. your_call ranks lower than actual (under-triage)
#   4. otherwise your_call ranks higher than actual (over-triage)

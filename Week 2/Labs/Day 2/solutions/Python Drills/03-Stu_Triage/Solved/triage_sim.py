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

# Compare the adjuster's call to the system's reading
if your_call not in rank:
    print("Not a valid severity. Next time choose low, medium, or high.")
elif your_call == actual:
    print(f"You assessed {your_call}. The system read {actual}.")
    print("Correct triage. Route it to the standard queue.")
elif rank[your_call] < rank[actual]:
    print(f"You assessed {your_call}. The system read {actual}.")
    print("Under-triaged. This claim is riskier than you flagged. Escalate it.")
else:
    print(f"You assessed {your_call}. The system read {actual}.")
    print("Over-triaged. You escalated more than needed. That ties up a senior adjuster.")

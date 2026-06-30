# Triage Faceoff: assess an incoming claim's severity against the system's reading
import random

count = 0
correct_answers = 0

print("=== Charter Oak Mutual: Triage Faceoff ===")

# The three severity levels, from least to most severe
levels = ["low", "medium", "high"]
rank = {"low": 1, "medium": 2, "high": 3}

while count < 5:
    # The system assigns the claim's true severity at random
    actual = random.choice(levels)
    # for test purposes
    # print(f"Actual: {actual}")

    # The adjuster assesses the severity
    your_call = input("Assess this claim: (low), (medium), or (high)? ").strip().lower()
    print(f"Your call: {your_call}")

    # TODO: Compare your_call to actual using the rank lookup.
    # Handle four cases in this order:
    #   1. your_call is not a valid severity
    #   2. your_call matches actual (correct triage)
    #   3. your_call ranks lower than actual (under-triage)
    #   4. otherwise your_call ranks higher than actual (over-triage)
    while your_call not in levels:
        print("Your call is not a valid severity. Try again.")
        your_call = input("Assess this claim: (low), (medium), or (high)? ").strip().lower()

    if your_call == actual:
        print("Your call matches the actual (correct triage)")
        correct_answers += 1
    else:
        if rank[your_call] < rank[actual]:
            print("Your call ranks lower than actual (under-triage)")
        else:
            print("Your call ranks higher than actual (over-triage)")

    count += 1

print(f"You got {correct_answers} claims triaged correctly!")
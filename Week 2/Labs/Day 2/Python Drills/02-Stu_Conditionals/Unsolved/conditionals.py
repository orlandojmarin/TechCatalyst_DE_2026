# 1.
claim_amount = 5000
if 2 * claim_amount > 10000:
    print("Escalate to senior adjuster")
else:
    print("Handle in standard queue")

# 2.
policy = "AUTO"
if len(policy) < 5:
    print("Short policy code accepted")
else:
    print("Policy code too long")

# 3.
claim_age_days = 21
if claim_age_days > 20:
    print("Claim is overdue for review")
else:
    print("Claim is still within the review window")

# 4.
severity = 2
flags = 5
if (severity ** 3 >= flags) and (flags ** 2 < 26):
    print("Route to SIU")
else:
    print("Standard handling")

# 5.
payout = 18000
authority_level = 1
manager_override = True

if (payout < 2000) and (authority_level >= 1):
    print("Adjuster can approve directly")
elif (payout < 10000) and (authority_level >= 2):
    print("Needs a senior adjuster")
elif (payout < 25000) and (authority_level >= 3):
    print("Needs a claims manager")
elif ((payout < 50000) and (authority_level >= 3)) or (manager_override and (payout < 50000)):
    print("Approved via manager override")
else:
    print("Escalate to claims committee")

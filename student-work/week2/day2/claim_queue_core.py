"""Student Do: Claim Queue.

Manage a queue of claim ids through the day using list operations.
"""

# Create the day's claim queue (CLM-1001 through CLM-1007)
claim_queue = ["CLM-1001", "CLM-1002", "CLM-1003", "CLM-1004", "CLM-1005", "CLM-1006", "CLM-1007"]

# Find the first two claims in the queue
print(claim_queue[0:2])
print()

# Find every claim except the first two
print(claim_queue[2:])
print()

# Find every other claim, starting from the second claim
print(claim_queue[1::2])

# A new claim arrives. Append CLM-1008 to the queue
claim_queue.append("CLM-1008")
print(claim_queue)
print()

# CLM-1004 was reopened. Change it to CLM-1004-REOPEN by index
claim_queue[3] = "CLM-1004-REOPEN"
print(claim_queue)
print()

# Count how many claims are in the queue
claim_count = len(claim_queue)
print(f"There are {claim_count} claims in the queue")
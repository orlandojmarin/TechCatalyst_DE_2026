"""Student Do: Claim Queue.

This script showcases basic list operations to help an adjuster manage a
queue of claim ids through the day.
"""

# Create the day's claim queue
print("Today's claim queue:")
queue = ["CLM-1001", "CLM-1002", "CLM-1003", "CLM-1004", "CLM-1005", "CLM-1006", "CLM-1007"]
print(queue)
print()

# Find the first two claims in the queue
print("What are the first two claims in the queue?")
print(queue[:2])
print()

# Find every claim except the first two
print("What are all the claims except the first two?")
print(queue[2:])
print()

# Find every other claim, starting from the second claim
print("What is every other claim, starting from the second?")
print(queue[1::2])
print()

# A new claim arrives. Append it to the end of the queue
print("A new claim just arrived...")
queue.append("CLM-1008")
print(queue)
print()

# A claim is reopened. Change it by index
print("CLM-1004 was reopened...")
queue[3] = "CLM-1004-REOPEN"
print(queue)
print()

# Count how many claims are in the queue
print("How many claims are in the queue?")
print(len(queue))
print()

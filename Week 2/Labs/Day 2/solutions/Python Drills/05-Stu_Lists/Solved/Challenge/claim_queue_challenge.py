"""Student Do: Claim Queue (Challenge).

Continues the Core script: the adjuster works the queue and updates it.
"""

# Create the day's claim queue
print("Today's claim queue:")
queue = ["CLM-1001", "CLM-1002", "CLM-1003", "CLM-1004", "CLM-1005", "CLM-1006", "CLM-1007"]
print(queue)
print()

# A new claim arrives. Append it to the end of the queue
queue.append("CLM-1008")

# A claim is reopened. Change it by index
queue[3] = "CLM-1004-REOPEN"
print("Queue after the new claim and the reopen:")
print(queue)
print()

# -------------------- Work the queue --------------------

# Find the index of the reopened claim
print("Where is 'CLM-1004-REOPEN' in the queue?")
print(queue.index("CLM-1004-REOPEN"))
print()

# Remove a claim by value (it closed)
print("CLM-1006 just closed...")
queue.remove("CLM-1006")
print(queue)
print()

# Remove a claim by index (it was transferred)
print("CLM-1001 was transferred to another adjuster...")
transferred_index = queue.index("CLM-1001")
queue.pop(transferred_index)
print(queue)
print()

# Remove the last claim in the queue
print("Picking up the last claim in the queue...")
queue.pop(-1)
print(queue)
print()

print("Queue worked down for the day.")

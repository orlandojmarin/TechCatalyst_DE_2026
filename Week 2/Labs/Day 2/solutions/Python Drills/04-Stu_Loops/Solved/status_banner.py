# Claim pipeline banner: announce a batch of claims moving through a stage

# Create a variable named stage
stage = "INTAKE"

# Loop through each letter of the stage name and print a banner line
for letter in stage:
    print(f"Give me a {letter}!")
    print(f"{letter}!")

# Print what the stage spells
print()
print("What does that spell?!")
print(f"{stage}! Claims are moving through {stage}.")
print()

# Use a range to show the batch of claims processed
print("Processing today's batch:")
for n in range(1, 6):
    print(f"  Claim {n} of 5 processed")

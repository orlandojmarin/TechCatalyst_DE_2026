# Claim pipeline banner: announce a batch of claims moving through a stage

# Create a variable named stage and give it a pipeline stage (for example "INTAKE")
stage = "INTAKE"

# Loop through each letter of the stage name and print a banner line for each
for letter in stage:
    print(f"Give me a {letter}!")
    print(f"{letter}!")


# Print what the stage spells
print()
print("What does that spell?!")
print(f"{stage}! Claims are moving through {stage}.")
print()

# Use a second for loop over range(1, 6) to print one line per claim in the batch
print("Processing today's batch:")
for claim_number in range(1,6):
    print(f" Claim {claim_number} of 5 processed")
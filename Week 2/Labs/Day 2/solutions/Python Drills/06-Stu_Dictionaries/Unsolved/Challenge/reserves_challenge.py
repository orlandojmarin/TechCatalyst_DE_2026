"""Student Activity: Claim Reserves (Challenge).

Iterate the reserves dictionary to compute book-level metrics and group
claims into reserve tiers.
"""

# Initialize the reserves dictionary and apply the Core updates
# (set CLM-2003 to 16000, add CLM-2016 at 9000, delete CLM-2013)


# Initialize metric variables: total_reserve, claim_count


# Track the largest and smallest reserve and the claim id that holds each


# Initialize one list per reserve tier: severe, major, moderate, minor
# severe >= 20000, major >= 5000, moderate >= 1000, minor < 1000


# Iterate over the key-value pairs of the dictionary. For each claim:
#   - add to the running total and count
#   - update the largest and smallest reserve
#   - append the claim id to the correct tier list


# Compute the average reserve


# Print the metrics and the four tier lists

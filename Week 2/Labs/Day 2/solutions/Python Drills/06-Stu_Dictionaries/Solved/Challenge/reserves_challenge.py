"""Student Activity: Claim Reserves (Challenge).

Iterate the reserves dictionary to compute book-level metrics and group
claims into reserve tiers.
"""

# Initialize a dictionary of claim ids and reserves (in dollars)
reserves = {
    "CLM-2001": 32000,
    "CLM-2002": 28000,
    "CLM-2003": 17000,
    "CLM-2004": 12500,
    "CLM-2005": 8700,
    "CLM-2006": 7200,
    "CLM-2007": 5300,
    "CLM-2008": 4800,
    "CLM-2009": 3100,
    "CLM-2010": 1200,
    "CLM-2011": 950,
    "CLM-2012": 400,
    "CLM-2013": 14500,
    "CLM-2014": 600,
    "CLM-2015": 22000,
}

# Apply the same updates as the Core step
reserves["CLM-2003"] = 16000
reserves["CLM-2016"] = 9000
del reserves["CLM-2013"]

# Initialize metric variables
total_reserve = 0
claim_count = 0

# Track the largest and smallest reserve and the claim that holds it
maximum_key = ""
maximum_value = None
minimum_key = ""
minimum_value = None

# Reserve tiers:
#   severe:   reserve >= 20000
#   major:    reserve >= 5000 and < 20000
#   moderate: reserve >= 1000 and < 5000
#   minor:    reserve < 1000
severe = []
major = []
moderate = []
minor = []

# Iterate over the key-value pairs of the dictionary
print()
for claim_id, reserve in reserves.items():
    print(f"Claim: {claim_id} | Reserve: ${reserve:,}")

    # Running total and count
    total_reserve += reserve
    claim_count += 1

    # Largest reserve
    if maximum_value is None or reserve > maximum_value:
        maximum_value = reserve
        maximum_key = claim_id

    # Smallest reserve
    if minimum_value is None or reserve < minimum_value:
        minimum_value = reserve
        minimum_key = claim_id

    # Group by reserve tier
    if reserve >= 20000:
        severe.append(claim_id)
    elif reserve >= 5000:
        major.append(claim_id)
    elif reserve >= 1000:
        moderate.append(claim_id)
    else:
        minor.append(claim_id)
print()

# Average reserve across the book
average_reserve = round(total_reserve / claim_count, 2)

# Print the metrics
print(f"Total Reserve: ${total_reserve:,}")
print(f"Total Number of Claims: {claim_count}")
print(f"Average Reserve: ${average_reserve:,.2f}")
print(f"Largest Reserve: {maximum_key} (${maximum_value:,})")
print(f"Smallest Reserve: {minimum_key} (${minimum_value:,})")
print("------------------------------------------------")
print(f"Severe claims: {severe}")
print(f"Major claims: {major}")
print(f"Moderate claims: {moderate}")
print(f"Minor claims: {minor}")
print()

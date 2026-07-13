"""Student Activity: Claim Reserves.

Use a Python dict to map claim ids to their reserve amount (in dollars),
then update, add, and remove entries.
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
    "CLM-2015": 22000
}

severe_claims = []
major_claims = []
moderate_claims = []
minor_claims = []

# A re-estimate lowered the reserve on CLM-2003 to 16000. Update it.
reserves["CLM-2003"] = 16000

# A new claim CLM-2016 arrived with a reserve of 9000. Add it.
reserves["CLM-2016"] = 9000

# CLM-2013 was withdrawn. Remove it from the dictionary.
del reserves["CLM-2013"]

# Print the modified dictionary
print(reserves)
print()

# Iterate over the key-value pairs in reserves and calculate:
# total reserve
# total number of claims
# average reserve
# largest reserve (and the claim that holds it)
# smallest reserve (and the claim that holds it)
total_reserve = 0
total_num_claims = 0
largest_reserve_claim = "CLM-2001"
smallest_reserve_claim = "CLM-2001"

for claim in reserves:
    total_num_claims += 1
    total_reserve += reserves[claim]

    # track the largest and smallest claims by key
    if reserves[claim] > reserves[largest_reserve_claim]:
        largest_reserve_claim = claim
    if reserves[claim] < reserves[smallest_reserve_claim]:
        smallest_reserve_claim = claim

    # Use an if-elif chain and lists to group claims by reserve tier
    if reserves[claim] >= 20000:
        severe_claims.append(claim)
    elif reserves[claim] >= 5000:
        major_claims.append(claim)
    elif reserves[claim] >= 1000:
        moderate_claims.append(claim)
    else:
        minor_claims.append(claim)
    
# calculate the average reserve
average_reserve = total_reserve / total_num_claims

# print the output
print(f"Total Reserve: ${total_reserve:,.2f}")
print(f"Total Number of Claims: {total_num_claims}")
print(f"Average Reserve: ${average_reserve:,.2f}")
print(f"Largest Reserve: {largest_reserve_claim:} (${reserves[largest_reserve_claim]:,})")
print(f"Smallest Reserve: {smallest_reserve_claim:} (${reserves[smallest_reserve_claim]:,})")
print("-" * 50)
print(f"Severe claims: {severe_claims}")
print(f"Major claims: {major_claims}")
print(f"Moderate claims: {moderate_claims}")
print(f"Minor claims: {minor_claims}")



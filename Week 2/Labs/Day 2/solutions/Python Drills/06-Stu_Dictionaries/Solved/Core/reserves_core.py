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
    "CLM-2015": 22000,
}

# A re-estimate lowered the reserve on CLM-2003
reserves["CLM-2003"] = 16000

# A new claim arrived with its own reserve
reserves["CLM-2016"] = 9000

# CLM-2013 was withdrawn, so remove it from the book
del reserves["CLM-2013"]

# Print the modified dictionary
print(reserves)

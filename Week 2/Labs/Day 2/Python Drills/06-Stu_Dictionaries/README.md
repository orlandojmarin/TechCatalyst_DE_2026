# Claim Reserves by Tier

In this activity, you will create a dictionary, update it, remove from it, and
then iterate over it to compute metrics and group claims into reserve tiers.

## Background

A reserve is the money set aside to pay a claim. The claims team keeps a
dictionary that maps each claim id to its reserve so they can answer questions
like: how much money is tied up in open claims, which claim is the largest
exposure, and how many claims fall into each severity tier. You will build and
work that dictionary.

## Instructions

Copy `Unsolved/Core/reserves_core.py` to your project and complete the following:

- Initialize the `reserves` dictionary with these claim id and reserve pairs (in
  dollars):

  - CLM-2001: 32000
  - CLM-2002: 28000
  - CLM-2003: 17000
  - CLM-2004: 12500
  - CLM-2005: 8700
  - CLM-2006: 7200
  - CLM-2007: 5300
  - CLM-2008: 4800
  - CLM-2009: 3100
  - CLM-2010: 1200
  - CLM-2011: 950
  - CLM-2012: 400
  - CLM-2013: 14500
  - CLM-2014: 600
  - CLM-2015: 22000

- A re-estimate lowered the reserve on `CLM-2003` to `16000`. Update it.

- A new claim `CLM-2016` arrived with a reserve of `9000`. Add it.

- `CLM-2013` was withdrawn. Delete it from the dictionary.

## Challenge

Group claims by their reserve tier and report book-level metrics.

- Iterate over the key-value pairs in `reserves` and calculate:

  - Total reserve
  - Total number of claims
  - Average reserve
  - Largest reserve (and the claim that holds it)
  - Smallest reserve (and the claim that holds it)

- Use an if-elif chain and lists to group claims by reserve tier:

  - `severe`: reserve greater than or equal to \$20,000
  - `major`: reserve greater than or equal to \$5,000 and less than \$20,000
  - `moderate`: reserve greater than or equal to \$1,000 and less than \$5,000
  - `minor`: reserve less than \$1,000

## Hint

Your Challenge results should look like the following:

```text
Total Reserve: $151,750
Total Number of Claims: 15
Average Reserve: $10,116.67
Largest Reserve: CLM-2001 ($32,000)
Smallest Reserve: CLM-2012 ($400)
------------------------------------------------
Severe claims: ['CLM-2001', 'CLM-2002', 'CLM-2015']
Major claims: ['CLM-2003', 'CLM-2004', 'CLM-2005', 'CLM-2006', 'CLM-2007', 'CLM-2016']
Moderate claims: ['CLM-2008', 'CLM-2009', 'CLM-2010']
Minor claims: ['CLM-2011', 'CLM-2012', 'CLM-2014']
```

## Stretch: sets

A set holds unique values and does fast membership and set math. Add this:

```python
types = {"auto", "property", "auto", "liability"}   # duplicates collapse
print(sorted(types), "auto" in types)

ct_states = {"CT", "MA", "RI"}
ne_states = {"MA", "NH", "VT"}
print("in both:", sorted(ct_states & ne_states))    # intersection
print("either:", sorted(ct_states | ne_states))     # union
```

Expected: `['auto', 'liability', 'property'] True`, then `in both: ['MA']`, then
`either: ['CT', 'MA', 'NH', 'RI', 'VT']`. Use a set whenever you need distinct
values or fast "is this in the collection?" checks.

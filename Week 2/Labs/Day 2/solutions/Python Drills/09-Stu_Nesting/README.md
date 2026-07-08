# Claim Payment Rollup

In this activity, you will work with nested data structures by storing payment
records in a list, storing those lists in a dictionary keyed by claim id, and then
rolling up the total paid per claim.

**Priority:** finish this drill first in the afternoon block. The shape you build
here, a dictionary of lists of records, is exactly what a REST API returns to you
on Day 3.

## Background

Every claim accumulates payment events over its life: a medical payment, a rental
payment, a property payment. The claims system stores those events as a list per
claim, and all the claims together in one dictionary keyed by claim id. A new
batch of payments just came in as a separate feed. You will append the new
payments to the right claims, then total what has been paid on each claim.

## Instructions

Using `Unsolved/Core/payment_rollup_core.py`, complete the following:

* Use the `new_payments` dictionary to add each new payment event to the matching
  claim's list in `claim_payments`. Each appended record should be in the format
  `[date, kind, amount]`.

  * Loop through `new_payments`, build the `[date, kind, amount]` record from each
    event dictionary, and append it to the correct claim's list.

* Print the modified `claim_payments` dictionary.

## Challenge

Roll up the total amount paid for each claim into a `results` dictionary.

* Loop through every key-value pair in `claim_payments`.

* For each claim, sum the `amount` field (index `2`) across all of its records.

* Round to two decimals and store it in `results` under the claim id.

## Hint

Your `results` should look like the following:

```text
{'CLM-3001': 2750.0, 'CLM-3002': 5000.0, 'CLM-3003': 1400.0, 'CLM-3004': 5000.0}
```

To sum one field across a list of records, use a generator:
`sum(record[2] for record in records)`.

## Bridge to Day 3 and the Mini-Capstone

This nested shape (dict keyed by id, holding lists of records) is the same shape
as the `claim_payments.json` file in the mini-capstone, and the same shape a REST
API returns on Day 3. Once you can walk this structure by hand, reading an API
response tomorrow is the same skill.

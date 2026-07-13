# Flattening Nested Policyholder Data

On Day 3 you pulled JSON from a REST API with `requests`. Real APIs rarely return a flat table. They return nested objects: a policyholder record that contains a list of that policyholder's claims. `pd.json_normalize` is the tool that turns that nested structure into a flat DataFrame you can actually work with.

## Instructions

Using the [starter file](Unsolved/policyholder_normalize.ipynb) and `Resources/policyholders.json`, complete the following steps:

1. Load `policyholders.json` with Python's built-in `json` module (`json.load`), and print the first record. Note that each policyholder has a nested `"claims"` list, and some policyholders have an empty list.

2. Use `pd.json_normalize(data)` directly on the raw list, with no other arguments. Look at what happens to the `claims` column: it is not flattened, it is a column of Python lists.

3. Now use `pd.json_normalize` with `record_path="claims"` and `meta=["policyholder_id", "name", "state"]`. This flattens each nested claim into its own row, while keeping the policyholder's `policyholder_id`, `name`, and `state` attached to every claim row.

4. Confirm that policyholders with an empty `claims` list do not appear at all in the result from step 3. Explain in a markdown cell why that happens, and what a data engineer would need to do differently if the business needs a row for every policyholder, including the ones with zero claims.

5. Using the flattened DataFrame from step 3, group by `policyholder_id` and calculate the total claim `amount` per policyholder.

## Challenge

Merge the totals from step 5 back onto the full policyholder list from step 1 (a DataFrame from `pd.json_normalize(data)` with `record_path` omitted, keeping only `policyholder_id`, `name`, and `state`), using a **left join** so that policyholders with zero claims show up with a total of `0` instead of disappearing. This is the difference between an inner and a left join you saw in Day 2, applied to real nested API data.

## Hint

* `record_path` tells `json_normalize` which nested list to explode into rows. `meta` tells it which top-level fields to carry along onto every exploded row.
* Consult the [json_normalize documentation](https://pandas.pydata.org/docs/reference/api/pandas.json_normalize.html) if you get stuck.

## References

Synthetic nested policyholder and claims dataset created for this activity, shaped like a typical REST API response.

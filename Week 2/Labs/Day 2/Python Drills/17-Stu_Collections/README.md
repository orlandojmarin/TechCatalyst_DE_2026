# collections: defaultdict and Counter

**Label: Core.** `collections` gives you cleaner tools for the thing you do
constantly in data engineering: group and count. `Counter` tallies occurrences;
`defaultdict` gives every new key a starting value so you skip the `setdefault`
dance. This is the muscle that becomes `groupby` on Day 4.

## Before and after

```python
# Before: setdefault to sum per group
paid_by_type = {}
for c in claims:
    bucket = paid_by_type.setdefault(c["policy_type"], 0.0)
    paid_by_type[c["policy_type"]] = bucket + c["paid"]

# After: defaultdict gives a 0.0 automatically
from collections import defaultdict
paid_by_type = defaultdict(float)
for c in claims:
    paid_by_type[c["policy_type"]] += c["paid"]
```

## Instructions

Copy `Unsolved/collections_demo.py` into your `student-work/week2/day2` project.

### Core

1. Use `Counter` to count claims per `policy_type` in one line. Print the counts
   and `most_common(1)`.
2. Use `defaultdict(float)` to sum `paid` per policy type.
3. Use `defaultdict(list)` to group claim ids per policy type.

### Challenge

4. Combine the count and the sum to print the **average** paid per policy type.

## Expected Output

```text
counts: {'auto': 3, 'property': 2, 'liability': 1}
most common: [('auto', 3)]
paid by type: {'auto': 5100.0, 'property': 7200.0, 'liability': 4000.0}
ids by type: {'auto': ['CLM-1', 'CLM-3', 'CLM-6'], 'property': ['CLM-2', 'CLM-5'], 'liability': ['CLM-4']}
average paid by type:
  auto: 1700.0
  liability: 4000.0
  property: 3600.0
```

## Success Criteria

- `Counter` replaces a manual counting loop.
- `defaultdict(float)` and `defaultdict(list)` replace `setdefault`.
- You can explain what the argument to `defaultdict(...)` does (it is the factory
  for a missing key's starting value).

## Hint

<details>
<summary>What does `defaultdict(list)` do on a missing key?</summary>

The first time you touch a new key, `defaultdict` calls the factory (`list`) to
create an empty list, so `ids_by_type[key].append(x)` just works without a
"key not found" check.

</details>

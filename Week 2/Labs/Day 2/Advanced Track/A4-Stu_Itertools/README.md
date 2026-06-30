# Advanced Track A4: itertools pipelines

**Optional, for fast finishers. Targets Python 3.13.**

`itertools` builds memory-efficient iterator pipelines. You will not use all of it,
but a handful show up constantly in data work: `chain`, `islice`, `accumulate`, and
`groupby`.

## Instructions

Copy `Unsolved/itertools_demo.py` into your project. Two batches of claims are
provided.

### Core

1. `chain`: combine `batch1` and `batch2` into one stream; print the claim ids.
2. `islice`: take the first two from the chained stream without building the whole
   list.
3. `accumulate`: print the running total of `paid`.

### Challenge

4. `groupby`: group the claims by `policy_type`. Remember `groupby` only groups
   **consecutive** equal keys, so sort by the key first.

## Expected Output

```text
chained: ['CLM-1', 'CLM-2', 'CLM-3', 'CLM-4']
first two: ['CLM-1', 'CLM-2']
running total: [1200.0, 6200.0, 7000.0, 11000.0]
grouped:
  auto: ['CLM-1', 'CLM-3']
  property: ['CLM-2']
```

## Success Criteria

- You use each of `chain`, `islice`, `accumulate`, and `groupby` once.
- You sorted before `groupby` and can explain why it is required.

## Hint

<details>
<summary>Why did groupby miss a group?</summary>

`groupby` starts a new group every time the key changes between adjacent items. If
the data is not sorted by that key, the same key appears in several non-adjacent
runs and you get duplicate or split groups. Sort first.

</details>

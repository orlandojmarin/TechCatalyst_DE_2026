# Lambdas, map, and filter

**Label: Core.** A lambda is a one-line anonymous function. `map` applies a
function to every item; `filter` keeps the items that match a condition. You will
meet this exact pattern again in Week 5 with PySpark, where `map` and `filter` are
how you transform large datasets.

## The three tools

```python
# lambda: a function with no name, written inline
add_tax = lambda x: x * 1.10

# map: apply a function to every item, returns an iterator
list(map(lambda c: c["reserve"], claims))

# filter: keep items where the function returns True
list(filter(lambda c: c["status"] == "open", claims))
```

## Instructions

Copy `Unsolved/lambdas_map_filter.py` into your `student-work/week2/day2` project.
The `claims` list is provided.

### Core

1. Sort the claims by `reserve`, largest first, using `sorted(..., key=lambda c:
   c["reserve"], reverse=True)`. Print the sorted claim ids.
2. Use `map` to project each claim to its `claim_id`. Print the list.
3. Use `map` to bump each `reserve` by 10 percent (`round(c["reserve"] * 1.10,
   2)`). Print the list.
4. Use `filter` to keep only the open claims. Print their ids.
5. Combine `filter` and `map` to get the ids of claims where `paid` exceeds
   `reserve`.

### Stretch

6. Rewrite step 4 as a list comprehension (see Advanced Track A1). Comprehensions
   are usually more readable in Python; `map`/`filter` matter because they are the
   model PySpark uses.

## Expected Output

```text
Sorted by reserve (desc): ['CLM-9003', 'CLM-9005', 'CLM-9002', 'CLM-9001', 'CLM-9004']
Ids: ['CLM-9001', 'CLM-9002', 'CLM-9003', 'CLM-9004', 'CLM-9005']
Reserves +10%: [5500.0, 13200.0, 22000.0, 3300.0, 16500.0]
Open claim ids: ['CLM-9001', 'CLM-9003', 'CLM-9004', 'CLM-9005']
Reserve breaches: ['CLM-9005']
```

## Success Criteria

- You use `lambda` as a sort key, and `map` and `filter` each at least once.
- You wrap `map` and `filter` in `list(...)` to see the results (they return lazy
  iterators).
- You can explain when a comprehension would read better than `map`/`filter`.

## Hint

<details>
<summary>Why does `map` print as a weird object without `list()`?</summary>

`map` and `filter` return lazy iterators, not lists. They produce values only when
you consume them. Wrap them in `list(...)` to materialize the results. PySpark
works the same lazy way, which is part of why this pattern matters.

</details>

## The third one: `reduce`

`map` and `filter` are built-ins, but `reduce` was moved to `functools` in Python 3,
a signal that it is not core day-to-day Python. It applies a function cumulatively
to fold a sequence into one value.

```python
from functools import reduce

paids = [1200, 5000, 800, 4000]
total = reduce(lambda acc, x: acc + x, paids, 0)
print("reduce total:", total)   # 11000, the same as sum(paids)
```

Know what `reduce` does because you will see it in real codebases and functional
pipelines, but in everyday Python a comprehension or a built-in like `sum()` is
clearer. Understand it; you will rarely write it.

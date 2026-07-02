# Day 2 Advanced Track (optional)

For fast finishers. Do the core drills and the mini-capstone first. These drills
add modern Python you will use constantly as a data engineer. They target the
Python 3.13 environment used in class.

Same workflow as the drills: copy the `Unsolved` file into your
`student-work/week2/day2` project and write the logic yourself. Do not copy from
`solutions/`.

## Drills

| Drill | Feature | What you practice |
|---|---|---|
| `A1-Stu_Comprehensions/` | list/dict/set comprehensions | Build collections in one line, with filters and transforms |
| `A2-Stu_Pattern_Matching/` | `match`/`case` (3.10) | Route and destructure records by shape, with guards and OR patterns |
| `A3-Stu_Classes_to_Dataclasses/` | classes, `@dataclass`, type hints | Model a claim as an object, then let a dataclass write the boilerplate |
| `A4-Stu_Itertools/` | `itertools` (chain, islice, accumulate, groupby) | Build memory-efficient iterator pipelines |
| `A5-Stu_Decorator/` | decorators, `functools.wraps`, `*args`/`**kwargs` | Wrap a function with a `@timer` to add behavior without changing it |

## Stretch tiers on the core drills

Two more modern features are added as stretch tiers on the core drills, so look
for the "Stretch (modern Python)" section in:

- `Python Drills/07-Stu_Iterate_Lists/` for the **walrus operator** (`:=`) and a
  **generator**.
- `Python Drills/09-Stu_Nesting/` for a **generator** that yields large claims.

## Why these matter

- Comprehensions and generators are everywhere in real pipeline code.
- `match`/`case` is the clean way to handle the many shapes an API response can
  take, which is exactly what you do tomorrow on Day 3.
- Dataclasses and type hints are how modern teams model records instead of passing
  bare dicts around.

## What comes later (not today)

Decorators, full object-oriented design, generators in depth, and exception groups
(`except*`) are introduced later where they fit naturally. Exception groups, for
example, belong with Day 3's concurrent API calls.

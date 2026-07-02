# Reading: DataFrame Engines for Bigger Data (Pandas, Polars, Modin, FireDucks)

> **Version-sensitive content.** Polars, Modin, and FireDucks move fast. Official
> docs and package pages were checked on 2026-06-30. Recheck install commands,
> compatibility claims, and benchmark numbers before teaching a later cohort.

## Why this matters

pandas is the standard, and for most day-to-day data it is the right tool. But it
has two well-known limits:

- **Single-threaded.** Core pandas uses one CPU core, so it leaves most of your
  machine idle on big jobs.
- **Memory-bound.** Your data has to fit in RAM, with headroom for copies.

When you hit those limits, you have two strategies, and the difference between them
is the whole point of this reading:

1. **Keep the pandas API, swap the engine.** Tools like **Modin** and **FireDucks**
   are near drop-in: you change one import and your existing pandas code runs
   faster. Best for upgrading legacy code with minimal rewrite.
2. **Adopt a faster, modern API.** **Polars** is a new DataFrame library (not
   pandas) that is multi-threaded and built for speed. You rewrite, but you get the
   best performance and a cleaner, expression-based API. This is the direction the
   ecosystem is moving, and the one we lean into.

## The landscape

| Engine | API | How you adopt it | Parallel? | Strength |
|---|---|---|---|---|
| **pandas** | the standard | already know it | single core | huge ecosystem, everything integrates with it |
| **Polars** | new (its own) | rewrite in Polars | multi-threaded, lazy + eager | speed, low memory, modern API; growing fast |
| **Modin** | pandas (drop-in) | `import modin.pandas as pd` | multi-core / cluster (Ray, Dask) | scale existing pandas code with minimal change |
| **FireDucks** | pandas (drop-in) | `import fireducks.pandas as pd` | multi-threaded, lazy/compiled | big speedups on existing pandas code; Linux |

### pandas: the baseline
The default. Unmatched ecosystem (every library speaks pandas). Eager, single-core,
in-memory. For small to medium data, it is simple and fast enough. Do not reach for
anything heavier until you actually need to.

### Polars: the strategic choice
A Rust-based DataFrame library with its own API. It is multi-threaded by default and
has a **lazy** mode that optimizes a whole query before running it. The API is
expression-based:

```python
import polars as pl

(
    pl.scan_csv("weather.csv")          # lazy: nothing runs yet
      .filter(pl.col("tmax").is_not_null())
      .group_by("station")
      .agg(pl.col("tmax").mean().alias("avg_tmax"))
      .collect()                        # now it runs, optimized
)
```

It is not a drop-in for pandas (the API differs), but it is fast, memory-efficient,
and increasingly popular. **This is the engine we focus on going forward.**

### Modin: scale pandas with one import
Modin aims to be a drop-in pandas replacement that parallelizes across all your
cores (and even a cluster) using a backend like Ray or Dask:

```python
# Before
import pandas as pd
# After (the rest of your code is unchanged)
import modin.pandas as pd
```

The promise: take **existing** pandas code and make it use the whole machine with
essentially no rewrite. Coverage of the pandas API is high but not total, so test
your specific operations.

### FireDucks: a compiled, accelerated pandas
FireDucks (from NEC) is also a near drop-in pandas accelerator:

```python
import fireducks.pandas as pd
```

Under the hood it uses lazy execution and a compiler to speed up pandas workloads,
often dramatically, while aiming for high pandas compatibility. It targets Linux
(x86), which fits the classroom Linux environment. It is newer than Modin and
Polars, so treat performance and compatibility claims as version-specific and
verify on your data.

## How to choose

| Situation | Reach for |
|---|---|
| Small or medium data, broad ecosystem needs | **pandas** |
| New code, want speed and a modern API, willing to learn it | **Polars** |
| A pile of **existing** pandas code that is too slow, minimal rewrite budget | **Modin** or **FireDucks** (swap the import, test) |
| Truly distributed / cluster-scale, terabytes | **Spark** (Week 5), not a single-machine DataFrame |

Rules of thumb:

- Do not optimize data you do not have. Most jobs are fine in pandas.
- "Minimal rewrite" wins (Modin/FireDucks) are perfect for legacy code you cannot
  afford to rewrite, but always test, because drop-in is never quite 100%.
- For new pipelines where performance matters, learning Polars pays off.
- When data outgrows one machine, that is a distributed-compute problem (Spark),
  not a faster-DataFrame problem.

## In today's mini-project

You clean the silver layer in **both pandas and Polars** so you feel the API
difference firsthand on the same task. As a stretch, swap the pandas import for
`modin.pandas` or `fireducks.pandas` and see your existing pandas clean run on a
different engine without changing the logic. That is the "upgrade legacy code with
one line" idea, made real.

## Sources to verify before teaching

- Polars: <https://docs.pola.rs/>
- Modin: <https://modin.readthedocs.io/>
- FireDucks: <https://fireducks-dev.github.io/>
- pandas 3.0 release notes: <https://pandas.pydata.org/docs/whatsnew/v3.0.0.html>

Use `course-content-research` (with network access) to confirm current install
commands, supported platforms, and any performance or compatibility numbers.

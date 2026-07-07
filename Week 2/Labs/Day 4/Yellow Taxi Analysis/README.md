# Yellow Taxi Analysis (carryover to Week 3 Day 1)

Your first realistically sized dataset: one month of NYC Yellow Taxi trips, about 3.5 million rows. Guided pandas transformations with expected outputs shown, ending in a partitioned parquet write that quietly exposes a real data quality problem.

**AI-Free Zone:** write the code yourself.

## Lab Index

### Provided Files

| File | Purpose |
|---|---|
| `README.md` | This file. |
| `Yellow Taxi Analysis - Student.ipynb` | The guided activity. Copy it into `student-work/week3/day1/` and work on the copy. |
| `solutions/Yellow_Taxi_Analysis_Solutions.ipynb` | Instructor reference, including both challenge solutions. Do not copy from it. |
| `data (downloaded)` | `yellow_tripdata_2024-04.parquet` from the [NYC TLC Trip Record Data page](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page), about 55 MB. Checked 2026-07-06. |

### Deliverables

| # | Deliverable | Evidence |
|---|---|---|
| 1 | Completed notebook copy in `student-work/week3/day1/` | All cells run with the repo-root `.venv` kernel. |
| 2 | Partitioned parquet output | `outputs/Yellow_Taxi_Transformed/` with year and month partition folders. |
| 3 | Challenge 1 answer | The strange partitions named, the offending rows captured, and one sentence on what happened. |
| 4 | Challenge 2 (stretch) | A per-month transform function, not copied cells. |

## Setup

Environment: the shared repo-root `.venv`. Nothing new to install; pandas and pyarrow are already there.

From the repo root:

```bash
cp "Week 2/Labs/Day 4/Yellow Taxi Analysis/Yellow Taxi Analysis - Student.ipynb" student-work/week3/day1/
cd student-work/week3/day1
mkdir -p data
curl -L -o data/yellow_tripdata_2024-04.parquet "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-04.parquet"
```

Keep the download out of Git: `data/` and `*.parquet` are already covered by the gitignore rules.

## Success Criteria

- The notebook runs top to bottom on your copy with the repo-root kernel.
- Your derived columns match the expected outputs embedded in the notebook.
- The parquet output is partitioned by `Trip_Year` and `Trip_Month`.
- You found the strange partitions and can explain what created them.

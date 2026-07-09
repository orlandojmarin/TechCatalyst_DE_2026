# Mini-Project: Medallion ETL (raw to bronze to silver)

This mini-capstone runs on **Week 3 Day 3**, after Python and pandas review.
Build a small, real pipeline that lands raw data untouched (**bronze**) and
refines it into a clean, typed table (**silver**). The full plan and rubric are
in the Day 3 `README.md` (`Week 3/Labs/Day 3/README.md`); this file is the
how-to for the code.

**Graded work runs in `--local` mode only.** The optional cloud path (public S3
read, GCS write) uses Application Default Credentials
(`gcloud auth application-default login`), never a downloaded key file. There
are no key files in this folder by design.

## Definition of Done

By the end of the required part, you should have:

1. A bronze CSV copied byte-for-byte into a dated folder.
2. A pandas silver DataFrame with 14 rows.
3. A silver parquet file written and read back successfully.
4. A short evidence note explaining what worked.

Optional after that:

- Try the same silver logic in Polars.
- Attempt S3 to GCS.
- Convert the notebook into a script after instructor approval.

Local pipeline success is required. Cloud success is optional. A serious cloud
attempt plus a clear blocker note is acceptable evidence.

## Files

| Path | What it is |
|---|---|
| `Medallion_ETL_Mini_Project.ipynb` | **Start here.** The guided notebook: concept examples, small TODO cells, policy explanations, expected row counts, optional Polars stretch, guarded cloud cells. |
| `starter/medallion_etl.py` | The bonus script path: after instructor approval, move your notebook code into this scaffold (`argparse`, functions, `--local`, optional `--polars`) and run it from the terminal. |
| `data/raw/weather_raw.csv` | Local raw data (20 messy rows) for offline mode. |
| `solutions/Medallion_ETL_Mini_Project_Solutions.ipynb` | Instructor reference for the notebook. Open at the debrief. |
| `solutions/medallion_etl_solution.py` | Instructor reference for the script conversion. |

## Setup

Complete `Activity_0_UV_GCS_Setup.md` first. It is the source of truth for
environment setup, file copying, ADC login, bucket checks, and troubleshooting.
The commands below are a quick reminder only.

On Week 3 Day 3, work under `student-work/week3/day3/`. Do not edit the
provided files in place. Use the repo-root `.venv` for the
notebook kernel and terminal commands.

From the repo root:

```bash
uv add "pandas>=3.0" polars pyarrow boto3 google-cloud-storage
gcloud auth application-default login
gcloud config set project YOUR_PROJECT_ID
```

This single install command prepares both the required local path and the
optional extensions. For the required local pandas path, the important packages
are pandas and pyarrow. The cloud packages are only needed for the optional
GCS/S3 extension, and Polars is only needed for the optional comparison section.
Complete the pandas local pipeline first.

The `.venv` lives at the repo root. Select the repo-root `.venv/bin/python` in
VS Code, and select the same `.venv` as the Jupyter kernel before opening the
notebook. If you see `VIRTUAL_ENV does not match the project environment`, run
`deactivate`, then retry with `uv run`.

Then copy `Medallion_ETL_Mini_Project.ipynb`, `starter/medallion_etl.py`, and
`data/` from this folder into `student-work/week3/day3/` and work on the copies.
Never copy from `solutions/`.

## Build Order

1. **Tier 1, required core journey.** Copy `Medallion_ETL_Mini_Project.ipynb`
   into `student-work/week3/day3/` and work through the local pandas path:
   concept helpers, extract, bronze with a byte-identical proof, profiling,
   silver one policy at a time, parquet write, and parquet read-back. Expected
   checkpoint: **pandas silver = 14 rows**.
2. **Tier 2, optional reinforcement.** Try the same silver logic in Polars only
   after the pandas path is complete.
3. **Tier 3, real-world extension.** Attempt public S3 to GCS. Success is useful,
   but a clear blocker note is acceptable if auth or permissions block you.
4. **Bonus after instructor approval.** Move your working notebook code into your
   copy of `starter/medallion_etl.py` and run it like a pipeline, from your work
   folder:

```bash
uv run python medallion_etl.py --local   # reads/writes local files
uv run python medallion_etl.py           # S3 to GCS, once local works
uv run python medallion_etl.py --local --polars  # optional stretch
```

The script must print the same row counts the notebook produced.

5. **Architecture last.** Draw a lightweight current-state architecture after you
   have local evidence and any cloud evidence or blocker note. A Mermaid diagram,
   draw.io sketch, slide, screenshot, or hand-drawn picture is enough.

## Implementation Checkpoints

1. **Extract.** Required local path: `read_raw_local()` reads bytes from
   `data/raw/weather_raw.csv`. Optional cloud path: implement
   `read_raw_from_s3()` with `boto3` unsigned. The source is public, so no AWS
   keys are needed.
2. **Bronze.** If you attempt cloud, implement `write_bronze_gcs()` to upload
   the raw bytes unchanged to
   `bronze/<dataset>/ingest_date=YYYY-MM-DD/...`. Never edit bronze.
3. **Silver (pandas).** Implement `to_silver()`: normalize names, coerce types,
   strip date text before parsing, drop no-date rows, dedupe on `(station, date)`,
   fix `prcp` (null/negative to 0), drop rows missing `tmax`/`tmin`, add
   `temp_range` and `is_rainy`. Write parquet locally. Upload to
   `silver/<dataset>/...` only if you attempt cloud.
4. **Silver (Polars), optional stretch.** Implement `to_silver_polars()`: the
   same clean in Polars. Its row count should match your pandas result.

## Expected Local Result

With the provided `weather_raw.csv` and the cleaning above:

```text
silver rows: 14
```

pandas silver is 14 rows (6 dropped: missing date, duplicates, bad or missing
temperatures). The optional Polars stretch should also give 14 if attempted.

## Intermediate Checkpoints

| Step | Expected evidence |
|---|---|
| After reading raw CSV | Shape is `(20, 5)` |
| After date parsing | `1` failed date |
| After dropping missing dates | `19` rows |
| After dropping duplicates | `17` rows |
| After dropping missing temperatures | `14` rows |
| Final silver | `14` rows, with MA1BOS 5, RI1PVD 3, US1NY 6 |

## Success Criteria

- `--local` runs end to end and pandas silver = 14 rows.
- Bronze is proven byte-for-byte identical to the source with `assert`.
- The silver parquet is read back and verified with `assert`.
- Your README or PR description includes a short evidence note.
- If attempted, the cloud run lands an immutable bronze object and a typed silver
  parquet in your GCS bucket, or your PR includes a clear blocker note.
- Your README or PR description includes a lightweight current-state architecture
  diagram.
- For the advanced script path, functions have docstrings, there is a `__main__`
  guard, and there are no secrets anywhere (ADC for GCP, anonymous read for S3).

## Hints

<details>
<summary>Read the source from S3 without AWS keys</summary>

```python
import boto3
from botocore import UNSIGNED
from botocore.config import Config
s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))
raw = s3.get_object(Bucket=SOURCE_BUCKET, Key=SOURCE_KEY)["Body"].read()
```
</details>

<details>
<summary>Upload to GCS with ADC (no key file)</summary>

```python
from google.cloud import storage
client = storage.Client(project=GCP_PROJECT)
client.bucket(GCS_BUCKET).blob(blob_path).upload_from_filename(local_parquet)
```

After `gcloud auth application-default login`, this uses your project
credentials.
</details>

<details>
<summary>pandas and Polars give different row counts</summary>

Check the order of operations and the dedupe key. Both should drop no-date rows,
dedupe on `(station, date)`, and require non-null `tmax`/`tmin`. Polars is a
different API, but the cleaning decisions must be the same.
</details>

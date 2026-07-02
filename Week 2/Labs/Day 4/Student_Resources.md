# Week 2 Day 4 Student Resources: pandas, Polars, and GCS

**AI-Free Zone:** write the pipeline yourself. You may read documentation, inspect examples, and ask the instructor for help, but do not use AI assistants to write or complete the code.

Today's active dataset is a small NOAA-style daily weather extract with messy station, date, temperature, and precipitation values. The local fallback file is provided at `Mini_Project_Medallion_ETL/data/raw/weather_raw.csv`. The cloud path reads the same raw file from a public S3 bucket and writes your bronze and silver layers to your own GCS bucket.

## Core Documentation

| Resource | Why it helps |
|---|---|
| [pandas User Guide](https://pandas.pydata.org/docs/user_guide/index.html) | Authoritative guide for indexing, missing data, groupby, merge, and copy-on-write behavior. Checked 2026-06-30. |
| [pandas 3.0.0 release notes](https://pandas.pydata.org/docs/whatsnew/v3.0.0.html) | Current behavior changes to know, especially copy-on-write and string dtype defaults. Checked 2026-06-30. |
| [pandas DataFrame API](https://pandas.pydata.org/docs/reference/frame.html) | Method reference for `info`, `describe`, `isna`, `drop_duplicates`, `merge`, and `to_parquet`. Checked 2026-06-30. |
| [Polars user guide](https://docs.pola.rs/) | Primary Polars reference for eager and lazy DataFrame work. Checked 2026-06-30. |
| [Polars migration guide from pandas](https://docs.pola.rs/user-guide/migration/pandas/) | Side-by-side comparison of pandas and Polars patterns. Checked 2026-06-30. |
| [Google Cloud Storage Python client](https://cloud.google.com/python/docs/reference/storage/latest) | Reference for `Client`, `bucket`, `blob`, `upload_from_string`, and `upload_from_filename`. Checked 2026-06-30. |
| [Boto3 S3 client docs](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html) | Reference for `get_object`, used to read the public S3 source. Checked 2026-06-30. |

## pandas Fundamentals

Start with pandas. It is the main tool to master today because it is the common language of Python data work.

```python
import io
import pandas as pd

raw_bytes = Path("data/raw/weather_raw.csv").read_bytes()
df = pd.read_csv(io.BytesIO(raw_bytes))

df.shape
df.dtypes
df.info()
df.describe()
df.isna().sum()
df.duplicated().sum()
```

Profile before cleaning. You are looking for object columns that should be numeric, impossible values, missing required fields, duplicate business keys, and row counts that change unexpectedly.

## pandas 3.0+ Notes

pandas 3.0 enables copy-on-write behavior by default. The practical rule is simple: avoid chained assignment and write changes directly back to the original DataFrame.

Use this:

```python
mask = df["tmax"].between(-40, 130)
df.loc[~mask, "tmax"] = pd.NA
```

Avoid this:

```python
df[df["tmax"] > 130]["tmax"] = pd.NA
```

The second pattern is ambiguous. In modern pandas, it does not reliably update the original DataFrame. Use `.loc[row_selector, column_selector] = value` when you mean to update a DataFrame.

## Cleaning Pattern

```python
df.columns = [col.strip().lower() for col in df.columns]
df["station"] = df["station"].astype("string").str.strip().str.upper()
df["date"] = pd.to_datetime(df["date"], errors="coerce")

for col in ("tmax", "tmin", "prcp"):
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna(subset=["date"])
df = df.drop_duplicates(subset=["station", "date"])
df["prcp"] = df["prcp"].fillna(0.0).clip(lower=0)
df = df.dropna(subset=["tmax", "tmin"])

df["temp_range"] = df["tmax"] - df["tmin"]
df["is_rainy"] = df["prcp"] > 0
```

Explain each decision in your project README. Dropping a row, filling a value, clipping a negative, and choosing a dedupe key are data engineering decisions, not just syntax.

## Polars Comparison

Polars is not a pandas drop-in. It has its own expression-based API and can run multi-threaded work efficiently.

```python
import io
import polars as pl

pl_df = pl.read_csv(io.BytesIO(raw_bytes))
pl_df = pl_df.rename({col: col.strip().lower() for col in pl_df.columns})
pl_df = pl_df.with_columns(
    pl.col("station").cast(pl.Utf8).str.strip_chars().str.to_uppercase(),
    pl.col("date").str.strptime(pl.Date, "%Y-%m-%d", strict=False),
    pl.col("tmax").cast(pl.Float64, strict=False),
    pl.col("tmin").cast(pl.Float64, strict=False),
    pl.col("prcp").cast(pl.Float64, strict=False),
)
```

In your README, compare one pandas operation with the matching Polars operation. Good examples: type casting, `groupby` versus `group_by`, or pandas method chains versus Polars expressions.

## Modin and FireDucks, Briefly

| Tool | What it is | Best classroom takeaway |
|---|---|---|
| pandas | Standard in-memory DataFrame library | Learn this first. It is the ecosystem baseline. |
| Polars | Separate DataFrame library with eager and lazy APIs | Best new-tool option when you can rewrite for speed and lower memory use. |
| Modin | Near drop-in pandas accelerator using engines such as Ray or Dask | Useful when existing pandas code is too slow and a rewrite is not realistic. |
| FireDucks | Near drop-in pandas accelerator for Linux environments | Useful as a compatibility experiment, but treat support and speed claims as version-specific. |

Do not use Modin or FireDucks in the required mini-project. The required comparison is pandas and Polars so the class can discuss a real API difference.

## Shipping to GCS

Use Application Default Credentials. Do not create or commit key files.

```bash
gcloud auth application-default login
gcloud config set project YOUR_PROJECT_ID
```

Upload pattern:

```python
from google.cloud import storage

client = storage.Client(project=GCP_PROJECT)
bucket = client.bucket(GCS_BUCKET)

bronze_blob = bucket.blob(
    f"bronze/{DATASET}/ingest_date={INGEST_DATE}/{DATASET}_raw.csv"
)
bronze_blob.upload_from_string(raw_bytes, content_type="text/csv")

silver_blob = bucket.blob(f"silver/{DATASET}/{DATASET}_clean.parquet")
silver_blob.upload_from_filename("data/silver/weather/weather_clean.parquet")
```

## Lab Deliverable Checklist

| Done? | Deliverable |
|---|---|
| [ ] | Work is inside `student-work/week2/`, not inside the provided lab folder. |
| [ ] | `pyproject.toml` and `uv.lock` show pandas, Polars, pyarrow, boto3, and google-cloud-storage. |
| [ ] | Local run works with `uv run python medallion_etl.py --local`. |
| [ ] | Cloud run reads the public S3 object anonymously and writes bronze raw bytes to GCS. |
| [ ] | Silver parquet is written to `gs://techcatalyst-de-2026-<your-username>-raw/silver/weather/weather_clean.parquet`. |
| [ ] | pandas cleaning decisions are explained in your README. |
| [ ] | Polars row count matches pandas row count, and your README notes one API difference. |
| [ ] | Pull request includes your script, README, UV files, and a screenshot of the GCS silver object. |
| [ ] | You reviewed one teammate's PR with at least two substantive comments. |

## Common Errors

| Error | Cause | Fix |
|---|---|---|
| `VIRTUAL_ENV does not match the project environment` | A leftover environment is active from another folder | Run `deactivate`, then retry `uv run ...` from `student-work/week2/`. |
| `ModuleNotFoundError: No module named 'pyarrow'` | Parquet dependency missing | Run `uv add pyarrow`, then rerun with `uv run`. |
| `DefaultCredentialsError` | GCS auth is not configured for local Python | Run `gcloud auth application-default login`. |
| `403` or `404` from GCS | Wrong project, bucket name, or bucket permissions | Check `gcloud config get-value project` and confirm the bucket exists. |
| pandas and Polars row counts differ | Cleaning decisions do not match across engines | Compare drop order, dedupe key, null handling, and negative precipitation handling. |

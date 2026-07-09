"""Week 3 Day 3 mini-project: medallion ETL (S3 raw -> GCS bronze -> GCS silver).

Build the pipeline tier by tier. Start with --local so you can iterate offline,
then switch to the cloud path once your GCS write works.

Auth (cloud mode): run once -> gcloud auth application-default login   (no key files)

Run from your copied work folder (the folder that contains data/):
    uv run python medallion_etl.py --local     # build and test offline first
    uv run python medallion_etl.py             # S3 -> GCS once local works
    uv run python medallion_etl.py --local --polars  # optional stretch
"""
import argparse
import io
from datetime import date
from pathlib import Path

import pandas as pd

# ---- Config: edit for your setup ----
SOURCE_BUCKET = "techcatalyst-de-2026"        # public S3 source (read-only)
SOURCE_KEY = "raw/weather/weather_raw.csv"
GCP_PROJECT = "your-gcp-project-id"                  # your assigned project
GCS_BUCKET = "techcatalyst-de-2026-your-username-raw"
DATASET = "weather"
INGEST_DATE = date.today().isoformat()

LOCAL_RAW = Path("data/raw/weather_raw.csv")
LOCAL_BRONZE = Path("data/bronze")
LOCAL_SILVER = Path("data/silver")


def require_cloud_config() -> None:
    """Fail early if the editable cloud settings still contain placeholders."""
    if GCP_PROJECT == "your-gcp-project-id":
        raise ValueError("Set GCP_PROJECT to your assigned Google Cloud project ID.")
    if "your-username" in GCS_BUCKET:
        raise ValueError("Set GCS_BUCKET to your bucket name.")


def bronze_blob_path() -> str:
    """Return the GCS object name for the immutable bronze raw file."""
    return f"bronze/{DATASET}/ingest_date={INGEST_DATE}/{DATASET}_raw.csv"


def silver_blob_path() -> str:
    """Return the GCS object name for the cleaned silver parquet file."""
    return f"silver/{DATASET}/{DATASET}_clean.parquet"


# ---- 1. EXTRACT ----
def read_raw_from_s3() -> bytes:
    """Read raw CSV bytes from the public S3 source.

    This is the cloud version of Path.read_bytes().

    Step sequence:
    1. Import boto3, UNSIGNED, and Config.
    2. Create an S3 client with Config(signature_version=UNSIGNED).
    3. Call get_object(Bucket=SOURCE_BUCKET, Key=SOURCE_KEY).
    4. Read and return obj["Body"].read().

    The source object is public and read-only, so no AWS keys are needed.
    """
    # TODO 1: import boto3, UNSIGNED, and Config.
    # TODO 2: create the unsigned S3 client.
    # TODO 3: fetch the object from SOURCE_BUCKET and SOURCE_KEY.
    # TODO 4: return the response body as bytes.
    pass


def read_raw_local() -> bytes:
    return LOCAL_RAW.read_bytes()


# ---- 2. BRONZE (land raw, unchanged) ----
def write_bronze_gcs(raw_bytes: bytes) -> str:
    """Upload raw bytes unchanged to the GCS bronze path and return the gs:// URI.

    Bronze is evidence of what arrived. Do not parse it, clean it, or rewrite it
    as a DataFrame before this upload.

    Step sequence:
    1. Call require_cloud_config() so placeholder project or bucket names fail
       with a clear message.
    2. Import google.cloud.storage.
    3. Create storage.Client(project=GCP_PROJECT). This uses ADC from gcloud auth.
    4. Build blob_path with bronze_blob_path().
    5. Create the blob handle with client.bucket(GCS_BUCKET).blob(blob_path).
    6. Upload raw_bytes with content_type="text/csv".
    7. Return f"gs://{GCS_BUCKET}/{blob_path}".
    """
    # TODO 1: call require_cloud_config().
    # TODO 2: create the GCS client.
    # TODO 3: build the bronze blob path.
    # TODO 4: upload raw_bytes unchanged.
    # TODO 5: return the gs:// URI.
    pass


def write_bronze_local(raw_bytes: bytes) -> str:
    out_dir = LOCAL_BRONZE / DATASET / f"ingest_date={INGEST_DATE}"
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{DATASET}_raw.csv"
    path.write_bytes(raw_bytes)
    return str(path)


# ---- 3. SILVER (clean with pandas) ----
def to_silver(raw_bytes: bytes) -> pd.DataFrame:
    df = pd.read_csv(io.BytesIO(raw_bytes))
    # TODO: normalize column names to lowercase
    # TODO: station -> stripped uppercase; date -> strip text, then
    #       pd.to_datetime(errors="coerce"); tmax/tmin/prcp ->
    #       pd.to_numeric(errors="coerce")
    # TODO: drop rows with no date; drop_duplicates on (station, date)
    # TODO: prcp -> fillna(0.0).clip(lower=0); drop rows missing tmax or tmin
    # TODO: add derived columns temp_range and is_rainy
    # pandas 3.0+ note: avoid chained assignment. Use df.loc[row_mask, "col"] = value
    # when you mean to update the original DataFrame.
    return df


def write_silver_gcs(df: pd.DataFrame) -> str:
    """Write silver parquet locally, upload it to GCS, and return the gs:// URI.

    Silver is the cleaned table. We write a local parquet first for two reasons:
    it gives you local evidence to inspect, and upload_from_filename can send the
    exact file to GCS.

    Step sequence:
    1. Call require_cloud_config().
    2. Write df to data/silver/weather/weather_clean.parquet with index=False.
    3. Create storage.Client(project=GCP_PROJECT).
    4. Build blob_path with silver_blob_path().
    5. Upload the local parquet file with upload_from_filename(...).
    6. Return f"gs://{GCS_BUCKET}/{blob_path}".
    """
    # TODO 1: call require_cloud_config().
    # TODO 2: write the DataFrame to the local parquet path.
    # TODO 3: create the GCS client.
    # TODO 4: upload the parquet file to silver_blob_path().
    # TODO 5: return the gs:// URI.
    pass


def write_silver_local(df: pd.DataFrame) -> str:
    out = LOCAL_SILVER / DATASET / f"{DATASET}_clean.parquet"
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(out, index=False)
    return str(out)


# ---- Silver in Polars (the same clean, a different engine) ----
def to_silver_polars(raw_bytes: bytes):
    """Optional stretch: reproduce to_silver() using Polars.

    Leave this as None if you are focusing on the required pandas path.
    """
    # TODO: reproduce to_silver() using Polars: pl.read_csv, rename to lowercase,
    # cast types (pl.col("date").str.strptime(pl.Date, ...); cast Float64 for the
    # numeric cols), drop_nulls(["date"]), unique(["station","date"]), set null or
    # negative prcp to 0, drop_nulls(["tmax","tmin"]), add temp_range and is_rainy.
    # Return the Polars DataFrame and compare its row count to your pandas version.
    pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--local", action="store_true", help="run fully local, no cloud")
    parser.add_argument("--polars", action="store_true", help="run optional Polars stretch")
    args = parser.parse_args()

    raw_bytes = read_raw_local() if args.local else read_raw_from_s3()
    print(f"extracted {len(raw_bytes)} bytes")

    bronze_uri = write_bronze_local(raw_bytes) if args.local else write_bronze_gcs(raw_bytes)
    print("bronze:", bronze_uri)

    df = to_silver(raw_bytes)
    print(f"silver rows: {len(df)}")
    silver_uri = write_silver_local(df) if args.local else write_silver_gcs(df)
    print("silver:", silver_uri)

    if args.polars:
        pl_df = to_silver_polars(raw_bytes)
        if pl_df is None:
            print("polars silver rows: TODO")
        else:
            print("polars silver rows:", pl_df.height)
    else:
        print("polars stretch skipped")


if __name__ == "__main__":
    main()

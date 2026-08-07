"""
Optional: loading your conformed data into BigQuery as a second destination.

You learned the Snowflake Python SDKs in Week 4 but not the BigQuery client,
so this exists so the API mechanics do not cost you sprint time. This is an
optional lane. Snowflake remains the graded destination.

Setup from the repository root:

    uv add google-cloud-bigquery
    gcloud auth application-default login

If you do this, make it worth presenting: measure load time, query the same
question on both platforms, and compare cost models and developer experience.
A comparison with real numbers behind it is a strong presentation section.
An unmeasured "we also loaded it into BigQuery" is not.
"""

import time

from google.cloud import bigquery

PROJECT_ID = "your-project-id"
DATASET_ID = "capstone"
LOCATION = "US"


def get_client():
    return bigquery.Client(project=PROJECT_ID)


def ensure_dataset(client):
    dataset_ref = f"{PROJECT_ID}.{DATASET_ID}"
    dataset = bigquery.Dataset(dataset_ref)
    dataset.location = LOCATION
    return client.create_dataset(dataset, exists_ok=True)


def load_parquet_from_gcs(client, gcs_uri, table_name):
    """
    Load Parquet from GCS into BigQuery.

    BigQuery loads from GCS, not from S3. If your conformed data is in S3 you
    will need to copy it to a GCS bucket first (gsutil or the storage client),
    or use BigQuery Omni. Budget for that step before you commit to this lane.
    """
    table_id = f"{PROJECT_ID}.{DATASET_ID}.{table_name}"

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.PARQUET,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    )

    start = time.perf_counter()
    load_job = client.load_table_from_uri(gcs_uri, table_id, job_config=job_config)
    load_job.result()
    elapsed = time.perf_counter() - start

    table = client.get_table(table_id)
    print(f"{table_name}: {table.num_rows:,} rows in {elapsed:.1f}s")
    return table.num_rows, elapsed


def load_dataframe(client, df, table_name):
    """Load a pandas DataFrame directly. Fine for lookups, not for trip data."""
    table_id = f"{PROJECT_ID}.{DATASET_ID}.{table_name}"
    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    )
    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    job.result()
    print(f"{table_name}: loaded {len(df):,} rows")


def query_with_cost(client, sql):
    """
    Run a query and report what it scanned.

    BigQuery bills on bytes processed, so this number is the cost. Use it in
    your platform comparison. Note that Snowflake bills on warehouse time
    instead, which is why the two are not directly comparable and why saying
    so is part of a good answer.
    """
    start = time.perf_counter()
    job = client.query(sql)
    rows = job.result()
    elapsed = time.perf_counter() - start

    gb = job.total_bytes_processed / 1024**3
    print(f"{elapsed:.2f}s, {gb:.3f} GB processed, billed {job.total_bytes_billed / 1024**3:.3f} GB")
    return rows


def dry_run_cost(client, sql):
    """Estimate bytes scanned without running the query. Check before you run."""
    job_config = bigquery.QueryJobConfig(dry_run=True, use_query_cache=False)
    job = client.query(sql, job_config=job_config)
    gb = job.total_bytes_processed / 1024**3
    print(f"This query would scan {gb:.3f} GB")
    return job.total_bytes_processed


if __name__ == "__main__":
    client = get_client()
    ensure_dataset(client)
    print(f"Ready: {PROJECT_ID}.{DATASET_ID}")

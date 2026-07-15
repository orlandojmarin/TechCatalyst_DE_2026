"""Starter script for the Polars ETL and SQLite refresher.

Copy this file to student-work/week4/day1/refresher before editing it.
Complete the pandas activity first so the shared SQLite file already exists.
"""

from pathlib import Path
import sqlite3

import polars as pl


S3_URI = "s3://techcatalyst-de-2026/nyc-taxi/yellow-tripdata/yellow_tripdata_2026-01.parquet"
POLARS_STORAGE_OPTIONS = {
    "aws_region": "us-east-1",
    "skip_signature": "true",
}

REQUIRED_COLUMNS = {
    "tpep_pickup_datetime", "tpep_dropoff_datetime", "PULocationID", "DOLocationID",
    "trip_distance", "fare_amount", "tip_amount", "payment_type",
}
CHARGE_COLUMNS = {
    "fare_amount", "extra", "mta_tax", "tip_amount", "tolls_amount",
    "improvement_surcharge", "congestion_surcharge", "Airport_fee",
}
DB_PATH = Path("nyc_taxi_refresher.db").resolve()
DB_URI = f"sqlite:///{DB_PATH}"


def main() -> None:
    # TODO 1: union and sort REQUIRED_COLUMNS and CHARGE_COLUMNS.
    # Expected: 14 unique names in read_columns.

    # TODO 2: scan S3_URI with pl.scan_parquet.
    # Pass storage_options=POLARS_STORAGE_OPTIONS, select read_columns,
    # and collect the result as pldf.
    # Show pldf.head() and pldf.schema.

    # TODO 3: validate that every REQUIRED_COLUMNS name was loaded.

    # TODO 4: create pldf_clean with fractional duration minutes,
    # a null-safe total charge, trip_date, and is_valid_trip.
    # Use .dt.total_seconds(fractional=True) / 60 for duration.
    # Show pldf_clean.head() and pldf_clean.schema.

    # TODO 5: create pldf_daily_summary and pldf_quality_summary.
    # Expected shapes: (33, 6) and (1, 4).

    # TODO 6: use DataFrame.write_database() to write:
    # polars_daily_summary and polars_quality_summary.
    # Pass connection=DB_URI and if_table_exists="replace".

    with sqlite3.connect(DB_PATH) as connection:
        tables = connection.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name"
        ).fetchall()
    print("SQLite tables:", tables)


if __name__ == "__main__":
    main()


"""Starter script for the pandas ETL and SQLite refresher.

Copy this file to student-work/week4/day1/refresher before editing it.
"""

from pathlib import Path
import sqlite3

import pandas as pd


S3_URI = "s3://techcatalyst-de-2026/nyc-taxi/yellow-tripdata/yellow_tripdata_2026-01.parquet"
PANDAS_STORAGE_OPTIONS = {"anon": True}

REQUIRED_COLUMNS = {
    "tpep_pickup_datetime", "tpep_dropoff_datetime", "PULocationID", "DOLocationID",
    "trip_distance", "fare_amount", "tip_amount", "payment_type",
}
CHARGE_COLUMNS = {
    "fare_amount", "extra", "mta_tax", "tip_amount", "tolls_amount",
    "improvement_surcharge", "congestion_surcharge", "Airport_fee",
}
DB_PATH = Path("nyc_taxi_refresher.db").resolve()


def main() -> None:
    # TODO 1: union and sort REQUIRED_COLUMNS and CHARGE_COLUMNS.
    # Expected: 14 unique names in read_columns.

    # TODO 2: read S3_URI with pd.read_parquet.
    # Pass columns=read_columns, engine="pyarrow", and
    # storage_options=PANDAS_STORAGE_OPTIONS.
    # Show pdf.head() and pdf.info().

    # TODO 3: validate that every REQUIRED_COLUMNS name was loaded.

    # TODO 4: create pdf_clean with fractional duration minutes,
    # a null-safe total charge, trip_date, and is_valid_trip.
    # Show pdf_clean.head() and pdf_clean.info().

    # TODO 5: create pdf_daily_summary and pdf_quality_summary.
    # Expected shapes: (33, 6) and (1, 4).

    # This connection creates the SQLite file if it does not exist.
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute("SELECT 1")

        # TODO 6: use DataFrame.to_sql() to write:
        # pandas_daily_summary and pandas_quality_summary.
        # Use if_exists="replace" and index=False.
        pass

    print("SQLite database:", DB_PATH)


if __name__ == "__main__":
    main()


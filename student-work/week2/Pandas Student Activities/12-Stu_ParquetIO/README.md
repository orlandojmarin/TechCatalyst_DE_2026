# Parquet In, Parquet Out

The deferred medallion mini-capstone asks you to write cleaned data as parquet, not CSV. This activity is the isolated warm up: before you wire parquet into the medallion pipeline, get comfortable with what parquet actually does differently from CSV.

## Instructions

Using the [starter file](Unsolved/parquet_io.ipynb) and `Resources/insurance_claims.csv`, complete the following steps:

1. Read `insurance_claims.csv` into a DataFrame with `pd.read_csv`. Check `df.dtypes`. Note that `claim_date` reads in as a plain string (`object` or `str`), not a date.

2. Convert `claim_date` to a real datetime column with `pd.to_datetime`.

3. Write the DataFrame to `Resources/insurance_claims.parquet` using `df.to_parquet(..., index=False)`. You will need the `pyarrow` package installed (`uv add pyarrow` if it is not already in your project).

4. Read the parquet file back into a new DataFrame with `pd.read_parquet`. Check `df.dtypes` again.

5. Compare the two files on disk with `os.path.getsize()` for both `insurance_claims.csv` and `insurance_claims.parquet`. Report which one is smaller and by how much.

6. Answer in a markdown cell: after the round trip through parquet, did `claim_date` come back as a datetime, or did you have to re-parse it like you did with the CSV? What does that tell you about why bronze/silver pipelines write parquet instead of CSV?

## Challenge

Add a `claim_amount` filter to keep only claims over $5,000, then write that filtered subset to a second parquet file, partitioned by `region` using `df.to_parquet(path, partition_cols=["region"])`. Look at what `partition_cols` does to the folder structure it creates. This is the same partitioning idea behind `ingest_date=YYYY-MM-DD/` in a bronze zone.

## Hint

* `pd.read_csv` never remembers dtypes across a save and reload; every column becomes a string again once written back out as CSV. Parquet is a binary, typed, columnar format, so it remembers.
* Consult the [pandas Parquet documentation](https://pandas.pydata.org/docs/user_guide/io.html#parquet) if you get stuck.

## References

Synthetic insurance claims dataset created for this activity.

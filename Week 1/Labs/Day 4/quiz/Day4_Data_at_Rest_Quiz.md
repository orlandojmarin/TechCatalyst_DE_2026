# Day 4: Data at Rest — Storage, Schema & Query-in-Place
# Score 100

## Q1: BigQuery and Snowflake both separate storage from compute. What does that let you do?
- [ ] Keep the stored data only while a query is actively running
- [ ] Query files that contain no schema of any kind
- [x] Resize compute independently of the stored data
- [ ] Skip storage costs as long as you query often
::time=25

## Q2: A curated, governed table optimized for fast BI on one business subject is best described as a…
- [ ] data lake
- [x] data mart
- [ ] landing zone
- [ ] raw object store
::time=20

## Q3: In `gs://taxi-raw/raw/yellow/year=2026/file.parquet`, the `raw/yellow/year=2026/` portion is…
- [x] a prefix shown as folders, though the key is one flat string
- [ ] a real, nested directory tree physically stored on the disk volume
- [ ] a separate storage bucket nested inside this bucket
- [ ] schema metadata the engine needs before it can read
::time=25

## Q4: Your pipeline lands trip data as Parquet rather than CSV mainly because Parquet…
- [ ] can be opened and read in any plain text editor
- [ ] needs no schema at all in order to be queried
- [ ] groups whole rows together to speed up single-row inserts
- [x] is columnar, so a query reads only the columns it needs
::time=25

## Q5: An external table over a CSV uses "schema-on-read." That means…
- [ ] data is validated, cleaned, and reshaped before it is ever stored
- [x] the engine applies structure at read time, not at write time
- [ ] the schema is written permanently inside the CSV file
- [ ] only columnar file formats can be read this way
::time=25

## Q6: Creating a BigQuery external table over a GCS file…
- [ ] copies the rows into BigQuery-managed storage
- [ ] converts the CSV to Parquet automatically
- [x] saves only metadata; the data stays in GCS
- [ ] makes the underlying file publicly downloadable
::time=25

## Q7: You query a tiny external CSV and Job information shows **409 B processed** but **10 MB billed**. Why?
- [x] BigQuery bills a 10 MB minimum per query, rounded up
- [ ] The CSV file is secretly about 10 MB on disk
- [ ] External-table queries are always billed at a flat 10 MB
- [ ] Bytes processed and bytes billed are always identical
::time=30

## Q8: On a row-oriented external CSV, why do `SELECT * ... LIMIT 10` and a full `GROUP BY` scan about the same bytes?
- [ ] `LIMIT 10` lets the engine stop reading after ten rows
- [ ] `GROUP BY` reads only the two columns that it needs
- [ ] The whole file is cached in memory right after the first scan
- [x] CSV is row-oriented, so the whole file is read either way
::time=35

## Q9: With Public Access Prevention on, an anonymous browser hits a GCS object URL and gets **AccessDenied**, yet the console **Open** works. Why?
- [ ] The console turns off public-access prevention briefly
- [ ] The object is public to any signed-in Google user
- [x] The console sends a request signed with your identity
- [ ] AccessDenied appears only in incognito mode
::time=30

## Q10: Regulators require claims files be kept 7 years and not deletable early — even by an admin. Which control enforces that?
- [ ] An object lifecycle (age-based) deletion rule
- [x] A locked retention policy (Bucket Lock)
- [ ] Object versioning
- [ ] Soft delete
::time=30

## Q11: In the AWS↔GCP mapping, S3 **Object Lock (Compliance mode)** is the counterpart of…
- [x] a locked GCS retention policy
- [ ] GCS object versioning plus soft delete recovery
- [ ] GCS soft delete on its own
- [ ] GCS uniform bucket-level access
::time=25

## Q12: Amazon Athena can run SQL over S3 files only after…
- [ ] the files are first fully loaded into a managed database
- [ ] the bucket is made publicly readable to anyone
- [ ] the CSVs are first converted to Parquet format
- [x] a table is registered in the Glue Data Catalog
::time=25

## Q13: What is a Glue Crawler's actual job?
- [ ] Run your saved Athena queries automatically on a schedule
- [ ] Copy S3 files into a Redshift data warehouse
- [x] Infer schema and register tables in the Glue catalog
- [ ] Encrypt the objects that are stored in your bucket
::time=25

## Q14: Creating an S3 bucket for a data-lake landing zone, which bucket type do you choose?
- [ ] Directory bucket for low-latency workloads
- [x] General purpose bucket
- [ ] Table bucket for managed Iceberg tables
- [ ] Vector bucket for similarity search
::time=20

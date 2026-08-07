# Capstone Data Catalog

Read this before you write any code. It will save you a day.

---

## What you have

All raw files are in the capstone RAW bucket, in Parquet format, partitioned by taxi type and month.

```
s3://capstone-techcatalyst-raw/yellow_taxi/yellow_tripdata_2025-01.parquet
s3://capstone-techcatalyst-raw/yellow_taxi/yellow_tripdata_2025-02.parquet
...
s3://capstone-techcatalyst-raw/yellow_taxi/yellow_tripdata_2026-06.parquet

s3://capstone-techcatalyst-raw/green_taxi/green_tripdata_2025-01.parquet
...
s3://capstone-techcatalyst-raw/green_taxi/green_tripdata_2026-06.parquet

s3://capstone-techcatalyst-raw/lookup/taxi_zone_lookup.csv
s3://capstone-techcatalyst-raw/lookup/taxi_zones.zip          (shapefiles, optional)
s3://capstone-techcatalyst-raw/reference/trip_record_user_guide.pdf
s3://capstone-techcatalyst-raw/reference/data_dictionary_trip_records_yellow.pdf
s3://capstone-techcatalyst-raw/reference/data_dictionary_trip_records_green.pdf
```

| Dataset | Files | Approximate rows | Approximate size |
| :--- | :--- | :--- | :--- |
| Yellow taxi | 12 (Jan to Jun 2025, Jan to Jun 2026) | ~40 million | ~700 MB |
| Green taxi | 12 (same months) | ~600 thousand | ~16 MB |
| Taxi zone lookup | 1 | 265 | ~12 KB |

Green is tiny compared to Yellow. That is not an error in the data, it reflects the actual size of the two fleets. Plan your joins accordingly, and be careful about drawing conclusions from Green in low-volume zones.

## Optional scale track: High Volume FHV

If your team wants to prove it can handle real volume, the Uber and Lyft data is available on request:

```
s3://capstone-techcatalyst-raw/hvfhv/fhvhv_tripdata_YYYY-MM.parquet
```

This is roughly **20 million rows and 500 MB per month**. One month of HVFHV is larger than the entire Yellow and Green dataset combined. Do not touch this until your required pipeline works end to end. It has broken previous cohorts' timelines.

---

## Schemas

### Yellow taxi

| Column | Type | Notes |
| :--- | :--- | :--- |
| `VendorID` | int | Technology provider that supplied the record |
| `tpep_pickup_datetime` | timestamp | Meter engaged |
| `tpep_dropoff_datetime` | timestamp | Meter disengaged |
| `passenger_count` | nullable int | Driver-entered, not measured |
| `trip_distance` | double | Miles, reported by the taximeter |
| `RatecodeID` | nullable int | See lookup below |
| `store_and_fwd_flag` | string | `Y` if the record was held in vehicle memory before sending |
| `PULocationID` | int | Pickup taxi zone |
| `DOLocationID` | int | Dropoff taxi zone |
| `payment_type` | int | See lookup below |
| `fare_amount` | double | Time and distance fare only |
| `extra` | double | Miscellaneous surcharges |
| `mta_tax` | double | |
| `tip_amount` | double | **Credit card tips only. See the trap below.** |
| `tolls_amount` | double | |
| `improvement_surcharge` | double | |
| `total_amount` | double | Does not include cash tips |
| `congestion_surcharge` | double | |
| `airport_fee` | double | |
| `cbd_congestion_fee` | double | **2025 onward only. See the schema change below.** |

### Green taxi

Same shape with these differences:

- Pickup and dropoff columns are named `lpep_pickup_datetime` and `lpep_dropoff_datetime`, not `tpep_*`.
- Adds `ehail_fee` (frequently entirely null).
- Adds `trip_type`: `1` = street-hail, `2` = dispatch.
- Has no `airport_fee`.

**Your union of Yellow and Green will not work until you reconcile these.** Renaming the timestamp columns and adding a `taxi_type` column is the minimum. Decide deliberately what to do about the columns that exist in only one of them.

---

## The 2025 schema change

New York City's central business district tolling program began **January 5, 2025**. The `cbd_congestion_fee` column was added to the trip records starting with 2025 data.

Both of your years are 2025 and later, so both should carry the column. Confirm this yourself on the actual files rather than trusting this document, because a column that is present but entirely null behaves very differently from one that is populated, and the difference will matter to any fare analysis you build.

More generally: verify the schema of every file before you union anything. Assuming twelve files share a schema because they share a naming convention is one of the most common and most expensive mistakes in this line of work.

---

## Lookup values

You will need these to make your output readable. `payment_type = 1` means nothing to a business audience.

**`payment_type`**

| Value | Meaning |
| :--- | :--- |
| 1 | Credit card |
| 2 | Cash |
| 3 | No charge |
| 4 | Dispute |
| 5 | Unknown |
| 6 | Voided trip |

**`RatecodeID`**

| Value | Meaning |
| :--- | :--- |
| 1 | Standard rate |
| 2 | JFK |
| 3 | Newark |
| 4 | Nassau or Westchester |
| 5 | Negotiated fare |
| 6 | Group ride |
| 99 | Unknown, undocumented |

**`store_and_fwd_flag`**: `Y` = store and forward trip, `N` = sent live.

**`VendorID`** and the full official definitions are in the data dictionary PDFs in the `reference/` prefix. Read them.

You will find values in the data that do not appear in the official dictionary. That is not a bug in this catalog, it is a real property of the dataset, and how you handle it belongs in your Data Quality Incident Report.

**Taxi zones**: `taxi_zone_lookup.csv` maps `LocationID` 1 to 265 to a borough, a zone name, and a service zone. Note that IDs `264` and `265` are the catch-all "unknown" and "outside of NYC" entries. They will show up in your top-ten lists and make you look foolish in a presentation if you have not thought about them.

---

## Known traps

These are real and they are in your data. This list is not exhaustive. Finding the ones not listed here is part of the assignment.

### The cash tip trap

`tip_amount` is populated for credit card transactions. **Cash tips are not recorded and appear as `0.00`.**

If you compute average tip percentage across all trips, you will produce a number that is wrong, and it will be wrong in a specific direction: it will understate tipping, and it will make cash-heavy zones and cash-heavy times of day look stingy when they are not.

Almost every cohort produces this chart at least once. Decide explicitly how you are handling it, and say so on the slide.

### Timestamps outside the file's month

A file named `yellow_tripdata_2025-03.parquet` contains records with pickup dates in other months, and occasionally in other years entirely, sometimes decades off. These are meter or transmission errors.

If you partition by a date derived from the data rather than from the filename, you will end up with partitions for dates that should not exist.

### Impossible values

Expect to find, in varying quantities:

- Negative `fare_amount` and negative `total_amount` (adjustments and refunds)
- `trip_distance` of exactly `0` on trips with a substantial fare
- `trip_distance` in the thousands of miles
- `passenger_count` of `0`, and nulls
- Dropoff timestamps earlier than pickup timestamps
- Trips lasting a fraction of a second, and trips lasting many hours
- `total_amount` that does not equal the sum of its component charges

### Duplicates

Check for them. Decide what constitutes a duplicate in this dataset before you deduplicate, because there is no natural primary key and two genuinely distinct trips can share a great many field values.

---

## A note on method

You are not expected to fix all of this. You are expected to know what is in there, decide what to do, and be able to explain the decision.

The strongest possible answer to "why did you drop those records" is a number, a reason, and an honest statement of what was lost. The weakest is "they looked wrong."

---

## Extending the data

You may bring in other sources. These pair naturally with the taxi data:

| Source | Where | Pairs well with |
| :--- | :--- | :--- |
| NYC Open Data | https://opendata.cityofnewyork.us | Collisions, air quality, construction, 311 requests |
| NYC TLC | https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page | The official record layouts and any months you want to add |
| NOAA / Open-Meteo | https://open-meteo.com/en/docs/historical-weather-api | Weather effects on demand, free and no key required |

Enrichment is a differentiator, not a requirement. A clean core pipeline with one well-defended finding beats a sprawling one that joins five sources and concludes nothing.

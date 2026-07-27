# Activity 3: Sources, Seeds, and Tests

**Module:** Week 5 Day 4  
**Estimated Time:** 70 to 85 minutes  
**Difficulty:** Intermediate  
**Format:** Individual, self-paced; partner check at each checkpoint  
**Prerequisites:** Activity 2 complete, all seven models building

## Objective

Turn a working collection of models into a trustworthy dbt project. You will declare raw inputs as sources, load a small reference dataset as a seed, build an analysis-ready mart, and convert data assumptions into executable tests.

## Where this fits in the journey

Activities 1 and 2 proved that dbt can transform data. This activity adds three things a folder of SQL worksheets does not provide:

| dbt resource | Question it answers |
|---|---|
| Source | Where did this raw data come from? |
| Seed | Which small reference data belongs with the project code? |
| Test | What must be true before downstream work can be trusted? |

The flow after this activity is:

```text
AIRBNB.RAW sources
        |
        v
staging views -> dimensions and fact -> mart
                                         ^
                                         |
                               full moon date seed

Tests attach to models and stop bad assumptions from traveling downstream.
```

## Task 1: Declare the raw sources

The staging models currently hardcode names such as `AIRBNB.RAW.RAW_LISTINGS`. That works, but the location is repeated in several SQL files. A source declaration moves warehouse location details into one YAML file and gives the raw tables logical names.

Create `models/sources.yml`:

```yaml
sources:
  - name: airbnb
    database: AIRBNB
    schema: RAW
    tables:
      - name: listings
        identifier: RAW_LISTINGS
      - name: hosts
        identifier: RAW_HOSTS
      - name: reviews
        identifier: RAW_REVIEWS
```

The distinction matters:

- `name: listings` is the logical name used in your dbt code.
- `identifier: RAW_LISTINGS` is the physical table name in Snowflake.
- `database: AIRBNB` is required because your profile defaults to `TECHCATALYST`.
- `schema: RAW` completes the physical input location.

Without `database: AIRBNB`, dbt would look for `TECHCATALYST.RAW.RAW_LISTINGS`, which is the wrong database.

Now replace only the input line inside each staging CTE.

`models/src/src_listings.sql`:

```sql
WITH raw_listings AS (
    SELECT * FROM {{ source('airbnb', 'listings') }}
)
```

Use the matching logical names in `src_reviews.sql` and `src_hosts.sql`, then run:

```bash
dbt run --select src_listings src_reviews src_hosts
```

This activity spells out the long form, `--select`. It behaves exactly like `-s`. The three space-separated names select a group of three models, not their downstream children.

Compile one model and inspect the result:

```bash
dbt compile --select src_listings
```

**Checkpoint:** the compiled SQL still reads `AIRBNB.RAW.RAW_LISTINGS`. The data did not move. You centralized its location, added source nodes to the DAG, and made future location changes safer.

### Source versus `ref()`

Use `source()` when dbt does not build the input, such as an ingestion tool's raw table. Use `ref()` when another dbt model or seed owns the input. This boundary tells the lineage graph where your dbt project begins.

## Task 2: Load a small reference seed

### Why are full moon dates in an Airbnb project?

Imagine that an Airbnb analyst asks a playful exploratory question:

> Do reviews written the day after a full moon have a different sentiment pattern from reviews written on other days?

The Airbnb review data contains the event we want to analyze: one row for each review, including its date and sentiment. It does **not** tell us which calendar dates were full moons. That information must come from a second dataset.

The full moon CSV is a tiny reference calendar. Its grain is one row per full moon date. In Task 3, you will use it to label each review as either:

- `day after full moon`, when the review date is one day after a date in the seed, or
- `other day`, when it is not.

This is an intentionally memorable example of **data enrichment**. Data engineers frequently combine a large event dataset with a smaller reference dataset to add analytical context. The reference data might be unusual here, but the engineering pattern is common.

The result can show an association in this dataset. It cannot prove that a full moon caused a change in review sentiment. The review date is also the date the review was written, not necessarily the date of the guest's stay. Those limitations matter when communicating the result.

### What exactly is a dbt seed?

A seed begins as a CSV file stored inside the dbt project. Running `dbt seed` loads that file into the warehouse as a relation that SQL models can query.

```text
CSV file in the project
        |
        | dbt seed
        v
table in TECHCATALYST.<STUDENTNAME>
        |
        | ref('seed_full_moon_dates')
        v
mart_fullmoon_reviews
```

The CSV is the project-controlled definition of the data. The Snowflake table is the generated warehouse copy. If the CSV changes, the project change can be reviewed in Git and `dbt seed` can load the revised values into another environment.

Seeds are dbt resources, but they are not SQL models:

- A **model** begins with a SQL `SELECT` statement and transforms warehouse data.
- A **seed** begins with rows in a CSV file and loads those rows into the warehouse.
- Both can be referenced with `ref()`, which gives dbt dependency order and lineage.

### Why a data engineer might choose a seed

Seeds work well when the data is:

- small enough to review in a text file,
- slow-changing,
- owned by the analytics project,
- non-sensitive, and
- useful in multiple transformations or tests.

Common production examples include:

- country or state code mappings,
- a small list of internal business categories,
- test-account IDs that reporting should exclude,
- manually approved risk bands,
- a short fiscal-period lookup, or
- legacy values mapped to current standard values.

Seeds are a poor fit for large, frequently changing, sensitive, or operational data. Airbnb reviews belong in an ingestion-managed raw table because new review events keep arriving. Millions of review rows should not be committed to Git or reloaded from a project CSV.

Use this decision rule:

| Situation | Best dbt resource | Why |
|---|---|---|
| An ingestion process owns a changing warehouse table | `source()` | dbt reads it but does not own or create it |
| The project owns a small, stable CSV lookup | Seed, then `ref()` | dbt loads it, versions it with the project, and tracks its lineage |
| The value can be derived from warehouse data with SQL | Model, then `ref()` | dbt should calculate it instead of storing duplicate manual data |

The full moon dates could be a source in a larger company if another team maintained an enterprise calendar table. In this lab, the project owns a small CSV copy, so a seed is the simplest appropriate choice.

### Load the seed

From the dbt project root:

```bash
mkdir -p seeds
curl -L https://dbt-datasets.s3.us-east-2.amazonaws.com/seed_full_moon_dates.csv \
  -o seeds/seed_full_moon_dates.csv
dbt seed --select seed_full_moon_dates
```

**Checkpoint:** `TECHCATALYST.<STUDENTNAME>.<STUDENTNAME>_SEED_FULL_MOON_DATES` exists.

Open the table and inspect a few rows:

```sql
SELECT *
FROM TECHCATALYST.<STUDENTNAME>.<STUDENTNAME>_SEED_FULL_MOON_DATES
ORDER BY full_moon_date
LIMIT 10;
```

Before continuing, be able to explain the lifecycle in your own words: the repository stores the CSV, `dbt seed` creates its warehouse copy, and downstream models use `ref()` to depend on it.

## Task 3: Build the full moon mart

A mart answers a specific analytical question. It should be easy for an analyst to query without reconstructing transformation logic.

Create `models/mart/mart_fullmoon_reviews.sql`:

```sql
WITH fct_reviews AS (
    SELECT * FROM {{ ref('fct_reviews') }}
),
full_moon_dates AS (
    SELECT * FROM {{ ref('seed_full_moon_dates') }}
)
SELECT
    r.*,
    CASE
        WHEN fm.full_moon_date IS NULL THEN 'other day'
        ELSE 'day after full moon'
    END AS moon_phase_group
FROM fct_reviews r
LEFT JOIN full_moon_dates fm
    ON TO_DATE(r.review_date) = DATEADD(DAY, 1, fm.full_moon_date)
```

Both CTEs have a purpose here. They name two inputs with different grains before the join:

- `fct_reviews`: one row per review
- `full_moon_dates`: one row per full moon date

The `LEFT JOIN` preserves every review. `DATEADD(DAY, 1, ...)` makes the comparison explicit: the matching group contains reviews written one day after a full moon, not reviews written on the full moon date.

The seed does not contain every calendar date, and it does not contain Airbnb data. It only supplies the special dates needed to enrich the review events. The mart combines the two datasets and gives analysts a convenient grouping column.

Build the mart and answer its question:

```bash
dbt run --select mart_fullmoon_reviews
```

```sql
SELECT
    moon_phase_group,
    review_sentiment,
    COUNT(*) AS reviews
FROM TECHCATALYST.<STUDENTNAME>.<STUDENTNAME>_MART_FULLMOON_REVIEWS
GROUP BY moon_phase_group, review_sentiment
ORDER BY moon_phase_group, review_sentiment;
```

**Checkpoint:** both `day after full moon` and `other day` groups appear. The query provides evidence, but it does not prove that the moon caused a sentiment change.

## Task 4: Declare generic data tests

A data test is an assertion about the rows produced by a resource. Generic tests cover reusable checks such as uniqueness, nullability, accepted values, and relationships.

Create `models/schema.yml`:

```yaml
models:
  - name: dim_listings_cleansed
    columns:
      - name: listing_id
        data_tests:
          - unique
          - not_null
      - name: host_id
        data_tests:
          - not_null
          - relationships:
              arguments:
                to: ref('dim_hosts_cleansed')
                field: host_id
      - name: room_type
        data_tests:
          - accepted_values:
              arguments:
                values:
                  - Entire home/apt
                  - Private room
                  - Shared room
                  - Hotel room

  - name: dim_hosts_cleansed
    columns:
      - name: host_id
        data_tests:
          - unique
          - not_null
      - name: host_name
        data_tests:
          - not_null
```

Run the generic tests:

```bash
dbt test
```

You declared eight generic tests:

| Test | Business meaning |
|---|---|
| `unique` + `not_null` on listing ID | Every listing has one usable key |
| `not_null` on listing host ID | Every listing identifies a host |
| `relationships` on listing host ID | Every referenced host exists |
| `accepted_values` on room type | Room categories stay within the expected domain |
| `unique` + `not_null` on host ID | Every host has one usable key |
| `not_null` on host name | Cleansing removed anonymous nulls |

YAML indentation is part of the syntax. `arguments` belongs under the test name, and `to` plus `field` belong under `arguments`.

**Checkpoint:** all eight generic tests pass. If one fails, read its name and inspect the returned invalid rows before changing either the model or the test.

## Task 5: Write a singular data test

Generic tests are reusable. A singular test is a SQL query for a project-specific rule.

The contract is simple:

- zero returned rows means pass,
- one or more returned rows means fail.

Create `tests/dim_listings_minimum_nights.sql`:

```sql
SELECT *
FROM {{ ref('dim_listings_cleansed') }}
WHERE minimum_nights < 1
LIMIT 10
```

Run only this test:

```bash
dbt test --select dim_listings_minimum_nights
```

**Checkpoint:** the test passes because Activity 2 changed zero-night minimums to one.

### Prove that the test protects something

1. Temporarily comment out the `WHEN minimum_nights = 0 THEN 1` branch in `dim_listings_cleansed.sql`.
2. Rebuild the dimension with `dbt run --select dim_listings_cleansed`.
3. Rerun the singular test and inspect the failing rows.
4. Restore the `CASE` expression.
5. Rebuild the dimension and rerun the test until it passes.

Seeing the failure closes the learning loop: the model enforces the rule, and the test detects when the rule disappears.

## Task 6: Build the project as one dependency graph

Run:

```bash
dbt build
```

`dbt run` builds selected models. `dbt test` tests existing resources. `dbt build` selects seeds, models, snapshots, and tests together and executes them in DAG order. A failed upstream test can cause dependent nodes to skip, which prevents known-bad data from traveling farther.

Read the command output from top to bottom. Identify:

1. when the seed loads,
2. when staging views build,
3. when dimensions and the fact build,
4. when tests run, and
5. when the mart becomes eligible to build.

## Explain it back

1. Why did `sources.yml` need `database: AIRBNB`?
2. When should data be a source, a seed, or a model?
3. What does the full moon seed add that cannot be found in `fct_reviews`?
4. Why would the raw Airbnb reviews be a poor seed?
5. Why does a relationships test not replace a `not_null` test?
6. What does a failing singular test return?
7. What additional protection does `dbt build` provide?

## Success Criteria

- Every staging model uses `source()` for `AIRBNB.RAW`.
- The seed exists in `TECHCATALYST.<STUDENTNAME>` and is referenced with `ref()`.
- You can explain the CSV-to-warehouse lifecycle of a seed and identify when a seed is the wrong choice.
- The mart builds and preserves both `day after full moon` and `other day` reviews.
- Eight generic tests and one singular test pass.
- You observed the singular test fail after temporarily removing its cleansing rule.
- `dbt build` completes successfully.
- You can explain source versus seed versus model, and generic versus singular test.

## Hints

<details>
<summary>The source compiles to TECHCATALYST.RAW</summary>

Add `database: AIRBNB` at the same indentation level as `schema: RAW`.

</details>

<details>
<summary>dbt reports a YAML syntax error</summary>

Use spaces, not tabs. Check that each `arguments:` block is nested under its test name.

</details>

<details>
<summary>The singular test still passes after editing the model</summary>

Editing a SQL file does not change the warehouse table. Run the model before rerunning the test.

</details>

## Stretch

1. Add a relationships test from `fct_reviews.listing_id` to `dim_listings_cleansed.listing_id`. If it fails, inspect the invalid keys before deciding whether the data or the assumption should change.
2. Add `not_null` to `fct_reviews.reviewer_name`, then run only tests attached to that model with `dbt test --select fct_reviews`.

# Activity 4: Snapshots, Docs, and Packages (Stretch)

**Module:** Week 5 Day 4  
**Estimated Time:** 55 to 70 minutes, optional  
**Difficulty:** Intermediate to Advanced  
**Format:** Individual, self-paced  
**Prerequisites:** Activity 3 complete, `dbt build` passing

## Objective

Explore three practices used in production dbt projects:

1. snapshots preserve row history,
2. documentation stays beside the code it explains, and
3. packages provide reusable, reviewed macros.

This activity uses only dbt Core commands. It does not require a dbt extension.

## Part 1: Capture history with a snapshot

### The problem snapshots solve

An ordinary table stores the current value. If a listing's minimum stay changes from two nights to five, an overwrite destroys the old value.

A dbt snapshot implements a Type 2 slowly changing dimension. Instead of overwriting history, it stores another version:

| listing_id | minimum_nights | dbt_valid_from | dbt_valid_to |
|---|---:|---|---|
| 101 | 2 | first change time | second change time |
| 101 | 5 | second change time | `NULL` |

`dbt_valid_to IS NULL` means the row is the current version. The closed row answers historical questions such as, "What was the minimum stay when this review was written?"

### Why this lab uses a small seed

The real raw tables are shared. A self-study lab should not depend on an instructor changing shared data at the right moment, so you will simulate a mutable input with a two-row seed in your own schema. The snapshot mechanics are the same as they would be for a mutable source table.

### Step 1: Create the initial input

Create `seeds/snapshot_listings_demo.csv`:

```csv
id,listing_name,minimum_nights,updated_at
101,Capitol View Apartment,2,2026-07-27 09:00:00
102,Riverfront Studio,3,2026-07-27 09:00:00
```

Load it:

```bash
dbt seed --select snapshot_listings_demo --full-refresh
```

### Step 2: Define the snapshot

Create `snapshots/listings_demo_snapshot.yml`:

```yaml
snapshots:
  - name: scd_listings_demo
    relation: ref('snapshot_listings_demo')
    config:
      unique_key: id
      strategy: timestamp
      updated_at: updated_at
      hard_deletes: invalidate
```

Read the configuration before running:

| Setting | Purpose |
|---|---|
| `relation` | The current-state input that dbt will compare |
| `unique_key` | Matches one business entity across runs |
| `strategy: timestamp` | Treats a newer `updated_at` as a changed row |
| `hard_deletes: invalidate` | Closes a version if the input row disappears |

Run the first snapshot:

```bash
dbt snapshot --select scd_listings_demo
```

Inspect it:

```sql
SELECT
    id,
    listing_name,
    minimum_nights,
    dbt_valid_from,
    dbt_valid_to
FROM TECHCATALYST.<STUDENTNAME>.<STUDENTNAME>_SCD_LISTINGS_DEMO
ORDER BY id, dbt_valid_from;
```

**Checkpoint:** two rows exist and both have `dbt_valid_to IS NULL`.

### Step 3: Simulate a source change

Edit only the row for ID 101 in the CSV:

```csv
101,Capitol View Apartment,5,2026-07-27 10:00:00
```

Reload the changed seed, then rerun the snapshot:

```bash
dbt seed --select snapshot_listings_demo --full-refresh
dbt snapshot --select scd_listings_demo
```

Run the same query again.

**Checkpoint:** ID 101 now has two versions. The old version has a non-null `dbt_valid_to`; the five-night version is current. ID 102 still has one version because its values and timestamp did not change.

### What the snapshot did not do

A snapshot sees only the states present when `dbt snapshot` runs. If a value changes three times between snapshot runs, dbt cannot reconstruct the two intermediate states. Production teams schedule snapshots at a frequency that matches the history they need.

## Part 2: Generate documentation from the project

Documentation is most reliable when it is versioned with the model and updated in the same pull request.

Edit the existing `dim_listings_cleansed` entry in `models/schema.yml`. Keep its tests and add the descriptions shown here:

```yaml
models:
  - name: dim_listings_cleansed
    description: >
      One row per Airbnb listing, with minimum stay and price values
      cleaned for analysis.
    columns:
      - name: listing_id
        description: Primary key for a listing.
        data_tests:
          - unique
          - not_null
      - name: minimum_nights
        description: '{{ doc("dim_listings_cleansed__minimum_nights") }}'
```

Do not create a second `dim_listings_cleansed` block. Add these properties to the block you already have.

Create `models/docs.md`:

```markdown
{% docs dim_listings_cleansed__minimum_nights %}
Minimum number of nights required to rent the property.

Some raw listings use 0, which is not a valid stay length.
The cleansing model replaces 0 with 1.
{% enddocs %}
```

Generate the documentation artifacts:

```bash
dbt docs generate
```

Serve the site from one terminal:

```bash
dbt docs serve --port 8080 --no-browser
```

Open `http://localhost:8080` in Chrome. Find `dim_listings_cleansed` and inspect:

1. the model description,
2. the rendered long-form column description,
3. attached tests,
4. compiled SQL, and
5. upstream and downstream lineage.

Press `Ctrl+C` in the terminal when you finish.

**Aha check:** dbt did not need a separate lineage diagram. `source()` and `ref()` already recorded the relationships, so documentation could render the DAG from the project itself.

## Part 3: Reuse a package macro

Packages are dbt projects that expose reusable macros, tests, and sometimes models. They are similar to libraries in a programming language.

Create `packages.yml` beside `dbt_project.yml`:

```yaml
packages:
  - package: dbt-labs/dbt_utils
    version: 1.4.1
```

Install the pinned package:

```bash
dbt deps
```

Pinning makes the project reproducible. A team should review a package and its release notes before upgrading rather than silently accepting future changes.

### Add a surrogate review key

The raw reviews do not provide a single review ID. Use `dbt_utils.generate_surrogate_key` to create a deterministic hash from the columns that identify a review in this dataset.

In `models/fct/fct_reviews.sql`, replace the current `SELECT *` with:

```sql
SELECT
    {{ dbt_utils.generate_surrogate_key([
        'listing_id',
        'review_date',
        'reviewer_name',
        'review_text'
    ]) }} AS review_id,
    *
FROM src_reviews
WHERE review_text IS NOT NULL

{% if is_incremental() %}
  AND review_date > (SELECT MAX(review_date) FROM {{ this }})
{% endif %}
```

The macro call is Jinja. During compilation, dbt replaces it with Snowflake SQL that handles nulls consistently and hashes the selected values.

The model has `on_schema_change='fail'`, and adding `review_id` changes its schema. Rebuild it deliberately:

```bash
dbt run --select fct_reviews --full-refresh
```

Verify the result:

```sql
SELECT
    COUNT(*) AS row_count,
    COUNT(review_id) AS populated_ids,
    COUNT(DISTINCT review_id) AS distinct_ids
FROM TECHCATALYST.<STUDENTNAME>.<STUDENTNAME>_FCT_REVIEWS;
```

**Checkpoint:** all three counts are equal.

A surrogate key does not invent uniqueness. If two source rows contain identical values for every input column, they receive the same hash. Equal counts here confirm that the selected columns identify the reviews in this dataset.

## Explain it back

1. Why does a snapshot create another row instead of updating the old row?
2. What does `dbt_valid_to IS NULL` mean?
3. Why must snapshots run on a schedule?
4. How did dbt know which models to draw upstream of a dimension?
5. Why pin a package version?
6. What guarantee does a surrogate key provide, and what guarantee does it not provide?

## Success Criteria

- The controlled snapshot demo shows two versions for listing 101.
- You can interpret `dbt_valid_from` and `dbt_valid_to`.
- `dbt docs generate` succeeds and the local site shows descriptions, tests, SQL, and lineage.
- `dbt_utils` 1.4.1 installs with `dbt deps`.
- `fct_reviews` rebuilds with a populated, unique `review_id`.
- You can explain snapshots, docs-as-code, packages, and surrogate-key limitations.

## Hints

<details>
<summary>The snapshot still has one version for ID 101</summary>

Confirm that you changed both `minimum_nights` and `updated_at`, reran `dbt seed --full-refresh`, and then reran `dbt snapshot`.

</details>

<details>
<summary>dbt reports a duplicate model entry in schema.yml</summary>

Edit the existing `dim_listings_cleansed` block. Do not paste a second model block with the same name.

</details>

<details>
<summary>The dbt_utils macro is undefined</summary>

Confirm that `packages.yml` is beside `dbt_project.yml`, then run `dbt deps`.

</details>

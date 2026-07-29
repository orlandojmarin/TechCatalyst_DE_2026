# Activity 3 Solution: Sources, Seeds, and Tests

## Task 1: Source declaration

`models/sources.yml`:

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

The `database` property is required. The profile's default database is `TECHCATALYST`, but the raw inputs live in `AIRBNB`.

## Refactored staging models

`models/src/src_listings.sql`:

```sql
WITH raw_listings AS (
    SELECT * FROM {{ source('airbnb', 'listings') }}
)
SELECT
    id AS listing_id,
    name AS listing_name,
    listing_url,
    room_type,
    minimum_nights,
    host_id,
    price AS price_str,
    created_at,
    updated_at
FROM raw_listings
```

`models/src/src_reviews.sql`:

```sql
WITH raw_reviews AS (
    SELECT * FROM {{ source('airbnb', 'reviews') }}
)
SELECT
    listing_id,
    date AS review_date,
    reviewer_name,
    comments AS review_text,
    sentiment AS review_sentiment
FROM raw_reviews
```

`models/src/src_hosts.sql`:

```sql
WITH raw_hosts AS (
    SELECT * FROM {{ source('airbnb', 'hosts') }}
)
SELECT
    id AS host_id,
    name AS host_name,
    is_superhost,
    created_at,
    updated_at
FROM raw_hosts
```

The compiled SQL still points to `AIRBNB.RAW.RAW_LISTINGS`, `AIRBNB.RAW.RAW_REVIEWS`, and `AIRBNB.RAW.RAW_HOSTS`. The behavior is unchanged, but the locations are centralized and the DAG begins at source nodes.

## Tasks 2 through 6: Expected outcomes

- `dbt seed --select seed_full_moon_dates` creates `TECHCATALYST.<STUDENTNAME>.<STUDENTNAME>_SEED_FULL_MOON_DATES`.
- The mart query returns `day after full moon` and `other day` groups.
- `dbt test` runs eight generic tests plus the singular test.
- The singular test fails only while the minimum-night cleansing rule is removed.
- `dbt build` loads the seed, builds selected resources in dependency order, runs tests, and skips downstream work when an upstream failure blocks it.

## Stretch answers

### Relationships from reviews to listings

```yaml
  - name: fct_reviews
    columns:
      - name: listing_id
        data_tests:
          - relationships:
              arguments:
                to: ref('dim_listings_cleansed')
                field: listing_id
```

If it fails, inspect the returned listing IDs. Do not automatically delete the rows or weaken the test. First decide whether the intended contract is wrong, the fact needs a deliberate filter, or the dimension is missing valid listings.

### Reviewer name nullability

```yaml
  - name: fct_reviews
    columns:
      - name: reviewer_name
        data_tests:
          - not_null
```

Run only tests attached to the model:

```bash
dbt test --select fct_reviews
```

A failure creates a business decision. The team must decide whether to preserve anonymous reviews, replace the missing label, filter the rows, or change the claimed contract.

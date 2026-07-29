# Activity 2 Solution: Materializations and Core Models

Task 1 (`dim_listings_cleansed`) and Task 3 (`fct_reviews`) are given in the activity. The solo work is Tasks 2 and 4.

## Task 2: `models/dim/dim_hosts_cleansed.sql`

```sql
WITH src_hosts AS (
    SELECT * FROM {{ ref('src_hosts') }}
)
SELECT
    host_id,
    NVL(host_name, 'Anonymous') AS host_name,
    is_superhost,
    created_at,
    updated_at
FROM src_hosts
```

Verification:

```sql
SELECT COUNT(*)
FROM TECHCATALYST.<STUDENTNAME>.<STUDENTNAME>_DIM_HOSTS_CLEANSED
WHERE host_name IS NULL;
```

The query returns 0.

## Task 4: `models/dim/dim_listings_w_hosts.sql`

```sql
WITH l AS (
    SELECT * FROM {{ ref('dim_listings_cleansed') }}
),
h AS (
    SELECT * FROM {{ ref('dim_hosts_cleansed') }}
)
SELECT
    l.listing_id,
    l.listing_name,
    l.room_type,
    l.minimum_nights,
    l.price,
    l.host_id,
    h.host_name,
    h.is_superhost AS host_is_superhost,
    l.created_at,
    GREATEST(l.updated_at, h.updated_at) AS updated_at
FROM l
LEFT JOIN h ON h.host_id = l.host_id
```

Verification: the two counts match.

```sql
SELECT
  (
    SELECT COUNT(*)
    FROM TECHCATALYST.<STUDENTNAME>.<STUDENTNAME>_DIM_LISTINGS_CLEANSED
  ) AS listings,
  (
    SELECT COUNT(*)
    FROM TECHCATALYST.<STUDENTNAME>.<STUDENTNAME>_DIM_LISTINGS_W_HOSTS
  ) AS joined;
```

`GREATEST` earns its place because the joined row can change when either parent changes. Its `updated_at` should therefore be the later parent timestamp. If either input can be null in a different dataset, use Snowflake's `GREATEST_IGNORE_NULLS` or an explicit null-handling rule.

## Stretch answers

1. A per-model `{{ config(materialized='view') }}` overrides the folder default from `dbt_project.yml`; after the run, Snowsight shows the object flipped from table to view. Config precedence: in-model config beats folder config beats project default.
2. In the compiled `fct_reviews`, `{{ this }}` renders to `TECHCATALYST.<STUDENTNAME>.<STUDENTNAME>_FCT_REVIEWS`. It must be the physical, aliased name because the incremental filter queries the already materialized table. Using `ref('fct_reviews')` would create a self-reference in the DAG.

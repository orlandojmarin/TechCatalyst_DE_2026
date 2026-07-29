# Activity 4 Solution: Snapshots, Docs, and Packages

## Snapshot files

Initial `seeds/snapshot_listings_demo.csv`:

```csv
id,listing_name,minimum_nights,updated_at
101,Capitol View Apartment,2,2026-07-27 09:00:00
102,Riverfront Studio,3,2026-07-27 09:00:00
```

`snapshots/listings_demo_snapshot.yml`:

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

Updated row:

```csv
101,Capitol View Apartment,5,2026-07-27 10:00:00
```

After the second seed and snapshot run, listing 101 has two versions:

| ID | Minimum nights | Valid to |
|---|---:|---|
| 101 | 2 | Non-null timestamp |
| 101 | 5 | `NULL` |

Listing 102 still has one current version.

## Documentation result

`dbt docs generate` produces the catalog and manifest used by the local documentation site. The model page should show descriptions from `schema.yml` and `docs.md`, attached tests, compiled SQL, and lineage built from `source()` and `ref()`.

## Package result

`packages.yml`:

```yaml
packages:
  - package: dbt-labs/dbt_utils
    version: 1.4.1
```

The updated `fct_reviews` projection:

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

Verification:

```sql
SELECT
    COUNT(*) AS row_count,
    COUNT(review_id) AS populated_ids,
    COUNT(DISTINCT review_id) AS distinct_ids
FROM TECHCATALYST.<STUDENTNAME>.<STUDENTNAME>_FCT_REVIEWS;
```

Equal counts show that the chosen input columns identify reviews uniquely in this dataset. The macro generates a deterministic key, but it cannot make duplicate source records logically unique.

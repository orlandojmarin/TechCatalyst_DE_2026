# Activity 1 Solution: First Models

Tasks 1 and 2 are given in the activity. The solo work is Task 3.

## Task 3: `models/src/src_hosts.sql`

```sql
WITH raw_hosts AS (
    SELECT * FROM AIRBNB.RAW.RAW_HOSTS
)
SELECT
    id AS host_id,
    name AS host_name,
    is_superhost,
    created_at,
    updated_at
FROM raw_hosts
```

Run and verify:

```bash
dbt run --select src_hosts
```

```sql
SELECT host_id, host_name
FROM TECHCATALYST.<STUDENTNAME>.<STUDENTNAME>_SRC_HOSTS
LIMIT 5;
```

## Task 4 notes

`target/compiled/airbnb/models/src/src_hosts.sql` contains the rendered `SELECT`. `target/run/airbnb/models/src/src_hosts.sql` wraps it in the DDL dbt executed, including `CREATE OR REPLACE VIEW TECHCATALYST.<STUDENTNAME>.<STUDENTNAME>_SRC_HOSTS AS (...)`. This is where you can see the alias macro's effect on the physical object name.

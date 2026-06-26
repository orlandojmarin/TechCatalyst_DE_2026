# Day 4 Stretch Worksheet: Query Files in Place with Athena (AWS Mirror)

## Part 1: Land the File in S3

**Bucket:** techcatalyst-de-2026-orlando-aws
**Prefixes created:**
- taxi_zones/
- athena-results/

**File uploaded:** taxi_zone_lookup.csv → s3://techcatalyst-de-2026-orlando-aws/taxi_zones/

---

## Part 2: Point Athena at It

**Database created:**

```sql
CREATE DATABASE IF NOT EXISTS techcatalyst_orlando;
```

**External table DDL:**

```sql
CREATE EXTERNAL TABLE IF NOT EXISTS taxi_zones (
  LocationID INT,
  Borough STRING,
  Zone STRING,
  service_zone STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES ('separatorChar' = ',', 'quoteChar' = '"')
LOCATION 's3://techcatalyst-de-2026-orlando-aws/taxi_zones/'
TBLPROPERTIES ('skip.header.line.count' = '1');
```

**Q1:** Nothing got "loaded" anywhere. What does `EXTERNAL` + `LOCATION` mean about where the data lives versus where the table definition lives?

> Answer:

---

## Part 3: Query + the Cost Meter

**Query 1:**

```sql
SELECT Borough, COUNT(*) AS zones
FROM taxi_zones
GROUP BY Borough
ORDER BY zones DESC;
```

**Q2:** How many zones per borough? How much data was scanned?

> Answer:

**Query 2:**

```sql
SELECT * FROM taxi_zones;
```

**Q3:** Did `SELECT *` scan more than the grouped query? What's the one-sentence rule about scanning columns you don't need?

> Answer:

---

## Q4 (the multicloud point)

In one or two sentences, state the idea BigQuery and Athena share, and one way they differ.

> Answer:

---

## Success Criteria

- [ ] CSV uploaded to its own `taxi_zones/` prefix in S3
- [ ] Athena query-result location set to a separate prefix
- [ ] `taxi_zones` external table created (no data copied)
- [ ] Both queries ran; recorded the Data scanned figure
- [ ] Q1 to Q4 answered

# Day 4 Lab Worksheet: Query Files in Place with BigQuery

## Concept Checkpoint

1. Where is the data? ______
2. What file format is it? ______
3. How are columns identified and typed? ______
4. Is there a header row to skip? ______

---

## Part 1: Inspect the Stored CSV

1. Delimiter: ______
2. Header present? ______
3. Predicted types for the three columns: ______
4. What could go wrong if a later file contains `unknown` in `fare_amount`? ______

---

## Part 2: Review or Create the External Table

**Before running:** What do the three options control, and what omitted DDL element causes schema autodetection?

> Answer:

**After running:** Record the schema shown by BigQuery.

| Column | BigQuery type | Does it match your prediction? |
| :--- | :--- | :--- |
| `PULocationID` | | |
| `fare_amount` | | |
| `trip_date` | | |

---

## Part 3: Run the Supplied Queries

### Query A: Preview Rows

**Predict:** Does `LIMIT 10` mean BigQuery can stop scanning a row-oriented CSV after exactly ten rows? Why or why not?

> Prediction:

**Results:**

- Result schema observation (column names and types): ______
- Estimated bytes before Run: ______
- Bytes processed after Run: ______
- One external-CSV limitation revealed or relevant to this query: ______

### Query B: Aggregate by Date

**Predict:** What data must BigQuery read to calculate the count and total for every date?

> Prediction:

**Results:**

- Date with the greatest `total_fare`: ______
- Result schema observation (column names and types): ______
- Estimated bytes before Run: ______
- Bytes processed after Run: ______
- One external-CSV limitation revealed or relevant to this query: ______

---

## Part 4: Compare the Scan Signal and Limitations

| Observation | Query A | Query B |
| :--- | :--- | :--- |
| Rows returned | | |
| Bytes processed | | |
| Did fewer output rows guarantee fewer input bytes? | | |

Which limitation would matter most for a repeated production workload, and why?

> Answer:

---

## Part 5: External or Loaded Curated Table?

1. A new partner CSV needs a one-time quality check: **external / loaded**, because ______
2. A daily executive dashboard needs predictable performance and stable fields: **external / loaded**, because ______

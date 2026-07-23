# Student Resources: SQL, PySpark, and Delta Lake

AI assistance is allowed with review required. Use these links to verify behavior and explain concepts, not to replace your own reasoning.

## Core Documentation

| Resource | Why it helps | Checked |
|---|---|---|
| [Databricks Free Edition](https://docs.databricks.com/aws/en/getting-started/free-edition) | Current Free Edition capabilities and setup | 2026-07-22 |
| [Free Edition limitations](https://docs.databricks.com/aws/en/getting-started/free-edition-limitations) | Serverless, quotas, and unsupported features | 2026-07-22 |
| [Sample datasets](https://docs.databricks.com/aws/en/discover/databricks-datasets) | Official built-in sample schemas | 2026-07-22 |
| [SQL parameter markers](https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-parameter-marker) | Safe values passed from Python or widgets into SQL | 2026-07-22 |
| [PySpark DataFrame reference](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/dataframe.html) | DataFrame methods used in activities | 2026-07-22 |
| [Notebook code and magic commands](https://docs.databricks.com/aws/en/notebooks/notebooks-code) | `%sql`, `%fs`, `%run`, and notebook behavior | 2026-07-22 |
| [Databricks utilities](https://docs.databricks.com/aws/en/dev-tools/databricks-utils) | Widgets, filesystem utilities, and task values | 2026-07-22 |
| [Delta Lake tables](https://docs.databricks.com/aws/en/delta/) | Delta concepts and operations | 2026-07-22 |

## SQL to PySpark Quick Map

| SQL | PySpark |
|---|---|
| `SELECT a, b` | `.select("a", "b")` |
| `WHERE x > 0` | `.filter(F.col("x") > 0)` |
| `GROUP BY` | `.groupBy(...).agg(...)` |
| `ORDER BY` | `.orderBy(...)` |
| `CASE WHEN` | `F.when(...).otherwise(...)` |
| `QUALIFY` | Add a window column, then `.filter(...)` |
| `DESCRIBE HISTORY table_name` | `DeltaTable.forName(spark, table_name).history()` |
| `table_name VERSION AS OF 3` | `spark.read.option("versionAsOf", 3).table(table_name)` |

## Lab Deliverable Checklist

| Done | Deliverable |
|---|---|
| [ ] | Notebook 01 bridge activity passes validation |
| [ ] | Notebook 02 PySpark activity passes validation |
| [ ] | Notebook 03 SQL and PySpark time-travel results agree |
| [ ] | `taxi_dropoff_activity` exists as managed Delta |
| [ ] | Notebooks exported to `student-work/week5/day2/` |

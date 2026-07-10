# Student Resources: AWS Glue Visual ETL Lab

> [!WARNING]
> **AI-Free Zone (Weeks 1 to 4).** Do not use AI assistants to complete this lab. Today's lab is drag and drop, so there is nothing to generate anyway. Read the docs below when you get stuck.

## Core Documentation

| Resource | Why it is useful |
|---|---|
| [AWS Glue Studio: Visual job authoring](https://docs.aws.amazon.com/glue/latest/ug/edit-nodes-chapter.html) | The reference for every node type on the canvas: sources, transforms, targets. |
| [Using files in Amazon S3 as the data source](https://docs.aws.amazon.com/glue/latest/dg/edit-jobs-source-s3-files.html) | Explains the S3 direct source, Infer schema, and the CSV options (delimiter, quote character) you set in this lab. |
| [Editing Glue transform nodes](https://docs.aws.amazon.com/glue/latest/ug/transforms-configure.html) | Details on Change Schema, Filter, Join, and Custom Transform, including the DynamicFrameCollection behavior. |
| [AWS Glue versions and release notes](https://docs.aws.amazon.com/glue/latest/dg/release-notes.html) | What Glue 5.x runs under the hood (Spark 3.5, Python 3.11) and why the version dropdown matters. |
| [AWS Glue job parameters and worker types](https://docs.aws.amazon.com/glue/latest/dg/add-job.html) | What G.1X means and how workers, retries, and timeouts affect cost. |
| [Data preview in Glue Studio](https://docs.aws.amazon.com/glue/latest/ug/data-preview.html) | How preview sessions work, why they need an IAM role, and how they bill. |
| [What is a medallion architecture? (Databricks glossary)](https://www.databricks.com/glossary/medallion-architecture) | Vendor-neutral enough to be the standard explainer for Bronze, Silver, Gold. |
| [NYC TLC Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) | The source dataset, including the data dictionary for the yellow trip columns. |

## Key Concepts

### Bronze vs Silver in one rule

If reproducing a downstream table would require going back to the original source system, your Bronze layer failed its job. Bronze exists so that everything after it can be rebuilt from inside your own lake.

### DynamicFrame vs DataFrame

Glue's native structure is the **DynamicFrame**: like a Spark DataFrame, but each record carries its own schema, which tolerates messy semi-structured data. The Custom Transform snippet in the lab converts to a DataFrame (`toDF()`) to use `na.drop()`, then converts back. You will meet DataFrames properly in Week 5 PySpark.

### Why the generated script matters

The visual canvas is a projection of a real PySpark script. Teams check that script into version control, diff it in code review, and sometimes eject from the canvas entirely when a job outgrows it. A visual tool you cannot inspect is a liability; one that generates readable code is leverage.

## Lab Deliverable Checklist

| Done | Deliverable |
|---|---|
| [ ] | Bronze ingest job `<username>_bronze_ingest` succeeded (screenshot of run and of `bronze/` objects) |
| [ ] | Silver transform job `<username>_silver_transform` succeeded (screenshot of run and of `silver/` Parquet) |
| [ ] | `student-work/week3/day5/glue_lab_notes.md`: one node-to-generated-code observation |
| [ ] | Same file: two or three sentences on what belongs in Bronze vs Silver and why |
| [ ] | No extra job re-runs left billing; job editor tabs closed |

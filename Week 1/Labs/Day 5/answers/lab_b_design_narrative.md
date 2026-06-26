# Lab B Phase 3: Design Narrative — NYC Taxi Demand Forecasting Pipeline

## Walkthrough

Data starts at the NYC TLC website, where Yellow Taxi trip records are published monthly as Parquet files. An AWS Lambda function (triggered by Step Functions on a monthly schedule) downloads the new file and lands it in S3 bronze alongside the static Taxi Zone Lookup CSV. Nothing is transformed at this point, it's just raw data as-landed.

From bronze, a Glue job picks up the raw Parquet, validates it (checking for nulls, schema mismatches, row counts), joins it with the zone lookup table to attach borough and zone names to each LocationID, and writes the cleaned result to S3 silver as Parquet. Records that fail validation get routed to a quarantine prefix so we can investigate later without blocking the pipeline. This quality gate exists because our business requirement depends on accurate zone-level counts, so garbage in means bad forecasts out.

A second Glue job reads from silver and aggregates trips by zone and hour, producing the gold-layer metrics that feed our demand forecasting. These aggregated results load into Redshift, where analysts can run heavier queries and where the forecasting model pulls its training data. For lighter ad-hoc exploration, analysts can also query silver directly via Athena without spinning up Redshift.

Forecast results (predicted demand by zone/hour) get written to DynamoDB for fast key-value lookups. Fleet ops managers hit a QuickSight dashboard connected to Redshift for heatmaps, or their operational tools call an API Gateway + Lambda endpoint that reads from DynamoDB.

Orchestration runs through Step Functions with EventBridge triggering the monthly pipeline. If a Glue job fails, Step Functions retries it and sends an SNS alert. CloudWatch monitors row counts between layers so we catch data quality drops early.

## Key Design Decisions

**Is this primarily ETL, ELT, or hybrid, and why?**
ELT. We land raw Parquet in S3 first (the "load"), then transform in place with Glue (the "transform"). This makes sense because the data already arrives in a columnar format, so there's no need to transform before storing it.

**Which component is OLTP, OLAP, object storage, or specialized storage?**
- S3 (bronze, silver) = object store
- Redshift = warehouse/OLAP
- DynamoDB = key-value store (for fast forecast lookups)
- Athena = serverless query engine (queries object storage directly, not a store itself)

**What does the orchestrator do that the pipeline itself does not?**
Step Functions handles scheduling (when to run), dependency ordering (bronze must finish before silver starts), retry logic (if a Glue job fails), and alerting (SNS notification on failure). The pipeline components themselves just do their specific job without knowing about the bigger picture.

**Is there any Reverse ETL path? If not, name one future operational destination that could use curated outputs.**
Not currently. One future path: push forecasted demand predictions back into a driver-facing mobile app so drivers can see where demand will be highest in the next hour and reposition themselves.

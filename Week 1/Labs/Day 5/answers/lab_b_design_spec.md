# Lab B Phase 1: Design Spec — NYC Taxi Demand Forecasting Pipeline

## 1a. Business and Stakeholder Requirements

**Business requirement:** Forecast taxi demand by zone and time of day so drivers can be positioned where riders will need them most during peak periods.

**Stakeholders and consumers:**
- Fleet operations managers — use forecasts to recommend driver positioning and shift scheduling
- Data analysts — explore historical demand patterns and evaluate forecast accuracy
- A demand forecasting model — consumes cleaned trip data to predict future demand by zone/hour
- A dashboard — displays real-time and forecasted demand heatmaps by zone

---

## 1b. System Requirements

### Functional (the WHAT)

| Functional | Your answer |
| :--- | :--- |
| Data sources and formats | NYC TLC Yellow Taxi Trip Records (Parquet, monthly, millions of rows), Taxi Zone Lookup Table (CSV, static reference data mapping LocationID to borough/zone) |
| Data-store families needed | Object store (S3 for the data lake), warehouse/OLAP (Redshift or Athena for analytics queries), key-value (DynamoDB for serving forecast results) |
| Storage and zones | S3 with medallion layers: bronze (raw Parquet as-landed), silver (cleaned/validated trips joined with zone lookup), gold (aggregated demand metrics by zone/hour) |
| Pipeline pattern (ETL, ELT, or hybrid) | ELT — land the raw Parquet in S3 first, then transform in place using Glue/Athena since the data arrives already in a columnar format |
| Querying and access | Athena for ad-hoc analysis on the lake, Redshift for heavier analytical workloads and forecast model training data |
| Visualization or serving | QuickSight dashboard for demand heatmaps, API Gateway + Lambda + DynamoDB for serving forecast results to operations tools |
| Real-time or batch | Batch — trip records are published monthly with a two-month lag, so real-time isn't applicable for the source data. Forecasts would be regenerated on a scheduled basis (daily or weekly) |

### Non-functional (the HOW WELL)

| Non-functional | Your answer |
| :--- | :--- |
| Scalability (volume now and at 10x) | Current: millions of rows per month for one taxi type. At 10x: adding green taxi, FHV, and HVFHV datasets. S3 and Athena scale horizontally without provisioning, so the architecture handles this without redesign. |
| Reliability and availability | Orchestrator (Step Functions) retries failed jobs. S3 versioning on the bronze layer for recovery. Idempotent transforms so reruns don't produce duplicates. |
| Security and PII handling | Pickup/dropoff locations at the zone level (not exact coordinates) reduce PII risk. No passenger names in the dataset. IAM policies restrict access per layer. Encrypt S3 at rest (SSE-S3). |
| Observability (how you know it works) | CloudWatch for Glue job metrics and failures. Row-count checks between layers (bronze count vs silver count after filtering). Alerts via SNS if a monthly load fails or data quality drops below threshold. |

---

## 1c. Data Spec

| Spec field | Value |
| :--- | :--- |
| Sources | NYC TLC Yellow Taxi Trip Records (Parquet, monthly), Taxi Zone Lookup Table (CSV, static) |
| Grain (one row is...) | One taxi trip (pickup to dropoff) |
| Freshness (per consumer) | Analysts: monthly (as TLC publishes). Dashboard/model: refreshed within 24 hours of new data landing. |
| Key metrics or outputs | Trip count by zone and hour, average trip duration by zone, peak demand windows, forecasted demand by zone/hour |
| Sensitive fields | Pickup/dropoff location IDs (low risk since they're zone-level, not exact addresses). No PII like names or payment card numbers in the dataset. |
| Top 2 cost drivers | 1. Glue/Athena compute for transformations and queries (billed per data scanned). 2. S3 storage across three medallion layers (raw + cleaned + aggregated). |

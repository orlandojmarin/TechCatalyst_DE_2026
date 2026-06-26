# Lab A: Read a Reference Architecture

## Part 1: Pick a Reference Architecture

**Title:** Amazon OpenSearch Trending Queries with AWS Glue and Amazon Bedrock
**URL:** https://d1.awsstatic.com/architecture-diagrams/ArchitectureDiagrams/amazon-opensearch-trending-queries-with-glue-and-amazon-bedrock.pdf

---

## Part 2: Read It Like an Engineer

| Question | Your answer |
| :--- | :--- |
| What business problem does this architecture solve? | Identifying the top trending search queries so the business can optimize content strategy, improve user experience, and potentially increase revenue. |
| What are the zones, left to right (ingest, store, transform, serve)? | Ingest: steps 1-5 (user queries flow through API Gateway → OpenSearch → Kinesis → Firehose → Lambda compress → lands in S3). Store: S3 at three stages (raw logs after step 5, Parquet after step 8, clustered output after step 10), plus Glue Catalog (crawlers at steps 7, 9, 11). Transform: steps 8, 10, 12, 13 (Glue consolidation to Parquet, K-means clustering, Athena top-N query, Bedrock classification). Serve: steps 14-15 (DynamoDB → Lambda → API Gateway back to the search page and business analysts). Orchestration: step 6 (EventBridge daily scheduler triggers Step Functions to coordinate the batch workflow). |
| Name the services in each zone | Ingest (steps 1-5): Amazon OpenSearch, API Gateway, Kinesis Data Streams, Data Firehose, Lambda (compress). Store: S3 (three stages: raw, Parquet, clustered), Glue Catalog (crawlers at steps 7, 9, 11). Transform (steps 8, 10, 12, 13): AWS Glue jobs (steps 8, 10), Athena (step 12), Lambda, Bedrock (step 13). Serve (steps 14-15): DynamoDB, Lambda, API Gateway. Orchestration (step 6): EventBridge, Step Functions. |
| Where does data quality get checked (if shown)? | Not explicitly shown as a quality gate. The Glue consolidation step (step 8, raw → Parquet) is where bad data would likely get caught or filtered out, and the crawlers (steps 7, 9, 11) enforce schema via the catalog. |
| Where is sensitive data or access control handled (if shown)? | Not explicitly called out in the diagram. Access control would be handled by IAM policies on the services, but the architecture doesn't show specific PII handling or encryption. |
| What looks like the top cost driver? | Probably the AWS Glue jobs (steps 8 and 10, running daily transforms on all the query logs) and the Amazon Bedrock invocations (step 13, LLM calls to classify each cluster). |
| Is it batch, streaming, or both? | Both. Streaming: steps 1-5, query logs flow through Kinesis in near-real-time (buffered every 15 min by Firehose). Batch: step 6 onward, a daily EventBridge scheduler triggers Step Functions which kicks off the Glue jobs, clustering, and Bedrock classification. |

---

## Part 3: Map It to Medallion

**Bronze (raw, as-landed):** Raw compressed query logs in S3 (output from steps 4-5, Firehose/Lambda, before any transformation).

**Silver (cleaned, conformed):** Consolidated Parquet files in S3 (after step 8, the Glue consolidation job transforms and structures the raw logs).

**Gold (business-ready):** Clustered and classified trending queries stored in DynamoDB (output of steps 10-13, K-means clustering + Bedrock classification), ready to be served to users and analysts.

**Where would a malformed file go?** The architecture doesn't explicitly show a quarantine path. I would add a dead-letter or quarantine prefix in S3 where the Glue consolidation job could route malformed records instead of dropping them silently.

**Q:** Does this architecture follow medallion thinking, a different layering, or no clear layering?

> Answer: It follows medallion thinking, with data clearly moving through raw (S3 logs) → cleaned/structured (Parquet in S3) → business-ready (classified trending queries in DynamoDB), even though it doesn't explicitly label the layers as bronze/silver/gold.

---

## Part 4: Steal One Idea

**One design choice to reuse in Lab B:** The S3 layering pattern (raw logs → Parquet → final output) with Glue crawlers cataloging each stage. This keeps data organized and queryable at every step.

**One choice to change for the taxi use case, and why:** I wouldn't need the Bedrock/LLM classification step. The taxi pipeline doesn't need AI to categorize results; instead I'd use that transform stage for data quality checks and aggregations (like trip counts by zone or time).

---

## Success Criteria

- [x] Chose one GCP or AWS data-analytics reference architecture (title + URL recorded)
- [x] Identified zones, flow, and services
- [x] Located quality, PII, and cost (or noted where they are missing)
- [x] Mapped it to bronze, silver, gold
- [x] Named one idea to reuse and one to change

# Presentation Script: From PoC to Production

**Total time: ~8 minutes (split across 3 presenters)**

---

## Presenter 1: The Problem and Why Pandas Breaks (~2.5 min)

### Slide 1: Title (15 seconds)

"Good morning. Our team was asked to take the accident-data proof of concept we built last week, the pandas ETL to Snowflake pipeline, and design a production architecture that handles real-world scale. Here is what we propose."

### Slide 2: The Business Problem (45 seconds)

"Let us start with what changed. Our PoC handled one CSV file. Production handles 2,400 CSV files every single day from three different sources: telematics devices, our claims intake system, and partner insurers. We are looking at hundreds of terabytes of history, and all three sources need to be integrated, joined on policy and incident keys, deduplicated, and standardized into one schema. On top of that, the VP wants today's data showing up instantly on the claims dashboard."

### Slide 3: Challenge 1 - The Pandas Ceiling (60 seconds)

"So why can't we just run our PoC 2,400 times? Let's do the math. Our PoC took about 2 minutes per file for 463,000 rows. Multiply that by 2,400 files and you get 80 hours of processing on a single machine. That is more than three days to process one day's data. We would never catch up.

But it is not just time. Pandas loads the entire dataset into memory, typically using 2x to 5x the file size in RAM. A 2 GB file might need 10 GB of RAM. And even if each individual file is small enough, you still have an orchestration nightmare: tracking 2,400 successes, retrying failures, and managing partial completions.

The class of tool that solves this is distributed processing, specifically Apache Spark. It partitions data across a cluster and processes files in parallel with built-in fault tolerance."

---

## Presenter 2: Architecture Decisions (~3 min)

### Slide 4: Challenge 2 - Where Processing Runs (50 seconds)

"We chose AWS Glue, which is managed Spark, for our processing engine. Three reasons. First, it is serverless: we do not provision or manage clusters, and it scales automatically to our daily peak. Second, our data already lives in S3, and Glue has native integration. Third, we literally built a Glue Visual ETL pipeline in Week 3 for the NYC Taxi data, so we know the tool works for medallion architectures.

We rejected on-premise because of procurement time, patching burden, and the inability to scale elastically. And since we already pay for Snowflake, we push the final integration work, the joins and deduplication, into Snowflake SQL rather than doing everything in Spark."

### Slide 5: Challenge 3 - When It Breaks at 3 AM (60 seconds)

"Our architecture uses the medallion pattern with three layers. Bronze in S3 stores raw files exactly as they landed, immutable and replayable. Silver, also in S3 as Parquet, holds the cleaned, typed, and standardized data. Gold in Snowflake holds the integrated, business-ready tables.

Here is why layers matter. Say a partner insurer sends corrupted files on Tuesday and we discover it Thursday. With layers, we quarantine the bad files, reprocess just those dates from Bronze through Silver, and reload into Gold. Without layers, we would have to rebuild everything from the original source, potentially days of work.

Schema changes from one source get absorbed at the Silver layer. The mapping logic updates there, and Bronze and Gold remain stable.

For idempotency, Snowflake's COPY INTO command tracks which files have already been loaded. If our pipeline dies halfway through and we rerun it, the files already loaded get skipped automatically. No duplicates."

### Slide 6: Challenge 4 - Where Layers Live (50 seconds)

"Layer placement is a cost decision. Bronze and Silver live in S3 at roughly 2.3 cents per GB per month. For hundreds of terabytes, that is significantly cheaper than Snowflake storage. Plus, Bronze is an archive; we do not need a query engine on raw CSV files.

Gold lives in Snowflake as permanent tables because the dashboard needs sub-second query response, and permanent tables give us full Time Travel and Fail-safe recovery.

The bridge between S3 and Snowflake is an external stage with a storage integration. No AWS keys in our code, and COPY INTO handles the bulk load."

---

## Presenter 3: Performance, Sizing, and Risks (~2.5 min)

### Slide 7: Challenge 5 - I Only Want Today (45 seconds)

"The VP wants today's data instantly. A plain SQL view does not help because it still scans the entire history table on every query. Our solution is a small transient table called CLAIMS_TODAY that the pipeline truncates and rebuilds each morning. It holds only one day of data, so queries are fast and storage is minimal.

For historical queries, we cluster the main table on claim_date. Snowflake's micro-partition pruning means a date filter skips all irrelevant data physically. And with 200 opens per day by 40 people, Snowflake's result cache means repeated identical queries cost zero additional compute."

### Slide 8: Sizing and Estimates (60 seconds)

"Here are our numbers. The build is a 7-week effort in four phases: harden the PoC and build the Glue pipeline in weeks one and two, build integration logic in weeks three and four, backfill hundreds of terabytes of history in weeks five and six at roughly 2 TB per hour with 10 Glue workers, and cutover in week seven.

The smallest viable team is two data engineers. Ideally we add a platform engineer for infrastructure and an analyst liaison for validation.

Monthly run costs: S3 storage dominates at roughly $5,000 per month for 200 TB, controlled by lifecycle policies that move old Bronze data to Glacier. Glue compute runs about $1,200 per month, controlled by worker count. Snowflake compute is roughly $2,000 per month, controlled by auto-suspend and warehouse size."

### Slide 9: Top Three Risks (45 seconds)

"Risk one: partner file quality degrades silently. Our mitigation is the data contract gate between Bronze and Silver, with schema checks, row-count thresholds, and automatic quarantine.

Risk two: the historical backfill takes longer than estimated and blocks our go-live. We mitigate by running backfill as a separate high-parallelism job, processing in date-range chunks so we can validate incrementally.

Risk three: Snowflake costs spike during peak analyst usage. We mitigate with auto-suspend after 60 seconds idle, resource monitors with dollar alerts, and a separate warehouse for ETL loads versus dashboard reads."

### Slide 10: Decision Summary (15 seconds)

"To summarize our five decisions: Spark for parallelism, Glue plus Snowflake for processing, medallion layers for recovery, S3 for cheap bulk storage with Snowflake for serving, and a daily-rebuilt Gold table for instant dashboard response."

### Slide 11: Architecture Diagram (15 seconds)

"This diagram shows the end-to-end flow. Every arrow is labeled with what moves, in what format, and at what cadence. The data contract gate and quarantine path ensure we catch problems before they reach the business."

### Slide 12: Questions (transition)

"We are happy to take questions. We expect at least one 'why not just...' per challenge, so bring them on."

---

## Anticipated Q&A Prep

| Likely question | Prepared answer |
|---|---|
| "Why not do everything in Snowflake?" | Snowflake can ingest from S3 directly, but Spark (Glue) gives us fine-grained cleaning logic (regex, custom Python) that SQL handles awkwardly. We use each tool where it is strongest. |
| "Why not Databricks instead of Glue?" | Databricks is excellent but adds a separate vendor relationship and cost. Glue is native to AWS where our S3 already lives, and the managed Spark is sufficient for CSV-to-Parquet ETL. |
| "80 hours is a rough estimate. What if files are small?" | Fair point. If files average 50 MB, pandas per-file might work, but you still need orchestration (Airflow/Glue Workflows) to track 2,400 jobs, retry failures, and avoid duplicates. Spark solves both the compute and orchestration problem. |
| "Why transient for CLAIMS_TODAY instead of a view?" | A view re-scans on every read. With 200 daily opens, that is 200 full scans. A pre-built transient table is scanned zero times at read (result cache), costs less to store (no Fail-safe), and is trivially cheap to rebuild once per day. |
| "What about real-time streaming?" | The brief says files land daily in batches. If the business later wants sub-minute freshness, Snowpipe (auto-ingest on S3 event notification) is the next step. Our architecture supports it because Bronze is already in S3. |

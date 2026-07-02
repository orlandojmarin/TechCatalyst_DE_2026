# TechCatalyst DE 2026 — Curriculum Mapping (Validated June 2026)

8 weeks, Mon–Fri, June 22 – August 14, 2026. ~10 students, group-based delivery.

> [!IMPORTANT]
> **Holiday:** July 4, 2026 falls on a Saturday → observed **Friday, July 3 (Week 2, Day 5)**.
> Adjustment: Data Architecture (originally W2D1) moves to W1D5 so Week 2 fits in 4 days.

---

## Platform Verification Notes (as of June 2026)

| Platform | What changed / what to teach |
| :--- | :--- |
| **GCP DE** | **Knowledge Catalog** is the current governance catalog name. BigQuery began restricting Legacy SQL availability after June 1, 2026, so teach GoogleSQL only. **BigQuery Data Engineering Agent** now GA (natural-language pipeline building), a useful Week 6 demo. Dataflow lineage in Knowledge Catalog is GA. |
| **GCP AI** | Vertex AI rebranded **Gemini Enterprise Agent Platform**; use the unified **google-genai SDK**. Current models: Gemini 2.5 family (stable) and 3.x. Gemini callable from BigQuery SQL (`ML.GENERATE_TEXT` / AI functions), a DE-native GenAI pattern. |
| **AWS DE** | Story is now **SageMaker Lakehouse + S3 Tables (managed Iceberg) + Glue** (auto Iceberg optimization, Glue Data Quality). EMR still valid for the Spark deployment day; mention S3 Tables when teaching Iceberg. |
| **Snowflake** | **dbt Projects on Snowflake** runs dbt natively (incl. Fusion engine) — show after local dbt. **Openflow** (managed NiFi) = ingestion story, mention conceptually. Cortex: **AISQL functions** (COMPLETE, CLASSIFY, SUMMARIZE…), Cortex Code → **CoCo**, Snowflake Intelligence → **CoWork**. Use current naming in slides. |
| **dbt** | **Fusion engine** (Rust, 30x faster parse) + official **VS Code extension** (requires Fusion, free). Teach dbt with Fusion + VS Code; concepts identical to Core. |
| **Databricks** | Use **Databricks Free Edition** (serverless). No cluster profile management; Delta Lake, notebooks, SQL, basic Unity Catalog all work. Jobs/pipelines now branded **Lakeflow**. Certifications are explicitly out of scope for this cohort. |

---

## Week × Day Mapping

| Week | Theme | Day 1 | Day 2 | Day 3 | Day 4 | Day 5 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1** (Jun 22-26) | Data & Cloud Foundations | Data primer, DE roles, batch vs streaming, modern data stack | Cloud fundamentals: IaaS/PaaS/SaaS, GCP vs AWS, IAM, billing + **guided BigQuery Sandbox preview** (Citi Bike public data; copy/paste SQL; bytes-processed cost model) | Developer foundations: VS Code, Linux terminal, Python envs (venv/pip context plus uv), Git/GitHub deep dive through push/pull/clone/fetch | Data at rest: storage architectures (lake/lakehouse/warehouse/mart), storage-compute separation, formats & lifecycle. Labs: secure GCS landing zone (console + CLI) + query-in-place with a BigQuery external table + team NYC-Taxi storage design; S3 comparison | Think like an architect: requirements to data spec; pipeline vocabulary + ETL/ELT/Reverse ETL; **data architectures** (batch/streaming, Lambda/Kappa, Medallion); architecture diagramming (Draw.io); read a reference architecture + team pipeline design (deliverable) + pipeline thread kickoff (NYC Taxi) |
| **2** (Jun 29-Jul 2, 4 days) | Developer Foundations, AI-Free Zone | Linux CLI, shell, cron + Git collaboration (branch, PR, conflicts) | Python foundations: types, collections, control flow, functions | Intermediate Python: OOP, error handling, file I/O, `requests` API calls | Python drills plus pandas review and drills; medallion ETL mini-capstone deferred to Week 3 Day 1 | *July 3 holiday* |
| **3** (Jul 6-10) | Review, Modern Warehousing & SQL (GCP-first) | Terminal review, Python review/drills, pandas review/drills, then deferred medallion ETL mini-capstone | BigQuery architecture: storage/compute, partitioning, clustering | SQL by hand on BigQuery: JOINs, GROUP BY, HAVING | Ingestion: Pub/Sub, Beam concepts, Dataflow batch (GCS to BQ) | Orchestration (Cloud Composer DAGs) + governance: IAM, **Knowledge Catalog**, PII masking in BQ |
| **4** (Jul 13–17) | Snowflake, dbt & Advanced SQL | Snowflake architecture, virtual warehouses, RBAC, cost optimization | Advanced SQL: window functions, CTEs, tuning (BQ + Snowflake) | dbt fundamentals with **Fusion + VS Code ext**: sources, models, tests; demo **dbt Projects on Snowflake** | Advanced dbt: incremental models, snapshots + **GitHub Actions CI/CD** | Snowflake **Cortex AISQL** enrichment lab + masking policies & tagging |
| **5** (Jul 20–24) | Big Data & PySpark | Distributed computing, Spark architecture (driver/executors), DataFrames | **Databricks Free Edition**: notebooks, PySpark transforms | Advanced PySpark + **Delta Lake & Apache Iceberg** (ACID, time travel, schema evolution; mention S3 Tables) | Production deploy: package script → **GCP Dataproc** job | Secondary cloud: **AWS EMR** job + Dataproc Serverless overview |
| **6** (Jul 27–31) | GenAI & AI-Assisted Engineering | GenAI foundations: LLMs, tokens, embeddings, prompt engineering | Programmatic LLMs: **google-genai SDK**, REST, LangChain concepts | Vertex AI / **Gemini Enterprise Agent Platform**: DE's role in ML, AutoML, feature pipelines | Applied NLP: Gemini classification lab + **BigQuery AI functions** in SQL | **GitHub Copilot** for DE: agent mode, context engineering, code review discipline + BQ Data Engineering Agent demo |
| **7** (Aug 3–7) | BI, Visualization & Data Apps | Data storytelling + **Streamlit** app on BQ/Snowflake | **Tableau** (primary BI tool) | **ThoughtSpot** (AI search analytics) | Comparative BI architecture: semantic layers, caching, access control + **Looker** intro (optional/time-permitting) | **Capstone kickoff**: brief, teams, dataset reveal, EDA |
| **8** (Aug 10–14) | **100% Capstone Sprint** (no new instruction) | Architecture finalization + roles (stand-ups begin) | Ingestion sprint (GCS → PySpark/Dataflow → BQ/Snowflake) | Transformation & governance sprint (Snowflake, dbt, PII, Knowledge Catalog) | AI enrichment (Cortex/Gemini) + Tableau dashboard or Streamlit app | **Final presentations** + retrospective |

**Capstone:** reuse the proven NYC Taxi (2024/2025) capstone, re-platformed: RAW zone in GCS (+S3 secondary), PySpark/Dataflow transforms, Snowflake + dbt modeling, Cortex/Gemini enrichment, BI/Streamlit delivery.

---

## Key concepts coverage check

Solution architecture (W1D5, W7D4, W8) · SQL mastery (W3-W4) · Python/Pandas/Polars (W2, W3D1 review) · PySpark (W5) · Lakehouse, Delta, Iceberg, Medallion (W1D5, W3D1, W5D3) · ELT/ETL (W3D1 mini-capstone) · Data quality & PII (W3D5, W4D4-W4D5, W8D3) · Incremental processing (W4D4) · Star vs snowflake, OLAP vs OLTP (W3) · Spark SQL (W5) · Jobs & orchestration (W3D5, W5D4) · Governance (W3D5, W4D5) · Performance optimization (W3D2, W4D2, W5)

# TechCatalyst Data Engineering Capstone 2026

**Teams:** 3 teams of 3
**Sprint:** Monday August 10 to Friday August 14
**Everything due:** Friday August 14
**Demo Day:** Wednesday August 19, 20 minutes plus 5 minutes of questions

---

## The mission

![Four yellow Taxis lined behind each other](images/yellow-cab.png)

You are a three person data consultancy. A client has handed you two and a half years' worth of New York City taxi trip records sitting in a raw S3 bucket, and a vague brief: "there is something useful in here, find it."

Your job is to build a working data platform on top of that raw data, use it to answer a question that matters, and convince a room of technical and business people that your answer is correct.

You choose the question. You choose the architecture. You defend both.

## Lab Index

### Provided files

| File | What it is |
| :--- | :--- |
| `README.md` | This brief |
| `Data_Catalog.md` | Bucket paths, schemas, the 2025 schema change, and known data traps |
| `Reference_Architecture.md` | The two approved pipeline patterns and a diagram template |
| `Milestones.md` | Day by day checkpoints for the sprint |
| `Rubric.md` | How you are graded, in detail |
| `Presentation_Guide.md` | Structure and expectations for Demo Day |
| `Team_Charter_Template.md` | Roles, git workflow, and decision log template |
| `Data_Quality_Report_Template.md` | Template for the required incident report |
| `starter/snowflake_connect.py` | Connection helper covering all three Snowflake Python paths |
| `starter/snow.cfg.template` | Credentials file template, copy to `snow.cfg` and never commit it |
| `starter/load_raw_from_s3.sql` | Stage, `INFER_SCHEMA`, and `COPY INTO` for the raw files |
| `starter/dbt_project_skeleton/` | A dbt Core project wired to Snowflake, with a starting staging model |
| `starter/bigquery_load_snippet.py` | Reference code for the optional BigQuery destination |

### Deliverables

| # | Deliverable | Required |
| :--- | :--- | :--- |
| 1 | Working pipeline from S3 RAW to Snowflake gold models | Yes |
| 2 | dbt Core project with staging models, mart models, and tests | Yes |
| 3 | Data Quality Incident Report | Yes |
| 4 | At least one defended 2025 vs 2026 year-over-year finding | Yes |
| 5 | Dashboard in Tableau or Looker | Yes |
| 6 | Architecture diagram of what you actually built | Yes |
| 7 | Cost and performance rationale | Yes |
| 8 | GitHub repository with a README that lets someone else re-run your work | Yes |
| 9 | AI use disclosure | Yes |
| 10 | Future state proposal with effort estimate | Yes |
| 11 | Demo Day presentation, every member speaking | Yes |
| 12 | Streamlit app, Databricks lane, BigQuery destination / BQ ML, AI enrichment | Optional |

---

## The data

Yellow and Green taxi trip records, January to May 2025 and January to May 2026. 20 files total (10 Yellow, 10 Green), over 30 million rows.

Full paths, schemas, and the things that will bite you are in `Data_Catalog.md`. **Read it before you write any code.** It documents a schema change that occurred in 2025 and several data defects we already know are in there.

You may bring in additional public data. NYC Open Data is the natural source, and weather data is a popular enrichment. This is encouraged but not required, and it is worth nothing if the core pipeline is weak.

## The required spine

Every team must deliver this, regardless of which architecture you choose:

```
S3 RAW  ->  [ your ingestion and transformation ]  ->  Snowflake  ->  dbt models  ->  Tableau or Looker
```

**Snowflake is the graded destination.** dbt Core runs against Snowflake. You may add BigQuery as a second destination if you want to, but it does not replace Snowflake.

Beyond that, the design is yours. `Reference_Architecture.md` describes two patterns that we know work end to end. Pick one, adapt it, or propose your own, but be ready to explain why.

## Choose your analytical question

Do not start with the tools. Start with a question you actually want answered, then build the thing that answers it.

Good questions are specific, answerable with this data, and have a "so what" a business person would care about. Some starting points, though you are strongly encouraged to invent your own:

- How did trip demand and fares shift between January-May 2025 and January-May 2026, and which zones changed the most?
- Where and when does the gap between Yellow and Green service leave neighborhoods underserved?
- Which pickup and dropoff patterns predict an unusually slow trip, and what would that be worth to a dispatcher?
- What does tipping behavior reveal about payment type, trip length, and time of day, and did it change year over year?
- Which zones show the largest change in congestion-related charges, and what does that suggest?

Be adventurous. Try tools you have not used. A team that reaches for something unfamiliar and reports honestly on how it went will score better than a team that plays it safe and produces something obvious.

## What we are looking for beyond working code

Three requirements exist because they are what separates an engineer people trust from one they do not.

### 1. The Data Quality Incident Report

This data is dirty in ways that will silently corrupt your analysis. Find the problems. Quantify them. Decide what to do, and write down why.

For each defect you find, record:

| Field | Meaning |
| :--- | :--- |
| What | The defect, described precisely |
| Scale | How many records, and what percentage |
| Impact | Which of your metrics it would distort, and in which direction |
| Decision | Drop, correct, quarantine, or keep with a caveat |
| Why | Your reasoning, including what you gave up |

Finding a problem and silently deleting the rows is not an acceptable answer. Neither is finding nothing. `Data_Catalog.md` names several defects to get you started; there are more that it does not name.

### 2. A defended year-over-year finding

You have two comparable five month periods (January to May 2025 versus January to May 2026). Produce at least one claim of the form "X changed by Y between 2025 and 2026," and be ready to defend it.

Defending it means you can answer:
- Is the comparison fair? Same months, same vehicle types, same filters?
- Could a data quality problem explain the difference instead?
- Is the change large enough to be real, or is it noise?

A confident claim that collapses under the first question is worse than a cautious one that holds.

### 3. Cost and performance rationale

You are not reporting a bill. You are explaining your engineering judgment. Address:

- Which table types you used and why (transient versus permanent, and what you traded away)
- Warehouse sizing and auto-suspend settings
- How you handled file sizing and formats on load
- Your dbt materialization choices (view, table, or incremental) and the reasoning per model
- What you would change if this data were ten times larger

## Tooling notes, read these before you plan

**Databricks Free Edition cannot connect to your S3 bucket or to Snowflake.** Free Edition is serverless only, does not support custom storage locations or storage credentials, and restricts outbound network access to a limited set of trusted domains. Do not architect a pipeline that depends on Databricks moving data in or out.

If you want to demonstrate PySpark, Delta Lake, or Lakeflow, use the **optional Databricks lane**: manually upload a subset of the data to a Unity Catalog volume, do your work there, and present it as a scale or orchestration proof of concept. That is a legitimate and welcome extension. It is just not a link in your main pipeline.

**Orchestration** means a re-runnable script. A clean Python driver that executes your pipeline end to end is a complete answer. We did not teach Airflow or Cloud Composer, and neither is expected.

**AI assistance is allowed.** You must disclose where you used it and what you verified yourself. Code you cannot explain in the Q&A will be treated as code you did not write.

## Working agreements

- All work goes in your team's GitHub repository, not in this course repo.
- Every team member commits code. We will look at the commit history.
- Fill in `Team_Charter_Template.md` on Monday morning and keep the decision log current.
- Ask for help early. A team stuck for three hours on a connection string has wasted a quarter of a sprint day.

---

## Sprint at a glance

| Stage | Focus |
| :--- | :--- |
| 1 | Charter, question selection, architecture decision, first data landing |
| 2 | Ingestion and transformation to Snowflake |
| 3 | dbt models, then the **Architecture Defense** |
| 4 | Analysis, dashboard, and presentation build |
| 5 | Delivery: everything due Friday August 14 |
| 6 | **Demo Day**, Wednesday August 19 |

Detail and checkpoints are in `Milestones.md`.

Good luck. Build something you would be willing to put your name on.

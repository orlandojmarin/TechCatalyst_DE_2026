# Reference Architecture

Two patterns are described here. Both work end to end. Both are defensible. Pick one, adapt it, or design your own and justify it.

What you may not do is skip the decision. At the Architecture Defense you will be asked why you built it the way you did, and "it is what we tried first" is not an answer.

---

## The fixed points

Whatever you choose, these are non-negotiable:

| Stage | Requirement |
| :--- | :--- |
| Landing | S3 RAW bucket, read only, provided to you |
| Warehouse | Snowflake, the graded destination |
| Transformation to gold | dbt Core, running against Snowflake |
| Delivery | Tableau or Looker |

Everything between landing and warehouse is your call.

---

## Pattern A: ELT, warehouse-centric

```
S3 RAW (parquet)
   |
   |  external stage + COPY INTO
   v
Snowflake BRONZE          raw landing tables, minimal typing
   |
   |  dbt
   v
Snowflake SILVER          cleaned, conformed, unioned, typed
   |
   |  dbt
   v
Snowflake GOLD            marts serving your analytical question
   |
   v
Tableau / Looker
```

**How it works.** Point a Snowflake external stage at the RAW bucket, use `INFER_SCHEMA` to read the Parquet layout, and `COPY INTO` bronze tables. Everything after that is SQL, run and tested by dbt.

**Choose this if** you want the most reliable path, your team is strongest in SQL, or you want to spend your time on modeling and analysis rather than on plumbing.

**Strengths.** Fewest moving parts, fewest places to fail. Snowflake ingests Parquet efficiently, so 30 million rows is not a challenge. dbt owns every transformation, which means every transformation is tested, documented, and version controlled. Easy to re-run from scratch.

**Weaknesses.** You do very little outside the warehouse, so it demonstrates less breadth. All compute is Snowflake credits. Cleaning very messy data in SQL is sometimes clumsier than doing it in a DataFrame.

**Skills it demonstrates.** Snowflake stages and loading (Week 4), dbt modeling and testing (Week 5), advanced SQL (Weeks 3 to 5).

---

## Pattern B: ETL, engine-side transform

```
S3 RAW (parquet)
   |
   |  pandas / Polars / PySpark / AWS Glue
   v
S3 CONFORMED (parquet)    cleaned, unioned, partitioned, your own prefix
   |
   |  external stage + COPY INTO
   v
Snowflake SILVER
   |
   |  dbt
   v
Snowflake GOLD
   |
   v
Tableau / Looker
```

**How it works.** Read the raw Parquet with a DataFrame engine, do your cleaning and conforming there, write partitioned Parquet back to your own S3 prefix, then load that into Snowflake and model the gold layer with dbt.

**Choose this if** you want to show DataFrame and file-format skill, your cleaning logic is genuinely awkward in SQL, or you want a story about processing efficiency.

**Strengths.** Demonstrates more of the curriculum. Keeps heavy row-level cleaning off warehouse credits. Produces a reusable conformed zone that other consumers could read directly. Gives you a real story about partitioning and file sizing.

**Weaknesses.** More moving parts and more failure modes. You must handle memory: 30 million rows will not fit comfortably in pandas at once on your VM, so you will be reading file by file, using Polars lazy scanning, or using Glue. Two places where transformation logic can live means it can drift.

**Engine notes.**

- **Polars** with `scan_parquet` and lazy evaluation handles this volume well on a single machine. Probably your best local option.
- **pandas** works if you process one month at a time and concatenate results, not if you load everything at once.
- **AWS Glue** has native S3 access and scales without you managing anything. The safest choice if you want distributed processing in your actual pipeline.
- **PySpark locally** works but is fiddly to set up for the payoff.

**Skills it demonstrates.** DataFrame engines (Weeks 2, 3, 5), AWS Glue (Week 3), file formats and partitioning (Week 1), plus everything Pattern A shows downstream.

---

## Optional lanes

These add to your score if they work and are honestly presented. None of them substitutes for the required spine.

### Databricks lane

**Read this before planning around it.** Databricks Free Edition is serverless only, does not support custom workspace storage locations or storage credentials, restricts outbound network access to a limited set of trusted domains, and allows one active pipeline per pipeline type. **It cannot read your S3 bucket and it cannot write to Snowflake.**

What you can do: upload a subset of files to a Unity Catalog volume through the workspace UI, then build a medallion pipeline in Delta Lake with PySpark, and orchestrate it with Lakeflow Jobs. Present it as a proof of concept for how the pipeline would run at scale on a paid tier.

That is a genuinely valuable contribution and we will score it. Just do not make your required deliverables depend on it.

### BigQuery as a second destination

Load your conformed data into BigQuery alongside Snowflake using the BigQuery Python client, and compare the two platforms on load time, query performance, cost model, and developer experience. `starter/bigquery_load_snippet.py` gives you the loading code so you are not spending sprint time on API mechanics.

A real comparison with numbers behind it is a strong presentation section.

### Streamlit application

Build an interactive app on top of your Snowflake gold models. This does not replace the Tableau or Looker dashboard, it complements it, and it is the clearest way to differentiate your team's deliverable.

### AI enrichment

Options you have the background for: BigQuery ML for a forecast or clustering model, an LLM to classify or summarize something in your data, Cloud Vision or Cloud Natural Language if you bring in a source that suits them, or a retrieval-augmented layer over the taxi documentation.

Apply this to a real question. AI bolted onto the end because it was available is transparent and scores poorly.

### Orchestration

A single re-runnable Python script that executes your pipeline end to end and can recover from a partial failure satisfies this. Make it idempotent: running it twice should not double your data.

---

## Your architecture diagram

You must submit a diagram of what you **actually built**, not what you planned on Monday. Draw.io is what you used in Week 1 and is the expected tool.

It should show:

- Every storage location, with the actual bucket paths and database or schema names
- Every processing step, labeled with the tool that runs it
- The direction of data flow
- Where transformation logic lives
- Your orchestration entry point

A reader who has never seen your project should be able to look at the diagram and know where to go to re-run it.

Include a second diagram for your future state proposal, showing what you would build next and roughly what it would cost in effort.

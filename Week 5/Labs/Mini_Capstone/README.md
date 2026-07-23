# Week 5 Mini-Capstone: The Million Song Lakehouse

**Format:** Teams of about three  
**Introduced:** Day 3  
**Presented:** Day 5, every team member presents  
**Platform:** Databricks Free Edition with serverless compute

AI assistance is allowed with review required. Your team must run, inspect, and explain every submitted line.

## Why This Project

Sparkify has song metadata and listening logs. The files are useful, but analysts should not build every report directly from JSON. Your team will turn the source records into a small, reliable lakehouse with Delta tables and a dimensional model.

This is a learning project, not a production rebuild of Spotify. Keep the design small and the code readable. A direct query is better than a complicated query that produces the same answer.

By the end, your team will be able to:

1. Explain why thousands of tiny files can be slow even when the total data size is small.
2. Translate a source data dictionary into SQL DDL.
3. Use `COPY INTO` to load Bronze Delta tables and PySpark to build Silver tables.
4. Choose SQL or PySpark for team-owned Gold transformations and explain the choice.
5. Publish an analyst-facing SQL view that joins the fact to all four dimensions without changing the fact grain.
6. Validate row counts, keys, joins, and layer reconciliation.
7. Run the build and validation notebooks as a Lakeflow Job.
8. Present an architecture diagram, an entity relationship diagram (ERD), and evidence-based findings.

## The Data Story

The project uses the Udacity subset of the Million Song project.

| Source | Rows | What one row represents |
|---|---:|---|
| `songs_compact.jsonl` | 14,896 | One song metadata record |
| `logs_compact.jsonl` | 8,056 | One application event |
| Listening events | 6,820 | One log event where `page = 'NextSong'` and the user is known |

The original song layout contains 14,896 tiny JSON files totaling only about 3.7 MB. Reading them one by one from remote storage spends more time listing and opening files than processing data. The provided compact file contains the same records and retains the original relative filename in `_source_file`.

That is an important engineering lesson: use Spark for distributed processing, but do not confuse many files with a large dataset.

## Source Data Dictionary

The JSONL files are the Landing layer. Each line is one JSON object. Your team will use these contracts to create the Bronze Delta tables with SQL DDL.

### `songs_compact.jsonl`

| Column | SQL type | Meaning |
|---|---|---|
| `_source_file` | `STRING` | Original relative JSON filename |
| `artist_id` | `STRING` | Source artist identifier |
| `artist_latitude` | `DOUBLE` | Artist-location latitude, when known |
| `artist_location` | `STRING` | Artist location text |
| `artist_longitude` | `DOUBLE` | Artist-location longitude, when known |
| `artist_name` | `STRING` | Artist name |
| `duration` | `DOUBLE` | Song duration in seconds |
| `num_songs` | `BIGINT` | Number of songs represented by the source record |
| `song_id` | `STRING` | Source song identifier |
| `title` | `STRING` | Song title |
| `year` | `BIGINT` | Release year, with `0` meaning unknown |

### `logs_compact.jsonl`

| Column | SQL type | Meaning |
|---|---|---|
| `_source_file` | `STRING` | Original relative JSON filename |
| `artist` | `STRING` | Artist name reported by the listening event |
| `auth` | `STRING` | Authentication state |
| `firstName` | `STRING` | User first name |
| `gender` | `STRING` | User gender code |
| `itemInSession` | `BIGINT` | Event position within the session |
| `lastName` | `STRING` | User last name |
| `length` | `DOUBLE` | Track length reported by the event |
| `level` | `STRING` | Subscription level |
| `location` | `STRING` | User location |
| `method` | `STRING` | HTTP method recorded by the application |
| `page` | `STRING` | Application event type, such as `NextSong` |
| `registration` | `DOUBLE` | Registration timestamp in Unix milliseconds |
| `sessionId` | `BIGINT` | Session identifier |
| `song` | `STRING` | Song title reported by the event |
| `status` | `BIGINT` | HTTP status code |
| `ts` | `BIGINT` | Event timestamp in Unix milliseconds |
| `userAgent` | `STRING` | Browser or client user-agent string |
| `userId` | `STRING` | User identifier, which can be empty |

The schema is part of the pipeline contract. Do not use schema inference for the graded build.

Some source song titles and artist names contain only digits and are encoded as JSON numbers. They are still names, so the contract deliberately declares `title` and `artist_name` as `STRING`. This is one reason an explicit schema is safer than relying on inference.

## Before You Start

Complete this project in Databricks through Chrome. You do not need the virtual machine or a local Python environment.

You will briefly download the provided course files through Chrome so you can import the notebooks and upload the data to Databricks.

| Location | What belongs there |
|---|---|
| Chrome Downloads | Temporary copies of the provided notebooks and JSONL files |
| Databricks Workspace | The three imported notebooks that your team edits and runs |
| `/Volumes/workspace/<team_schema>/landing/` | The two JSONL files that Databricks reads |

### 1. Download the provided files

Use the course repository or instructor-provided course link in Chrome to download:

```text
Week 5/Labs/Day 2/00_Shared_Setup.py
Week 5/Labs/Mini_Capstone/Mini_Capstone_Starter.py
Week 5/Labs/Mini_Capstone/Validate_Mini_Capstone_Starter.py
Week 5/Labs/Mini_Capstone/data/songs_compact.jsonl
Week 5/Labs/Mini_Capstone/data/logs_compact.jsonl
```

### 2. Import the notebooks into Databricks

Create one Databricks Workspace folder for your team. Import:

1. `00_Shared_Setup.py`
2. `Mini_Capstone_Starter.py`
3. `Validate_Mini_Capstone_Starter.py`

Keep all three notebooks in the same Workspace folder so `%run ./00_Shared_Setup` works.

### 3. Create the team schema and landing volume

Run `00_Shared_Setup`. For the schema widget, use a shared team name such as:

```text
w5_team_orange
```

The setup notebook creates:

- `workspace.<team_schema>` for your Delta tables
- `workspace.<team_schema>.landing` for the source files

### 4. Upload the compact data

In Databricks, open **Catalog** in the left navigation. Navigate to:

```text
workspace > <team_schema> > Volumes > landing
```

Select **Add data**, then **Upload files to this volume**. Upload these files from Chrome Downloads:

```text
songs_compact.jsonl
logs_compact.jsonl
```

The Databricks destination is:

```text
/Volumes/workspace/<team_schema>/landing/
```

Return to the starter notebook and run the source check. Do not continue until both files are visible.

## The Learning Journey

| Sequence | Stage | What your team learns and produces |
|---:|---|---|
| 1 | Contract and ingest | Translate the data dictionary into SQL DDL and load Bronze with `COPY INTO`. |
| 2 | SQL first | Confirm the load, then profile pages, users, years, nulls, and candidate keys. |
| 3 | Design gate | Draw the architecture and ERD before building tables. |
| 4 | Silver | Clean song records and listening events without changing their declared grains. |
| 5 | Gold | Build four dimensions, one songplay fact table, and one analyst-facing view. |
| 6 | Validate | Run executable checks for counts, keys, nulls, and join multiplication. |
| 7 | Operate | Create a two-task Lakeflow Job: build, then validate. |
| 8 | Analyze | Answer at least two business questions from the Gold model. |
| 9 | Communicate | Present both findings, the visualization, and the defended design. |

## Layer and Naming Contract

| Layer | Required objects | Responsibility |
|---|---|---|
| Landing | JSON Lines files in the team volume | Files delivered to the project |
| Bronze | `bronze_songs`, `bronze_logs` | Source-shaped Delta loaded with explicit SQL DDL and `COPY INTO` |
| Silver | `silver_song_catalog`, `silver_listen_events` | Clean, typed, analysis-ready records |
| Gold | `gold_dim_song`, `gold_dim_artist`, `gold_dim_user`, `gold_dim_time`, `gold_fact_songplay` | Dimensional model for analysts |
| Analyst view | `gold_songplay_analysis_vw` | Virtual, flattened interface that joins the fact to all four dimensions while preserving one row per listening event |

Do not use `raw_*` or `stage_*` names. `stage` already means something different in Snowflake, and identical Silver and Gold copies do not add value.

Do not partition these tables. They are far too small for manual partitioning to help.

## SQL and PySpark Choice

This project uses both interfaces, but it does not ask you to build the same pipeline twice.

| Work | Interface rule |
|---|---|
| Bronze DDL, `COPY INTO`, and profiling | Use SQL. |
| Silver | Use the provided PySpark scaffold. This section practices the Week 5 DataFrame skills. |
| Worked time dimension | Use the provided SQL example. |
| Remaining Gold tables | Choose SQL or PySpark for each table. |
| Analyst view and business questions | Use SQL. |

For a team-owned Gold table, choose the interface that makes the transformation easiest to read, test, and maintain. The starter gives the table contract and validation checkpoints, not a completed PySpark transformation.

Keep only one final implementation of each table. All table names, columns, grains, row counts, and validation requirements stay the same regardless of the interface.

Do not claim that SQL or PySpark is always faster. Both can produce Spark execution plans. Defend the choice using the actual work, such as readability, the type of transformation, your team's ability to maintain it, and how easily you could validate it.

## Design Gate: Think Before You Build

Complete this gate after profiling Bronze and before building Silver and Gold.

### Architecture diagram

Draw a simple left-to-right diagram that includes:

- course data files
- the team Unity Catalog volume
- Bronze, Silver, and Gold Delta tables
- the `gold_songplay_analysis_vw` analyst-facing view
- the build notebook and validation notebook
- the Lakeflow Job dependency
- SQL queries and the final visualization

Use any browser-based diagram tool or presentation software available to your team.

Add one sentence under the diagram explaining where each layer begins and ends.

### Gold ERD

Draw an ERD containing:

- `gold_dim_song`
- `gold_dim_artist`
- `gold_dim_user`
- `gold_dim_time`
- `gold_fact_songplay`

For every table, label:

- its grain
- its primary key
- its foreign keys
- whether a fact relationship can be missing

The song metadata is a subset, so some listening events may not match a song or artist. Your ERD should show those two relationships as optional.

### Two short decision records

Write one paragraph answering:

> Why does the project use compact source files for the main build instead of asking every team to read 14,896 remote JSON files?

Then start an implementation choice record:

| Gold table | SQL or PySpark | Why this is the clearest choice |
|---|---|---|
| Example: `gold_dim_artist` | PySpark | The aggregation follows directly from the DataFrame used in the previous section. |

Replace the example with at least one choice your team made. You will defend that choice in the presentation.

## Team Roles

Use these roles to start, then review one another's work:

| Role | First responsibility |
|---|---|
| Ingestion and performance | Source checks, SQL DDL, `COPY INTO`, Bronze, and the small-file explanation |
| Modeling | Silver transformations, Gold dimensions, fact grain, and ERD |
| Quality and operations | Assertions, reconciliation, Lakeflow Job, and run evidence |

Everyone must understand the complete pipeline. Every member presents at least one design or implementation decision.

## Required Validation

`Validate_Mini_Capstone_Starter.py` is not another data-loading notebook. It reads the tables created by the build notebook and checks whether they meet the project contracts.

The starter is intentionally incomplete. Replace every `TODO`, implement each assertion, and remove each `NotImplementedError`. Run it only after the build notebook has created all required tables. In the Lakeflow Job, it becomes the second task so a broken contract stops the workflow after the build.

Your validation notebook must fail clearly when a contract is broken. At minimum, check:

1. Bronze contains 14,896 songs and 8,056 logs.
2. Silver contains 6,820 eligible listening events.
3. Gold dimension primary keys are unique and not null.
4. Gold fact rows equal Silver listening-event rows.
5. The fact join did not multiply listening events.
6. `user_id` and `time_id` are never null and always exist in their dimensions.
7. The percentage of facts matched to song metadata is calculated and reported.
8. `gold_songplay_analysis_vw` contains 6,820 rows and 6,820 distinct `songplay_id` values.

## Lakeflow Job

Create one job with two notebook tasks:

1. `build_million_song_lakehouse`: your completed build notebook
2. `validate_million_song_lakehouse`: your completed validation notebook, dependent on the build task

Add one job parameter named `user_schema` and set it to your team schema, such as `w5_team_orange`. Both notebook tasks must use that same value.

Run the job successfully. Then make one validation expectation incorrect, run the job again, observe the failed validation task, repair it, and run green once more.

The purpose is to prove that validation protects the published model. Two clear tasks teach that lesson without unnecessary orchestration.

## Analyst Questions

Answer at least two business questions with SQL. These are the findings your team will present, not optional practice queries.

First create `gold_songplay_analysis_vw` by joining the fact table to all four dimensions. The view must keep the fact grain: one row per eligible listening event. Use inner joins for the required user and time relationships. Use left joins for song and artist because the available metadata is incomplete.

Select and alias columns explicitly. Do not use `SELECT *`. In particular, name the fact's subscription level `event_level` and the user dimension's latest level `current_user_level` so analysts can tell them apart.

Use the completed view for both business questions. Save both queries in the build notebook and include both answers in the final presentation.

Choose questions that the available data can answer honestly. Examples include:

- At what hours do known users listen most often?
- How does listening activity differ between free and paid users?
- Which locations produce the most listening events?
- What percentage of listening events match the available song catalog?

Create at least one visualization that supports one of the two findings. Give it a useful title, label the measures, and state the finding in one sentence.

## Presentation

Present for 15 minutes:

1. the business problem and source-file challenge
2. the architecture diagram
3. the Gold ERD, table grains, and analyst-view grain
4. one SQL-first profiling result
5. one PySpark transformation and one Gold SQL or PySpark choice, including why it fit and what trade-off you considered
6. the Lakeflow Job and validation evidence
7. at least two business findings, including the supporting visualization
8. one improvement you would make with more time

### Evidence to show in the presentation

Include the following evidence in the presentation:

- the Lakeflow Job task graph
- the successful build and validation run
- the intentionally failed validation run
- the repaired green run
- one useful validation result, such as row reconciliation or match coverage
- both business findings and the analyst visualization

Do not submit these screenshots or evidence items as separate files. The presentation is the evidence package.

## What Your Team Submits

Submit these five deliverables:

1. the final presentation as PowerPoint or PDF
2. the completed build notebook exported from Databricks as a source `.py` file
3. the completed validation notebook exported from Databricks as a source `.py` file
4. the architecture diagram as an image or PDF
5. the Gold ERD as an image or PDF

Include the architecture diagram and ERD in the presentation as well as submitting their exported files.

To export each notebook, open it in Databricks and select **File > Export > Source file**. You do not need to submit the setup notebook, JSONL files, separate SQL files, visualization files, or a separate evidence packet.

## Mini Lesson: Stable IDs for Repeatable Pipelines

The fact table needs one `songplay_id` for each listening event. That ID should still identify the same event when the pipeline runs again.

`monotonically_increasing_id()` can generate unique numbers during one Spark execution, but the numbers depend on Spark partitions. A later run can divide or order the data differently, so the same source event can receive a different number. That makes the ID unsuitable for a repeatable fact-table key.

A deterministic hash solves a different problem. It converts the same identifying field values into the same fixed-length result every time.

Here is a generic example for an event dataset:

```python
from pyspark.sql import functions as F

stable_event_id = F.sha2(
    F.concat_ws(
        "||",
        F.coalesce(F.col("event_timestamp").cast("string"), F.lit("<null>")),
        F.coalesce(F.col("customer_id").cast("string"), F.lit("<null>")),
        F.coalesce(F.col("session_id").cast("string"), F.lit("<null>")),
    ),
    256,
)

events_with_id = events.withColumn("event_id", stable_event_id)
```

Read the expression from the inside out:

1. `cast("string")` gives every input a consistent representation.
2. `coalesce(..., F.lit("<null>"))` gives missing values an explicit marker.
3. `concat_ws("||", ...)` combines the identifying fields in a fixed order.
4. `sha2(..., 256)` produces a SHA-256 hexadecimal string.

The hash is only as good as the fields you choose. If two source rows have the same selected values, they receive the same hash. The hash does not repair duplicate source events, and it is not encryption. It gives the pipeline a compact, repeatable fingerprint for the selected fields.

For the songplay fact, ask:

> Which source fields together identify one listening event and remain the same after a rerun?

## Hints

<details>
<summary>How should we create a repeatable fact key?</summary>

Follow the stable-ID lesson above. Use the event timestamp, user, session, song, artist, and length in a fixed order. Cast values to strings, handle nulls explicitly, join the values with a separator, and pass the result to `sha2(..., 256)`.

After building the fact table, rerun the build and confirm that the same events receive the same IDs. Also confirm that `songplay_id` is not null and that its distinct count equals the fact row count.
</details>

<details>
<summary>How should we select the current user record?</summary>

Use `row_number()` over a window partitioned by `userId` and ordered by `ts` descending. Build it from all valid log events, not only `NextSong` events.
</details>

<details>
<summary>How should we protect the fact grain?</summary>

State the fact grain before joining. Count rows before and after the join. A left join preserves unmatched listening events, but it does not protect you from duplicate song matches.
</details>

## Stretch Goals

- Implement one Gold dimension in SQL and PySpark, compare readability, and keep only the clearer version.
- Add a `gold_hourly_listening` aggregate for a dashboard.
- Add table and column comments in Catalog Explorer.
- Explain how you would ingest new daily log files incrementally without implementing the full production design.

## Lab Index

### Provided Files

| File | Purpose |
|---|---|
| `README.md` | Project brief, sequence, deliverables, and success criteria |
| `Student_Resources.md` | Current official documentation and concise examples |
| `Week 5/Labs/Day 2/00_Shared_Setup.py` | Creates the team schema, landing volume, and shared notebook variables |
| `Mini_Capstone_Starter.py` | Guided source orientation followed by team implementation checkpoints |
| `Validate_Mini_Capstone_Starter.py` | Starter for the executable quality gate |
| `data/songs_compact.jsonl` | 14,896 song records with original source filenames |
| `data/logs_compact.jsonl` | 8,056 application events with original source filenames |

These are the only course files students need to complete the project.

Source background: [Million Song Dataset official site](https://millionsongdataset.com/). The course files are the song and Sparkify log subset distributed for the Udacity data engineering project.

### Deliverables

| Deliverable | What it contains |
|---|---|
| Presentation | Diagrams, design decisions, run evidence, validation evidence, at least two business findings, an analyst visualization, and every team member's explanation |
| Exported build notebook | Completed Bronze, Silver, Gold, analyst-facing view, and at least two business-question queries |
| Exported validation notebook | Completed executable checks |
| Architecture diagram | Source, volume, layers, notebooks, job, and analyst surface |
| Gold ERD | Table grains, primary keys, foreign keys, and optional relationships |

The job screenshots, validation screenshots, SQL queries, and visualization do not need separate submissions. They belong in the presentation or exported notebooks.

## Success Criteria

- A new team member can read the notebook and understand why each section exists.
- Every table and view has a declared grain and clear responsibility.
- The analyst-facing view joins all four dimensions and preserves 6,820 distinct fact rows.
- The solution uses simple SQL and PySpark rather than unnecessary abstractions.
- The team can explain one Gold SQL or PySpark choice without claiming that one interface is always faster.
- The presentation includes at least two findings supported by the team's saved SQL queries.
- A clean run rebuilds the tables without manual table edits.
- Validation stops the job when a contract is broken.
- The team can explain why compacting the source helped without claiming that pandas replaces Spark.
- The architecture diagram, ERD, code, and presentation use the same table names.

## Currentness Check

| Topic | Official source checked | Date checked | Content decision |
|---|---|---|---|
| Databricks Free Edition | [Free Edition limitations](https://docs.databricks.com/aws/en/getting-started/free-edition-limitations) | 2026-07-22 | Use serverless notebooks, managed tables, volumes, SQL, and a two-task job |
| Volume file upload | [Work with files in Unity Catalog volumes](https://docs.databricks.com/aws/en/volumes/volume-files) | 2026-07-22 | Upload the two compact files through Catalog Explorer |
| Bronze ingestion | [`COPY INTO` with Unity Catalog volumes](https://docs.databricks.com/aws/en/ingestion/cloud-object-storage/copy-into/unity-catalog) | 2026-07-23 | Translate the data dictionary into explicit Delta DDL, then load each JSONL file from the team volume |
| Analyst view | [Create and manage views](https://docs.databricks.com/aws/en/views/create-views) and [`CREATE VIEW`](https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-syntax-ddl-create-view) | 2026-07-23 | Create a persistent Unity Catalog view with explicit columns over the Gold star schema |
| Job parameters | [Configure job parameters](https://docs.databricks.com/aws/en/jobs/job-parameters) and [Notebook tasks](https://docs.databricks.com/aws/en/jobs/tasks/notebook) | 2026-07-23 | Use one `user_schema` job parameter, which is pushed to both notebook tasks and read through the setup widget |
| Table layout | [When to partition tables](https://docs.databricks.com/aws/en/tables/partitions) | 2026-07-22 | Do not partition the small project tables |
| Stable identifiers | [Spark `monotonically_increasing_id`](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.monotonically_increasing_id.html) and [`sha2`](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.sha2.html) | 2026-07-23 | Teach why partition-dependent IDs are not repeatable and use a deterministic SHA-256 fingerprint |
| Notebook export | [Import and export Databricks notebooks](https://docs.databricks.com/aws/en/notebooks/notebook-export-import) | 2026-07-23 | Submit the completed build and validation notebooks as source `.py` files |

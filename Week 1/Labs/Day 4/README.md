# Week 1 · Day 4: Lab

**Theme:** Data at Rest (object storage, layout, lifecycle, protection, and query-in-place)
**Format:** Two required hands-on labs plus a team design activity, with optional AWS and compliance extensions

> [!IMPORTANT]
> **Before you start:** confirm with your instructor that your course project, billing, and Storage/BigQuery roles are active, and that you can sign in to the **Google Cloud Console** (Cloud Shell is only needed for the optional CLI steps). If any check fails, use the no-permission fallback inside each lab (representative evidence or pair as observer/recorder) — do **not** change access controls or attach personal billing.

> [!NOTE]
> **Console first.** These labs lead with the web **Console** (portal) because it is the easiest way to *see* what each service does — every control is visible and labeled. Each lab also shows the same action via **CLI** in optional **💻 Also via CLI** boxes, so you feel the trade-off: the portal is great for learning and exploring; the CLI is faster once you know what you want; the Python **SDK** (Week 2) is for automation. The CLI boxes are optional — skip them without missing the lesson.

> **AI-Free Zone (Weeks 1 to 4).** No Copilot / Amazon Q / LLM-generated commands or SQL. When you do use the CLI, type it yourself and read the errors. The required query lab supplies its SQL so you focus on prediction and observation.

## Lab Index

### Provided files

| File | What it is |
| :--- | :--- |
| [README.md](README.md) *(this file)* | Lab index, activity order, and deliverables |
| [Activity_1_Cloud_Object_Storage.md](Activity_1_Cloud_Object_Storage.md) | Required core lab: build a secure Cloud Storage landing zone (100 min) + team design (45 min) |
| [Activity_3_S3_Object_Storage_AWS_Mirror.md](Activity_3_S3_Object_Storage_AWS_Mirror.md) | Optional: the **same** landing-zone lab on **AWS S3** — same files, same controls, full GCS↔S3 concept map (~75 min) |
| [Activity_2_Query_in_Place_with_BigQuery.md](Activity_2_Query_in_Place_with_BigQuery.md) | Required guided lab: query a CSV in place with a BigQuery external table (40 min) |
| [Activity_4_Athena_Query_in_Place.md](Activity_4_Athena_Query_in_Place.md) | Optional: query S3 **in place** with Athena — single-table query-in-place (the AWS mirror of the BigQuery lab, ~35 min) |
| [Activity_5_Athena_Joins.md](Activity_5_Athena_Joins.md) | Optional **follow-on** to Activity 4: add a second table and **JOIN** two files in S3 (~45 min) |
| [Activity_6_Glue_Crawler.md](Activity_6_Glue_Crawler.md) | Optional/backup: auto-discover schema with an **AWS Glue Crawler** → Glue Data Catalog; when a crawler beats manual DDL (~35–40 min) |
| [Activity_7_Bucket_Lock.md](Activity_7_Bucket_Lock.md) | Optional: retention policy, Bucket Lock, and holds (compliance) |
| [Student_Resources.md](Student_Resources.md) | GCS, BigQuery, lifecycle, and S3 references, plus a Day 4 glossary |
| [Lab Resources/](Lab%20Resources/) | `yellow_trip_sample.csv`, `coffee.jpg`, `hartford.jpeg`, `intro.docx` |
| [quiz/Day4_Data_at_Rest_Quiz.md](quiz/Day4_Data_at_Rest_Quiz.md) | Balanced Markdown Mash quiz for storage, schema-on-read, query-in-place, GCS/S3 controls, Athena, Glue, and Bucket Lock |

### Required activity order

1. **Cloud Object Storage landing-zone lab** (`Activity_1_Cloud_Object_Storage.md`), about 100 min: build and secure a raw and a processed bucket, organize prefixes, and configure lifecycle and recovery controls.
2. **Query files in place with BigQuery** (`Activity_2_Query_in_Place_with_BigQuery.md`), about 40 min: schema-on-read, external table, bytes processed, and the external-vs-loaded decision.
3. **Team storage-convention activity** (inside the landing-zone lab), about 45 min: design the NYC Taxi storage contract that feeds Day 5.

Optional extensions (only after the required work), in a sensible learning order: **Activity 3** (S3 storage mirror of Activity 1) → **Activity 4** (Athena query-in-place, AWS mirror of Activity 2) → **Activity 5** (Athena JOINs) → **Activity 6** (Glue Crawler: auto-discover the tables you wrote by hand) → **Activity 7** (Bucket Lock / compliance).

### Deliverables

| # | Deliverable | Format | From | Due |
| :--- | :--- | :--- | :--- | :--- |
| 1 | `day4_lab.md`: preflight evidence, commands, answers to Q1 to Q7, four Predict/Observe responses, lifecycle JSON, and both bucket screenshots (or fallback evidence) | Markdown | Landing-zone lab | End of day |
| 2 | BigQuery query-in-place submission: concept answers, schema, Query A and B observations with bytes processed, limitations, and the two external-vs-loaded decisions | Markdown or form | Query-in-place lab | End of day |
| 3 | Team storage-convention one-pager (required items 1 to 7) plus a 3-minute readout | One page | Team activity | End of day |
| 4 | (Optional) S3, Athena, Athena JOINs, Glue Crawler, or Bucket Lock extension notes appended to `day4_lab.md` | Markdown | Optional | End of day |

---

## How the day fits together

The day follows **Place → Organize → Protect → Query → Operate**. The landing-zone lab builds and secures the storage layer; the query-in-place lab shows how an engine reads files where they rest (schema-on-read); the team activity turns those ideas into a concrete storage contract that becomes the input to the Day 5 NYC Taxi pipeline. Branch-level architecture (ETL/ELT, dimensional modeling, lakehouse internals) is awareness-level today and gets its full treatment in Week 3.

Use the Day 4 quiz early on Day 5 or as an end-of-day check if you want retrieval practice before students move from storage design into full pipeline architecture.

## Permissions and fallbacks

Both required labs depend on a course-managed GCP project. If your account cannot create or inspect resources, do not change access controls: use the no-permission fallback inside each lab (representative evidence and supplied results) or pair with an authorized classmate as observer/recorder. The instructor pre-class checklist and the centralized fallback section live in the Day 4 instructor guide.

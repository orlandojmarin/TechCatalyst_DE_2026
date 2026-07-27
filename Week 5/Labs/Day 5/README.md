# Week 5 Day 5: Apache NiFi and Million Song Mini-Capstone Presentations

Today has three priorities:

1. Complete the guided Apache NiFi activity.
2. Finish and validate the Million Song Mini-Capstone.
3. Present your team's lakehouse solution.

## Learning Objectives

By the end of today, you will be able to:

- explain what Apache NiFi is and where it fits in a data pipeline
- describe how NiFi moves data through processors, connections, queues, and controller services
- build and verify a small S3-to-Snowflake flow
- explain why a plain NiFi insert flow can create duplicates when it runs again
- validate a Databricks lakehouse pipeline before presenting it
- explain and defend your team's architecture, engineering choices, and business findings

## Day Arc

| Sequence | Block | Outcome |
|----------|-------|---------|
| 1 | Apache NiFi tutorial | Build and verify the guided S3-to-Snowflake flow |
| 2 | Mini-capstone work session | Finish the pipeline, run validation, and collect required evidence |
| 3 | Presentation preparation | Finalize the slides, architecture diagram, ERD, findings, and team speaking roles |
| 4 | Team presentations | Present and defend the completed lakehouse solution |
| 5 | Submission check | Confirm that all required exports are saved under `student-work/week5/` |

## Lab Index

Provided files:

| File | Purpose |
|------|---------|
| [`Activity_0_Apache_NiFi_S3_to_Snowflake.md`](Activity_0_Apache_NiFi_S3_to_Snowflake.md) | Beginner tutorial for installing NiFi 2.10.0 and building an S3-to-Snowflake flow with a sample of the Week 4 accidents dataset |
| [`Reading_Apache_NiFi_Fundamentals.md`](Reading_Apache_NiFi_Fundamentals.md) | Short mental-model reading about FlowFiles, processors, services, queues, metrics, and idempotency |
| [`Student_Resources.md`](Student_Resources.md) | Official documentation and a final lab checklist |
| [`../Mini_Capstone/README.md`](../Mini_Capstone/README.md) | Complete Million Song Mini-Capstone requirements, presentation expectations, submission list, and rubric |

Deliverables:

| Deliverable | Save under | Purpose |
|-------------|------------|---------|
| NiFi lab notes | `student-work/week5/day5/nifi-lab-notes.md` | Record both row counts, explain the deliberate duplicate-load experiment, capture provenance, and compare NiFi with Openflow |
| Final mini-capstone presentation | `student-work/week5/` | Submit the team's PowerPoint or PDF |
| Completed build notebook export | `student-work/week5/` | Submit the Databricks source `.py` export |
| Completed validation notebook export | `student-work/week5/` | Submit the Databricks source `.py` export |
| Architecture diagram and Gold ERD | `student-work/week5/` | Submit both visuals as images or PDFs |

## Part 1: Complete the Apache NiFi Tutorial

Open [`Activity_0_Apache_NiFi_S3_to_Snowflake.md`](Activity_0_Apache_NiFi_S3_to_Snowflake.md) and follow it from beginning to end.

Your NiFi work is complete when:

- the NiFi user interface opens successfully
- the flow runs without queued failures
- Snowflake contains 1,000 rows after the first run
- the deliberate second run produces 2,000 rows
- you can explain why this flow reloads data while `COPY INTO` normally skips an already loaded file
- you capture the required flow, query, and provenance evidence
- you answer the reflection questions in `student-work/week5/day5/nifi-lab-notes.md`

## Part 2: Finish and Validate the Mini-Capstone

Continue from your team's current progress. Use the complete requirements in the [Million Song Mini-Capstone guide](../Mini_Capstone/README.md).

Before preparing the final presentation, confirm that:

- the build notebook completes successfully
- the validation notebook passes
- the Lakeflow Job shows a successful build and validation run
- the presentation includes the intentionally failed validation run and the repaired green run
- the architecture diagram and Gold ERD match the objects your team built
- the analyst view preserves one row per eligible listening event
- both business questions have supported answers
- at least one useful visualization supports a business finding

## Part 3: Prepare and Deliver the Team Presentation

Each team has 15 minutes. Every team member must present.

Your presentation must explain:

1. the business problem and source-file challenge
2. the architecture diagram
3. the Gold ERD, table grains, and analyst-view grain
4. one SQL-first profiling result
5. one PySpark transformation and one Gold implementation choice
6. the trade-off behind a key engineering decision
7. the Lakeflow Job and validation evidence
8. at least two business findings, including the supporting visualization
9. one improvement your team would make with more time

Be ready to answer questions and defend your choices with evidence from the pipeline.

## Day 5 Completion Checklist

- [ ] I completed the Apache NiFi tutorial.
- [ ] I saved the required NiFi notes and evidence.
- [ ] I explained the second-run duplicates and the difference from `COPY INTO`.
- [ ] My team completed the mini-capstone build notebook.
- [ ] My team completed the validation notebook and required failure-and-repair test.
- [ ] Our Lakeflow Job evidence is included in the presentation.
- [ ] Our architecture diagram and Gold ERD match the implemented pipeline.
- [ ] Our presentation includes two supported business findings and a visualization.
- [ ] Every team member has a speaking role.
- [ ] All five mini-capstone deliverables are saved under `student-work/week5/`.

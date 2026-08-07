# TechCatalyst Data Engineering 2026: Capstone Overview

**Audience:** Program sponsors and people managers
**Cohort:** 9 students, 3 teams of 3
**Sprint:** Monday August 10 to Friday August 14, 2026
**Final delivery deadline:** Friday August 14
**Demo Day:** Wednesday August 19

---

## What the project is

Each team builds a complete, working data platform on real public data and then presents it to a mixed audience of technical and business stakeholders.

The teams receive over 30 million rows of New York City taxi trip records covering January to May 2025 and January to May 2026, landed in a raw Amazon S3 bucket exactly as they would find it in practice: multiple files, no documentation beyond the vendor's data dictionary, inconsistent quality, and no schema guarantees.

From that starting point, each team must:

1. Choose a business question worth answering.
2. Design a pipeline architecture and justify the design.
3. Ingest, clean, and conform the data.
4. Model it into an analytics-ready warehouse in Snowflake using dbt.
5. Investigate and report on the data's quality defects.
6. Deliver findings through a business intelligence dashboard.
7. Present and defend the whole thing in 20 minutes.

There is no prescribed answer. Teams pick their own analytical question and are graded as much on the quality of their reasoning as on the code they write.

## Why this project

The dataset was chosen deliberately. It is large enough that naive approaches fail, public enough to be verifiable, and messy enough that the students must build real transformation logic and then prove it produced the right answer.

Transformation skill is the foundation of the role, and this project exercises it hard: unioning two fleets with different schemas, typing and deriving dozens of fields, and modeling 30 million rows into a warehouse that answers a business question. **What separates a strong data engineer from an adequate one is that their transformations come with evidence.** Anyone can produce a number. Producing a number the business can act on without checking it is the harder skill, and it is the one this capstone is built to develop.

The two-year span (2025 and 2026) is also deliberate. A single period of data only supports descriptive reporting. Two comparable periods force the students to answer a harder and more valuable question: what changed, by how much, and can we defend that claim?

## What completing this project demonstrates

The capstone is designed so that each deliverable maps to a professional competency, not just a tool.

| Competency demonstrated | How the capstone proves it | Taught in |
| :--- | :--- | :--- |
| **Solution architecture** | Team selects between two valid pipeline architectures, documents the decision, and defends the trade-offs under questioning at the Architecture Defense | Weeks 1, 7 |
| **Requirements framing** | Team converts an open business domain into a specific, answerable question with a defined scope | Weeks 1, 4 |
| **Cloud platform engineering** | Working pipeline across S3 and Snowflake, with optional BigQuery, Databricks, or AWS Glue extensions | Weeks 1, 3, 4, 5 |
| **Data ingestion at scale** | Reliable, re-runnable load of over 30 million rows from object storage into a warehouse | Weeks 4, 5 |
| **Data quality and trust** | A required Data Quality Incident Report: defects found, quantified, and a documented decision on how each was handled | Weeks 3, 4 |
| **Analytics engineering** | Layered dbt models (using dbt Core) with tests and documentation, built on Snowflake | Week 5 |
| **Advanced SQL** | Year-over-year comparison requiring window functions, not simple aggregation | Weeks 3, 4, 5 |
| **Data modeling** | Dimensional design serving a stated analytical purpose | Weeks 1, 4, 5 |
| **Cost and performance judgment** | Written justification of engineering choices and their cost implications, plus what would change at ten times the volume | Weeks 4, 5 |
| **Business intelligence delivery** | A dashboard in Tableau or Looker built for a business audience | Week 7 |
| **Data storytelling** | A 20 minute presentation that lands with technical and non-technical listeners simultaneously | Week 7 |
| **Professional collaboration** | Git-based teamwork, defined roles, a written decision log, and every member presenting | Weeks 1, 2 |
| **Responsible AI use** | A disclosure of where AI assistance was used and what the team independently verified | Weeks 5, 6 |
| **Applied AI (optional)** | Teams may extend with LLM enrichment, BigQuery ML, Cloud Vision, or retrieval-augmented generation | Week 6 |

## What we are deliberately testing beyond code

Three requirements exist specifically because they separate engineers who can be trusted with production systems from those who cannot.

**The Data Quality Incident Report.** Teams must find real defects in the data (trips with negative fares, zero-distance trips billed at high totals, records timestamped outside their own file's month), quantify how many records are affected, and decide and defend a course of action for each. Discovering that a dataset is flawed is easy. Deciding what to do about it, and being able to explain that decision to someone who is depending on the number, is the actual skill.

**The Architecture Defense.** Partway through the sprint, each team defends its design for ten minutes and takes questions. This surfaces struggling teams while there is still time to help, and it gives every student a live rehearsal of technical communication under pressure before Demo Day.

**The cost and performance rationale.** Teams do not report a bill. They explain the choices they made and why: table types, warehouse sizing, materialization strategy, file handling, and what they would change if the data grew tenfold. This is the reasoning a senior engineer is expected to produce on demand.

## How teams are evaluated

| Area | Weight |
| :--- | :--- |
| Pipeline: completeness, reliability, reproducibility | 25% |
| Data quality investigation and remediation decisions | 15% |
| Modeling and analytics engineering (dbt on Snowflake) | 15% |
| Analytical insight and the year-over-year finding | 15% |
| Business intelligence delivery | 10% |
| Presentation, storytelling, and defense under questioning | 20% |

Note that presentation and defense carry the single largest weight after the pipeline itself. This is intentional. The program's position is that an insight nobody can act on has not been delivered.

## Demo Day

Work is delivered by Friday August 14. Demo Day is Wednesday August 19, which gives teams a few days to rehearse rather than presenting something they finished hours earlier.

Three 20 minute presentations plus 5 minutes of questions each, delivered to a mixed technical and business audience. Every student speaks and every student takes questions.

Each team presents a problem statement, a reference architecture diagram, a live or recorded dashboard demonstration, their principal year-over-year finding with the evidence behind it, an honest account of the data quality problems they encountered, and a proposed future state with an effort estimate.

Sponsors are encouraged to ask hard questions. The students have been told to expect them, and the ability to say "we do not know, and here is how we would find out" is treated as a passing answer rather than a failing one.

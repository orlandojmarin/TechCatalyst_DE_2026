# Lab B: Design Your Taxi Pipeline (Week 1 Deliverable)

**Module:** Data architectures and pipeline design (Day 5) · **Format:** Teams of 3 to 4 · ⏱️ 120 minutes

> [!WARNING]
> **AI-Free Zone (Weeks 1 to 4).** Reason through the requirements and draw the architecture yourselves. No AI-generated diagrams or design write-ups. The point is the architect's discipline: let requirements drive the boxes.

**This is the Week 1 deliverable.** Your team designs the end-to-end conceptual architecture you will actually build over the next seven weeks.

## The scenario

You are the data engineering team for a transportation analytics startup. You will ingest NYC TLC trip records (millions of rows per month, Parquet, published monthly: https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) plus at least one companion dataset (taxi zones lookup, collisions, air quality). Pick a business slant: demand forecasting, driver economics, safety analysis, or one you propose.

---

## Phase 1: Requirements first (35 min, no drawing)

Translate the business need into requirements, then into a spec. Do this in order; do not skip to drawing.

### 1a. Business and stakeholder requirements

- **Business requirement:** the high-level goal (for example, "send drivers where demand will be highest at peak times").
- **Stakeholders and consumers:** who uses the output, and what action do they take with it? (analysts, ops managers, a model, a dashboard)

### 1b. System requirements

| Functional (the WHAT) | Your answer |
| :--- | :--- |
| Data sources and formats | |
| Data-store families needed | |
| Storage and zones | |
| Pipeline pattern (ETL, ELT, or hybrid) | |
| Querying and access | |
| Visualization or serving | |
| Real-time or batch | |

| Non-functional (the HOW WELL) | Your answer |
| :--- | :--- |
| Scalability (volume now and at 10x) | |
| Reliability and availability | |
| Security and PII handling | |
| Observability (how you know it works) | |

### 1c. Translate to a data spec

Write the spec the design must satisfy:

| Spec field | Value |
| :--- | :--- |
| Sources | |
| Grain (one row is...) | |
| Freshness (per consumer) | |
| Key metrics or outputs | |
| Sensitive fields | |
| Top 2 cost drivers | |

> The six architect questions are the quick checklist behind this: sources/formats/volumes, freshness, consumers, what can go wrong, what is sensitive, what it costs.

## Phase 2: Draw it (55 min)

In Draw.io (https://app.diagrams.net; a starter skeleton with zone containers is in this folder):

- Zones left to right: **Ingest → Lake (medallion: bronze/silver) → Transform → Warehouse → Serve**
- Reuse yesterday's storage layout convention for the lake zone
- Label **every arrow**: what moves, in what format, how often
- Label the pipeline pattern: **ETL**, **ELT**, or **hybrid**, and explain where transformation happens
- Mark ⚠ where data quality checks happen, and 🔒 where PII handling happens
- Mark where orchestration would run the workflow: schedule, dependency, retry, or alert
- Name real services (GCP primary; you may note AWS equivalents)
- Classify each storage/database component by family: object store, warehouse/OLAP, operational relational/OLTP, document, key-value/cache, wide-column, graph, time-series, vector/search, or "not needed"
- Borrow one idea from the reference architecture you read in Lab A

You may use [Reference_Architecture_Examples.md](Reference_Architecture_Examples.md) as a checklist for diagram grammar. Do not copy an example diagram directly; your boxes and arrows must follow your Phase 1 requirements and business slant.

## Phase 3: Narrative (15 min)

Write a half-page walkthrough a new engineer could follow: start at the source, end at the dashboard, mention each decision and **why**. Tie at least two decisions back to a requirement from Phase 1.

Your narrative must explicitly answer:

- Is this primarily ETL, ELT, or hybrid, and why?
- Which component is OLTP, OLAP, object storage, or specialized storage?
- What does the orchestrator do that the pipeline itself does not?
- Is there any Reverse ETL path? If not, name one future operational destination that could use curated outputs.

## Phase 4: Readout (5 min per team + critique)

Every member presents one zone. Reviewers use the critique protocol:

- What happens when a file fails halfway?
- Where would PII leak?
- What does this cost at 10x volume?
- What would you cut to ship in one week?

---

## Deliverable (commit to one team member's repo, link from others)

- `design_spec.md` (Phase 1: business/stakeholder/system requirements + the data spec)
- `architecture.drawio` + exported `architecture.png`
- `design_narrative.md` (the Phase 3 walkthrough)

## Rubric (instructor)

| Criterion | Weight |
| :--- | :--- |
| Requirements and spec drive the design (not boxes-first) | 25% |
| Functional and non-functional requirements both addressed | 15% |
| Correct medallion zones + storage convention reuse | 15% |
| Arrows labeled with data, format, cadence | 15% |
| Pipeline/database vocabulary used correctly (ETL/ELT, OLTP/OLAP, orchestration) | 10% |
| Quality and PII checkpoints placed sensibly | 10% |
| Narrative clarity + readout defense | 15% |

### Professional diagram checklist

Before readout, confirm:

- Every major component exists because of a requirement, not because it appeared in an example.
- Every arrow says what data moves, the format, and the cadence.
- Quality gates, PII handling, orchestration, and failure paths are visible.
- At least one trade-off is defensible: freshness vs cost, simplicity vs flexibility, or speed vs correctness.

> [!NOTE]
> This diagram is a living document: you will revise it in Weeks 3, 5, and 7 as the real pipeline takes shape, and it becomes the backbone of your capstone presentation.

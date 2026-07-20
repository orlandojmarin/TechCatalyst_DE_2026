# Group Activity: From PoC to Production

**Module:** Week 5 Day 1 opener (builds on Week 4 Day 4, Activity 4)
**Estimated Time:** 60 minutes design, 8 minutes per team to present, plus Q&A
**Format:** 3 teams of 3. Every member presents a part and defends a decision.
**Prerequisites:** Last week's Activity 4 (your pandas ETL to Snowflake) is the PoC in question
**Deliverable:** A one-page architecture brief, one diagram, one sizing table, and a presented defense. No code.

## The memo

> From: VP of Claims Analytics
> To: Your data engineering team
> Subject: Green light, and a reality check
>
> The accident-data proof of concept you demoed this week was exactly what we hoped for: S3 to clean tables in Snowflake, analysts already asking for more. So here is the real project.
>
> The production feed is not one CSV. Roughly **2,400 CSV files land in our raw S3 bucket every day** from telematics devices, claim intake systems, and partner insurers. History already sits at **several hundred terabytes** and grows daily. Before anything reaches analysts, the three sources must be **integrated**: joined on policy and incident keys, deduplicated across partners, and standardized to one schema.
>
> One more thing. The claims leadership dashboard must open on **today's data instantly**. Nobody is willing to wait on a query that grinds through years of history to show one day.
>
> Bring me a solution architecture, not code: what you would build, on what, why, what it costs in people and time, and what happens when it breaks. You present Thursday.

## Why this activity exists

Your PoC works. This exercise is about knowing, precisely, **why it does not scale**, and what a senior engineer proposes instead. Data engineering is the design: requirements, trade-offs, the diagram, the plan, and the defense. The code comes after, and this morning you are not writing any. One more thing: several of this week's lessons, starting this afternoon, are direct answers to questions in this brief. Wrestle with them honestly now and the rest of the week will feel like reveals.

## The five challenges

Work through all five. For each, your brief needs a decision and a justification, not a survey of options.

### Challenge 1: The pandas ceiling

Your PoC read one CSV into memory, transformed it with pandas, and pushed it up with `write_pandas`. Be exact about what breaks at 2,400 files a day and hundreds of TB:

- Where exactly does the in-memory model fail first: RAM, single-machine CPU, network, or the 24 hours in a day? Estimate, do not hand-wave: if one file takes your PoC 2 minutes, what does one day's load take on one machine?
- Is there a file size below which pandas per file is still fine? What orchestration problem remains even then (2,400 successes and failures a day to track)?
- What class of tool exists for this? You have not been taught it yet; name it anyway from your research.

### Challenge 2: Where does the processing run?

On-premise servers, or a cloud service? If cloud, name the actual service and its role:

- On AWS, what does Glue offer here? What is the equivalent path on GCP? Name at least one alternative to each (managed Spark platforms count).
- What does the on-premise option really cost: procurement, patching, scaling for the daily peak, and who wakes up when it breaks?
- Your company already pays for Snowflake. Does that change the answer? Could some or all of the transformation run **in** Snowflake, and what would you need to know to decide?

### Challenge 3: When it breaks at 3 AM

Your PoC is one script: if it dies halfway, you rerun it from the top and hope. Production cannot work that way.

- Design your layers: what lands untouched, what is cleaned and integrated, what is served to the business. Name each layer's job in one sentence.
- A partner insurer sends corrupted files on Tuesday and you discover it Thursday. Walk through the recovery with layers, then without them. What exactly does the no-layers version have to redo, and from where?
- Which layer absorbs a **schema change** from one of the three sources, so the other two keep flowing?
- Your pipeline dies halfway through the 2,400 files and someone reruns it. What stops the first half from being loaded **twice**? Describe, in plain English, the property you want ("running it again causes no damage") and at least one way to get it: a ledger of which files were already processed, rebuilding instead of appending, or something else you propose. Keep this question in your pocket: this afternoon you will learn how Snowflake loads files from cloud storage, and it has a built-in answer.

### Challenge 4: Where do the layers live?

Object store, Snowflake, or a split? Decide layer by layer:

- Hundreds of TB of raw history: S3 or Snowflake tables? What does each cost you in storage, and what does each let you do with the data?
- The integrated middle layer: where does it live so that the processing engine from Challenge 2 can reach it efficiently?
- The gold layer the dashboard reads: is there any argument for it living anywhere other than Snowflake? Which table types from last week (permanent, transient) fit which layer, and why?
- Draw the boundary on your diagram: which arrows cross from the object store into Snowflake? You do not yet know Snowflake's machinery for pulling files in from cloud storage (that is this afternoon's topic), so label the arrow in plain English: "bulk load from bucket" is enough for now.

### Challenge 5: "I only want today"

The dashboard opens on today's data instantly, against a table holding years of history.

- A plain view (`CREATE VIEW today AS SELECT ... WHERE date = CURRENT_DATE()`) is the obvious move. What does a view actually do, and does it make the scan smaller by itself?
- What physical design makes that date filter cheap? You saw the idea in BigQuery last week (partitioning: the engine skips data outside the date range); research what Snowflake offers in the same spirit (clustering, and what micro-partition pruning means).
- What else could serve the "today" page: a small gold table rebuilt each morning by the pipeline? A materialized view? Compare at least two options on freshness, cost, and complexity, and pick one.
- The dashboard is opened about 200 times a day by 40 people. Does that change your answer?

## The sizing section (required, and where most teams get exposed)

Leadership funds plans, not diagrams. Commit to numbers and defend them:

| Question | Your answer must include |
|---|---|
| Tools | The named services in your final design, one line each on its job |
| Build effort | Phases (PoC hardening, pipeline build, backfill of the historical TBs, cutover), with weeks per phase |
| The backfill | How long to process hundreds of TB of history, and does it use the same pipeline as the daily load or a one-time variant? |
| Team | How many people, what roles (data engineer, platform, analyst liaison), and what the smallest viable team is |
| Run cost drivers | The two or three line items that will dominate the monthly bill, and which knob controls each |

Estimates will be rough. Wrong-but-reasoned beats vague: state your assumptions (file size, processing rate per node, team velocity) so your numbers can be challenged on their merits.

## Deliverables

1. **One diagram**: sources to dashboard, every layer labeled with where it lives and what moves it. Draw.io, whiteboard photo, or slide, your choice.
2. **The decision table**: five challenges, five decisions, one-sentence justification each.
3. **The sizing table**, filled in.
4. **Top three risks** with a mitigation each (technical or organizational).
5. **The pitch**: 8 minutes, every member presents, then defend under questioning. Expect at least one "why not just..." question per challenge.

## Rules

- Week 5 rules: AI is allowed with review required. Use it to explain concepts if you like, but the decisions, numbers, and diagram must be yours, and you must be able to defend every line without it. Official documentation (AWS, GCP, Snowflake, Databricks) is your primary source.
- Name real services. "The cloud handles it" earns the follow-up question you deserve.
- Disagreement inside the team is raw material: put the strongest rejected option in your justification ("we chose X over Y because...").
- You have not been taught the distributed tools yet. That is the point: architects routinely size and select technology one step ahead of their own hands-on skill. Starting tomorrow, this week hands you those exact tools, and by Friday you can judge your own proposal.

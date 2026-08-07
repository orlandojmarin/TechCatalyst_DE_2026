# Capstone Rubric

Total 100 points. Team score, with an individual adjustment described at the end.

| Area | Weight |
| :--- | :--- |
| Pipeline: completeness, reliability, reproducibility | 25 |
| Data quality investigation and remediation decisions | 15 |
| Modeling and analytics engineering | 15 |
| Analytical insight and the year-over-year finding | 15 |
| Business intelligence delivery | 10 |
| Presentation, storytelling, and defense | 20 |

---

## Pipeline (25 points)

| Level | Description |
| :--- | :--- |
| Excellent (22 to 25) | Runs end to end from a clean start. Idempotent: re-running does not duplicate data. Row counts reconcile to source. Failures are handled or clearly logged. Someone else could run it from the README alone. |
| Good (17 to 21) | Runs end to end. Minor manual steps. Counts mostly reconcile. README is usable with some guesswork. |
| Adequate (12 to 16) | Produces the data but only with manual intervention or in a specific order that is not documented. Re-running is risky. |
| Weak (0 to 11) | Incomplete, does not run without the author present, or the data in Snowflake cannot be traced back to the source. |

Reconciling row counts against the source files is the single clearest signal of a trustworthy pipeline. Teams that can state exactly how many records entered, how many were dropped, and why, score well here.

## Data quality (15 points)

| Level | Description |
| :--- | :--- |
| Excellent (13 to 15) | Multiple real defects found, including at least one not listed in the catalog. Each is quantified. Each decision is justified with what was gained and lost. The team knows how the remaining defects limit their conclusions. |
| Good (10 to 12) | The catalog's known traps are found, quantified, and handled with stated reasoning. |
| Adequate (7 to 9) | Defects noted and handled, but reasoning is thin, or scale is not quantified. |
| Weak (0 to 6) | Generic null checks. Rows dropped without explanation. The cash tip trap present in a chart unacknowledged. |

Presenting a chart built on the cash tip trap without naming it costs points here and in the presentation.

## Modeling and analytics engineering (15 points)

| Level | Description |
| :--- | :--- |
| Excellent (13 to 15) | Clear layering. Models are named and structured so their purpose is obvious. Tests cover keys, categorical values, and relationships, and they pass. Materialization choices are deliberate and explained. Documentation generated. |
| Good (10 to 12) | Sensible layering and working tests. Some structural or naming inconsistency. |
| Adequate (7 to 9) | dbt used, models run, minimal testing, structure mostly mirrors the source tables without modeling intent. |
| Weak (0 to 6) | dbt barely used, or used as a thin wrapper over one large query. |

Write the query a strong engineer would actually write. A CTE that exists to demonstrate CTEs, or a model layer that adds nothing, scores lower than the simpler correct version. Complexity is not evidence of skill.

## Analytical insight (15 points)

| Level | Description |
| :--- | :--- |
| Excellent (13 to 15) | A specific, quantified year-over-year finding that survives questioning. The team checked whether a data quality issue could explain it, confirmed the comparison is fair, and stated their confidence honestly. There is a clear "so what". |
| Good (10 to 12) | A solid quantified finding, defended adequately, with a plausible business implication. |
| Adequate (7 to 9) | Descriptive results. Comparison present but shallow, or the "so what" is asserted rather than supported. |
| Weak (0 to 6) | Counts and averages with no comparison, or a claim that collapses under the first question. |

Uncertainty stated honestly scores better than false confidence. "The change is 4 percent and we do not think that is distinguishable from noise" is a good answer.

## Business intelligence delivery (10 points)

| Level | Description |
| :--- | :--- |
| Excellent (9 to 10) | Dashboard in Tableau or Looker connected to the Snowflake models. Built for a business reader: the point is clear without narration. Sound chart choices, labeled axes, no chartjunk. |
| Good (7 to 8) | Connected and functional. Some charts require explanation to interpret. |
| Adequate (5 to 6) | Dashboard exists but is a collection of charts rather than an argument. |
| Weak (0 to 4) | Missing, disconnected from the models, or unreadable. |

A Streamlit app is a bonus, not a substitute.

## Presentation and defense (20 points)

| Level | Description |
| :--- | :--- |
| Excellent (18 to 20) | Coherent narrative from problem to recommendation. Technical and business audiences both served. Every member speaks well and handles questions. Architecture diagram is clear and matches what was built. Timing respected. Answers to hard questions are direct, including honest admissions of what they do not know. |
| Good (14 to 17) | Clear story, good visuals, all members contribute, most questions handled competently. |
| Adequate (10 to 13) | Content present but the narrative is a tool tour rather than an argument. Uneven participation. Questions partly handled. |
| Weak (0 to 9) | Disorganized, badly over or under time, one or two people carrying it, or unable to answer questions about their own work. |

"I do not know, and here is how I would find out" is a passing answer. Bluffing is not, and it is obvious.

---

## Required deliverables

These are pass or fail. A missing item costs 5 points from the total.

- [ ] GitHub repository with a README that lets someone else re-run the work
- [ ] Working pipeline from S3 RAW to Snowflake gold models
- [ ] dbt Core project with staging models, mart models, and passing tests
- [ ] Data Quality Incident Report
- [ ] At least one defended year-over-year finding
- [ ] Dashboard in Tableau or Looker
- [ ] Architecture diagram of what was actually built
- [ ] Cost and performance rationale
- [ ] Future state proposal with diagram and effort estimate
- [ ] AI use disclosure
- [ ] Completed team charter with decision log

## Bonus (up to 5 points)

Awarded for optional work that is genuinely integrated and honestly presented, not bolted on: the Databricks lane, a BigQuery comparison with real numbers, a Streamlit app, meaningful AI enrichment, or substantial external data enrichment.

A team that attempts something ambitious, hits a wall, and presents a clear account of what went wrong and what they learned can earn bonus points. Intellectual honesty about a failure is a professional skill and we score it as one.

## Individual adjustment

The team score is the starting point for every member. It can be adjusted up or down based on commit history, the role recorded in the charter, contribution to the deliverables, and performance during questions.

Everyone presents. Everyone answers at least one question. A member who cannot speak to the team's technical decisions will be adjusted down regardless of the team's score.

## On AI use

You may use AI assistants. You must disclose where, in a short section covering what you used them for and what you verified independently.

Undisclosed use is an integrity issue. More practically: you will be asked in the Q&A to explain how your code works, and code you cannot explain will be treated as code you did not write. That is also true in a job interview and in a production incident review, which is the actual reason this rule exists.

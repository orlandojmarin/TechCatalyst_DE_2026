# Sprint Milestones (Suggested - THIS IS TO HELP YOU ORGANIZE)

Five build days, everything due Friday August 14, then **Demo Day on Wednesday August 19**.

The gap between delivery and Demo Day is rehearsal time, not build time. Your pipeline is frozen on Friday. Use the days after it to get good at explaining what you built.

Each day has a **checkpoint** that you demonstrate, not describe. "It is nearly working" is not a checkpoint.

---

## Monday: decide and land

The goal today is not to build much. It is to make the decisions that make the rest of the week possible.

- Complete `Team_Charter_Template.md`: roles, git workflow, how you will make decisions when you disagree.
- Create your team GitHub repository. Every member commits something today, even if it is only a README edit.
- Read `Data_Catalog.md` as a team.
- Profile the raw data. Open two or three files. Check the schemas actually match. Count rows. Look at the columns you plan to use.
- Choose your analytical question. Write it down as one sentence.
- Choose Pattern A or Pattern B and record why in your decision log.
- Get one file all the way into Snowflake.

**Checkpoint:** one raw file loaded into a Snowflake table, and your one-sentence question written in your repository README.

Landing one file today is worth more than designing an elegant pipeline you have not tested. The connection, the credentials, the stage, and the file format are where days get lost.

---

## Tuesday: ingest and conform

- Load all 20 files through your chosen pattern.
- Union Yellow and Green, reconciling the column differences.
- Apply typing and derived columns: trip duration, day of week, hour, month, year, taxi type, and whatever your question needs.
- Join the zone lookup so your locations have names.
- Begin the Data Quality Incident Report. Log defects as you hit them, with counts. Do not leave this to Thursday; you will have forgotten what you found and why you dropped it.

**Checkpoint:** all 20 files loaded, Yellow and Green unioned into one queryable table in Snowflake, with a row count you can reconcile against the source files.

Reconciling that row count is the point. If you loaded 30.2 million rows and the source files hold 30.4 million, find the missing 200 thousand before you move on.

---

## Wednesday: model, then defend your architecture

- Build your dbt project: staging models, then marts.
- Add tests. At minimum `not_null` and `unique` on your keys, `accepted_values` on your categorical lookups, and a relationship test on your zone join.
- Run `dbt docs generate` and look at your lineage graph.
- Produce your first year-over-year comparison.
- Prepare for the Architecture Defense.

**Checkpoint: the Architecture Defense.** Ten minutes per team plus questions, to the instructor and the other teams.

Cover: your question, your architecture and why you chose it, what has broken so far, what you are worried about, and what you are cutting if you run out of time. Bring your diagram.

This is not a graded presentation. It is the moment to surface problems while there is still time to solve them, and it is your first live rehearsal for Demo Day. Teams that paint an optimistic picture here and deliver a broken pipeline on Friday will be asked why.

---

## Thursday: analyze and visualize

- Finish your gold models.
- Connect Tableau or Looker to Snowflake and build the dashboard.
- Finalize the Data Quality Incident Report.
- Write the cost and performance rationale.
- Produce your architecture diagram of what you actually built, and the future state diagram.

**Checkpoint:** dashboard connected to Snowflake showing real data.

Take screenshots of your dashboard as you go. Live demos fail, networks drop, and Snowflake sessions expire.

---

## Friday: deliver

Everything is due today. **Freeze the pipeline.**

- Repository README finished, good enough that someone else could re-run your work.
- All required deliverables committed and complete.
- First full rehearsal, out loud, with slides and a timer.

**Checkpoint:** every required deliverable in the repository, and a pipeline that runs from a clean start.

After today you do not touch the pipeline. Every cohort has at least one team that "improves" something working the night before presenting and demos a broken build. The work you deliver Friday is the work you present.

---

## Before Demo Day

You have the weekend and two days. This is rehearsal time. Use it.

- Rehearse the full talk out loud, timed, at least twice more.
- Practice the handoffs between speakers specifically. They are where teams look unrehearsed.
- Have someone outside your team listen and tell you what they did not follow.
- Prepare for the questions in `Presentation_Guide.md`, especially "how do you know that number is right?"
- Confirm your screenshots are captured and your demo path works end to end.

Teams that treat these days as extra build time and skip rehearsal are consistently the ones that go over time and lose their recommendation.

---

## Demo Day: Wednesday August 19

Presentations to a mixed technical and business audience: 20 minutes plus 5 minutes of questions per team.

**Checkpoint:** the presentation itself.

Everyone speaks. Everyone takes at least one question.

---

## If you fall behind

Cut in this order. Do not cut from the top of the list.

1. AI enrichment
2. Databricks lane
3. BigQuery second destination
4. Streamlit app
5. Additional enrichment datasets
6. Extra dbt models beyond what your question needs
7. Scope of the analytical question itself: narrow it

Never cut: the working pipeline into Snowflake, the dbt models, the data quality report, the dashboard, or the rehearsal.

A narrow question answered well and presented confidently scores higher than an ambitious one delivered half-finished. Every year, at least one team learns this the hard way.

---

## Getting help

Ask early. A team blocked for three hours on a connection string has burned a quarter of a sprint day for no learning at all.

Bring: what you are trying to do, what you tried, the exact error, and what you have already ruled out. That is also how you will be expected to ask for help professionally.

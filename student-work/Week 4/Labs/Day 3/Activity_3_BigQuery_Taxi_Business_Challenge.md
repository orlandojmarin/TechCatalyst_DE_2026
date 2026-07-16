# Activity 3: BigQuery Taxi Business Challenge

**Module:** Week 4 Day 3  
**Estimated Time:** 45 to 55 minutes  
**Difficulty:** Intermediate  
**Format:** Three teams of three  
**Prerequisites:** Activity 2

## Objective

Translate one stakeholder request into a readable two-CTE GoogleSQL query, validate its grain, create a manual BigQuery visualization, and present an evidence-based interpretation.

This is an AI-Free Zone activity. Write the SQL and interpretation as a team. Do not use generated SQL, natural-language analysis, Auto-Chart, or an Insights feature. You may use BigQuery's manual visualization controls after your query is complete and validated.

## Shared data contract

Every team uses only:

```text
bigquery-public-data.chicago_taxi_trips.taxi_trips
```

Every query must:

1. Use `2023-12-25` through `2023-12-31`.
2. Keep only rows where `fare > 0`.
3. Use exactly two CTEs: one base CTE and one grouped-metrics CTE.
4. Use one source table and no join.
5. Return exactly five rows.
6. State the grain of both CTEs and the final result.
7. Produce one manually configured bar chart from the final result.

## Team assignments

With nine learners, form three teams of three:

| Team | Assigned option | Grouping dimension | Main ranking metric |
|---|---|---|---|
| Team 1 | Option A | Company | Total revenue |
| Team 2 | Option B | Payment type | Trip count |
| Team 3 | Option C | Trip-start hour | Trip count |

Each option has the same workload:

- two CTEs;
- one grouped aggregation;
- the same `COUNT`, `SUM`, and `AVG` calculations;
- four final columns;
- one descending top-five ranking;
- one bar chart;
- one evidence, interpretation, recommendation, and limitation story.

## Option A: Company revenue leaders

Business request: Which five named companies produced the highest total trip revenue during the verified week?

### SQL contract

1. Create `base_trips` with one positive-fare trip per row.
2. Select `company` and `trip_total` in `base_trips`.
3. Exclude null and blank company names in `base_trips`.
4. Create `company_metrics` with one row per company.
5. Calculate `trip_count`, `total_revenue`, and `avg_trip_total`.
6. Return `company`, `trip_count`, `total_revenue`, and `avg_trip_total`.
7. Round the two monetary measures to two decimals.
8. Sort by total revenue descending, then company ascending, and return five rows.

### Visualization contract

- Chart: bar chart
- Category: `company`
- Metric: `total_revenue`
- Title: `Top 5 Companies by Trip Revenue`

### Story question

How concentrated is revenue among the five leaders, and what operational or partnership question should the stakeholder investigate next?

## Option B: Payment volume leaders

Business request: Which five payment types handled the most positive-fare trips, and how did their revenue and average trip totals differ?

### SQL contract

1. Create `base_trips` with one positive-fare trip per row.
2. Select `payment_type` and `trip_total` in `base_trips`.
3. Exclude null and blank payment types in `base_trips`.
4. Create `payment_metrics` with one row per payment type.
5. Calculate `trip_count`, `total_revenue`, and `avg_trip_total`.
6. Return `payment_type`, `trip_count`, `total_revenue`, and `avg_trip_total`.
7. Round the two monetary measures to two decimals.
8. Sort by trip count descending, then payment type ascending, and return five rows.

### Visualization contract

- Chart: bar chart
- Category: `payment_type`
- Metric: `trip_count`
- Title: `Top 5 Payment Types by Trip Volume`

### Story question

Do the highest-volume payment types also have the highest average trip totals, and what additional evidence would be needed before recommending one payment channel over another?

## Option C: Hourly demand leaders

Business request: Which five trip-start hours had the highest positive-fare demand during the verified week?

### SQL contract

1. Create `base_trips` with one positive-fare trip per row.
2. Create `trip_hour` with `EXTRACT(HOUR FROM trip_start_timestamp)`.
3. Select `trip_hour` and `trip_total` in `base_trips`.
4. Create `hourly_metrics` with one row per trip-start hour.
5. Calculate `trip_count`, `total_revenue`, and `avg_trip_total`.
6. Return `trip_hour`, `trip_count`, `total_revenue`, and `avg_trip_total`.
7. Round the two monetary measures to two decimals.
8. Sort by trip count descending, then trip hour ascending, and return five rows.

### Visualization contract

- Chart: bar chart
- Category: `trip_hour`
- Metric: `trip_count`
- Title: `Five Busiest Trip-Start Hours`

### Story question

What time-of-day demand pattern appears, and what staffing or capacity decision could this result inform?

## Complete the SQL first

1. Copy `starter/day3_public_taxi_business_challenge.sql` into `student-work/week4/day3/` if you have not already done so.
2. Record the assigned option and required final columns.
3. Write the name and grain of both required CTEs.
4. Write and run the complete query in the standard BigQuery SQL editor.
5. Confirm the output against the option's checks below.
6. Record BigQuery's byte estimate.

Do not begin the visualization until the SQL result is correct.

## Visualization and story challenge

After validating the query:

1. Open the BigQuery visualization tool available in the classroom interface.
2. If it opens BigQuery data canvas, add a SQL node and paste the SQL your team already wrote.
3. Run the SQL node and add a visualization from its result.
4. Select the bar chart and fields listed in your option's visualization contract.
5. Configure the title manually.
6. Do not use a natural-language prompt, generated SQL, Auto-Chart, or generated Insights.
7. Export the chart as a PNG or capture a clear screenshot.
8. Save it under `student-work/week4/day3/` as `team_<option>_taxi_story.png`.

If the visualization tool is unavailable, create a careful chart sketch from the five result rows. Label both axes and preserve the correct ranking.

## Team roles and presentation

Every team member must speak:

| Role | Responsibility during the build | Presentation contribution |
|---|---|---|
| SQL planner | Confirms filters, CTE names, and grain. | Explains the question and query structure. |
| Validator | Checks rows, ordering, uniqueness, and byte estimate. | Explains why the result is technically credible. |
| Story analyst | Builds the manual chart and drafts the story. | Explains the pattern, recommendation, and limitation. |

Prepare a three-minute presentation with four statements:

1. **Evidence:** What exact pattern appears in the result and chart?
2. **Interpretation:** What might that pattern mean for the stakeholder?
3. **Recommendation:** What reasonable action or investigation should happen next?
4. **Limitation:** What can this one-week result not prove?

## Expected output checks

| Option | Required check |
|---|---|
| A | Exactly 5 rows, 5 unique nonblank companies, 4 columns, and revenue sorted descending. |
| B | Exactly 5 rows, 5 unique nonblank payment types, 4 columns, and trip count sorted descending. |
| C | Exactly 5 rows, 5 unique hours from 0 through 23, 4 columns, and trip count sorted descending. |

For every option, confirm that the chart contains five categories and that its ordering agrees with the query result.

## Required deliverables

Your copied starter file and chart must provide:

1. Assigned option and fixed date window.
2. Both CTE names and grains.
3. One complete query.
4. Output validation evidence.
5. BigQuery byte estimate.
6. Chart type, category, metric, and title.
7. Chart PNG or screenshot.
8. Evidence, interpretation, recommendation, and limitation statements.
9. One next validation.

## Hints

<details>
<summary>The result contains fewer or more than five rows</summary>

Apply `ORDER BY` to the grouped result, then use `LIMIT 5` in the final query.

</details>

<details>
<summary>The chart order does not match the SQL result</summary>

Set the chart's sort field to the same metric and direction used by the SQL query. Do not let the chart silently sort categories alphabetically.

</details>

## Success criteria

- Every team receives the same structural workload.
- The source, dates, filters, CTE names, and output grain are explicit.
- The query uses exactly two CTEs and no unnecessary join.
- The final result has exactly five rows and four columns.
- The chart uses the team's verified SQL result and manual controls.
- The spoken interpretation separates evidence from assumptions.
- The recommendation follows from the evidence.
- The limitation identifies something a successfully executed query cannot prove.

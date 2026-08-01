# Group Activity: Chart Clinic

**Estimated Time:** 50 minutes
**Team size:** two or three
**Deliverable:** a five-minute presented and defended dashboard redesign

## The situation

A claims operations leader circulated a dashboard to justify a budget request for additional claims-processing headcount next quarter. Leadership is expected to approve or reject the request based on what this dashboard shows.

The dashboard is bad. It was built by someone who reached for whatever chart type looked impressive rather than the chart type that answers the question being asked. Your team's job is to diagnose exactly why it fails, then design and defend a replacement that leadership could actually act on.

Work in teams of two or three. Every part below produces something you carry into the presentation.

## The artifact

No image ships with this activity. The dashboard is described in text below so you can reconstruct it on paper or in a notebook with no file to open. It has one title and four visuals.

**Title:** "Q3 Dashboard," centered at the top of the page.

**Visual 1, a 3D exploded pie chart.** Nine slices, one per claim category (Auto, Property, Liability, Workers' Comp, Medical, Homeowners, Umbrella, Marine, Cyber), showing each category's share of total claim volume this quarter. The pie is rendered in 3D with every slice pulled apart from the center.

**Visual 2, a dual-axis line chart.** Two lines over the last 12 months: average claim cost on the left axis, staff headcount on the right axis. The two lines are scaled so they rise and fall together across the year.

**Visual 3, a table.** Forty rows of raw claim records dropped below the charts. No column headers, no title, no sort order, no units.

**Visual 4, a status grid.** Nine tiles, one per claim category, each colored solid red or solid green. Red means the category's average claim cost rose from last quarter, green means it fell. No numbers appear on the tiles, only the color.

## Part 1: diagnose

For each of the four visuals, write two things:

1. The specific failure, using this morning's chart-choice vocabulary: the question shape the visual should be answering, the chart that shape calls for, and what the dashboard used instead.
2. The decision this dashboard is supposed to support that this visual does not support.

Two of the four visuals have failures worth naming precisely:

- The dual-axis line does not just pick the wrong chart. Plotting two series on two independent axes lets you scale each axis so the lines appear to move together, whether or not the underlying numbers are actually related. That is not evidence that headcount and claim cost are connected. Correlation is not causation, and a dual-axis chart does not even establish correlation, it manufactures the appearance of one.
- The status grid's red-green coloring is not a style complaint, it is an access failure. Roughly 1 in 12 men has some form of red-green color vision deficiency. Encoding "rose" versus "fell" in red versus green alone makes the tile grid unreadable to a meaningful share of any audience, including possibly someone in the room this dashboard is presented to.

Also write one sentence on why the dashboard's own title, "Q3 Dashboard," fails. Use this morning's distinction between a label title and a conclusion title.

## Part 2: redesign

Sketch a replacement, on paper or in a notebook cell. Code does not need to run.

Rules for the redesign:

- Every chart carries a conclusion title, not a label title.
- The whole redesign fits on one screen. You do not get four charts just because the original had four. Decide what earns a place and what does not.
- Any chart you keep from the original four must have its chart type fixed, not just its title.

## Part 3: the six-step arc

Write the six-step story arc for your redesigned dashboard. Use the same six steps from this morning, in order, one or two sentences each:

1. **Decision.** What choice is this analysis meant to inform?
2. **Context.** What does the audience already know, and what do they need to know to follow the rest?
3. **Evidence.** What is the specific finding, in numbers?
4. **Insight.** Why does that finding matter, what does it mean for the decision?
5. **Caveat.** What does the data not show, stated honestly?
6. **Recommendation.** What should the audience do next?

Base every step on your redesign, not on the original dashboard.

## Part 4: present and defend

Present for five minutes. Every team member speaks. After you present, other teams challenge your redesign.

Come prepared for this exact challenge, because every team will face some version of it: "you removed a chart my director asked for, defend that." You need a real answer for why the chart you cut does not belong on a one-screen dashboard, not just "it looked bad."

## Deliverable table

| Part | Deliverable | Done? |
|---|---|---|
| Part 1: Diagnose | A named failure and a named unsupported decision for each of the four visuals, plus one sentence on the title | ☐ |
| Part 2: Redesign | A one-screen sketch, every chart carrying a conclusion title | ☐ |
| Part 3: Six-step arc | All six steps written for the redesigned dashboard, one or two sentences each | ☐ |
| Part 4: Present and defend | A five-minute presentation, delivered by the whole team, with a defended answer to the removed-chart challenge | ☐ |

## What good looks like

- The diagnosis names a decision the dashboard fails to support, not just an aesthetic complaint about how a chart looks.
- Every title on the redesigned dashboard is a conclusion, not a label.
- The caveat is specific enough to be inconvenient: it names something the redesigned dashboard genuinely does not show, not a generic disclaimer.

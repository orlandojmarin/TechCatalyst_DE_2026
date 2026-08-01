# Reading: Charts That Argue

**TechCatalyst Data Engineering 2026 · Week 7 Day 1**

Read this before class, or during the first break. There are no slides today, so this file carries that weight instead. The activities are where you build things. This is where the reasoning behind what you build lives.

---

## 1. Why this week exists

You have spent seven weeks building pipelines: extracting data, cleaning it, loading it, joining it, aggregating it. None of that argues for anything on its own. Nobody outside the data team sees your SQL. What they see is a chart, a dashboard, or a paragraph about what the numbers mean, and that is the only part of the work most audiences ever judge.

This week is the last mile. You already know how to compute the right answer. Now you practice making it land: choosing the chart that shows it, titling it so the reader does not have to work for the point, and building an app that lets someone explore it without you standing next to them.

Week 8 is the capstone, and it is judged substantially on presentation. A technically strong pipeline with a confusing readout scores worse than a simpler pipeline presented clearly. Chart choice, title writing, honest smoothing, and a working Streamlit app are graded as directly as your code.

## 2. The three questions a chart must answer

Before you open a plotting library, answer three questions.

**Who is the audience?** A chart for a fellow data engineer can show raw distributions and let the reader draw conclusions. A chart for a claims manager or an executive has one job: state the finding.

**What decision are they making?** Every professional chart exists because someone is about to decide something: approve a budget, negotiate a rate, flag a pattern, expand a policy. If you cannot name the decision, you default to showing everything, which shows nothing.

**What would change their mind?** This forces the counterargument into view. If the audience already believes the finding, the chart is confirmation, not persuasion. If they do not, the number has to be checkable and the caveat visible, not buried in a footnote.

## 3. Choosing the chart

Once you know the audience, the decision, and what would move them, the chart type follows from the shape of the question, not from habit. This is the table from Activity 3:

| Question shape | Chart | Avoid |
|---|---|---|
| How does one number compare across categories? | Bar | Pie, which makes close values indistinguishable |
| How did one number move over time? | Line | Bar, which implies discrete buckets |
| How are two numbers related? | Scatter | Dual-axis line, which invents correlations |
| How is one number distributed? | Histogram or box | A single mean, which hides the shape |
| How does a total split into parts? | Stacked bar | Pie, once you exceed about four slices |

**Comparing a number across categories** favors a bar, because length is easy to compare at a glance. A pie asks the reader to compare angles or areas instead, which people are measurably bad at once slices get close in size. Activity 3 shows this directly: the same ten states plotted as a pie look almost identical, because the ratios only range from about 6.65 down to about 3.99. Plotted as a horizontal bar, the ranking is instant.

**A number moving over time** wants a line, which shows the shape of change, not just endpoints. A bar chart implies each period is a separate bucket unrelated to its neighbors, which hides trends.

**Two numbers related to each other** want a scatter plot, one point per observation, so the reader sees the actual relationship. A dual-axis line tempts you to overlay series on different scales, but it also lets you pick axis ranges that make any two lines look correlated, a trick even when unintentional.

**A distribution** wants a histogram or box plot, because a single mean throws the shape away. Two datasets can share an average and still have very different spreads.

**A total splitting into parts** wants a stacked bar, not a pie, past three or four categories, for the same reason as the first row.

## 4. The title is the argument

A title has room for one sentence. Most people spend it on a label: what the axes already show. A **label title** describes the chart. A **conclusion title** states the finding, in numbers, so the reader can check it against the chart without doing math.

| Label title | Conclusion title |
|---|---|
| Ratio by state | New Jersey hospitals bill 6.7 times what Medicare pays |
| Discharges over time | Discharge volume is flat, so the cost growth is price, not demand |
| Charges versus payments | Payments barely move as charges rise |

Only the New Jersey rewrite is a finding from data you actually plotted; the other two rows are the same pattern borrowed from other analysis, useful as a template, not as claims about the hospital claims dataset.

What makes the New Jersey title work: it names a number, checkable against the bar. Compare that to "New Jersey bills 44 percent more than Texas." Readers split on whether that means 1.44 times as much or something else, and a title different readers parse differently is a puzzle, not a finding. State both values directly, or spell out the percentage rather than leaving it ambiguous.

## 5. Interactivity is a tool, not a decoration

Hover, zoom, and pan feel free once a library makes them one line of code. They are not free: every interactive element asks something of the reader, and that is a fair trade only when it helps.

Interactivity earns its place when the reader is exploring, not receiving a conclusion. Hand someone a chart and say "find the day demand collapsed," and hover lets them find it themselves, with the exact date and value appearing on contact, which is exactly the anomaly-hunting work in Activity 6. It also earns its place when identifying one specific point matters, like which state is that outlier bar.

Interactivity is noise when the chart carries one message and is headed into a slide or a printed report. A chart with an annotated arrow pointing at Maryland and a title that already states the finding does not need a tooltip nobody will click, because the reader is being told something, not exploring. The same data in an interactive app is a different object with a different job, which is why this course teaches both.

## 6. From chart to app

A static chart answers the one question you anticipated. A dashboard or app answers the next question too, the one the reader thinks of after looking at your chart, without you in the room to build a new one for them: "what about last month," or "what if I lower the threshold."

Streamlit makes this possible through a model worth understanding before you build with it: the **rerun model**. A Streamlit app does not run once and wait for input. Every time the reader interacts with the page, moving a slider, clicking a button, switching a data source, Streamlit reruns your entire script from the top. Widgets are not events you handle individually; they are values your script reads fresh on every rerun. That explains the main trap: anything expensive at the top level of your script, like loading a large CSV, runs again on every interaction unless you deliberately cache it. You meet caching directly in Activity 4.

## 7. Honest smoothing and honest forecasting

Smoothing and forecasting both make a chart easier to read, and both can quietly delete the finding you care about.

A rolling average is a real tool: daily data is noisy, and averaging across a window reveals the trend underneath the jitter. But the same averaging that removes noise also removes a real signal if that signal is a single sharp event rather than a gradual trend. The NYC taxi data makes this unmissable. On 2015-01-27, during Winter Storm Juno, rides fell to 232,058 against a typical level near 800,000, an approximately 70 percent collapse, the single largest disruption in the series. A 7-day rolling average centered on that day flattens it into the surrounding week: computed directly on this data, the smoothed reading lands around 604,000, a moderate-looking dip rather than the deepest point in over a year of data. The chart still runs without errors. It just stops telling you what happened.

Forecasting carries a different risk. A forecast is not a fact about the future, it is a claim, and every claim rests on an assumption about how the past predicts what comes next. Activity 6 fits a Holt-Winters model with a 7-day seasonal period, reasonable for taxi demand because ridership genuinely repeats on a weekly commuting cycle. That same assumption is close to meaningless applied to a stock ticker, which has no comparable weekly structure, even though the model still produces numbers either way.

## 8. The six-step arc

Every deliverable in this course, from a written case study to a live dashboard, follows the same six-step arc. Learn the order now; you will reuse it for the rest of the course and in the Week 8 capstone.

1. **Decision.** What choice is this analysis meant to inform?
2. **Context.** What does the audience already know, and what do they need to know to follow the rest?
3. **Evidence.** What is the specific finding, in numbers?
4. **Insight.** Why does that finding matter for the decision?
5. **Caveat.** What does the data not show, stated honestly?
6. **Recommendation.** What should the audience do next?

Here is the arc applied to the Maryland finding from the hospital claims data.

**Decision.** Should a payer negotiate hospital rates directly, the way Maryland does, or let the market set them the way the rest of the country does?

**Context.** In every other state in this dataset, each hospital negotiates its own charges against what Medicare pays, which is why the ratio varies so widely by state.

**Evidence.** New Jersey hospitals bill on average 6.65 times what Medicare pays. Maryland bills 1.06 times, the lowest in the dataset, because Maryland operates an all-payer hospital rate-setting system, the only one in the United States.

**Insight.** Maryland is not an outlier of scale, it is an outlier of policy: one rate that applies to every payer keeps the billed-versus-paid gap nearly closed, where the rest of the country negotiates that gap hospital by hospital.

**Caveat.** This dataset covers Medicare inpatient claims only, nothing about commercial insurance or outpatient care, and it has no date column at all, so nothing here supports a claim about a trend over time, only a comparison across states at whatever point this data was collected.

**Recommendation.** Before a payer or state health department expands Maryland-style rate setting elsewhere, study its effect on hospital margins and patient access within Maryland itself. A lower ratio alone does not prove the policy is good for patients, only that it changes what gets billed.

The caveat step is not an apology tacked onto the end. It is what makes the recommendation trustworthy, and lets a reader act on the other five steps with their eyes open.

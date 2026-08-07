# Simply Music: Looker Studio Dashboard Activity

## Why you are doing this

You are the analyst for **Simply Music**. Leadership wants one interactive page that a sales manager can open, filter, and use in a five-minute standup. This activity is for practice and fun: explore the data, design something readable, and see how interaction changes the story.

You are **not** trying to clone the mockups pixel for pixel. Use them as layout inspiration. Your chart list and the business questions are the real guide.

You can recreate the same questions later in Tableau. For this activity, stay in **Looker Studio**.

## What you will get comfortable with

- Connecting a CSV (or Google Sheet) to Looker Studio
- Fixing field types and building calculated fields
- Scorecards, date controls, dropdown filters, drill-down, cross-filtering, and a map
- Choosing a chart because it answers a question, not because it looks fancy
- Making a single page that a non-technical manager can read

## Scenario

Simply Music sells musical instruments and accessories through its website and three Florida stores: West Palm Beach, Fort Lauderdale, and Tampa.

Your dashboard should help answer:

1. How much did we sell, and how profitable were those sales?
2. How are sales and profit changing over time?
3. Which sales channels, product lines, and products are driving the results?
4. Where are website orders delivered?
5. Which products bring both revenue and a broad customer base?

## Layout guide (hybrid page)

The mockups in this folder show two classic dashboard shapes:

- **Bird's-eye:** trends and channel/location overview
- **Detailed:** product drill-down, rankings, map, customer reach

For class, build **one hybrid 16:9 page** that borrows the best of both:

| Zone | Put here |
|---|---|
| Header | Title (logo text is enough), scorecards, date range, channel and product-line filters |
| Upper body | Revenue and profit over time, revenue (or revenue + profit) by channel |
| Lower body | Product drill-down, top products by profit, customers per product, website delivery map |
| Your choice | One extra insight chart that teaches something the required charts miss |

Open the images any time from [`README.md`](README.md) or the `images/` folder. The Looker bird's-eye screenshot is an example of style and numbers, not a solution key.

Do not copy mockup colours blindly. Use a restrained palette: one primary colour, one highlight colour, neutral background, readable labels, consistent number formats.

## Files

Path from the ClassDemo folder:

`Data Sources/simply_music_combined.csv`

That file is ready to analyse: one row per sales transaction, with date, product, customer, channel, and destination fields already joined.

Optional later (star-schema play):

| File | Role |
|---|---|
| `Data Sources/transactions.csv` | Fact: one row per sales transaction |
| `Data Sources/time.csv` | Date dimension |
| `Data Sources/products.csv` | Product dimension |
| `Data Sources/customers.csv` | Customer dimension |

| From | Key | To |
|---|---|---|
| Transactions | `TIME_KEY` | Time |
| Transactions | `PRODUCT_KEY` | Products |
| Transactions | `CUSTOMER_KEY` | Customers |

`Data Sources/visualization_exercise.xlsx` is only a small field-planning scratch pad if you like sketching ideas before you build. You can ignore it.

## Before you click anything

1. Open [Looker Studio](https://lookerstudio.google.com) and sign in with a Google account.
2. Have `simply_music_combined.csv` ready on disk (or already uploaded to Google Drive).
3. Prefer this path in class: upload the CSV to **Google Sheets** first, then connect that sheet in Looker Studio. Direct **File upload** works in many accounts, but Sheets is usually smoother when several people build at once.

## Part 1: Connect and prepare the data

### Connect

1. Create a blank report (**Create** → **Report**).
2. Add data:
   - **Google Sheets:** pick the sheet that contains the combined data, or
   - **File upload:** upload `simply_music_combined.csv`.
3. When the report opens, rename the data source to **Simply Music Sales**  
   (**Resource** → **Manage added data sources** → edit the name).
4. Open the data source field list and check types. Make these **Number** metrics if they are not already:

   - `UNITS_SOLD`
   - `DOLLARS_SOLD`
   - `COST`
   - `UNIT_PRICE`

### Calculated fields

Still in the data source editor, create these fields. Use the names exactly as written so charts stay easy to share and debug.

| Field name | Formula | Type / role |
|---|---|---|
| `Order Date` | `PARSE_DATE("%Y%m%d", CAST(TIME_KEY AS TEXT))` | Date dimension |
| `Gross Profit` | `DOLLARS_SOLD - (COST * UNITS_SOLD)` | Currency metric |
| `Destination State Clean` | `REGEXP_REPLACE(DESTINATION_STATE, "^US-", "")` | Geo dimension: Country subdivision / Region (US state name) |

Backup date formula if `PARSE_DATE` misbehaves (the combined file already has parts):

```text
DATE(YEAR, MONTH, DAY)
```

Name that field `Order Date` as well if you use the backup, and hide or ignore the other version.

### Date range for the report

1. Set **Order Date** as the report date-range dimension.
2. Set the default range to the full data window: **5 Jan 2018 to 29 Dec 2019**.

### Profit formula (read once)

`DOLLARS_SOLD` is revenue for the whole transaction row.  
`COST` is **cost per unit**.  

So gross profit is:

```text
DOLLARS_SOLD - (COST * UNITS_SOLD)
```

If you forget the `* UNITS_SOLD`, profit will look too high on multi-unit rows.

### Data quirks (you did not break anything)

- Product line is spelled `Accesories` in the source data. Leave it.
- Only **Website** transactions have a delivery state. Store rows have blank destinations on purpose.
- Two state names are misspelled (`Massachussets`, `Lousiana`). They may not plot on the map. That is a data quality Easter egg, not a Looker failure.

## Part 2: Build the dashboard

Use a **16:9 landscape** page. Title idea:

**Simply Music | Sales Performance**  
*Interactive sales, product, channel, and delivery analysis*

A text title is enough. You do not need a logo file.

### A. Controls and interactions

Add these in the header area:

1. **Date range control** bound to `Order Date`
2. **Dropdown list** for `CHANNEL`
3. **Dropdown list** for `PRODUCT_LINE`

On at least one bar chart (product drill-down is a great choice):

1. Select the chart
2. Turn on **cross-filtering** / **Apply filter** in the chart interactions settings
3. Click a bar in View mode and watch the rest of the page react

Add a tiny on-page instruction, for example:

*Click a product or channel bar to filter the rest of the dashboard. Use the header controls to reset the story.*

### B. KPI scorecards

Create four scorecards:

| Scorecard | Metric / chart-level formula | Format |
|---|---|---|
| Total Revenue | `SUM(DOLLARS_SOLD)` | Currency |
| Gross Profit | `SUM(Gross Profit)` | Currency |
| Gross Margin | `SUM(Gross Profit) / SUM(DOLLARS_SOLD)` | Percent, 1 decimal |
| Units Sold | `SUM(UNITS_SOLD)` | Whole number |

**Important:** build Gross Margin as a **ratio of sums**, not an average of row-level margins.

If you have room and want more context, add one of these for fun:

| Scorecard | Formula | Why it is interesting |
|---|---|---|
| Unique Customers | `COUNT_DISTINCT(CUSTOMER_KEY)` | Reach, not only dollars |
| Average Selling Price | `SUM(DOLLARS_SOLD) / SUM(UNITS_SOLD)` | Realised revenue per unit |
| Average Transaction Value | `SUM(DOLLARS_SOLD) / COUNT(TIME_KEY)` | Typical row size (one row ≈ one transaction here) |

### C. Core visualisations

Build these. Resize and rearrange as you like; keep the purpose of each chart.

| Visual | Suggested setup | Business question |
|---|---|---|
| Revenue and profit trend | Time series; dimension `Order Date`; metrics `SUM(DOLLARS_SOLD)` and `SUM(Gross Profit)`; **show by Month** (not every day) | How are revenue and profit changing over time? |
| Revenue by channel | Bar chart; dimension `CHANNEL`; metric `SUM(DOLLARS_SOLD)`; sort descending. Optional upgrade: add `SUM(Gross Profit)` as a second metric | Which channel contributes the most revenue (and profit)? |
| Product drill-down | Bar chart; enable drill-down in this order: `PRODUCT_LINE` → `PRODUCT_TYPE` → `DESCRIPTION`; metric `SUM(DOLLARS_SOLD)`; turn on cross-filtering | Which categories and products sell best? |
| Most profitable products | Horizontal bar; dimension `DESCRIPTION`; metric `SUM(Gross Profit)`; top 10; sort descending | Which products create the most gross profit? |
| Customers per product | Horizontal bar; dimension `DESCRIPTION`; metric `COUNT_DISTINCT(CUSTOMER_KEY)`; top 10 | Which products reach the broadest customer base? |
| Website delivery map | Google Maps bubble map; location `Destination State Clean`; size `SUM(UNITS_SOLD)`; **chart filter** `CHANNEL = Website` | Where do website orders go? |

#### Map tips

- Set the geo type of `Destination State Clean` to a **region / country subdivision (1st level)** style field when Looker offers it.
- Filter the chart to **Website** only. Stores have no delivery state.
- Expect a sparse US map (only about 17 destination states appear in the data).
- Misspelled states may simply not draw. Optional stretch: fix them with a `CASE` calculated field.

#### Drill-down tips

1. Add the three product dimensions to the chart.
2. Enable **Drill down**.
3. Set the default level to `PRODUCT_LINE`.
4. In View mode, use the drill controls to move into product type and description.

### D. One insight visual (your call)

Add **one** chart that teaches something new. Title it as a question or a conclusion, not "Chart 7."

Ideas:

- **100% stacked bar:** revenue mix by `PRODUCT_LINE` and `CHANNEL`
- **Scatter:** revenue vs gross profit, detail on `DESCRIPTION` (high revenue, thin margin products jump out)
- **Table with bars:** product, revenue, gross profit, margin, units
- **Donut:** units by `CHANNEL` (only if labels stay readable)

### E. Optional extras if you are having fun

These appear in the bird's-eye mockups. They are optional:

- Units sold over time (monthly)
- Grouped bar of revenue and profit by channel side by side
- A second page that is pure overview, with this page as the detailed view

## Part 3: Design that feels professional

- Give every visual a title that says what is measured or what question it answers.
- Currency for money, whole numbers for units and customers.
- Skip 3D, rainbow palettes, and more than two accent colours.
- Keep type readable at normal browser zoom.
- Put the headline KPIs at the top; leave a little whitespace so the page can breathe.
- After you build, switch to **View** mode and click around like a manager would.
- Confirm header filters move the charts, and that the map stays about website deliveries.

## Part 4: Reality check (self-check, not a grade)

Clear all filters and use the full date range. Your scorecards should land on these values (formatting may round the display):

| Check | Expected value |
|---|---:|
| Transaction rows | 5,000 |
| Total revenue | $42,889,566 |
| Gross profit | $9,235,989.44 |
| Gross margin | 21.53% |
| Units sold | 6,475 |

If something is off, walk this short list:

1. Is `Order Date` covering 5 Jan 2018 to 29 Dec 2019?
2. Is any chart or page filter still active?
3. Are `DOLLARS_SOLD`, `COST`, and `UNITS_SOLD` numeric?
4. Does Gross Profit multiply `COST` by `UNITS_SOLD`?
5. Is Gross Margin `SUM(profit) / SUM(revenue)`, not an average of row margins?

When the numbers match, go play: filter to Website only, drill into Musical instruments, then into a product type, and watch profit and the map update.

## You're in good shape when...

- The page answers the five scenario questions without explanation from you
- Filters and at least one cross-filter make the dashboard feel interactive
- Scorecards match the reality-check table on the full date range
- The map is clearly about website deliveries
- You would not be embarrassed to share the View link with a classmate

No formal submission is required. Save or share the report if you want to keep it for your portfolio.

## Optional extension: model the star schema in Looker Studio

Only after the hybrid page works with the combined file.

1. Add `transactions.csv`, `time.csv`, `products.csv`, and `customers.csv` as data sources (Sheets or File upload).
2. Start from transactions as the base table.
3. Blend (or join, depending on your Looker Studio UI) to:
   - `time` on `TIME_KEY`
   - `products` on `PRODUCT_KEY`
   - `customers` on `CUSTOMER_KEY`
4. Use a **left outer** relationship from transactions so every sale is kept.
5. Build a **table** first: transaction keys, product description, customer name, revenue. Match row count and revenue to the reality-check table before you chart anything.
6. Recreate `Order Date`, `Gross Profit`, and one chart from the blended source.

### Why this stays optional

Blending is a modelling puzzle on top of visual design. For learning interaction and storytelling, the flat file is the friendlier start. In real projects you usually join or model upstream (warehouse, dbt, semantic layer), then point Looker Studio at the clean result.

## Stuck? Common fixes

| Symptom | Likely cause | What to try |
|---|---|---|
| Date control does nothing | `Order Date` not set as date-range dimension, or charts use raw `TIME_KEY` | Use `Order Date` everywhere; set report date range dimension |
| Revenue huge, profit absurd | `COST` not multiplied by units, or field typed as text | Fix Gross Profit formula; force Number type |
| Margin looks like ~20% of a single row | Averaging row margins | Use `SUM(Gross Profit) / SUM(DOLLARS_SOLD)` |
| Map empty | No Website filter, wrong geo type, or all filters cleared to stores only | Filter map to Website; set geo type; clear other filters |
| Map sparse or missing states | Only 17 states in data; two names misspelled | Expected; optional `CASE` cleanup |
| Drill-down missing | Drill not enabled or only one dimension on the chart | Add all three product fields; enable drill-down |
| Cross-filter does nothing | Interaction off, or you are still in Edit without previewing clicks | Enable Apply filter; test in View mode |
| Counts explode after blend | Join fan-out or wrong join keys | Validate with a table first; left join from transactions only |

## Reference links

- [Looker Studio home](https://lookerstudio.google.com)
- [Create and manage data sources](https://support.google.com/looker-studio/answer/6300774)
- [Calculated fields](https://support.google.com/looker-studio/answer/6299685)
- [PARSE_DATE and date conversion](https://docs.cloud.google.com/data-studio/convert-text-and-numbers-to-date-and-date--time)
- [Report date ranges](https://docs.cloud.google.com/data-studio/set-report-date-ranges)
- [Chart interactions and cross-filtering](https://support.google.com/looker-studio/answer/9173975)
- [Geo field types](https://docs.cloud.google.com/data-studio/geo-dimension-reference)
- [Looker Studio documentation hub](https://lookerstudio.google.com/overview)

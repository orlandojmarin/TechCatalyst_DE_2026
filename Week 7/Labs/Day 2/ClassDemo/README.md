# Simply Music Class Demo

Explore the same sales story in two BI tools. The goal is curiosity and craft, not a graded submission. Build something you would be proud to show a sales manager, then play with filters until the data surprises you.

## Start here

| Order | What | File |
|---|---|---|
| 1 | Looker Studio dashboard build (guided) | [simply_music_looker_studio_activity.md](simply_music_looker_studio_activity.md) |
| 2 | Tableau recreation of the same business questions | Use the mockups below once you are comfortable in Looker Studio |

Data lives in [`Data Sources/`](Data%20Sources/). For the main dashboard, use **`simply_music_combined.csv`**.

## Story

**Simply Music** sells instruments and accessories online and in three Florida stores (West Palm Beach, Fort Lauderdale, Tampa). You are building an interactive sales performance view so a manager can answer:

1. How much did we sell, and how profitable were those sales?
2. How are sales and profit changing over time?
3. Which channels, product lines, and products drive the results?
4. Where do website orders get delivered?
5. Which products reach many customers, not only high revenue?

## Mockups and examples

These images are layout inspiration, not a pixel-perfect checklist. The Looker activity uses a **hybrid single page**: bird's-eye trends at the top, detailed product and delivery analysis below.

### Data model

![Simply Music star schema](images/image-20260805133614804.png)

*Fact table in the centre, with Time, Product, and Customer dimensions.*

### Bird's-eye layout (overview)

![Bird's-eye page mockup](images/image-20260805133624231.png)

![Looker bird's-eye example](images/image-20260805133941644.png)

*Scorecards, date control, revenue/profit over time, units over time, and channel/location bars.*

### Detailed layout (product and delivery)

![Detailed page mockup](images/image-20260805133634382.png)

![Tableau detailed example](images/image-20260805133724116.png)

*Product drill-down, profit ranking, channel mix, customer reach, and a delivery map.*

### Tableau bird's-eye example

![Tableau bird's-eye example](images/image-20260805133904508.png)

*Useful later when you recreate the story in Tableau. Numbers should match the validation checks in the Looker activity.*

## Files

| File | Use it for |
|---|---|
| `Data Sources/simply_music_combined.csv` | Main dashboard (recommended start) |
| `Data Sources/transactions.csv` | Optional star-schema rebuild |
| `Data Sources/time.csv` | Optional star-schema rebuild |
| `Data Sources/products.csv` | Optional star-schema rebuild |
| `Data Sources/customers.csv` | Optional star-schema rebuild |
| `Data Sources/visualization_exercise.xlsx` | Optional scratch pad of field ideas if you like planning on paper first |

## Tips for a smooth session

- Open [Looker Studio](https://lookerstudio.google.com) with a Google account.
- Prefer uploading the CSV to **Google Sheets**, then connecting Sheets in Looker Studio. File upload works for many accounts, but Sheets is more reliable in a classroom.
- Treat colours and exact chart positions as yours to design. Match the **questions**, not the palette.
- When something looks wrong, clear filters and compare to the validation numbers in the activity.
- Source quirks are real: product line is spelled `Accesories`, and two state names are misspelled. That is part of the data, not something you broke.

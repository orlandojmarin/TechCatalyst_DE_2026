# Activity 5: BigQuery ML Hands-On Lab

You will build four machine learning models in BigQuery, one of each major type, and then decide whether you would actually ship them.

**Complete [Activity 4](./Activity_4_BigQueryML_SelfStudy.md) first.** This lab assumes the vocabulary, the metrics, and the train/test discipline from that walkthrough. Section references below point back to it.

Everything runs in the **BigQuery Sandbox**. Write your queries directly in the BigQuery Studio SQL editor.

### What makes this lab different from the walkthrough

In Activity 4 every dataset was prepared to work. Here, three of the four have a real defect waiting for you: a dirty column that silently breaks a model, a dataset with almost no predictive signal, and a missing-value sentinel hiding in plain sight. Finding those is the actual skill.

**The deliverable is not four trained models. It is four judgments about whether each model is trustworthy.**

---

## Setup

```sql
CREATE SCHEMA IF NOT EXISTS `ml`
OPTIONS (location = 'US');
```

Upload these four CSVs from `Week 6/Labs/Day 1/datasets/` via **Add data, then Upload**, with **Auto detect** schema enabled:

| CSV file | Table name | Task |
|----------|-----------|------|
| `regression/mpg.csv` | `ml.car_mpg` | Task 1 |
| `classification/loans.csv` | `ml.loan_applications` | Task 2 |
| `clustering/cereal.csv` | `ml.cereal_nutrition` | Task 3 |
| `timeseries/air_passenger.csv` | `ml.air_passengers` | Task 4 |

**Before writing any model SQL, inspect every schema.** This is not optional here, and Task 1 will show you why:

```sql
SELECT table_name, column_name, data_type
FROM `ml.INFORMATION_SCHEMA.COLUMNS`
WHERE table_name IN ('car_mpg', 'loan_applications', 'cereal_nutrition', 'air_passengers')
ORDER BY table_name, ordinal_position;
```

Auto-detect renames columns containing spaces or parentheses. Use the names this query reports, not the names in the CSV header.

---

## Task 1: Regression, and a Column That Lies

**Table:** `ml.car_mpg`, 398 rows. **Goal:** predict fuel efficiency (`mpg`) from vehicle attributes, then determine which attribute most reduces it.

### Step 1.1: Find the problem before you train

Look at the `data_type` your setup query reported for each column of `car_mpg`.

Four of the five feature columns came back as `INT64` or `FLOAT64`. One did not.

**Identify which column came back as `STRING`, then find out why:**

```sql
SELECT horsepower, COUNT(*) AS n
FROM `ml.car_mpg`
WHERE SAFE_CAST(horsepower AS FLOAT64) IS NULL
GROUP BY horsepower;
```

> **What you should find:** 6 rows where `horsepower` is the literal string `?`.

Six bad values out of 398 changed the type of the entire column, about 1.5 percent of it. This is Decision 2 from Activity 4 Step 3.5, happening for real.

**Why this would wreck the model if you missed it:** a `STRING` feature is treated as **categorical**, not numeric. `LINEAR_REG` would one-hot encode roughly 94 distinct horsepower values into 94 indicator columns, learn a separate meaningless weight for each, and report `NULL` in the `weight` column of `ML.WEIGHTS`. You would get a model, no error message, and a nonsense answer to the business question.

### Step 1.2: Train the model

Build `ml.car_mpg_model` as a `LINEAR_REG` with label `mpg` and features `cylinders`, `displacement`, `horsepower`, `weight`, `acceleration`.

Three requirements:

1. **Repair `horsepower` in the training query** using `SAFE_CAST(horsepower AS FLOAT64)`. `SAFE_CAST` returns `NULL` instead of erroring on `?`, and BQML then imputes those 6 nulls with the column mean (Activity 4 Section 10.1). Alias it back to `horsepower` so `ML.WEIGHTS` stays readable.
2. **Set an explicit split:** `data_split_method = 'RANDOM'` and `data_split_eval_fraction = 0.2`.
3. Do not select any other columns.

**Why requirement 2 is mandatory here:** this table has 398 data rows, which is below the 500-row threshold. Leaving the default `AUTO_SPLIT` means **no holdout at all**, and `ML.EVALUATE` would report training-set metrics while looking completely normal (Activity 4 Step 6.2).

### Step 1.3: Evaluate

Run `ML.EVALUATE` and report `r2_score` and `mean_absolute_error`.

> **What you should see:** `r2_score` roughly **0.61 to 0.75**, `mean_absolute_error` roughly **2.9 to 3.7**.
>
> Because MAE is in real units, read it as: "our mpg estimate is typically off by about 3.5 mpg." Decide for yourself whether that is good enough to put on a car sticker.
>
> Your exact numbers will differ from your neighbor's, because the split is random. Metrics that move a little between runs are normal and expected.

### Step 1.4: Which attribute hurts fuel efficiency most?

This is the business question, and it is where the lab earns its keep.

**First, the default weights:**

```sql
SELECT processed_input, weight
FROM ML.WEIGHTS(MODEL `ml.car_mpg_model`)
ORDER BY ABS(weight) DESC;
```

Write down the top feature.

**Now, standardized weights:**

```sql
SELECT processed_input, weight
FROM ML.WEIGHTS(MODEL `ml.car_mpg_model`, STRUCT(TRUE AS standardize))
ORDER BY ABS(weight) DESC;
```

Write down the top feature again.

> **What you should see, and it should bother you:**
>
> | Ranking | Default weights | Standardized weights |
> |---------|----------------|---------------------|
> | 1 | `cylinders` (about -0.36) | **`weight`** (about -4.5) |
> | 2 | `horsepower` (about -0.039) | `horsepower` (about -1.5) |
> | 3 | `acceleration` (about -0.007) | `cylinders` (about -0.61) |
> | 4 | `displacement` (about -0.0014) | `displacement` (about -0.15) |
> | 5 | **`weight`** (about -0.0054) | `acceleration` (about -0.02) |
>
> **Vehicle weight ranks last by default and first when standardized.** The two queries give opposite answers to the same question, from the same model.
>
> Only the top three of the standardized list are stable. `displacement` and `acceleration` are both near zero, and which of them comes fourth depends on whether you imputed or dropped the six `?` rows. Report the top three; do not build an argument on the bottom two.

**Explain why in your write-up.** The reasoning: the default weight for `weight` is "mpg lost per **one pound**," and one pound is a trivial change across a range spanning 1,613 to 5,140. The default weight for `cylinders` is "mpg lost per **one cylinder**," and cylinders only span 3 to 8, so one unit is a huge change. Ranking raw weights ranks units, not importance. Standardizing converts every weight to "mpg lost per one standard deviation," which is the fair comparison.

**The correct answer to the business question is vehicle weight**, which also matches physical intuition: hauling more mass burns more fuel. The default ordering would have led you to report the wrong driver with total confidence.

### Step 1.5: Predict

Use `ML.PREDICT` on 10 rows, selecting `predicted_mpg` alongside the actual `mpg` and the features. Remember to apply the same `SAFE_CAST` repair to the prediction input that you used in training.

> **What you should see:** predictions in the same ballpark as actuals, off by a few mpg in either direction.
>
> If you omit the `SAFE_CAST` from the prediction input, the query fails rather than returning bad numbers: the model expects a numeric `horsepower` and GoogleSQL will not implicitly convert your `STRING` column to `FLOAT64`. **Features must be prepared identically at training and prediction time**, and forgetting this is one of the most common production ML bugs. Here the type system catches it for you. In a real pipeline the mismatch is usually subtler and silent.

### Stretch: does regularization help?

Train `ml.car_mpg_l2` identically but with `l2_reg = 1.0`, and compare `r2_score` and standardized weights against the original.

`displacement`, `horsepower`, `weight`, and `cylinders` all measure roughly "how big is this engine," which is the multicollinearity case from Activity 4 Section 10.2. Watch whether L2 spreads weight more evenly across the correlated features. Then note whether R² actually improved, and be honest if it did not.

---

## Task 2: Classification, and Deciding Not to Ship

**Table:** `ml.loan_applications`, 100 rows. **Goal:** predict `status` (`approve` or `deny`) from five financial indicators.

> **Read this before you start.** Your job in this task is **not** to produce a good model. It is to determine whether the model you produce is good, and to make a defensible recommendation either way. A data engineer who ships a bad model because nobody checked causes more damage than one who ships nothing.

### Step 2.1: Establish the baseline first

Before training anything, find out what "doing nothing" scores:

```sql
SELECT
  status,
  COUNT(*) AS n,
  ROUND(100 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS pct
FROM `ml.loan_applications`
GROUP BY status;
```

> **What you should see:** about **53 `deny`** and **47 `approve`**.
>
> So a model that ignores every feature and always answers `deny` is **53 percent accurate**. That is the bar. Any model scoring near 53 percent has learned nothing, no matter how sophisticated it looks. Write this number down now, before you see the model's score, so you cannot talk yourself into a bad result later.

### Step 2.2: Train

Build `ml.loan_approval_model` as `LOGISTIC_REG`, label `status`, features `assets`, `liabilities`, `income`, `credit_score`, `mortgage`, with `auto_class_weights = TRUE`.

**Leave the data split at its default this time, and note why in your write-up.** With 100 rows you are far below the 500-row threshold, so BQML will train on all 100 and evaluate on those same 100. You are about to read the most flattering metrics this data can possibly produce. That matters for how you interpret them.

### Step 2.3: Evaluate, and compare against your baseline

Run `ML.EVALUATE` and record `roc_auc`, `accuracy`, `precision`, `recall`, and `f1_score`.

> **What you should see:** `roc_auc` somewhere around **0.60 to 0.70**, and `accuracy` around **0.55 to 0.70**.
>
> Now put those next to what you know:
>
> - ROC AUC of 0.5 is a coin flip (Activity 4 Section 11). You are much closer to 0.5 than to 1.0.
> - Your accuracy is barely above the 53 percent you get by always guessing `deny`.
> - **And these are training-set numbers.** On genuinely unseen applicants, performance would be worse, not better.
>
> **This model has found almost nothing.** That is the correct reading, and arriving at it is the whole point of the task.

### Step 2.4: Watch what happens when you interpret noise anyway

Run the weights, standardized so the ranking is fair:

```sql
SELECT processed_input, weight
FROM ML.WEIGHTS(MODEL `ml.loan_approval_model`, STRUCT(TRUE AS standardize))
ORDER BY weight DESC;
```

> **What you should see:** the three largest weights all have the wrong sign for lending, and the two features a lender would actually underwrite on carry almost no weight at all.
>
> Expect **`liabilities` to be the single largest weight, pushing toward approval** (around +0.5), with `mortgage` and `assets` behind it. Expect **`income` and `credit_score` to sit near zero** (roughly ±0.06), which is a different finding from "negative."
>
> Read the top of the list as a sentence: *"the more debt an applicant carries, the more likely we approve them, and income and credit score barely matter."*

**No responsible lender behaves this way.** The model is not describing lending, it is describing random variation in 100 rows.

Be precise about the near-zero weights, because this is a trap in its own right. A weight of -0.03 is not a small negative effect you can report as "credit score pushes toward denial." **The sign of a near-zero weight is not reproducible**, and if you refit this model on resampled versions of the same 100 rows, those two signs flip roughly a third of the time. The defensible claim is that `income` and `credit_score` carry no weight, while the strongest predictor of approval is debt.

This is what a weights table looks like when there is no signal to find, and the important lesson is that **it looks exactly as authoritative as a real one.** Nothing in the output is flagged, colored, or starred. The only thing standing between this table and a bad business decision is an engineer who checked the baseline and the AUC first.

Also note the features are anonymized values between 0 and 1 with no stated units, so even a good model here could not tell you what "assets of 0.44" means in dollars.

### Step 2.5: Make the call

Run `ML.PREDICT` on 10 applicants, showing `predicted_status`, actual `status`, and the probability for the predicted class. Recall from Activity 4 Step 7.5 that `predicted_status_probs` is an array of structs, so `UNNEST` it.

> **What you should see:** two to four of the ten predictions wrong, and probabilities clustered between about 0.52 and 0.72, which is the model saying "I do not know." Across all 100 applicants no probability lands outside roughly 0.28 to 0.68, so the model is not confident about anyone.

**Now write your recommendation.** Answer, in three or four sentences: would you deploy this model to score real loan applications? Support it with the baseline comparison, the ROC AUC, and the weight signs. State one thing that would have to change before you would revisit the decision, such as more rows, features with real units, or a genuine holdout evaluation.

There is no penalty for concluding the model should not ship. That is the defensible answer here.

### Stretch: see the trade-off curve

Run `ML.ROC_CURVE` and inspect `recall` against `false_positive_rate` across thresholds. On a model with real signal, recall stays high while the false positive rate stays low. Describe what you see instead, and connect it to the AUC you measured.

---

## Task 3: Clustering, and Naming What You Find

**Table:** `ml.cereal_nutrition`, 74 rows. **Goal:** group breakfast cereals by nutrition, then describe the groups in language a shopper would understand.

### Step 3.1: Get the real column names

`cereal.csv` has headers with spaces and parentheses, such as `Protein (g)` and `Vitamins and Minerals`. **Auto-detect rewrote these on upload.** Run the `INFORMATION_SCHEMA` query from Setup, filtered to `cereal_nutrition`, and use exactly the names it reports.

Guessing here produces `Unrecognized name` errors, which is the single most common way to lose time in this task.

### Step 3.2: Find the hidden bad value

```sql
SELECT
  MIN(Calories) AS min_cal, MAX(Calories) AS max_cal,
  MIN(Sugars) AS min_sugar, MAX(Sugars) AS max_sugar,
  MIN(Fat) AS min_fat, MAX(Fat) AS max_fat
FROM `ml.cereal_nutrition`;
```

> **What you should see:** `min_sugar` is **-1**.

A cereal with negative sugar does not exist. This is a **sentinel value**, an old convention where an impossible number stands in for "missing," and this dataset uses `-1`. Find the row:

```sql
SELECT * FROM `ml.cereal_nutrition` WHERE Sugars < 0;
```

> **What you should find:** one row, `Quaker_Oatmeal`.

**Why this matters more for clustering than for regression.** K-Means groups by distance. A false `-1` in a column whose real values run 0 to 15 drags that cereal toward an extreme, and because you are standardizing, it also shifts the mean and standard deviation used for every other row. One bad value distorts the whole model.

Exclude it with `WHERE Sugars >= 0` in your training query, and say in your write-up why you chose to drop the row rather than treat `-1` as real. Note that `SAFE_CAST` would not have helped: `-1` is a perfectly valid number, so nothing errors. **Only knowing the domain catches this one.**

### Step 3.3: Train

Build `ml.cereal_clusters` as `KMEANS` with `num_clusters = 3`, `distance_type = 'EUCLIDEAN'`, `standardize_features = TRUE`, over the five nutrition columns, excluding the bad row.

Two decisions to justify in your write-up:

- **Why `standardize_features = TRUE`:** `Vitamins and Minerals` runs 0 to 100 while `Fat` runs 0 to 5. Without standardizing, the vitamin column would dominate distance and the model would effectively ignore fat, protein, and sugar (Activity 4 Section 8.2).
- **Why `EUCLIDEAN` rather than `COSINE`:** you want cereals with genuinely similar nutritional amounts grouped together, which is straight-line distance. Cosine compares proportions regardless of magnitude, which would call a 50-calorie and a 150-calorie cereal identical if their nutrient ratios matched.

**Do not include `Cereal Name` or `Manufacturer` as features.** They are text, so BQML would one-hot encode them and cluster partly on brand instead of nutrition. You will attach the names back in Step 3.5, where they belong.

### Step 3.4: Read the centroids and name the clusters

Use `ML.CENTROIDS`. The pivoted form from Activity 4 Step 8.3 is much easier to read across clusters than the default long output.

> **What you should see:** three columns of real nutritional values, and your model trained on 73 rows (74 minus the sentinel). Expect one high-sugar, low-protein group, one low-sugar group with the highest protein and lowest calories, and one small heavily fortified group sitting at 100 on vitamins and minerals.

**Give each cluster a plain-English name**, something a shopper would recognize, such as "kids' sugar cereals," "adult health cereals," "fortified brands." Record the name and the two or three centroid values that justify it.

This naming step is the deliverable, not a formality. A cluster you cannot name is a cluster nobody will use (Activity 4 Step 8.3).

### Step 3.5: Assign cereals and check the names make sense

Create `ml.cereal_clustered_results` with `ML.PREDICT`, passing `Cereal Name` and `Manufacturer` through the prediction input so they land in the output next to `CENTROID_ID`. They were not features, so the model ignores them and returns them untouched.

Then look at the members of each cluster:

```sql
SELECT cluster_id, STRING_AGG(cereal_name, ', ' ORDER BY cereal_name LIMIT 8) AS examples
FROM `ml.cereal_clustered_results`
GROUP BY cluster_id
ORDER BY cluster_id;
```

> **This is the moment of truth.** If the cluster you named "kids' sugar cereals" contains Froot Loops and Cap'n Crunch, your interpretation holds. If it contains Shredded Wheat, your names are wrong and you need to revisit them.
>
> **Checking cluster membership against your own knowledge is how you validate an unsupervised model.** There is no accuracy score to lean on, so domain sense is the test.

### Stretch: choose k honestly

Train a 5-cluster version and compare `davies_bouldin_index` against your 3-cluster model, then answer both halves:

1. Which `k` scores better on the index (lower wins)?
2. Can you name all 5 clusters as clearly as you named the 3?

**If the answers disagree, say so and pick interpretability.** Explaining why you overrode a metric is a stronger answer than following it.

---

## Task 4: Forecasting

**Table:** `ml.air_passengers`, 144 rows. **Goal:** forecast monthly airline passengers 12 months beyond the historical record.

### Step 4.1: Inspect, and run the duplicate check

```sql
SELECT
  MIN(date) AS first_month,
  MAX(date) AS last_month,
  COUNT(*) AS n_rows,
  COUNT(DISTINCT date) AS distinct_dates
FROM `ml.air_passengers`;
```

> **What you should see:** 144 rows from **1949-01-31 to 1960-12-31**, with `n_rows` equal to `distinct_dates`.
>
> That equality is the mandatory pre-training check from Activity 4 Step 9.2. `ARIMA_PLUS` requires one row per timestamp.

**Also check the `data_type` of `date` from your setup query.** Because the values are clean `YYYY-MM-DD` strings, auto-detect typed this column as `DATE` already.

**So do not call `PARSE_DATE` on it.** `PARSE_DATE` expects a `STRING`, and passing it a `DATE` fails with `No matching signature for function PARSE_DATE for argument types: STRING, DATE`. Use the column directly. If your upload happened to produce a `STRING`, then and only then convert it.

This is worth internalizing: **check the type, then decide, rather than defensively wrapping conversions around columns that do not need them.** Unnecessary casts fail just as loudly as missing ones.

### Step 4.2: Train

Build `ml.air_passenger_model` as `ARIMA_PLUS` with `time_series_timestamp_col = 'date'` and `time_series_data_col = 'passengers'`.

Set `data_frequency = 'MONTHLY'` explicitly. The dates land on the last day of each month, so the gaps between them vary from 28 to 31 days. Auto-detection generally handles this, but stating the frequency removes the ambiguity and documents your intent.

Also set `decompose_time_series = TRUE`, which you need for the stretch.

Do not set a data split. Time-series models handle sequencing internally, and a random split would train on the future to predict the past (Activity 4 Section 9).

### Step 4.3: Evaluate

Run `ML.EVALUATE` and report `has_seasonality`, `seasonal_periods`, `non_seasonal_p/d/q`, and `AIC`.

> **What you should see:** `has_seasonality` is **true** with a **YEARLY** period.
>
> That is the model confirming what you would see by eye: air travel peaks every summer. **A time-series model that misses obvious seasonality is a red flag**, so this check is your confirmation the model understood the data.

### Step 4.4: Forecast 12 months

Run `ML.FORECAST` with `STRUCT(12 AS horizon, 0.95 AS confidence_level)`, selecting the forecast value and both prediction interval bounds.

> **What you should see:** 12 rows continuing into 1961, following the summer-peak shape, with values above the 1960 level because this series trends upward.
>
> **Look at the interval width in month 1 versus month 12.** It grows noticeably. Explain in your write-up why that is correct behavior rather than a defect.

### Step 4.5: Build the dashboard table

Create `ml.air_passengers_with_forecast` combining historical actuals and the 12-month forecast into one table with a `row_type` column marking each row as `actual` or `forecast`, following the pattern in Activity 4 Step 9.8.

> **What you should see:** 144 `actual` rows followed by 12 `forecast` rows, forming one continuous series.

**This table is the point of the whole lab.** It is production-ready output that a BI tool can chart directly, and you produced it with SQL alone: no export, no Python environment, no model file to deploy. Schedule the query and the forecast refreshes itself.

### Stretch: decompose and detect

1. Run `ML.EXPLAIN_FORECAST` and separate the `trend` component from the yearly seasonal component. Write one sentence a business stakeholder would understand, of the form: "passenger volume grows about X per year, and every summer adds roughly Y more on top."
2. Run `ML.DETECT_ANOMALIES` with `STRUCT(0.95 AS anomaly_prob_threshold)` and report any historical months flagged as unusual. If none are flagged, lower the threshold to 0.8 and try again, then explain what changing that threshold actually did.

---

## Deliverables

Submit to `student-work/week6/day1/` a single file named `bqml_lab.md` containing your queries and your answers.

### Queries

- [ ] **Task 1:** schema inspection, the `?` investigation, `LINEAR_REG` with `SAFE_CAST` and an explicit split, `ML.EVALUATE`, both `ML.WEIGHTS` variants, `ML.PREDICT`.
- [ ] **Task 2:** class baseline query, `LOGISTIC_REG`, `ML.EVALUATE`, standardized `ML.WEIGHTS`, `ML.PREDICT` with unnested probabilities.
- [ ] **Task 3:** schema inspection, sentinel-value investigation, `KMEANS` excluding the bad row, `ML.CENTROIDS`, `ML.EVALUATE`, `ML.PREDICT` persisted to `ml.cereal_clustered_results`.
- [ ] **Task 4:** duplicate-timestamp check, `ARIMA_PLUS`, `ML.EVALUATE`, `ML.FORECAST` with intervals, unified actuals-plus-forecast table.

### Written answers

These are what actually get discussed, so answer them in full sentences.

- [ ] **1a.** Which column in `car_mpg` arrived as `STRING`, why, and what would the model have done if you had not repaired it?
- [ ] **1b.** Which vehicle attribute most reduces fuel efficiency? Give both `ML.WEIGHTS` rankings, explain why they disagree, and state which one answers the question.
- [ ] **1c.** Why did Task 1 require an explicit `data_split_method` when Task 2 did not bother?
- [ ] **2a.** What is the majority-class baseline for `loans`, and how does your model's accuracy compare?
- [ ] **2b.** What does your ROC AUC say about how much signal exists in this data?
- [ ] **2c.** Read the weight signs aloud as a sentence about lending. Is it plausible? What does that tell you?
- [ ] **2d.** **Would you deploy this model?** Three to four sentences, citing baseline, AUC, and weight signs, plus one thing that would have to change for you to reconsider.
- [ ] **3a.** What value did you find in `Sugars`, why is it there, and why does it damage a clustering model more than it would damage a regression?
- [ ] **3b.** Name your three clusters in plain English, with the centroid values that justify each name.
- [ ] **3c.** Do the actual cereals in each cluster match your names? Give one example that confirms it, or one that forced you to rename.
- [ ] **4a.** Why does `PARSE_DATE` fail on this table, and how did you know before running it?
- [ ] **4b.** Why do the forecast confidence intervals widen further into the future, and why is that correct?
- [ ] **4c.** Why can you not use a random train/test split on a time series?

### Stretch (optional)

- [ ] Task 1 L2 comparison, Task 2 ROC curve, Task 3 five-cluster comparison, Task 4 decomposition and anomaly detection.

---

## Success Criteria

You have finished when:

1. Four models exist in your `ml` dataset and every task's expected-output check matched.
2. You found all three data defects: the `?` in `horsepower`, the near-zero signal in `loans`, and the `-1` in `Sugars`.
3. You can explain the `ML.WEIGHTS` ranking reversal in Task 1 and say which ranking is correct.
4. You wrote a defensible ship-or-no-ship recommendation for the loan model.
5. You named your cereal clusters and checked the names against actual cluster members.
6. `ml.air_passengers_with_forecast` contains 144 actual rows and 12 forecast rows.

**The models are the easy part.** Every one of them is 6 to 12 lines of SQL. What you are practicing is the habit of checking a model before trusting it, which is the part that separates a data engineer from someone who can copy a `CREATE MODEL` statement.

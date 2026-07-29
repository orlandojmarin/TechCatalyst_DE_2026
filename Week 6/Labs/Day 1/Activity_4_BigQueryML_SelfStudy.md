# Activity 4: BigQuery ML (BQML) Self-Study Walkthrough

This is a guided, self-paced walkthrough. You will build seven machine learning models inside BigQuery using nothing but GoogleSQL, and more importantly, you will learn how to read what they tell you.

**No prior machine learning experience is assumed.** Section 2 gives you every term you need. Work top to bottom, run every query, and compare what you get against the "What you should see" box under each step. If your numbers are wildly different from the expected range, something upstream went wrong, and the troubleshooting table in Section 12 will usually tell you what.

---

## 1. Why BigQuery ML Matters to a Data Engineer

Here is the normal way a machine learning model reaches production:

1. Export a few million rows out of the warehouse to CSV or Parquet.
2. Move that file to a machine with Python, pandas, and scikit-learn.
3. Train a model in a notebook.
4. Save the trained model as a pickle or joblib file.
5. Build a serving container or a batch job that loads the pickle.
6. Write the predictions back into the warehouse so the dashboard can read them.

Six steps, at least three environments, one file format conversion, and a pickle file that somebody now has to version, store, and keep in sync with the code that created it.

BigQuery ML collapses that to this:

```sql
CREATE OR REPLACE MODEL `ml.my_model` OPTIONS(...) AS SELECT ... ;  -- train
CREATE OR REPLACE TABLE `ml.predictions` AS SELECT * FROM ML.PREDICT(MODEL `ml.my_model`, (SELECT ...));  -- serve
```

The model is an **object that lives in your dataset**, right next to your tables. You can see it in the BigQuery console. Prediction is a table function, which means predictions can be joined, filtered, and aggregated like any other table, and shipping them to production is `CREATE TABLE AS SELECT`.

That is the real payoff, and it is worth being precise about what disappears: no export, no file format conversion, no pickle file, no serving container, no second environment to keep in sync, and no egress cost. You will feel this most in Section 9, where you produce one table that a dashboard can chart directly, containing both historical actuals and future forecasts.

### The honest trade-off

BQML is not a replacement for Python ML. You get a fixed catalog of model types and far less control over the training loop than scikit-learn or PyTorch gives you. What you get in exchange is that the model lives where the data lives, and a SQL-literate team can maintain it. For the large class of business problems solved by a regression, a classifier, a clustering, or a forecast, that trade is usually worth it.

---

## 2. The Vocabulary You Need First

Read this section before writing any SQL. Everything later assumes these seven terms.

| Term | Plain meaning | In this walkthrough |
|------|---------------|---------------------|
| **Feature** | An input column the model is allowed to look at. Also called a predictor. | `years_experience`, `JobLevel`, `Age` |
| **Label** | The answer column you want the model to produce. Also called the target. | `salary`, `MonthlyIncome`, `target` |
| **Training** | Showing the model many rows where you already know the answer, so it can learn the pattern connecting features to label. | `CREATE MODEL ... AS SELECT` |
| **Inference (prediction)** | Asking the trained model for an answer on a row it has not seen. | `ML.PREDICT` |
| **Model** | The saved set of learned numbers (weights) that turns features into a prediction. Not code, just numbers. | An object in your `ml` dataset |
| **Supervised learning** | You have a label. The model learns to reproduce it. | Sections 5, 6, 7 |
| **Unsupervised learning** | You have no label. The model finds structure on its own. | Section 8 (clustering) |

### The one idea that makes everything else click

A model is just a **set of numbers**. For the simplest model you will build in Section 5, the model is literally two numbers:

```
predicted_salary = 25792 + 9450 * years_experience
```

Training means "find the best values for 25792 and 9450." Inference means "plug a number into that formula." Everything else in this walkthrough, forecasting, classification, clustering, is a more elaborate version of the same two-part idea: **learn some numbers, then apply them.**

When you run `ML.WEIGHTS` later, you are literally looking at those numbers. That is not a debugging tool, it is the model itself.

### Supervised vs unsupervised, made concrete

You will use the same `employee_data` table twice, which makes the difference impossible to miss:

- **Section 6 (supervised):** "Here are 1,470 employees and their salaries. Learn to predict salary." You have an answer key, so you can measure whether the model is right.
- **Section 8 (unsupervised):** "Here are the same 1,470 employees. No salary, no answer key. Group them into 4 similar types." There is nothing to be right *about*, so you judge the result by whether the groups are useful and nameable.

---

## 3. Setup

### 3.1 What you need

Everything runs in the **BigQuery Sandbox**, which is free and requires no credit card, or in a normal Google Cloud project if you have one. Open [BigQuery Studio](https://console.cloud.google.com/bigquery) in Chrome.

### 3.2 Cost and sandbox limits

Read this before you start so nothing surprises you:

- The sandbox gives you 10 GB of storage and 1 TB of query processing per month, free. Every dataset in this walkthrough is tiny (the largest is 1,470 rows), so you will not come close to either limit.
- **In the sandbox, tables and models expire automatically after 60 days.** That is fine for a class exercise, but do not build anything you need long term here.
- `CREATE MODEL` is billed differently from a normal query in a paid project. It is free in the sandbox, but check the [BQML pricing page](https://cloud.google.com/bigquery/pricing#bqml) before you run `CREATE MODEL` against a real project at work.

### 3.3 Create your dataset, and watch the region

```sql
CREATE SCHEMA IF NOT EXISTS `ml`
OPTIONS (location = 'US');
```

**The `location = 'US'` matters.** In Section 9 you will query `bigquery-public-data`, which lives in the US multi-region. BigQuery cannot join or query across regions. If you create your `ml` dataset in `EU` or `us-east1`, that section fails with a confusing "Not found: Dataset" or "dataset not found in location" error, and the cause is not obvious from the message. Create it in `US` and this never comes up.

### 3.4 Load the tables

Upload each CSV from `Week 6/Labs/Day 1/datasets/` using the BigQuery console: **Add data, then Upload, choose the file, set Format to CSV, expand Advanced options, and check "Auto detect" for the schema.**

| CSV file | Table name to use | Used in |
|----------|-------------------|---------|
| `regression/salary_data.csv` | `ml.salary_data` | Section 5 |
| `clustering/employee_data.csv` | `ml.employee_data` | Sections 6 and 8 |
| `classification/usage_stats.csv` | `ml.usage_stats` | Section 7 |
| `timeseries/milk_production.csv` | `ml.milk_production` | Section 9 |

### 3.5 Always check your schema after upload

Do this once now, and make it a habit. Auto-detect makes two decisions on your behalf that will bite you later if you do not look.

```sql
SELECT column_name, data_type
FROM `ml.INFORMATION_SCHEMA.COLUMNS`
WHERE table_name = 'usage_stats';
```

**Decision 1: column names get normalized.** BigQuery column names cannot contain spaces or parentheses. When your CSV header has `Usage Stats` or `Protein (g)`, BigQuery rewrites it, usually turning invalid characters into underscores. Do not guess what it became. Run the query above and use the names it reports.

**Decision 2: one bad value changes a column's type.** If a numeric column contains even a single `?` or `N/A`, auto-detect types the entire column as `STRING`, silently. A model will then treat that column as a category instead of a number and produce nonsense. You will see exactly this happen in Activity 5.

> **What you should see:** three feature columns plus `target` for `usage_stats`. Note the exact spelling of the feature columns, because you will type them in Section 7.

---

## 4. How to Read This Walkthrough

Each of the next five sections builds one model type, in increasing order of difficulty:

| Section | Model type | Question it answers | Learning |
|---------|-----------|---------------------|----------|
| 5 | `LINEAR_REG` | Predict a number | Your first model, in 6 lines |
| 6 | `LINEAR_REG` | Predict a number, honestly | Train/test split, overfitting, reading weights |
| 7 | `LOGISTIC_REG` | Predict a category | Probabilities, thresholds, imbalanced classes |
| 8 | `KMEANS` | Find groups, no answer key | Unsupervised learning, naming segments |
| 9 | `ARIMA_PLUS` | Predict the future | Time series, seasonality, anomalies |

Regression comes first because it is the most intuitive. Time series comes last because it has the most moving parts, not because it is the most important.

---

## 5. Section 5: Your First Model

**Dataset:** `ml.salary_data`, 30 rows, 2 columns. **Question:** given someone's years of experience, what salary should we expect?

This dataset is deliberately tiny and obvious so that you can check the model's reasoning against your own intuition.

### 5.1 Look at the data first

Never train on a table you have not looked at.

```sql
SELECT * FROM `ml.salary_data` ORDER BY years_experience;
```

> **What you should see:** 30 rows, experience from about 1.1 to 10.5 years, salary from about $37,700 to $122,400. Salary clearly rises with experience. You could almost draw the line yourself, and that is the point.

### 5.2 Train the model

```sql
CREATE OR REPLACE MODEL `ml.salary_model`
OPTIONS(
  model_type = 'LINEAR_REG',
  input_label_cols = ['salary']
) AS
SELECT
  years_experience,
  salary
FROM `ml.salary_data`;
```

Three things to notice, because this pattern repeats in every model you build today:

1. `model_type` picks the algorithm. `LINEAR_REG` predicts a number.
2. `input_label_cols` names the answer column. **Every other column in the SELECT automatically becomes a feature.** There is no separate "features" option, so if you do not want a column used, do not select it.
3. The `AS SELECT` at the end is the training data. Any query works here, including joins and CTEs.

### 5.3 Look at the model you just built

```sql
SELECT
  processed_input,
  weight
FROM ML.WEIGHTS(MODEL `ml.salary_model`);
```

> **What you should see:** two rows. `years_experience` with a weight near **9450**, and `__INTERCEPT__` near **25792**.
>
> Read it out loud: *"Start everyone at about $25,800, then add about $9,450 for every year of experience."* That sentence is the entire model. This is what people mean when they call linear regression interpretable.

### 5.4 Evaluate it

```sql
SELECT
  r2_score,
  mean_absolute_error
FROM ML.EVALUATE(MODEL `ml.salary_model`);
```

> **What you should see:** `r2_score` around **0.96**, `mean_absolute_error` around **$4,600**.
>
> **R² (r-squared)** answers "what fraction of the variation in salary did the features explain?" It runs 0 to 1. 0.96 means experience alone explains 96 percent of the salary differences here, which is unusually high because this is a teaching dataset. Real business data rarely does this well.
>
> **MAE** is in real units: the model's typical miss is about $4,600.

Notice that MAE is the number you would actually quote to a stakeholder. "Our salary estimate is typically off by about $4,600" is a sentence a hiring manager can act on. "Our R² is 0.96" is not.

### 5.5 Predict

```sql
SELECT
  years_experience,
  ROUND(predicted_salary, 0) AS predicted_salary
FROM ML.PREDICT(
  MODEL `ml.salary_model`,
  (SELECT * FROM UNNEST([2.0, 5.0, 8.0]) AS years_experience)
);
```

> **What you should see:** roughly $44,700, $73,000, and $101,400.
>
> The output column is named `predicted_` plus your label column name. That naming rule holds for every BQML model, so a model with label `mpg` produces `predicted_mpg`.

Check the math yourself: 25792 + 9450 × 5 = 73,042. The model is doing exactly what Section 2 said it would.

### 5.6 A warning about this model

You just evaluated the model on the same 30 rows you trained it on. That is like grading a student on the exact questions they studied. The 0.96 is real, but it is not evidence the model works on new people.

Section 6 fixes this, and it is the most important section in this walkthrough.

---

## 6. Section 6: Honest Evaluation, Train/Test Split, and Overfitting

**Dataset:** `ml.employee_data`, 1,470 rows. **Question:** predict an employee's `MonthlyIncome`.

### 6.1 The problem with what we just did

A model can succeed two ways. It can **learn the real pattern**, which works on new data, or it can **memorize the training rows**, which does not. Both look identical if you only ever test on training data.

Memorizing instead of learning is called **overfitting**, and it is the single most common way machine learning projects fail quietly.

The fix is simple and non-negotiable: **hold some rows back.** Train on most of the data, then evaluate on rows the model has never seen. If it does well on both, it learned. If it does well on training but poorly on held-out data, it memorized.

### 6.2 The BQML trap you must know about

BQML's default is `data_split_method = 'AUTO_SPLIT'`, and here is what that actually does:

| Rows in training query | What AUTO_SPLIT does |
|------------------------|----------------------|
| Fewer than 500 | **All rows used for training. No holdout at all.** |
| 500 to 50,000 | 20 percent held out for evaluation |
| More than 50,000 | 10,000 rows held out for evaluation |

Read the first row again. **On a small table, `ML.EVALUATE` reports training-set metrics**, and nothing in the output warns you. Your Section 5 model had 30 rows, so its 0.96 was a training score.

This is why several datasets in Activity 5 need an explicit split: `mpg` has 397 rows, `loans` has 100, and `cereal` has 73. All three are below the threshold.

`employee_data` has 1,470 rows, so AUTO_SPLIT gives you a genuine 20 percent holdout. Let us use it and see the difference for real.

### 6.3 Train with a real holdout

```sql
CREATE OR REPLACE MODEL `ml.income_model`
OPTIONS(
  model_type = 'LINEAR_REG',
  input_label_cols = ['MonthlyIncome'],
  data_split_method = 'RANDOM',
  data_split_eval_fraction = 0.2
) AS
SELECT
  Age,
  JobLevel,
  DistanceFromHome,
  JobSatisfaction,
  Department,
  MonthlyIncome
FROM `ml.employee_data`;
```

Being explicit with `RANDOM` and `data_split_eval_fraction` is a good habit even when AUTO_SPLIT would have done the right thing, because it makes the split visible to whoever reads your SQL next.

Also notice `Department` is a **text column**. You did not have to encode it. BQML one-hot encodes strings automatically, which Section 10 explains.

### 6.4 Evaluate on data the model never saw

```sql
SELECT
  r2_score,
  mean_absolute_error
FROM ML.EVALUATE(MODEL `ml.income_model`);
```

> **What you should see:** `r2_score` around **0.89**, `mean_absolute_error` around **$1,200**.
>
> This 0.89 means something the Section 5 number did not. It was measured on roughly 294 employees the model never trained on. You can defend this number in a meeting.

### 6.5 See overfitting with your own eyes

Compare held-out performance against training performance directly:

```sql
-- Performance on the held-out 20 percent (the honest number)
SELECT 'eval (unseen rows)' AS measured_on, r2_score, mean_absolute_error
FROM ML.EVALUATE(MODEL `ml.income_model`)

UNION ALL

-- Performance on the full original table (mostly rows it trained on)
SELECT 'train (seen rows)', r2_score, mean_absolute_error
FROM ML.EVALUATE(
  MODEL `ml.income_model`,
  (SELECT Age, JobLevel, DistanceFromHome, JobSatisfaction, Department, MonthlyIncome
   FROM `ml.employee_data`)
);
```

> **What you should see:** two rows with **similar** scores, roughly 0.89 and 0.91.
>
> A small gap like this is healthy and expected. It means the model learned a real pattern rather than memorizing.
>
> **What a problem looks like:** train R² of 0.99 next to eval R² of 0.55. That gap is the signature of overfitting, and it is the diagnostic you just learned to run. Any time someone shows you a model with only one score, ask which set it was measured on.

### 6.6 Reading feature weights, and the trap that reverses your answer

Now ask the obvious business question: **what actually drives income here?**

```sql
SELECT
  processed_input,
  weight
FROM ML.WEIGHTS(MODEL `ml.income_model`)
ORDER BY ABS(weight) DESC;
```

> **What you should see:** `JobLevel` dominating at roughly **+4000**, `Age` near +9, `DistanceFromHome` near -16, `JobSatisfaction` near -48, plus a `category_weights` entry for `Department`.
>
> Reading: each step up in job level is worth about $4,000 a month. Age adds about $9 a month per year, which is nearly nothing once job level is accounted for.

**Here is the trap.** By default, `ML.WEIGHTS` returns weights **in each feature's original units**. A weight is "dollars per one unit of this feature," and every feature has a different unit. `JobLevel` moves 1 to 5. `Age` moves 18 to 60. Comparing their raw weights is comparing dollars-per-level against dollars-per-year, which is not a fair comparison.

To rank features by actual influence, ask for standardized weights:

```sql
SELECT
  processed_input,
  weight
FROM ML.WEIGHTS(MODEL `ml.income_model`, STRUCT(TRUE AS standardize))
ORDER BY ABS(weight) DESC;
```

`STRUCT(TRUE AS standardize)` rescales every weight to "dollars per one standard deviation of this feature," which puts all features on a common footing.

> **What you should see:** `JobLevel` still on top, but the others reorder.
>
> In this dataset the ranking barely changes, because `JobLevel` overwhelms everything. **Do not conclude that the option does not matter.** In Activity 5 you will meet a model where the default ordering and the standardized ordering give *completely opposite* answers, and the default one is wrong. Remember this option exists.

**Rule to carry forward:** use the default weights to state what a feature is worth in business units. Use standardized weights to rank features against each other. Mixing those two up produces confident, wrong conclusions.

---

## 7. Section 7: Classification, Probabilities, and Thresholds

**Dataset:** `ml.usage_stats`, 1,210 rows. **Question:** predict the `target` column, which is 1 or 0.

Regression predicts a number. **Classification predicts a category.** Under the hood it does something subtler and more useful: it predicts a *probability* for each category, then converts that to a label.

### 7.1 Look at the data, especially the balance

```sql
SELECT
  target,
  COUNT(*) AS rows,
  ROUND(100 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS pct
FROM `ml.usage_stats`
GROUP BY target;
```

> **What you should see:** about **1,089 rows of class 0 (90 percent)** and **121 rows of class 1 (10 percent)**.

This imbalance is the most important thing about this dataset, and it sets up the lesson in 7.4.

### 7.2 Train the classifier

Use the exact feature column names you found in Step 3.5.

```sql
CREATE OR REPLACE MODEL `ml.usage_model`
OPTIONS(
  model_type = 'LOGISTIC_REG',
  input_label_cols = ['target'],
  auto_class_weights = TRUE,
  data_split_method = 'RANDOM',
  data_split_eval_fraction = 0.2
) AS
SELECT * FROM `ml.usage_stats`;
```

`auto_class_weights = TRUE` tells the model to treat the rare class as equally important despite being outnumbered 9 to 1. Without it, a model can score well by mostly ignoring the rare class, which is usually the class you actually care about (fraud, churn, a claim that will escalate).

### 7.3 Evaluate

```sql
SELECT *
FROM ML.EVALUATE(MODEL `ml.usage_model`);
```

> **What you should see:** `roc_auc` around **0.99**, with precision, recall, and accuracy all high.

Here is what each metric means, and when to use which:

| Metric | Question it answers | Use it when |
|--------|--------------------|-----------------|
| **Accuracy** | What fraction of all predictions were right? | Classes are roughly balanced. Misleading otherwise, see 7.4 |
| **Precision** | When the model said "yes," how often was it right? | A false alarm is expensive (wrongly denying a valid claim) |
| **Recall** | Of all the real "yes" cases, how many did we catch? | A miss is expensive (letting fraud through) |
| **F1** | Single score balancing precision and recall | You need one number and both errors matter |
| **ROC AUC** | Across every possible threshold, how well does the model separate the two classes? | Judging overall model quality. **0.5 means coin flip, 1.0 means perfect** |

**ROC AUC is the one to anchor on**, because it does not depend on where you set the threshold. A 0.99 here means the model separates the classes almost perfectly.

### 7.4 Why accuracy alone will fool you

Ask what a model that does no work at all would score:

```sql
SELECT
  ROUND(100 * COUNTIF(target = 0) / COUNT(*), 1) AS accuracy_of_always_guessing_zero
FROM `ml.usage_stats`;
```

> **What you should see: 90.0 percent.**

A model that ignores every feature and always answers 0 is 90 percent accurate on this data. If someone reports "90 percent accuracy" here, they have reported the accuracy of doing nothing.

**Always compare accuracy against the majority-class baseline.** It is one query, and it is the fastest way to catch a worthless model. This is why ROC AUC is the better headline metric: always-guess-zero scores 0.5 AUC, exactly as it deserves.

### 7.5 Predictions are probabilities, not just labels

```sql
SELECT
  predicted_target,
  prob AS confidence,
  Customer_Rank
FROM ML.PREDICT(
  MODEL `ml.usage_model`,
  (SELECT * FROM `ml.usage_stats` LIMIT 10)
),
UNNEST(predicted_target_probs)
WHERE label = 1
ORDER BY prob DESC;
```

Two things to unpack, because the output shape surprises everyone the first time:

1. `predicted_target` is the final label, chosen by taking the highest-probability class.
2. `predicted_target_probs` is an **array of structs**, one entry per class, each with a `label` and a `prob`. In the console it renders as a nested cell that looks broken. It is not. You `UNNEST` it and filter to the class you care about, as above.

The probability is more useful than the label. "This account has an 0.87 chance of being class 1" supports a business decision that a bare "1" does not.

### 7.6 The threshold is a business decision, not a model decision

By default the model calls anything above **0.5** a 1. That default is arbitrary, and changing it trades precision against recall:

- **Lower the threshold to 0.3:** catch more real positives (higher recall), accept more false alarms (lower precision).
- **Raise it to 0.7:** fewer false alarms (higher precision), miss more real cases (lower recall).

`ML.ROC_CURVE` shows you the whole trade-off at once:

```sql
SELECT
  threshold,
  recall,
  false_positive_rate,
  true_positives,
  false_positives,
  false_negatives
FROM ML.ROC_CURVE(MODEL `ml.usage_model`)
WHERE threshold BETWEEN 0.1 AND 0.9
ORDER BY threshold;
```

> **What you should see:** as `threshold` rises, `recall` falls and `false_positive_rate` falls with it.

Which threshold is right is not a question the model can answer. It depends on what a miss costs versus what a false alarm costs, and that is a conversation with the business, not a hyperparameter.

---

## 8. Section 8: Clustering, Learning Without an Answer Key

**Dataset:** `ml.employee_data` again, 1,470 rows. **Question:** are there natural employee groups in this data?

This is the same table from Section 6, deliberately. There we had `MonthlyIncome` as the answer key. Here we throw the answer key away and ask the model to find structure by itself.

### 8.1 What K-Means actually does

Plain version, no math:

1. You pick a number of groups, `k`. Say 4.
2. The algorithm drops 4 points at random into the data, called **centroids**.
3. Every row joins whichever centroid it is closest to.
4. Each centroid moves to the average position of its members.
5. Repeat 3 and 4 until nothing moves.

The result is `k` groups where members resemble each other more than they resemble other groups. A **centroid** is the average member of its group, which is exactly why centroids are how you interpret the result.

### 8.2 Train the model

```sql
CREATE OR REPLACE MODEL `ml.employee_clusters`
OPTIONS(
  model_type = 'KMEANS',
  num_clusters = 4,
  distance_type = 'EUCLIDEAN',
  standardize_features = TRUE
) AS
SELECT
  Age,
  MonthlyIncome,
  DistanceFromHome,
  JobLevel,
  JobSatisfaction
FROM `ml.employee_data`;
```

Note there is no `input_label_cols`. That is the signature of unsupervised learning: no answer column exists.

**Why `standardize_features = TRUE` is essential here.** `MonthlyIncome` runs 1,009 to 19,999. `JobSatisfaction` runs 1 to 4. Distance is dominated by whichever feature has the biggest raw numbers, so without standardizing, this model would cluster on income alone and quietly ignore the other four features. Standardizing puts every feature on the same scale so each gets a fair vote. **Leave this on unless you have a specific reason not to.**

**Why `EUCLIDEAN` and not `COSINE`.** Euclidean is straight-line distance, which is what "similar employees" means here. Cosine measures the *angle* from the origin, which is right when you care about proportions rather than magnitudes, like text documents or a customer's spending *mix*. When in doubt, start with Euclidean.

### 8.3 Interpret the clusters, which is the real work

```sql
SELECT
  centroid_id,
  feature,
  ROUND(numerical_value, 1) AS centroid_value
FROM ML.CENTROIDS(MODEL `ml.employee_clusters`)
ORDER BY feature, centroid_id;
```

Or pivoted, which is much easier to read across clusters:

```sql
SELECT
  feature,
  ROUND(MAX(IF(centroid_id = 1, numerical_value, NULL)), 1) AS cluster_1,
  ROUND(MAX(IF(centroid_id = 2, numerical_value, NULL)), 1) AS cluster_2,
  ROUND(MAX(IF(centroid_id = 3, numerical_value, NULL)), 1) AS cluster_3,
  ROUND(MAX(IF(centroid_id = 4, numerical_value, NULL)), 1) AS cluster_4
FROM ML.CENTROIDS(MODEL `ml.employee_clusters`)
GROUP BY feature
ORDER BY feature;
```

> **What you should see:** four columns of real, readable numbers. One cluster will show high `MonthlyIncome` and high `JobLevel`, another low income and low job level, and others will separate on `Age` or `DistanceFromHome`.
>
> Because you clustered on real units, you can read these directly: a centroid with `MonthlyIncome` near 17,000 and `JobLevel` near 4.5 is your senior leadership group.

**Your job now is to name each cluster.** Something like "senior leadership," "early-career close to the office," "long-commute mid-career." If you cannot write a plain-English name for a cluster, that is a real finding, and it usually means `k` is wrong.

A clustering nobody can describe is a clustering nobody will use. Naming the segments *is* the deliverable, not the model.

### 8.4 Check the quality

```sql
SELECT
  davies_bouldin_index,
  mean_squared_distance
FROM ML.EVALUATE(MODEL `ml.employee_clusters`);
```

**Davies-Bouldin index** measures how tight and well-separated the clusters are. **Lower is better.** There is no universal "good" value, so it is only meaningful as a comparison between two models on the same data, which is why you always try more than one `k`.

### 8.5 Choose k by comparing

```sql
CREATE OR REPLACE MODEL `ml.employee_clusters_k3`
OPTIONS(model_type = 'KMEANS', num_clusters = 3,
        distance_type = 'EUCLIDEAN', standardize_features = TRUE) AS
SELECT Age, MonthlyIncome, DistanceFromHome, JobLevel, JobSatisfaction
FROM `ml.employee_data`;

SELECT 'k=3' AS model, davies_bouldin_index FROM ML.EVALUATE(MODEL `ml.employee_clusters_k3`)
UNION ALL
SELECT 'k=4', davies_bouldin_index FROM ML.EVALUATE(MODEL `ml.employee_clusters`);
```

Lower wins, but only as a tiebreaker. **If k=3 scores slightly worse but produces three groups you can name and act on, while k=4 produces four you cannot, use k=3.** Interpretability beats a marginal metric improvement in clustering, because the output is meant for humans.

### 8.6 Assign rows and persist

`ML.PREDICT` passes through any extra columns you select, which lets you keep identifying columns alongside the assignment:

```sql
CREATE OR REPLACE TABLE `ml.employee_segments` AS
SELECT
  CENTROID_ID AS cluster_id,
  EmployeeID,
  Department,
  Age,
  MonthlyIncome,
  JobLevel
FROM ML.PREDICT(
  MODEL `ml.employee_clusters`,
  (SELECT EmployeeID, Department, Age, MonthlyIncome,
          DistanceFromHome, JobLevel, JobSatisfaction
   FROM `ml.employee_data`)
);

-- Sanity check: how big is each cluster, and does the profile make sense?
SELECT
  cluster_id,
  COUNT(*) AS employees,
  ROUND(AVG(MonthlyIncome), 0) AS avg_income,
  ROUND(AVG(Age), 1) AS avg_age
FROM `ml.employee_segments`
GROUP BY cluster_id
ORDER BY cluster_id;
```

`EmployeeID` and `Department` were not features. The model ignores them and hands them back untouched, which is how you join results to anything else.

> **Watch for:** one cluster holding 95 percent of the rows, or a cluster with 3 members. Both mean `k` needs to change or a feature is dominating.

### 8.7 When your features arrive pre-scaled

Open `datasets/clustering/wholesale_customers.csv` and look at the values. They are mostly small numbers, many negative, centered near zero. That file has **already been standardized** by whoever produced it, so each value is "standard deviations from average," not dollars.

You will receive data like this constantly, and it changes how you read the output:

- A centroid value of `+1.5` means "1.5 standard deviations above average," not "$1.50."
- You can still say "this cluster spends well above average on Grocery."
- You **cannot** say "this cluster spends $8,000 on Grocery," and no query will recover that, because the original scale is gone.
- `standardize_features` is effectively a no-op, since the data is already standardized.

**The lesson: always ask whether a numeric column is in real units before you interpret a model built on it.** If you need to report findings in dollars, you need the raw table, and that is a conversation to have with the data's owner *before* you build the model.

---

## 9. Section 9: Time-Series Forecasting

**Datasets:** `ml.milk_production` and a BigQuery public dataset. **Question:** what happens next?

Time series is different from everything above in one crucial way: **row order matters.** In Sections 5 through 8, shuffling the rows changes nothing. Here, the sequence *is* the signal.

That also means a random train/test split is invalid. You cannot train on the future to predict the past. `ARIMA_PLUS` handles this internally, which is why you never specify a split for it.

### 9.1 What ARIMA_PLUS does for you

`ARIMA_PLUS` is highly automated. Given a date column and a value column it will detect trend, detect seasonality (weekly, monthly, yearly), model holiday effects, fill in missing timestamps, handle spikes and step changes, and select its own parameters. That is a lot of statistics you are getting for two lines of options.

### 9.2 Look at the data first

```sql
SELECT
  MIN(month) AS first_month,
  MAX(month) AS last_month,
  COUNT(*) AS n_months,
  COUNT(DISTINCT month) AS distinct_months
FROM `ml.milk_production`;
```

> **What you should see:** 168 rows from 1962-01 to 1975-12, and `n_months` equal to `distinct_months`.
>
> **That last check matters.** `ARIMA_PLUS` requires **one row per timestamp**. Duplicate dates cause a training error. Run this check on every time series before you train, because the error message you get otherwise is not obvious.

### 9.3 Train, with options explained

```sql
CREATE OR REPLACE MODEL `ml.milk_ts`
OPTIONS(
  model_type = 'ARIMA_PLUS',
  time_series_timestamp_col = 'month',
  time_series_data_col = 'production',
  data_frequency = 'MONTHLY',
  auto_arima = TRUE,
  decompose_time_series = TRUE,
  adjust_step_changes = TRUE,
  holiday_region = 'US'
) AS
SELECT month, production
FROM `ml.milk_production`;
```

| Option | What it does |
|--------|--------------|
| `time_series_timestamp_col` | The date column |
| `time_series_data_col` | The numeric column being forecast |
| `data_frequency = 'MONTHLY'` | States the spacing. Auto-detection usually works, but stating it is safer and self-documenting |
| `auto_arima = TRUE` | Tries many parameter combinations and keeps the best. On by default, shown here for visibility |
| `decompose_time_series = TRUE` | Required to use `ML.EXPLAIN_FORECAST` in 9.6 |
| `adjust_step_changes = TRUE` | Handles permanent level shifts, like a plant coming online |
| `holiday_region = 'US'` | Models US holiday effects. Matters for daily retail data, minor for monthly milk |

### 9.4 Evaluate

```sql
SELECT * FROM ML.EVALUATE(MODEL `ml.milk_ts`);
```

Time-series evaluation looks nothing like regression evaluation, so do not go looking for R²:

- **`non_seasonal_p`, `non_seasonal_d`, `non_seasonal_q`**: the ARIMA parameters auto-selected for you. `d` is how many times the series was differenced to remove trend.
- **`has_seasonality` / `seasonal_periods`**: whether a repeating cycle was found. Expect `YEARLY` here, since milk production has a strong annual cycle.
- **`AIC`**: model quality score, **lower is better**. Only comparable between models fit on the same series.
- **`log_likelihood`**: how well the model fits the history. Higher is better.

### 9.5 Forecast

```sql
SELECT
  forecast_timestamp,
  ROUND(forecast_value, 1) AS forecast,
  ROUND(prediction_interval_lower_bound, 1) AS lower_bound,
  ROUND(prediction_interval_upper_bound, 1) AS upper_bound
FROM ML.FORECAST(
  MODEL `ml.milk_ts`,
  STRUCT(12 AS horizon, 0.95 AS confidence_level)
);
```

`horizon` is how many periods ahead, here 12 months. `confidence_level` of 0.95 produces bounds meaning **"we are 95 percent confident the true value lands between lower and upper."**

> **What you should see:** 12 monthly rows continuing into 1976, following the annual seasonal shape, with the interval widening the further out you go.
>
> **That widening is the most important thing on the screen.** Uncertainty grows with distance. Always show the interval alongside the forecast. A single forecast number without bounds hides exactly the information a decision-maker needs.

### 9.6 Explain the forecast

```sql
SELECT
  time_series_timestamp,
  ROUND(time_series_data, 1) AS actual,
  ROUND(trend, 1) AS trend,
  ROUND(seasonal_period_yearly, 1) AS yearly_seasonality
FROM ML.EXPLAIN_FORECAST(
  MODEL `ml.milk_ts`,
  STRUCT(12 AS horizon, 0.95 AS confidence_level)
)
ORDER BY time_series_timestamp DESC
LIMIT 24;
```

This decomposes the series into additive parts. Roughly: `forecast = trend + seasonality + holiday effect + baseline`.

Being able to say **"production rises about X per year, and every spring adds another Y on top"** is far more persuasive than handing someone a forecast number, because it explains the *why*.

### 9.7 Detect anomalies with the same model

A model that knows what is normal can flag what is not, at no extra training cost:

```sql
SELECT
  month,
  production,
  is_anomaly,
  ROUND(lower_bound, 1) AS expected_low,
  ROUND(upper_bound, 1) AS expected_high
FROM ML.DETECT_ANOMALIES(
  MODEL `ml.milk_ts`,
  STRUCT(0.95 AS anomaly_prob_threshold)
)
WHERE is_anomaly
ORDER BY month;
```

Any historical month whose actual value fell outside the model's expected range is flagged. This is a genuinely useful data quality pattern: train a forecast model on a pipeline metric such as daily row counts, then alert when reality leaves the expected band. Lower `anomaly_prob_threshold` flags more points.

### 9.8 The payoff: one table a dashboard can chart

This is the section that shows why doing ML in the warehouse is worth it.

```sql
CREATE OR REPLACE TABLE `ml.milk_actuals_and_forecast` AS
SELECT
  month AS date,
  production AS milk_value,
  'actual' AS row_type,
  NULL AS lower_bound,
  NULL AS upper_bound
FROM `ml.milk_production`

UNION ALL

SELECT
  DATE(forecast_timestamp),
  forecast_value,
  'forecast',
  prediction_interval_lower_bound,
  prediction_interval_upper_bound
FROM ML.FORECAST(
  MODEL `ml.milk_ts`,
  STRUCT(24 AS horizon, 0.95 AS confidence_level)
);

SELECT * FROM `ml.milk_actuals_and_forecast` ORDER BY date;
```

> **What you should see:** 168 `actual` rows followed by 24 `forecast` rows, one continuous series with confidence bounds on the forecast portion only.

Stop and consider what just happened. **One SQL statement produced a production-ready table combining history and predictions, which Looker or Tableau can chart directly.** No export, no pickle file, no serving container, no orchestration between three environments. Schedule this query and you have a self-updating forecast.

That is the whole argument for BigQuery ML in one query.

### 9.9 Working with a public dataset

BQML reads public datasets directly, with no copying. This also demonstrates a query pattern worth internalizing.

```sql
CREATE OR REPLACE VIEW `ml.covid_fr_daily` AS
SELECT
  date,
  SUM(new_confirmed) AS new_confirmed
FROM `bigquery-public-data.covid19_open_data.covid19_open_data`
WHERE country_name = 'France'
  AND aggregation_level = 0
  AND new_confirmed IS NOT NULL
GROUP BY date;
```

**Why `aggregation_level = 0` and `SUM` both matter.** This table stores the same country at several levels of detail: level 0 is the whole country, level 1 is regions, level 2 is smaller subdivisions. Filtering only on `country_name` returns the country row *and* every region row for the same date, which would give you duplicate timestamps and break `ARIMA_PLUS`. `aggregation_level = 0` keeps only national rows, and `GROUP BY date` with `SUM` guarantees one row per date even if the source has more.

Verify before training, exactly as in 9.2:

```sql
SELECT COUNT(*) AS rows, COUNT(DISTINCT date) AS distinct_dates
FROM `ml.covid_fr_daily`;
```

> **These two numbers must be equal.** If they are not, do not train, fix the query.

```sql
CREATE OR REPLACE MODEL `ml.covid_fr_ts`
OPTIONS(
  model_type = 'ARIMA_PLUS',
  time_series_timestamp_col = 'date',
  time_series_data_col = 'new_confirmed',
  data_frequency = 'DAILY',
  holiday_region = 'FR'
) AS
SELECT date, new_confirmed FROM `ml.covid_fr_daily`;

SELECT
  forecast_timestamp,
  ROUND(forecast_value, 0) AS forecast,
  ROUND(prediction_interval_lower_bound, 0) AS lower_bound,
  ROUND(prediction_interval_upper_bound, 0) AS upper_bound
FROM ML.FORECAST(MODEL `ml.covid_fr_ts`, STRUCT(15 AS horizon, 0.90 AS confidence_level));
```

> **Two things to notice.** The confidence bounds here are enormously wide compared to the milk forecast, because this series is far more volatile. That is the model being honest about its own uncertainty, and it is correct behavior.
>
> Also, this dataset stopped updating, so you are forecasting forward from its final date, not from today. Read it as a historical exercise. If the table has been retired since this was written, skip to Section 10, the technique is identical.

---

## 10. Section 10: What BQML Does Automatically

Understanding the preprocessing you did not write matters, because it explains output that would otherwise look strange.

### 10.1 Automatic feature engineering

When you pass columns into `CREATE MODEL`, BQML preprocesses them for you:

1. **One-hot encoding.** String columns become indicator columns automatically. This is why `Department` worked in Section 6 with no preparation, and why it appears in `ML.WEIGHTS` under `category_weights` rather than as a single `weight`.
2. **Missing value imputation.** Numeric `NULL`s are filled with the column mean. Categorical `NULL`s become their own category. This is convenient and slightly dangerous: **a column that is 60 percent `NULL` will be silently filled with its own average and look like a real feature.** Check null rates before trusting a feature.
3. **Feature standardization.** `STANDARDIZE_FEATURES` defaults to `TRUE` for GLM models, rescaling numeric features to mean 0 and standard deviation 1 so that a feature measured in the tens of thousands does not automatically overpower one measured in single digits.

Point 3 is why `ML.WEIGHTS` has that `standardize` argument from Section 6.6. Internally the model trains on standardized features, but by default `ML.WEIGHTS` converts the weights back to your original units for readability. Useful for reporting, misleading for ranking.

### 10.2 Regularization, in plain terms

**Overfitting** (Section 6.1) is a model learning noise instead of pattern. **Regularization** fights it by penalizing large weights, pushing the model toward simpler explanations:

```
Total Loss = Prediction Error + Penalty on Weight Size
```

The model can no longer buy a small accuracy gain with a wildly large weight, because the penalty costs more than the gain.

#### L1 regularization (Lasso, `l1_reg`)

- Penalty is the sum of absolute weight values.
- Pushes weak features' weights to **exactly zero**.
- **Why it matters to you:** L1 is automatic feature selection. Pass 50 columns, and if L1 zeroes 35, those 35 add nothing. That is a direct signal about which columns your pipeline actually needs to keep computing.

#### L2 regularization (Ridge, `l2_reg`)

- Penalty is the sum of squared weight values.
- Shrinks weights toward zero without reaching it.
- **Why it matters:** L2 handles **multicollinearity**, where features carry the same information. In Activity 5's `mpg` data, `displacement`, `horsepower`, `weight`, and `cylinders` all measure "how big is this engine." Without L2, the model splits credit between them erratically and weights swing wildly on small data changes. L2 spreads credit smoothly.

#### Using both

```sql
CREATE OR REPLACE MODEL `ml.income_model_regularized`
OPTIONS(
  model_type = 'LINEAR_REG',
  input_label_cols = ['MonthlyIncome'],
  l1_reg = 0.1,
  l2_reg = 0.1,
  data_split_method = 'RANDOM',
  data_split_eval_fraction = 0.2
) AS
SELECT Age, JobLevel, DistanceFromHome, JobSatisfaction, Department, MonthlyIncome
FROM `ml.employee_data`;

SELECT 'no regularization' AS model, r2_score FROM ML.EVALUATE(MODEL `ml.income_model`)
UNION ALL
SELECT 'L1 + L2', r2_score FROM ML.EVALUATE(MODEL `ml.income_model_regularized`);
```

> **What you should see:** very similar R² values.
>
> That is the expected result and it is not a failure. Regularization helps most when you have many features and few rows. With 5 features and 1,470 rows there is little to overfit, so there is little to fix. **Knowing when a technique is not needed is as valuable as knowing how to apply it.**

---

## 11. Section 11: Metrics Reference

Keep this for Activity 5.

### Regression (`LINEAR_REG`)

| Metric | Meaning | Reading it |
|--------|---------|------------|
| `r2_score` | Fraction of variance explained | 0 to 1, higher better. Above 0.7 is strong for business data. Above 0.98 on real data usually means a leaked label |
| `mean_absolute_error` | Typical miss, in real units | Lower better. **The number to quote to stakeholders** |
| `root_mean_squared_error` | Like MAE but punishes big misses harder | Use when large errors are disproportionately costly |

**Label leakage** deserves a warning. If R² comes back at 0.999, suspect that a feature secretly contains the answer, for example predicting `total_price` while `unit_price` and `quantity` are both features. It is the most common cause of a "too good" model.

### Classification (`LOGISTIC_REG`)

| Metric | Meaning | Reading it |
|--------|---------|------------|
| `accuracy` | Fraction correct overall | **Always compare against the majority-class baseline first** |
| `precision` | Of predicted positives, fraction actually positive | Prioritize when false alarms are costly |
| `recall` | Of actual positives, fraction caught | Prioritize when misses are costly |
| `f1_score` | Harmonic mean of precision and recall | Single balanced score |
| `roc_auc` | Class separation across all thresholds | **0.5 = coin flip, 0.7 = usable, 0.9+ = strong, 1.0 = suspicious** |

An ROC AUC of 1.0 on real data is almost never good news. It usually means leakage.

### Clustering (`KMEANS`)

| Metric | Meaning | Reading it |
|--------|---------|------------|
| `davies_bouldin_index` | Cluster tightness and separation | Lower better. Only meaningful compared across `k` values |
| `mean_squared_distance` | Average distance from points to their centroid | Lower better, but always falls as `k` rises, so never optimize it alone |

### Time series (`ARIMA_PLUS`)

| Metric | Meaning | Reading it |
|--------|---------|------------|
| `AIC` | Model quality with a complexity penalty | Lower better, comparable only within the same series |
| `has_seasonality` | Repeating cycle detected | Confirms the model found the pattern you expect |
| `non_seasonal_p/d/q` | Auto-selected ARIMA parameters | Informational, `auto_arima` chose these |

---

## 12. Troubleshooting

| Error or symptom | Likely cause | Fix |
|------------------|--------------|-----|
| `Not found: Dataset` on a public dataset | Your `ml` dataset is not in the US multi-region | Recreate it with `location = 'US'` (Step 3.3) |
| `Unrecognized name: Detergents_and_Paper` | Auto-detect renamed the column on upload | Query `INFORMATION_SCHEMA.COLUMNS` and use the real name (Step 3.5) |
| `No matching signature for function PARSE_DATE` | The column is already a `DATE`, and `PARSE_DATE` needs a `STRING` | Drop `PARSE_DATE` and use the column directly |
| Time-series training fails on duplicate timestamps | More than one row per date | Aggregate with `GROUP BY date` first (Step 9.2) |
| `ML.WEIGHTS` shows `NULL` weight and a `category_weights` array | The column is a `STRING`, so it was treated as categorical | Check for `?` or `N/A` values, then `SAFE_CAST` to a number |
| R² near 1.0, or ROC AUC near 1.0 | Label leakage, a feature contains the answer | Re-read your feature list and remove it |
| Accuracy is high but the model is useless | Imbalanced classes | Compare against the majority baseline, use `roc_auc` and `auto_class_weights` (Step 7.4) |
| Suspiciously good metrics on a small table | Under 500 rows, so AUTO_SPLIT held nothing back | Set `data_split_method = 'RANDOM'` explicitly (Step 6.2) |
| One cluster holds nearly every row | A feature dominates, or `k` is wrong | Confirm `standardize_features = TRUE`, try other `k` values |

---

## 13. Function Reference

| Statement or function | Purpose | Typical usage |
|---|---|---|
| `CREATE OR REPLACE MODEL` | Trains a model | `OPTIONS(model_type = '...') AS SELECT ...` |
| `ML.EVALUATE` | Returns quality metrics | `SELECT * FROM ML.EVALUATE(MODEL m)` |
| `ML.PREDICT` | Runs inference, passes extra columns through | `ML.PREDICT(MODEL m, (SELECT ...))` |
| `ML.WEIGHTS` | Shows learned weights | Add `STRUCT(TRUE AS standardize)` to compare features |
| `ML.FORECAST` | Future values for time-series models | `STRUCT(12 AS horizon, 0.95 AS confidence_level)` |
| `ML.EXPLAIN_FORECAST` | Splits forecast into trend, seasonality, holiday | Requires `decompose_time_series = TRUE` |
| `ML.DETECT_ANOMALIES` | Flags points outside the expected band | `STRUCT(0.95 AS anomaly_prob_threshold)` |
| `ML.CENTROIDS` | Cluster centers, how you name segments | `SELECT * FROM ML.CENTROIDS(MODEL m)` |
| `ML.ROC_CURVE` | Precision/recall trade-off by threshold | `SELECT * FROM ML.ROC_CURVE(MODEL m)` |

---

## 14. Before You Move On

Check that you can answer these from memory. They are exactly what Activity 5 asks you to apply.

- [ ] I can explain what a feature and a label are, and which BQML option names the label.
- [ ] I know why evaluating on training data is misleading, and what `AUTO_SPLIT` does below 500 rows.
- [ ] I can describe overfitting and name the query that detects it.
- [ ] I know why `ML.WEIGHTS` needs `STRUCT(TRUE AS standardize)` to rank features fairly.
- [ ] I can explain why 90 percent accuracy can mean a worthless model.
- [ ] I know what ROC AUC of 0.5 means.
- [ ] I can explain why `standardize_features = TRUE` matters for K-Means.
- [ ] I know why a clustering I cannot name is a clustering I should not ship.
- [ ] I can explain why forecast confidence intervals widen over time.
- [ ] I can name the check to run before training any time-series model.

You are ready for Activity 5.

# Activity 5 Solution: BigQuery ML Hands-On Lab

This is a worked walkthrough, not an answer sheet. Every query is here, but so is the reasoning that produced it, because the queries are the easy part of this lab and the reasoning is the part you will be paid for.

**Use it this way:** attempt the task first, then read the matching section here. If your numbers differ from the reference values, read the "Why your numbers will differ" note below before assuming you made a mistake.

---

## How to read the numbers in this document

Reference values in this document come from fitting the same models on the same CSVs with ordinary least squares, logistic regression, and k-means outside BigQuery, so you have something concrete to compare against. They are anchors, not targets.

**Why your numbers will differ from these, legitimately:**

| Cause | Effect |
|-------|--------|
| `data_split_method = 'RANDOM'` draws a different holdout every run | R², MAE, accuracy, and AUC move by a few points |
| BQML's optimizer stops on its own convergence rule, not at the exact least-squares solution | weights differ in the second or third decimal |
| K-Means starts from random centroid positions | cluster ID numbers are arbitrary and will not match anyone else's |
| How you repaired the dirty `horsepower` column | small weights change noticeably, large ones barely move |

What should **not** differ is any conclusion in this document. If your ranking of the top feature flips, or your ship decision flips, something upstream went wrong.

## The four questions this lab is really teaching

Every task below is the same four questions applied to a different model type. Learn the questions, not the syntax.

1. **Is the data what I think it is?** Types, ranges, impossible values, duplicate keys.
2. **Was the model measured honestly?** On rows it never saw, against the score of doing nothing.
3. **Does the model's explanation of the world make sense?** Weights, centroids, seasonality.
4. **Would I sign my name to shipping this?**

---

## Setup

```sql
CREATE SCHEMA IF NOT EXISTS `ml`
OPTIONS (location = 'US');
```

```sql
SELECT table_name, column_name, data_type
FROM `ml.INFORMATION_SCHEMA.COLUMNS`
WHERE table_name IN ('car_mpg', 'loan_applications', 'cereal_nutrition', 'air_passengers')
ORDER BY table_name, ordinal_position;
```

> **What you should see:**
>
> | Table | Rows | Notable types |
> |-------|-----:|---------------|
> | `car_mpg` | 398 | `mpg`, `displacement`, `acceleration` are `FLOAT64`; `cylinders`, `weight` are `INT64`; **`horsepower` is `STRING`** |
> | `loan_applications` | 100 | five `FLOAT64` features, `status` is `STRING` |
> | `cereal_nutrition` | 74 | all five nutrition columns are `INT64`; names normalized (see below) |
> | `air_passengers` | 144 | **`date` is `DATE`**, `passengers` is `INT64` |

Two things in that table are the entire point of running it.

`horsepower` is a `STRING` in a file where every value looks numeric. That is Task 1's defect, visible before you write a line of model SQL.

`date` is already a `DATE`. That fact stops you from writing a `PARSE_DATE` that would fail in Task 4.

### A note on the cereal column names

BigQuery column names cannot contain spaces or parentheses, so auto-detect rewrites the header on upload by replacing each invalid character with an underscore. `Vitamins and Minerals` becomes `Vitamins_and_Minerals`. `Protein (g)` has a space, an opening parenthesis, and a closing parenthesis, so it normalizes to `Protein__g_`.

This document writes it as `Protein__g_`. **Confirm against your own `INFORMATION_SCHEMA` output and substitute whatever your load actually produced.** Reading the name from the catalog rather than the CSV header is the habit; the specific rendering is not worth memorizing.

---

## Task 1: Regression, and Ranking Causes Honestly

### The concept first: what `LINEAR_REG` learns

A linear regression is one arithmetic sentence. For this task it will be:

```
predicted_mpg = intercept
              + (w1 x cylinders)
              + (w2 x displacement)
              + (w3 x horsepower)
              + (w4 x weight)
              + (w5 x acceleration)
```

Training means finding the six numbers that make this sentence wrong by as little as possible across all 398 cars. That is all. `ML.WEIGHTS` shows you those six numbers, which is why linear regression is the model type you can actually argue with.

Each weight has a unit, and the unit is **"mpg per one unit of that feature."** Hold onto that sentence, because Step 1.4 is entirely about it.

### 1.1 Find the dirty column

```sql
SELECT horsepower, COUNT(*) AS n
FROM `ml.car_mpg`
WHERE SAFE_CAST(horsepower AS FLOAT64) IS NULL
GROUP BY horsepower;
```

> **What you should see:** one row. `horsepower = '?'`, `n = 6`.

Six values out of 398, about 1.5 percent of the column, changed the declared type of all 398. Auto-detect scans the column, hits a value it cannot parse as a number, and falls back to the type that can hold anything: `STRING`.

**Why `SAFE_CAST` is the right tool for the investigation.** A plain `CAST(horsepower AS FLOAT64)` fails the entire query on the first `?` and tells you nothing except that something is wrong somewhere. `SAFE_CAST` returns `NULL` instead of erroring, which turns "this query is broken" into "here are the exact 6 values that are broken." Use `SAFE_CAST` whenever you are diagnosing, and use the `NULL`s it produces as your defect list.

**What happens if you miss it.** Nothing visible, which is the danger. BQML sees a `STRING` feature and applies its standard treatment for text: one-hot encoding. This column has **94 distinct string values**, so the model builds roughly 94 indicator features, one per horsepower value, and learns a separate weight for each. `'130'` and `'132'` become two unrelated categories with no notion that one is larger than the other.

You would then get:

- a model that trains without a single warning;
- `ML.WEIGHTS` showing `NULL` in the `weight` column for `horsepower` and a large `category_weights` array instead;
- no answer at all to "how much does horsepower cost you in mpg," because there is no single horsepower weight to read.

A model, no error, and a nonsense answer to the business question. This is the most common shape of a silent ML failure: the pipeline is green and the output is meaningless.

### 1.2 Train

```sql
CREATE OR REPLACE MODEL `ml.car_mpg_model`
OPTIONS(
  model_type = 'LINEAR_REG',
  input_label_cols = ['mpg'],
  data_split_method = 'RANDOM',
  data_split_eval_fraction = 0.2
) AS
SELECT
  cylinders,
  displacement,
  SAFE_CAST(horsepower AS FLOAT64) AS horsepower,
  weight,
  acceleration,
  mpg
FROM `ml.car_mpg`;
```

Three deliberate choices in that statement.

**The `SAFE_CAST` with an alias.** The cast turns the 6 `?` values into `NULL`, and BQML then fills each `NULL` with the mean of the column (about **104.5** horsepower). The `AS horsepower` alias matters more than it looks: without it the feature is named `f0_` and every later `ML.WEIGHTS` and `ML.PREDICT` output becomes unreadable. Name your engineered features.

**The explicit split.** `AUTO_SPLIT` holds nothing back below 500 rows, and this table has 398. Left on the default, `ML.EVALUATE` would report how well the model scores the same rows it learned from, formatted identically to an honest score. Setting `RANDOM` with `data_split_eval_fraction = 0.2` reserves about 80 cars the model never sees.

**Nothing else selected.** There is no "features" option in `CREATE MODEL`. Every column in the `SELECT` that is not the label becomes a feature, so the `SELECT` list *is* your feature list.

#### Impute or drop? Both are defensible

Dropping the six rows is equally correct and arguably cleaner:

```sql
-- Alternative repair: drop the 6 unusable rows instead of imputing them
... FROM `ml.car_mpg`
WHERE SAFE_CAST(horsepower AS FLOAT64) IS NOT NULL;
```

What matters is that you can say which you chose and why:

| Choice | Argument for it | Cost |
|--------|-----------------|------|
| Impute with the mean (BQML's default on `NULL`) | Keeps all 398 rows; the other five features on those rows are still real information | Invents a horsepower value for 6 cars, which slightly flattens the horsepower relationship |
| Drop the 6 rows | Never trains on a fabricated number | Loses 1.5 percent of the data |

At 6 rows out of 398 the two answers land in the same place. At 200 rows out of 398 they would not, and the choice would need a real conversation. **Say which you did.** An unstated imputation is how a fabricated number ends up in a board deck.

### 1.3 Evaluate

```sql
SELECT r2_score, mean_absolute_error, root_mean_squared_error
FROM ML.EVALUATE(MODEL `ml.car_mpg_model`);
```

> **What you should see:** `r2_score` roughly **0.61 to 0.75**, `mean_absolute_error` roughly **2.9 to 3.7**.
>
> Reference: across 200 simulated 80/20 splits of this data, holdout R² had a median of **0.70** and MAE a median of **3.28**. In-sample R² on all 398 rows is **0.705**.

Read both metrics out loud, because they answer different questions.

**R² of 0.70** means the five engine and body measurements together explain about 70 percent of why one car gets different mileage than another. The remaining 30 percent lives in things this table does not contain: model year, transmission, aerodynamics, where it was driven. For business data, 0.70 is a genuinely useful model.

**MAE of 3.3** means the typical prediction misses by about 3.3 mpg. This is the number you take to a stakeholder, because it is in units they own. "Our estimate is usually within about 3 mpg" is a sentence someone can make a decision against. "Our R² is 0.70" is not.

Now apply it: is 3.3 mpg good enough to print on a window sticker next to a 25 mpg rating? That is a 13 percent error on the thing the customer is reading. Probably not. Good enough to rank a fleet purchase from most to least efficient? Very likely yes. **The metric does not decide; the use decides.** A model is only ever good enough *for something*.

Note also that `root_mean_squared_error` will be larger than MAE (roughly 4.2 here). RMSE squares each error before averaging, so a handful of large misses inflate it. When RMSE runs far above MAE, you have a few badly mispredicted rows worth looking at individually.

### 1.4 The ranking reversal, and why it happens

The business question is "which attribute most reduces fuel efficiency." Both queries below claim to answer it. They disagree.

```sql
-- Default: each weight is in that feature's own units
SELECT processed_input, weight
FROM ML.WEIGHTS(MODEL `ml.car_mpg_model`)
ORDER BY ABS(weight) DESC;
```

```sql
-- Standardized: every weight is per one standard deviation, so they are comparable
SELECT processed_input, weight
FROM ML.WEIGHTS(MODEL `ml.car_mpg_model`, STRUCT(TRUE AS standardize))
ORDER BY ABS(weight) DESC;
```

> **Reference weights.** Both columns come from the same fit, the `SAFE_CAST` and mean-impute version on all 398 rows:
>
> | Feature | Raw weight (mpg per unit) | Feature's std dev | Standardized weight (mpg per std dev) |
> |---------|--------------------------:|------------------:|-------------------------------------:|
> | `weight` | -0.0054 | 846 lb | **-4.54** |
> | `horsepower` | -0.0390 | 38.4 hp | -1.49 |
> | `cylinders` | **-0.3587** | 1.70 | -0.61 |
> | `displacement` | -0.0014 | 104 cu in | -0.15 |
> | `acceleration` | -0.0070 | 2.75 | -0.02 |
>
> Ranked by raw magnitude: `cylinders`, `horsepower`, `acceleration`, `displacement`, `weight`.
> Ranked by standardized magnitude: **`weight`**, `horsepower`, `cylinders`, `displacement`, `acceleration`.
>
> **Vehicle weight is dead last on one list and first on the other.**

#### Why the two lists disagree

Look at the third column of that table, then do the arithmetic yourself.

The raw weight for `weight` is -0.0054, meaning **one additional pound costs 0.0054 mpg.** True, and useless for ranking. One pound is nothing in a column that runs from 1,613 to 5,140 lb.

The raw weight for `cylinders` is -0.3587, meaning **one additional cylinder costs 0.36 mpg.** Also true. But one cylinder is a massive change in a column that only takes the values 3 through 8.

Ranking raw weights ranks *units*. Pounds are small, cylinders are large, so pounds lose. Ask the fair question instead: what happens when each feature moves by a typical amount for that feature, one standard deviation?

```
weight:    -0.0054 mpg/lb  x  846 lb  =  -4.54 mpg
cylinders: -0.3587 mpg/cyl x  1.70    =  -0.61 mpg
```

A typical swing in vehicle weight costs about **4.5 mpg**. A typical swing in cylinder count costs about **0.6 mpg**. That is a factor of seven, in the opposite direction from the raw ranking. `STRUCT(TRUE AS standardize)` does exactly this multiplication for you.

**The correct answer to the business question is vehicle weight**, which also agrees with physics: moving more mass takes more fuel. The default ordering would have you report cylinder count, confidently and wrongly.

**The rule to carry out of this lab:** use default weights to state what one unit is worth in business terms ("each 100 lb costs about half an mpg"). Use standardized weights to rank features against each other. Mixing them up is a well-dressed way to be wrong.

#### Two honest caveats about this table

**The bottom of the list is noise.** `displacement` at -0.15 and `acceleration` at -0.02 are near zero, and near-zero weights are not reliably ordered. If you dropped the 6 bad rows instead of imputing them, the reference fit gives `displacement` -0.01 and `acceleration` -0.08, which swaps positions 4 and 5. Nothing is wrong in either case. **Only differences that survive a change in your preprocessing are worth reporting.** The top three are stable across every variation tested; ranks four and five are not, so do not build an argument on them.

**These weights are not causal, and the correlation matrix shows why.** In this data:

| Pair | Correlation |
|------|------------:|
| `cylinders` and `displacement` | 0.95 |
| `displacement` and `weight` | 0.93 |
| `cylinders` and `weight` | 0.90 |
| `horsepower` and `displacement` | 0.89 |

All four features are largely measuring one underlying thing: how big is this car. When features overlap this heavily (**multicollinearity**, Activity 4 Section 10.2), the model has many nearly equivalent ways to split credit between them, and the split it picks is somewhat arbitrary. So the defensible claim is "heavier, larger-engined cars burn more fuel, and weight carries the most of that signal." The overreach is "if we shaved 846 lb off this exact car we would gain 4.5 mpg." Regression describes association. Only an experiment or a physical model gets you causation.

### 1.5 Predict

```sql
SELECT
  ROUND(predicted_mpg, 1) AS predicted_mpg,
  mpg AS actual_mpg,
  cylinders, horsepower, weight
FROM ML.PREDICT(
  MODEL `ml.car_mpg_model`,
  (SELECT
     cylinders,
     displacement,
     SAFE_CAST(horsepower AS FLOAT64) AS horsepower,
     weight,
     acceleration,
     mpg
   FROM `ml.car_mpg`
   LIMIT 10)
);
```

> **What you should see:** ten rows where `predicted_mpg` sits within a few mpg of `actual_mpg`, in both directions. The output column is `predicted_` plus your label name, which is why it is `predicted_mpg` here.

Passing `mpg` into the prediction input is intentional. It is not used as a feature at prediction time; `ML.PREDICT` hands unrecognized columns straight through to the output, which is how you get the prediction and the truth side by side for comparison.

**The `SAFE_CAST` has to be repeated here, and this is the most transferable lesson in Task 1.** The model was trained against a schema where `horsepower` is `FLOAT64`. Hand it the raw `STRING` column and the query fails, because GoogleSQL does not implicitly convert `STRING` to `FLOAT64`. You get an error, not silently degraded predictions.

That failure is the good case. The general problem it points at is **training/serving skew**: any difference between how features are prepared at training time and at prediction time. Here the type system catches it. In a real pipeline the skew is usually subtler and silent, for example training on a currency in dollars and serving cents, or training with a filter that the serving query forgets. It is one of the most common and most expensive production ML bugs, and the defense is structural: define the transformation once and call it from both paths, rather than typing it twice.

### Stretch: does L2 regularization help?

```sql
CREATE OR REPLACE MODEL `ml.car_mpg_l2`
OPTIONS(
  model_type = 'LINEAR_REG',
  input_label_cols = ['mpg'],
  l2_reg = 1.0,
  data_split_method = 'RANDOM',
  data_split_eval_fraction = 0.2
) AS
SELECT
  cylinders, displacement,
  SAFE_CAST(horsepower AS FLOAT64) AS horsepower,
  weight, acceleration, mpg
FROM `ml.car_mpg`;

SELECT 'baseline' AS model, r2_score FROM ML.EVALUATE(MODEL `ml.car_mpg_model`)
UNION ALL
SELECT 'l2 = 1.0', r2_score FROM ML.EVALUATE(MODEL `ml.car_mpg_l2`);
```

> **What you should see:** two R² values that differ by less than the gap between two random splits of the same model. In the reference fit, R² was unchanged to four decimal places.
>
> The standardized weights barely move either: `weight` from -4.54 to -4.44, `horsepower` from -1.49 to -1.50, `displacement` from -0.15 to -0.23.

**The correct answer to this stretch is "no, and here is why not."** Regularization exists to stop a model from overfitting, and overfitting requires enough freedom to memorize. With 398 rows and 5 features there is almost nothing to memorize, so there is almost nothing for L2 to fix.

The direction of the tiny changes is still instructive: the largest weight shrank slightly and the smallest ones grew slightly, which is L2 doing its intended job of spreading credit more evenly across those heavily correlated engine-size features. The effect is real and it is in the third decimal.

**Knowing that a technique does not apply, and saying so, is a stronger answer than applying it and reporting a difference that is inside the noise.** L2 would matter here if you had 50 features and 100 rows.

---

## Task 2: Classification, and Deciding Not to Ship

### The concept first: what `LOGISTIC_REG` learns

Logistic regression does not predict a category. It predicts a **probability**, then converts that probability to a category by comparing it against a threshold, 0.5 by default.

It gets there with the same arithmetic sentence as Task 1, with one extra step:

```
score       = intercept + (w1 x assets) + (w2 x liabilities) + ...
probability = squash(score) into the 0 to 1 range
label       = 'approve' if probability > 0.5 else 'deny'
```

So a weight in a logistic model reads as **"how much does this feature push the score toward `approve`."** Positive pushes toward approval, negative pushes toward denial, and zero means the feature is not participating. That reading is all you need for Step 2.4, and Step 2.4 is where this task pays off.

### 2.1 Baseline first, before you see any model score

```sql
SELECT
  status,
  COUNT(*) AS n,
  ROUND(100 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS pct
FROM `ml.loan_applications`
GROUP BY status;
```

> **What you should see:** `deny` 53 rows (53.0 percent), `approve` 47 rows (47.0 percent).
>
> **Baseline accuracy to beat: 53 percent.**

That 53 percent is the score of a model with no features, no training, and no code: always answer `deny`. It is the floor. Any accuracy near 53 percent means the features contributed nothing, no matter how sophisticated the algorithm.

Running this **before** training is not a formality, it is a defense against your own reasoning. A 60 percent accuracy looks like a passing grade in isolation. Next to 53 percent it looks like almost nothing. Anchor first and the second reading is the one you get.

### 2.2 Train

```sql
CREATE OR REPLACE MODEL `ml.loan_approval_model`
OPTIONS(
  model_type = 'LOGISTIC_REG',
  input_label_cols = ['status'],
  auto_class_weights = TRUE
) AS
SELECT assets, liabilities, income, credit_score, mortgage, status
FROM `ml.loan_applications`;
```

`auto_class_weights = TRUE` tells the model to treat the smaller class as equally important. At 53/47 the imbalance is mild and this option changes little, but it is the right habit: the class you care about is usually the rare one.

**No data split, deliberately.** With 100 rows there is no holdout worth having; a 20 percent split would be 20 applicants, and any metric computed on 20 rows swings wildly. So `AUTO_SPLIT` trains on all 100 and evaluates on those same 100.

Be precise about what that means for the next step. You are about to read **the most flattering numbers this dataset can possibly produce**, measured on rows the model has already seen. Any honest estimate is lower. That framing is what makes the conclusion in 2.5 unavoidable rather than harsh.

### 2.3 Evaluate against the baseline

```sql
SELECT roc_auc, accuracy, precision, recall, f1_score
FROM ML.EVALUATE(MODEL `ml.loan_approval_model`);
```

> **What you should see:** `roc_auc` roughly **0.60 to 0.70**, `accuracy` roughly **0.55 to 0.70**.
>
> Reference fit on all 100 rows, scored on those same 100 rows: **ROC AUC 0.676**, accuracy **0.68** with balanced class weights (**0.60** without them), precision 0.64, recall 0.75, F1 0.69.

Now line the numbers up against what you know:

| Reading | Value | What it means |
|---------|-------|---------------|
| Baseline accuracy | 0.53 | Free, no model |
| Model accuracy | about 0.60 to 0.68 | A gain of 7 to 15 points, **on rows it trained on** |
| ROC AUC | about 0.68 | 0.50 is a coin flip, 1.0 is perfect |

**ROC AUC is the metric to anchor on**, because it does not depend on where the 0.5 threshold sits. Read it concretely: pick one real `approve` applicant and one real `deny` applicant at random, and AUC is the chance the model gives the `approve` one a higher score. At 0.68 it gets that right about two times in three. A coin gets it right one time in two.

Notice that recall (0.75) is well above precision (0.64). The model says `approve` fairly freely, catching most real approvals while being wrong about a third of the ones it approves. On a real lending desk that asymmetry is a cost you can price: false approvals are defaults, false denials are lost customers. Here it is not worth pricing, because the underlying signal is not there.

**This model has found almost nothing.** Reaching that conclusion, from evidence, is the deliverable for Task 2.

### 2.4 What a weights table looks like when there is no signal

```sql
SELECT processed_input, weight
FROM ML.WEIGHTS(MODEL `ml.loan_approval_model`, STRUCT(TRUE AS standardize))
ORDER BY weight DESC;
```

> **Reference standardized weights** (change in score per one standard deviation, positive pushes toward `approve`):
>
> | Feature | Standardized weight | Sign was consistent in |
> |---------|-------------------:|-----------------------:|
> | `liabilities` | +0.47 | 100 percent of resamples |
> | `mortgage` | +0.27 | 99 percent |
> | `assets` | +0.24 | 99 percent |
> | `income` | -0.06 | 36 percent positive, 64 percent negative |
> | `credit_score` | -0.03 | 39 percent positive, 61 percent negative |
>
> The right-hand column comes from refitting the model on 500 bootstrap resamples of the same 100 rows and counting how often each weight kept its sign.
>
> **Expect the default, unstandardized weights to be about five to six times larger** (`liabilities` near +2.5, for instance). Each feature is scaled 0 to 1 with a standard deviation near 0.17, so dividing by 0.17 inflates every number. Same model, different units, and only the standardized column is comparable across features.

Two findings here, and the second is the one most students miss.

**Finding one: the largest weight is backwards.** `liabilities` is the strongest feature in the model and it pushes toward approval. Read it as a sentence: *"the more debt an applicant carries, the more likely we approve them."* No lender operates this way. `mortgage` says the same thing.

**Finding two: the two features a lender would actually underwrite on carry essentially no weight at all.** `income` at -0.06 and `credit_score` at -0.03 are not weak negative effects, they are zero with a sign attached. The bootstrap column proves it: resample the same 100 applicants and those two signs flip roughly one time in three. **The sign of a near-zero weight is not a finding, it is a coin flip you have mistaken for a finding.**

That distinction matters for how you write up 2c. "Income pushes toward denial" is a claim your own data will not reproduce. "Income and credit score carry no weight in this model, while carrying more debt is the strongest predictor of approval" is a claim that holds up, and it is more damning.

One subtlety worth knowing, because it will come up again: `income` actually correlates *positively* with approval in the raw data (+0.08), yet lands with a small negative weight in the fitted model. That flip is normal when features overlap; the model has already spent the signal elsewhere and uses `income` as a small correction on top. It is another reason a single weight is not a standalone statement about the world.

**The most important property of the table you just produced is that it looks exactly like a real one.** Nothing is flagged, greyed out, or starred. It has plausible feature names, ordered numbers, and correct signs on three of five rows. Paste it into a slide and it will pass review in most rooms. The only thing standing between it and a bad lending decision is an engineer who ran the baseline query and the AUC first.

Also note what the features are: anonymized values between 0 and 1 with no documented units. Even with a good model you could not tell anyone what "assets of 0.44" means in dollars, which means you could not act on it. Undocumented units are their own blocker, separate from model quality.

### 2.5 Predict, and make the call

```sql
SELECT
  predicted_status,
  status AS actual_status,
  ROUND(prob, 3) AS confidence
FROM ML.PREDICT(
  MODEL `ml.loan_approval_model`,
  (SELECT * FROM `ml.loan_applications` LIMIT 10)
),
UNNEST(predicted_status_probs)
WHERE label = predicted_status;
```

The `UNNEST` plus `WHERE label = predicted_status` idiom is worth keeping. `predicted_status_probs` is an array of structs, one entry per class, each with a `label` and a `prob`. Unnesting it multiplies each row by the number of classes, and filtering to the chosen label collapses it back to one row per applicant carrying the probability of whatever the model actually picked.

> **What you should see:** roughly 2 to 4 of the 10 predictions wrong, with confidences clustered between 0.52 and 0.72.
>
> Across all 100 applicants in the reference fit, predicted probabilities span only about **0.28 to 0.68**. Not one applicant gets a confident verdict in either direction.

That compressed range is the model telling you the truth about itself. A model with real signal produces a spread of probabilities: some applicants at 0.03, some at 0.96, because some cases genuinely are clear. Probabilities that all huddle near 0.5 mean "every applicant looks about the same to me," which is the honest summary of what these five anonymized columns support.

#### Model answer for question 2d

> No, this model should not be deployed to score real loan applications. Its accuracy of about 0.68 is only modestly above the 0.53 you get free by always answering `deny`, and its ROC AUC of 0.68 sits far closer to a 0.5 coin flip than to a usable model. Both numbers are measured on the same 100 rows the model trained on, because 100 rows is below BQML's 500-row split threshold, so genuine performance on new applicants would be worse than this. The weights confirm there is no real signal to find: `liabilities` is the strongest predictor of approval, which is backwards for lending, while `income` and `credit_score` carry weights near zero whose signs flip across resamples of the same data. No applicant in the table receives a probability outside about 0.28 to 0.68, so the model is not confident about anyone. I would revisit the decision given substantially more rows, features documented in real units instead of anonymized 0-to-1 values, and a genuine holdout evaluation.

Any answer that reaches "do not ship" while citing at least two of the three arguments (baseline comparison, ROC AUC, weight behavior) is a complete answer. **There is no penalty for recommending against your own model.** Shipping a model nobody checked does more damage than shipping nothing, and being the person who catches it is the job.

### Stretch: read the trade-off curve

```sql
SELECT threshold, recall, false_positive_rate, true_positives, false_positives
FROM ML.ROC_CURVE(MODEL `ml.loan_approval_model`)
WHERE threshold BETWEEN 0.1 AND 0.9
ORDER BY threshold;
```

> **What you should see:** as `threshold` rises, `recall` and `false_positive_rate` fall together, at roughly the same rate.

That "together, at the same rate" is what an AUC near 0.5 looks like as a table. On a model with real signal you can buy recall cheaply: lower the threshold, catch many more true approvals, and let in only a few false ones. Here every point of recall costs you almost a point of false positive rate. There is no threshold that gives you a good trade, which is a different and more useful statement than "the AUC is low." It says the problem is not a badly tuned cutoff, it is the model.

---

## Task 3: Clustering, and Naming What You Find

### The concept first: what K-Means does, and what "no answer key" changes

There is no label column in this task. You are not asking "predict X," you are asking "does this data fall into natural groups." K-Means answers it geometrically:

1. Place `k` points at random in the data. Each is a **centroid**.
2. Assign every cereal to its nearest centroid.
3. Move each centroid to the average position of its members.
4. Repeat 2 and 3 until nothing moves.

Two consequences follow directly from "distance decides everything," and they explain every option in Step 3.3.

**Consequence one: scale is power.** A column with big numbers contributes more distance than a column with small numbers, purely because its numbers are bigger. That is what `standardize_features` fixes.

**Consequence two: there is no accuracy score, ever.** With no label there is nothing to be right about. Quality is judged by whether the groups are tight, separated, and above all *nameable*. Which is why the deliverable for this task is a set of names, not a model.

### 3.1 Get the real column names

Run the `INFORMATION_SCHEMA` query from Setup, filtered to `cereal_nutrition`, and use exactly the names it reports. Typing `Protein (g)` produces `Unrecognized name`, and hunting that error is the single biggest time sink in this task.

### 3.2 The defect no cast can catch

```sql
SELECT
  MIN(Calories) AS min_cal, MAX(Calories) AS max_cal,
  MIN(Sugars) AS min_sugar, MAX(Sugars) AS max_sugar,
  MIN(Fat) AS min_fat, MAX(Fat) AS max_fat
FROM `ml.cereal_nutrition`;
```

> **What you should see:** `Calories` 50 to 160, `Fat` 0 to 5, and `Sugars` **-1** to 15.

A cereal with negative sugar does not exist. This is a **sentinel value**: an impossible number used as a stand-in for "missing," a convention older than most of the tooling you will use, and still everywhere. Common sentinels are `-1`, `-999`, `9999`, and `1900-01-01`.

```sql
SELECT * FROM `ml.cereal_nutrition` WHERE Sugars < 0;
```

> **What you should find:** exactly one row, `Quaker_Oatmeal`, with `Sugars = -1` and `Vitamins_and_Minerals = 0`.

**Why no type check would have saved you.** `-1` is a perfectly valid `INT64`. The column loaded as `INT64`, `SAFE_CAST` returns a number, no error is raised anywhere, and every automated check passes. Task 1's defect announced itself by changing a column's type. This one is invisible to the machine and obvious to a human who knows what sugar is. **`MIN` and `MAX` on every numeric column is a thirty-second query that catches an entire class of bug that types cannot.** Run it on every table you are about to model.

**Why this hurts clustering more than it would hurt regression.** Two compounding effects:

1. **The bad row lands in the wrong group.** Real sugar values run 0 to 15. At -1, `Quaker_Oatmeal` sits about 1.7 standard deviations below the column mean, so distance drags it toward the low-sugar extreme. On its actual nutrition it belongs with the plain cereals anyway, so here you may not notice, which is precisely why you cannot rely on noticing.
2. **The damage spreads to every other row.** Because you standardize, the mean and standard deviation of `Sugars` are computed from the column *including* the -1. In this data that shifts the mean from 6.88 to 6.77 and the standard deviation from 4.40 to 4.47. Every one of the other 73 cereals gets rescaled by numbers that a fabricated value helped produce. One bad cell perturbs the whole model, and in a regression it would have perturbed one row's contribution instead.

Exclude it, and say so in your write-up:

```sql
... FROM `ml.cereal_nutrition`
WHERE Sugars >= 0
```

**Why drop rather than treat -1 as real or impute it?** Dropping is cleanest here because the value is definitively impossible (not merely surprising), it is one row out of 74, and this is unsupervised work where a fabricated coordinate would sit inside a group and quietly bend a centroid. Mean-imputing it would be defensible too, and you would say so. Leaving it as -1 is not defensible under any argument.

### 3.3 Train

Substitute the normalized column names your own load produced.

```sql
CREATE OR REPLACE MODEL `ml.cereal_clusters`
OPTIONS(
  model_type = 'KMEANS',
  num_clusters = 3,
  distance_type = 'EUCLIDEAN',
  standardize_features = TRUE
) AS
SELECT
  Calories,
  Protein__g_,
  Fat,
  Sugars,
  Vitamins_and_Minerals
FROM `ml.cereal_nutrition`
WHERE Sugars >= 0;
```

> **What you should see:** the model trains on **73 rows**, the 74 in the table minus the sentinel row.

Note there is no `input_label_cols`. That absence is the signature of unsupervised learning.

**Why `standardize_features = TRUE`, with the actual ranges.** In this table `Vitamins_and_Minerals` runs 0 to 100 while `Fat` runs 0 to 5. Without standardizing, a 30-point difference in fortification contributes 36 times more squared distance than the entire range of fat, and the model would cluster on the vitamin column alone while formally including four features it effectively ignores. Standardizing rescales each feature to mean 0 and standard deviation 1, so every column gets an equal vote.

**Why `EUCLIDEAN` rather than `COSINE`.** Euclidean is straight-line distance, which matches the question: group cereals with genuinely similar nutritional amounts. Cosine compares direction rather than magnitude, so it would call a 50-calorie and a 150-calorie cereal nearly identical as long as their nutrient proportions matched. Cosine is right when the shape of a profile matters and its size does not, as with text documents or a customer's spending mix. Here size matters. Start with Euclidean unless you can name why not.

**Why `Cereal Name` and `Manufacturer` are not features.** They are text, so BQML would one-hot encode them and let brand identity contribute distance, giving you clusters that are partly about General Mills. You will attach the names back in Step 3.5, where they belong: as labels on the result, not as inputs to it.

### 3.4 Read the centroids and name the clusters

```sql
SELECT
  feature,
  ROUND(MAX(IF(centroid_id = 1, numerical_value, NULL)), 1) AS cluster_1,
  ROUND(MAX(IF(centroid_id = 2, numerical_value, NULL)), 1) AS cluster_2,
  ROUND(MAX(IF(centroid_id = 3, numerical_value, NULL)), 1) AS cluster_3
FROM ML.CENTROIDS(MODEL `ml.cereal_clusters`)
GROUP BY feature
ORDER BY feature;
```

The pivot is worth the extra lines. Reading centroids means comparing a feature *across* clusters, and the default long format makes you do that by scrolling.

Because you clustered on real units and let BQML handle standardizing internally, `ML.CENTROIDS` reports values back in real units. A centroid is the average member of its group, so you can read these numbers as a nutrition label for an imaginary typical cereal.

> **Reference centroids.** Cluster ID numbers are arbitrary and yours will be in a different order:
>
> | Feature | Group A | Group B | Group C |
> |---------|--------:|--------:|--------:|
> | `Calories` | 93.6 | 115.3 | 116.7 |
> | `Protein__g_` | 2.8 | 2.1 | 2.7 |
> | `Fat` | 0.5 | 1.4 | 0.8 |
> | `Sugars` | 3.2 | 10.6 | 6.3 |
> | `Vitamins_and_Minerals` | 20.5 | 24.3 | **100.0** |
> | members | 33 | 34 | 6 |
>
> This solution was stable across ten different random starts: same three groups, same sizes, every time.

**Now name them, from the numbers:**

| Name | The centroid values that justify it |
|------|--------------------------------------|
| **Plain adult cereals** (Group A) | Lowest sugar at 3.2 g, lowest fat at 0.5 g, lowest calories at 94, highest protein at 2.8 g |
| **Sweetened cereals** (Group B) | Highest sugar at 10.6 g, more than triple Group A, with the highest fat at 1.4 g and the lowest protein at 2.1 g |
| **Heavily fortified brands** (Group C) | `Vitamins_and_Minerals` at 100 against a table-wide average of 28, with mid-range sugar at 6.3 g |

Group C is worth a second look because it teaches something about how clustering actually behaves. Fortification in this data is not spread out, it is trimodal: **60 cereals sit at exactly 25, seven at 0, and six at 100.** Those six sit so far from everyone else on that one feature that K-Means spends an entire cluster on them, no matter what the other four columns say. That is not a flaw, it is the algorithm faithfully reporting that your data contains a small extreme group. But it does mean one of your three clusters is defined by a single feature, and you should say so rather than pretend it is a rich nutritional profile.

**A cluster you cannot name is a cluster nobody will use.** Naming is the deliverable.

### 3.5 Assign cereals, then check your names against reality

```sql
CREATE OR REPLACE TABLE `ml.cereal_clustered_results` AS
SELECT
  CENTROID_ID AS cluster_id,
  cereal_name,
  Manufacturer,
  Calories, Protein__g_, Fat, Sugars, Vitamins_and_Minerals
FROM ML.PREDICT(
  MODEL `ml.cereal_clusters`,
  (SELECT
     `Cereal Name` AS cereal_name,
     Manufacturer,
     Calories, Protein__g_, Fat, Sugars, Vitamins_and_Minerals
   FROM `ml.cereal_nutrition`
   WHERE Sugars >= 0)
);
```

`cereal_name` and `Manufacturer` were not features, so the model ignores them and passes them through untouched. Aliasing `` `Cereal Name` `` to `cereal_name` here saves you backticks in every downstream query.

The `WHERE Sugars >= 0` is repeated for the same reason the `SAFE_CAST` was repeated in Task 1: **prediction input must be prepared exactly like training input.** Drop it and `Quaker_Oatmeal` gets scored by a model that never saw a -1 and has no sensible place to put it.

```sql
SELECT
  cluster_id,
  COUNT(*) AS n,
  ROUND(AVG(Sugars), 1) AS avg_sugar,
  ROUND(AVG(Vitamins_and_Minerals), 1) AS avg_vitamins,
  STRING_AGG(cereal_name, ', ' ORDER BY cereal_name LIMIT 8) AS examples
FROM `ml.cereal_clustered_results`
GROUP BY cluster_id
ORDER BY cluster_id;
```

> **What you should see:** 73 rows across 3 clusters, sized about 33, 34, and 6, with membership like this:
>
> | Group | Members you should recognize |
> |-------|------------------------------|
> | Plain adult | All-Bran, Shredded Wheat (all three sizes), Corn Flakes, Rice Krispies, Grape-Nuts, Cheerios, Special K, Wheaties |
> | Sweetened | Smacks (15 g), Froot Loops (13 g), Cap'n Crunch (12 g), Frosted Flakes (11 g), Cocoa Puffs, Trix, Lucky Charms, Golden Grahams |
> | Heavily fortified | Product 19, Total Corn Flakes, Total Whole Grain, Total Raisin Bran, both Just Right varieties |

**This is the validation step, and it is the only one available to you.** There is no accuracy score for a clustering. What you have instead is your own knowledge of breakfast cereal, which for this dataset is an excellent test. Froot Loops and Smacks landing together in the group you named "sweetened" confirms the interpretation. Shredded Wheat landing there would have refuted it.

Two membership details worth putting in your write-up, because they show the model is doing something more interesting than sorting by one column:

**Cheerios and Honey Nut Cheerios split.** Same brand, same shape, 1 g of sugar versus 10 g. They land in different clusters. That is the model grouping on nutrition rather than branding, which is exactly what you asked for by leaving `Manufacturer` out of the features.

**100% Natural Bran lands with the sweetened cereals.** It sounds like a health food and the name suggests Group A, but it carries 8 g of sugar and 5 g of fat, the highest fat in the table. Raisin Bran and Cracklin' Oat Bran join it for the same reason. **The model is right and the label on the box is misleading**, which is a genuinely useful finding and a better line in a write-up than a cluster with no surprises in it.

If your names do not survive this check, rename the clusters and say what forced the change. Revising an interpretation because the members contradicted it is the process working, not a mistake to hide.

### Check the quality metrics

```sql
SELECT davies_bouldin_index, mean_squared_distance
FROM ML.EVALUATE(MODEL `ml.cereal_clusters`);
```

> **Reference:** Davies-Bouldin index about **1.10**, and a mean squared distance a little under 3 on standardized features.

**Davies-Bouldin** combines how tight each cluster is with how far apart the clusters are. Lower is better. There is no universal threshold for "good," so the number is only meaningful as a comparison between two models on the same data. That is why choosing `k` always means training more than one model.

**Mean squared distance** is the average squared distance from each point to its own centroid. Lower looks better, and this is a trap: it falls automatically every time you add a cluster, all the way to zero when every point is its own cluster. **Never optimize it alone.**

### Stretch: choose k honestly

```sql
CREATE OR REPLACE MODEL `ml.cereal_clusters_k5`
OPTIONS(model_type = 'KMEANS', num_clusters = 5,
        distance_type = 'EUCLIDEAN', standardize_features = TRUE) AS
SELECT Calories, Protein__g_, Fat, Sugars, Vitamins_and_Minerals
FROM `ml.cereal_nutrition`
WHERE Sugars >= 0;

SELECT 'k=3' AS model, davies_bouldin_index, mean_squared_distance
FROM ML.EVALUATE(MODEL `ml.cereal_clusters`)
UNION ALL
SELECT 'k=5', davies_bouldin_index, mean_squared_distance
FROM ML.EVALUATE(MODEL `ml.cereal_clusters_k5`);
```

> **Reference results:**
>
> | | Davies-Bouldin | Mean squared distance | Cluster sizes |
> |---|---:|---:|---|
> | k=3 | 1.098 | 2.73 | 33, 34, 6 |
> | k=5 | **1.063** | 1.79 | 25, 22, 12, 8, 6 |
>
> `k=5` wins on the index, narrowly. The mean squared distance drops by a third, which tells you nothing, because it always drops.

So answer both halves of the question:

1. **Which k scores better?** `k=5`, by 0.035 on Davies-Bouldin. That is a very thin margin on 73 rows.
2. **Can you name all five?** Try it. Two of the five hold 8 and 6 cereals, and the split inside the sweetened family comes down to a couple of grams of sugar and a gram of fat. You will find yourself naming groups "sweetened" and "slightly more sweetened," which is not a distinction a shopper or a category manager can act on.

**The strong answer keeps k=3 and explains the override:** the metric improvement is inside the noise for a table this small, and three groups can be named, defended, and used, while five cannot. Clustering output is consumed by humans, so interpretability is not a soft consideration, it is the requirement. Explaining why you overrode a metric is a better answer than following it silently.

---

## Task 4: Forecasting

### The concept first: what makes time series different

In Tasks 1 through 3 you could shuffle the rows and nothing would change. Here the sequence *is* the signal. That single difference drives everything below.

`ARIMA_PLUS` models the series as a sum of parts:

```
value = trend + seasonality + holiday effects + noise
```

**Trend** is the long-run direction. **Seasonality** is the repeating cycle. **Noise** is what is left. The model's job is to separate them, then extend the trend and the seasonality forward while admitting it cannot extend the noise.

It also means a random train/test split is invalid, not merely suboptimal. Holding out a random 20 percent puts future months in training and past months in evaluation, so the model would be predicting the past having already seen the future. That is impossible at inference time, and it makes your measured performance a fiction. `ARIMA_PLUS` handles sequencing internally, which is why you never pass it a split.

### 4.1 Inspect, and run the duplicate check

```sql
SELECT
  MIN(date) AS first_month,
  MAX(date) AS last_month,
  COUNT(*) AS n_rows,
  COUNT(DISTINCT date) AS distinct_dates
FROM `ml.air_passengers`;
```

> **What you should see:** 144 rows, **1949-01-31 to 1960-12-31**, and `n_rows = distinct_dates = 144`.

**That equality is a required pre-flight check.** `ARIMA_PLUS` needs exactly one row per timestamp; duplicates fail training with an error that does not obviously say "duplicates." The check costs one query. In real work the usual cause is a source table storing multiple grains together, for example national and regional rows for the same date, and the fix is `GROUP BY date` with an aggregate before you train.

**On the `date` column type: check first, then decide.** Your Setup query already reported that `date` is a `DATE`, because the values are clean `YYYY-MM-DD` strings that auto-detect parsed successfully. So use the column directly.

Do **not** wrap it in `PARSE_DATE`. `PARSE_DATE` converts a `STRING` into a `DATE`; hand it something already a `DATE` and you get:

```
No matching signature for function PARSE_DATE for argument types: STRING, DATE
```

This is worth generalizing. Task 1 needed a cast and Task 4 does not, and both facts came from the same `INFORMATION_SCHEMA` query. Defensively wrapping conversions around columns that do not need them is not "safe," it is a second way to fail. **Read the type, then write the code.**

### 4.2 Train

```sql
CREATE OR REPLACE MODEL `ml.air_passenger_model`
OPTIONS(
  model_type = 'ARIMA_PLUS',
  time_series_timestamp_col = 'date',
  time_series_data_col = 'passengers',
  data_frequency = 'MONTHLY',
  decompose_time_series = TRUE
) AS
SELECT date, passengers
FROM `ml.air_passengers`;
```

| Option | Why it is here |
|--------|----------------|
| `time_series_timestamp_col = 'date'` | Names the time axis. Note it takes the column name as a **string** |
| `time_series_data_col = 'passengers'` | Names the value being forecast |
| `data_frequency = 'MONTHLY'` | These dates land on month ends, so the gaps vary from 28 to 31 days. Auto-detection handles that, but stating it removes the ambiguity and documents your intent |
| `decompose_time_series = TRUE` | Stores the trend and seasonal components so `ML.EXPLAIN_FORECAST` can retrieve them later. Cheap now, impossible to add without retraining |

There is no `input_label_cols` and no data split. Everything else `ARIMA_PLUS` decides for itself: differencing order, seasonal period, and its own ARIMA parameters. That automation is why two lines of options buy you a fairly serious statistical model.

### 4.3 Evaluate

```sql
SELECT non_seasonal_p, non_seasonal_d, non_seasonal_q,
       has_seasonality, seasonal_periods, AIC, log_likelihood
FROM ML.EVALUATE(MODEL `ml.air_passenger_model`);
```

> **What you should see:** `has_seasonality` is **true** and `seasonal_periods` contains **YEARLY**.

Do not look for R² here. Time-series evaluation answers a different question, namely "did the model find the structure that is actually in this series."

| Column | Plain reading |
|--------|---------------|
| `has_seasonality`, `seasonal_periods` | Whether a repeating cycle was detected, and its period. **This is your confirmation check** |
| `non_seasonal_d` | How many times the series had to be differenced (subtracting the previous value) to remove the trend. A `d` of 1 says "this series rises, so the model works with month-to-month changes" |
| `non_seasonal_p`, `non_seasonal_q` | How many past values and how many past errors the model uses. `auto_arima` chose these by trying combinations |
| `AIC` | Fit quality with a penalty for complexity. Lower is better, comparable only between models on the same series |
| `log_likelihood` | How well the model fits the history. Higher is better |

`has_seasonality = true` with a yearly period is the line that matters, because you can verify it independently. Air travel peaks every summer, visibly, in a chart or a pivot of the raw data. In this table July and August run about **71 passengers above** their own year's average while November and February run about 45 to 48 **below**. A model that reported no seasonality on this series would be telling you it missed something you can see with your eyes, and that would be a red flag pointing at a mis-detected frequency, not at the data.

### 4.4 Forecast 12 months

```sql
SELECT
  forecast_timestamp,
  ROUND(forecast_value, 0) AS forecast,
  ROUND(prediction_interval_lower_bound, 0) AS lower_bound,
  ROUND(prediction_interval_upper_bound, 0) AS upper_bound
FROM ML.FORECAST(
  MODEL `ml.air_passenger_model`,
  STRUCT(12 AS horizon, 0.95 AS confidence_level)
);
```

`horizon` is how many periods forward, so 12 months here. `confidence_level = 0.95` produces bounds meaning "we are 95 percent confident the true value falls between lower and upper."

> **What you should see:** 12 rows covering 1961, following the summer-peak shape, every month above its 1960 counterpart.
>
> **Sanity-check it against the data instead of trusting it.** 1960 ran from 390 in November to 622 in July, averaging 476. The series has been adding roughly 32 passengers per year to its average, and grew about 11 percent from 1959 to 1960. So a July 1961 forecast in the neighborhood of 640 to 700 is consistent with the history; a July 1961 forecast of 500, or of 1,200, would mean something went wrong. Build that habit of bracketing a forecast from the raw data before you accept it.

**Look at the interval width in month 1 against month 12.** It grows, noticeably and monotonically. Explain in your write-up why that is correct behavior rather than a defect:

Each forecast step is built on the step before it, so uncertainty compounds as you move away from the last real observation. The trend and seasonal estimates were fitted on data through December 1960, and the further past that you project, the more room there is for those estimates to be slightly off. Widening intervals are the model reporting its own growing ignorance honestly.

**A flat interval twelve months out would be the alarming result.** It would mean the model claims to know 1961 as well as it knows early 1961, which nothing can. And always publish the interval alongside the forecast: a bare number hides exactly the information a decision-maker needs in order to decide how much to bet on it.

### 4.5 Build the dashboard table

```sql
CREATE OR REPLACE TABLE `ml.air_passengers_with_forecast` AS
SELECT
  date,
  CAST(passengers AS FLOAT64) AS passengers,
  'actual' AS row_type,
  NULL AS lower_bound,
  NULL AS upper_bound
FROM `ml.air_passengers`

UNION ALL

SELECT
  DATE(forecast_timestamp),
  forecast_value,
  'forecast',
  prediction_interval_lower_bound,
  prediction_interval_upper_bound
FROM ML.FORECAST(
  MODEL `ml.air_passenger_model`,
  STRUCT(12 AS horizon, 0.95 AS confidence_level)
);

SELECT row_type, COUNT(*) AS n
FROM `ml.air_passengers_with_forecast`
GROUP BY row_type;
```

> **What you should see:** 144 `actual` rows and 12 `forecast` rows, forming one continuous series with bounds populated on the forecast rows only.

Three details in that statement earn their place.

**`CAST(passengers AS FLOAT64)`.** `UNION ALL` requires matching types across branches. `passengers` loaded as `INT64` and `forecast_value` is `FLOAT64`, so without the cast the query fails on a type mismatch. Worth working through rather than copying: reconciling types across branches of a union is routine warehouse work.

**`DATE(forecast_timestamp)`.** `ML.FORECAST` returns a `TIMESTAMP` even though you trained on a `DATE`. Converting keeps one date type in the output column so a chart can order it.

**`row_type`.** This is what makes the table safe to hand to someone. A chart can style the two segments differently, and no analyst can accidentally average a prediction together with a measurement. Mark generated rows, always.

**Then stop and look at what you just produced.** One SQL statement, one table, containing twelve years of history and twelve months of forecast with confidence bounds, ready for Looker or Tableau to chart directly. No export, no Parquet conversion, no Python environment, no pickle file to version, no serving container, no orchestration between three systems. Schedule this query and the forecast refreshes itself.

That is the entire argument for doing this class of ML in the warehouse, and it is why a data engineer who knows BQML can deliver a forecast on their own.

### Stretch: decompose and detect

```sql
SELECT
  time_series_timestamp,
  ROUND(time_series_data, 1) AS actual,
  ROUND(trend, 1) AS trend,
  ROUND(seasonal_period_yearly, 1) AS yearly_seasonality
FROM ML.EXPLAIN_FORECAST(
  MODEL `ml.air_passenger_model`,
  STRUCT(12 AS horizon, 0.95 AS confidence_level)
)
ORDER BY time_series_timestamp DESC
LIMIT 24;
```

> **What you should see:** `trend` rising steadily across the whole series with no reversals, and `yearly_seasonality` peaking mid-year and dipping in the late autumn. The two components plus the remainder add back up to `actual` on historical rows.

The stakeholder sentence is the deliverable here, and the raw data supports it directly. Annual average traffic grew from 127 in 1949 to 476 in 1960, about **32 additional passengers per year** on the annual average. July and August sit about **70 above** their own year's average, November about 48 below.

> "Passenger volume has grown by roughly 30 per year every year since 1949, and on top of that growth, July and August each run about 70 above the year's own average while November runs about 50 below."

That sentence is worth more than the forecast table it came from, because it tells the business *why* the next number is what it is. Someone can act on it: staff up for summer, and plan capacity growth annually.

```sql
SELECT *
FROM ML.DETECT_ANOMALIES(
  MODEL `ml.air_passenger_model`,
  STRUCT(0.95 AS anomaly_prob_threshold)
)
WHERE is_anomaly;
```

Select `*` the first time you run this. The output carries `is_anomaly`, `anomaly_probability`, `lower_bound`, and `upper_bound` alongside your own `date` and `passengers` columns, with the timestamp column named after your `time_series_timestamp_col` and returned as a `TIMESTAMP`. Look at what is actually there before you write a column list.

> **What you should see:** few or no flagged months at 0.95. This series is unusually smooth, which is why it is a teaching classic.

Then lower the threshold to 0.8 and run it again. More months get flagged. Be precise about what you changed:

**You did not discover more anomalies. You widened the definition of one.** The threshold sets how far outside the model's expected band a point must fall before it earns the label. It is a sensitivity dial, and where you set it is a business decision about the cost of a false alarm against the cost of a miss, exactly like the classification threshold in Task 2. That is why "the model found 14 anomalies" is a meaningless claim on its own, and "the model flagged 14 months at a 0.8 threshold" is a real one.

This is also a genuinely useful production pattern beyond forecasting: train `ARIMA_PLUS` on a pipeline metric such as daily row counts or job duration, then alert whenever reality leaves the expected band. You get data quality monitoring that learns what normal looks like, including normal seasonality, instead of a static threshold somebody has to keep retuning.

---

## Model Answers to the Written Questions

**1a.** `horsepower` loaded as `STRING` because 6 of its 398 values are the literal `?` rather than a number, and BigQuery's auto-detect types a whole column as `STRING` when any value fails to parse as numeric. Untreated, `LINEAR_REG` would treat the column as categorical and one-hot encode its 94 distinct values into roughly 94 indicator features, learning an unrelated weight for each and losing any notion that 130 is larger than 100. `ML.WEIGHTS` would then show `NULL` in the `weight` column for `horsepower` plus a large `category_weights` array, so there would be no single horsepower weight to report. No error would be raised at any point.

**1b.** Vehicle `weight`. The default `ML.WEIGHTS` ranking puts `cylinders` first (about -0.36) and `weight` last (about -0.005), while the standardized ranking puts `weight` first (about -4.5) and `cylinders` third (about -0.6). They disagree because default weights are stated per one unit of each feature, and a unit means something completely different in each column: one pound out of a 1,613 to 5,140 lb range is negligible, while one cylinder out of a 3 to 8 range is enormous. Ranking raw weights therefore ranks units rather than influence. Standardized weights restate every weight as the effect of a one standard deviation move, which is a comparable amount of change for each feature, so the standardized ranking is the one that answers the business question. It also matches physical intuition, since moving more mass takes more fuel.

**1c.** `car_mpg` has 398 rows, which is below BQML's 500-row threshold, so `AUTO_SPLIT` would have trained on all of them and held nothing back, leaving `ML.EVALUATE` reporting training-set metrics that look exactly like honest ones. Task 1 asks for a performance figure you could defend, so it forces `data_split_method = 'RANDOM'` with a 20 percent holdout. Task 2 has only 100 rows, where a 20 percent holdout would be 20 applicants and any metric computed on it would be too unstable to mean anything. There the point is the opposite: read the most flattering possible numbers, measured on the training rows themselves, and observe that even those fail to clear the 53 percent baseline.

**2a.** The majority-class baseline is 53 percent, achieved by always answering `deny` (53 of 100 rows are `deny`). Model accuracy lands somewhere around 60 to 68 percent depending on the run, a gain of roughly 7 to 15 points over doing nothing at all, and that gain is measured on the same rows the model trained on.

**2b.** An ROC AUC near 0.68 means that given one real `approve` applicant and one real `deny` applicant, the model ranks them correctly about two times in three, against one in two for a coin flip. It sits much closer to the 0.5 floor than to a usable model, so there is very little separable signal in these five features. Because there was no holdout, the true figure on unseen applicants would be lower still.

**2c.** Read as a sentence, the model says: "the more debt and mortgage an applicant carries the more likely we approve them, while income and credit score make almost no difference." That is not plausible; no lender approves on debt load and ignores income and credit. It tells you the model is describing random variation in 100 rows rather than lending behavior. The precise reading matters here: `liabilities` is the largest weight and it is pointing the wrong way, while `income` and `credit_score` are not strongly negative but effectively zero, with signs that flip across roughly a third of bootstrap resamples of the same data. A near-zero weight has no reliable sign, so the defensible claim is that the two features underwriting actually depends on carry no weight at all.

**2d.** See the model answer in Section 2.5.

**3a.** `Sugars = -1` on `Quaker_Oatmeal`, a sentinel value standing in for missing data. It damages clustering more than regression for two reasons. First, K-Means assigns membership purely by distance, so a false extreme pulls that row toward the wrong group. Second, and worse, because features are standardized the mean and standard deviation of `Sugars` are computed from the column including the -1 (mean 6.77 and standard deviation 4.47 with it, versus 6.88 and 4.40 without), so every other cereal is rescaled using numbers a fabricated value helped produce. One bad cell perturbs the entire model rather than one row's contribution. `SAFE_CAST` cannot catch it because `-1` is a perfectly valid `INT64`; nothing errors and no type changes. Only knowing that sugar cannot be negative reveals it, which is why `MIN` and `MAX` on every numeric column belongs in your pre-training routine.

**3b.** Three clusters, named from the centroid values: **plain adult cereals** (sugar 3.2 g, fat 0.5 g, calories 94, the highest protein at 2.8 g); **sweetened cereals** (sugar 10.6 g, more than triple the first group, fat 1.4 g, the lowest protein at 2.1 g); and **heavily fortified brands** (`Vitamins_and_Minerals` at 100 against a table average of 28). Worth stating alongside the names: the third cluster is defined almost entirely by one feature, because fortification in this data is trimodal at 0, 25, and 100, and only six cereals sit at 100.

**3c.** Yes. The sweetened cluster contains Smacks, Froot Loops, Cap'n Crunch, Frosted Flakes, Cocoa Puffs, and Trix, and the plain cluster contains All-Bran, all three Shredded Wheat varieties, Corn Flakes, and Grape-Nuts, which is what those names predict. Two membership details confirm the model is grouping on nutrition rather than branding: Cheerios (1 g of sugar) and Honey Nut Cheerios (10 g) land in different clusters despite the shared brand, and 100% Natural Bran lands with the sweetened cereals because it carries 8 g of sugar and the highest fat in the table at 5 g, in spite of a name that suggests otherwise.

**4a.** `PARSE_DATE` converts a `STRING` into a `DATE`, and this column is already a `DATE`, so the call fails with `No matching signature for function PARSE_DATE for argument types: STRING, DATE`. I knew before running it because the `INFORMATION_SCHEMA.COLUMNS` query in Setup reported `date` as `DATE`; auto-detect parsed the clean `YYYY-MM-DD` values successfully on upload. The general lesson is to read the type and then write the code, since an unnecessary conversion fails just as loudly as a missing one.

**4b.** Each forecast step is computed from the steps before it, so uncertainty compounds with distance from the last real observation, and the fitted trend and seasonal components have more room to drift the further you project past the data they were estimated from. The widening interval is the model reporting its own growing uncertainty honestly. A constant interval width twelve months out would be the suspicious result, because it would claim the model knows December 1961 as precisely as it knows January 1961.

**4c.** A random split would place future months in the training set and past months in the evaluation set, letting the model learn from the future in order to predict the past. That inflates measured performance and describes a situation that cannot exist at inference time, when only the past is available. Time-series validation has to respect chronological order, training on an earlier window and evaluating on a later one, and `ARIMA_PLUS` handles that sequencing internally, which is why you never pass it a `data_split_method`.

---

## What You Should Be Able to Do Now

The SQL in this lab was 6 to 12 lines per model. These habits are the part that transfers, and none of them are specific to BigQuery.

| Habit | The query or check |
|-------|--------------------|
| Read types before writing model SQL | `INFORMATION_SCHEMA.COLUMNS` |
| Find sentinel values and impossible ranges | `MIN` and `MAX` on every numeric column |
| Know what "doing nothing" scores before you train | majority-class `GROUP BY` for classification |
| Insist on an honest holdout | explicit `data_split_method` below 500 rows |
| Rank features fairly | `ML.WEIGHTS` with `STRUCT(TRUE AS standardize)` |
| Distinguish a finding from noise | does the conclusion survive a change in preprocessing? |
| Validate an unsupervised model | name the clusters, then check the members against what you know |
| Verify a time-series model found the obvious | `has_seasonality` and one row per timestamp |
| Publish uncertainty with every prediction | prediction intervals, and a `row_type` column marking generated rows |
| Recommend against your own model when the evidence says so | Task 2 |

Everything you did here maps directly onto scikit-learn, Spark MLlib, and Snowflake ML. `CREATE MODEL` is `fit`, `ML.PREDICT` is `predict`, `ML.EVALUATE` is a metrics call, `standardize_features` is a `StandardScaler`. What changes between platforms is syntax. What does not change is that a model with no baseline, no holdout, and no sanity check on its weights is not a result, it is a liability with good formatting.

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `Unrecognized name` on a cereal column | You typed the name from the CSV header instead of the normalized one | Run the `INFORMATION_SCHEMA` query in Setup and copy the names from it |
| `No matching signature for function PARSE_DATE` | You wrapped a column that is already a `DATE` | Use `date` directly (Step 4.1) |
| `ML.WEIGHTS` shows `NULL` for `horsepower` plus a big `category_weights` array | You trained without `SAFE_CAST`, so the column was treated as categorical | Step 1.1, the column is a `STRING` because of 6 `?` values |
| Prediction fails after training succeeded | `SAFE_CAST` applied at training but not at prediction | Prepare features identically in both places (Step 1.5) |
| Type mismatch in the Task 4 `UNION ALL` | `passengers` is `INT64`, `forecast_value` is `FLOAT64` | `CAST(passengers AS FLOAT64)` (Step 4.5) |
| Your model's feature is named `f0_` | You wrote an expression without an alias | Alias engineered features, for example `SAFE_CAST(...) AS horsepower` |
| Your loan model scored 62 percent and you thought that was fine | You never ran the baseline | Step 2.1, compare against 53 percent |
| Your cluster IDs do not match a classmate's | Expected. K-Means numbers clusters arbitrarily | Compare centroid descriptions and membership, never ID numbers |
| Task 1 R² is outside the stated range | The random split drew a different holdout | Normal between about 0.61 and 0.75. Outside that, check your `SAFE_CAST` and your feature list |
| Task 3 trained on 74 rows instead of 73 | The `WHERE Sugars >= 0` filter is missing | Step 3.2, the sentinel row must be excluded from training and from prediction |

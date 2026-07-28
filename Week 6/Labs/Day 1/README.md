# Week 6 · Day 1: Databricks Project Debrief, Cross-Tool Refresher, BigQuery ML, and Architecture Decisions

Today's session connects your Week 5 Databricks engineering work with cross-tool DataFrame fluency across Pandas, Polars, and Snowpark, culminating in SQL-native Machine Learning with BigQuery ML.

---

## Session Sequence Arc

| Block | Focus | Pedagogical Intent & Activity |
|-------|-------|-------------------------------|
| **Block 1** | **Databricks Project Debrief** | **Student Presentations**: Intern teams present their Week 5 Databricks Million Song Data Warehouse solutions, defending PySpark transformations, Unity Catalog schemas, and scalability decisions ([Activity 0](./Activity_0_Databricks_Mini_Project_Presentations.md)). |
| **Block 2** | **Cross-Tool Refresher** | **Multi-Engine Fluency**: Compare how identical data engineering operations work across SQL, Pandas, Polars, PySpark, and Snowpark ([Activity 1](./Activity_1_Cross_Tool_SQL_to_Pandas_Drills.ipynb) and [Activity 2](./Activity_2_Window_Functions_in_Pandas.ipynb)). |
| **Block 3** | **DataFrame API Comparison** | **Snowpark and PySpark**: Code-along and solo practice building lazy DataFrame pipelines in Snowpark that mirror PySpark syntax ([Code-Along](./Code_Along_Snowpark_Basics.ipynb) and [Activity 3](./Activity_3_Snowpark_First_Flight.ipynb)). |
| **Block 4** | **BigQuery ML Self-Study** | **SQL-Native Machine Learning**: Guided self-study on building ML models directly inside BigQuery without data egress ([Activity 4](./Activity_4_BigQueryML_SelfStudy.md)). |
| **Block 5** | **BigQuery ML Activity Lab** | **Hands-On Practice**: Students build, evaluate, and inspect four machine learning models in the BigQuery SQL editor ([Activity 5](./Activity_5_BigQueryML_HandsOnLab.md)). |
| **Block 6** | **Boardroom Architecture Showdown** | **Strategy and Communication Practice**: Three teams receive the same greenfield insurance challenge, research two credible approaches, compare one anchor decision, create draw.io diagrams, and present a recommendation to the instructor acting as the business stakeholder ([Group Activity](./Group_Activity_Boardroom_Architecture_Showdown.md)). |

---

## Detailed Lab Breakdown

### Part 1: Databricks Project Presentations
- **Activity 0**: Team presentations of the Week 5 Databricks ETL Project. Focus on PySpark DataFrame logic, Star Schema design, data quality checks, and architectural tradeoffs.

### Part 2: Cross-Tool Refresher (Pandas, Polars, Snowpark, PySpark)
- **Activity 1 (Cross-Tool SQL vs Pandas vs Polars Drills)**: Take SQL queries you know cold and match their outputs line-by-line using Pandas and Polars DataFrame methods.
- **Activity 2 (Window Functions in Pandas & Polars)**: Translate SQL `OVER (PARTITION BY ... ORDER BY ...)` clauses into Pandas (`.shift()`, `.pct_change()`, `.rolling()`) and Polars window expressions (`.over()`).
- **Code-Along (Snowpark Basics)**: Learn lazy evaluation, query plan generation (`.explain()`), and DataFrame transformations in Snowpark.
- **Activity 3 (Snowpark First Flight)**: Build a multi-window claims aggregation pipeline in Snowpark and write tables back to Snowflake.

### Part 3: BigQuery ML (SQL Machine Learning)
- **Activity 4 (BQML Self-Study Walkthrough)**: Guided walkthrough of `ARIMA_PLUS` time-series forecasting, `KMEANS` clustering, `LINEAR_REG`, `LOGISTIC_REG`, `l1_reg` / `l2_reg` regularization penalties, feature weights (`ML.WEIGHTS`), and metrics (`ML.EVALUATE`).
- **Activity 5 (BQML Hands-On Student Lab)**: Build 4 ML models directly in BigQuery Sandbox using `air_passenger.csv`, `mpg.csv`, `loans.csv`, and `cereal.csv`.

### Part 4: Architecture Evaluation and Client Defense

- **Reading**: Learn how senior data engineers frame business needs, research unfamiliar tools, compare trade-offs, make a recommendation, and communicate it in plain language.
- **Group Activity**: Three teams of three complete the same Juniper Shield Insurance challenge in 210 minutes. Each team creates a main and alternative architecture in draw.io, builds a six-slide proposal, and presents to the instructor acting as the business stakeholder.
- **Presentation Template**: Use the slide-by-slide scaffold to organize an exact 15-minute boardroom presentation, followed by three minutes of stakeholder Q&A and two minutes of immediate feedback. There is no written proposal, file submission, or activity grade.

*Instructor solutions:* Located in the `solutions/` folder.

---

## Lab Index

Provided files:

| File | Purpose |
|------|---------|
| `Activity_0_Databricks_Mini_Project_Presentations.md` | Presentation guidelines and peer discussion rubric for Week 5 Databricks ETL project |
| `Activity_1_Cross_Tool_SQL_to_Pandas_Drills.ipynb` | Hands-on drills translating SQL filtering and aggregations into Pandas and Polars |
| `Activity_2_Window_Functions_in_Pandas.ipynb` | Practice translating SQL window functions into Pandas and Polars window expressions (`.over()`) |
| `Code_Along_Snowpark_Basics.ipynb` | Instructor code-along notebook introducing Snowpark lazy DataFrame API |
| `Activity_3_Snowpark_First_Flight.ipynb` | Student practice activity building a Snowpark window aggregation pipeline |
| `Activity_4_BigQueryML_SelfStudy.md` | Guided Markdown walkthrough covering BQML time-series, clustering, GLM, L1/L2 regularization, and metrics |
| `Activity_5_BigQueryML_HandsOnLab.md` | Student hands-on activity lab requiring creation of 4 BQML models in BigQuery SQL Editor |
| `Reading_Evaluating_Data_Platform_Architectures.md` | Learner explainer on strategic thinking, research, open-source effort, tool evaluation, diagrams, and business communication |
| `Group_Activity_Boardroom_Architecture_Showdown.md` | Three-and-a-half-hour insurance architecture challenge for three teams completing the same assignment |
| `starter/Insurance_Architecture_Presentation_Template.md` | Six-slide planning scaffold for the live boardroom presentation and stakeholder discussion |
| `solutions/Activity_1_Cross_Tool_SQL_to_Pandas_Drills_Solution.ipynb` | Solution notebook for Activity 1 (Pandas & Polars solutions) |
| `solutions/Activity_2_Window_Functions_in_Pandas_Solution.ipynb` | Solution notebook for Activity 2 (Pandas & Polars solutions) |
| `solutions/Activity_3_Snowpark_First_Flight_Solution.ipynb` | Solution notebook for Activity 3 |
| `solutions/Activity_5_BigQueryML_HandsOnLab_Solution.md` | Instructor reference solution guide for Activity 5 |
| `datasets/timeseries/air_passenger.csv` | Monthly airline passenger records for Time-Series Forecasting |
| `datasets/regression/mpg.csv` | Vehicle performance specs for Continuous Value Regression |
| `datasets/classification/loans.csv` | Loan financial indicators for Binary Classification |
| `datasets/clustering/cereal.csv` | Cereal nutritional information for K-Means Clustering |
| `feedback_sample.csv` | 10-row subset of rider feedback for Prompt Lab Challenges A & C |
| `answer_key_20.csv` | 20 feedback rows with hidden labels for Challenge B |

Files you create (submit via PR):

| File | Purpose |
|------|---------|
| `student-work/week6/day1/` | Completed notebooks (Activities 1, 2, 3) and BigQuery ML SQL scripts (Activity 5) |
| `prompts.md` | Final prompt per challenge, before/after accuracy for Challenge B, top 3 lessons learned |

The Boardroom Architecture Showdown is presented live. Its working slides and draw.io diagrams are not submitted or scored.

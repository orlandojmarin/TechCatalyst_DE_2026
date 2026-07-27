# Week 6 · Day 1: Databricks Project Debrief, Cross-Tool Refresher, & BigQuery ML

Today's session connects your Week 5 Databricks engineering work with cross-tool DataFrame fluency across Pandas, Polars, and Snowpark, culminating in SQL-native Machine Learning with BigQuery ML.

---

## Session Sequence Arc

| Block | Focus | Pedagogical Intent & Activity |
|-------|-------|-------------------------------|
| **Block 1** | **Databricks Project Debrief** | **Student Presentations**: Intern teams present their Week 5 Databricks Million Song Data Warehouse solutions, defending PySpark transformations, Unity Catalog schemas, and scalability decisions ([Activity_0_Databricks_Mini_Project_Presentations.md](file:///Users/tarekatwan/Repos/MyWork/Teach/repos/TechCatalyst_DE_2026/Week%206/Labs/Day%201/Activity_0_Databricks_Mini_Project_Presentations.md)). |
| **Block 2** | **Cross-Tool Refresher** | **Multi-Engine Fluency**: Compare how identical data engineering operations (filters, GroupBy, Window functions) work across SQL, Pandas, Polars, PySpark, and Snowpark ([Activity_1_Cross_Tool_SQL_to_Pandas_Drills.ipynb](file:///Users/tarekatwan/Repos/MyWork/Teach/repos/TechCatalyst_DE_2026/Week%206/Labs/Day%201/Activity_1_Cross_Tool_SQL_to_Pandas_Drills.ipynb) & [Activity_2_Window_Functions_in_Pandas.ipynb](file:///Users/tarekatwan/Repos/MyWork/Teach/repos/TechCatalyst_DE_2026/Week%206/Labs/Day%201/Activity_2_Window_Functions_in_Pandas.ipynb)). |
| **Block 3** | **DataFrame API Comparison** | **Snowpark & PySpark**: Code-along and solo practice building lazy DataFrame pipelines in Snowpark that mirror PySpark syntax ([Code_Along_Snowpark_Basics.ipynb](file:///Users/tarekatwan/Repos/MyWork/Teach/repos/TechCatalyst_DE_2026/Week%206/Labs/Day%201/Code_Along_Snowpark_Basics.ipynb) & [Activity_3_Snowpark_First_Flight.ipynb](file:///Users/tarekatwan/Repos/MyWork/Teach/repos/TechCatalyst_DE_2026/Week%206/Labs/Day%201/Activity_3_Snowpark_First_Flight.ipynb)). |
| **Block 4** | **BigQuery ML Self-Study** | **SQL-Native Machine Learning**: Guided self-study walkthrough on building ML models directly inside BigQuery without data egress ([Activity_4_BigQueryML_SelfStudy.md](file:///Users/tarekatwan/Repos/MyWork/Teach/repos/TechCatalyst_DE_2026/Week%206/Labs/Day%201/Activity_4_BigQueryML_SelfStudy.md)). |
| **Block 5** | **BigQuery ML Activity Lab** | **Hands-On Practice**: Students build, evaluate, and inspect 4 machine learning models (Forecasting, Regression, Classification, Clustering) in BigQuery SQL Editor ([Activity_5_BigQueryML_HandsOnLab.md](file:///Users/tarekatwan/Repos/MyWork/Teach/repos/TechCatalyst_DE_2026/Week%206/Labs/Day%201/Activity_5_BigQueryML_HandsOnLab.md)). |

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

*Instructor Solutions:* Located in the `solutions/` folder.

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

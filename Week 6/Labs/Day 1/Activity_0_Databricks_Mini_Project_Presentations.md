# Activity 0: Databricks Mini-Project Student Presentations

**Format:** Team presentations and peer debriefing (approx. 5 to 7 minutes per intern team).  
**Prerequisites:** Completion of the Week 5 Databricks Million Song Data Warehouse Mini-Project.

---

## 1. Objective

Present your Databricks PySpark ETL pipeline and data warehouse architecture to the cohort. As a data engineer, your job is not only to write code, but also to defend your architectural choices, explain performance tradeoffs, and demonstrate how raw data was transformed into an analytical data warehouse.

---

## 2. Presentation Structure

Each intern team will walk through their solution covering the following four sections:

### 1. Architecture Overview
- How did your pipeline ingest raw JSON and CSV files from Databricks storage?
- What schema transformations, data cleaning, and deduplication steps were applied?

### 2. PySpark DataFrame Engineering
- Show 1 to 2 key PySpark transformations you implemented (e.g. `join`, `withColumn`, `groupBy`, window functions).
- Explain why you chose those specific PySpark functions over standard Python or SQL.

### 3. Data Warehouse Design
- Show your final Star Schema / Snowflake Schema tables created in Databricks Unity Catalog / Delta Lake.
- How do fact tables and dimension tables link together?

### 4. Lessons Learned and Trade-Offs
- What was the most challenging part of scaling PySpark operations on Databricks?
- What would you refactor if you had another day to work on this pipeline?

---

## 3. Peer Debrief & Discussion Questions

During peer presentations, non-presenting interns should formulate questions based on the following engineering criteria:
- **Scalability**: How well does the PySpark code handle partition skew or large aggregations?
- **Data Quality**: How were `NULL` values and duplicate records handled before loading into final tables?
- **Code Clarity**: Is the PySpark logic clean, modular, and easy to maintain?

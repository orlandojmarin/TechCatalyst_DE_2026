# Week 6 · Day 1: Student Resources: BigQuery ML & GenAI Foundations

> **The AI-free zone ends today.** Weeks 1 to 4 built the skills that let you review generated code and SQL. Starting now, AI is a tool, not a replacement for the accountability you practiced. Nothing merges that you cannot explain line by line.

---

## Core Documentation

| Resource | Why it helps |
|----------|-------------|
| [Polars User Guide](https://docs.pola.rs/) | Official guide to Polars expressions, lazy vs eager evaluation, and window expressions (`.over()`) |
| [Snowpark Developer Guide](https://docs.snowflake.com/en/developer-guide/snowpark/python/index) | Official reference for Snowpark Python Session, DataFrame API, and window functions |
| [BigQuery ML ARIMA_PLUS Syntax](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series) | Official GoogleSQL reference for time-series forecasting, seasonality, and anomaly detection |
| [BigQuery ML K-Means Syntax](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-kmeans) | Official GoogleSQL reference for K-Means unsupervised clustering, centroids, and distance metrics |
| [BigQuery ML GLM Syntax](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-glm) | Official GoogleSQL reference for Linear Regression (`LINEAR_REG`) and Logistic Regression (`LOGISTIC_REG`) |
| [Google AI Studio quickstart](https://ai.google.dev/gemini-api/docs/ai-studio-quickstart) | Where today's prompt lab runs: login, model picker, temperature slider, system prompt panel |
| [Gemini models overview](https://ai.google.dev/gemini-api/docs/models) | Context window sizes, pricing per million tokens (input vs output), model tiers |
| [Gemini prompting strategies](https://ai.google.dev/gemini-api/docs/prompting-strategies) | Official guide to role, format, few-shot, and constraints: the 6 levers |

---

## How LLMs Actually Work (Working-Engineer Level)

```
Your prompt
    │
    ▼
Tokenizer  →  [token IDs]  →  Billions of weights  →  Next token probability
                                (trained once,          distribution
                                 costs millions)
                                      │
                                      ▼
                              Sample next token
                              (temperature controls
                               how "adventurous")
                                      │
                                      └── repeat until stop token
```

**Three things to internalize:**

1. **No database lookup.** The model is pattern completion, not retrieval. It can invent plausible-sounding nonsense with zero hesitation.
2. **Training vs inference.** Training happens once and costs millions. Every API call you make is inference; that is where your costs live.
3. **Temperature.** Low (0 to 0.2) = deterministic, safe for classification and extraction. High (0.8 to 1.0) = creative, good for brainstorming. Default to low for DE work.

---

## Tokens: Cost and Memory

| Rule of thumb | Detail |
|---------------|--------|
| ~4 characters ≈ 1 token (English) | "taxi" = 1 token; "deduplication" = 3 tokens |
| Context window = working memory | Prompt + history + output all share this limit |
| Output costs more than input | Gemini Flash: input ~$0.075/M, output ~$0.30/M (check current pricing) |
| Instructions first, data after | Models weight the start and end of context more heavily |

**The DE math:** classifying 1M feedback rows = 1M API calls × (prompt tokens + response tokens). **Estimate BEFORE you run.**

### Token estimation quick check

```
Rough estimate: characters ÷ 4 ≈ tokens
412 feedback rows × ~50 chars each → ~5,150 tokens/batch
1M claim notes × ~200 chars each  → ~50M tokens → ~$3,750 at Pro pricing
```

---

## Embeddings: Meaning as Coordinates

```python
# What an embedding model does (concept, not today's code)
"refund took forever"        → [0.12, -0.83, 0.44, ...]   # 768+ dimensions
"still waiting on my money"  → [0.11, -0.79, 0.48, ...]   # CLOSE (similar meaning)
"driver was very friendly"   → [-0.67, 0.21, -0.05, ...]  # FAR (different meaning)
```

Distance ≈ similarity of **meaning**, not spelling. This is why "refund" and "reimbursement" cluster together even though they share no letters.

**DE use cases for this week and beyond:**
- Deduplicate claims beyond exact-match (Thursday)
- Cluster feedback into themes without labeling every row
- Semantic search: "find tickets similar to this complaint"
- RAG (Retrieval-Augmented Generation): embed docs → store → retrieve nearest → hand to LLM as context (capstone option)

Both BigQuery and Snowflake store and search vectors natively; Thursday's lab touches BigQuery's `VECTOR_SEARCH`.

---

## The 6 Prompt Levers

| Lever | Weak | Strong |
|-------|------|--------|
| **Role** | *(none)* | `"You are a data quality analyst reviewing rider feedback."` |
| **Specificity** | `"classify this"` | `"Assign exactly one label from: pricing \| driver \| app \| cleanliness \| other"` |
| **Format** | `"give me the answer"` | `"Respond as JSON: {\"label\": ..., \"confidence\": 0–1}"` |
| **Examples (few-shot)** | zero examples | 2–3 labeled examples before the task row |
| **Constraints** | *(none)* | `"If unsure, use 'other'. Never invent labels not in the list."` |
| **Data placement** | data before instructions | Instructions first, then the data, clearly delimited |

---

## Output Is Data: Validate It

LLMs optimize for **plausible**, not **true**. They invent zone names, statutes, and pandas methods with total confidence.

```yaml
# dbt test applied to LLM output columns
models:
  - name: classified_feedback
    columns:
      - name: ai_label
        tests:
          - not_null
          - accepted_values:
              values: [pricing, driver, app, cleanliness, other]
      - name: ai_confidence
        tests:
          - dbt_utils.accepted_range:
              min_value: 0
              max_value: 1
```

---

## Lab Deliverable Checklist

| Item | Done? |
|------|-------|
| Activity 0: Presented Databricks Mini-Project solution and participated in peer debrief | ☐ |
| Activity 1: Completed SQL to Pandas & Polars Drills ([Activity_1_Cross_Tool_SQL_to_Pandas_Drills.ipynb](file:///Users/tarekatwan/Repos/MyWork/Teach/repos/TechCatalyst_DE_2026/Week%206/Labs/Day%201/Activity_1_Cross_Tool_SQL_to_Pandas_Drills.ipynb)) | ☐ |
| Activity 2: Completed Window Functions in Pandas & Polars ([Activity_2_Window_Functions_in_Pandas.ipynb](file:///Users/tarekatwan/Repos/MyWork/Teach/repos/TechCatalyst_DE_2026/Week%206/Labs/Day%201/Activity_2_Window_Functions_in_Pandas.ipynb)) | ☐ |
| Code-Along: Snowpark Basics executed ([Code_Along_Snowpark_Basics.ipynb](file:///Users/tarekatwan/Repos/MyWork/Teach/repos/TechCatalyst_DE_2026/Week%206/Labs/Day%201/Code_Along_Snowpark_Basics.ipynb)) | ☐ |
| Activity 3: Completed Snowpark First Flight Activity ([Activity_3_Snowpark_First_Flight.ipynb](file:///Users/tarekatwan/Repos/MyWork/Teach/repos/TechCatalyst_DE_2026/Week%206/Labs/Day%201/Activity_3_Snowpark_First_Flight.ipynb)) | ☐ |
| Activity 4: Completed BigQuery ML Self-Study Walkthrough ([Activity_4_BigQueryML_SelfStudy.md](file:///Users/tarekatwan/Repos/MyWork/Teach/repos/TechCatalyst_DE_2026/Week%206/Labs/Day%201/Activity_4_BigQueryML_SelfStudy.md)) | ☐ |
| Activity 5: Task 1 (BQML): Trained `ARIMA_PLUS` on `air_passenger.csv` and generated 12-month forecast | ☐ |
| Activity 5: Task 2 (BQML): Trained `LINEAR_REG` on `mpg.csv`, evaluated $R^2$, and inspected `ML.WEIGHTS` | ☐ |
| Activity 5: Task 3 (BQML): Trained `LOGISTIC_REG` on `loans.csv`, evaluated ROC AUC, and inspected `ML.WEIGHTS` | ☐ |
| Activity 5: Task 4 (BQML): Trained `KMEANS` on `cereal.csv`, inspected centroids, and persisted results to table | ☐ |
| AI Studio open; Gemini 2.0 Flash selected; temperature 0.2 | ☐ |
| Challenge A: Extraction prompt built iteratively (+role, +format, +constraints, +examples) | ☐ |
| Challenge B: Baseline accuracy scored against `answer_key_20.csv` column C; re-scored after tuning | ☐ |
| Challenge C: Executive, technical, and one-liner summaries produced from 15-row text block | ☐ |
| `prompts.md` created with prompt iterations, B accuracy, and top lessons | ☐ |

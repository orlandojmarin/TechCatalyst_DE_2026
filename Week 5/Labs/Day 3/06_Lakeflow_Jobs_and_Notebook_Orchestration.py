# Databricks notebook source
# MAGIC %md
# MAGIC # 06: Lakeflow Jobs and Notebook Orchestration
# MAGIC
# MAGIC You have built a pipeline interactively. A production pipeline must also run in the right order, receive parameters, report useful evidence, and fail clearly when its contract is broken.
# MAGIC
# MAGIC This notebook explains the orchestration pieces first. The activity at the end asks you to build and operate a real Lakeflow Job in Databricks Free Edition.
# MAGIC
# MAGIC You will learn to:
# MAGIC
# MAGIC - distinguish `%run`, `dbutils.notebook.run`, and Lakeflow Job tasks;
# MAGIC - understand why job tasks need explicit data and parameter contracts;
# MAGIC - pass parameters into task notebooks with widgets;
# MAGIC - pass small runtime values between tasks with `dbutils.jobs.taskValues`;
# MAGIC - read the Jobs & Pipelines run page;
# MAGIC - create, fail, repair, and validate a four-task Wanderbricks workflow.
# MAGIC
# MAGIC **Dataset:** `samples.wanderbricks`  
# MAGIC **Files used:** the five notebooks in `tasks/`  
# MAGIC **Setup helper needed:** no, each task owns its configuration

# COMMAND ----------

# MAGIC %md
# MAGIC ## How this notebook works
# MAGIC
# MAGIC Most of this lab moves between this companion notebook and the **Jobs & Pipelines** UI. Use this map so you always know what to run and where to go next.
# MAGIC
# MAGIC | Order | Item | Who runs it | When |
# MAGIC |---:|---|---|---|
# MAGIC | 1 | This notebook | You, interactively | Run the guided example in Part 5 |
# MAGIC | 2 | The five files in `tasks/` | Nobody yet | Import and read them in Part 6 |
# MAGIC | 3 | `Task_1_Build_Bronze` through `Task_4_Validate_Gold` | The Lakeflow Job | After you build the four-task DAG in Part 8 |
# MAGIC | 4 | The Jobs & Pipelines run page | You inspect it | After the green run, the failed run, and the repair run |
# MAGIC | 5 | This notebook | You, interactively | Return for the SQL validation in Part 8, Task 5 |
# MAGIC
# MAGIC `_shared_config` is not a separate job task. Each task notebook loads it with `%run`.
# MAGIC
# MAGIC **Important:** Do not run the four task notebooks interactively as the lab. Open them to read the code, then let the job run them in dependency order.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 1: Why split a pipeline into tasks?
# MAGIC
# MAGIC One giant notebook can run from top to bottom, but it hides operational boundaries.
# MAGIC
# MAGIC Our workflow has four contracts:
# MAGIC
# MAGIC ```text
# MAGIC build_bronze -> build_silver -> build_gold -> validate_gold
# MAGIC ```
# MAGIC
# MAGIC | Task | Reads | Writes or proves |
# MAGIC |---|---|---|
# MAGIC | `build_bronze` | Wanderbricks bookings and payments | governed bronze Delta tables |
# MAGIC | `build_silver` | bronze plus property and user dimensions | one trusted row per booking |
# MAGIC | `build_gold` | trusted booking facts | one daily revenue row per check-in date |
# MAGIC | `validate_gold` | gold plus upstream metrics | clear pass or failure |
# MAGIC
# MAGIC Separate tasks provide visible dependencies, task-level retries, isolated failures, and easier debugging.
# MAGIC
# MAGIC Notebook 05 built the medallion transformations primarily in SQL. The provided job tasks rebuild the same layer contracts with PySpark because the tasks also use Python widgets, assertions, and `dbutils.jobs.taskValues`. Lakeflow Jobs can orchestrate SQL tasks too. We are choosing PySpark here because the operational control logic benefits from Python, not because SQL stopped being valid.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 2: Choose the correct notebook mechanism
# MAGIC
# MAGIC These tools sound similar but solve different problems.
# MAGIC
# MAGIC | Mechanism | Same session? | Main use |
# MAGIC |---|---:|---|
# MAGIC | `%run ./helper` | yes | load small shared definitions into the current notebook session |
# MAGIC | `dbutils.notebook.run(path, timeout, arguments)` | no, child run | call one notebook directly and receive one string result |
# MAGIC | Lakeflow Job task | separate task session | scheduled, observable workflows with dependencies, retries, and task state |
# MAGIC
# MAGIC **Decision rule:** Use `%run` for a genuine shared helper. Use job tasks for pipeline stages that deserve independent status and recovery.
# MAGIC
# MAGIC That is why every provided task uses `%run ./_shared_config`, but the pipeline stages themselves are separate job tasks.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 3: Parameters enter through widgets
# MAGIC
# MAGIC Open `tasks/_shared_config` in another Databricks tab while reading this section.
# MAGIC
# MAGIC The helper creates three widgets:
# MAGIC
# MAGIC - `target_catalog`: where job tables are written;
# MAGIC - `target_schema`: your personal schema;
# MAGIC - `batch_id`: a label added to bronze rows.
# MAGIC
# MAGIC A widget always returns text. The helper validates identifiers before using them in table names.
# MAGIC
# MAGIC Current Lakeflow Jobs behavior automatically pushes job parameters down to notebook tasks, which accept key-value parameters. The task receives the job value instead of the notebook default.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Parameter flow
# MAGIC
# MAGIC ```text
# MAGIC Job parameter target_schema
# MAGIC            |
# MAGIC            v  automatic pushdown to notebook task
# MAGIC dbutils.widgets.get("target_schema")
# MAGIC            |
# MAGIC            v
# MAGIC workspace.<your_schema>.job_bronze_wander_bookings
# MAGIC ```
# MAGIC
# MAGIC This makes the notebook reusable. The code stays the same while the target schema changes by environment or learner.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 4: Runtime values move through `taskValues`
# MAGIC
# MAGIC Parameters are configuration known before the run. Task values are small results discovered during the run.
# MAGIC
# MAGIC The provided tasks use this pattern:
# MAGIC
# MAGIC ```python
# MAGIC # Upstream task
# MAGIC dbutils.jobs.taskValues.set(key="booking_rows", value=booking_rows)
# MAGIC
# MAGIC # Downstream task
# MAGIC booking_rows = dbutils.jobs.taskValues.get(
# MAGIC     taskKey="build_bronze",
# MAGIC     key="booking_rows",
# MAGIC     debugValue=0,
# MAGIC )
# MAGIC ```
# MAGIC
# MAGIC Use task values for small control or validation values, not for a DataFrame. Tables and files carry the actual datasets between tasks.
# MAGIC
# MAGIC We omit a silent `default`. If the task key or value key is wrong during a job run, the task should fail with a useful error. `debugValue` is only the value returned when you study the notebook interactively outside a job.
# MAGIC
# MAGIC Databricks also supports dynamic task-value references such as `{{tasks.build_bronze.values.booking_rows}}` in downstream task parameters. Those references reduce code coupling when many tasks consume the same value. This lab uses `get` so you can see and understand the `dbutils` mechanism directly.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 5: Guided example, observe the task boundary
# MAGIC
# MAGIC Before building a job, run a small example interactively.
# MAGIC
# MAGIC **Goal:** Observe the difference between a notebook input and an upstream task value.
# MAGIC
# MAGIC **Predict:** This notebook is not currently running as a job task. What should `taskValues.get` return when a `debugValue` is supplied?

# COMMAND ----------

dbutils.widgets.text("demo_batch_id", "interactive_01", "Demo batch ID")
demo_batch_id = dbutils.widgets.get("demo_batch_id")

demo_upstream_rows = dbutils.jobs.taskValues.get(
    taskKey="build_bronze",
    key="booking_rows",
    debugValue=-1,
)

print(f"Widget input available now: demo_batch_id={demo_batch_id}")
print(f"Upstream task value outside a job: {demo_upstream_rows}")

# COMMAND ----------

# MAGIC %md
# MAGIC **Look for:** The widget returns `interactive_01`. The task-value lookup returns `-1` because there is no job run and no upstream `build_bronze` task in this interactive session.
# MAGIC
# MAGIC **Why it matters:** A widget is an input to the current notebook. A task value belongs to a particular upstream task in a particular job run. The debug value makes the provided task notebooks inspectable outside the job without pretending that an upstream result exists.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 6: Read the provided task notebooks before building the job
# MAGIC
# MAGIC Import these five files into one Databricks Workspace folder:
# MAGIC
# MAGIC 1. `tasks/_shared_config.py`
# MAGIC 2. `tasks/Task_1_Build_Bronze.py`
# MAGIC 3. `tasks/Task_2_Build_Silver.py`
# MAGIC 4. `tasks/Task_3_Build_Gold.py`
# MAGIC 5. `tasks/Task_4_Validate_Gold.py`
# MAGIC
# MAGIC Read them in order. For each file, identify:
# MAGIC
# MAGIC - its input table or dataset;
# MAGIC - its output table or assertion;
# MAGIC - the widget parameters it receives;
# MAGIC - the task values it sets or gets;
# MAGIC - the condition that would make it fail.
# MAGIC
# MAGIC **Do not run Task 1, 2, 3, or 4 interactively as the lab.** Open them only to inspect the code. The job will run them in dependency order, with the correct parameters and upstream task values.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 7: Preview the run evidence you will collect
# MAGIC
# MAGIC You have not created or run the job yet. Part 8 will guide you through three run states. Do not try to inspect them now.
# MAGIC
# MAGIC | Run state | Evidence available on the run page |
# MAGIC |---|---|
# MAGIC | First green run | DAG arrows, task status and duration, resolved parameters, and notebook output |
# MAGIC | Intentional failed run | Green upstream tasks, failed validation task, exact assertion message, and **Repair run** option |
# MAGIC | Repaired run | Successful validation plus evidence that successful upstream tasks were not rebuilt |
# MAGIC
# MAGIC A green job is evidence that the configured run completed. It is not proof that the business result is correct. That is why `validate_gold` contains explicit reconciliation and quality checks.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part 8: Your activity, build the Wanderbricks workflow
# MAGIC
# MAGIC ### Scenario
# MAGIC
# MAGIC Finance needs the Wanderbricks daily revenue product rebuilt as an observable workflow. You will create a four-task job, run it successfully, cause a controlled validation failure, and repair only the failed portion.
# MAGIC
# MAGIC ### Success evidence
# MAGIC
# MAGIC Capture these items for your lab submission:
# MAGIC
# MAGIC - screenshot of the four-task DAG with a successful run;
# MAGIC - screenshot or copied output from `validate_gold`;
# MAGIC - screenshot of the intentional failure message;
# MAGIC - screenshot of the repaired run;
# MAGIC - query output proving the gold table exists in your schema;
# MAGIC - a short explanation of parameters, task values, and repair runs.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 1: Create the job
# MAGIC
# MAGIC 1. Open **Jobs & Pipelines** from the left navigation.
# MAGIC 2. Select **Create**, then create a job.
# MAGIC 3. Name it `w5_wanderbricks_<yourname>`.
# MAGIC 4. Use serverless compute, the Free Edition default.
# MAGIC
# MAGIC Add these job parameters:
# MAGIC
# MAGIC | Key | Value |
# MAGIC |---|---|
# MAGIC | `target_catalog` | `workspace` |
# MAGIC | `target_schema` | your Week 5 schema, such as `w5_maria` |
# MAGIC | `batch_id` | `manual_01` |

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 2: Add the bronze task
# MAGIC
# MAGIC Create a notebook task with:
# MAGIC
# MAGIC | Setting | Value |
# MAGIC |---|---|
# MAGIC | Task name | `build_bronze` |
# MAGIC | Notebook | `Task_1_Build_Bronze` |
# MAGIC | Depends on | none |
# MAGIC
# MAGIC Leave the bronze task's parameter section empty. The three job-level parameters are automatically pushed to notebook tasks, so do not duplicate them here. You will confirm the resolved values after the first run.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 3: Add silver, gold, and validation
# MAGIC
# MAGIC Create the remaining notebook tasks:
# MAGIC
# MAGIC | Task name | Notebook | Depends on |
# MAGIC |---|---|---|
# MAGIC | `build_silver` | `Task_2_Build_Silver` | `build_bronze` |
# MAGIC | `build_gold` | `Task_3_Build_Gold` | `build_silver` |
# MAGIC | `validate_gold` | `Task_4_Validate_Gold` | `build_gold` |
# MAGIC
# MAGIC The three job parameters are automatically pushed to every notebook task. Add one task-specific parameter to `validate_gold`:
# MAGIC
# MAGIC | Key | Value |
# MAGIC |---|---|
# MAGIC | `minimum_dates` | `1` |
# MAGIC
# MAGIC **Check before running:** The DAG must be a single chain with four tasks. A missing dependency can make a consumer run before its table exists.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 4: Run it green
# MAGIC
# MAGIC 1. Select **Run now**.
# MAGIC 2. Open the run page.
# MAGIC 3. Watch task states move through the dependency chain.
# MAGIC
# MAGIC When the job completes:
# MAGIC
# MAGIC 1. Confirm the DAG is one four-task chain with the correct dependency arrows.
# MAGIC 2. Confirm all four tasks are green and review each task's duration.
# MAGIC 3. Open each task's run details and review its resolved parameters.
# MAGIC 4. Open each task's notebook output.
# MAGIC 5. Confirm the output prints your target schema and batch ID. If the run page collapses the parameter details, this output is your fallback evidence that pushdown worked.
# MAGIC 6. Record the bronze booking and payment counts.
# MAGIC 7. Record the silver booking count and revenue.
# MAGIC 8. Confirm gold reports the same totals.
# MAGIC 9. Save a screenshot of the successful DAG.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 5: Validate the published tables with SQL
# MAGIC
# MAGIC Return to this notebook. If needed, run the following cell to point at your schema.

# COMMAND ----------

dbutils.widgets.text("validation_schema", "w5_yourname", "Schema used by the job")
VALIDATION_SCHEMA = dbutils.widgets.get("validation_schema").strip().lower()
print(f"Validating workspace.{VALIDATION_SCHEMA}")

# COMMAND ----------

gold_table = f"workspace.{VALIDATION_SCHEMA}.job_gold_wander_daily_revenue"
silver_table = f"workspace.{VALIDATION_SCHEMA}.job_silver_wander_booking_facts"

assert spark.catalog.tableExists(silver_table), f"Missing {silver_table}"
assert spark.catalog.tableExists(gold_table), f"Missing {gold_table}"

silver_rows = spark.table(silver_table).count()
gold_booking_rows = spark.table(gold_table).agg({"booking_count": "sum"}).first()[0]

assert silver_rows == gold_booking_rows, "Gold booking counts do not reconcile to silver."
display(spark.table(gold_table).orderBy("check_in_date"))
print("Published table validation passed.")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 6: Cause a controlled failure
# MAGIC
# MAGIC 1. Edit only the `validate_gold` task.
# MAGIC 2. Change its `minimum_dates` parameter from `1` to `9999`.
# MAGIC 3. Save the task.
# MAGIC
# MAGIC **Predict before running:** Which tasks should complete successfully? Which task should fail?
# MAGIC
# MAGIC 4. Run the complete job again.
# MAGIC 5. Open the failed run page.
# MAGIC 6. Confirm `build_bronze`, `build_silver`, and `build_gold` are green.
# MAGIC 7. Confirm only `validate_gold` is red.
# MAGIC 8. Open `validate_gold` and copy the assertion message that states how many dates were found.
# MAGIC 9. Confirm the resolved `minimum_dates` value for this task run was `9999`.
# MAGIC 10. Locate the **Repair run** option, but do not start the repair until you correct the parameter in Task 7.
# MAGIC
# MAGIC This failure is intentional. It proves that a quality gate can stop a pipeline from being treated as successful.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 7: Repair the run
# MAGIC
# MAGIC 1. Edit the `validate_gold` task, change `minimum_dates` back to `1`, and save the task.
# MAGIC 2. Return to the same failed run page from Task 6.
# MAGIC 3. Choose **Repair run**.
# MAGIC 4. In the repair dialog, confirm that `validate_gold` is the unsuccessful task to rerun.
# MAGIC 5. Start the repair.
# MAGIC 6. Confirm `validate_gold` now succeeds with `minimum_dates=1`.
# MAGIC 7. Confirm the three successful upstream build tasks were preserved rather than run again.
# MAGIC 8. Save a screenshot of the repaired green run.
# MAGIC
# MAGIC The repair uses the current task settings, which is why you corrected `minimum_dates` before starting it.
# MAGIC
# MAGIC **Why repair matters:** In a long workflow, repeating expensive successful tasks wastes time and compute. Repair runs preserve useful completed work while retrying the failed path.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Task 8: Explain the contracts
# MAGIC
# MAGIC Add a Markdown cell below and answer:
# MAGIC
# MAGIC 1. What information entered each task as a widget parameter?
# MAGIC 2. What information moved between tasks as a task value?
# MAGIC 3. What data moved between tasks through Delta tables?
# MAGIC 4. Why was `%run` suitable for `_shared_config` but not a replacement for the four job tasks?
# MAGIC 5. What did the repair run avoid repeating?

# COMMAND ----------

# MAGIC %md
# MAGIC **Write your answers here.**

# COMMAND ----------

# MAGIC %md
# MAGIC ## Final checklist
# MAGIC
# MAGIC - [ ] Four imported task notebooks plus `_shared_config` are in one Workspace folder.
# MAGIC - [ ] Job parameters use your personal schema.
# MAGIC - [ ] The DAG is bronze to silver to gold to validation.
# MAGIC - [ ] The first run is green.
# MAGIC - [ ] The Delta tables exist and reconcile.
# MAGIC - [ ] `minimum_dates=9999` creates a clear validation failure.
# MAGIC - [ ] A repair run succeeds after the parameter is corrected.
# MAGIC - [ ] Your explanation distinguishes parameters, task values, tables, and `%run`.
# MAGIC
# MAGIC When every item is checked, your Week 5 Databricks sequence is complete.

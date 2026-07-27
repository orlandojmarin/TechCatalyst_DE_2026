# Activity 0: dbt Core Setup

**Module:** Week 5 Day 4  
**Estimated Time:** 50 to 60 minutes  
**Difficulty:** Beginner  
**Format:** Individual, self-paced  
**Prerequisites:** VS Code, a Linux terminal, and your Snowflake credentials from Week 4

## Objective

Install dbt Core with the Snowflake adapter, create a dbt project, connect it to Snowflake, and prove that the connection works. Your project will read shared raw data from `AIRBNB.RAW` and create only your objects in `TECHCATALYST.<STUDENTNAME>`.

## Start with the mental model

dbt is a transformation tool. It does not replace ingestion, Snowflake, or SQL.

You write SQL `SELECT` statements and describe how they depend on one another. dbt then:

1. compiles your templates into Snowflake SQL,
2. creates views or tables from that SQL,
3. runs models in dependency order,
4. tests assumptions about the results, and
5. generates documentation and lineage from the same project files.

The important separation for this lab is:

| Layer | Location | Your access |
|---|---|---|
| Raw input | `AIRBNB.RAW` | Read shared tables |
| Your development output | `TECHCATALYST.<STUDENTNAME>` | Create and replace your own objects |
| dbt code | `student-work/week5/day4/airbnb` | Edit and commit your project |
| Snowflake credentials | `~/.dbt/profiles.yml` | Keep outside the repository |

## Why dbt Core today, and where Fusion fits

You may see two local dbt engines in current documentation:

- **dbt Core v1** is the established Python-based open-source engine and adapter ecosystem used in this lab.
- **dbt Fusion** is a newer engine written in Rust. It understands multiple SQL dialects directly and is designed for faster parsing, compilation, execution, early SQL error detection, autocomplete, inline errors, and richer code navigation.

The official installation page still labels the **Fusion CLI** as Preview as of July 27, 2026. For a classroom where everyone must follow the same tested path, we will use dbt Core v1.12 with `dbt-snowflake`. This avoids mixing preview CLI behavior with Core commands.

The engine choice does not change the concepts you learn today. Fusion uses the same dbt language and project structure: models, `ref()`, `source()`, Jinja, tests, snapshots, materializations, documentation, and the DAG all transfer. See the official [Fusion overview](https://docs.getdbt.com/docs/fusion/about-fusion) and [dbt installation paths](https://docs.getdbt.com/docs/local/install-dbt).

## Task 1: Install dbt Core in the course environment

Start at the repository root. The repository already has one UV project and one `.venv`, so do not run `uv init` and do not create another virtual environment inside `student-work/`.

```bash
source .venv/bin/activate
uv pip install dbt-snowflake
dbt --version
```

`dbt-snowflake` installs dbt Core plus the adapter that translates dbt operations into Snowflake-specific SQL. Your version output should contain a Core version and a Snowflake plugin version.

This lab uses `uv pip install` because dbt is a classroom tool for this activity rather than a runtime dependency of the course's Python exercises. The package still goes into the existing root `.venv`. If that environment is recreated later, run this install command again.

If you later see `VIRTUAL_ENV does not match the project environment`, run:

```bash
deactivate
cd <REPOSITORY_ROOT>
source .venv/bin/activate
```

## Task 2: Create your dbt project

From the repository root:

```bash
mkdir -p student-work/week5/day4
cd student-work/week5/day4
dbt init --skip-profile-setup airbnb
cd airbnb
rm -r models/example
```

The project belongs under `student-work/` so a future `git pull` cannot overwrite it.

Before continuing, inspect the scaffold:

| Path | What belongs there |
|---|---|
| `dbt_project.yml` | Project-wide paths and defaults |
| `models/` | SQL models and their YAML properties |
| `seeds/` | Small CSV reference data |
| `snapshots/` | Rules for retaining row history |
| `tests/` | SQL queries that return invalid rows |
| `macros/` | Reusable Jinja logic |
| `target/` | Generated SQL, logs, and metadata |

The project code and the profile have different jobs. `dbt_project.yml` is safe to commit. `profiles.yml` contains connection details and stays outside the repository.

## Task 3: Configure the Snowflake connection

Create the dbt profile directory and open the profile:

```bash
mkdir -p ~/.dbt
code ~/.dbt/profiles.yml
```

Add this profile, replacing every placeholder:

```yaml
airbnb:
  target: dev
  outputs:
    dev:
      type: snowflake
      account: <ACCOUNT_PROVIDED_BY_INSTRUCTOR>
      user: <STUDENTNAME>
      password: <YOUR_PASSWORD>
      authenticator: username_password_mfa
      role: DE
      warehouse: COMPUTE_WH
      database: TECHCATALYST
      schema: <STUDENTNAME>
      threads: 4
```

The profile's default database and schema control where dbt creates your models. They do not control the raw input location. Activity 3 will declare `AIRBNB.RAW` explicitly as a source.

`username_password_mfa` tells the Snowflake Python connector to use username and password authentication with MFA token caching when the account permits it. Approve only a Duo push that you triggered. Never place your password in a model, worksheet, screenshot, or committed file.

## Task 4: Add a safe object-name prefix

Your schema is already separated by student name. We will also prefix every object name so ownership is obvious in logs and screenshots.

Create `macros/generate_alias_name.sql`:

```sql
{% macro generate_alias_name(custom_alias_name=none, node=none) -%}
    {%- if custom_alias_name -%}
        {{ target.user | lower }}_{{ custom_alias_name | trim }}
    {%- else -%}
        {{ target.user | lower }}_{{ node.name }}
    {%- endif -%}
{%- endmacro %}
```

### Jinja before dbt: a general-purpose template engine

Jinja is not a dbt product and it is not a SQL dialect. It is a general-purpose **text templating engine** from the Pallets Python project. A template contains ordinary text plus placeholders or instructions. A program supplies values, Jinja renders the template, and the result is a finished text document.

For example, this template:

```jinja
Welcome, {{ learner_name }}!
```

could be rendered with `learner_name = "Sam"` to produce:

```text
Welcome, Sam!
```

The output does not have to be HTML or SQL. Jinja can generate any text format. Different tools provide Jinja with different values and functions:

| Tool or context | What Jinja commonly helps generate |
|---|---|
| Flask web applications | HTML pages containing application data |
| Ansible automation | Configuration files and tasks containing environment-specific values |
| dbt projects | SQL adapted to model dependencies, environments, and reusable project rules |

The common problem is repetition mixed with variation. A team wants one understandable template, but a few names, values, columns, or sections must change based on context. Jinja supplies those changing parts before the final text is used.

Read more in the official [Jinja introduction](https://jinja.palletsprojects.com/en/stable/intro/), [Flask templating guide](https://flask.palletsprojects.com/en/stable/templating/), and [Ansible templating guide](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_templating.html).

### Why dbt adopted Jinja

SQL is excellent at describing a data transformation, but a maintainable data project needs more than a fixed query. dbt must also:

- resolve a logical model name to the correct database, schema, and alias for the current environment;
- understand which models depend on other models;
- include or omit SQL for different run conditions;
- reuse carefully chosen SQL patterns instead of copying them into many files;
- read project variables and target information during compilation.

Jinja gives dbt a templating layer for those jobs. dbt adds its own context, including functions such as `ref()`, `source()`, `config()`, and `is_incremental()`.

The order matters:

```text
model.sql containing SQL + Jinja
        |
        v
dbt renders Jinja and compiles the model
        |
        v
plain SQL for the selected warehouse
        |
        v
Snowflake executes the SQL
```

Snowflake never executes Jinja. By the time Snowflake receives the statement, the curly-brace instructions have been replaced or removed. This is why inspecting `target/compiled/` is so useful: it shows the boundary between dbt's templating work and Snowflake's SQL work.

### Recognizing Jinja syntax

| Syntax | Meaning | dbt-shaped example |
|---|---|---|
| `{{ ... }}` | Evaluate an expression and insert text into the compiled result | `{{ ref('src_listings') }}` |
| `{% ... %}` | Run an instruction such as `if`, `for`, `set`, or `macro` | `{% if is_incremental() %}` |
| `{# ... #}` | Add a Jinja comment that will not appear in compiled SQL | `{# compile-time note #}` |
| `value \| lower` | Pass a value through a filter that transforms it | `target.user \| lower` |

Jinja syntax is Python-like, but a dbt model is not a Python script. Its final rendered output still must be valid SQL.

### Four dbt examples you will meet

**1. Resolve another model with `ref()`**

```sql
SELECT *
FROM {{ ref('src_listings') }}
```

For a student named `JDOE`, the compiled relation will be similar to:

```sql
SELECT *
FROM TECHCATALYST.JDOE.JDOE_SRC_LISTINGS
```

`ref()` also records a dependency in dbt's lineage graph. This is safer than hardcoding a physical relation because dbt can adapt the name for another target and build models in dependency order.

**2. Resolve declared raw data with `source()`**

```sql
SELECT *
FROM {{ source('airbnb', 'listings') }}
```

After Activity 3 declares the source in YAML, dbt will compile this to the configured `AIRBNB.RAW.RAW_LISTINGS` relation. `source()` makes the raw dependency visible and testable.

**3. Change SQL only during an incremental run**

```sql
{% if is_incremental() %}
WHERE review_date > (
    SELECT MAX(review_date) FROM {{ this }}
)
{% endif %}
```

On the first full build, `is_incremental()` is false, so dbt omits the entire `WHERE` block. On a later incremental run, it is true, so dbt includes the filter. `{{ this }}` becomes the current model's physical relation.

**4. Reuse logic through a macro**

The `generate_alias_name` block you just created is a macro, which is similar to a reusable function for text generation:

- `target.user` is a dbt-provided value for the active Snowflake user.
- `| lower` and `| trim` are Jinja filters.
- `{% if custom_alias_name %}` chooses one of two naming paths.
- `{{ ... }}` writes the chosen name into dbt's generated SQL.

The macro overrides dbt's alias-generation hook. If your Snowflake user is `JDOE`, a model named `src_listings` becomes `JDOE_SRC_LISTINGS` in Snowflake. Later, `ref('src_listings')` still uses the logical model name because dbt tracks the physical alias for you.

Jinja is powerful, but more templating is not automatically better. Use it when it removes meaningful repetition or lets dbt understand project context. Prefer explicit SQL when a loop or macro would make the model harder to read. The official [dbt Jinja and macros guide](https://docs.getdbt.com/docs/build/jinja-macros) recommends favoring readability.

## Task 5: Configure materialization defaults

In `dbt_project.yml`, replace the generated `models:` section with:

```yaml
models:
  airbnb:
    +materialized: view
    src:
      +materialized: view
    dim:
      +materialized: table
    fct:
      +materialized: incremental
    mart:
      +materialized: table
```

A materialization is dbt's answer to, "What should this model's `SELECT` become in the warehouse?"

### Read the YAML as a hierarchy

The keys under `models:` match folders under `models/`:

```text
models/
├── src/
├── dim/
├── fct/
└── mart/
```

The configuration reads from broadest to most specific:

| YAML path | Models affected | Materialization |
|---|---|---|
| `models.airbnb` | Every model in this project unless overridden | `view` |
| `models.airbnb.src` | Models under `models/src/` | `view` |
| `models.airbnb.dim` | Models under `models/dim/` | `table` |
| `models.airbnb.fct` | Models under `models/fct/` | `incremental` |
| `models.airbnb.mart` | Models under `models/mart/` | `table` |

`airbnb` is the project name, not a database or folder. `src`, `dim`, `fct`, and `mart` are resource paths. The leading `+` marks `materialized` as a configuration that applies to models beneath that path.

A model can override its folder when there is a clear reason:

```sql
{{ config(materialized='view') }}
```

The closest configuration wins. An in-model config overrides the folder, and the folder overrides the project default.

### Five built-in materialization types

dbt defines five built-in materialization concepts. Adapter support varies by warehouse.

| Type | What dbt creates | Best fit | Main trade-off |
|---|---|---|---|
| `view` | A SQL view with query logic but no stored result rows | Thin renaming and casting layers | Fresh data, but complex view stacks can be slow to query |
| `table` | A table rebuilt from the full `SELECT` on each run | Reused transformations and BI-facing outputs | Fast reads, but full rebuilds take time |
| `incremental` | A table built fully once, then updated from a filtered result set | Large, growing event or fact data | Faster later runs, but late data and updates need explicit rules |
| `ephemeral` | No warehouse object; dbt injects the model SQL as a CTE into downstream models | Small intermediate logic used by one or two models | Fewer warehouse objects, but harder debugging if overused |
| `materialized_view` | A warehouse-managed persisted view that refreshes data | Platforms that support this dbt materialization | Behavior and options depend on the adapter |

Snowflake is an important exception to the last row. `dbt-snowflake` does not support dbt's generic `materialized_view` materialization. It provides the Snowflake-specific `dynamic_table` materialization instead, with settings such as `target_lag` and `snowflake_warehouse`. Dynamic tables are outside today's lab.

Read more in the official [dbt materializations reference](https://docs.getdbt.com/docs/build/materializations) and [Snowflake configurations](https://docs.getdbt.com/reference/resource-configs/snowflake-configs).

### Why this project uses view, table, incremental, table

| Folder | Choice | Reason |
|---|---|---|
| `src` | `view` | The models stay thin and expose the latest raw rows without storing another full copy |
| `dim` | `table` | Dimensions are reused and queried often, so stored results simplify and speed downstream reads |
| `fct` | `incremental` | Review events grow over time, so later runs should process only the selected new rows |
| `mart` | `table` | Reporting outputs should be fast and predictable for analysts or BI tools |

This resembles a medallion architecture, but the mapping is not one-to-one:

- `AIRBNB.RAW` is the bronze-like ingested layer.
- `src` is the thin staging boundary that standardizes raw names.
- `dim` and `fct` are the cleansed, reusable core, similar to silver.
- `mart` is the analysis-ready output, similar to gold.

### Incremental options you will meet

An incremental materialization still needs model-specific rules. These options do not appear automatically just because the folder says `incremental`.

| Option | Purpose |
|---|---|
| `unique_key` | Identifies a logical row so strategies such as `merge` can update matching records |
| `incremental_strategy` | Chooses how Snowflake applies the selected rows; supported strategies include `merge`, `append`, `delete+insert`, `insert_overwrite`, and `microbatch` |
| `is_incremental()` | Jinja condition that is true only during a normal incremental run against an existing target |
| `--full-refresh` | Rebuilds the complete target instead of using the incremental branch |

Snowflake's default incremental strategy is `merge`, but `merge` needs a valid `unique_key` to match rows. The Activity 2 fact model does not define a `unique_key`; it filters by a date watermark and appends the returned new rows. That simple pattern makes the mechanism visible before introducing update and deduplication policies.

## Task 6: Prove the setup

From `student-work/week5/day4/airbnb`:

```bash
dbt debug
dbt parse
```

`dbt debug` checks the project, profile, dependencies, and Snowflake connection. `dbt parse` reads the project and Jinja without building warehouse objects.

**Expected result:** `dbt debug` reports that all checks passed, and `dbt parse` completes without an error.

## Explain it back

Before moving on, answer these in your own words:

1. Why are dbt Core and `dbt-snowflake` both installed?
2. Why is `profiles.yml` outside the repository?
3. Which setting chooses the output database and schema?
4. What will the alias macro change, and what will it not change?
5. What happens to Jinja before Snowflake receives a model's SQL?
6. Why is `ref('src_listings')` more useful than a hardcoded physical table name?
7. Why does this project use views for `src` models but incremental tables for `fct` models?

## Success Criteria

- `dbt --version` reports dbt Core and the Snowflake adapter.
- The project exists at `student-work/week5/day4/airbnb`.
- No second UV project or `.venv` exists inside `student-work/`.
- `~/.dbt/profiles.yml` points to `TECHCATALYST.<STUDENTNAME>`.
- `dbt debug` and `dbt parse` both pass.
- You can distinguish the dbt project from the connection profile.
- You can explain Jinja's compile-time role and recognize expressions, statements, comments, and filters.
- You can explain what each folder's materialization creates and why the choices differ.

## Troubleshooting

- `dbt: command not found`: return to the repository root and run `source .venv/bin/activate`.
- `Could not find profile named 'airbnb'`: confirm the top-level profile key and the `profile:` value in `dbt_project.yml` are both `airbnb`.
- Account connection error: use the account identifier provided by the instructor, not the full Snowsight URL.
- Schema error: replace `<STUDENTNAME>` in the profile with your actual Snowflake username.
- Repeated or unexpected Duo prompts: deny prompts you did not trigger and ask the instructor to verify the account's MFA caching configuration.
- `Object does not exist` for `AIRBNB`: do not change roles on your own. Ask the instructor to verify that role `DE` can read `AIRBNB.RAW`.

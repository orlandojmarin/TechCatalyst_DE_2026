# Activity 0: DBeaver And SQLite Setup

**Module:** Week 4 Day 1
**Estimated Time:** 30 to 40 minutes
**Difficulty:** Beginner
**Format:** Individual setup with instructor checkpoints
**Prerequisites:** Course repo open in VS Code and Chrome available

## Objective

In this activity, you will open a local SQLite database in DBeaver Community, inspect its tables, and run your first local SQL query.

## Why We Start Local

BigQuery is powerful, but it adds cloud login, public datasets, and query cost estimates. SQLite lets us practice the same SQL thinking on small local files first. Today you will use DBeaver as a visual SQL workbench, then transfer the same habits to BigQuery.

## Currentness Check

Checked on 2026-07-08:

| Topic | Source | Content decision |
|---|---|---|
| DBeaver Community download | https://dbeaver.io/download/ | Use DBeaver Community as the free desktop SQL client. |
| SQLite connection in DBeaver | https://dbeaver.com/docs/dbeaver/Database-driver-SQLite/ | Connect by choosing the local SQLite database file path. |

## Provided Databases

| File | Story | Main tables |
|---|---|---|
| `data/bron.db` | Basketball game log analysis | `king_james` |
| `data/call_center_database2.db` | Call center performance analysis | `agent`, `call`, `customer` |
| `data/crime_database.db` | Detective investigation | `crime_scene`, `individual`, `drivers`, `interrogation`, `gym_affiliated`, `gym_record`, `facebook_event` |

## Setup Steps

1. Install DBeaver Community from https://dbeaver.io/download/ if it is not already installed.
2. Open DBeaver.
3. Select **New Database Connection**.
4. Choose **SQLite**.
5. For the database path, choose this file from the course repo:

```text
Week 4/Labs/Day 1/data/bron.db
```

6. If DBeaver asks to download the SQLite driver, allow it.
7. Click **Test Connection**.
8. Click **Finish**.
9. In the Database Navigator, expand the connection and find the `king_james` table.
10. Open a SQL editor for this connection.

## First Query

Run this query:

```sql
SELECT
  G,
  Date,
  Opp,
  HomeAway,
  PTS
FROM king_james
LIMIT 10;
```

## Checkpoint

Show the instructor or a partner:

- Your DBeaver connection to `bron.db`.
- The `king_james` table in the navigator.
- A query result grid with 10 rows.

## Copy Then Complete

For written answers, work in your own student folder:

```bash
mkdir -p student-work/week4/day1
cd student-work/week4/day1
```

Create these files as you work:

```text
w4d1_sqlite_drills.sql
```

If you attempt the optional BigQuery homework tonight, you will also create `homework_bigquery_drills.sql` in the same folder.

Do not edit the provided files in `Week 4/Labs/Day 1/` directly.

## Success Criteria

- DBeaver opens a local SQLite database.
- You can find a table and preview its columns.
- You can run a `SELECT` query in DBeaver.
- You know where to save your own SQL answers.
- You do not use AI assistants to write SQL. Weeks 1 to 4 are still an AI-Free Zone.

## Instructor Notes

- Some students may double-click the `.db` file from Finder or the file browser. Redirect them to DBeaver's database connection flow.
- If the driver download fails, use the instructor machine for the first demo while students continue with BigQuery later.
- Keep the setup focused. The first win is a successful query result grid.

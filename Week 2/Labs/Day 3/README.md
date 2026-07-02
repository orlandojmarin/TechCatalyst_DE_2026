# Week 2 Day 3: APIs, Async, SDKs, and a First Look at DataFrames

**Module:** Intermediate Python, APIs, and an early bridge into pandas/Polars
**Estimated time:** flexible; see `## How the day fits together` below
**Format:** Individual build, pair review
**Environment:** Linux terminal, VS Code, Chrome, GitHub, UV
**Difficulty:** Intermediate

## How the day fits together

Day 3 has three parts. The instructor sets the actual pacing (this can run
long, spill into homework, or extend into Day 4; do not treat the time
estimates below as fixed):

1. **Guided notebooks** (Activity 1, then Activity 2): concept-first, richly
   explained, with worked examples and a few "your turn" sections. This is
   where new ideas get introduced.
2. **Independent build** (`Bonus_Lab_Weather_API_Explorer.ipynb`): the same
   category of skills (fetch, handle failures, retry, summarize, ship a CLI),
   built up from a blank file with much less scaffolding, ending in a runnable
   `weather_explorer.py`. This is where you prove you actually learned it, not
   just followed along. The Bonus Lab walks the build in progressive
   iterations; the finished `weather_explorer.py` is the deliverable.
3. **DataFrame Fundamentals** (Activity 3): a first look at pandas and Polars,
   using the real data you collected in Activity 1, bridging into Day 4's
   deeper pandas/Polars/cloud-shipping work.

## Lab Index

### Provided files

| File | Purpose |
|---|---|
| `README.md` | This guide and the day's structure |
| `Reading_Ingesting_Data_from_REST_APIs.md` | Concept explainer: why and how API ingestion works |
| `Student_Resources.md` | Curated references and quick code patterns |
| `Activity_0_UV_API_Project_Setup.md` | Pre-lab UV project setup for `student-work/week2/day3/` |
| `Activity_1_HTTP_and_REST_Fundamentals.ipynb` | Guided notebook: request/response anatomy, pagination, rate limits, requests vs httpx, and building a real multi-city weather dataset |
| `Activity_2_Async_SDKs_and_the_AI_Era.ipynb` | Guided notebook: sync vs async, API vs SDK, calling Gemini both via SDK and raw HTTP |
| `Activity_3_DataFrame_Fundamentals.ipynb` | Guided notebook: pandas and Polars basics on your own weather data, bridge to Day 4 |
| `Bonus_Lab_Weather_API_Explorer.ipynb` | The independent build: builds a `weather_explorer.py` CLI from a blank file in progressive iterations |
| `Group_Activity_Advise_on_API_Ingestion.md` | Non-technical advising and presentation activity |
| `quiz/Day_3_Exit_Ticket.md` | End-of-day Markdown Mash exit ticket |
| `starter/weather_explorer_starter.py` | Independent-build CLI starter scaffold |

Dataset: GitHub's public API and Open-Meteo, both keyless (Activity 1 and the
independent build); Open-Meteo again in Activity 3 and the Bonus Lab. All
non-Taxi, per the Week 2 dataset rule.

### Deliverables

| Deliverable | Description |
|---|---|
| Activity 1 and 2 notebooks | Completed, including the multi-city `weather_records` list |
| Activity 3 notebook | Completed, `df` and `pldf` with derived columns |
| `weather_explorer.py` | Working independent-build CLI (min/max/current temperature, with retry) |
| `pyproject.toml` and `uv.lock` | Day 3 UV project files in `student-work/week2/day3/` |
| Pull request | Opened, with two substantive review comments on a teammate's PR |
| Exit ticket | Completed `quiz/Day_3_Exit_Ticket.md` |
| Group recommendation | One-page memo or slide plus a 2 minute team presentation |

## Setup

Complete `Activity_0_UV_API_Project_Setup.md` first. Day 3 uses its own UV
project at `student-work/week2/day3/`. From the repo root:

```bash
mkdir -p student-work/week2/day3
cd student-work/week2/day3
uv init
uv add requests httpx python-dotenv boto3 google-genai pandas polars ipykernel
```

`ipykernel` is what lets VS Code use this environment as a notebook kernel. The
`.venv`, `pyproject.toml`, and `uv.lock` are created in
`student-work/week2/day3/`. Select `student-work/week2/day3/.venv/bin/python` as
the VS Code interpreter and notebook kernel. Keep copied notebooks,
`weather_explorer.py`, and any `data/` you create under `student-work/week2/day3/`
so they never conflict with a `git pull`. The full step-by-step, including the
first-time kernel selection in VS Code, is in
`Activity_0_UV_API_Project_Setup.md`.

Confirm the environment:

```bash
uv run python -c "import requests, pandas, polars; print('env ok')"
```

Activity 2 reads a Gemini key from a `.env` file. Create `.env` at the repo root
and make sure `.env` is gitignored so secrets never reach Git. (Activity 2's S3
read is unsigned and needs no AWS key.)

## Independent Build: `weather_explorer.py`

After the guided notebooks, prove the skills from a blank file. The **Bonus
Lab** (`Bonus_Lab_Weather_API_Explorer.ipynb`) walks you through building
`weather_explorer.py` in progressive iterations: one request, wrap it in a
function, several cities (sync then async), add a retry with backoff, and
finally ship it as a command-line tool. The finished script is the deliverable.

You build it in your work folder at `student-work/week2/day3/`, starting from
`starter/weather_explorer_starter.py` (copied in during Activity 0). It uses
Open-Meteo, which is free and keyless.

Run it from your work folder; `uv run` finds the Day 3 project environment
automatically:

```bash
cd student-work/week2/day3
uv run python weather_explorer.py "Hartford,US" 41.7658 -72.6734
```

Expected output shape (real numbers vary):

```text
Weather for Hartford,US
  current: 71.6F
  today's low:  61.2F
  today's high: 78.4F
```

### Success Criteria

- `weather_explorer.py` runs from the command line with a city label and
  latitude/longitude, and prints today's min, max, and current-hour temperature.
- A transient failure is retried with exponential backoff, not left to crash on
  the first error.
- The fetch uses `timeout=10` and checks the response before using the body.
- You can explain why the retry function wraps the plain fetch function instead
  of duplicating its logic.

### Stretch

- Add a `--humidity` flag that also prints the day's average humidity.
- Refactor the functions into a small client class so `main()` reads top to
  bottom in a few lines.

## Submit

Commit these under your course repo (via a pull request, then leave two
substantive review comments on a teammate's PR):

```text
student-work/week2/day3/weather_explorer.py
student-work/week2/day3/Activity_1_HTTP_and_REST_Fundamentals.ipynb
student-work/week2/day3/Activity_2_Async_SDKs_and_the_AI_Era.ipynb
student-work/week2/day3/Activity_3_DataFrame_Fundamentals.ipynb
```

The day environment files (`pyproject.toml`, `uv.lock`) live in
`student-work/week2/day3/`, and `.venv/` is gitignored.

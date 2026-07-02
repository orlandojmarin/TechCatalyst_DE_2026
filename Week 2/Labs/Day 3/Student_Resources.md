# Week 2 Day 3 Student Resources: APIs, SDKs, and DataFrames

**AI-free zone:** write the lab code by hand. Use these notes for patterns, vocabulary, and official references.

## Currentness Check

| Topic | Current source checked | Date checked | Content decision |
|---|---|---|---|
| UV project workflow | <https://docs.astral.sh/uv/concepts/projects/init/> | 2026-06-29 | Use `uv init`, `uv add`, `uv run`, and `uv lock` for local Python projects |
| Requests workflow | <https://requests.readthedocs.io/en/latest/user/quickstart/> | 2026-06-29 | Use `params`, `timeout`, `.json()`, and `raise_for_status()` |
| GitHub REST API | <https://docs.github.com/en/rest> | 2026-06-29 | Keyless at classroom volume; send a `User-Agent`; search paginates with `per_page` and `page` |
| Python exceptions | <https://docs.python.org/3/tutorial/errors.html> | 2026-06-29 | Catch specific exceptions and re-raise surprises |
| Python CSV module | <https://docs.python.org/3/library/csv.html> | 2026-06-29 | Use `csv.DictWriter` for flat cleaned output |
| Python JSON module | <https://docs.python.org/3/library/json.html> | 2026-06-29 | Use `json.dump` for files and `json.loads` for strings |
| Open-Meteo API | <https://open-meteo.com/en/docs> | 2026-06-29 | Keyless; needs latitude/longitude and a `current`/`hourly` field list |
| pandas | <https://pandas.pydata.org/docs/user_guide/index.html> | 2026-06-29 | pandas 3.0 copy-on-write: assign with `.loc[mask, "col"] = value`, not chained indexing |
| Polars | <https://docs.pola.rs/> | 2026-06-29 | Expression API (`pl.col`, `.with_columns`, `.filter`); no row index |

## APIs and HTTP

| Resource | Why it helps |
|---|---|
| [GitHub REST API](https://docs.github.com/en/rest) | The first real API in Activity 1: repo and search endpoints, keyless, needs a `User-Agent` header |
| [Requests Quickstart](https://requests.readthedocs.io/en/latest/user/quickstart/) | Official examples for query parameters, JSON responses, and errors |
| [HTTPX docs](https://www.python-httpx.org) | The modern successor to requests: sync and async, HTTP/2, used by FastAPI |
| [HTTP Status Codes, MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status) | Quick lookup for `200`, `400`, `403`, `404`, `429`, and `500` |
| [Open-Meteo Docs](https://open-meteo.com/en/docs) | Free, keyless weather API used in Activity 1 and the independent build; uses latitude/longitude and a `current`/`hourly` field list |
| [boto3 S3 client, unsigned access](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html) | The `Config(signature_version=UNSIGNED)` pattern used in Activity 2 to read a public S3 object (`head_object`/`get_object`) with no AWS credentials |
| [asyncio docs](https://docs.python.org/3/library/asyncio.html) | Standard-library async used in Activity 2 and the Bonus Lab with `httpx.AsyncClient` and `asyncio.gather` |
| [google-genai SDK](https://ai.google.dev/gemini-api/docs) | The current, supported Gemini SDK used in Activity 2 (never install the deprecated `google-generativeai`) |

## Pandas and Polars

| Resource | Why it helps |
|---|---|
| [pandas User Guide](https://pandas.pydata.org/docs/user_guide/index.html) | DataFrame basics used in Activity 3: `read_csv`, `.head()`, `.info()`, `.describe()`, filtering, `.loc` |
| [pandas Copy-on-Write](https://pandas.pydata.org/docs/user_guide/copy_on_write.html) | Why pandas 3.0 wants `.loc[mask, "col"] = value`, not chained indexing |
| [Polars User Guide](https://docs.pola.rs/) | The expression API (`pl.col`, `.with_columns`, `.filter`) contrasted with pandas in Activity 3 |
| [Polars vs pandas](https://docs.pola.rs/user-guide/migration/pandas/) | Side-by-side translation for anyone who knows pandas already |

## Three Lines You Always Write

```python
import requests

resp = requests.get(url, params=params, timeout=10)
resp.raise_for_status()
records = resp.json()
```

Why these matter:

- `params` lets Requests encode query parameters correctly.
- `timeout=10` prevents a stuck script from hanging forever.
- `raise_for_status()` turns HTTP failure responses into exceptions you can handle.
- `.json()` turns a JSON response body into Python dictionaries and lists.

## Pagination Pattern

Most list or search endpoints return one page at a time. GitHub's search API,
which you use in Activity 1, paginates with `per_page` and `page`:

```python
import time


def fetch_all(url, headers, per_page=100, max_pages=10):
    records = []
    for page in range(1, max_pages + 1):
        params = {"q": "data engineering", "per_page": per_page, "page": page}
        resp = requests.get(url, headers=headers, params=params, timeout=10)
        resp.raise_for_status()
        page_data = resp.json().get("items", [])
        if not page_data:
            break
        records.extend(page_data)
        time.sleep(0.5)
    return records
```

This pattern has two stop conditions:

- An empty page means the API has no more records for your query.
- `max_pages` protects you from an accidental infinite loop or huge download.

## API Keys

Some APIs today need no key at all (GitHub and Open-Meteo at classroom volume);
Gemini in Activity 2 does. When a key is needed, keep it in the environment,
never in code. GitHub, for example, works keyless but gives a much higher rate
limit if you send a token:

```python
import os

token = os.environ.get("GITHUB_TOKEN")
headers = {"User-Agent": "techcatalyst-de-2026"}
if token:
    headers["Authorization"] = f"Bearer {token}"
```

Do not commit API keys or tokens to Git.

## Secrets and .env

When a key is required, as in Activity 2 for Google Gemini, keep it in a `.env` file and load it with `python-dotenv`. The `.env` file goes in `.gitignore` so it is never committed. (Activity 2's AWS example needs no key at all: it reads a public S3 object with `Config(signature_version=UNSIGNED)`.)

```text
# .env  (never commit this file)
GOOGLE_API_KEY=your-key-here
```

```python
from dotenv import load_dotenv
import os

load_dotenv()
key = os.environ["GOOGLE_API_KEY"]
```

`uv add python-dotenv` to install it. The `google-genai` client reads `GOOGLE_API_KEY` from the environment after `load_dotenv()`.

## Exception Handling

Official reference: [Python Errors and Exceptions](https://docs.python.org/3/tutorial/errors.html)

```python
try:
    latitude = float(raw_latitude)
except (TypeError, ValueError):
    latitude = None
```

```python
try:
    records = fetch_all(url)
except requests.exceptions.RequestException as exc:
    print(f"API request failed: {exc}")
```

Rules:

- Catch specific exceptions you can handle.
- Let surprising errors crash loudly while you are developing.
- Do not use `except: pass`.

## File I/O: CSV and JSON

Official references:

- [Python csv module](https://docs.python.org/3/library/csv.html)
- [Python json module](https://docs.python.org/3/library/json.html)

### `load` Versus `loads`

| Function | Input | Use when |
|---|---|---|
| `json.load(file_obj)` | File object | Reading a JSON file |
| `json.loads(text)` | String | Parsing JSON text already in memory |
| `json.dump(obj, file_obj)` | Python object and file object | Writing JSON to a file |
| `json.dumps(obj)` | Python object | Returning a JSON string |

### Write Raw JSON

```python
with open("data/weather_raw.json", "w") as file:
    json.dump(weather_records, file, indent=2)
```

### Write Clean CSV

```python
fieldnames = ["city", "temp_f", "humidity", "conditions"]

with open("data/weather.csv", "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(weather_records)
```

## OOP: Just Enough to Read Real Code

```python
class OpenMeteoClient:
    def __init__(self, base_url="https://api.open-meteo.com/v1/forecast"):
        self.base_url = base_url

    def current(self, latitude, longitude):
        params = {
            "latitude": latitude, "longitude": longitude,
            "current": "temperature_2m", "temperature_unit": "fahrenheit",
        }
        resp = requests.get(self.base_url, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json()["current"]
```

The goal today is reading fluency. After this, `requests.Session()`, `storage.Client()`, and other client objects should feel less mysterious.

## Day 3 Checklist

| Part | Deliverable | Done |
|---|---|---|
| Setup | Shared repo-root UV project active (`uv init` at the repo root); `requests`, `httpx`, `python-dotenv`, `boto3`, `google-genai`, `pandas`, `polars`, `ipykernel` added; `.venv` selected as the kernel | [ ] |
| Activity 1 | HTTP fundamentals notebook complete: GitHub status + nested field, `weather_records` list built for 8 cities, working `httpx` call | [ ] |
| Activity 2 | Async/SDK notebook complete: `asyncio.gather` run is faster than the sync run, boto3 unsigned read works, raw Gemini `httpx` POST matches the SDK call | [ ] |
| Activity 3 | DataFrame notebook complete: weather data loaded into pandas and Polars, filtering and a derived column done in both | [ ] |
| Independent build | `weather_explorer.py` (from the Bonus Lab) runs from the CLI for 3+ cities with retry protection | [ ] |

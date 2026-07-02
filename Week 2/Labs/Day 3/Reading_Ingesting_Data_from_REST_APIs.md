---
title: "Ingesting Data from REST APIs"
module: "Week 2 Day 3"
type: explainer
audience: "Beginning data engineers"
---

# Ingesting Data from REST APIs

**AI-free zone:** read this to build intuition, then write today's lab code by hand. This explainer is the "why" behind the lab. The quick code patterns and links live in `Student_Resources.md`.

## Why This Matters

A large part of data engineering is getting data from somewhere you do not control into a place you do. A REST API is one of the most common somewheres. When you call an API, you are a guest on another team's system. It can be slow, it can fail, it can change its fields, and it can limit how often you may ask. A good ingestion script expects all of that and still produces a clean, reproducible result. That mindset, not the syntax, is the real skill today.

## Core Idea

An API request is a question, and the response is an answer with a receipt. The receipt is the status code. A `200` means the answer is good. A `404` means you asked for something that does not exist. A `429` means you asked too often. Your script should always read the receipt before trusting the answer. The pattern you will use all day is small: send a request with parameters and a timeout, check the receipt with `raise_for_status()`, then turn the body into Python objects with `.json()`.

## The Anatomy of a Request and a Response

Every request has a few parts:

- Method: the verb. `GET` reads data, `POST` sends data. Today you mostly use `GET`.
- URL: the address of the resource, such as `https://api.github.com/repos/psf/requests`.
- Query parameters: options added to the URL, such as `?q=data&per_page=3`. Pass them with `params=` so the library encodes them safely.
- Headers: metadata about the request, such as a `User-Agent` or an API key. Secrets travel in headers, not in the URL.
- Body: data you send on a `POST`, usually JSON.

Every response has:

- A status code: the receipt (`200`, `404`, `429`, `500`).
- Headers: metadata about the response, such as the content type.
- A body: the payload, usually JSON, which you parse with `.json()`.

When someone says "call an API," this is the whole vocabulary. Everything else today builds on these parts.

## How It Works

Three ideas carry most of the weight.

First, resilience. The network is not reliable, so a request can hang forever unless you set a `timeout`. A failed response should fail loudly during development, not slip through silently. Catching only the errors you can handle, such as `requests.exceptions.RequestException`, keeps real bugs visible.

Second, pagination. APIs rarely hand you everything at once. They give you a page and let you ask for the next one with parameters like `page` and `per_page` (GitHub's names; other APIs use `limit` and `offset`). You loop until a page comes back empty, and you also stop after a maximum number of pages so a mistake cannot trigger an enormous download.

Third, raw then clean. Save the unmodified response to a raw file first, then produce a separate clean file. The raw file is your evidence. If a downstream number looks wrong tomorrow, you can compare the clean output against the raw record and see exactly what your cleaning did. If you only keep the cleaned data, you have thrown away the ability to debug.

## Example

A minimal, resilient fetch reads like this:

```python
import requests

params = {"q": "data engineering", "per_page": 100, "page": 1}
resp = requests.get(url, params=params, timeout=10)
resp.raise_for_status()
records = resp.json()
```

That is four lines, but each line defends against a specific failure: wrong query encoding, a hung request, a bad response treated as good, and a body that is still text instead of Python objects.

## The Library: requests and httpx

`requests` is the classic Python HTTP library and is everywhere in tutorials and existing code. `httpx` is the modern successor. Its synchronous API is nearly identical, so migrating is mostly mechanical: the same `get`, `params`, `headers`, `raise_for_status`, and `json` all carry over. The reason to prefer `httpx` for new work is that it also supports async, HTTP/2, full type hints, and cleaner timeout and connection handling. Prefer a `Client` used as a context manager so connections are pooled and closed cleanly.

```python
import httpx

with httpx.Client(timeout=10) as client:
    resp = client.get(url, params=params)
    resp.raise_for_status()
    records = resp.json()
```

## Sync versus Async

Synchronous code makes one call and waits for it to finish before the next call starts. If you fetch ten endpoints one at a time, the total time is the sum of all ten. Asynchronous code starts the calls and lets them wait together, so the total time is closer to the slowest single call. Async helps when your program spends its time waiting on the network or disk, which is most of data ingestion. It does not speed up heavy computation. This is the same model FastAPI uses later in the course: an async endpoint can serve other requests while one waits on a database or an API.

## API versus SDK

An API is the contract: the URL, method, headers, and body you send over HTTP. An SDK is a language specific library that wraps that API and handles the tedious parts for you, such as authentication, request signing, retries, and pagination. You can usually do the same work either way. For AWS you almost always use the SDK (`boto3`), because raw AWS requests must be signed with a multi step signature that the SDK handles for you. For Google Gemini you can use the `google-genai` SDK or call the REST endpoint directly. The SDK is shorter and safer for production; raw HTTP is good for learning and for small one off calls.

This is also why API skills still matter in the AI era. An AI assistant is reached through an API. So is every cloud service. Even MCP, the protocol that lets AI agents use tools, is API calls underneath. The pipelines you build are made of API calls.

## Keeping Secrets Out of Code

API keys and cloud credentials must never appear in your code or in Git. The standard pattern is a `.env` file holding your secrets, listed in `.gitignore` so it is never committed, and loaded at runtime with `python-dotenv`.

```python
from dotenv import load_dotenv
import os

load_dotenv()
key = os.environ["GOOGLE_API_KEY"]
```

A single leaked key can become a real security incident at work, so build this habit from day one.

## Common Mistakes

- Calling `.json()` before `raise_for_status()`, so a failed response is parsed as if it succeeded.
- Forgetting `timeout`, so one slow endpoint freezes the whole script.
- Using `except: pass`, which hides the exact bug you need to see.
- Looping pages with no maximum guard, which risks a runaway download.
- Writing raw API records straight to CSV, which produces ragged columns because records do not all share the same keys.
- Hardcoding an API key or pasting it into a notebook instead of loading it from a `.env` file.
- Reaching for async on CPU heavy work, where it does not help.

## Key Takeaways

- Treat an API as an unreliable guest system and plan for failure.
- Always read the status code before trusting the body.
- Paginate with two stop conditions: an empty page and a maximum page count.
- Keep raw and clean data as separate files so you can always audit your work.
- Catch the errors you can handle and let surprises crash while you build.
- requests and httpx are nearly identical; prefer httpx for new work and gain async.
- An SDK wraps an API; use the SDK for cloud work and raw HTTP to learn.
- Keep secrets in a `.env` file loaded with python-dotenv, never in code or Git.

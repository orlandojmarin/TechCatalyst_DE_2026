# Deploy Stretch: Streamlit Community Cloud

**OPTIONAL.** This is for students who finish Activities 1 through 7 early. It is not required, it is not graded, and nothing later in the course depends on it. If you are still working through the activities, skip this and come back later.

## What deploying gets you

Right now your app only runs on your own machine, at a `localhost` address only you can open. Deploying it to Streamlit Community Cloud gives it a real public URL, something like `https://your-app-name.streamlit.app`, that anyone can open in a browser with no setup. That is worth having for your capstone presentation in Week 8: a link in your slides that a reviewer can click and interact with beats a screenshot or a screen share every time.

## Prerequisite: your own public GitHub repository

You need a GitHub account. If you do not have one, create one now at [github.com](https://github.com).

You also need a **new, public** repository that belongs to you, separate from the course repository. Do not push this to the TechCatalyst course repo, and do not fork it. Create a fresh repository (for example `taxi-demand-explorer`) from your own GitHub account, public, so Streamlit Community Cloud can read from it for free.

## What to push

Push exactly three things to your new repository:

1. Your app file (a copy of `activity_6_forecast_anomalies.py` or `activity_7_narrate_with_llm.py`, whichever you finished, from your `student-work/week7/day1/` folder).
2. A `requirements.txt` (see below).
3. The data file your app loads, `nyc_taxi.csv`, in a `data/` folder next to the app file.

Do not push the course's `pyproject.toml` or `uv.lock`. Those describe the whole course project's dependencies, not just this one app, and Streamlit Community Cloud does not read them anyway: it installs from a `requirements.txt` file it finds in your repository. A `requirements.txt` with only the packages this one app needs is the right file for a single deployed app, even though the course itself uses UV and `pyproject.toml` for everything else.

### `requirements.txt`

These versions are the ones verified against this course's environment. Use them as-is:

```
pandas==3.0.3
streamlit==1.60.0
plotly==6.9.0
statsmodels==0.14.6
yfinance==1.5.2
openai==2.51.0
python-dotenv==1.2.2
```

If you are only deploying the Activity 6 version of the app (no LLM narration), you can drop `openai` and `python-dotenv` from this list and skip the secrets section below entirely, since that version never reads an API key. If you are deploying the Activity 7 version, keep all seven lines and read the next section before you deploy.

## The API key: use Streamlit secrets, never the repo

Activity 7 reads `OPENAI_API_KEY` from a local `.env` file at the repository root. That works on your machine because `.env` is listed in the course's root `.gitignore` and never gets committed. A freshly created public repository does not have that `.gitignore` protecting it unless you add the same rule yourself, and even then, `.env` was never meant to travel with the deployed app in the first place.

**Do not commit your `.env` file, and do not paste your API key into any file you push to GitHub.** If a key ever does end up in a public repo, anyone who finds it can use it and run up charges against your account. If that happens, treat the key as burned: go to your OpenAI account, revoke that key immediately, and issue a new one before doing anything else. Do not wait to see if anyone actually uses it first.

Streamlit Community Cloud has a separate mechanism for this exact problem: **Secrets**. Secrets live in the app's own settings on Streamlit's servers, in TOML format, and are never part of your repository.

To set a secret while deploying a new app, click **Advanced settings** on the deploy form and paste your secret into the **Secrets** field, in TOML form:

```toml
OPENAI_API_KEY = "sk-your-key-here"
```

To set or change a secret on an app that is already deployed: from your workspace at [share.streamlit.io](https://share.streamlit.io), find the app, click the three-dot menu next to it, choose **Settings**, open the **Secrets** tab, paste the same TOML, and click **Save**.

Inside your code, a secret you set this way is available through `st.secrets`:

```python
st.secrets["OPENAI_API_KEY"]
```

Streamlit also exposes root-level secrets like this one as ordinary environment variables in the deployed app, the same way `os.environ.get("OPENAI_API_KEY")` reads a value from `.env` locally. That means the guard already in Activity 7's starter file, `os.environ.get("OPENAI_API_KEY")`, works unmodified once you set `OPENAI_API_KEY` as a secret on Community Cloud: you do not have to rewrite that check to call `st.secrets` instead.

If you want a single, explicit line of code that is guaranteed to work in both places regardless of that automatic exposure, use this pattern instead of relying on it silently:

```python
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()  # populates os.environ from .env when running locally; does nothing on Community Cloud

def get_secret(name: str) -> str | None:
    """Read a secret from the environment first, then from Streamlit secrets.

    Locally, load_dotenv() has already copied .env into os.environ, so the
    first branch returns the key. On Community Cloud, the value you set in
    the app's Secrets panel is what the second branch reads, whether or not
    it was also mirrored into the environment.
    """
    value = os.environ.get(name)
    if value:
        return value
    try:
        return st.secrets[name]
    except Exception:
        return None

api_key = get_secret("OPENAI_API_KEY")
```

Either way, the key itself never appears in a file you commit. It lives in your local `.env` (gitignored) and in the app's Secrets panel (not part of the repo at all).

## Connecting your app at share.streamlit.io

1. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with your GitHub account.
2. Click **Create app** in the upper right.
3. Choose the option for an app you already have, then fill in:
   - **Repository**: your new public repo.
   - **Branch**: usually `main`.
   - **Main file path**: the path to your app file inside the repo, for example `activity_7_narrate_with_llm.py`.
4. If your app needs the OpenAI key, click **Advanced settings** and paste your `OPENAI_API_KEY` into the **Secrets** field as shown above, before you deploy.
5. Click **Deploy**. The first deploy takes a few minutes while Community Cloud installs everything in `requirements.txt`.

## Everything in a public repo is public

A public GitHub repository is exactly that: public. Anyone on the internet can read every file in it, including every commit in its history, even ones you later delete or overwrite. That covers your app's `.py` file, your `requirements.txt`, and your `data/nyc_taxi.csv`.

The NYC taxi data is fine to publish; it is already public. But do not add anything from this course that touches Hartford or any insurance client data, real or synthetic, to this repository. If you want to demo an insurance-flavored app later, use synthetic data you generate yourself and treat it as public the moment you push it, because it is.

## Troubleshooting

**"ModuleNotFoundError" for a package you know you're using.**
The package is missing from `requirements.txt`, or it is misspelled. Compare the import at the top of your app file against every line in `requirements.txt`. A common miss on this app: forgetting `openai` or `python-dotenv` when you copy the Activity 7 version.

**The app works locally but crashes on "file not found" for `nyc_taxi.csv` once deployed.**
This is exactly why the app resolves its data path with `Path(__file__).parent` and a fallback, instead of a hardcoded string:

```python
HERE = Path(__file__).parent
DATA = HERE / "data" / "nyc_taxi.csv"
if not DATA.exists():
    DATA = HERE.parent / "data" / "nyc_taxi.csv"
```

If it still fails once deployed, check that `nyc_taxi.csv` actually made it into your GitHub repo (large files are sometimes skipped by accident) and that it sits in a `data/` folder in the same place relative to your app file as it does in `student-work/week7/day1/`.

**`st.error("No OPENAI_API_KEY found...")` or a `KeyError` on `OPENAI_API_KEY` once deployed, even though the app worked locally.**
Your local `.env` never travels with the deploy. Add `OPENAI_API_KEY` as a secret in the app's **Settings > Secrets** panel (see above), click **Save**, and let the app restart. If you just added the secret and it still is not picking up, double check the TOML you pasted uses the exact key name `OPENAI_API_KEY` with no typo and no extra quoting.

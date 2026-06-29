# Lab D: Fun Lab, Your GitHub Profile Page

**Module:** Developer foundations (Day 3) · **Format:** Solo (it is *your* page) · ⏱️ about 20–30 minutes

> [!NOTE]
> **The fun one.** You just learned repos, commits, and PRs. Now use them to build something that is 100% *you*: a personal branding page that greets anyone who visits your GitHub. You will grow it every week of the program.

---

##  Goal

By the end of this lab you have:

- a **GitHub profile README** that appears on your public profile page;
- a clean first version: who you are, your data-engineering focus, and what you are learning;
- a plan to update it each week as you finish labs and the longitudinal project.

##  Why this matters

Your GitHub profile is the first thing a recruiter, teammate, or hiring manager sees. A blank profile says "beginner"; a thoughtful one says "I take my craft seriously." By the end of TechCatalyst you will have real projects to show : this page is where you showcase them. Start it now, grow it weekly, and by Week 8 you have a portfolio front door that did not exist on Day 1.

## 👀 See it first

1. **The instructor's profile:** [github.com/tatwan](https://github.com/tatwan) : notice the headline, the "About Me", the skills grouped by category, and the project links. Yours will be simpler today and grow over time.
2. **GitHub's own explanation:** [Setting up and managing your GitHub profile -> Profile README](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/managing-your-profile-readme).

>  **The trick:** GitHub treats a repository named **exactly your username** as special. The `README.md` in `yourusername/yourusername` is rendered right on your profile page. That is the whole secret.

---

##  The special repository

If your username is `janedoe`, you create a repo called **`janedoe`**. When you do, GitHub shows a banner like:

>  **janedoe/janedoe is a special repository.** Its `README.md` will appear on your public profile.

That banner is how you know you named it correctly.

> [!IMPORTANT]
> **Note:** this lab can be completed in the GitHub web editor. If you want extra Git practice, use your local terminal and VS Code.

---

## Part 1: Create the special repo (5 min)

1. Go to **github.com**, click **+** (top right) -> **New repository**.
2. **Repository name:** type your username **exactly** (same spelling and case as your profile). Watch for the  "special repository" banner : that is your confirmation.
3. **Public** (it must be public to show on your profile).
4. Check **Add a README file**.
5. Click **Create repository**.

 **Checkpoint:** you saw the "special repository" banner, and the repo is created with a `README.md`.

---

## Part 2: Write your profile (15 min)

1. In your new repo, open `README.md` and click the **pencil (✏️ Edit)**.
2. **Delete** the default line and paste the starter template below.
3. Replace every `REPLACE-ME` with your own words. **Write it yourself** : this is *your* story, not an AI's. Keep it short and honest; you will add to it weekly.

```markdown
# Hi, I'm REPLACE-ME-YOUR-NAME

### Aspiring Data Engineer, TechCatalyst DE 2026

I'm building production-grade data engineering skills by hand, no shortcuts.

---

##  About Me

- REPLACE-ME: one line about your background, degree, where you are from, or how you got into data.
- Currently in the **TechCatalyst Data Engineering 2026** bootcamp at The Hartford.
- REPLACE-ME: one thing you are excited to build or learn.
- Reach me: [LinkedIn](REPLACE-ME-LINKEDIN-URL)

---

##  Currently Learning

Working through an 8-week, real-world data pipeline (NYC Taxi data) covering:

- **Now (Week 1):** Cloud foundations, Git/GitHub, Python environments, data architecture
- **Coming up:** Python for DE · SQL & BigQuery · Snowflake & dbt · PySpark · GenAI · BI dashboards

---

##  Data Engineering Toolbox

> I update this as I learn each tool in the program.

**Comfortable with:** REPLACE-ME (e.g., Git, GitHub, VS Code, the command line)

**Learning now:** Python · Google Cloud (BigQuery, GCS) · SQL

**Coming soon:** Snowflake · dbt · PySpark · Airflow

---

##  Projects

- **TechCatalyst Capstone (in progress):** an end-to-end data pipeline covering ingestion, warehousing, transformation, and analytics. Details coming as I build it.
- _Add your own repos here as you create them._

---

##  Let's Connect

- LinkedIn: REPLACE-ME-LINKEDIN-URL
- REPLACE-ME (optional)
```

4. Scroll down, write a commit message like `Create my profile README`, and click **Commit changes**.

 **Checkpoint:** the edit is committed (you can edit the web file as many times as you like : each save is a commit).

---

## Part 3: See it live (2 min)

1. Visit **`github.com/yourusername`** (your profile, not the repo).
2. Your README now renders at the top of your profile. 

 **Checkpoint:** your profile page shows your new page instead of an empty profile.

---

##  Make it a habit: grow it every week

This page is never "done." Each Friday, spend five minutes adding what you built:

| Week | Add to your profile |
| :--- | :--- |
| 1 (now) | Your intro, focus, and starter toolbox |
| 2 | Python : link your first script repo; move Python to "Comfortable with" |
| 3 | SQL & BigQuery : note what you queried |
| 4 | Snowflake & dbt : add a transformation project |
| 5 | PySpark : add your Spark ETL repo |
| 6 | GenAI : add your Gemini/LLM project |
| 7 | A BI dashboard or Streamlit app screenshot |
| 8 | Pin your capstone repo and write a short project summary |

> By graduation, "Coming soon" should be empty and "Projects" should be full.

---

## Success Criteria

- [ ] Created a repo named **exactly** your username (saw the  special-repo banner)
- [ ] Repo is **public** and has a `README.md`
- [ ] Replaced every `REPLACE-ME` with your own words (written by you, not AI)
- [ ] Visited `github.com/yourusername` and saw your page render
- [ ] Know which week you'll next update it

---

##  Optional polish (for fast finishers)

- **Badges:** add shields.io badges (like the LinkedIn/Website badges on the instructor's profile). Browse [shields.io](https://shields.io/) and the [Markdown badges gallery](https://github.com/Ileriayo/markdown-badges).
- **GitHub stats card:** drop in an auto-updating stats image from [github-readme-stats](https://github.com/anuraghazra/github-readme-stats) : e.g. `![stats](https://github-readme-stats.vercel.app/api?username=YOURNAME)`.
- **A profile picture and bio:** set your avatar and the short bio in **Settings -> Public profile** so the whole page looks complete.

---

## Optional: Do It the Git Way Instead of the Web Editor

Prefer to practice today's skills? You can clone the special repo locally and use the full cycle:

```bash
cd ~/techcatalyst-work
git clone https://github.com/YOUR-USERNAME/YOUR-USERNAME.git profile-readme
cd profile-readme
# edit README.md in VS Code, then:
git add README.md
git commit -m "Write my profile README"
git push
```

Same result: your profile updates on push.

---

##  What you learned

- A repo named after your username is **special**: its `README.md` is your public profile page.
- You can edit Markdown directly on GitHub. The web editor commits for you, no local setup required.
- Your profile is a living portfolio: small weekly updates compound into a strong professional presence by Week 8.

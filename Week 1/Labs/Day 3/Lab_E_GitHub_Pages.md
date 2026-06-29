# Lab E: Fun Lab, Your GitHub Pages Site

**Module:** Developer foundations (Day 3) · **Format:** Solo (it is *your* site) · ⏱️ about 25–35 minutes

> [!NOTE]
> **The other fun one.** Lab D gave you a profile *README*. This lab gives you a real *website* : a welcome page and a mini-blog, live on the internet at your own URL, with a clean theme you can recolor and grow. GitHub hosts it for free.

---

##  Goal

By the end of this lab you have:

- a **live website** at `https://YOURUSERNAME.github.io/data-blog/` (or your chosen repo name);
- a polished **welcome page** (hero, about, links) plus a **first blog post**, using a provided HTML/CSS theme;
- the muscle memory to **add a new post** in five minutes any week of the program.

##  Why this matters

A profile README says who you are in a paragraph. A site lets you tell the longer story: write up a project, explain a tricky bug you solved, show a dashboard screenshot. Recruiters love a candidate who writes. The skill itself is real: GitHub Pages is how thousands of engineers ship docs, portfolios, and project sites. You will publish one today and feed it all program long.

## 👀 See it first

1. **What you are about to build:** a landing page with a hero, an about section, and a list of posts. Each post is its own page. The theme includes a light-mode toggle.
2. **GitHub's own explanation:** [GitHub Pages -> Creating a GitHub Pages site](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site).

> **The trick:** GitHub Pages takes the HTML files in a repo, or a folder inside it, and serves them as a real website. No servers, no build step, just `index.html` and `style.css`.

---

## 📦 What's in the starter template

In this lab folder you'll find `github-pages-template/`. Copy these three files into your repo:

| File | What it is |
| :--- | :--- |
| `index.html` | Your home page: hero, about cards, a list of post cards, and contact links. |
| `style.css` | The theme. All colors are CSS variables at the top : change `--accent` to recolor the whole site. |
| `posts/first-post.html` | One example blog post. Copy it to make each new post. |

> [!IMPORTANT]
> **Note:** like Lab D, this can be done in the GitHub web editor. If you want more Git practice, use your local terminal and VS Code.

---

## Part 1: Create the repo (5 min)

1. Go to **github.com**, click **+** (top right) -> **New repository**.
2. **Repository name:** `data-blog` (any name works; this becomes part of your URL).
3. **Public** (Pages serves public repos for free).
4. Check **Add a README file**.
5. Click **Create repository**.

 **Checkpoint:** you have a public repo named `data-blog`.

---

## Part 2: Add the template files (10 min)

You'll recreate the three starter files in your repo using the web editor.

1. In your repo, click **Add file -> Create new file**.
2. Name it **`index.html`**. Open `github-pages-template/index.html` from this lab folder, copy all of it, and paste it in.
3. Commit with a message like `Add home page`.
4. Repeat for **`style.css`** (paste from the template), commit.
5. For the post: click **Add file -> Create new file** and name it **`posts/first-post.html`** : typing the `posts/` prefix creates the folder automatically. Paste from the template and commit.

>  You should now have `index.html`, `style.css`, and `posts/first-post.html` in your repo.

 **Checkpoint:** three files committed, with `first-post.html` sitting inside a `posts/` folder.

---

## Part 3: Turn on GitHub Pages (3 min)

1. In your repo, go to **Settings -> Pages** (left sidebar).
2. Under **Build and deployment -> Source**, choose **Deploy from a branch**.
3. Set **Branch** to `main` and folder to **`/ (root)`**. Click **Save**.
4. Wait about 1 minute. Refresh the page. GitHub shows: **"Your site is live at `https://YOURUSERNAME.github.io/data-blog/`."**

 **Checkpoint:** you have a live URL. Open it : you should see the themed welcome page.

> [!NOTE]
> First deploy can take 1–2 minutes. If you see a 404, wait, then hard-refresh (Cmd/Ctrl+Shift+R). The link from a post back to home and the theme toggle should both work.

---

## Part 4: Make it yours (10 min)

Edit `index.html` and `posts/first-post.html` and replace every `REPLACE-ME`:

- **Your name** in the title, nav brand, and hero.
- **About** : two or three honest sentences. Write it yourself (AI-Free Zone).
- **Links** : your GitHub, LinkedIn, and email.
- **First post** : fill in `posts/first-post.html`: why you're here, what Week 1 felt like, what's next.

Each save in the web editor is a commit; the live site updates within a minute.

**Want a different color?** Open `style.css` and change `--accent` (and `--accent-2`) near the top. The whole site re-themes instantly.

 **Checkpoint:** no `REPLACE-ME` left, your post reads like *you*, and the live site reflects your edits.

---

##  Make it a habit: one post per week

Adding a post is a two-step copy:

1. In `posts/`, copy `first-post.html` to a new file (e.g. `week2-python.html`) and edit the title, date, and body.
2. In `index.html`, copy one `<article class="post-card">` block, paste it at the **top** of the post list, and point its link at your new file.

| Week | Post idea |
| :--- | :--- |
| 1 (now) | Why I'm here + first impressions |
| 2 | My first Python script that pulls an API |
| 3 | The SQL query I was proudest of |
| 4 | What dbt actually does, in my words |
| 5 | Running the same Spark job three ways |
| 6 | Letting an LLM tag my data |
| 7 | A dashboard screenshot + what it shows |
| 8 | My capstone: the whole pipeline, end to end |

> By graduation you will have an 8-post engineering blog, a portfolio that writes your story for you.

---

## Success Criteria

- [ ] Created a **public** repo and added `index.html`, `style.css`, and `posts/first-post.html`
- [ ] Enabled **GitHub Pages** (Settings -> Pages, deploy from `main` / root)
- [ ] Site is **live** at `https://YOURUSERNAME.github.io/<repo>/`
- [ ] Replaced every `REPLACE-ME` with your own words (written by you, not AI)
- [ ] Theme toggle works and the post links to/from the home page
- [ ] Know how you'll add next week's post

---

##  Optional polish (for fast finishers)

- **Recolor it:** change `--accent` / `--accent-2` in `style.css`, or build a second color scheme by editing the `[data-theme="light"]` block.
- **Add a favicon:** drop a small `favicon.ico` in the repo root and add `<link rel="icon" href="favicon.ico">` in the `<head>`.
- **Link it everywhere:** add the site URL to your GitHub profile README (from Lab D) and your LinkedIn.
- **A real photo:** add an `<img>` of a project screenshot in a post : it makes the page feel alive.

---

##  Optional: do it "the Git way" instead of the web editor

Prefer to practice today's skills? Clone the repo locally and use the full cycle:

```bash
cd ~/techcatalyst-work
git clone https://github.com/YOUR-USERNAME/data-blog.git data-blog
cd data-blog
# copy the three template files into place, then:
git add index.html style.css posts/first-post.html
git commit -m "Add GitHub Pages site"
git push
```

Same result: Pages rebuilds on push.

---

##  What you learned

- **GitHub Pages** serves the HTML in a repo as a free, live website. No server, no build step.
- A site is just `index.html` + `style.css`; **CSS variables** let you re-theme everything from one place.
- Linking pages (home ↔ `posts/`) and folders (`posts/first-post.html`) is the backbone of every static site.
- Your blog is a living portfolio: one short post a week compounds into a real engineering presence by Week 8.

# JobStreet Indonesia Job Market Scraper

<p align="left">
  <img src="https://img.shields.io/badge/Python-3.9+-blue?style=flat-square&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Selenium-Automation-green?style=flat-square" alt="Selenium">
  <img src="https://img.shields.io/badge/Pandas-Analysis-purple?style=flat-square&logo=pandas" alt="Pandas">
</p>

I built this to answer a simple question: what does the data job market in Indonesia actually look like right now? Instead of reading secondhand reports, I scraped JobStreet directly and ran the numbers myself.

The scraper handles login sessions, anti-bot detection, and dynamic content loading — then exports clean data to CSV and JSON for analysis in Jupyter.

**From the latest run:** 95 job listings, 86 companies, 29 cities.

---

## What the data shows

Jakarta accounts for about **62% of all data job postings** — South Jakarta being the densest area, followed by Central Jakarta. Data Analyst is the most in-demand role at 44%, with Data Engineer trailing at ~33%.

Only 28% of listings actually show salary numbers. From those that do, the median sits around **Rp 7.5M/month** for entry-to-mid level, with senior positions reaching up to Rp 22.5M.

---

## How it works

The scraper uses Selenium with a persistent Chrome profile, so you only log in once and the session is saved for future runs. Each keyword scrapes across multiple pages, collecting title, company, location, salary, and posting date per job card. After finishing all keywords, duplicates are removed (title + company as composite key) before saving.

The analysis is in `analysis.ipynb` — covers location distribution, salary parsing from raw strings using regex, job category classification, and a summary dashboard with four panels.

---

## Stack

Python 3.9, Selenium, Pandas, Matplotlib, Seaborn, Jupyter Notebook

---

## Setup

```bash
git clone https://github.com/hansenlaw/jobstreet_scrapping.git
cd jobstreet_scrapping
pip install -r requirements.txt
```

Run the scraper:

```bash
python jobstreet_scrapping.py
```

On first run, Chrome will open and ask you to log in to JobStreet. Once you do, hit ENTER in the terminal to start scraping. Login is saved to `~/.jobstreet_profile` so you won't need to do this again.

Output: `jobstreet_jobs_TIMESTAMP.csv` and `jobstreet_jobs_TIMESTAMP.json`

To change what gets scraped, edit these two lines near the top of the file:

```python
KEYWORDS = ["data analyst", "data scientist", "data engineer"]
PAGES_PER_KEYWORD = 5
```

---

## Analysis

```bash
jupyter notebook analysis.ipynb
```

The notebook picks up the latest CSV file automatically and walks through the full analysis — no manual file selection needed.

---

## A few things that were tricky

**Anti-bot detection** — Selenium is detectable by default. JobStreet either blocks it or serves a broken page. The fix was combining a persistent user profile with `--disable-blink-features=AutomationControlled`. This makes the browser behave close enough to a real session that it works consistently.

**Dynamic loading** — Content is rendered via JavaScript, so you need scroll simulation and enough wait time before parsing. Without this, most job cards just don't show up.

**Inconsistent HTML** — Card structure varies across listing types, so I wrote multiple CSS selector fallbacks per field. If one selector fails, it tries the next one before giving up.

**Salary parsing** — Salary comes in as a raw string like `"Rp 7.000.000 – Rp 10.000.000 per month"`. Getting usable numbers out of that required regex with some edge case handling since the formatting isn't always consistent across listings.

---

## What's next

- Expand to other portals (Glints, Kalibrr, LinkedIn) for comparison
- Schedule automated runs with cron or Airflow
- Store data in PostgreSQL so you can track changes over time
- Build a Streamlit dashboard for interactive exploration

---

**Hansen Lawrence** — Data Engineer / Data Analyst
[LinkedIn](https://linkedin.com/in/yourprofile) · [GitHub](https://github.com/hansenlaw)

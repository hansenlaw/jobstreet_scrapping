# JobStreet Indonesia Job Market Scraper & Analysis

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-blue?style=flat-square&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Selenium-Web%20Scraping-green?style=flat-square" alt="Selenium">
  <img src="https://img.shields.io/badge/Pandas-Data%20Analysis-purple?style=flat-square&logo=pandas" alt="Pandas">
  <img src="https://img.shields.io/badge/Status-Active-success?style=flat-square" alt="Status">
</p>

## Overview

Automated web scraper to collect and analyze job market data from **JobStreet Indonesia**. This project demonstrates skills in **web scraping**, **data collection**, and **data analysis** - essential skills for Data Engineer and Data Analyst roles.

### Key Results
- **95+ job listings** scraped from multiple keywords
- **50+ unique companies** identified
- **10+ cities** covered across Indonesia
- Salary range analysis for data roles

---

## Features

| Feature | Description |
|---------|-------------|
| Multi-keyword Scraping | Scrape multiple job categories in one run |
| Anti-bot Bypass | Persistent browser profile to avoid login popups |
| Data Export | Export to CSV and JSON formats |
| Data Analysis | Jupyter notebook with visualizations |
| Duplicate Removal | Automatic deduplication of job listings |

---

## Tech Stack

```
Python 3.9+
├── Selenium (Web Automation)
├── Pandas (Data Manipulation)
├── Matplotlib (Visualization)
└── Jupyter Notebook (Analysis)
```

---

## Project Structure

```
jobstreet_scrapping/
├── jobstreet_scrapping.py    # Main scraper script
├── analysis.ipynb            # Data analysis notebook
├── requirements.txt          # Dependencies
├── data/                     # Output directory
│   ├── jobstreet_jobs_*.csv
│   └── jobstreet_jobs_*.json
└── README.md
```

---

## Installation

```bash
# Clone repository
git clone https://github.com/hansenlaw/jobstreet_scrapping.git
cd jobstreet_scrapping

# Install dependencies
pip install -r requirements.txt
```

---

## Usage

### 1. Configure Settings

Edit `jobstreet_scrapping.py`:

```python
KEYWORDS = ["data analyst", "data scientist", "data engineer"]
PAGES_PER_KEYWORD = 5
```

### 2. Run Scraper

```bash
python jobstreet_scrapping.py
```

### 3. First Run
- Browser will open automatically
- Login if prompted (login will be saved for future runs)
- Press ENTER in terminal to start scraping

### 4. Output
- `jobstreet_jobs_TIMESTAMP.csv` - Data in CSV format
- `jobstreet_jobs_TIMESTAMP.json` - Data in JSON format

---

## Data Analysis

See [`analysis.ipynb`](analysis.ipynb) for detailed analysis including:

- Top hiring companies
- Job distribution by location
- Salary range analysis
- Most in-demand job titles

### Sample Insights

| Metric | Value |
|--------|-------|
| Total Jobs Scraped | 95+ |
| Unique Companies | 50+ |
| Jobs with Salary Info | ~30% |
| Top Location | Jakarta |

---

## Sample Output

| Title | Company | Location | Salary |
|-------|---------|----------|--------|
| Data Analyst | PT Main Games Indonesia | Jakarta Selatan | - |
| Junior Business Analyst | PT Perangkat Lunak Indonesia | Jakarta Pusat | Rp 5.5-7 jt |
| Data Analyst | PT Nusantara Sakti Group | Jakarta Barat | Rp 7-10 jt |

---

## Skills Demonstrated

- **Web Scraping**: Selenium, HTML parsing, CSS selectors
- **Data Engineering**: ETL pipeline, data collection, automation
- **Data Analysis**: Pandas, data cleaning, visualization
- **Python**: OOP, error handling, file I/O
- **Version Control**: Git, GitHub

---

## Future Improvements

- [ ] Add more job portals (LinkedIn, Glints, Kalibrr)
- [ ] Schedule automated daily scraping
- [ ] Store data in PostgreSQL database
- [ ] Build interactive dashboard with Streamlit
- [ ] Add salary prediction model

---

## Author

**Hansen Lawrence**
Data Engineer | Data Analyst

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=flat-square&logo=linkedin)](https://linkedin.com/in/yourprofile)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black?style=flat-square&logo=github)](https://github.com/hansenlaw)

---

## License

This project is for educational and portfolio purposes.

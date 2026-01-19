# JobStreet Indonesia Job Scraper

Web scraper untuk mengambil data lowongan kerja dari JobStreet Indonesia menggunakan Python dan Selenium.

## Fitur
- Scrape multiple keywords sekaligus
- Auto-save login (tidak perlu login ulang)
- Export ke CSV dan JSON
- Statistik hasil scraping

## Instalasi

```bash
pip install selenium
```

## Cara Pakai

1. Edit `KEYWORDS` dan `PAGES_PER_KEYWORD` di file `jobstreet_scrapping.py`:
```python
KEYWORDS = ["data analyst", "data scientist", "data engineer"]
PAGES_PER_KEYWORD = 5
```

2. Jalankan script:
```bash
python jobstreet_scrapping.py
```

3. Jika pertama kali, browser akan terbuka untuk login. Setelah login, tekan ENTER.

## Output
- `jobstreet_jobs_TIMESTAMP.csv` - Data dalam format CSV
- `jobstreet_jobs_TIMESTAMP.json` - Data dalam format JSON

## Tech Stack
- Python 3
- Selenium WebDriver
- Google Chrome

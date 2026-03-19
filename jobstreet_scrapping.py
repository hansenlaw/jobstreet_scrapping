"""
JobStreet Indonesia Job Scraper
Simple & Easy to Understand
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import csv
import json
import os
from datetime import datetime
from collections import Counter


# ============== SETTINGS (UBAH DI SINI) ==============
KEYWORDS = ["data analyst", "data scientist", "data engineer"]  # Tambah/kurangi sesuai kebutuhan
PAGES_PER_KEYWORD = 5  # Jumlah halaman per keyword
# =====================================================


class JobStreetScraper:

    def __init__(self):
        self.driver = None
        self.all_jobs = []
        self.profile_dir = os.path.expanduser("~/.jobstreet_profile")

    def start_browser(self):
        """Buka browser Chrome"""
        options = Options()

        # Simpan profile supaya tidak perlu login ulang
        os.makedirs(self.profile_dir, exist_ok=True)
        options.add_argument(f"--user-data-dir={self.profile_dir}")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        # Cari Chrome di komputer
        chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        ]
        for path in chrome_paths:
            if os.path.exists(path):
                options.binary_location = path
                break

        self.driver = webdriver.Chrome(options=options)
        print("Browser started!")

    def close_browser(self):
        """Tutup browser"""
        if self.driver:
            self.driver.quit()
            print("Browser closed.")

    def scroll_page(self):
        """Scroll halaman untuk load semua job"""
        for i in range(5):
            self.driver.execute_script(f"window.scrollTo(0, {(i+1) * 600});")
            time.sleep(0.3)

    def close_popup(self):
        """Tutup popup login jika muncul"""
        try:
            self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
            time.sleep(0.5)
        except:
            pass

    def extract_job_info(self, card):
        """Ambil info job dari card element"""
        job = {
            "title": "N/A",
            "company": "N/A",
            "location": "N/A",
            "salary": "N/A",
            "date": "N/A",
            "url": "N/A",
            "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # Title
        for selector in ["[data-automation='jobTitle']", "a[data-testid='job-card-title']", "h3 a"]:
            try:
                elem = card.find_element(By.CSS_SELECTOR, selector)
                job["title"] = elem.text.strip()
                job["url"] = elem.get_attribute("href") or "N/A"
                if job["title"]: break
            except: pass

        # Company
        for selector in ["[data-automation='jobCompany']", "a[data-automation='jobCompany']"]:
            try:
                elem = card.find_element(By.CSS_SELECTOR, selector)
                job["company"] = elem.text.strip()
                if job["company"]: break
            except: pass

        # Location
        for selector in ["[data-automation='jobLocation']", "[data-automation='jobCardLocation']"]:
            try:
                elem = card.find_element(By.CSS_SELECTOR, selector)
                job["location"] = elem.text.strip()
                if job["location"]: break
            except: pass

        # Salary
        try:
            elem = card.find_element(By.CSS_SELECTOR, "[data-automation='jobSalary']")
            job["salary"] = elem.text.strip()
        except: pass

        # Date
        try:
            elem = card.find_element(By.CSS_SELECTOR, "[data-automation='jobListingDate']")
            job["date"] = elem.text.strip()
        except: pass

        return job

    def scrape_keyword(self, keyword, max_pages):
        """Scrape jobs untuk satu keyword"""
        jobs = []
        seen = set()

        for page in range(1, max_pages + 1):
            # Buat URL
            keyword_slug = keyword.lower().replace(" ", "-")
            url = f"https://id.jobstreet.com/id/job-search/{keyword_slug}-jobs"
            if page > 1:
                url += f"?pg={page}"

            print(f"  Page {page}: {url}")

            # Buka halaman
            self.driver.get(url)
            time.sleep(3)
            self.close_popup()
            self.scroll_page()
            time.sleep(1)

            # Cari job cards
            cards = self.driver.find_elements(By.CSS_SELECTOR,
                "article[data-automation='normalJob'], article[data-card-type='JobCard'], article")

            # Extract setiap job
            count = 0
            for card in cards:
                job = self.extract_job_info(card)
                if job["title"] != "N/A":
                    job_id = f"{job['title']}_{job['company']}"
                    if job_id not in seen:
                        seen.add(job_id)
                        jobs.append(job)
                        count += 1

            print(f"    Found {count} jobs")
            time.sleep(2)

        return jobs

    def scrape_all(self, keywords, pages_per_keyword):
        """Scrape semua keywords"""
        for i, keyword in enumerate(keywords, 1):
            print(f"\n[{i}/{len(keywords)}] Keyword: {keyword.upper()}")
            jobs = self.scrape_keyword(keyword, pages_per_keyword)
            self.all_jobs.extend(jobs)
            print(f"  Total so far: {len(self.all_jobs)} jobs")

        # Hapus duplikat
        seen = set()
        unique = []
        for job in self.all_jobs:
            job_id = f"{job['title']}_{job['company']}"
            if job_id not in seen:
                seen.add(job_id)
                unique.append(job)

        self.all_jobs = unique
        return unique

    def save_to_csv(self, filename):
        """Simpan ke CSV"""
        if not self.all_jobs:
            print("No jobs to save!")
            return

        with open(filename, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=self.all_jobs[0].keys())
            writer.writeheader()
            writer.writerows(self.all_jobs)
        print(f"Saved: {filename}")

    def save_to_json(self, filename):
        """Simpan ke JSON"""
        if not self.all_jobs:
            print("No jobs to save!")
            return

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.all_jobs, f, indent=2, ensure_ascii=False)
        print(f"Saved: {filename}")

    def show_stats(self):
        """Tampilkan statistik"""
        if not self.all_jobs:
            return

        companies = Counter(j["company"] for j in self.all_jobs if j["company"] != "N/A")
        locations = Counter(j["location"] for j in self.all_jobs if j["location"] != "N/A")

        print(f"\n{'='*50}")
        print(f"TOTAL JOBS: {len(self.all_jobs)}")
        print(f"{'='*50}")
        print(f"Unique Companies: {len(companies)}")
        print(f"Unique Locations: {len(locations)}")

        print(f"\nTop 5 Companies:")
        for company, count in companies.most_common(5):
            print(f"  - {company}: {count}")

        print(f"\nTop 5 Locations:")
        for loc, count in locations.most_common(5):
            print(f"  - {loc}: {count}")


# ============== MAIN PROGRAM ==============
if __name__ == "__main__":
    print("""
    ╔════════════════════════════════════════════╗
    ║     JobStreet Indonesia Job Scraper        ║
    ╚════════════════════════════════════════════╝
    """)

    print(f"Keywords: {KEYWORDS}")
    print(f"Pages per keyword: {PAGES_PER_KEYWORD}")
    print(f"Estimasi: ~{len(KEYWORDS) * PAGES_PER_KEYWORD * 30} jobs\n")

    # Cek first run
    first_run = not os.path.exists(os.path.expanduser("~/.jobstreet_profile"))

    if first_run:
        print("="*50)
        print("FIRST RUN - Login akan disimpan untuk next run")
        print("="*50)

    # Mulai scraping
    scraper = JobStreetScraper()

    try:
        scraper.start_browser()

        # First run: buka homepage dulu untuk login
        if first_run:
            print("\n1. Browser akan buka JobStreet")
            print("2. Jika ada popup login, silakan LOGIN")
            print("3. Tekan ENTER di terminal setelah selesai\n")
            scraper.driver.get("https://id.jobstreet.com")
            time.sleep(2)
            input("Tekan ENTER untuk mulai scraping...")

        # Scrape
        jobs = scraper.scrape_all(KEYWORDS, PAGES_PER_KEYWORD)

        # Save
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        scraper.save_to_csv(f"jobstreet_jobs_{timestamp}.csv")
        scraper.save_to_json(f"jobstreet_jobs_{timestamp}.json")

        # Stats
        scraper.show_stats()

    except KeyboardInterrupt:
        print("\n\nStopped! Saving collected data...")
        if scraper.all_jobs:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            scraper.save_to_csv(f"jobstreet_partial_{timestamp}.csv")

    except Exception as e:
        print(f"\nError: {e}")

    finally:
        scraper.close_browser()

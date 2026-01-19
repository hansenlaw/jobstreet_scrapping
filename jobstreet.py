# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# import time

# # Setup ChromeDriver
# driver = webdriver.Chrome()

# # Buka halaman JobStreet dengan keyword "data"
# url = "https://www.jobstreet.co.id/id/job-search/data-jobs/"
# driver.get(url)

# # Tunggu load
# time.sleep(5)

# # Temukan semua elemen article yang mewakili job card
# job_cards = driver.find_elements(By.XPATH, "//article[contains(@class, 'gg45di0')]")

# # Loop setiap job card
# for card in job_cards:
#     try:
#         title = card.find_element(By.XPATH, ".//a[contains(@data-testid, 'job-card-title')]").text
#     except:
#         title = "Title not found"
    
#     try:
#         company = card.find_element(By.XPATH, ".//a[contains(@data-automation, 'jobCompany')]").text
#     except:
#         company = "Company not found"

#     try:
#         location = card.find_element(By.XPATH, ".//a[contains(@class, 'gg45di0 gg45dif  gg45di0 gg45dif qqxpw20 qqxpw22')]").text
#     except:
#         location = "Location not found"

#     try:
#         salary = card.find_element(By.XPATH, ".//span[contains(@class, 'gg45di0 _1c7ocld2 _1ubeeig4z _1ubeeig0 _1ubeeigr _1c7ocld4')]").text
#     except:
#         salary = "Salary not found"

#     try:
#         date = card.find_element(By.XPATH, ".//span[contains(@data-automation, 'jobListingDate')]").text
#     except:
#         date = "Date not found"
    
#     print(f"Title: {title}")
#     print(f"Company: {company}")
#     print(f"Location: {location}")
#     print(f"Salary: {salary}")
#     print(f"Date: {date}")

#     print("-" * 40)

# # Tutup browser
# driver.quit()


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import polars as pl

# Setup ChromeDriver
driver = webdriver.Chrome()

# Buka halaman JobStreet dengan keyword "data"
url = "https://www.jobstreet.co.id/id/job-search/data-jobs/"
driver.get(url)

# Tunggu halaman awal load
time.sleep(5)

# Melacak data yang sudah disimpan agar tidak duplikat
seen_jobs = set()
job_data = []

# Loop untuk 10 halaman
for page in range(10):
    print(f"🔍 Scraping halaman {page + 1}...")
    time.sleep(5)  # beri waktu untuk load konten tiap halaman

    # Temukan semua elemen article yang mewakili job card
    job_cards = driver.find_elements(By.XPATH, "//article[contains(@class, 'gg45di0')]")

    # Loop setiap job card
    for card in job_cards:
        try:
            title = card.find_element(By.XPATH, ".//a[contains(@data-testid, 'job-card-title')]").text
        except:
            title = "Title not found"
        
        try:
            company = card.find_element(By.XPATH, ".//a[contains(@data-automation, 'jobCompany')]").text
        except:
            company = "Company not found"

        try:
            location = card.find_element(By.XPATH, ".//a[contains(@class, 'gg45di0 gg45dif  gg45di0 gg45dif qqxpw20 qqxpw22')]").text
        except:
            location = "Location not found"

        try:
            salary = card.find_element(By.XPATH, ".//span[contains(@class, 'gg45di0 _1c7ocld2 _1ubeeig4z _1ubeeig0 _1ubeeigr _1c7ocld4')]").text
        except:
            salary = "Salary not found"

        try:
            date = card.find_element(By.XPATH, ".//span[contains(@data-automation, 'jobListingDate')]").text
        except:
            date = "Date not found"
        
        # Gunakan title + company + date sebagai identitas unik
        job_id = (title, company, date)

        if job_id not in seen_jobs:
            seen_jobs.add(job_id)
            job_data.append({
                "Title": title,
                "Company": company,
                "Location": location,
                "Salary": salary,
                "Date": date
            })
            print(f"✅ {title} | {company}")
        else:
            print(f"⚠️ [Duplikat] {title} - {company} ({date})")

    # Klik tombol "Next"
    try:
        next_button = driver.find_element(By.XPATH, "//a[@title='Selanjutnya']").click()
    except:
        print("⛔ Tidak ada halaman berikutnya. Berhenti.")
        break

# Tutup browser
driver.quit()

# Simpan ke file CSV menggunakan Polars
df = pl.DataFrame(job_data)
df.write_csv("jobstreet_scraped_data.csv")
print("\n✅ Data scraping selesai dan disimpan ke 'jobstreet_scraped_data.csv'")

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# تابع برای جمع‌آوری لینک مقالات در صفحه جاری
def scrape_links(driver):
    links = []
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a.fw-bold"))
        )
        articles = driver.find_elements(By.CSS_SELECTOR, "a.fw-bold")
        for article in articles:
            href = article.get_attribute('href')
            if href:
                links.append(href)
    except Exception as e:
        print(f"Error scraping links: {e}")
    return links

# تابع برای حرکت به صفحه بعد
def go_to_next_page(driver):
    try:
        next_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'Pagination_arrow_next')]"))
        )
        driver.execute_script("arguments[0].click();", next_button)
        time.sleep(5)
        return True
    except Exception as e:
        print(f"Could not navigate to the next page: {e}")
        return False

# تابع اصلی
def main(url, output_file, max_pages=10):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)

    all_links = []

    try:
        for page in range(max_pages):
            print(f"Scraping page {page + 1}...")

            # استخراج لینک‌ها از صفحه جاری
            links = scrape_links(driver)
            print(f"Found {len(links)} links on page {page + 1}.")
            all_links.extend(links)

            # حرکت به صفحه بعد
            if not go_to_next_page(driver):
                print("No more pages or navigation failed.")
                break

        # ذخیره داده‌ها در فایل اکسل
        if all_links:
            df = pd.DataFrame({"Article Link": all_links})
            df.to_excel(output_file, index=False)
            print(f"Scraping completed. Data saved to {output_file}")
        else:
            print("No links were scraped.")
    except Exception as e:
        print(f"Error during scraping: {e}")
    finally:
        driver.quit()

# اجرای کد
if __name__ == "__main__":
    start_url = "https://ieeexplore.ieee.org/search/searchresult.jsp?queryText=Power%20Engineering&highlight=true&returnType=SEARCH&matchPubs=true&refinements=ContentType:Journals&returnFacets=ALL&ranges=2020_2022_Year"
    output_excel = "scraped_links_Power_Engineering.xlsx"
    main(start_url, output_excel, max_pages=10)

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import openpyxl
import time
from webdriver_manager.chrome import ChromeDriverManager

# تنظیمات مرورگر
def get_driver():
    options = Options()
   # options.add_argument('--headless')  # اجرای بدون باز شدن مرورگر
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('window-size=1200x600')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

# خواندن لینک‌ها از فایل اکسل
def read_links_from_excel(file_name):
    workbook = openpyxl.load_workbook(file_name)
    sheet = workbook.active
    links = [cell.value for cell in sheet['A'] if cell.value]  # ستون A شامل لینک‌ها
    return links

# استخراج اطلاعات مقاله با Selenium و BeautifulSoup
def get_article_data(driver, url):
    driver.get(url)

    # انتظار برای بارگذاری عنوان
    try:
        WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'h1.document-title.text-2xl-md-lh span')))
    except Exception as e:
        print(f"خطا در بارگذاری {url}: {e}")
        return {}

    # استفاده از BeautifulSoup برای تحلیل HTML صفحه
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # استخراج عنوان
    title_element = soup.select_one('h1.document-title.text-2xl-md-lh span')
    title = title_element.text.strip() if title_element else 'عنوان یافت نشد'

    # استخراج نام نویسندگان
    authors = [author.text.strip() for author in soup.select('span.authors-info span.blue-tooltip a')]

    # استخراج چکیده
    #abstract_element = soup.select_one('div[_ngcontent-kko-c175][xplmathjax]')
    #abstract = abstract_element.text.strip() if abstract_element else 'چکیده یافت نشد'
    # استخراج چکیده
    # استخراج چکیده
    abstract_element = soup.find('div', attrs={'xplmathjax': True})  # یافتن <div> با ویژگی xplmathjax
    abstract = abstract_element.text.strip() if abstract_element else 'چکیده یافت نشد'


    # استخراج نام ژورنال
    journal_element = soup.select_one('div.stats-document-abstract-publishedIn a.stats-document-abstract-publishedIn')
    journal_name = journal_element.text.strip() if journal_element else 'ژورنال یافت نشد'

    # استخراج تاریخ انتشار
    pub_date_element = soup.select_one('div.doc-abstract-pubdate')
    pub_date_text = pub_date_element.text.replace("Date of Publication", "").strip() if pub_date_element else 'تاریخ انتشار یافت نشد'

    return {
        'title': title,
        'authors': authors,  # لیست نویسندگان
        'abstract': abstract,
        'journal_name': journal_name,
        'year': pub_date_text,
    }

# ذخیره داده‌ها در فایل اکسل جدید
def save_to_excel(data, file_name='out_scraped_links_Power_Engineering.xlsx'):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Article Data"

    # نوشتن عنوان ستون‌ها
    sheet.append(["Link", "Title", "Journal Name", "Year", "Abstract"] + [f"Author {i+1}" for i in range(10)])  # اضافه کردن لینک به عنوان اولین ستون

    # افزودن داده‌ها
    for article in data:
        link = article.get('link', 'لینک یافت نشد')  # لینک ورودی
        title = article.get('title', 'عنوان یافت نشد')
        journal_name = article.get('journal_name', 'ژورنال یافت نشد')
        year = article.get('year', 'سال انتشار یافت نشد')
        abstract = article.get('abstract', 'چکیده یافت نشد')
        authors = article.get('authors', [])
# افزودن نویسندگان به سلول‌های جداگانه
        row = [link, title, journal_name, year, abstract] + authors + [''] * (10 - len(authors))  # پر کردن سلول‌های خالی در صورت نیاز
        sheet.append(row)

    workbook.save(file_name)
    print(f"Data saved to {file_name}")

# اجرای کد
input_file = "scraped_links_Power_Engineering.xlsx"  # فایل لینک‌های ورودی
links = read_links_from_excel(input_file)

# بارگذاری مرورگر و استخراج داده‌ها
driver = get_driver()
all_articles_data = []
for link in links:
    try:
        data = get_article_data(driver, link)
        if data:
            data['link'] = link  # اضافه کردن لینک به داده‌های استخراج شده
            all_articles_data.append(data)
    except Exception as e:
        print(f"خطا در پردازش لینک {link}: {e}")
driver.quit()

# ذخیره داده‌ها در فایل اکسل
save_to_excel(all_articles_data)
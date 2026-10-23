
# Detection of AI-Generated Scientific Abstracts Using Linguistic Features and Machine Learning

## Project Overview

This project investigates the classification of scientific abstracts into three categories:

- Human-written
- AI-generated (GPT-3.5)
- AI-paraphrased

The research explores linguistic features and machine learning approaches, including DistilBERT, to distinguish between human-written and AI-generated scientific text.

## Data Collection

The initial data collection workflow was developed in Python using Selenium and pandas.

The script was designed to collect article links from IEEE Xplore search result pages based on manually specified research topics and search filters.

### Search Configuration

- Source: IEEE Xplore
- Content type: Journals
- Publication years: 2020–2022
- Search topics: Approximately 100 manually specified topics
- Example query: Power Engineering
- Maximum pages per execution: 10
- Output format: Excel (.xlsx)

### Data Collection Workflow

1. Configure a search URL for a research topic.
2. Open the search results page using Selenium and Chrome.
3. Extract article links from the current page.
4. Navigate through subsequent result pages.
5. Save the collected links to an Excel file.

### Tools and Libraries

- Python
- Selenium
- pandas
- Chrome WebDriver
- webdriver-manager
- openpyxl (if used by the Excel export environment)

  ## Article Metadata and Abstract Extraction

After collecting article URLs, a second Python script was developed to extract article information from individual IEEE Xplore pages.

### Extracted Fields

The script attempts to collect the following information for each article:

- **Link:** Original article URL
- **Title:** Article title
- **Authors:** Names of the listed authors
- **Journal Name:** Name of the journal
- **Publication Date:** Publication date displayed on the article page
- **Abstract:** Scientific abstract

### Extraction Workflow

1. Read article URLs from an Excel file using `openpyxl`.
2. Open each article page using Selenium WebDriver.
3. Wait for the article title element to become visible.
4. Parse the loaded HTML using BeautifulSoup.
5. Extract the available metadata and abstract.
6. Store each article's information in a structured Excel file, with separate columns for the URL, title, journal, publication date, abstract, and up to ten author fields.

### Tools and Libraries

- Python
- Selenium
- BeautifulSoup
- openpyxl
- Chrome WebDriver
- webdriver-manager

### Output

The script saves the extracted records to an Excel workbook named `out_scraped_links_Power_Engineering.xlsx` by default.

The extraction process depends on the page structure and HTML selectors used by IEEE Xplore. Missing fields are assigned fallback text, such as "Abstract not found," when the corresponding element cannot be located.


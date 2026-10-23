
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

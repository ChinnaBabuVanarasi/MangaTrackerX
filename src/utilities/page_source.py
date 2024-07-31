import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def get_page_source(manga_url):
    time.sleep(5)
    # print(manga_url)
    options = Options()
    options.add_argument("--headless")
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/58.0.3029.110 Safari/537")
    driver = webdriver.Chrome(options=options)
    driver.get(manga_url)
    content = driver.page_source
    soup = BeautifulSoup(content, "html.parser")

    return soup


def get_date_added():
    current_datetime = datetime.now()
    return datetime(current_datetime.year,
                    current_datetime.month,
                    current_datetime.day
                    )

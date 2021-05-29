from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import re

def crawling(keyword, numberOfvideos):
    print("Let's crawling!")
    keyword = keyword
    numberOfvideos = numberOfvideos
    urls = []

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome('chromedriver', chrome_options=chrome_options)

    address = [
        'https://www.youtube.com/results?search_query={}&sp=EgQQARgD',
        'https://www.youtube.com/results?search_query={}&sp=EgQQARgB'
    ]

    for i in address:
        driver.get(i.format(keyword))
        # WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input#search"))).send_keys("야구공")
        # driver.find_element_by_css_selector("button.style-scope.ytd-searchbox#search-icon-legacy").click()

        # while True:
        for i in range(numberOfvideos):
            scroll_height = 1000
            document_height_before = driver.execute_script("return document.documentElement.scrollHeight")
            driver.execute_script(f"window.scrollTo(0, {document_height_before + scroll_height});")
            time.sleep(1.3)
            document_height_after = driver.execute_script("return document.documentElement.scrollHeight")
            if document_height_after == document_height_before:
                break

        for my_href in WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "a.yt-simple-endpoint.style-scope.ytd-video-renderer#video-title"))):
            urls.append(re.sub("https://www\.youtube\.com/watch\?v=", "", my_href.get_attribute("href")))
    
    driver.close()
    print("총 영상 수: {}".format(len(urls)))
    return urls








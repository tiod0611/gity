from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import re

def crawling(keyword, numberOfvideos):

    keyword = keyword
    numberOfvideos = numberOfvideos
    urls = []

    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")

    driver_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chromedriver.exe")
    driver=webdriver.Chrome(chrome_options=options, executable_path=driver_path)
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
    return urls








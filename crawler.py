# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# import time


# driver = webdriver.Chrome()
# keyword = '야구'
# url = 'https://www.youtube.com/results?search_query=' + keyword
# driver.get(url)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
driver=webdriver.Chrome(chrome_options=options, executable_path=r'C:\pycode\project\gity\chromedriver.exe')
driver.get("https://www.youtube.com/")
WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input#search"))).send_keys("야구공")
driver.find_element_by_css_selector("button.style-scope.ytd-searchbox#search-icon-legacy").click()
print([my_href.get_attribute("href") for my_href in WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "a.yt-simple-endpoint.style-scope.ytd-video-renderer#video-title")))])
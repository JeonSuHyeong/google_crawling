import os
import urllib
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# 폴더 생성

keyword = "도서관"

if not os.path.exists(keyword):
    os.makedirs(keyword)

query = keyword

url = f"https://www.google.com/search?q={query}&tbm=isch"
driver = webdriver.Chrome()
driver.get(url)

SCROLL_PAUSE_TIME = 1
# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

new_height = 0

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Wait to load page
    sleep(SCROLL_PAUSE_TIME)
    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        try:
            # 결과 더보기 버튼이 나타날 때까지 대기
            more_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".mye4qd"))
            )
            more_button.click()
            sleep(2)
        except:
            break
    last_height = new_height

img_elements = driver.find_elements(By.CSS_SELECTOR,".rg_i")

for i, img in enumerate(img_elements):
    print(f"{query} : {i+1}/{len(img_elements)} proceed...")
    try:
        image_xpath = f'//*[@id="islrg"]/div[1]/div[{i+1}]/a[1]/div[1]/img'

        image_element = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.XPATH, image_xpath))
        )
        image_element = driver.find_element(By.XPATH,image_xpath)
        image_url = str(image_element.get_attribute("src"))
        urllib.request.urlretrieve(image_url, str(f"{keyword}/library_han_{i}.jpg"))
        sleep(1)
        print(f"img {i} done")
    except:
        print(f"error {i}")
        print(type(image_element))
        print(type(image_url))
        sleep(0.5)


# 웹 드라이버 종료
driver.quit()

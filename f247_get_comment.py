from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import json
from selenium.common.exceptions import NoSuchElementException
# Configure Chrome options
chrome_options = ChromeOptions()
# Run Chrome in headless mode (no GUI)
chrome_options.add_argument("--headless")

user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
chrome_options.add_argument(f'user-agent={user_agent}')
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# Set up the Chrome web driver
driver_test = webdriver.Chrome(service=ChromeService(
    "./chromedriver.exe"), options=chrome_options)

def get_comment(driver, link):
    driver.get(link)
    # searchs = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'post-stream')))
    wait = WebDriverWait(driver, 10)
    try:
        searchs = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'post-stream')))
        label = searchs.find_elements(By.CLASS_NAME, "stats_label")
        label_comment = int(label[1].text)
        label_comment += 1
    except TimeoutException:
        # Handle the case where the 'post-stream' element is not found within the specified time
        print("Timeout: 'post-stream' element not found. Exiting function.")
        return {}
    current_i = 1
    data_comment = []
    # SCROLL_PAUSE_TIME = 1
    # last_height = driver.execute_script("return document.body.scrollHeight")
    # print(last_height)
    # while True:
    #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #     time.sleep(SCROLL_PAUSE_TIME)
    #     new_height = driver.execute_script("return document.body.scrollHeight")
    #     if new_height == last_height:
    #         break
    #     last_height = new_height
    while True:
        for _ in range(1,21):
            try:
                if current_i > label_comment:
                    break
                comment = searchs.find_element(By.ID, f"post_{current_i}")
                comment_data = {
                    "user_href": comment.find_element(By.CLASS_NAME, "main-avatar").get_attribute("href"),
                    "username": comment.find_element(By.CLASS_NAME, "username").text,
                    "react": comment.find_element(By.CLASS_NAME, 'like_count').text,
                    "badge": comment.find_element(By.CLASS_NAME, 'custom_badge').text,
                }
                cooked_element = comment.find_element(By.CLASS_NAME, 'cooked')
                if cooked_element.text:
                    comment_data["content"] = cooked_element.text
                else:
                    comment_data["content"] = ""
                data_comment.append(comment_data)
                print("comment " + str(current_i))
                current_i += 1
            except NoSuchElementException:
                print(f"Element with ID 'post_{current_i}' not found. Skipping.")
                current_i += 1
            if current_i > label_comment:
                break
        
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        if current_i > label_comment:
            break
    data_comment.reverse()
    driver.quit()
    return data_comment


# get_comment(driver_test, "https://f247.com/t/tam-dong-anv-co-hoi-nao-cho-co-phieu-thuy-san-trong-6-thang-cuoi-nam-2023-hen-thang-10-quay-lai/")
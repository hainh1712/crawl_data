from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
from selenium.common.exceptions import NoSuchElementException
# Configure Chrome options
chrome_options = ChromeOptions()
# Run Chrome in headless mode (no GUI)
# chrome_options.add_argument("--headless")

user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
chrome_options.add_argument(f'user-agent={user_agent}')
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# Set up the Chrome web driver
# driver = webdriver.Chrome(service=ChromeService(
#     "./chromedriver.exe"), options=chrome_options)

def get_comment(driver, link):
    # url = f"https://f247.com/t/phan-tich-co-phieu-nhua-aaa/153640"
    driver.get(link)
    time.sleep(4)
    searchs = driver.find_element(By.CLASS_NAME, 'post-stream')
    label = searchs.find_elements(By.CLASS_NAME, "stats_label")
    label_comment = int(label[1].text)
    label_comment += 1
    current_i = 1
    data_comment = []
    while True:
        # Lấy chiều cao của trang web
        # page_height = driver.execute_script("return document.body.scrollHeight")

        # # Cuộn xuống đáy trang web
        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # time.sleep(2)

        # # Lấy lại chiều cao mới của trang web sau khi cuộn
        # new_page_height = driver.execute_script("return document.body.scrollHeight")

        # # Kiểm tra xem trang web đã cuộn xuống đáy chưa
        # if new_page_height == page_height:
        #     break
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
                print(current_i)
                current_i += 1
            except NoSuchElementException:
                # If the element is not found, print a message and move to the next iteration
                print(f"Element with ID 'post_{current_i}' not found. Skipping.")
                current_i += 1

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        if current_i == label_comment:
            break
    data_comment.reverse()
    # with open("data_comment.json", "w") as file:
    #     json.dump(data_comment, file, indent=2)

        # Kiểm tra xem trang web đã cuộn xuống đáy chưa
        # if new_page_height == page_height:
        #     break
    driver.quit()
    return data_comment



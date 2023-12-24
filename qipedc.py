from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
import time
import csv
# Configure Chrome options
chrome_options = ChromeOptions()
# Run Chrome in headless mode (no GUI)
# chrome_options.add_argument("--headless=new")

user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
chrome_options.add_argument(f'user-agent={user_agent}')
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

csv_filename = "data_qipedc.csv"
with open(csv_filename, mode="w", encoding="utf-8-sig", newline="") as csv_file:
    fieldnames = ["word", "url_video"]
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()

url = f"https://qipedc.moet.gov.vn/dictionary?fbclid=IwAR3yzUrTYUiAfoPD9za0TFIhyLD0Alq1vhaJFi1ReA2lout3atLSV9I2NjY"

driver = webdriver.Chrome(service=ChromeService("./chromedriver.exe"), options=chrome_options)
driver.get(url)
time.sleep(5)
pagination_wrapper = driver.find_element(By.ID, "pagination-wrapper")
buttons = pagination_wrapper.find_elements(By.CLASS_NAME, "page")
last_button = buttons[-1]
last_value = last_button.get_attribute("value")
current_page = 1
while True:
    product_list = driver.find_element(By.ID, "product")
    words = product_list.find_elements(By.TAG_NAME, "a")
    for word in words:
        print(f"Đang ở trang {current_page}")
        word_symbol = word.find_element(By.CLASS_NAME, "f-f-Lato-Black").text
        # get url_video
        src_vid = word.find_element(By.TAG_NAME, "img").get_attribute("src")
        parts = src_vid.split("/")[-1].split(".")[0]
        link_url = "https://qipedc.moet.gov.vn/videos/" + parts +".mp4?autoplay=true"
        print("============")
        print(word_symbol)
        with open(csv_filename, mode="a", encoding="utf-8-sig", newline="") as csv_file:
            fieldnames = ["word", "url_video"]
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            csv_writer.writerow({
                "word": word_symbol,
                "url_video": link_url
            })
    if current_page == int(last_value):
        break
    current_page += 1
    next_button = pagination_wrapper.find_element(By.XPATH, f'//button[@value="{current_page}"]')
    next_button.click()
    time.sleep(1)

driver.quit()
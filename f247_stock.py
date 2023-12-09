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
from f247_get_comment import get_comment
# from test import get_comment
# Configure Chrome options
chrome_options = ChromeOptions()
# Run Chrome in headless mode (no GUI)
# chrome_options.add_argument("--headless")

user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
chrome_options.add_argument(f'user-agent={user_agent}')
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# driver = webdriver.Chrome(service=ChromeService(
#     "./chromedriver.exe"), options=chrome_options)

with open("list_stocks.json", "r") as file:
    stocks_data = json.load(file)

def f247():
    data = []
    data_href = []
    for symbol in stocks_data:
        driver = webdriver.Chrome(service=ChromeService("./chromedriver.exe"), options=chrome_options)
        print(symbol)
        url = f"https://f247.com/tag/{symbol}"
        driver.get(url)
        time.sleep(2) 
        max_scroll_iterations = 10

        scroll_iterations = 0
        wait = WebDriverWait(driver, 10)
        try:
            searchs = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'tbody')))
        except TimeoutException:
            print("Timeout: 't-body' element not found. Exiting function.")
            continue
        while True:
            # driver.execute_script(f"window.scrollBy(0, {window_height});")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            scroll_iterations += 1
            page_height = driver.execute_script("return document.body.scrollHeight")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            new_page_height = driver.execute_script("return document.body.scrollHeight")
            if new_page_height == page_height or scroll_iterations > max_scroll_iterations:
                break
            
        post_child = searchs.find_elements(By.CLASS_NAME, "raw-topic-link")
        for link in post_child:
            href = link.get_attribute("href")
            print(href)
            data_href.append(href)
    with open("data_href.json", "w") as file:
        json.dump(data_href, file, indent=2)
        driver.close()
    #     search = searchs.find_elements(By.CLASS_NAME, "topic-list-item")   
    #     for search_element in search:
    #         href = search_element.find_element(By.CLASS_NAME, "raw-topic-link").get_attribute("href")
    #         data_href.append(href)
    #         infomation = {
    #             "type": "f247",
    #             "stock_name": symbol,
    #             "href": href,
    #             "author_href": search_element.find_element(By.CLASS_NAME, "topic-author-avatar").find_element(By.TAG_NAME, "a").get_attribute("href"),
    #             "title": search_element.find_element(By.CLASS_NAME, "raw-topic-link").text,
    #             "author_name": search_element.find_element(By.CLASS_NAME, "topic-user-create-info").find_element(By.TAG_NAME, 'a').text,
    #             "date": search_element.find_element(By.CLASS_NAME, "relative-date").text,
    #             "category": search_element.find_element(By.CLASS_NAME, "category-name").text,
    #             "discourse-tags": [],    
    #         }
    #         tags = search_element.find_elements(By.CLASS_NAME, "discourse-tag")
    #         for tag in tags:
    #             infomation["discourse-tags"].append(tag.text)
    #         print("=====================================")
    #         print(href)
    #         driver_href = webdriver.Chrome(service=ChromeService("./chromedriver.exe"), options=chrome_options)
    #         infomation_comment = get_comment(driver_href, href)
    #         # driver_href.close()
    #         infomation["comment"] = infomation_comment

    #         data.append(infomation)
    # with open("data_stock_f247.json", "w") as file:
    #     json.dump(data, file, indent=2)
        
f247()
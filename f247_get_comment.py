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
import csv
# Configure Chrome options
chrome_options = ChromeOptions()
# Run Chrome in headless mode (no GUI)
chrome_options.add_argument("--headless=new")

user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
chrome_options.add_argument(f'user-agent={user_agent}')
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# Set up the Chrome web driver
with open("stock_link_error.csv", mode="w", encoding="utf-8-sig", newline="") as csv_file:
    fieldnames = ["link_error"]
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()

csv_filename = "data_stock_f247.csv"
# with open(csv_filename, mode="w", encoding="utf-8-sig", newline="") as csv_file:
#     fieldnames = ["post_title", "post_category", "post_tags",
#                     "user_post", "date_post", "react_post", "badge_post", "content_post", 
#                     "user_comment", "date_comment", "react_comment", "badge_comment", "content_comment"]
#     csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
#     csv_writer.writeheader()

def get_comment(url):
    # url = f"https://f247.com/t/gia-nhua-dau-vao-giam-co-phieu-nao-huong-loi/494297"
    print(url)
    driver = webdriver.Chrome(service=ChromeService("./chromedriver"), options=chrome_options)
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    try:
        intro_post = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'title-wrapper')))
        searchs = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'post-stream')))
        label = searchs.find_elements(By.CLASS_NAME, "stats_label")
        if len(label) == 2:
            label_comment = int(label[1].text)
            label_comment += 1
        else:
            print("Error: Not enough elements in the 'label' list.")
            with open(csv_filename, mode="a", encoding="utf-8-sig", newline="") as csv_file:
                fieldnames = ["link_error"]
                csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                csv_writer.writerow({
                    "link_error": url
                })
            return  {}
    except TimeoutException:
        print("Timeout: 'post-stream' element not found. Exiting function.")
        with open(csv_filename, mode="a", encoding="utf-8-sig", newline="") as csv_file:
            fieldnames = ["link_error"]
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            csv_writer.writerow({
                "link_error": url
            })
        return {}
    general_post = {
        "title": intro_post.find_element(By.CLASS_NAME, "fancy-title").text.encode().decode('utf-8'),
        "category": intro_post.find_element(By.CLASS_NAME, "category-name").text.encode().decode('utf-8'),
        "discourse-tags": [], 
    }
    tags = intro_post.find_elements(By.CLASS_NAME, "discourse-tag")
    for tag in tags:
        general_post["discourse-tags"].append(tag.text)
    post = searchs.find_element(By.ID, f"post_1")
    data_post = {
        "user": post.find_element(By.CLASS_NAME, "username").text,
        "date": post.find_element(By.CLASS_NAME, "relative-date").text,
        "react": post.find_element(By.CLASS_NAME, 'like_count').text,
        "badge": post.find_element(By.CLASS_NAME, 'custom_badge').text.encode().decode('utf-8'),
        "content": post.find_element(By.CLASS_NAME, 'cooked').text.encode().decode('utf-8')
    }
    current_i = 2
    data_comment = []
    while True:
        for _ in range(2,20):
            page_height = driver.execute_script("return document.body.scrollHeight")
            try:
                comment = searchs.find_element(By.ID, f"post_{current_i}")
                comment_data = {
                    "user": comment.find_element(By.CLASS_NAME, "username").text,
                    "date": comment.find_element(By.CLASS_NAME, "relative-date").text,
                    "react": comment.find_element(By.CLASS_NAME, 'like_count').text,
                    "badge": comment.find_element(By.CLASS_NAME, 'custom_badge').text.encode().decode('utf-8'),
                }
                cooked_element = comment.find_element(By.CLASS_NAME, 'cooked')
                if cooked_element.text:
                    comment_data["content"] = cooked_element.text.encode().decode('utf-8')
                else:
                    comment_data["content"] = ""
                print("comment " + str(current_i))
                current_i += 1
                with open(csv_filename, mode="a", encoding="utf-8-sig", newline="") as csv_file:
                    fieldnames = ["post_title", "post_category", "post_tags",
                                    "user_post", "date_post", "react_post", "badge_post", "content_post", 
                                    "user_comment", "date_comment", "react_comment", "badge_comment", "content_comment"]
                    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                    csv_writer.writerow({
                        "post_title": general_post["title"],
                        "post_category": general_post["category"],
                        "post_tags": general_post["discourse-tags"],
                        "user_post": data_post["user"],
                        "date_post": data_post["date"],
                        "react_post": data_post["react"],
                        "badge_post": data_post["badge"],
                        "content_post": data_post["content"],
                        "user_comment": comment_data["user"],
                        "date_comment": comment_data["date"],
                        "react_comment": comment_data["react"],
                        "badge_comment": comment_data["badge"],
                        "content_comment": comment_data["content"],
                    })
            except NoSuchElementException:
                print(f"Element with ID 'post_{current_i}' not found. Skipping.")
                current_i += 1
            # if current_i > label_comment:
            #     break
        
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        new_page_height = driver.execute_script("return document.body.scrollHeight")
        if new_page_height == page_height:
            break
    data_comment.reverse()
    driver.quit()
    
with open("post_href_error.csv", "r", newline="", encoding="utf-8") as file:
    data_href = csv.reader(file)
    next(data_href)  
    for row in data_href:
        post_href = row[0]  
        if not any(row):
            break
        get_comment(post_href)





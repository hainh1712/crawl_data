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
from pymongo import MongoClient
# Configure Chrome options
chrome_options = ChromeOptions()
# Run Chrome in headless mode (no GUI)
chrome_options.add_argument("--headless=new")

user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
chrome_options.add_argument(f'user-agent={user_agent}')
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# Set up the Chrome web driver

# csv_filename = "data_stock_f247.csv"
# with open(csv_filename, mode="w", encoding="utf-8-sig", newline="") as csv_file:
#     fieldnames = ["post_title", "post_category", "post_tags",
#                     "user_post", "date_post", "react_post", "badge_post", "content_post", 
#                     "user_comment", "date_comment", "react_comment", "badge_comment", "content_comment"]
#     csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
#     csv_writer.writeheader()

def get_comment(url, stock_tag):
    # url = f"https://f247.com/t/gia-nhua-dau-vao-giam-co-phieu-nao-huong-loi/494297"
    print(url)
    driver = webdriver.Chrome(service=ChromeService("./chromedriver.exe"), options=chrome_options)
    driver.get(url)
    wait = WebDriverWait(driver, 6)
    try:
        intro_post = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'title-wrapper')))
        searchs = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'post-stream')))
        label = searchs.find_elements(By.CLASS_NAME, "stats_label")
        if len(label) == 2:
            label_comment = int(label[1].text)
            label_comment += 1
        else:
            print("Error: Not enough elements in the 'label' list.")
            return  {}
    except TimeoutException:
        print("Timeout: 'post-stream' element not found. Exiting function.")
        return {}
    general_post = {
        "title_post": intro_post.find_element(By.CLASS_NAME, "fancy-title").text.encode().decode('utf-8'),
        "category_post": intro_post.find_element(By.CLASS_NAME, "category-name").text.encode().decode('utf-8'),
        "discourse-tags_post": [], 
    }
    tags = intro_post.find_elements(By.CLASS_NAME, "discourse-tag")
    for tag in tags:
        general_post["discourse-tags_post"].append(tag.text)
    post = searchs.find_element(By.ID, f"post_1")
    data_post = {
        "user_post": post.find_element(By.CLASS_NAME, "username").text,
        "date_post": post.find_element(By.CLASS_NAME, "relative-date").text,
        "react_post": post.find_element(By.CLASS_NAME, 'like_count').text,
        "badge_post": post.find_element(By.CLASS_NAME, 'custom_badge').text.encode().decode('utf-8'),
        "content_post": post.find_element(By.CLASS_NAME, 'cooked').text.encode().decode('utf-8')
    }
    data_each_post = {
        "post_title": general_post["title_post"],
        "post_category": general_post["category_post"],
        "post_tags": general_post["discourse-tags_post"],
        "post_user": data_post["user_post"],
        "post_date": data_post["date_post"],
        "post_react": data_post["react_post"],
        "post_badge": data_post["badge_post"],
        "post_content": data_post["content_post"],
        "comment": []
    }
    current_i = 2
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
                    if stock_tag.lower() in comment_data["content"].lower():
                        data_each_post["comment"].append(comment_data)
                else:
                    comment_data["content"] = ""
                print("comment " + str(current_i))
                current_i += 1
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
    try:
        with open(f'data/{stock_tag}.json', 'r', encoding='utf-8') as json_file:
            existing_data = json.load(json_file)
    except FileNotFoundError:
        existing_data = []
    existing_data.append(data_each_post)
    with open(f'data/{stock_tag}.json', 'w', encoding='utf-8') as json_file:
        json.dump(existing_data, json_file, ensure_ascii=False, indent=2)
    driver.quit()
    
with open("post_href_tag.csv", "r", newline="", encoding="utf-8") as file:
    data_href = csv.reader(file)
    next(data_href)  
    for row in data_href:
        post_href = row[0]  
        tag = row[1]
        if not any(row):
            break
        get_comment(post_href, tag)
    





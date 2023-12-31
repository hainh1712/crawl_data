from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
# Configure Chrome options
chrome_options = ChromeOptions()
# Run Chrome in headless mode (no GUI)
# chrome_options.add_argument("--headless")

user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
chrome_options.add_argument(f'user-agent={user_agent}')
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# Set up the Chrome web driver
driver = webdriver.Chrome(service=ChromeService(
    "./chromedriver.exe"), options=chrome_options)

# URL of the web page you want to scrape
def binance():
    url = f"https://www.binance.com/en/blog/nft"
    driver.get(url)
    time.sleep(2)
    # Define the scroll amount and duration for smooth scrolling
    scroll_amount = 500  # Adjust this value as needed
    scroll_duration = 0.0001  # Adjust this value as needed
    # scroll_iterations = 5
    # Get the initial height of the page
    initial_height = driver.execute_script("return window.scrollY")
    while True:
        # Scroll down by the defined scroll amount
        driver.execute_script(f"window.scrollBy(0, {scroll_amount});")

        # Wait for a short duration to create a smooth scrolling effect
        time.sleep(scroll_duration)

        # Get the new scroll position
        new_height = driver.execute_script("return window.scrollY")

        # If no further scrolling is possible, break out of the loop
        if new_height == initial_height:
            break

        # Update the initial height
        initial_height = new_height
    posts = driver.find_element(By.CLASS_NAME, "css-1engawx")
    post_elements = posts.find_elements(By.TAG_NAME, "a")
    articles_list = []
    for article_element in post_elements:
        href = article_element.get_attribute("href")
        article = {
            "type": "binance",
            "post_title": article_element.find_element(By.CLASS_NAME, "carousel-card-title").text,
            "post_content": article_element.find_element(By.CLASS_NAME, "carousel-card-content").text,
            "post_date": article_element.find_element(By.CLASS_NAME, "carousel-card-date").text,
            "post_tags": "",
            "post_length": "",
            "post_link": href,
        } 
        driver.execute_script("window.open('" + href + "', '_blank');")

        driver.switch_to.window(driver.window_handles[-1])
        article_child = {
            "post_author": "",
            "post_description": driver.find_element(By.CLASS_NAME, "richtext-container").text,
            "post_image": []
        }
        images = driver.find_elements(By.TAG_NAME, "img")
        for image in images[1:-2]:
            src_value = image.get_attribute("src")
            article_child["post_image"].append(src_value)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        article.update(article_child)
        # article["binance"].update(article_child)
        articles_list.append(article)

    # with open("binance.json", "w") as outfile:
    #     json.dump(articles_list, outfile)
    try:
        with open("data.json", 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        # Nếu file không tồn tại, tạo một danh sách mới
        data = []
    data.extend(articles_list)
    with open("data.json", 'w') as file:
        json.dump(data, file, indent=2)

    driver.close()

binance()
    
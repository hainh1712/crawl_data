from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import argparse
from binance import binance
from rarible import rarible
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--binance", help="run binance", action="store_true")
    parser.add_argument("--rarible", help="run rarible", action="store_true")
    # parser.add_argument("crawlfile", type=str)

    args = parser.parse_args()
    # if args.crawlfile == "binance":
    #     binance()
    # else:
    #     rarible()
    if args.binance:
        binance()
    elif args.rarible:
        rarible()
    else:
        print("Please specify a valid option (--binance or --rarible)")
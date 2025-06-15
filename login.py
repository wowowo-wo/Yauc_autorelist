from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from chromedriver_py import binary_path
import pickle

options = Options()
options.add_argument('--user-data-dir=/tmp/chrome-profile')
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(service=Service(binary_path), options=options)

input("open chrome for log-in")
driver.get("https://auctions.yahoo.co.jp/")
input("press Enter after log-in")

with open("yahoo_cookies.pkl", "wb") as f:
    pickle.dump(driver.get_cookies(), f)

driver.quit()
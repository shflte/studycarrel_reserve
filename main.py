from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from dotenv import load_dotenv
import subprocess
import os
import time

from page_objects import LOGIN_PAGE
from login import login

load_dotenv()

chrome_driver_path = os.getenv("CHROME_DRIVER_PATH")
login_url = os.getenv("LOGIN_URL")
account = os.getenv("ACCOUNT")
password = os.getenv("PASSWORD")

if not chrome_driver_path:
    raise Exception("CHROME_DRIVER_PATH not set")

chrome_options = Options()
chrome_options.binary_location = chrome_driver_path

if os.getenv("HEADLESS") == "True":
    chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()

url = login_url
driver.get(url)
# wait for page to load 

login(driver, account, password)

while True:
    time.sleep(1)

driver.quit()
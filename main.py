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
from navigation import navigation
from date import select_date

load_dotenv()

chrome_driver_path = os.getenv("CHROME_DRIVER_PATH")
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

login(driver, account, password)
navigation(driver)
select_date(driver)
# select date
# choose time slots
# delete reservation

breakpoint()

driver.quit()

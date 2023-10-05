from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from dotenv import load_dotenv
import os

from login import login
from navigation import navigation
from date import select_date
from reserve import reserve

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

room = "201"
time_slots = [
    (3, 10),
    (11, 18),
    (19, 26)
]
return_status = []
for time_slot in time_slots:
    navigation(driver)
    select_date(driver)
    status = reserve(driver, room, time_slot)
    return_status.append(status)
    breakpoint()

print(return_status)

'''
status of reserving:
    success: 0
    reserved: -1
    not available: -2

delete reservation:
    success: 0
    error: -1
'''
# delete reservation

breakpoint()

driver.quit()

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from dotenv import load_dotenv
import os
import arrow

from login import login
from navigation import navigation
from date import select_date
from reserve import reserve
from cancel import cancel

'''
status of reserving:
    success: 0
    reserved: -1
    not available: -2

delete reservation:
    success: 0
    no reservation: 1
    no expiring reservation: 2
    unexpected error: -1
'''

def get_driver() -> webdriver.Chrome:
    chrome_options = Options()

    if os.getenv("HEADLESS") == "True":
        chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    return driver

def driver_login(driver: webdriver.Chrome):
    load_dotenv()

    account = os.getenv("ACCOUNT")
    password = os.getenv("PASSWORD")

    login(driver, account, password)

def reserve_carrel(room: str, date: arrow.arrow.Arrow, time_slots: tuple) -> list:
    driver = get_driver()
    driver_login(driver)

    return_status = []
    for time_slot in time_slots:
        navigation(driver)
        select_date(driver, date)
        status = reserve(driver, room, time_slot)
        return_status.append(status)

    driver.quit()
    return return_status

def cancel_reservation() -> int:
    driver = get_driver()
    driver_login(driver)

    status = cancel(driver)

    driver.quit()
    return status

if __name__ == "__main__":
    status = cancel_reservation()
    print(status)

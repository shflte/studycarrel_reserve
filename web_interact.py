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

def reserve_carrel(room: str, date: arrow.arrow.Arrow, time_slots: tuple) -> list:
    load_dotenv()

    account = os.getenv("ACCOUNT")
    password = os.getenv("PASSWORD")

    chrome_options = Options()

    if os.getenv("HEADLESS") == "True":
        chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()

    login(driver, account, password)

    return_status = []
    for time_slot in time_slots:
        navigation(driver)
        select_date(driver, date)
        status = reserve(driver, room, time_slot)
        return_status.append(status)

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
    # captcha retry

    driver.quit()
    return return_status

if __name__ == "__main__":
    room = "201"
    time_slots = [
        (3, 10),
        (11, 18),
        (19, 26)
    ]
    reserve_carrel(room, time_slots)

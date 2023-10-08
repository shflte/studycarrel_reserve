from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from dotenv import load_dotenv
import os
import arrow

from web_script.login import login
from web_script.navigation import navigation
from web_script.date import select_date
from web_script.reserve import reserve
from web_script.cancel import cancel
from web_script.reservation_table import reservation_table

'''
status of reserving:
    success: 0
    reserved: -1
    not available: -2
    limit exceeded: -3

delete reservation:
    success: 0
    no reservation: 1
    no expiring reservation: 2
    unexpected error: -1
'''

def get_driver() -> webdriver.Chrome:
    load_dotenv()
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

    logged_in = -1
    retry_count = 5
    while logged_in == -1 and retry_count > 0:
        logged_in = login(driver, account, password)
        retry_count -= 1
    
    if logged_in == -1:
        raise Exception("Login failed")

def reserve_carrel(room: str, date: arrow.arrow.Arrow, time_slot: float) -> int:
    load_dotenv()

    driver = get_driver()
    driver_login(driver)

    navigation(driver)
    select_date(driver, date)
    status = reserve(driver, room, time_slot)

    driver.quit()
    return status

def cancel_reservation() -> int:
    driver = get_driver()
    driver_login(driver)

    status = cancel(driver)

    driver.quit()
    return status

# return list of lists of string
def get_reservation_table() -> list:
    driver = get_driver()
    driver_login(driver)

    reservations = reservation_table(driver)

    driver.quit()
    return reservations

# if __name__ == "__main__":
#     status = cancel_reservation()
#     print(status)

if __name__ == "__main__":
    status = reserve_carrel("201", arrow.now().shift(days=0), 9.5)
    print(status)

# if __name__ == "__main__":
#     reservations = get_reservation_table()
#     print(reservations)

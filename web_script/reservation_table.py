from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from dotenv import load_dotenv
import os
import arrow
from web_script.page_objects import (
    RESERVED_LIST_PAGE
)

def reservation_table(driver: webdriver.Chrome) -> list:
    load_dotenv()
    reserve_url = os.getenv("RESERVE_URL")
    driver.get(reserve_url)

    iframe_element = driver.find_element(By.XPATH, RESERVED_LIST_PAGE.iframe)
    driver.switch_to.frame(iframe_element)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.XPATH, RESERVED_LIST_PAGE.reservation_list)))

    reservations = driver.find_elements(By.XPATH, RESERVED_LIST_PAGE.reservation_list)
    reservations = reservations[1:]

    table = []
    for i in range(len(reservations)):
        reservation = reservations[i]
        reservation_room_text = reservation.find_element(By.XPATH, RESERVED_LIST_PAGE.get_reserved_room_xpath(i + 2)).text
        reservation_time_text = reservation.find_element(By.XPATH, RESERVED_LIST_PAGE.get_reservation_time_xpath(i + 2)).text
        reservation_status_text = reservation.find_element(By.XPATH, RESERVED_LIST_PAGE.get_reservation_status_xpath(i + 2)).text
        tmp = [reservation_room_text, reservation_time_text, reservation_status_text]
        table.append(tmp)

    return table
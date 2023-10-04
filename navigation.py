from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from page_objects import (
    RESERVED_LIST_PAGE,
    RESERVE_RELATED_PAGE
)

from dotenv import load_dotenv
import time

def navigation(driver: webdriver.Chrome):
    wait = WebDriverWait(driver, 10)

    add_reservation_button = wait.until(EC.element_to_be_clickable((By.XPATH, RESERVED_LIST_PAGE.add_button)))

    add_reservation_button.click()
    # carrel_room_select = wait.until(EC.element_to_be_clickable((By.XPATH, RESERVE_RELATED_PAGE.carrel_room_select)))
    # agree_check_box = wait.until(EC.element_to_be_clickable((By.XPATH, RESERVE_RELATED_PAGE.agree_check_box)))
    # next_button = wait.until(EC.element_to_be_clickable((By.XPATH, RESERVE_RELATED_PAGE.next_button)))
    # reader_id_input = wait.until(EC.presence_of_element_located((By.XPATH, RESERVE_RELATED_PAGE.reader_id_input)))
    # print(reader_id_input)
    while True:
        time.sleep(1)
    submit_reader_id_button = driver.find_element(By.XPATH, RESERVE_RELATED_PAGE.submit_reader_id_button)
    request_all_button = driver.find_element(By.XPATH, RESERVE_RELATED_PAGE.request_all_button)





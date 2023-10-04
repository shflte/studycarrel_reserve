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
import os

def navigation(driver: webdriver.Chrome):
    load_dotenv()
    reserve_url = os.getenv("RESERVE_URL")
    reader_id_1 = os.getenv("READER_ID_1")
    reader_id_2 = os.getenv("READER_ID_2")


    wait = WebDriverWait(driver, 10)
    driver.get(reserve_url)

    # switch to iframe
    iframe_element = driver.find_element(By.XPATH, RESERVED_LIST_PAGE.iframe)
    driver.switch_to.frame(iframe_element)
    add_reservation_button = wait.until(EC.element_to_be_clickable((By.XPATH, RESERVED_LIST_PAGE.add_button)))
    add_reservation_button.click()
    
    # notice page
    carrel_room_select = wait.until(EC.element_to_be_clickable((By.XPATH, RESERVE_RELATED_PAGE.carrel_room_select)))
    agree_check_box = wait.until(EC.element_to_be_clickable((By.XPATH, RESERVE_RELATED_PAGE.agree_check_box)))
    next_button = driver.find_element(By.XPATH, RESERVE_RELATED_PAGE.next_button)
    carrel_room_select.click()
    agree_check_box.click()
    next_button.click()

    # enter reader id page
    reader_id_input_1 = driver.find_elements(By.XPATH, RESERVE_RELATED_PAGE.reader_id_input)[0]
    reader_id_input_2 = driver.find_elements(By.XPATH, RESERVE_RELATED_PAGE.reader_id_input)[1]
    submit_reader_id_button = driver.find_element(By.XPATH, RESERVE_RELATED_PAGE.submit_reader_id_button)
    reader_id_input_1.send_keys(reader_id_1)
    reader_id_input_2.send_keys(reader_id_2)
    submit_reader_id_button.click()

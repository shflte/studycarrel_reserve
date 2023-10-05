from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from dotenv import load_dotenv
import os
from page_objects import (
    TIME_SLOT_PAGE,
    DATE_PAGE
)

def reserve(driver: webdriver.Chrome, room: str, time_slots: tuple) -> int:
    wait = WebDriverWait(driver, 10)
    status = 0

    # request for all available rooms
    request_all_button = wait.until(EC.element_to_be_clickable((By.XPATH, DATE_PAGE.request_all_button)))
    request_all_button.click()

    # switch to popup window
    driver.switch_to.window(driver.window_handles[1])

    # choose room
    choose_room = wait.until(EC.element_to_be_clickable((By.XPATH, TIME_SLOT_PAGE.get_choose_room_xpath(room))))
    choose_room.click()

    # check if both checkboxes are present
    try:
        time_slots_checkbox_1 = driver.find_element(By.XPATH, TIME_SLOT_PAGE.get_time_slots_checkbox_xpath(room, time_slots[0]))
        time_slots_checkbox_2 = driver.find_element(By.XPATH, TIME_SLOT_PAGE.get_time_slots_checkbox_xpath(room, time_slots[1]))
        time_slot_box_1 = driver.find_element(By.XPATH, TIME_SLOT_PAGE.get_time_slots_block_xpath(room, time_slots[0]))
        time_slot_box_2 = driver.find_element(By.XPATH, TIME_SLOT_PAGE.get_time_slots_block_xpath(room, time_slots[1]))
    except:
        time_slots_checkbox_1 = None
        time_slots_checkbox_2 = None
        time_slot_box_1 = None
        time_slot_box_2 = None
        status = -2

    # check if attribute class is "disabled"
    if time_slot_box_1 and time_slot_box_2:
        if time_slot_box_1.get_attribute("class") == "disabled" or time_slot_box_2.get_attribute("class") == "disabled":
            status = -1

    # click if not disabled and present by checking status
    if status == 0:
        time_slots_checkbox_1.click()
        time_slots_checkbox_2.click()

        # submit
        submit_button = driver.find_element(By.XPATH, TIME_SLOT_PAGE.get_submit_button_xpath(room))
        submit_button.click()

        # alert check
        try:
            driver.switch_to.alert.accept()
        except:
            pass
    else:
        driver.close()
    
    driver.switch_to.window(driver.window_handles[0])

    return status

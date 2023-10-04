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

'''
time slot table

'''

def reserve(driver: webdriver.Chrome, room: str, time_slots: tuple):
    wait = WebDriverWait(driver, 10)

    # request for all available rooms
    request_all_button = wait.until(EC.element_to_be_clickable((By.XPATH, DATE_PAGE.request_all_button)))
    request_all_button.click()

    # switch to popup window
    driver.switch_to.window(driver.window_handles[1])

    # choose room
    choose_room = wait.until(EC.element_to_be_clickable((By.XPATH, TIME_SLOT_PAGE.get_choose_room_xpath(room))))
    choose_room.click()

    # choose time slots
    time_slots_checkbox = driver.find_element(By.XPATH, TIME_SLOT_PAGE.get_time_slots_checkbox_xpath(room, time_slots[0]))
    time_slots_checkbox.click()
    time_slots_checkbox = driver.find_element(By.XPATH, TIME_SLOT_PAGE.get_time_slots_checkbox_xpath(room, time_slots[1]))
    time_slots_checkbox.click()

    # submit
    submit_button = driver.find_element(By.XPATH, TIME_SLOT_PAGE.get_submit_button_xpath(room))
    submit_button.click()

    # alert check
    driver.switch_to.alert.accept()

    # switch back to main window
    driver.switch_to.window(driver.window_handles[0])
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import arrow
from web_script.page_objects import (
    TIME_SLOT_PAGE,
    DATE_PAGE
)

room_list = ["201", "202", "203", "501", "C601", "C602", "C603", "C604", "D601"]

def availability(driver: webdriver.Chrome) -> dict:
    wait = WebDriverWait(driver, 10)

    request_all_button = wait.until(EC.element_to_be_clickable((By.XPATH, DATE_PAGE.request_all_button)))
    request_all_button.click()

    driver.switch_to.window(driver.window_handles[1])
    wait.until(EC.presence_of_element_located((By.XPATH, TIME_SLOT_PAGE.get_time_slot_list_xpath(room_list[0]))))

    result = {}
    for room_id in room_list:
        time_slot_list = driver.find_elements(By.XPATH, TIME_SLOT_PAGE.get_time_slot_list_xpath(room_id))
        room_availability_list = []
        for i, time_slot_box in enumerate(time_slot_list):
            time_slot_time = arrow.get(time_slot_box.find_element(By.XPATH, TIME_SLOT_PAGE.get_time_slots_block_xpath_begin_time(room_id, i)).text, "HH:mm")
            availability = time_slot_box.get_attribute("class") != "disabled"
            room_availability_list.append((time_slot_time, availability))
        result[room_id] = room_availability_list

    driver.close()
    driver.switch_to.window(driver.window_handles[0])

    return result

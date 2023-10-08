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

def time_slot_to_str(time_slot: float) -> str:
    try:
        time = arrow.now().replace(hour=int(time_slot), minute=int((time_slot - int(time_slot)) * 60))
    except:
        time = arrow.now().replace(hour=23, minute=30)
    return time.format("HH:mm")

def reserve(driver: webdriver.Chrome, room: str, time_slot: float) -> int:
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

    time_slot_str = time_slot_to_str(time_slot)

    time_slots_checkbox_1 = None
    time_slot_box_1 = None
    try:
        time_slots_checkbox_1 = driver.find_element(By.XPATH, TIME_SLOT_PAGE.get_time_slots_checkbox_xpath(room, time_slot_str))
        time_slot_box_1 = driver.find_element(By.XPATH, TIME_SLOT_PAGE.get_time_slots_block_xpath(room, time_slot_str))
    except:
        return -2

    if time_slot_box_1:
        if time_slot_box_1.get_attribute("class") == "disabled":
            return -1
    else:
        return -2

    # find end of reservation
    time_slots_checkbox_2 = None
    offset = 0.5
    while offset < 4:
        try:
            time_slot_str = time_slot_to_str(time_slot + offset)
            tmp_box = driver.find_element(By.XPATH, TIME_SLOT_PAGE.get_time_slots_block_xpath(room, time_slot_str))
            if tmp_box.get_attribute("class") == "disabled":
                break
            else:
                time_slots_checkbox_2 = driver.find_element(By.XPATH, TIME_SLOT_PAGE.get_time_slots_checkbox_xpath(room, time_slot_str))
        except:
            break
        offset += 0.5

    # click if not disabled and present by checking status
    time_slots_checkbox_1.click()
    if time_slots_checkbox_2:
        time_slots_checkbox_2.click()

    # submit
    submit_button = driver.find_element(By.XPATH, TIME_SLOT_PAGE.get_submit_button_xpath(room))
    submit_button.click()

    # alert check
    try:
        if "已超過預約總時數" in driver.switch_to.alert.text or "在其它地方已預約相同時段" in driver.switch_to.alert.text:
            driver.switch_to.alert.accept()
            status = -3
    except:
        pass

    try:
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    except:
        pass

    return status

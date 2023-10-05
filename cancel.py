from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from dotenv import load_dotenv
import arrow
import os
from page_objects import (
    RESERVED_LIST_PAGE
)

def cancel(driver: webdriver.Chrome) -> int:
    load_dotenv()
    reserve_url = os.getenv("RESERVE_URL")
    driver.get(reserve_url)

    wait = WebDriverWait(driver, 10)
    status = 0

    breakpoint()

    try:
        nearest_reservation_time_element = wait.until(EC.element_to_be_clickable((By.XPATH, RESERVED_LIST_PAGE.get_nearest_reservation_time_xpath())))
        nearest_reservation_time_text = nearest_reservation_time_element.text.split().split("~")[0]
        nearest_reservation_time = arrow.get(nearest_reservation_time_text, "HH:mm:ss")
        current_time = arrow.now()
        time_diff = nearest_reservation_time - current_time
    except:
        nearest_reservation_time_element = None
        return 1

    if time_diff.seconds <= 600:
        nearest_reservation_cancel_checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, RESERVED_LIST_PAGE.get_nearest_reservation_cancel_checkbox_xpath())))
        nearest_reservation_cancel_checkbox.click()
        cancel_button = wait.until(EC.element_to_be_clickable((By.XPATH, RESERVED_LIST_PAGE.del_button)))
        cancel_button.click()
        try:
            driver.switch_to.alert.accept()
        except:
            status = -1

        driver.switch_to.window(driver.window_handles[0])
        driver.get(reserve_url)

        try:
            driver.find_element(By.XPATH, RESERVED_LIST_PAGE.get_nearest_reservation_time_xpath())
        except:
            status = 0
    else:
        status = 1
    
    return status

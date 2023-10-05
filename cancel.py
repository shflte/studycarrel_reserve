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

    iframe_element = driver.find_element(By.XPATH, RESERVED_LIST_PAGE.iframe)
    driver.switch_to.frame(iframe_element)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.XPATH, RESERVED_LIST_PAGE.reservation_list)))

    reservations = driver.find_elements(By.XPATH, RESERVED_LIST_PAGE.reservation_list)
    if len(reservations) == 1:
        return 1
    
    reservations = reservations[1:]
    for i in range(len(reservations)):
        reservation = reservations[i]
        reservation_time_element = reservation.find_element(By.XPATH, RESERVED_LIST_PAGE.get_reservation_time_xpath(i + 2))
        reservation_time_text = reservation_time_element.text.split("~")[0]
        reservation_time = arrow.get(reservation_time_text, "YYYYMMDD HH:mm:ss").replace(tzinfo="Asia/Taipei").shift(minutes=30)
        time_diff = reservation_time - arrow.now()

        if time_diff.seconds <= 1800:
            reservation_cancel_checkbox = reservation.find_element(By.XPATH, RESERVED_LIST_PAGE.get_reservation_cancel_checkbox_xpath(i + 2)
                                                                   )
            reservation_cancel_checkbox.click()
            cancel_button = reservation.find_element(By.XPATH, RESERVED_LIST_PAGE.del_button)
            cancel_button.click()

            confirm_button = wait.until(EC.element_to_be_clickable((By.XPATH, RESERVED_LIST_PAGE.confirm_button)))
            confirm_button.click()

            try:
                driver.switch_to.alert.accept()
            except:
                return -1

            driver.switch_to.window(driver.window_handles[0])
            driver.get(reserve_url)

            return 0

    return 2

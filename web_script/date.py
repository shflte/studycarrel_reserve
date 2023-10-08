# this script deals with the date and time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import arrow
from web_script.page_objects import DATE_PAGE

def same_month(date1: arrow.arrow.Arrow, date2: arrow.arrow.Arrow) -> bool:
    return date1.month == date2.month

def select_date(driver, date: arrow.arrow.Arrow):
    wait = WebDriverWait(driver, 10)

    # toggle calendar
    select_date_toggle = wait.until(EC.element_to_be_clickable((By.XPATH, DATE_PAGE.select_date_toggle)))
    select_date_toggle.click()

    # calendar elements
    calendar_next_month = wait.until(EC.element_to_be_clickable((By.XPATH, DATE_PAGE.calendar_next_month)))

    if not same_month(arrow.now(), date): # navigate to next month
        calendar_next_month.click()

    calendar_date = wait.until(EC.element_to_be_clickable((By.XPATH, DATE_PAGE.get_calendar_date_xpath(date.day))))
    calendar_date.click()

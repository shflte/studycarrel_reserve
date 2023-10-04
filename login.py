from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import subprocess
from page_objects import LOGIN_PAGE

from captcha_hack_2captcha import get_captcha_value

def login(driver: webdriver.Chrome, username: str, password: str):
    wait = WebDriverWait(driver, 10)
    captcha_img = wait.until(EC.presence_of_element_located((By.XPATH, LOGIN_PAGE.captcha_img)))

    # download captcha image and save it
    img_url = captcha_img.get_attribute("src")
    curl_command = f"curl -o captcha.png {img_url}"
    subprocess.run(curl_command, shell=True, check=True)

    # login
    username_input = driver.find_element(By.XPATH, LOGIN_PAGE.username_input)
    password_input = driver.find_element(By.XPATH, LOGIN_PAGE.password_input)
    captcha_input = driver.find_element(By.XPATH, LOGIN_PAGE.captcha_input)
    submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, LOGIN_PAGE.submit_button)))

    username_input.send_keys(username)
    password_input.send_keys(password)
    captcha_value = get_captcha_value()
    captcha_input.send_keys(captcha_value)
    driver.execute_script("arguments[0].click();", submit_button)

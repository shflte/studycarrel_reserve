from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from dotenv import load_dotenv
import subprocess
import requests
import os
import time

from page_objects import LOGIN_PAGE
from captcha_hack_2captcha import get_captcha_value

load_dotenv()

chrome_driver_path = os.getenv("CHROME_DRIVER_PATH")
login_url = os.getenv("LOGIN_URL")
account = os.getenv("ACCOUNT")
password = os.getenv("PASSWORD")

if not chrome_driver_path:
    raise Exception("CHROME_DRIVER_PATH not set")

chrome_options = Options()
chrome_options.binary_location = chrome_driver_path

if os.getenv("HEADLESS") == "True":
    chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()

url = login_url
driver.get(url)
# wait for page to load 
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

username_input.send_keys(account)
password_input.send_keys(password)
captcha_value = get_captcha_value()
captcha_input.send_keys(captcha_value)
driver.execute_script("arguments[0].click();", submit_button)

while True:
    time.sleep(1)

driver.quit()
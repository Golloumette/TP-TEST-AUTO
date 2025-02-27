import os
import tempfile
import uuid

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()

options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
unique_profile_dir = os.path.join(tempfile.gettempdir(), f"chrome_{uuid.uuid4()}")
options.add_argument(f"--user-data-dir={unique_profile_dir}")

driver = webdriver.Chrome(options=options)
driver.get("https://animationdigitalnetwork.com/")

driver.maximize_window()

wait = WebDriverWait(driver, 10)  # attend jusqu'à 10s
driver.save_screenshot("screenshot_before_click.png")
#try:
#    submit1 = wait.until(
        # EC.element_to_be_clickable((By.XPATH, "//*[contains(text(),'Continuer sans accepter')]"))
    # )
#     submit1.click()
# except:
#     print("Le bouton 'Continuer sans accepter' n'est pas apparu.")


submit2 = driver.find_element(By.XPATH, "//*[@data-testid='menu-login-link']")
submit2.click()
time.sleep(2)

submit3 = driver.find_element(By.XPATH, "//a[contains(text(),\"S'inscrire\")]")
submit3.click()

time.sleep(2)

submit4 = driver.find_element(By.XPATH, "//*[@data-testid='button']")
submit4.click()
time.sleep(1)

rand_num = random.randint(1000, 9999)
email_address = f"John.Doe{rand_num}@gmail.fr"
username_random = f"JohnDoe{rand_num}"

email = driver.find_element(By.NAME, "email")
email.send_keys(email_address)

password = driver.find_element(By.NAME, "password")
password.send_keys("Ceciestuntest123")

username = driver.find_element(By.NAME, "username")
username.send_keys(username_random)

password2 = driver.find_element(By.NAME, "passwordVerification")
password2.send_keys("Ceciestuntest123")

birthdate = driver.find_element(By.NAME, "birthdate")
birthdate.clear()  

actions = ActionChains(driver)
actions.click(birthdate)

actions.send_keys("28072002")
actions.perform()

radio_button = driver.find_element(By.XPATH, "//input[@type='radio' and @value='male']")
radio_button.click()

check_button = driver.find_element(By.XPATH, "//input[@type='checkbox' and @name='gcu']")
check_button.click()
time.sleep(5)

submit5 = driver.find_element(By.XPATH, "//*[@data-testid='registration-form-submit-button']")
submit5.click()

time.sleep(15)
driver.quit()

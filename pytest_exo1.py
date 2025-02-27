import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random
from selenium.webdriver.common.action_chains import ActionChains

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_registration_message(driver):
    driver.get("https://animationdigitalnetwork.com/")
    time.sleep(1)
    submit1 = driver.find_element(By.XPATH, "//*[contains(text(),'Continuer sans accepter')]")
    submit1.click()
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
    time.sleep(5)
    messagebox = driver.find_element(By.XPATH, "//*[@data-testid='messagebox-container']")
    texte = messagebox.text
    print(texte)
    assert "Votre compte a été créé" in texte
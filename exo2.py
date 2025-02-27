from selenium import webdriver
from selenium.webdriver.common.by import By
import time

options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(options=options)
driver.get("https://www.betclic.fr/football-sfootball/top-football-europeen-p0")

driver.maximize_window()
time.sleep(1)

cookie_buttons = driver.find_elements(By.ID, "popin_tc_privacy_button_2")
if cookie_buttons:
    cookie_buttons[0].click()
time.sleep(1)

matches = driver.find_elements(By.CLASS_NAME, "cardEvent_content")

for match in matches:
    event_info = match.find_element(By.CLASS_NAME, "event_info")
    competition = event_info.find_element(By.CLASS_NAME, "breadcrumb_list").text.strip()
    team1 = match.find_element(By.XPATH, ".//*[@data-qa='contestant-1-label']").text.strip()
    team2 = match.find_element(By.XPATH, ".//*[@data-qa='contestant-2-label']").text.strip()

    print("=" * 60)
    print(f"Compétition : {competition}")
    print(f"Match       : {team1} vs {team2}")

    market_odds_blocks = match.find_elements(By.CLASS_NAME, "market_odds")

    for odds_block in market_odds_blocks:
        buttons = odds_block.find_elements(By.CSS_SELECTOR, "button.btn.is-odd.is-large.has-trends")

        for btn in buttons:
            labels = btn.find_elements(By.CSS_SELECTOR, "span.btn_label")

            bet_name = labels[0].text.strip() if len(labels) > 0 and labels[0].text.strip() else "Nom non renseigné"
            bet_value = labels[1].text.strip() if len(labels) > 1 else "Valeur introuvable"

            print(f"  -  {bet_name} : {bet_value}")

    print("=" * 60)
    print()

time.sleep(2)
driver.quit()
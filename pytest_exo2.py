import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def test_betclic(driver):
    driver.get("https://www.betclic.fr/football-sfootball/top-football-europeen-p0")
    driver.maximize_window()
    time.sleep(1)

    cookie_buttons = driver.find_elements(By.ID, "popin_tc_privacy_button_2")
    if cookie_buttons:
        cookie_buttons[0].click()
    time.sleep(1)

    matches = driver.find_elements(By.CLASS_NAME, "cardEvent_content")
    assert len(matches) > 0, "No matches found"

    for match in matches:
        event_info = match.find_element(By.CLASS_NAME, "event_info")
        competition = event_info.find_element(By.CLASS_NAME, "breadcrumb_list").text.strip()
        team1 = match.find_element(By.XPATH, ".//*[@data-qa='contestant-1-label']").text.strip()
        team2 = match.find_element(By.XPATH, ".//*[@data-qa='contestant-2-label']").text.strip()

        assert competition, "Competition name is missing"
        assert team1, "Team 1 name is missing"
        assert team2, "Team 2 name is missing"

        market_odds_blocks = match.find_elements(By.CLASS_NAME, "market_odds")
        assert len(market_odds_blocks) > 0, "No market odds blocks found"

        for odds_block in market_odds_blocks:
            buttons = odds_block.find_elements(By.CSS_SELECTOR, "button.btn.is-odd.is-large.has-trends")

            for btn in buttons:
                labels = btn.find_elements(By.CSS_SELECTOR, "span.btn_label")

                bet_name = labels[0].text.strip() if len(labels) > 0 and labels[0].text.strip() else "Nom non renseigné"
                bet_value = labels[1].text.strip() if len(labels) > 1 else "Valeur introuvable"

                assert bet_name != "Nom non renseigné", "Bet name is missing"
                assert bet_value != "Valeur introuvable", "Bet value is missing"
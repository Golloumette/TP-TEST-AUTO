import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--window-size=1920,1080')  # Définit une taille de fenêtre explicite
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    # Optionnel : définir un user-agent pour simuler un navigateur standard
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def wait_for_element(driver, by, value, timeout=30):
    """Attend que l'élément soit visible (timeout par défaut à 30s)."""
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((by, value))
    )

def test_betclic(driver):
    driver.get("https://www.betclic.fr/football-sfootball/top-football-europeen-p0")
    
    # Tentative de clic sur le bouton de cookie (s'il existe)
    try:
        cookie_button = wait_for_element(driver, By.ID, "popin_tc_privacy_button_2", timeout=20)
        cookie_button.click()
    except Exception as e:
        print("Cookie button not found:", e)
    
    # Attendre quelques secondes pour laisser le temps au contenu de se charger
    time.sleep(5)
    
    # Sauvegarder un screenshot pour le diagnostic (sera uploadé via GitHub Actions si besoin)
    driver.save_screenshot("debug_betclic.png")
    
    # Attendre que les éléments des matchs soient présents
    matches = WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "cardEvent_content"))
    )
    assert len(matches) > 0, "No matches found"
    
    # Pour chaque match, vérifier les informations attendues
    for match in matches:
        event_info = match.find_element(By.CLASS_NAME, "event_info")
        competition = event_info.find_element(By.CLASS_NAME, "breadcrumb_list").text.strip()
        team1 = match.find_element(By.XPATH, ".//*[@data-qa='contestant-1-label']").text.strip()
        team2 = match.find_element(By.XPATH, ".//*[@data-qa='contestant-2-label']").text.strip()

        assert competition, "Competition name is missing"
        assert team1, "Team 1 name is missing"
        assert team2, "Team 2 name is missing"

        market_odds_blocks = match.find_elements(By.CLASS_NAME, "market_odds")
        assert market_odds_blocks, "No market odds blocks found"

        for odds_block in market_odds_blocks:
            buttons = odds_block.find_elements(By.CSS_SELECTOR, "button.btn.is-odd.is-large.has-trends")
            for btn in buttons:
                labels = btn.find_elements(By.CSS_SELECTOR, "span.btn_label")
                bet_name = labels[0].text.strip() if len(labels) > 0 and labels[0].text.strip() else "Nom non renseigné"
                bet_value = labels[1].text.strip() if len(labels) > 1 else "Valeur introuvable"
                assert bet_name != "Nom non renseigné", "Bet name is missing"
                assert bet_value != "Valeur introuvable", "Bet value is missing"

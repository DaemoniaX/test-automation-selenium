from concurrent.futures import wait
import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
"""
# https://www.youtube.com/watch?v=NB8OceGZGjA 23:40

#### Setup Zone ####

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.get("http://localhost:5011/")

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "search-input")))

#### Test Zone ####
input_element = driver.find_element(By.CLASS_NAME, "search-input")
input_element.send_keys("StoKs")
time.sleep(2)
input_element.clear()
time.sleep(0.5)
input_element.send_keys("Stocks")

#### End of Test Zone ####

time.sleep(9)
driver.quit() 

En fait le problème avec ce tuto, c'est qu'il ne fait pas vraiment de test. Il ne retourne rien, il fait plutot des 
tests visuels, y a pas de doc, si quelqu'un passe après moi il va lancer le script et rien ne lui dira si le test a réussi ou pas.

En python on a vu les tests pytest, deja ca a l'air plus intéressant. Et puis les time sleep qui pourraient
casser si le site est lent à répondre...

Je laisse ce bout en l'état là haut, pour montrer l'évolution. Je le développait en parrallèle du site react, et je l'ai abandonné
pour me concentrer sur le site. Et j'ai bien fait.

Du coup j'ai suivi la doc

"""

# URL de mon site
BASE_URL = "https://daemoniax.github.io/Portfolio-React/"


@pytest.fixture
def driver():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    
    yield driver
    driver.quit()

# /// TESTS ///

def test_home(driver):
    """Homepage et éléments de base"""
    driver.get(BASE_URL)
    wait = WebDriverWait(driver, 10)
    
    # Titre
    assert "Portfolio" in driver.title, "pas de titre"
    
    # NavBar
    nav = wait.until(EC.presence_of_element_located((By.TAG_NAME, "nav")))
    assert nav.is_displayed(), "Pas de NavBar visible"
    
    # Cards
    cards = driver.find_elements(By.CLASS_NAME, "panel-card")
    assert len(cards) > 0, "Pas de Cards"

def test_search(driver):
    """Search input"""
    driver.get(BASE_URL)
    wait = WebDriverWait(driver, 5)

    search_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".search-input")))
    
    search_input.clear()
    search_input.send_keys("Kiduland")
    wait.until(lambda d: len(d.find_elements(By.CLASS_NAME, "panel-card")) == 1)
    
    card = driver.find_element(By.CLASS_NAME, "panel-card")
    assert "Kiduland" in card.text, "Abscence de la carte Kiduland"
    
    search_input.clear()
    
    search_input.send_keys("Zorglub123")
    time.sleep(0.5)
    
    cards = driver.find_elements(By.CLASS_NAME, "panel-card")
    assert len(cards) == 0

def test_favorites(driver):
    """Cycle favoris"""
    driver.get(BASE_URL)
    wait = WebDriverWait(driver, 5)

    first_card_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".panel-card button")))
    first_card_btn.click()

    fav_section = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "favorites-section")))
    assert fav_section.is_displayed()
    
    fav_cards = fav_section.find_elements(By.CLASS_NAME, "panel-card")
    assert len(fav_cards) == 1

    fav_btn = fav_cards[0].find_element(By.TAG_NAME, "button")
    fav_btn.click()

    wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "favorites-section")))


@pytest.mark.parametrize("route, expected_text", [
    ("/#/CV", "Ingénieur ESIEE Paris"),
    ("/#/graphs", "Calculateur d'intérêts composés"),
    ("/#/kiduland", "Kiduland"),
    ("/#/backend", "Back"),
])
def test_routes(driver, route, expected_text):
    """Vérifie que les pages chargent et sont accessibles"""
    full_url = f"{BASE_URL.rstrip('/')}{route}"
    driver.get(full_url)
    
    wait = WebDriverWait(driver, 5)
    
    header = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1, h2, h3")))
    
    assert expected_text.lower() in header.text.lower(), f"La page {route} ne contient pas le titre testé"

def test_swiper(driver):
    """Test swiper"""
    driver.get(f"{BASE_URL}#/zuulbad")
    wait = WebDriverWait(driver, 10)

    swiper = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "swiper")))

    driver.execute_script("document.querySelector('.swiper').swiper.autoplay.stop();")

    next_btn = driver.find_element(By.CLASS_NAME, "swiper-button-next")
    
    #next_btn.click()
    driver.execute_script("arguments[0].click();", next_btn)
    time.sleep(0.5)


    active_slide = driver.find_element(By.CLASS_NAME, "swiper-slide-active")
    assert active_slide.is_displayed(), "si ça ne marche pas ce n'est pas forcément une erreur, il marche 1fois sur 2 pendant le test"


def test_external_link(driver):
    """Vérifie que le clic sur la carte JS Calculator ouvre un nouvel onglet"""
    driver.get(BASE_URL)
    wait = WebDriverWait(driver, 10)

    xpath_carte = "//div[contains(@class, 'panel-card')][contains(., 'JS Calculator')]"
    
    carte = wait.until(EC.presence_of_element_located((By.XPATH, xpath_carte)))
    
    original_window = driver.current_window_handle

    driver.execute_script("arguments[0].click();", carte)
    
    wait.until(EC.number_of_windows_to_be(2))
    
    driver.switch_to.window(driver.window_handles[-1])
            
    wait.until(EC.url_contains("Calculator"))
    assert "JSCalculator" in driver.current_url
    
    driver.close()
    driver.switch_to.window(original_window)


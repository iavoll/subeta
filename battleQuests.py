import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from login import login, pets
from finditems import grasp

RETRIES = 10
TOGGLED = False
ACTIVE = pets[0]

def restart():
    driver.get(f"https://subeta.net/explore/healer.php?act=heal&petid={ACTIVE}")
    elem = WebDriverWait(driver, 10).until(
        EC.title_is("Healer's Abode - Subeta")
    )
    grasp(driver)


def fight(url):
    driver.get(f"{url}&pet={ACTIVE}")
    after = EC.element_to_be_clickable((By.ID, "start-battle-button"))
    grasp(driver, after)
    # global TOGGLED
    # if not TOGGLED:
    #     elem = driver.find_element_by_id("preselect-setting-toggle")
    #     elem.click()
    #     TOGGLED = True

    elem = driver.find_element_by_id("start-battle-button")
    elem.click()
    elem = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "turn_button"))
    )
    
    # grasp(driver, after)
    # try:
    while elem:
        try:
            end_game = driver.find_element_by_css_selector("end-game-btn")
            break
        except:
            pass
        try:
            elem = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "turn_button"))
            )
            elem = driver.find_element_by_id("turn_button")
            elem.click()
        except:
            break
    # except:
    #     raise Exception("No button")
        
    # elem = driver.find_element_by_link_text("See Results")
    # elem.click()
    driver.get('https://subeta.net/games/battle/battle.php?act=end_game')
    grasp(driver)
    try:
        return 'You Won' in driver.find_element_by_xpath("//h2").text
    except:
        if "battle doesn't exist" in driver.page_source:
            return True
        else: return False


def attempt(url, tries):
    restart()
    result = fight(url)
    
    if result:
        driver.get('https://subeta.net/games/battle/quest.php/start')
        elem = WebDriverWait(driver, 10).until(
            EC.title_is("Battle Quests - Subeta")
        )
        grasp(driver)
        return True
    elif tries < RETRIES:
        attempt(url, tries + 1)
    else:
        return False
         

def cycle(driver):
    driver.get('https://subeta.net/games/battle/quest.php/start')
    elem = WebDriverWait(driver, 10).until(
        EC.title_is("Battle Quests - Subeta")
    )
    grasp(driver)

    url = driver.find_element_by_xpath("//a[contains(@href, 'act=battle')]").get_attribute('href')
    success = attempt(url, 0)
    
    if success:
        cycle(driver)
    else:
        return
        
    
driver = login()

driver.execute_script('window.localStorage.setItem("sb-battle-preselect", true);')
driver.get('https://subeta.net/games/battle/quest.php/start')
elem = WebDriverWait(driver, 10).until(
    EC.title_is("Battle Quests - Subeta")
)
grasp(driver)
cycle(driver)

driver.quit()
import sys, time
from selenium.common.exceptions import TimeoutException
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
MONSTER = sys.argv[1]

def turn_over(driver):
    finished = EC.visibility_of_element_located((By.LINK_TEXT, "See Results"))
    continuable = EC.visibility_of_element_located((By.XPATH, "//input[@class='btn btn-primary']"))
    if finished or continuable:
        return True
    return False


def restart():
    driver.get(f"https://subeta.net/explore/healer.php?act=heal&petid={ACTIVE}")
    try:
        WebDriverWait(driver, 10).until( EC.title_is("Healer's Abode - Subeta") )
    except:
        restart()
    grasp(driver)


def fight(url):
    driver.get(f"{url}&pet={ACTIVE}")
    try:
        driver.find_element_by_id("start-battle-button").send_keys(Keys.RETURN)
        WebDriverWait(driver, 10).until( EC.element_to_be_clickable((By.ID, "turn_button")) )
    except:
        driver.get("https://subeta.net/games/battle/battle.php")
        if "That battle doesn't exist!" in driver.page_source:
            fight(url)

    # grasp(driver, after)
    while True:
        try:
            driver.find_element_by_id("turn_button").send_keys(Keys.RETURN)
        except:
            pass
        try:
            WebDriverWait(driver,10).until( turn_over )
        except Exception as e:
            print(e)
            driver.refresh()
        try:
            driver.find_element_by_link_text("See Results")
            break
        except:
            pass

    driver.get('https://subeta.net/games/battle/battle.php?act=end_game')
    grasp(driver)
    try:
        return 'You Won' in driver.find_element_by_xpath("//h2").text
    except:
        return False


def attempt(url):
    restart()
    result = fight(url)
    
    if result:
        return True
    else:
        return False
         

def cycle(driver):
    url = f"https://subeta.net/games/battle/challenge.php?act=battle&id={MONSTER}"
    success = attempt(url)


driver = login()
driver.execute_script('window.localStorage.setItem("sb-battle-preselect", true);')
while True:
    cycle(driver)

driver.quit()
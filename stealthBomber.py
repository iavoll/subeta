from random import choice
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time

from login import login
from finditems import grasp

URL = "https://subeta.net/games/stealth_bomber.php"

def play():
    try: # Virgin start
        driver.find_element_by_link_text("Want to play?")
        driver.get(f"{URL}?act=start")
        grasp(driver)
    except:
        pass

    try: # pairing stage
        card_links = [x.get_attribute('href') for x in driver.find_elements_by_xpath("//a[contains(@href, '?act=pair&card')]")]
        for x in card_links:
            if card_links.count(x) > 1:
                driver.get(x)
                grasp(driver)
        while "continue the game" in driver.page_source:
            driver.get(f"{URL}?act=continue")
            grasp(driver)
    except:
        pass

    try: # blind stage
        links = [x.get_attribute('href') for x in driver.find_elements_by_xpath("//a[contains(@href, '?act=continue')]")]
        driver.get(choice(links))
        grasp(driver)
    except:
        pass

    try: # Post-finish start
        driver.find_element_by_link_text("Play Again?")
        driver.get(f"{URL}?act=start")
        grasp(driver)
    except:
        pass

    driver.get(URL)
    grasp(driver)


driver = login()

while True:
    play()
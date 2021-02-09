import sys, time

from random import choice, randrange
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from login import login, pets
from finditems import grasp


def click_random_areas(url):
    load_url(url)
    try:
        areas = driver.find_elements_by_xpath("//area")
        load_url(choice(areas).get_attribute('href'))
    except:
        pass


def load_url(url, condition=None):
    driver.get(url)
    if condition:
        WebDriverWait(driver, 15).until(condition)
    grasp(driver)


def bathe():
    load_url("https://subeta.net/explore/shengui_guo/bathhouse/pools.php?act=dip")


def bank_invitations(): # post-quests
    load_url("https://subeta.net/explore/subeautique.php/turnin")


def bank_tokens(): # post-quests
    load_url("https://subeta.net/explore/wizard_exchange.php")
    try:
        driver.find_element_by_css_selector("input[value='Exchange your tokens automatically!']").click()
        grasp(driver)
    except:
        pass


def coinMachine(driver):
    try:
        driver.get("https://subeta.net/explore/coinmachine.php")
        grasp(driver)
        driver.find_element_by_xpath("//div/b/../a").click()
        grasp(driver)
        return True
    except:
        return False


def crypts(): # > once per day
    load_url("https://subeta.net/explore/crypts.php?act=start")
    click_random_areas("https://subeta.net/explore/crypts.php?act=play")
    try:
        driver.find_element_by_link_text("Set Alert")
    except:
        crypts()


def decanter(): # > once per day
    load_url("https://subeta.net/games/decanter.php")
    grasp(driver)
    try:
        driver.find_element_by_xpath("//input[@type='submit']").click()
    except:
        pass
    while not any(x in driver.page_source for x in ["ruined", "play again"]):
        try:
            # options = len(driver.find_elements_by_xpath("//div/a/img")) + 1
            load_url(f"https://subeta.net/games/decanter.php?act={randrange(1,6)}")
        except:
            pass


def fruit():
    load_url("https://subeta.net/explore/tree.php?act=take")


def galley():
    load_url(f"https://subeta.net/explore/galley.php?act=rat&id={randrange(1,7)}")


def garbage():
    load_url("https://subeta.net/explore/trash_can.php?act=look")


def ice_fields(): # > once per day
    load_url("https://subeta.net/explore/ice_fields.php")
    def walk():
        try:
            directions = driver.find_elements_by_xpath("//center/a[contains(@href, 'move')]")
            load_url(choice(directions).get_attribute('href'))
            return True
        except IndexError:
            return False
    result = True
    while result:
        result = walk()


def jankenpon(): # > once daily
    moves = ["r", "p", "s"]
    for i in range(20):
        load_url(f"https://subeta.net/games/rps.php?act=choose&c={choice(moves)}")
        if "bored" in driver.page_source:
            break


def job_income():
    for i in pets:
        load_url(f"https://subeta.net/explore/job_agency.php?pet={i}&view=collect")


def mage_quests(): # post-quests
    load_url("https://subeta.net/explore/mage.php")
    try:
        items = [x.get_attribute('href') for x in driver.find_elements_by_xpath("//td/a")]
        for item in items:
            driver.get(item)
            grasp(driver)
    except:
        pass


def mallarchy_pond(): # > once daily
    load_url(f"https://subeta.net/explore/carnival_mallarchypond.php?duck={randrange(1,26)}")


def mind_reader():
    def move():
        try:
            load_url("https://subeta.net/games/mind_reader.php?action=start_game")
            options = driver.find_elements_by_xpath("//tr/td/a")
            load_url(choice(options).get_attribute('href'))
            return True
        # except ValueError:
        except IndexError:
            return False
    result = True
    while result:
        result = move()


def raffle():
    load_url("https://subeta.net/explore/carnival/ruffie_raffle.php")
    try:
        cards = driver.find_elements_by_xpath("//div[contains(@data-color, 'e')]")
        choice(cards).click()
    except:
        pass


def random_game(): # > once per day
    load_url("https://subeta.net/games/random.php/play")


def train():
    load_url("https://subeta.net/explore/train.php")
    try:
        driver.find_element_by_xpath("//input[contains(@value, 'Done')]").click()
        driver.find_element_by_xpath("//input[@value='Train your Pet']").click()
    except:
        try:
            driver.find_element_by_xpath(f"//input[@value='{pets[0]}']/../input[@value='Train your Pet']").click()
        except:
            pass


def underground_fish(): # > once per day
    click_random_areas("https://subeta.net/explore/underground/fishing.php")

if __name__ == "__main__":
    driver = login()

    def hourly():
        train()
        mallarchy_pond()
        underground_fish()
        galley()
        jankenpon()
        decanter()
        random_game()
        crypts()
        ice_fields()

    def daily():
        bathe()
        job_income()
        mind_reader()
        raffle()
        garbage()
        fruit()
        mage_quests()
        bank_tokens()
        bank_invitations()
        while coinMachine(driver): pass

    toggle = sys.argv[1] if len(sys.argv) > 1 else ''

    if 'hour' in toggle:
        while True:
            hourly()
            time.sleep(1800)
    # elif 'train' in toggle:
    else:
        daily()

    driver.quit()
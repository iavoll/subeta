import lxml.html
import sys
import time

from random import choice, randrange

from login import headless_login, pets
from finditems import headless_grasp as grasp


def click_random_areas(s, url):
    r = load_url(s, url)
    root = lxml.html.fromstring(r)
    root.make_links_absolute(url.split("?")[0])
    try:
        areas = [x for x in root.xpath('//area/@href')]
        area = choice(areas)
        print(area)
        return load_url(s, area)
    except:
        return None


def load_url(s, url):
    r = s.get(url, timeout=15)
    grasp(s, r.text)
    return r.text



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


def crypts(s): # > once per day
    load_url(s, "https://subeta.net/explore/crypts.php?act=start")
    r = click_random_areas(s, "https://subeta.net/explore/crypts.php?act=play")
    if r is not None and "Set Alert" not in r:
        crypts(s)


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


def train(s):
    load_url("https://subeta.net/explore/train.php")
    try:
        driver.find_element_by_xpath("//input[contains(@value, 'Done')]").click()
        driver.find_element_by_xpath("//input[@value='Train your Pet']").click()
    except:
        try:
            data = {
                "act": "dotrain",
                "petid": pets[0],
                "stat": "5",
                "train_normal": "Train+your+Pet"
            }
            r = s.post("https://subeta.net/explore/train.php", data=data)
        except:
            pass


def underground_fish(s): # > once per day
    click_random_areas(s, "https://subeta.net/explore/underground/fishing.php")

if __name__ == "__main__":
    s = headless_login()

    def hourly():
        train()
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

    crypts(s)
    # toggle = sys.argv[1] if len(sys.argv) > 1 else ''

    # if 'hour' in toggle:
    #     while True:
    #         hourly()
    #         time.sleep(3600)
    # # elif 'train' in toggle:
    # else:
    #     daily()

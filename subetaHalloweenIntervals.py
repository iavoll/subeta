# requires Chrome
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import random, regex, sys, time, threading

time_remaining = regex.compile(r'(?ms)You have(?:[ <b>]*(?P<hour>\d+)[ <b>\/]*hours*)?[ <b>]*(?P<min>\d+)[ <b>\/]*minutes*[ <b>and]*(?P<sec>\d+)[ <b>\/]*seconds*')
find_url = regex.compile(r"(?ms)The link you're trying to use has expired.*?<a href=['|\"](.*)['|\"] class=['|\"]btn btn-morostide['|\"]")


def rechercher(driver, default):
    captured_time = regex.search(time_remaining, driver.page_source)
    if captured_time:
        time = 60 * int(captured_time.group('min')) + int(captured_time.group('sec'))
        if captured_time.group('hour'):
            time += 3600 * int(captured_time.group('hour'))
        print(time)
        return time
    else:
        print(default)
        return default


def pumpkin(driver):
    try:
        elem = driver.find_element_by_class_name('floating_item').find_element_by_tag_name('a')
        elem.click()
    except:
        pass


def trickOrTreat(driver):
    driver.get('https://subeta.net/profile.php?act=trickortreat&random=true')
    pumpkin(driver)
    found_url = regex.search(find_url, driver.page_source)
    if found_url:
        query = found_url.group(1).replace('\n', '').replace('&amp;', '&')
        driver.get('https://subeta.net' + query)
        pumpkin(driver)
        time.sleep(rechercher(driver, 60 * 3))
        trickOrTreat(driver)
        # threading.Timer(rechercher(driver, 60 * 5), trickOrTreat)
    else:
        trickOrTreat(driver)
    # elem = WebDriverWait(driver, 10).until( EC.title_is('Trick or Treat - Subeta') )
        

def pumpkinPatch(driver):
    url = 'https://subeta.net/explore/pumpkins.php?act=pick&pick=' + str(random.randrange(1, 5, 1))
    driver.get(url)
    pumpkin(driver)
    driver.refresh()
    elem = WebDriverWait(driver, 10).until( EC.title_is('Pumpkin Patch - Subeta') )
    pumpkin(driver)
    time.sleep(rechercher(driver, 60 * 18))
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
    pumpkinPatch(driver)
    # threading.Timer(rechercher(driver, 60 * 25), pumpkinPatch)


driver = login()
function = sys.argv[1]
if function == 'trickOrTreat':
    trickOrTreat(driver)
else:
    pumpkinPatch(driver)
# threading.Thread(target=login, args=(trickOrTreat,)).start()
# threading.Thread(target=login, args=(pumpkinPatch,)).start()
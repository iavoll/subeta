# requires Chrome
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import random, re, sys, time

from login import login


time_remaining = re.compile(r"(?ms)You can't kiss again for(?:[ <b>]*(?P<min>\d+)[ <b>\/]*minutes*)?[ ]*(?P<sec>\d+)[ <b>\/]*seconds*")
seed = random.seed()


def pumpkin(driver):
    try:
        elem = driver.find_element_by_class_name('floating_item').find_element_by_tag_name('a').send_keys(Keys.RETURN)
        time.sleep(2)
        elem = driver.find_element_by_id('MB_close').send_keys(Keys.RETURN)
        time.sleep(2)
    except:
        pass


def rechercher(driver, default):
    time.sleep(2)
    alert_modal = driver.execute_script('return document.getElementById("sapi-output-modal").innerHTML;')
    # print(alert_modal)
    captured_time = re.search(time_remaining, alert_modal)
    if captured_time:
        seconds = int(captured_time.group('sec'))
        if captured_time.group('min'):
            seconds += 60 * int(captured_time.group('min'))
        print(seconds)
        return max(seconds - 2, 0)
    else:
        print(default)
        return default - 2


def camp(driver):
    driver.execute_script("location.reload(true);")
    pumpkin(driver)
    try:
        try:
            elem = driver.find_element_by_css_selector("tr > td > div.holiday.survival > a.holiday-kiss")
        except:
            links = driver.find_elements_by_css_selector("a.holiday-kiss")
            elem = links[random.randrange(len(links))]
        elem.send_keys(Keys.RETURN)
        time.sleep(rechercher(driver, 30))
        camp(driver)
    except:
        time.sleep(30)
        camp(driver)

driver = login()
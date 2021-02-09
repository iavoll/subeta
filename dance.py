# requires Chrome
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import random, re, sys, time

from login import login

time_remaining = re.compile(r"(?ms) have ([ <b>]*(?P<min>\d+)[ <b>\/]*minutes*)?([ ]*(?P<sec>\d+)[ <b>\/]*seconds*)? before you can")
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
    captured_time = re.search(time_remaining, alert_modal)
    if captured_time:
        seconds = -2
        if captured_time.group('sec'):
            seconds += int(captured_time.group('sec'))
        if captured_time.group('min'):
            seconds += 60 * int(captured_time.group('min'))
        print(seconds)
        return max(seconds, 0)
    else:
        print(default)
        return default - 2


def camp(driver):
    # driver.execute_script("location.reload(true);")
    # pumpkin(driver)
    driver.get("https://subeta.net/forums.php/forum/10/Atebus-Revolution-Masquerade")
    elem = WebDriverWait(driver, 10).until(
        EC.title_is("Atebus Revolution Masquerade - Subeta")
    )
    pumpkin(driver)
    try:
    #     elem = driver.find_element_by_css_selector("a.holiday-dance-invite")
    # except:
        links = driver.find_elements_by_css_selector("tbody > tr > td > a")
        elem = links[random.randrange(len(links))]
        elem.send_keys(Keys.RETURN)
        elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Dance with me!"))
        )
        # time.sleep(5)
        links = driver.find_elements_by_css_selector("a.holiday-dance-invite")
        elem = links[random.randrange(len(links))]
    except:
        time.sleep(10)
        camp(driver)
    try:
        elem.send_keys(Keys.RETURN)
        elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "sapi-output-modal"))
        )
        time.sleep(rechercher(driver, 10))
        camp(driver)
    except:
        time.sleep(10)
        camp(driver)

driver = login()
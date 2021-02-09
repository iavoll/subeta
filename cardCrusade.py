# requires Chrome
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import sys, time

from login import login


def pumpkin(driver):
    try:
        elem = driver.find_element_by_class_name('floating_item').find_element_by_tag_name('a').send_keys(Keys.RETURN)
        time.sleep(2)
        elem = driver.find_element_by_id('MB_close').send_keys(Keys.RETURN)
        time.sleep(2)
    except:
        pass


def play(driver):
    while True:
        pumpkin(driver)
        try:
            elem = driver.find_element_by_css_selector("div#main-content > div#content > div.container-fluid > center > table > tbody > tr > td > center > a")
            elem.send_keys(Keys.RETURN)
        except:
            break

driver = login()
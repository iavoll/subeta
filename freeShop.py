# requires Chrome
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import random, regex, sys, time

from login import login


time_remaining = regex.compile(r'(?ms)You have(?:[ <b>]*(?P<hour>\d+)[ <b>\/]*hours*)?[ <b>]*(?P<min>\d+)[ <b>\/]*minutes*[ <b>and]*(?P<sec>\d+)[ <b>\/]*seconds*')


def rechercher(driver, default):
    captured_time = regex.search(time_remaining, driver.page_source)
    if captured_time:
        time = 60 * int(captured_time.group('min')) + int(captured_time.group('sec'))
        if captured_time.group('hour'):
            time += 3600 * int(captured_time.group('hour'))
        #print(time)
        return time
    else:
        #print(default)
        return default


def camp(driver):
    driver.get("https://subeta.net/shop.php?shopid=43")
    try:
        #elem = driver.find_element_by_css_selector("input[class*='ui image'")
        links = driver.find_elements_by_css_selector("input[class*='ui image'")
        elem = links[random.randrange(len(links))]
        elem.click()
        elem = WebDriverWait(driver, 30)#.until( EC.title_is('Purchasing from Free Shop - Subeta') )
        if 'This item was already purchased.' in driver.page_source:
            camp(driver)
        else:
            time.sleep(rechercher(driver, 5))
            camp(driver)
    except:
        time.sleep(11)
        camp(driver) # will run ad inifinitum if there are no more pumpkins


driver = login()
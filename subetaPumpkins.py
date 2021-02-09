# requires Chrome
from selenium import webdriver,
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import random, regex, sys, time, threading


def pumpkin(driver):
    try:
        elem = driver.find_element_by_class_name('floating_item').find_element_by_tag_name('a').send_keys(Keys.RETURN)
        time.sleep(2)
        elem = driver.find_element_by_id('MB_close').send_keys(Keys.RETURN)
        time.sleep(2)
    except:
        pass


def carve(driver: WebDriver):
    elem = driver.find_element_by_xpath('//')


driver = login()
driver.get("https://subeta.net/inventory.php")
elem = WebDriverWait(driver, 10).until(
        EC.title_is("Your Inventory - Subeta")
    )
while carve(driver):
    continue
driver.quit()

name: str = sys.argv[1]
login()
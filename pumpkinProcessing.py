# requires Chrome
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import re, sys, time

from login import login

valid_pumpkins = ['Carvable Pumpkin', 'Pumpkin on the Vine', 'Carving Pumpkin', 'Fresh Pumpkin',
    'Freshly Picked Pumpkin', 'Ready-to-Carve Pumpkin', 'Uncarved Pumpkin']


def pumpkin(driver):
    try:
        elem = driver.find_element_by_class_name('floating_item').find_element_by_tag_name('a').send_keys(Keys.RETURN)
        time.sleep(2)
        elem = driver.find_element_by_id('MB_close').send_keys(Keys.RETURN)
        time.sleep(2)
    except:
        pass


def feed(driver):
    driver.get("https://subeta.net/inventory.php")
    pumpkin(driver)
    # try:
    elem = driver.find_element_by_css_selector("img[alt*='Carved Pumpkin']")
    elem.click()

    pumpkin(driver)
    try:
        elem = driver.find_element_by_partial_link_text("Pumpkin Collection")
        elem.click()
    except:
        try:
            elem = driver.find_element_by_link_text("Feed to a Pet")
            elem.click()
            elem = driver.find_element_by_css_selector("a[href*='&act=food&petid='")
            elem.click()

            alert = driver.switch_to_alert()
            alert.accept()
        except:
            # driver.quit()
            pass
    
    feed(driver)


def donate(driver):
    driver.get("https://subeta.net/explore/fireside_fantine.php")
    pumpkin(driver)
    try:
        elem = driver.find_element_by_css_selector("a[href*='?act=turnin&pumpkin'")
        elem.click()

        pumpkin(driver)
        donate(driver)
    except:
        donate(driver) # will run ad inifinitum if there are no more pumpkins


def carve(driver):
    driver.get("https://subeta.net/inventory.php")
    pumpkin(driver)
    for name in valid_pumpkins:
        try:
            elem = driver.find_element_by_css_selector(f"img[alt='{name}']")
            elem.click()

            pumpkin(driver)
            elem = driver.find_element_by_partial_link_text("Carve Pumpkin")
            elem.send_keys(Keys.RETURN)

            alert = driver.switch_to_alert()
            alert.accept()

            carve(driver)
        except:
            continue


driver = login()

function = sys.argv[1]
if function == 'carve':
    carve(driver)
elif function == 'donate':
    donate(driver)
elif function == 'feed':
    feed(driver)
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
# import re
import time


def pumpkin(driver, after=None):
    try:
        elem = driver.find_element_by_class_name('floating_item').find_element_by_tag_name('a').click()
        time.sleep(2)
        # WebDriverWait(driver, 5).until( EC.element_to_be_clickable((By.ID, "MB_close")) )
        elem = driver.find_element_by_id('MB_close').click()
        time.sleep(2)
        if after is not None:
            try:
                WebDriverWait(driver, 5).until( after )
            except:
                driver.refresh()
    except:
        pass


def tempest(driver):
    try:
        elem = driver.find_element_by_css_selector("a[href*='/explore/tempest.php'")
        # elem.send_keys(Keys.CONTROL + Keys.RETURN)
        elem.send_keys(Keys.COMMAND + Keys.RETURN)
        driver.switch_to.window(driver.window_handles[1])
        pumpkin(driver)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    except:
        pass


def headless_tempest(s, response_text):
    if "/explore/tempest.php" in response_text:
        _ = s.get("https://subeta.net/explore/tempest.php", timeout=10)


def grasp(driver, after=None):
    pumpkin(driver, after)
    tempest(driver)


def headless_grasp(s, response_text):
    headless_tempest(s, response_text)

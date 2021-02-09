# requires Chrome
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import re, sys, time

from finditems import grasp
from login import login

def donate(driver):
    driver.get("https://subeta.net/explore/freefood.php?act=donate")
    grasp(driver)
    try:
        elem = driver.find_element_by_xpath("//div[@class='col-12 text-center']//a/div/img")
        elem.click()

        grasp(driver)
        #donate(driver)
    except:
        pass
    #donate(driver) # will run ad inifinitum if there are no more pumpkins


def burn(driver):
    driver.get("https://subeta.net/explore/bonfire.php")
    grasp(driver)
    try:
        elem = driver.find_element_by_xpath("//a/div/img[not(contains(@alt, 'Wreathed'))]")
        elem.click()
        driver.switch_to.alert.accept()
        grasp(driver)
    except:
        pass
    #burn(driver)


driver = login()
functions = {
    "donate": donate,
    "burn": burn
}
while True:
    functions[sys.argv[1]](driver)
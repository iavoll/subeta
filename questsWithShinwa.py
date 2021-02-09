# requires Chrome
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import re, time

from login import login
from finditems import grasp

QUESTS = {"sarah", "wizard", "quentin", "library", "carl", "cinthia", "cursed", "maleria", "pete", "saggitarius", "blue"}

def doQuest(elem, url):
    elem.send_keys(Keys.RETURN)#.click()
    grasp(driver)
    items = driver.find_elements_by_partial_link_text("Shop Search")
    for item in items:
        item.send_keys(Keys.CONTROL + Keys.RETURN)              
    while len(driver.window_handles) > 1:
        driver.switch_to.window(driver.window_handles[1])
        grasp(driver)
        # elem = WebDriverWait(driver, 60).until(lambda driver: driver.execute_script('return document.getElementsByClassName().length > 0') == 'true')
        buylink = driver.find_element_by_css_selector("*.btn.btn-primary.btn-sm").send_keys(Keys.RETURN)
        try:
            elem = WebDriverWait(driver, 15).until(
                lambda driver: EC.title_contains("Purchasing from") or EC.presence_of_element_located((By.ID, "purchasedContainer"))
            )
        except TimeoutException:
            driver.refresh()
            buylink = driver.find_element_by_css_selector("*.btn.btn-primary.btn-sm").send_keys(Keys.RETURN)
            elem = WebDriverWait(driver, 15).until(
                lambda driver: EC.title_contains("Purchasing from") or EC.presence_of_element_located((By.ID, "purchasedContainer"))
            )
        if EC.title_contains("Purchasing from"):
            grasp(driver)
            time.sleep(5)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    driver.switch_to_window(main_window)
    finish = driver.find_element_by_css_selector("button.btn.btn-lg.btn-success").send_keys(Keys.RETURN)
    try:
        elem = WebDriverWait(driver, 15).until(
            lambda driver: EC.text_to_be_present_in_element((By.TAG_NAME, "h1"), "Finished")
        )
    except TimeoutException:
        driver.refresh()
        elem = WebDriverWait(driver, 15).until(
            lambda driver: EC.text_to_be_present_in_element((By.TAG_NAME, "h1"), "Finished")
        )
    grasp(driver)
    driver.get(url)
    grasp(driver)
    return driver.find_element_by_css_selector("input[value='Start Quest!']")


def loop(quests, done):
    for quest in quests:
        url = "https://subeta.net/quests.php/" + quest
        driver.get(url)
        grasp(driver)
        try:
            elem = driver.find_element_by_css_selector("input[value='Start Quest!']")
        except:
            src = driver.page_source
            if '10/10' in src or '15/15' in src or '5/5' in src or 'Try Saggitarius!' in src:
                done.append(quest)
            continue
        while elem:
            try:
                elem = doQuest(elem, url)
            except:                
                if quest == "wizard":
                    driver.get("https://subeta.net/explore/wizard_exchange.php")
                    grasp(driver)
                    elem = driver.find_element_by_css_selector("input[value='Exchange your tokens automatically!']").send_keys(Keys.RETURN)
                break
    if len(quests) > len(done):
        loop(quests, done)


def shinwa():
    driver.get("https://subeta.net/explore/goddess.php")
    elem = driver.find_element_by_xpath("//input[@type='submit']")
    elem.click()

        
driver = login()

driver.get("https://subeta.net/explore/shengui_guo/bathhouse/pools.php?act=dip")
grasp(driver)
    

loop(quests, [])
driver.quit()
# requires Chrome
import re, time

from datetime import datetime, timedelta
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from login import login, OS
from finditems import grasp


LAST_PURCHASE = ("", datetime.now())
quest_names = ["quentin", "library", "carl", "cinthia", "cursed", "maleria", "pete", "blue", "wizard", "saggitarius"]

def click(elem, new_tab=False):
    if OS == "UNIX":
        if new_tab:
            elem.send_keys(Keys.COMMAND + Keys.RETURN)
        else:
            elem.click()
    else:
        if new_tab:
            elem.send_keys(Keys.CONTROL + Keys.RETURN)
        else:
            elem.send_keys(Keys.RETURN)


def shopping_page():
    grasp(driver)
    try:
        # try:
        item = driver.find_element_by_css_selector("*.btn.btn-primary.btn-sm")
        # except NoSuchElementException:
        #     driver.refresh()
        #     shopping_page()
        global LAST_PURCHASE
        delay = (datetime.now() - LAST_PURCHASE[1]) / timedelta(microseconds=1)
        if item.tag_name == "input": # buying from NPC store
            # if LAST_PURCHASE[0] == "NPC":
            time.sleep(max(5000000 - delay, 0) * .000001)
            # else:
            #     time.sleep(max(1000000 - delay, 0) * .000001)
            click(item)
            try:
                WebDriverWait(driver, 15).until(
                    lambda x: EC.title_contains("Purchasing from")
                )
            except:
                driver.execute_script("window.history.go(-1)")
                driver.refresh()
                shopping_page()
            LAST_PURCHASE = ("NPC", datetime.now())
        else:
            time.sleep(max(1000000 - delay, 0) * .000001)
            click(item)
            try:
                WebDriverWait(driver, 15).until(
                    EC.visibility_of_element_located((By.ID, "purchasedContainer"))
                )
            except:
                driver.refresh()
                shopping_page()
            LAST_PURCHASE = ("user", datetime.now())
        
        if "Purchasing from" in driver.title:
            grasp(driver)
    except:
        driver.refresh()
        shopping_page()


def quest_start_page():
    try:
        elem = driver.find_element_by_css_selector("input[value='Start Quest!']")
        click(elem)
        return True
    except:
        try:
            driver.find_element_by_xpath("//button[text()='Finish Quest']") # if finish button on page, skip to progress page logic
            quest_progress_page()
        except Exception as e:
            return False # quests finished


def finish_quest():
    try:
        click(driver.find_element_by_xpath("//button[text()='Finish Quest']"))
        grasp(driver)
    except:
        driver.refresh()
        finish_quest()


def quest_progress_page():
    grasp(driver)
    items = driver.find_elements_by_partial_link_text("Shop Search")
    for item in items:
        # item.send_keys(Keys.CONTROL + Keys.RETURN) # windows
        click(item, True)
    while len(driver.window_handles) > 1:
        driver.switch_to.window(driver.window_handles[1])
        # elem = WebDriverWait(driver, 60).until(lambda driver: driver.execute_script('return document.getElementsByClassName().length > 0') == 'true')
        shopping_page()
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    # driver.switch_to_window(main_window) # needs to not be here in Mac
    finish_quest()


def check_inventory():
    pass


def finish_page(driver):
    finished = EC.text_to_be_present_in_element((By.TAG_NAME, "h1"), "Finished")
    error = EC.text_to_be_present_in_element((By.CLASS_NAME, "alert-heading"), "Oh No!")
    if finished or error:
        return True
    return False


def doQuest(url):
    driver.get(url)
    grasp(driver)
    try:
        # driver.find_elements_by_class_name("ui message") # Doesn't work in Windows
        driver.find_elements_by_xpath("//div[@class='ui message']")
        if quest_start_page():
            quest_progress_page()
        else:
            return driver.page_source
    except Exception as e:
        print(e)
        quest_progress_page()
    # driver.get(url + "/finish")
    try:
        WebDriverWait(driver, 15).until( finish_page )
    except:
        driver.refresh()
        WebDriverWait(driver, 15).until( finish_page )
        grasp(driver)
    try:
        driver.find_element_by_xpath("//h4[contains(text(), 'Oh No!')]")
        driver.execute_script("history.back();") # TODO: buy only missing item
        quest_progress_page() # TODO: buy only missing item
    except NoSuchElementException:
        pass

    driver.get(url)
    grasp(driver)

    return driver.page_source
    # try:
    #     time.sleep(2)
    #     # WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH, "//input[@type='submit']")))
    #     return driver.find_element_by_css_selector("input[value='Start Quest!']")
    # except:
    #     return False


def loop(quests, done):
    for quest in quests:
        url = "https://subeta.net/quests.php/" + quest
        src = doQuest(url)
        # while elem is not False:
        #     try:
        #         click(elem)
        #         elem = doQuest(url)
        #     except:                
        #         if quest == "wizard":
        #             driver.get("https://subeta.net/explore/wizard_exchange.php")
        #             grasp(driver)
        #             click(driver.find_element_by_css_selector("input[value='Exchange your tokens automatically!']"))
        #         break
        # src = driver.page_source
        quests_complete = ['10/10', '15/15', '16/16', '16/15', '5/5', 'that much sP']
        while not any(x in src for x in quests_complete):
            src = doQuest(url)
        done.append(quest)
    if len(quests) > len(done):
        loop(quests, done)


def shinwa():
    driver.get("https://subeta.net/explore/goddess.php")
    WebDriverWait(driver, 15).until(
        EC.title_is("Temple of Shinwa - Subeta")
    )
    grasp(driver, EC.element_to_be_clickable((By.XPATH, "//input[@type='submit']")))
    try:
        click(driver.find_element_by_xpath("//input[@type='submit']"))
        WebDriverWait(driver, 15).until(
            EC.text_to_be_present_in_element((By.TAG_NAME, "h1"), "Thank you!")
        )
    except:
        try:
            driver.find_element_by_xpath("//a[@class='btn btn-primary']")
            pass
        except:
            return
    try:
        quest_url = driver.find_element_by_xpath("//b/a").get_attribute('href')
        doQuest(quest_url)
        shinwa()
    except Exception as e:
        return # Shinwa finished(?)
    

if __name__ == "__main__":
    driver = login()
        
    loop(["sarah"], [])
    shinwa()
    loop(quest_names, [])
    driver.quit()

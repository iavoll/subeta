# requires Chrome
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import random, re, sys, time

from login import login, stash as shop_id
from finditems import grasp


time_remaining = re.compile(r'(?ms)You have(?:[ <b>]*(?P<hour>\d+)[ <b>\/]*hours*)?[ <b>]*(?P<min>\d+)[ <b>\/]*minutes*[ <b>and]*(?P<sec>\d+)[ <b>\/]*seconds*')

_, id, *target = sys.argv
if target:
    try:
        budget = int(target[0])
    except:
        budget = None
        description = str(target[0])
        print(description)
else:
    budget = None
    description = None

def rechercher(driver, default):
    captured_time = re.search(time_remaining, driver.page_source)
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
    driver.get(f"https://subeta.net/shop.php?shopid={id}")
    grasp(driver)
    try:
        items = driver.find_elements_by_xpath("//form[contains(@action, 'shop.php')]")
        # if budget is None:
            # elem = items[0].find_element(By.XPATH, ".//input[@class='ui image']")
        if description is not None:
            links = [x.find_element(By.XPATH, ".//input[@class='ui image']") for x in items
                     if description in x.text]
            elem = links[random.randrange(len(links))]
        elif budget is not None and budget > 0:
            links = [x.find_element(By.XPATH, ".//input[@class='ui image']") for x in items
                     if int(x.find_element(By.XPATH, ".//font/b").text.replace(",", "").split()[0]) < budget]
            elem = links[random.randrange(len(links))] # anything within budget
        #elif budget == 0:
        else:
            #links = [x.find_element(By.XPATH, ".//input[@class='ui image']") for x in
            #         sorted(items, key=lambda x:int(x.find_element(By.XPATH, ".//font/b").text.replace(",", "").split()[0]))]
            #elem = links[0] # cheapest thing
            elem = min(items, key=lambda x:int(x.find_element(By.XPATH, ".//font/b").text.replace(",", "").split()[0])).find_element(By.XPATH, ".//input[@class='ui image']") # cheapest thing
        elem.click()
        WebDriverWait(driver, 30).until( EC.title_contains('Purchasing from') )
        grasp(driver)
        source = driver.page_source
        
        if 'This item was already purchased.' in source:
            #camp(driver)
            return
        elif "You have too many items" in source:
            driver.get(f"https://subeta.net/user_shops.php/mine/{shop_id}/quick_stock")
            driver.find_element_by_xpath("//button[@x-type='wardrobe']").click()
            driver.find_element_by_xpath("//input[@value='Stock Now']").click()
            driver.execute_script("history.back();")
            driver.find_element_by_xpath("//button[@x-type='shop']").click()
            driver.find_element_by_xpath("//input[@value='Stock Now']").click()
            return
            
        while not any(x in source for x in ['Sold Out!', "You have too many items"]):
            time.sleep(5)
            driver.refresh() 
            WebDriverWait(driver, 30).until( EC.title_contains('Purchasing from') )
            grasp(driver)
            source = driver.page_source
        return
        #else:
        #    time.sleep(5)
        #camp(driver)
    except:
        time.sleep(11) # prime number so as not to line up with restock schedule
        return
    #camp(driver)


driver = login()
while True:
    camp(driver)
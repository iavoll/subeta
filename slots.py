from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import re, requests, sys, time
from login import headless_login, login, stash as shop
from finditems import grasp, headless_grasp
from dailies import coinMachine


slots_hash = re.compile(r"hash_sub['\"] value=['\"](.*?)['\"]>")
# result = re.compile(r"<h1>(.*?)</h1>")
quick_stock_items = re.compile(r"name=['\"]([mass|items].*?)['\"]")
slots_url = "https://subeta.net/games/slots.php"
coin_redemption_url = "https://subeta.net/explore/coinmachine.php?coin=9"
quick_stock_view = f"https://subeta.net/user_shops.php/mine/{shop}/quick_stock"
quick_stock_action = f"https://subeta.net/user_shops.php/mine/{shop}/qs"


slots_hash = re.compile(r"hash_sub['\"] value=['\"](.*?)['\"]>")
result = re.compile(r"<h1>(.*?)</h1>")
quick_stock_items = re.compile(r"name=['\"]([mass|items].*?)['\"]")
slots_url = "https://subeta.net/games/slots.php"
coin_redemption_url = "https://subeta.net/explore/coinmachine.php?coin=9"
quick_stock_view = f"https://subeta.net/user_shops.php/mine/{shop}/quick_stock"
quick_stock_action = f"https://subeta.net/user_shops.php/mine/{shop}/qs"


def play():
    try:
        driver.find_element_by_xpath("//input[@type='submit']").click()
        WebDriverWait(driver, 10).until(
            EC.title_is("Slots - Subeta")
        )
        grasp(driver)
    except:
        driver.get(f"https://subeta.net/user_shops.php/mine/{shop}/quick_stock")
        grasp(driver)
        driver.find_element_by_xpath("//button[@x-type='shop']").click()
        driver.find_element_by_xpath("//input[@type='submit']").click()
        grasp(driver)

        driver.get("https://subeta.net/games/slots.php")
        WebDriverWait(driver, 10).until(
            EC.title_is("Slots - Subeta")
        )
        grasp(driver)


def headless_play(s, hash_sub=None):
    try:
        if hash_sub is None:
            r = s.get(slots_url, timeout=1)
            hash_sub = slots_hash.findall(r.text)[0]
        r = s.post(slots_url, timeout=1, data=dict(hash_sub=hash_sub, act="spin")).text
        if "Oops, you have too many items in your" in r:
            headless_restock(s)
            return None
        elif "hash_sub" in r:
            # try:
            #     print(result.findall(r)[0])
            # except:
            #     pass
            new_hash = slots_hash.findall(r)[0]
        if "Slots Coin" in r:
            r = s.get(coin_redemption_url, timeout=1).text
            headless_grasp(s, r)
            # print("coin redeemed")
        return new_hash
    except Exception as e:
        #print(e)
        return None


def headless_restock(s):
    try:
        r = s.get(quick_stock_view, timeout=1).text
        headless_grasp(s, r)
        items = quick_stock_items.findall(r)
        r = s.post(quick_stock_action, data={x: "wardrobe" for x in items}).text
        headless_grasp(s, r)
        r = s.post(quick_stock_action, data={x: "shop" for x in items})
        headless_grasp(s, r)
        # print("stocked")
    except Exception as e:
        #print(e)
        headless_restock(s)


def selenium_version():
    driver = login()
    driver.get("https://subeta.net/games/slots.php")
    WebDriverWait(driver, 10).until(
        EC.title_is("Slots - Subeta")
    )
    while True:
        play()


def headless_version():
    s = headless_login()
    x = headless_play(s)
    while True:
        x = headless_play(s, x)


if __name__ == "__main__":
    headless_version()

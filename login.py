import requests

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

from finditems import grasp

OS = "UNIX"
pets = [0,0,0,0]
shop = 0
stash = 0
headers = {
    "Host": "subeta.net",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:83.0) Gecko/20100101 Firefox/83.0",
    "Accept": "text/javascript, text/html, application/xml, text/xml, */*",
    "Accept-Language": "en-US,en;q=0.5",
    "X-Requested-With": "XMLHttpRequest",
    "X-Prototype-Version": "1.7.2",
    "Content-type": "application/x-www-form-urlencoded",
    "Origin": "https://subeta.net",
    "Connection": "keep-alive"
}
login_form = {
    "Name": "",
    "Password": "",
    "act": "login",
    "actcode": "",
    "enhanced": "1",
    "Login": "Login"
}
chromedriver_location = "./chromedriver"

def login():
    driver = webdriver.Chrome(chromedriver_location)

    driver.get("https://subeta.net/inventory.php")
    main_window = driver.current_window_handle
    #log in
    elem = driver.find_element_by_name("Name")
    elem.clear()
    elem.send_keys(login_form["Name"])
    elem = driver.find_element_by_name("Password")
    elem.clear()
    elem.send_keys(login_form["Password"])
    elem.send_keys(Keys.RETURN)
    WebDriverWait(driver, 10).until(
        EC.title_is("News - Subeta")
    )
    grasp(driver)
    return driver


def headless_login():
    s = requests.Session()
    s.post("https://subeta.net/login.php", data=login_form, headers=headers)

    return s

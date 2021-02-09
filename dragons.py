from lxml import etree, html
import re
import requests
import time
from login import headless_login


quest_page = "https://subeta.net/explore/farmers_market.php?act=minion"


def check_page():
    r = s.get(quest_page, timeout=3)
    try:
        page = html.fromstring(r.content)
        item = page.xpath("//i/b/text()")[0]
    except:
        return False
    r = s.get(f"https://subeta.net/isearch.php?search={item.replace(' ', '+')}")



s = headless_login()

while True:
    if check_page():
        time.sleep
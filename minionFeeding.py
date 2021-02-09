import datetime
import lxml.html
from math import inf
import re
import requests
import sys
import time
from login import headless_login, shop, stash

base_url = "https://subeta.net"
minion_url = "https://subeta.net/explore/trapped.php"
search_url = "https://subeta.net/isearch.php"
item_id_pattern = re.compile(r"Item ID: (\d+)")


def check_account(s, item_name):
    r = s.get(search_url + "?search=" + item_name)
    if "found in your <a href='/inventory.php'>Inventory" in r.text:
        print(item_name, "found in inventory")
        return True
    # root = lxml.html.fromstring(r.text)
    # links = root.xpath("//span[text()='(Remove One)']")
    # [x for x in links if x.attrib["data-loc"] == "vault"]
    try:
        item_id = item_id_pattern.findall(r.text)[0]
    except:
        check_account(s, item_name)
    if "found in your shop" in r.text:
        r = s.post(search_url, data={
            "remove": item_id,
            "loc": "shop",
            "id": shop
        })
        print(item_name, "found in shop")
        return True
    elif "found in your gallery" in r.text:
        r = s.post(search_url, data={
            "remove": item_id,
            "loc": "gallery",
            "id": stash
        })
        print(item_name, "found in gallery")
        return True
    return False


def check_page(s, count, target):
    r = s.get(minion_url)
    root = lxml.html.fromstring(r.text)
    try:
        elements = root.xpath("//a/span/div/img/../../..")
    except:
        check_page(s, count, target)
    for minion in elements:
        item_name = minion[0][0][0].attrib["alt"]
        # print(item_name)
        if check_account(s, item_name):
            r = s.get(base_url + minion.attrib["href"])
            if "Thank you for volunteering" in r.text:
                count += 1
                if count == target:
                    return count
                time.sleep(5)
    return count


def loop(s, target=inf):
    count = 0
    while count < target:
        count = check_page(s, count, target)
        print(count)
        minutes = datetime.datetime.now().minute
        time.sleep((5 - minutes % 5) * 60)


if __name__ == "__main__":
    s = headless_login()
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = inf
    loop(s, target)
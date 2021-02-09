from datetime import datetime, timedelta
import requests
import re
import time

from login import headless_login, shop

snowball_purchase_url = "https://subeta.net/ss.php/snowballs/buy"
snowtapult_url = "https://subeta.net/explore/snowball.php?act=use&snowball="
snowtapult_hash = re.compile(r'"random" value="true"><input type="hidden" name="hash" value="([a-zA-Z0-9]+)">')
error = re.compile(r'Oh No!</h4>\s*(.*?)\s*<hr>')
items = {
    "Spidery Snowball": 158395,
    "Frosty Snowball": 131564
}


def buy(s, item_id, last_bought):
    data = {
        "itemid": item_id
    }
    r = s.post(snowball_purchase_url, data=data)
    if "Oh No!" in r.text:
        delay = (datetime.now() - last_bought)
        print("failed to buy", delay)
        # print("failed to buy", error.findall(r.text))
        delay = delay / timedelta(microseconds=1)
        # time.sleep(max(30000000 - delay, 0) * .000001)
        time.sleep(max(5000000 - delay, 0) * .000001)
        return buy(s, item_id, datetime.now())
    # print("successfully bought")
    # print(datetime.now())
    return datetime.now()


def fire(s, item_name, last_thrown):
    r = s.get(snowtapult_url + item_name)
    try:
        find_hash = snowtapult_hash.findall(r.text)[0]
        r = s.get(snowtapult_url + item_name + "&act=fire&random=true&hash=" + find_hash)
        if "Oh No!" in r.text:
            delay = (datetime.now() - last_thrown) / timedelta(microseconds=1)
            print("failed to throw", error.findall(r.text), max(5000000 - delay, 0) * .000001)
            time.sleep(max(5000000 - delay, 0) * .000001)
            return fire(s, item_name, datetime.now())
        else:
            print("successfully threw", datetime.now())
            return datetime.now()
    except Exception as e:
        print("throwing error", e)
        return fire(s, item_name, datetime.now())
        


def loop(s, item_name, last_bought, last_thrown):
    purchase = buy(s, items[item_name], last_bought)
    # if not purchase:
    #     time.sleep(10)
    #     return
    throw = fire(s, item_name, last_thrown)
    # if throw:
    #     time.sleep(5)
    time.sleep(5)
    return purchase, throw


if __name__ == "__main__":
    s = headless_login()
    last_bought = datetime.now()
    last_thrown = datetime.now()
    while True:
        last_thrown = fire(s, "Frosty Snowball", last_thrown)
        time.sleep(4)
        # last_bought, last_thrown = loop(s, "Spidery Snowball", last_bought, last_thrown)


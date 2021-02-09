import requests
import threading
import time

from login import headless_login, stash, shop

shop_search_url = f"https://subeta.net/user_shops.php/mine/{shop}?stocked_operator=eq&stocked=&category=&rarity=&use=&name="
recycle_action_url = "https://subeta.net/explore/recycle_beast.php?act=give_process&itemid="

def get_from_stash(s, item_name, item_id):
    data = {
        "act": "edit",
        f"category[{item_id}]": "None",
        f"remove[{item_id}]": "100",
        "destination": "Inventory"
    }
    r = s.post(shop_search_url + item_name, data=data)
    # print(r.text)


def submit_recycle(s, item_id, i):
    data = {
        "amount": 100
    }
    r = s.post(recycle_action_url + item_id, data=data)
    print("attempted recycle", i)


def recycle_thread(s, item_id):
    while True:
        submit_recycle(s, item_id)


if __name__ == "__main__":
    s = headless_login()
    item_name = "Slots Spork".replace(" ", "+")
    item_id = "278"
    i = 1
    while True:
        get_from_stash(s, item_name, item_id)
        submit_recycle(s, item_id, i)
        i += 1
        time.sleep(900)
    # recycle = threading.Thread(target=recycle_thread, args=(s, item_id))
    # recycle.start()


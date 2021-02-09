# requires Chrome
import datetime, os, random, re, sys, time, winsound

from login import headless_login, shop as shop_id
from finditems import grasp

item_ids = re.compile(r'value="(\d+)"')
url = "https://subeta.net/explore/blackheart.php"
time_remaining = re.compile(r'(?ms)You have(?:[ <b>]*(?P<hour>\d+)[ <b>\/]*hours*)?[ <b>]*(?P<min>\d+)[ <b>\/]*minutes*[ <b>and]*(?P<sec>\d+)[ <b>\/]*seconds*')

def rechercher(driver, default):
    captured_time = re.search(time_remaining, driver.page_source)
    if captured_time:
        time = 60 * int(captured_time.group('min')) + int(captured_time.group('sec'))
        if captured_time.group('hour'):
            time += 3600 * int(captured_time.group('hour'))
        print(time)
        return time
    else:
        #print(default)
        return default


def camp(s, offset, cooldown, success):
    r = s.get(url).text
    if "It'd be best if you didn't come around for a while." in r:
        if success: # if last attempt didn't also trigger cooldown
            offset += 10
        else: # if cooldown violated
            cooldown += 10
        print(offset, cooldown, str(datetime.datetime.now()))
        time.sleep(cooldown)
        return offset, cooldown, False
    elif "There doesn't seem to be anything here!" not in r:
        with open('./blackheart_logs/' + str(datetime.datetime.now()).replace(":", "_") + ".html", "w+") as f:
            f.write(r)
        items = item_ids.findall(r)
        while 'Oh No!' not in r.text:
            try:
                r = s.post(url, data={
                    "act": "buy",
                    "id": str(random.choice(items)),
                    "buy.x": "46",
                    "buy.y": "9"
                })
            except:
                break

    # time.sleep(offset)
    time.sleep(offset) # this sleep = attempt to evade cooldown
    return offset, cooldown, True
    #camp(driver)


s = headless_login()
print(datetime.datetime.now())
cooldown = 1200 # redefine offset = cooldown; max = 1850
offset = 300 # max = 650
success = True
# offset = 360 # calculated probable limit
# offset = 1050 # max reached so far, may be due to cooldown being > triggering interval
while True:
    offset, cooldown, success = camp(s, offset, cooldown, success)
import re
import requests
import sys

from login import headless_login

url = "https://subeta.net/explore/mystery_box.php"
result = re.compile(r'<p>(.*?)<\/p>\s*<a href=["\']mystery_box.php["\']>Back to the Box<\/a>')

def buy(s, count):
    i = 0
    while i < count:
        r = s.get(url)
        r = s.get(url + "?act=buy")
        print(result.findall(r.text)[0])
        i += 1

if __name__ == "__main__":
    s = headless_login()
    s.headers.update({"Referer": url})
    count = int(sys.argv[1])
    buy(s, count)

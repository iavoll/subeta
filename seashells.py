from login import headless_login
import re
from random import choice
import sys

base_url = "https://subeta.net/games/seashell_spotter.php"
sample_pattern = re.compile(r"-image:url\((.*?)\)")
# fallback_pattern = re.compile(rf"a href=['\"](.*?)['\"]><img src=")
# result_pattern = re.compile(r"(Your .* daily win streak is \d+ correct guesses.)")
sp_pattern = re.compile(r"[\d,]+ sP")


def guess(img_url):
    r = s.get(base_url)
    pattern = re.compile(rf'a href="(\?guess=\d)"><img src={img_url}')
    # print(r.text)
    result_url = pattern.findall(r.text)
    # print(result_url)
    if len(result_url) > 2:
        r = s.get(base_url + choice(result_url))
    else:
        r = s.get(base_url + result_url[0])
    try:
        # print(result_pattern.findall(r.text)[0])
        print(sp_pattern.findall(r.text)[0])
        return True
    except Exception as e:
        return False
    

def memorize():
    r = s.get(f"{base_url}?start=true")
    img_url = sample_pattern.findall(r.text)
    # print(img_url)
    try:
        return img_url[0]
    except:
        return ''


def play():
    img_url = memorize()
    return guess(img_url)


if __name__ == "__main__":
    s = headless_login()
    if len(sys.argv) > 1 and sys.argv[1] == "all":
        earned = True
        while earned:
            earned = play()
    else:
        play()
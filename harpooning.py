from math import ceil, floor, inf, sqrt
from itertools import takewhile
from random import sample
import re
import requests
import sys

from login import headless_login
base_url = "https://subeta.net/games/battleship.php"
link = re.compile(r'<a href="\?move=(\d+)"><img')

def guess(s, n):
    # # print("guess ", n)
    r = s.get(f"{base_url}?move={n}", allow_redirects=False)
    try:
        result = r.headers["location"]
    except:
        result = ''
    # print("guess", n, result == "?game=set&text=1")
    if result == "?game=set&text=2":
        return False
    elif result == "?game=set&text=1":
        r = s.get(base_url + result)
        # print("found on map: ", r.text.count("battleship_tile_monster") - 1)
        return True
    return None


def follow(s, result, candidates, choices, found):
    # print("follow", found)
    for n in candidates:
        result = guess(s, n)
        if result is not None and result:
            choices -= {n}
            found += 1
        else:
            break
    return choices, found
    # except Exception as e:
    #     # print (e)
    #     return choices, found


def start(s):
    s.get(f"{base_url}?set=nothing")
    s.get(f"{base_url}?create=game")


def play(s, found=0, target=inf):
    # print("game begun")
    r = s.get(f"{base_url}?game=set")
    links = link.findall(r.text)
    size = ceil(sqrt(int(links[-1])))
    # if "rough_water.png" in r:
    choices = set(int(x) for x in links)
    # else:
    #     choices = {x for x in range(pow(size, 2))}
    
    # n = sample(choices, 1)[0]
    while True:
        n = sample(choices, 1)[0]
        choices.discard(n)
        result = guess(s, n)
        if result is None:
            break
        elif result:
            old_found = found = found + 1
            # print("random", found)
            left = takewhile(lambda x: x in choices, range(n-1, floor(n/size)*size, -1))
            right = takewhile(lambda x: x in choices, range(n+1, ceil(n/size)*size, 1))
            choices, found = follow(s, True, left, choices, found)
            # print("left", found)
            choices, found = follow(s, True, right, choices, found)
            # print("right", found)
            # print("old found", old_found)
            if old_found == found:
                above = takewhile(lambda x: x in choices, range(n - size, 0, 0 - size))
                below = takewhile(lambda x: x in choices, range(n + size, size * size, size))
                choices, found = follow(s, True, above, choices, found)
                choices, found = follow(s, True, below, choices, found)
        if found >= target:
            return found
    start(s)
    # print("game ended")
    return found


if __name__ == "__main__":
    s = headless_login()
    s.headers.update({"Referer": f"{base_url}?game=set"})
    start(s)
    found = 0
    if len(sys.argv) > 1:
        target = int(sys.argv[1])
        while found < target:
            found = play(s, target=target, found=found)
    else:
        while True:
            found = play(s)
            # print(found)
        # found = play(s, found=found)

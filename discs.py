import itertools
import json
import requests

from login import headers, headless_login

s = headless_login()

headers["Referer"] =  "https://subeta.net/games/divine_discs.php"

game = "https://subeta.net/games/divine_discs.ajax.php"


def play(move):
    # move = [5,5,5,5]

    response = s.post(game, headers=headers, data={"row": str(move)})
    return 

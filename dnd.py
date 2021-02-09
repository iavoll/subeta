import lxml.html
import re
import requests

from login import headless_login

base_url = "https://subeta.net/games/mazes_mahars/index.php"
play_result = re.compile(r'mahars\/(?:cards|dice).*?>(?:<br\s*\/>)*(.*?)(?:<br\s*\/>)')

def continue_from_result():
    data = {
        "clear": "true"
    }
    r = s.post(base_url, data=data)


def continue_from_board(card):

    data = {
        "go": "true",
        "card_1": "1",
        "card_2": "1",
        "card_3": "0",
        "card_4": "0",
        "card_5": "0"
    }
    r = s.post(base_url, data=data)
    


def play(card_id):
    r = s.get(f"{base_url}?card_choice={card_id}")


def check_board(source):
    root = lxml.html.fromstring(source)



def check_state(r):
    if '<input id="computerGo"' in r.text:
        return 0 # no interaction
    if 'value="End Turn"' in r.text:
        return 1 # interaction required

s = headless_login()
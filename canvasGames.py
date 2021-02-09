import copy
import random
import re
import requests
import sys

from login import headless_login


html_parse = re.compile(r"<div id='gameid' .*?>(\d+)</div>")

def play(s, url, start_data, score_data):
    start_data["act"] = "start"
    r = s.post(url, data=start_data)

    score_data["act"] = "score"
    try:
        score_data["id"] = r.json().get('gameid', r.text)
    except:
        if "div" in r.text:
            score_data["id"] = html_parse.findall(r.text)[0]
        else:
            score_data["id"] = r.text
    r = s.post(url, data=score_data)
    print(r.text)
    if "You have already played" in r.text:
        return False
    return True


def play_2048(s, score):
    data = {
        "act": "finish",
        "score": score
    }
    r = s.post("https://subeta.net/games/2048.php", data=data)


def play_jewels(s, url, *args):
    start_data = {
        "act": "insert",
        "type": "1" # untimed > 1.5x, timed > 2x
    }
    r = s.post(url, start_data)
    gameid = r.text
    score = random.randrange(29000, 32000, 5)
    level = random.randrange(8,10)
    score_data = {
        "act": "score",
        "gameid": gameid,
        "score": score,
        "level": level,
        "secret": f"matlal{score}{level}jewels{gameid}baron"
    }
    r = s.post(url, data=score_data)
    print(r.text)
    if "You have already played" in r.text:
        return False
    return True


def compile(game):
    url = urls[game]
    start_data, score_data = data[game]
    # for i in range(10):
    function = functions.get(game, play)
    if isinstance(score_data.get("score"), range):
        instance = copy.copy(score_data)
        instance["score"]  = random.choice(score_data["score"])
        print(instance["score"])
        return function(s, url, start_data, instance)
    else:
        return function(s, url, start_data, score_data)


urls = {
    "balloonSweeper": "https://subeta.net/games/balloon_sweeper.ajax.php",
    "bugCatching": "https://subeta.net/games/bug_catching.ajax.php",
    "burrero": "https://subeta.net/games/burrero.ajax.php",
    "caliphsTomb": "https://subeta.net/games/caliphs_tomb.ajax.php",
    "flightSim": "https://subeta.net/games/flight_sim.ajax.php",
    "gravedigger": "https://subeta.net/games/gravedigger.ajax.php",
    "jewels": "https://subeta.net/games/jewels_ajax.php",
    "PeteSays": "https://subeta.net/games/pete_says.ajax.php",
    "piratePanic": "https://subeta.net/games/pirate_panic.ajax.php",
    "promoter": "https://subeta.net/games/promoter.ajax.php",
    "raceway": "https://subeta.net/games/raceway.ajax.php",
    "sledding": "https://subeta.net/games/sledding.ajax.php",
    "SahericSlide": "https://subeta.net/games/sliding_puzzle.ajax.php",
    "spectrail": "https://subeta.net/games/spectrail.ajax.php"
}

data = {
    "balloonSweeper": ({}, {"score": "1", "difficulty": "2"}),
    "bugCatching": ({}, {"score": range(60, 70)}),
    "burrero": ({}, {"score": range(2500, 2800)}),
    "caliphsTomb": ({"layout": "3"}, {"score": "53"}),
    "flightSim": ({}, {"score": "4900", "won_game": "true"}),
    "gravedigger": ({}, {"score": range(4710, 4730), "rows": "199", "depth": "199"}),
    "jewels": ({}, {}),
    "PeteSays": ({}, {"score": "30"}),
    "piratePanic": ({}, {"score": range(170, 270), "wave": "15"}),
    "promoter": ({"bandid": "false"}, {"score": range(200, 205)}),
    "raceway": ({}, {"difficulty": "1.5", "score": range(13800, 14000)}),
    "sledding": ({}, {"score": range(60000, 70000)}),
    "SahericSlide": ({"size": "6"}, {"grid_size": "6"}),
    "spectrail": ({}, {"score": range(670, 800)})
}

functions = {
    "jewels": play_jewels,
    "2048": play_2048
}


if __name__ == "__main__":
    s = headless_login()
    if len(sys.argv) == 2:
        compile(sys.argv[1])
    elif len(sys.argv) == 3:
        play_2048(s, sys.argv[2])
    else:
        for game in urls:
            for i in range(10):
                result = compile(game)
                if not result:
                    break
        
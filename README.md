# Assorted Subeta scripts

These are a collection of scripts that automate almost all site functions on Subeta. Please note that as written, they are **not** rate-limited: only site-enforced rate-limited is written in. Therefore, if you wish to avoid detection, add some sleeps.

There are 2 kinds of scripts here: Selenium scripts, which run a browser and in my experience don't work if your screen goes to sleep, and headless scripts that run however Python scripts run on your computer. Selenium scripts are slower and buggier, but the critical shopping quest script is a Selenium script so it's worth setting up. There are both headless and Selenium options for playing Slots, which is a major income source.

## Setup

1. Fill in `login.py` with your login info. Strings go between quote marks and IDs can be integers. Go on your pet and shop pages to find their IDs; I used one shop for selling things and one gallery for storing excess items (called `stash` in the code).

2. Install [Python](https://www.python.org/downloads/) if you don't already have it.
    1. If on Mac or Linux, use Terminal \(or your choice of terminal emulator\) to run Python scripts. You can install python by running `brew install python3` in Terminal as well.
    2. If on Windows, I recommend Git Bash. However, the scripts may still work in Powershell.

3. Download the package \(`git clone` or simply download the files and save them in a folder\).

4. While in the package directory, install the Python environment.
    1. Install virtualenv if you don't already have it \(`pip install virtualenv`\).
    2. Create a virtual environment \(`virtualenv venv`\) and activate it \(`source venv/bin/activate`\).
    3. Install the required packages \(`pip install -r requirements.txt`\).

5. If running Selenium scripts, download [chromedriver](https://chromedriver.chromium.org/downloads) into the package directory. Add this location to `login.py`.
    - Unfortunately, Selenium for Firefox was too buggy on the computers on which I developed these scripts, so I only developed them for Chrome. If necessary, download Chrome and download the matching version of Chromedriver.

6. Run scripts from command line (`python subetaQuests.py`) and watch the magic happen.
import json
import urllib
import random

def get_random_commander(): #not actually random picks from popular commanders
    URL = "https://edhrec-json.s3.amazonaws.com/en/commanders.json"
    page = urllib.request.urlopen(URL)
    data = json.loads(page.read().decode())

    iterate = 0
    commanders = []
    for i in data['container']['json_dict']['cardlists']:
        jiterate = 0
        for j in data['container']['json_dict']['cardlists'][iterate]['cardviews']:
            commanders.append(data['container']['json_dict']['cardlists'][iterate]['cardviews'][jiterate]['name'])
            jiterate += 1
        iterate += 1
    commander = random.choice(commanders)
    return commander


def get_url():
    print("Welcome NetDeckV2!")
    print("Use the -b OR -t options for budget (cheap/expensive) or theme respectively. "
          "Use random instead of a commander name to get a random popular commander.")
    print("Example: Edgar Markov -b expensive")

    commander = input("Enter your Commander: ")
    if "random" in commander:
        commander = commander.replace("random", get_random_commander())
    if "-b" in commander:
        x = commander.split(" -b")
        commander = x[0] + x[1] + " budget"
    if "-t" in commander:
        x = commander.split(" -t")
        if x[1] == " +1/+1 counters":
            x[1] = " p1 p1 counters"
        elif x[1] == " -1/-1 counters":
            x[1] = " m1 m1 counters"
        commander = x[0] + x[1] + " theme"
    commander = commander.replace(' ', '-').lower()
    commander = commander.replace(',', '').lower()
    commander = commander.replace("'", '').lower()

    URL = "https://edhrec-json.s3.amazonaws.com/en/commanders/" + commander + ".json"

    return URL
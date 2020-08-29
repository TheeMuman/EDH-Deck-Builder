import urllib.request
import json
import random


class Card:
    def __init__(self, name, percent, cmc, c_type, colors):
        self.name = name
        self.percent = percent
        self.cmc = cmc
        self.type = c_type
        self.colors = colors


def get_cards(data):
    iterate = 0
    cards = []
    for i in data:
        jiterate = 0
        for j in data[iterate]['cardviews']:
            cards.append(Card(data[iterate]['cardviews'][jiterate]['name'],
                              int(data[iterate]['cardviews'][jiterate]['label'][:data[iterate]['cardviews'][jiterate]['label'].find("%")]),
                              data[iterate]['cardviews'][jiterate]['cmc'],
                              data[iterate]['cardviews'][jiterate]['primary_type'],
                              data[iterate]['cardviews'][jiterate]['color_identity']))
            jiterate += 1
        iterate += 1
    return cards


def make_deck(cards, land_avg, basic_avg, c_colors, c_name):  # where the magic happens
    playables = []
    non_basic_land = []
    lands_left = land_avg + random.randrange(0, 3, 1)
    basics_left = basic_avg
    non_basics_left = lands_left - basics_left
    playables_left = 99 - lands_left

    basics = [sub.replace('G', 'Forest') for sub in c_colors]
    basics = [sub.replace('B', 'Swamp') for sub in basics]
    basics = [sub.replace('R', 'Mountain') for sub in basics]
    basics = [sub.replace('U', 'Island') for sub in basics]
    basics = [sub.replace('W', 'Plains') for sub in basics]
    basics = [sub.replace('', 'Wastes') for sub in basics]

    for card in cards:  # Find auto includes
        if card.percent >= 50 and card.type != "Land" and playables_left > 0 and card.name != c_name:
            playables.append(card)
            cards.remove(card)
            playables_left -= 1
        elif card.percent >= 40 and card.type == "Land" and non_basics_left > 0:
            non_basic_land.append(card)
            cards.remove(card)
            lands_left -= 1
            non_basics_left -= 1

    while playables_left > 0 or non_basics_left > 0:  # Fill in rest of playables and non-basics
        for card in cards:
            odds_weight = card.percent / 100 / 2
            if card.type != "Land" and playables_left > 0:
                if random.random() < odds_weight:
                    playables.append(card)
                    playables_left -= 1
                    cards.remove(card)
            elif card.type == "Land" and non_basics_left > 0:
                if random.random() < odds_weight:
                    non_basic_land.append(card)
                    lands_left -= 1
                    non_basics_left -= 1
                    cards.remove(card)

    playables_colors =[]
    for playable in playables:
        if not playable.colors:
            continue
        else:
            playables_colors.append(playable.colors)
    basic_land = get_basics(playables_colors, basics_left)
    basics_left -= len(basic_land)
    lands_left -= len(basic_land)  # just in case we want this count later
    while basics_left > 0:  # just in case rounding misses one
        basic_land.append(random.choice(basics))
        lands_left -= 1
        basics_left -= 1

    # make the final list
    deck = []
    for playable in playables:
        deck.append(playable.name)
    for non_basic in non_basic_land:
        deck.append(non_basic.name)
    for basic in basic_land:
        deck.append(basic)
    deck.append(c_name + " `Commander`")
    return deck


def get_basics(playables_colors, basics_left): #get the basic lands since
    red, blue, green, white, black = 0, 0, 0, 0, 0
    here_be_basics = []
    total_basics = basics_left
    
    if not playables_colors: #if you are in colorless for some reason
        while basics_left > 0:
            here_be_basics.append('Wastes')
            basics_left -= 1
        return here_be_basics
    else: #else do normal basic land adding
        for i in playables_colors:
            for j in i:
                if j == 'R':
                    red += 1
                if j == 'B':
                    black += 1
                if j == 'G':
                    green += 1
                if j == 'U':
                    blue += 1
                if j == 'W':
                    white += 1

        red_f = red / (blue+green+black+white+red)
        blue_f = blue / (blue+green+black+white+red)
        green_f = green / (blue+green+black+white+red)
        black_f = black / (blue+green+black+white+red)
        white_f = white / (blue+green+black+white+red)

        red = round(red_f * basics_left)
        blue = round(blue_f * basics_left)
        green = round(green_f * basics_left)
        black = round(black_f * basics_left)
        white = round(white_f * basics_left)

        while red > 0:
            here_be_basics.append('Mountain')
            red -= 1
            basics_left -= 1
        while blue > 0:
            here_be_basics.append('Island')
            blue -= 1
            basics_left -= 1
        while green > 0:
            here_be_basics.append('Forest')
            green -= 1
            basics_left -= 1
        while black > 0:
            here_be_basics.append('Swamp')
            black -= 1
            basics_left -= 1
        while white > 0:
            here_be_basics.append('Plains')
            white -= 1
            basics_left -= 1

        if len(here_be_basics) > total_basics:
            here_be_basics.pop()

        return here_be_basics


def format_list(deck):  # formatted printing
    deck.sort()
    deck_dic = dict()

    for card in deck:
        if card in deck_dic:
            deck_dic[card] += 1
        else:
            deck_dic[card] = 1

    deck_dic = {key: value for key, value in deck_dic.items() if value > 0}

    for key, value in deck_dic.items():
        print(value, key)

    print("Size of deck with commander is:", len(deck))


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


def __main__():
    URL = get_url()
    try:
        page = urllib.request.urlopen(URL)
    except:
        print("Problem getting the URL, check spelling and try again")

    data = json.loads(page.read().decode())

    # data for card objects
    cards = get_cards(data['container']['json_dict']['cardlists'])

    # data for decision making
    land_avg = data['land']
    basic_avg = data['basic']

    # commander data
    c_colors = data['container']['json_dict']['card']['color_identity']  # commander color requirements
    commander_name = data['container']['json_dict']['card']['name']  # commander's name

    deck = make_deck(cards, land_avg, basic_avg, c_colors, commander_name)
    format_list(deck)


__main__()

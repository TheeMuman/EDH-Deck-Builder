
import json
import urllib.request

import getURL
import getCardPool
import printList
import buildDeck


def __main__():
    URL = getURL.get_url()
    try:
        page = urllib.request.urlopen(URL)
    except:
        print("Problem getting the URL, check spelling and try again")

    data = json.loads(page.read().decode())

    # data for card objects
    cards = getCardPool.get_cards(data['container']['json_dict']['cardlists'])

    # data for decision making
    land_avg = data['land']
    basic_avg = data['basic']

    # commander data
    c_colors = data['container']['json_dict']['card']['color_identity']  # commander color requirements
    commander_name = data['container']['json_dict']['card']['name']  # commander's name

    deck = buildDeck.make_deck(cards, land_avg, basic_avg, c_colors, commander_name)
    printList.format_list(deck)


__main__()


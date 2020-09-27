import random
import basicLands


def make_deck(cards, land_avg, basic_avg, c_colors, c_name):  # where the magic happens
    playables = []
    non_basic_land = []
    lands_left = land_avg + random.randrange(0, 3, 1)
    basics_left = basic_avg
    non_basics_left = lands_left - basics_left
    playables_left = 99 - lands_left

    basic_land_types = {
        'G': 'Forest',
        'B': 'Swamp',
        'R': 'Mountain',
        'U': 'Island',
        'W': 'Plains'}
    basics = list(map(lambda e: basic_land_types[e], c_colors))
    if not basics:
        basics = ['Wastes']

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

    playables_colors = []
    for playable in playables:
        if not playable.colors:
            continue
        else:
            playables_colors.append(playable.colors)
    basic_land = basicLands.get_basics(playables_colors, basics_left)
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
    deck.append(c_name)  # where we add the commander
    return deck

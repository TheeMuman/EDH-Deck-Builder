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
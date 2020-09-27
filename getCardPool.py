from cardClass import Card

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
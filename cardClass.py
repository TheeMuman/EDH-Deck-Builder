class Card:#for our card objects
    def __init__(self, name, percent, cmc, c_type, colors):
        self.name = name
        self.percent = percent
        self.cmc = cmc
        self.type = c_type
        self.colors = colors

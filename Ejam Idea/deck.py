import random

class Deck:
    def __init__(self):
        self.cards = []  # Contains a copy of the deck
        self.deck = []  # Contains the actual deck

    def shuffle(self):
        random.shuffle(self.deck)
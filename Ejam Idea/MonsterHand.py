class MonsterHand:
    def __init__(self):
        self.inventory = [None,None,None,None,None,None]
        self.cardCnt = 0

    def newHand(self, deck):
        # Shuffle in new monster hand cards
        for i in range(len(self.inventory)):
            card = self.inventory[i]
            if card != None:
                self.inventory[i] = deck.pop()

    def update(self, deck):
        # Find the amt of remaining cards within the monster hand
        if self.cardCnt == 2: self.newHand(deck) # Add cards into the monster deck once we have 2 cards remaining



import pygame
import sys
import random


class Deck:
    def __init__(self):
        self.deck = []  # Contains the actual deck

    def shuffle(self):
        random.shuffle(self.deck)


class DungeonHand:
    def __init__(self):
        self.layouts = [Layout(129, 145, 105, 130), Layout(275, 140, 120, 137), Layout(445, 130, 120, 140),
                          Layout(117, 290, 110, 137), Layout(260, 290, 125, 135), Layout(444, 290, 130, 130)]
        self.inventory = [None, None, None, None, None, None]

    def newHand(self, deck):
        # Shuffle in new dungeon hand cards
        for i in range(len(self.inventory)):
            card = self.inventory[i]
            if card == None and len(deck) > 0:
                newCard = deck.pop()
                newCard.x = self.layouts[i].x + self.layouts[i].w/2 - newCard.w/2
                newCard.y = self.layouts[i].y + self.layouts[i].h/2 - newCard.h/2
                self.inventory[i] = newCard

    def update(self, deck):
        # Checks if we need the addition of cards into the dungeon hand
        # Find the amt of remaining cards within the dungeon hand
        cardCnt = 0
        for el in self.inventory:
            if el != None: cardCnt += 1

        if cardCnt <= 2: self.newHand(deck)  # Add cards into the dungeon deck once we have 2 cards remaining


class PlayerHand:
    def __init__(self):
        self.layouts = [Layout(380, 560, 110, 145), Layout(512, 566, 110, 145), Layout(380, 715, 110, 125),
                          Layout(509, 715, 112,135)]  # The inventory for the player should only hold the trinkets/special abilities
        self.inventory = [None, None, None, None]
        self.weaponLayout = Layout(80, 590, 120, 145)
        self.shieldLayout = Layout(220, 594, 110, 139)
        self.weapon = None
        self.shield = None


class Layout:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.card = None

    def within_border(self, x, y, w, h):
        if self.x <= x and x + w <= self.x + self.w:
            if self.y <= y and y + h <= self.y + self.h:
                return True

        return False


class Window:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.screen = pygame.display.set_mode((self.w, self.h))

    def fill(self):
        self.screen.fill((255, 255, 255))


class Card:

    def __init__(self, x, y, w, h, img):
        self.w = w
        self.h = h
        self.x = x
        self.y = y
        self.img = pygame.image.load(img)
        self.img = pygame.transform.scale(self.img, (self.w, self.h))
        self.offsetX = 0
        self.offsetY = 0

    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))

    def withinBorder(self, pos):  # Border check for seeing if mouse click is within boarder
        mx, my = pos
        if self.x < mx < self.x + self.w:
            if self.y < my < self.y + self.h:
                return True  # Clicking on it
        return False  # Not clicking it

    def moveTo(self, pos):
        mx, my = pos
        self.x = mx - self.offsetX
        self.y = my - self.offsetY

    def calculateOffset(self, pos):
        mx, my = pos
        self.offsetX = mx - self.x
        self.offsetY = my - self.y


class Mouse:
    def __init__(self):
        self.held = False  # Boolean for if the mouse is being held
        self.holdingCard = False  # Boolean for if a card is being held (Stores the actual card if this var is not False)
        self.prevCardLocation = None  # References the card's location prior to being moved (Used for snap back action)


def nextTurn(dungeonHand, deck):
    # Perform refilling of dungeon hand
    dungeonHand.update(deck)

    # Refresh shop

# SET UP AREA
#Initiate pygame
screen = Window(760, 880)
pygame.init()
clock = pygame.time.Clock()

# General usage
ability_cards = [Card(0, 0, 75, 125, "Images\Cake.png"), Card(0, 0, 75, 125, "Images\Cake.png"), Card(0, 0, 75, 125, "Images\Cake.png")] # all the ability cards that exist in the game
m = Mouse()


# Main game play variables
gameBackground = Card(0, 0, screen.w, screen.h, "Images\Gui3.png")
dungeonHand = DungeonHand()
playerHand = PlayerHand()
deck = Deck()
nextTurnButton = Layout(214,452,264,63)
shopButton = Layout(610,235,85,104)
sellButton = Layout(619,235,76,104)
deck.deck.append(Card(0, 0, 60, 100, "Images\Cake.png"))
deck.deck.append(Card(0, 0, 60, 100, "Images\Crayon.PNG"))
deck.deck.append(Card(0, 0, 60, 100, "Images\Potion.png"))
currentPage = "Gameplay"

# Can be removed later
card = Card(0, 0, 60, 100, "Images\Cake.png")
dungeonHand.inventory[3] = card

# Main shop variables
pygame.font.init()
StopToMenuButton = pygame.Rect(606,804,115,60)
myfont = pygame.font.SysFont('Century Gothic', 50)
shopBackground = Card(0, 0, screen.w, screen.h, "Images\ShopGui.png")
refresh_button = pygame.Rect(10, 10, 200, 60)
shop_cards = []

def update():
    global currentPage

    # Check inputs
    if currentPage == "Gameplay":

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                m.held = True
                pos = pygame.mouse.get_pos()
                x, y = pos
                print(pos)

                # Check for next turn click
                if nextTurnButton.within_border(x, y, 1, 1):
                    nextTurn(dungeonHand, deck.deck)

                # Check for shop click
                if sellButton.within_border(x,y,1,1):  # Transition into shop screen
                    currentPage = "Shop"
                    # Make shop
                    for i in range(len(ability_cards)):
                        card = ability_cards[i]
                        card.cost = str(random.randint(10,
                                                50))  # temporary placeholder for determining the cards' value. they will probably be pre-determined

                    x_inc = 150
                    for i in range(3):  # three shop cards will be handed out
                        ability_cards[i].x = x_inc
                        ability_cards[i].y = 150
                        shop_cards.append(ability_cards[i])
                        x_inc += 200


                # Check which card (if any) are gonna be dragged by the mouse
                for i in range(len(dungeonHand.inventory)):
                    card = dungeonHand.inventory[i]
                    if card != None:
                        if card.withinBorder(pos):
                            m.holdingCard = card
                            m.prevCardLocation = {"pos":[card.x, card.y],"location":"dungeon","i":i}
                            card.calculateOffset(
                                pos)  # Offset is required so that the card can be moved without being centered at the mouse
                            break

                for i in range(len(playerHand.inventory)):
                    card = playerHand.inventory[i]
                    if card != None:
                        if card.withinBorder(pos):
                            m.holdingCard = card
                            m.prevCardLocation = {"pos": [card.x, card.y], "location": "player", "i": i}
                            card.calculateOffset(
                                pos)  # Offset is required so that the card can be moved without being centered at the mouse
                            break

                if playerHand.shield != None:
                    card = playerHand.shield
                    if playerHand.shield.withinBorder(pos):
                        m.holdingCard = card
                        m.prevCardLocation = {"pos": [card.x, card.y], "location": "shield", "i": None}
                        card.calculateOffset(
                            pos)  # Offset is required so that the card can be moved without being centered at the mouse
                elif playerHand.weapon != None:
                    card = playerHand.weapon
                    if playerHand.weapon.withinBorder(pos):
                        m.holdingCard = card
                        m.prevCardLocation = {"pos": [card.x, card.y], "location": "weapon", "i": None}
                        card.calculateOffset(
                            pos)  # Offset is required so that the card can be moved without being centered at the mouse


            elif event.type == pygame.MOUSEBUTTONUP:
                m.held = False

                # In here, handle the ability for a card to jump back to its original position if the final position
                # doesn't belong to either dungeon or player hands

                if m.holdingCard != False:
                    # Check to see if the card fits in any player or dungeon slots
                    card = m.holdingCard
                    flag = False  # Bool for if the card has found a new slot (False = no slot found, True = slot found)

                    # See if it belongs now to player hand
                    for i in range(len(playerHand.layouts)):
                        layout = playerHand.layouts[i]
                        if layout.within_border(card.x, card.y, card.w, card.h) and playerHand.inventory[i] == None:  # Make sure that the card fits and that the slot is no occupied
                            playerHand.inventory[i] = card
                            flag = True

                    # See if it belongs now to dungeon hand
                    for i in range(len(dungeonHand.layouts)):
                        layout = dungeonHand.layouts[i]
                        if layout.within_border(card.x, card.y, card.w, card.h) and dungeonHand.inventory[i] == None:
                            dungeonHand.inventory[i] = card
                            flag = True

                    # Belongs to shield slot?
                    layout = playerHand.shieldLayout
                    if layout.within_border(card.x, card.y, card.w, card.h) and playerHand.shield == None:
                        playerHand.shield = card
                        flag = True

                    # Belongs to weapon slot?
                    layout = playerHand.weaponLayout
                    if layout.within_border(card.x, card.y, card.w, card.h) and playerHand.weapon == None:
                        playerHand.weapon = card
                        flag = True

                    # In case that the card hasn't found a new slot, we send it back to its original spot
                    if not flag:
                        card.x, card.y = m.prevCardLocation["pos"]
                    else:
                        # Remove history of the card in its original location
                        location = m.prevCardLocation["location"]
                        if location == "dungeon":
                            dungeonHand.inventory[m.prevCardLocation["i"]] = None
                        elif location == "player":
                            playerHand.inventory[m.prevCardLocation["i"]] = None
                        elif location == "weapon":
                            playerHand.weapon = None
                        elif location == "shield":
                            playerHand.shield = None

                    m.holdingCard = False  # We are now no longer holding a card

        # Update positions of held card
        if m.holdingCard != False:
            pos = pygame.mouse.get_pos()
            m.holdingCard.moveTo(pos)
    elif currentPage == "Shop":
        screen.fill()
        pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pos
                if (refresh_button.collidepoint(x, y)):  # Refresh button
                    # Make shop
                    for i in range(len(ability_cards)):
                        card = ability_cards[i]
                        card.cost = str(random.randint(10,
                                                50))  # temporary placeholder for determining the cards' value. they will probably be pre-determined

                    x_inc = 150
                    for i in range(3):  # three shop cards will be handed out
                        ability_cards[i].x = x_inc
                        ability_cards[i].y = 150
                        shop_cards.append(ability_cards[i])
                        x_inc += 200
                    # player.money -= 5

                elif StopToMenuButton.collidepoint(x,y):
                    # Return to main gameplay
                    currentPage = "Gameplay"

                else:
                    for card in shop_cards:
                        if card.withinBorder(pos):
                            shop_cards.remove(card)
                            # player.money -= card.cost


    # elif currentPage == "Main menu":



def draw():
    if currentPage == "Gameplay":
        screen.fill()
        gameBackground.draw(screen.screen)  # Draw background
        # Draw player hand
        for card in dungeonHand.inventory:
            if card != None: card.draw(screen.screen)
        # Draw dungeon hand
        for card in playerHand.inventory:
            if card != None: card.draw(screen.screen)
        # Draw Shield
        if playerHand.shield != None:
            playerHand.shield.draw(screen.screen)
        # Draw Sword
        if playerHand.weapon != None:
            playerHand.weapon.draw(screen.screen)

        pygame.display.update()
        clock.tick(70)  # Fps (Don't know why/how it does it)
    elif currentPage == "Shop":
        myfont = pygame.font.SysFont('Century Gothic', 30)
        shopBackground.draw(screen.screen)  # Draw background

        # Draw shop cards
        for card in shop_cards:
            card.draw(screen.screen)
            textsurface = myfont.render(card.cost, False, (255, 223, 0))
            screen.screen.blit(textsurface, (card.x + 15, 280))

        # Draw refresh button
        pygame.draw.rect(screen.screen, (255, 255, 255), refresh_button)
        textsurface = myfont.render('Refresh (10g)', False, (0, 0, 0))
        screen.screen.blit(textsurface, (50, 30))

        # Draw back button
        textsurface = myfont.render('Back', False, (0, 0, 0))
        pygame.draw.rect(screen.screen, (255, 255, 255),StopToMenuButton)
        screen.screen.blit(textsurface, (StopToMenuButton.x + 35, StopToMenuButton.y + 20))

        pygame.display.update()
        clock.tick(70)  # Fps (Don't know why/how it does it)
    # elif currentPage == "Main menu":


while True:
    # print(currentPage)
    update()
    draw()
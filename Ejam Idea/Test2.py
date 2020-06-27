import pygame
import sys
from random import randint


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
        self.held = False  # Outlines whether or not the card is currently being held by the cursor

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
        self.holdingCard = False  # Boolean for if a card is being held


screen = Window(760, 880)
pygame.init()
m = Mouse()
clock = pygame.time.Clock()
pygame.font.init()
myfont = pygame.font.SysFont('Century Gothic', 50)
background = Card(0, 0, screen.w, screen.h, r"C:\Users\dannie\PycharmProjects\untitled\Ejam Idea\Images\shop_gui.PNG")
ability_cards = [Card(0, 0, 75, 125, r"C:\Users\dannie\PycharmProjects\untitled\Ejam Idea\Images\Cake.png"), Card(0, 0, 75, 125, r"C:\Users\dannie\PycharmProjects\untitled\Ejam Idea\Images\Cake.png"),
                 Card(0, 0, 75, 125, r"C:\Users\dannie\PycharmProjects\untitled\Ejam Idea\Images\Cake.png")]  # all the ability cards that exist in the game
refresh_button = pygame.Rect(10, 10, 200, 60)
shop_cards = []  # cards that will be displayed in the shop


def make_shop():
    for i in range(len(ability_cards)):
        card = ability_cards[i]
        card.cost = str(randint(10,
                                50))  # temporary placeholder for determining the cards' value. they will probably be pre-determined

    x_inc = 150
    for i in range(3):  # three shop cards will be handed out
        ability_cards[i].x = x_inc
        ability_cards[i].y = 150
        shop_cards.append(ability_cards[i])
        x_inc += 200


make_shop()

while True:
    screen.fill()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if (refresh_button.collidepoint(x, y)):
                make_shop()
                # player.money -= 5
            m.held = True
            flag = False  # Flags whether or not new are in contact with a card (False = No contact, True = Contact)
            for card in shop_cards:  # Check to see which cards are clicked
                pos = pygame.mouse.get_pos()
                if card.withinBorder(pos):
                    flag = True
                    card.held = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if flag:
                for card in shop_cards:
                    if card.held:
                        # deck.append(card) add ------ commented because the deck has not been implemented yet
                        shop_cards.remove(card)
                        # player.money -= ability_card.value ------ commented because the deck has not been implemented yet
            m.held = False
            m.holdingCard = False
            for card in shop_cards: card.held = False  # Clear any history so that no cards are being held

    background.draw(screen.screen)  # Draw background

    # Draw shop cards
    for card in shop_cards:
        card.draw(screen.screen)
        textsurface = myfont.render(card.cost, False, (255, 223, 0))
        screen.screen.blit(textsurface, (card.x + 15, 280))
    pygame.draw.rect(screen.screen, (255, 255, 255), refresh_button)
    myfont = pygame.font.SysFont('Century Gothic', 30)
    textsurface = myfont.render('Refresh (5g)', False, (0, 0, 0))
    screen.screen.blit(textsurface, (25, 20))
    pygame.display.update()
    clock.tick(70)  # Fps (Don't know why/how it does it)

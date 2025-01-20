import copy
import random
import pygame

pygame.init()
# Game Variables
cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', "A"]
one_deck = 4 * cards
decks = 4
game_deck = copy.deepcopy(decks * one_deck)

WIDTH = 600
HEIGHT = 900

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blackjack")
fps = 60
timer = pygame.time.Clock()
font = pygame.font.Font("assets/fonts/TT Rounds Neue Trial Bold.ttf", 44)
active = False

# draw game conditions and buttons
def draw_game(act):
    button_list = []

# main game loop
run = True
while run:
    # Run game at our framerate and fill screen with bg color
    timer.tick(fps)
    screen.fill('black')

    # Event handling, if quit pressed then exit game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()

# End of game loop
pygame.quit()
import copy
import random
import pygame

pygame.init()

# Game Variables
suits = ['clubs', 'diamonds', 'hearts', 'spades']
cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', "A"]
one_deck = 4 * cards
decks = 4

# Game screen & fps
WIDTH = 600
HEIGHT = 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blackjack")
fps = 60
timer = pygame.time.Clock()

# fonts
font = pygame.font.Font("assets/fonts/TT Rounds Neue Trial Bold.ttf", 44)
small_font = pygame.font.Font("assets/fonts/TT Rounds Neue Trial Bold.ttf", 36)

# state of the game
activeGame = False
initial_deal = False
my_hand = []
dealer_hand = []
outcome = 0
reveal_dealer = False

# Win , Loss, Draw
records = [0, 0, 0]
player_score = 0
dealer_score = 0


# draw game conditions and buttons
def draw_game(act, record):
    button_list = []

    # On the start of the game, deal new hand
    if not act:
        deal = pygame.draw.rect(screen, "white", [150, 20, 300, 100], 0, 5)
        pygame.draw.rect(screen, "green", [150, 20, 300, 100], 3, 5)
        deal_text = font.render("DEAL HAND", True, "black")
        screen.blit(deal_text,(175, 40))
        button_list.append(deal)

    # Game started, show hit and stand
    else:
        # Hit button
        hit = pygame.draw.rect(screen, "white", [0, 700, 250, 100], 0, 5)
        pygame.draw.rect(screen, "green", [0, 700, 250, 100], 3, 5)
        hit_text = font.render("HIT", True, "black")
        screen.blit(hit_text,(85, 725))
        button_list.append(hit)

        # Stand button
        stand = pygame.draw.rect(screen, "white", [350, 700, 250, 100], 0, 5)
        pygame.draw.rect(screen, "green", [350, 700, 250, 100], 3, 5)
        stand_text = font.render("STAND", True, "black")
        screen.blit(stand_text,(400, 725))
        button_list.append(stand)

        # Records of wins, losess, draws
        score_text = small_font.render(f'Wins: {record[0]}     Losses: {record[1]}       Draws: {record[2]}', True, "white")
        screen.blit(score_text, (15, 840))

    return button_list

# dealing cards by selecting randomly in the deck, and make function for one card at a time
def deal_cards(current_hand, current_deck):
    card = random.randint(0, len(current_deck))
    current_hand.append(current_deck[card-1])
    current_deck.pop(card-1)
    return current_hand, current_deck

# draw cards visually onto screen
def draw_cards(player, dealer, reveal):
    for i in range(len(player)):
        sprite = pygame.image.load(f"assets/deck/{suits[i]}_{player[i]}.png")
        sprite = pygame.transform.smoothscale(sprite, (sprite.get_width() // 2, sprite.get_height() // 2))
        screen.blit(sprite, [70 + (70 * i), 460 + (10 * i), 120, 220])
    
    # if player not finished turn, dealer will hide one card
    for i in range(len(dealer)):
        sprite = pygame.image.load(f"assets/deck/{suits[i]}_{dealer[i]}.png")
        sprite = pygame.transform.smoothscale(sprite, (sprite.get_width() // 2, sprite.get_height() // 2))
        
        # hide second card
        if i != 0 or reveal:
            screen.blit(sprite, [70 + (70 * i), 160 + (10 * i), 120, 220])
        else:
            sprite = pygame.image.load(f"assets/deck/back_light.png")
            sprite = pygame.transform.smoothscale(sprite, (sprite.get_width() // 2, sprite.get_height() // 2))
            screen.blit(sprite, [70 + (70 * i), 160 + (10 * i), 120, 220])

def calculate_score(hand):
    score = 0
    aces_count = hand.count('A')
    for i in range(len(hand)):
        if hand[i] in ['J', 'Q', 'K']:
            score += 10
        elif hand[i] == 'A':
            score += 11
        else:
            score = score + int(hand[i])
    return score

# main game loop
run = True
while run:
    # Run game at our framerate and fill screen with bg color
    timer.tick(fps)
    screen.fill('black')
    # initial deal to player and dealer
    if initial_deal:
        for i in range(2):
            my_hand, game_deck = deal_cards(my_hand, game_deck)
            dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
        initial_deal = False

    # once game is activted and dealt calculate socres and display cards
    if activeGame:
        player_score = calculate_score(my_hand)
        draw_cards(my_hand, dealer_hand, reveal_dealer)
    buttons = draw_game(activeGame, records)

    # Event handling, if quit pressed then exit game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            if not activeGame:
                if buttons[0].collidepoint(event.pos):
                    activeGame = True
                    initial_deal = True
                    game_deck = copy.deepcopy(decks * one_deck)
                    my_hand = []
                    dealer_hand = []
                    outcome = 0

    pygame.display.flip()

# End of game loop
pygame.quit()
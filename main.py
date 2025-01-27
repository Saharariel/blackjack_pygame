import copy
import random
import pygame
import asyncio

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
game_active = False
initial_deal = False
my_hand = []
dealer_hand = []
outcome = 0
reveal_dealer = False
hand_active = False

# Win , Loss, Draw
records = [0, 0, 0]
player_score = 0
dealer_score = 0
add_score = False
results = ['', 'Player Busted!', 'Player Wins!', 'Dealer Wins!', 'Tie Game!']


# draw game conditions and buttons
def draw_game(act, record, result):
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

    #if there is an outcome for the hand that was played, display a restart button and tell user what happend.
    if result != 0:
        screen.blit(font.render(results[result], True, 'white'), (15,25))
        deal = pygame.draw.rect(screen, "white", [150, 350, 300, 100], 0, 5)
        pygame.draw.rect(screen, "green", [150, 350, 300, 100], 3, 5)
        pygame.draw.rect(screen, "black", [153, 353, 294, 94], 3, 5)
        deal_text = font.render("NEW HAND", True, "black")
        screen.blit(deal_text,(175, 370))
        button_list.append(deal)

    return button_list

# dealing cards by selecting randomly in the deck for one card at a time
def deal_cards(current_hand, current_deck):
    card = random.randint(0, len(current_deck))
    current_hand.append(current_deck[card-1])
    current_deck.pop(card-1)
    return current_hand, current_deck

# draw cards visually onto screen
def draw_cards(player, dealer, reveal):
    for i in range(len(player)):
        sprite = pygame.image.load(f"assets/deck/{suits[i-2]}_{player[i]}.png")
        sprite = pygame.transform.smoothscale(sprite, (sprite.get_width() // 2, sprite.get_height() // 2))
        screen.blit(sprite, [70 + (70 * i), 460 + (10 * i), 120, 220])
    
    # if player not finished turn, dealer will hide one card
    for i in range(len(dealer)):
        sprite = pygame.image.load(f"assets/deck/{suits[i-1]}_{dealer[i]}.png")
        sprite = pygame.transform.smoothscale(sprite, (sprite.get_width() // 2, sprite.get_height() // 2))
        
        # hide second card
        if i != 0 or reveal:
            screen.blit(sprite, [70 + (70 * i), 160 + (10 * i), 120, 220])
        else:
            sprite = pygame.image.load(f"assets/deck/back_light.png")
            sprite = pygame.transform.smoothscale(sprite, (sprite.get_width() // 2, sprite.get_height() // 2))
            screen.blit(sprite, [70 + (70 * i), 160 + (10 * i), 120, 220])

# draw scores for player and dealer on screen
def draw_scores(player, dealer):
    screen.blit(font.render(f"Score[{player}]", True, "white"), (385, 630))
    if reveal_dealer:
        screen.blit(font.render(f"Score[{dealer}]", True, "white"), (385, 100))

# calcualte score for player or dealer
def calculate_score(hand):
    score = 0
    aces_count = hand.count('A')

    # calculate the scores according to cards
    for i in range(len(hand)):
        if hand[i] in ['J', 'Q', 'K']:
            score += 10
        elif hand[i] == 'A':
            score += 11
        else:
            score += int(hand[i])

    # aces handling, if more then 21 change from 11 value to 1 value
    if score > 21 and aces_count > 0:
        for i in range(1, aces_count):
            if score > 21:
                score -= 10

    return score

# check endgame conditions function
def check_endgame(hand_act, deal_score, play_score, result, totals, add):
    # check end game scenarios- player has stood, busted or blackjacked
    # result 1-player busted, 2-win, 3-loss, 4-draw

    # First check for bust regardless of dealer's score
    if play_score > 21:
        result = 1
        if add:
            totals[1] += 1
            add = False
        return result, totals, add

    # Then check other conditions when dealer's turn is complete
    if not hand_act and deal_score >= 17:
        if deal_score < play_score <= 21 or deal_score > 21:
            result = 2
        elif play_score < deal_score <= 21:
            result = 3
        else:
            result = 4
        if add:
            if result == 3:
                totals[1] += 1
            elif result == 2:
                totals[0] += 1
            else:
                totals[2] += 1
            add = False
    return result, totals, add

# main game loop
async def main():
    game_active = False
    initial_deal = False
    my_hand = []
    dealer_hand = []
    outcome = 0
    reveal_dealer = False
    hand_active = False

    # Win , Loss, Draw
    records = [0, 0, 0]
    player_score = 0
    dealer_score = 0
    add_score = False
    run = True
    while run:
        # Run game at our framerate and fill screen with bg color
        timer.tick(fps)
        screen.fill('black')

        # initial(first) deal to player and dealer
        if initial_deal:
            for i in range(2):
                my_hand, game_deck = deal_cards(my_hand, game_deck)
                dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
            initial_deal = False

        # once game is activted and dealt calculate socres and display cards
        if game_active:
            player_score = calculate_score(my_hand)
            draw_cards(my_hand, dealer_hand, reveal_dealer)

            # Calcaulte dealers score    
            if reveal_dealer or player_score >= 21:
                dealer_score = calculate_score(dealer_hand)
                if dealer_score < 17:
                    dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)

            draw_scores(player_score, dealer_score)

        buttons = draw_game(game_active, records, outcome)

        # Event handling, if quit pressed then exit game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONUP:
                if not game_active:
                    # if presses deal cards and game not active
                    if buttons[0].collidepoint(event.pos):
                        game_active = True
                        initial_deal = True
                        game_deck = copy.deepcopy(decks * one_deck)
                        my_hand = []
                        dealer_hand = []
                        outcome = 0
                        hand_active = True
                        reveal_dealer = False
                        add_score = True
                else:
                    # if pressed hit and game is active and can hit at all
                    if buttons[0].collidepoint(event.pos) and player_score < 21 and hand_active:
                        my_hand, game_deck = deal_cards(my_hand, game_deck)

                    # if pressed stand and game is active (end turn)
                    elif buttons[1].collidepoint(event.pos) and not reveal_dealer:
                        reveal_dealer = True
                        hand_active = False
                    # Restart game
                    elif len(buttons) == 3:
                        if buttons[2].collidepoint(event.pos):
                            game_active = True
                            initial_deal = True
                            game_deck = copy.deepcopy(decks * one_deck)
                            my_hand = []
                            dealer_hand = []
                            outcome = 0
                            hand_active = True
                            reveal_dealer = False
                            add_score = True
                            player_score = 0
                            dealer_score = 0

        # if player busted
        if hand_active and player_score >= 21:
            hand_active = False
            reveal_dealer = True

        outcome, records, add_score = check_endgame(hand_active, dealer_score, player_score, outcome, records, add_score)
        
        # Update display
        pygame.display.flip()
        await asyncio.sleep(0)
# End of game loop

asyncio.run(main())

pygame.quit()

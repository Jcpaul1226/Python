#Game of Blackjack in Python using pygame
import copy
import random
import pygame

pygame.init()
#game variables
cards = ['2','3','4','5','6','7','8','9','J','Q','K','A']
one_deck = 4 * cards
decks = 1
WIDTH = 700
HEIGHT = 920
screen = pygame.display.set_mode([WIDTH,HEIGHT])
pygame.display.set_caption('Pygame Blackjack!')
fps = 60
timer = pygame.time.Clock()
pygame.font.init()
font = pygame.font.Font('freesansbold.ttf', 44)
smaller_font = pygame.font.Font('freesansbold.ttf', 36)
active = True
# win, loss, draw
records = [0,0,0]
book_records = [0,0,0]
player_score = 0
dealer_score = 0
book_score = 0
active = False
initial_deal = False
game_deck = copy.deepcopy(decks * one_deck)
book_deck = copy.deepcopy(game_deck)
my_hand = []
dealer_hand = []
book_hand = []
reveal_dealer = False
outcome = 0
book_outcome = 0
hand_active = True
book_active = False
outcomes = 0
add_score = False
book_add_score = False
results = ['','PLAYER BUSTED!','PLAYER WINS!', 'DEALER WINS', 'PUSH']

#deal cards by selecting randomly from deck, and make functions for one card at a time
def deal_cards(current_hand, current_deck):
    card = random.randint(0, len(current_deck))
    current_hand.append(current_deck[card-1])
    current_deck.pop(card-1)
    return current_hand, current_deck

#draw cards
def draw_cards(player,dealer,reveal,book):
    for i in range (len(player)):
        pygame.draw.rect(screen, 'white', [0 + (70*i),460 + (5*i),120,220],0,5)    #[(L ->R) horizontal, (T -> B) vertical,width height]
        screen.blit(font.render(player[i], True, 'black'), (5 + 70*i, 465 + 5*i))
        screen.blit(font.render(player[i], True, 'black'), (5 + 70*i, 635 + 5*i))
        pygame.draw.rect(screen, 'green', [0 + (70*i),460 + (5*i),120,220],5,5)
        

    for i in range (len(book)):
        pygame.draw.rect(screen, 'white', [350 + (70*i),460 + (5*i),120,220],0,5)
        screen.blit(font.render(book[i], True, 'black'), (355 + 70*i, 465 + 5*i))
        screen.blit(font.render(book[i], True, 'black'), (355 + 70*i, 635 + 5*i))
        pygame.draw.rect(screen, 'blue', [350 + (70*i),460 + (5*i),120,220],5,5)

    #if player hasn't finished turn,dealer will hide one card
    for i in range (len(dealer)):
        pygame.draw.rect(screen, 'white', [0 + (70*i),160 + (5*i),120,220],0,5)
        if i != 0 or reveal:
            screen.blit(font.render(dealer[i], True, 'black'), (5 + 70*i, 165 + 5*i))
            screen.blit(font.render(dealer[i], True, 'black'), (5 + 70*i, 335 + 5*i))
        else:
            screen.blit(font.render('??', True, 'black'), (5 + 75*i, 165 + 5*i))
            screen.blit(font.render('??', True, 'black'), (5 + 75*i, 335 + 5*i))
        pygame.draw.rect(screen, 'red', [0 + (70*i),160 + (5*i),120,220],5,5)

#pass in player or dealer hand and calculate best score
def calculate_score(hand):    
    #calculate hand score fresh every time,check how many aces we have
    hand_score = 0
    aces_count = hand.count('A')
    for i in range(len(hand)):
        #for 2,3,4,5,6,7,8,9 - just add the number to total
        for j in range(8):
            if hand[i] == cards[j]:
                hand_score += int(hand[i])
        #for 10 and face cards, just add 10
        if hand[i] in ['10','J','Q','K']:
            hand_score += 10
        #for aces start by adding 11, and reduce if needed after
        elif hand[i] == 'A':
            hand_score += 11
        #determine how many aces need to be 1 to stay under and as close to 21
    if hand_score > 21 and aces_count > 0:
        for i in range(1,aces_count):
            if hand_score > 21:
                hand_score -= 10
    return hand_score

#draw scores for player and dealer
def draw_scores(player,idealer,dealer,book):
    screen.blit(font.render(f'[{player}]',True, 'white'),(150,400))
    screen.blit(font.render(f'[{book}]',True, 'white'),(425,400))
    if reveal_dealer:
        screen.blit(font.render(f'[{dealer}]',True, 'white'),(160,100))
    else:
        screen.blit(font.render(f'[{idealer}]',True, 'white'),(160,100))

#draw game conditions and buttons
def draw_game(act, record, book_record, result ):
    button_list =[]
    #initial on startup (not active) only option is to deal new hand 
    if not act:
        deal  = pygame.draw.rect(screen, 'white', [150,20,300,100],0,5)
        pygame.draw.rect(screen, 'green', [150,20,300,100],3,5)
        deal_text = font.render('DEAL HAND',True, 'black')
        screen.blit(deal_text, (165, 50))
        button_list.append(deal)
    #once game started, show hit and stand buttons and win/loss records
    else:
        hit  = pygame.draw.rect(screen, 'white', [0,700,290,100],0,5)
        pygame.draw.rect(screen, 'green', [0,700,290,100],3,5)
        hit_text = font.render('HIT ME',True, 'black')
        screen.blit(hit_text, (55, 735))
        button_list.append(hit)

        dealer_text = font.render('Dealer: ',True,'white')
        screen.blit(dealer_text, ( 0, 100))

        player_text = font.render('Player: ',True,'white')
        screen.blit(player_text, ( 0, 400))

        book_text = font.render('Book: ',True,'white')
        screen.blit(book_text, ( 300, 400))

        stand  = pygame.draw.rect(screen, 'white', [300,700,290,100],0,5)
        pygame.draw.rect(screen, 'green', [300,700,290,100],3,5)
        stand_text = font.render('STAND',True, 'black')
        screen.blit(stand_text, (355, 735))
        button_list.append(stand)
        score_text = smaller_font.render(f'Wins: {record[0]} Losses: {record[1]}  Draws: {record[2]}', True , 'white')
        screen.blit(score_text,(15,810))
        book_score_text = smaller_font.render(f'BOOK: Wins: {book_record[0]} Losses: {book_record[1]}  Draws: {book_record[2]}', True , 'white')
        screen.blit(book_score_text,(15,850))

    #if there is an outcome for hand that is played, display restart button an result
    if result != 0:
        screen.blit(font.render(results[result],True,'white'), (180,25))
        deal  = pygame.draw.rect(screen, 'white', [150,220,300,100],0,5)
        pygame.draw.rect(screen, 'green', [150,220,300,100],3,5)
        pygame.draw.rect(screen, 'black', [153,223,294,94],3,5)
        deal_text = font.render('NEW HAND',True, 'black')
        screen.blit(deal_text, (165, 250))
        button_list.append(deal)

    return button_list

#Decide how the book would play players hands
def book_play(book_score,dealer_score):
    #stay = 0, hit = 1, double = 2
    book = 0
    if book_score < 9:
        book = 1
    elif book_score < 12 and book_score > 9:
        if book_score == 9 and book_score == 2 or dealer_score > 6:
            book = 1
        elif book_score == 10 and dealer_score > 9:
            book = 1 
        else:
            book = 2   
    if book_score == 12:
        if dealer_score > 3 and dealer_score < 7:
            book = 0
        else:
            book = 1
    if book_score > 12:
        if dealer_score > 6 and book_score < 17:
            book = 1 
        else:
            book = 0
    return book
        
#check endgame conditions function
def check_endgame(hand_act, deal_score, play_score, result, totals, add):
    #check end game scenarios, player stood, busted, or blackjack
    #result 1 - bust, 2-win,3-loss,4-push
    if not hand_act and dealer_score >= 17:
        if play_score == deal_score < 22:
            result = 4
        elif deal_score < play_score <= 21 or deal_score >21:
            result = 2
        elif play_score > 21:
            result = 1
        else:
            result = 3
        if add: 
            if result == 4:     
                totals[2] += 1
            elif result == 2:
                totals[0] += 1
            else:
                totals[1] += 1
            add = False
    return result, totals, add



#main game loop
run = True
while run:
    #run game at our framerate and fill screen with bg color
    timer.tick(fps)
    screen.fill('black')
    #initial deal to player and dealer
    if initial_deal:
        for i in range(2):
            my_hand, game_deck = deal_cards(my_hand, game_deck)
            dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
        book_hand = copy.deepcopy(my_hand)
        initial_deal = False
        idealer_score = calculate_score(dealer_hand[1])


    if active:
        player_score = calculate_score(my_hand)
        book_score = calculate_score(book_hand)
        book = book_play(book_score,idealer_score)
        draw_cards(my_hand,dealer_hand,reveal_dealer,book_hand)
        if book_active:
            if book_score < 21 and book > 0 :
                book_hand,game_deck = deal_cards(book_hand,game_deck)
                book = book_play(book_score,dealer_score)
                
            else:
             book_active = False
             book_score = calculate_score(book_hand)
        elif reveal_dealer:
            dealer_score = calculate_score(dealer_hand)
            if dealer_score < 17:
                dealer_hand,game_deck = deal_cards(dealer_hand,game_deck)
            else:
                dealer_score = calculate_score(dealer_hand)   
            
        draw_scores(player_score,idealer_score,dealer_score,book_score)
        
        

    #once game is activated and dealt, calculate scores and display cards
    button = draw_game(active,records,book_records, outcomes)

    #event handling, if quit pressed, then exit game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            #starts the game
            if not active:      
                if button[0].collidepoint(event.pos):
                    active = True
                    initial_deal = True
                    game_deck = copy.deepcopy(decks * one_deck)
                    my_hand = []
                    dealer_hand = []
                    outcome = 0
                    hand_active = True
                    book_active = False
                    reveal_dealer = False
                    book_outcome = 0
                    outcomes = 0
                    add_score =True
                    book_add_score =True
            else: 
                if button[0].collidepoint(event.pos) and player_score < 21 and hand_active:
                    my_hand, game_deck = deal_cards(my_hand, game_deck)
                elif button[1].collidepoint(event.pos) and not reveal_dealer:
                    reveal_dealer = True
                    book_active = True
                    hand_active = False
                elif len(button) == 3:
                    if button[2].collidepoint(event.pos):
                        active = True
                        initial_deal = True
                        game_deck = copy.deepcopy(decks * one_deck)
                        my_hand = []
                        dealer_hand = []
                        book_hand = []
                        outcome = 0
                        hand_active = True
                        reveal_dealer = False
                        book_active = False
                        outcomes = 0
                        book_outcome = 0
                        add_score =True
                        book_add_score =True
                        player_score = 0
                        dealer_score = 0
                        book_score = 0
    #if player busts, automatically end turn - treat like a stand
    if hand_active and player_score >= 21:
        hand_active = False
        book_active = True
        reveal_dealer = True

    outcomes, records, add_score = check_endgame(hand_active,dealer_score,player_score,outcomes,records,add_score)
    book_outcome, book_records, book_add_score = check_endgame(book_active,dealer_score,book_score,book_outcome,book_records,book_add_score)
    

    pygame.display.flip()   


pygame.quit()
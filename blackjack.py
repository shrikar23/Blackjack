# Mini-project #6 - Blackjack
import random

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
    
# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
dealer_card = False
ace_as_11 = False
player_value = 0
dealer_value = 0
player_turn = True
choice = ""

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print("Invalid card: ", suit, rank)

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.hands = []
        
    def __str__(self):
        result = "Hand contains"
        for i in range(len(self.hands)):
            test = str(self.hands[i])
            test1 = Card(test[0], test[1])
            result = result + " " + str(test1)
        return result

    def add_card(self, card):
        self.hands.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        total_value = 0
        aces = False
        for h in self.hands:
            a = str(h)
            value_of_card = VALUES[a[1:2]]
            total_value = total_value + value_of_card
            if a == "SA" or a == "HA" or a == "CA" or a == "DA":
                aces = True
        if aces:
            if total_value + 10 <= 21:
                return total_value + 10
            else:
                return total_value
            aces = False
        else:    
            return total_value    
   
    def draw(self, canvas, pos): 
    # Draw the cards. for dealer draw the first card flipped initially.
    # show the value when the player's turn is over.
        for i in range(len(self.hands)):
            test = str(self.hands[i])
            test1 = Card(test[0], test[1])
            if i == 0 and pos[1] == 100 and player_turn:
                canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
            else:
                test1.draw(canvas, [(i * 80) + pos[0], pos[1]])
            
# define deck class 
class Deck:
    def __init__(self):
        self.deck = []
        for s in range(len(SUITS)):
            for r in range(len(RANKS)):
                self.deck.append(SUITS[s] + RANKS[r])

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck)

    def deal_card(self):
        deck_card = Card(random.choice(SUITS), random.choice(RANKS))
        return deck_card
    
    def __str__(self):
        result = "Deck contains"
        for r in range(len(self.deck)):
            result = result + " " + str(self.deck[r])
        return result
    
#define event handlers for buttons
def deal():
    global choice, in_play, player_hand, dealer_hand, outcome, score, player_turn
    player_turn = True
    deck.shuffle()
    temp = Hand()
    player_hand = temp
    temp_1 = Hand()
    dealer_hand = temp_1
    outcome = ""
    p = 1
    d = 1
    temp1 = []
    temp2 = []
    if in_play:
        score -= 1
    # Deal 2 cards to the player and dealer respectively.
    while p <= 2 and d <= 2:
        deal_card = deck.deal_card()
        if deal_card not in temp1 and deal_card not in temp2 and p <= 2:
            temp1.append(deal_card)
            player_hand.add_card(deal_card)
            p += 1
            choice = "Hit or Stand ?"
            
        deal_card = deck.deal_card()
        if deal_card not in temp1 and deal_card not in temp2 and d <= 2:
            temp2.append(deal_card)
            dealer_hand.add_card(deal_card)
            d += 1
        
    in_play = True

def hit():
    # if the hand is in play, hit the player
    global in_play, player_value, player_hand, score, outcome, choice
    player_value = player_hand.get_value()
    if in_play:
        deal_card = deck.deal_card()
        player_hand.add_card(deal_card)
        player_value = player_hand.get_value()
        
    # if busted, assign a message to outcome, update in_play and score
        if player_value > 21:
            outcome = "You are busted." 
            choice = "New Deal ?"
            score -= 1
            in_play = False
            
def stand():
    global in_play, choice, player_value, dealer_hand, dealer_value, score, outcome, player_turn
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play:
        player_turn = False
        dealer_value = dealer_hand.get_value()
        deal_card = deck.deal_card()
        while dealer_value < 17:
            dealer_hand.add_card(deal_card)
            dealer_value = dealer_hand.get_value()   
    
    # assign a message to outcome, update in_play and score    
        if dealer_value > 21:
            outcome = "Dealer is busted" 
            choice = "New deal ?"
            score = +1
            in_play = False
        elif dealer_value > player_value:
            outcome = "Dealer wins"
            choice = "New Deal ?"
            score -= 1
            in_play = False
        elif dealer_value == player_value:
            outcome = "Dealer wins"
            choice = "New Deal ?"
            score -= 1
            in_play = False
        else:
            outcome = "You win" 
            choice = "New Deal ?"
            score += 1
            in_play = False
    
# draw handler    
def draw(canvas):
    player_hand.draw(canvas, [50, 400])
    dealer_hand.draw(canvas, [50, 100])
    canvas.draw_text(outcome, [250, 320], 25, "white")
    canvas.draw_text(choice, [250, 380], 25, "white")
    canvas.draw_text("Blackjack", [250, 40], 40, "cyan")
    canvas.draw_text("Dealer", [50, 90] , 25, "white")
    canvas.draw_text("Player", [50, 390], 25, "white")
    canvas.draw_text("Score = " + str(score), [400, 80], 25, "white")

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
deck = Deck()
player_hand = Hand()
dealer_hand = Hand()
deal()
frame.start()

import random

CLUBS = "c" #"/u2663"
HEARTS = "h" #"/u2665"
SPADES = "s" #"/u2660"
DIAMONDS = "d" #"/u2666"

# List of values and suits
suits = [CLUBS, HEARTS, SPADES, DIAMONDS]
ranks = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']

# Create Card Object
class Card(object):
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

# Create deck object and funtions
class Deck(object):

   def __init__(self):
        self.cards = []
        self.build()

   def build(self):
       self.cards = []
       for s in suits:
           for r in ranks:
               self.cards.append(Card(s, r))

   def show(self):
        for c in self.cards:
            print ("{}{}".format(c.rank, c.suit))

   def shuffle(self):
        for i in range(len(self.cards)-1, 0, -1):
            r = random.randint(0, i)
            self.cards[i], self.cards[r] = self.cards[r], self.cards[i]

   def drawCard(self):
       return self.cards.pop()

# Create comunity tables
class CommunityCards(object):
    def __init__(self):
        self.flop = []
        self.turn = []
        self.river = []
        self.board = []       
        
    def drawFlop(self, deck):
        self.flop.append(deck.drawCard())
        return self        

    def drawTurn(self, deck):
        self.turn.append(deck.drawCard())

    def drawRiver(self, deck):
        self.river.append(deck.drawCard())

    def newHand(self):
        self.flop = []
        self.turn = []
        self.river = []
        self.board = []
 
# Create player object to do
class Player(object):
    def __init__(self, name, chips):
        self.name = name
        self.chips = chips
        self.holeCards = []
        self.hand = []
        self.folded = False
        self.bet = 0
        self.allIn = False
        self.raiser = False
        self.subPot = 0
        self.out = False
        self.seat = 0
        self.handVal = []

    def draw(self, deck):
        self.holeCards.append(deck.drawCard())
        return self

    def showHand(self):
        for card in self.holeCards:
            return card

    def foldHand(self):
        self.bet = 0
        self.folded = True

    def newHand(self):
        self.holeCards = []
        self.hand = []
        self.folded = False
        self.bet = 0
        self.allIn = False
        self.raiser = False
        self.subPot = 0
        self.handVal = []

# Create table - Todo
class Table(object):
    def __init__(self, tableName, seats):
        self.name = tableName
        self.seats = []
        self.players = []
        self.button = 0
        self.pot = 0
        self.sidePot = [0] * seats
        self.c_sidepot = 0
        self.bet = 0
        self.rBet = 0 
        self.called = 0
        self.board = []
        self.raiser = ""
        self.inHand = []
        self.allIn = 0
        self.training = False #to remove printing from nn training

    def addPlayer(self, player):
        self.players.append(player)

    def removePlayer(self, player):
        self.players.remove(player)
        
    def foldPlayer(self, player):
        self.inHand.remove(player)

    def moveButton(self):
        self.button += 1
        self.button %= len(self.players)

    def collectPot(self):
        return self.pot
    
    def collectSidePot(self):
        return self.sidePot
        self.sidePot = 0   
        
        
    def newHand(self):
        self.pot = 0       
        self.bet = 0
        self.rBet = 0  
        self.called = 0
        self.allIn = 0
        self.sidePot = [0] * len(self.players)
        self.board = []
        self.raiser = 0   
        self.inHand = list(self.players)
        CommunityCards.newHand
        
        
        

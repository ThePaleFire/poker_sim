# Initialise Holdem Poker Tournament

# Import objects
from poker_objects import Table, Deck, Player
from pk_hand_sim import newHand
import random

#Neural Network setting
TRAINING = False # diable printing for training mode
HUMANPLAYERS = 0 # number of human players

# blind levels
SbLvl = [10, 15, 25, 40, 60, 80, 100, 150, 200, 300, 400, 600, 800, 1000,
         1500, 2000, 3000, 4000, 6000, 8000, 10000, 15000, 20000, 25000, 300000]

# define golbal constants:c
STACK = 1500 # chip allocation
SB = 10 # starting blinds
BB = 20 # starting blinds
BLV = 1 # starting blind lvp
PLAYERS = 2 # number of players

table = Table("Table1", PLAYERS) # initialise table
deck = Deck() # create a deck
handNum = 0 # initialise hand counta

def main():

    # print tournament type/ & blind stucture
    print("NL Hold'em [{} max, STT] - Level {} Blinds ({}/{})".format(PLAYERS, BLV, SB, BB))

    handNum = 0 # initialise hand counta
    
    # Add players to table
    for i in range(PLAYERS):
        name = input("Add player Name:".format(""))
        player = Player(name, STACK)
        table.addPlayer(player)
    # Shuffle player order fpor seating
    random.shuffle(table.players)
    table.seats = list(table.players)

    # Seat Players
    for i in range(0 ,len(table.players)):
        table.players[i].seat = i + 1

    # add all players to inhand150
    table.inHand = list(table.players)
    
    lvl = BLV
    sB = SB
    bB = BB
    
    while len(table.players) > 1: # loop until winning player
        
        deck.build() # ensure deck is re-built before each level
        deck.shuffle() # ensure deck is shuffled before each level
        
        for i in range(0, 10): # hands before blind increase
            handNum += 1
            print("Hand #{} - level{}".format(handNum, lvl))

            # call new hand
            newHand(table, deck, sB, bB, TRAINING)
            
            # If one player remaining end tournement
            if len(table.players) == 1:
                break
            
            i += 1
            # rebuild and shuffle deck
            deck.build()
            deck.shuffle()
            table.newHand()
            table.inHand = list(table.players)

    # increase blinds level
        lvl += 1
        sB = SbLvl[lvl-1]
        bB = sB * 2 
        
    print("{} wins the tournament".format(table.players[0].name))

if __name__ == "__main__":
    main()

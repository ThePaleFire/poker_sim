# -*- coding: utf-8 -*-
# Poker hand

# Import objects
from poker_objects import  CommunityCards
from pk_hand_valuation import HandVal

def newHand(t, deck, SB, BB, tMode):
    
    cCards = CommunityCards()

    #set button relative to players left in play
    btn = t.players.index(t.seats[t.button])

    # print button position
    if tMode == False:
        print("{} - seat #{} is the button".format(t.name, t.players[btn].seat))

    #print player seats
    if tMode == False:
        for p in t.players:
            print("seat {}: {} ({} in chips)".format(p.seat, p.name, p.chips))

    # post blinds
    t.players[(btn + 1) % len(t.players)].chips -= SB
    t.players[(btn + 1) % len(t.players)].bet = SB
    t.players[(btn + 2) % len(t.players)].chips -= BB
    t.players[(btn + 2) % len(t.players)].bet = BB
    t.pot += SB + BB
    t.bet = BB

    if tMode == False:
        print("{}: posts small blind {}".format(t.players[(btn + 1) % len(t.players)].name, SB))
        print("{}: posts big blind {}".format(t.players[(btn + 2) % len(t.players)].name, BB))

    # *** Deal Cards ***
    if tMode == False:
        print("*** HOLE CARDS ***")

    # Deal hole cards starting with player right of the button
    for i in range(0, 2):
        for i in range(0, len(t.players)):
            j = (i + btn + 1) % len(t.players)
            t.players[j].draw(deck)

    # *** Create community cards ********************************
    # Create community cards
    deck.drawCard # burn card
    cCards.drawFlop(deck).drawFlop(deck).drawFlop(deck)
    deck.drawCard # burn card
    cCards.drawTurn(deck)
    deck.drawCard # burn card
    cCards.drawRiver(deck)
    
    #turn and river are single objects so must be added as tuples
    cCards.board = cCards.flop + cCards.turn + cCards.river 
    # ********************************************************   
    
    # store 7 card hand for each player
    for i in range(0, len(t.players)):
        t.players[i].hand = t.players[i].holeCards + cCards.board

    if tMode == False:
        # print hole cards in order dealt
        for i in range(0, len(t.players)):
            j = (i + btn + 1) % len(t.players)
            print("Dealt to {} [".format(t.players[j].name), end="")
            print(' '.join([str("{}{}".format(card.rank, card.suit)) for card in t.players[j].holeCards]), end="")
            print("]")

    # *** PRE-FLOP ***
    # Call pre flop action
    Street(t, btn + 3, cCards, 0, tMode)
    if t.allIn < len(t.inHand) - 1:
        t.raiser = "" # reset table raiser

    # *** FLOP ****
    # Call flop action
    if len(t.inHand) != 1:
        Street(t, btn + 1, cCards, 1, tMode)
        if t.allIn < len(t.inHand) - 1:
            t.raiser = "" # reset table raiser
    
    # *** TURN ***
    if len(t.inHand) != 1:
        Street(t, btn + 1, cCards, 2, tMode) # Call turn action
        if t.allIn < len(t.inHand) - 1:
            t.raiser = "" # reset table raiser
    
    # *** RIVER ****
    if len(t.inHand) != 1:
        Street(t, btn + 1, cCards, 3, tMode) # call river action
        # Dont reset raiser for correct call order

    # *** SHOW DOWN ***
    if len(t.inHand) != 1:
        Showdown(t, btn, cCards, tMode)
    
    #reset for new hand    
    ResetHands(t)
    
    # *** SUMMARY ***
# =============================================================================
#     print("*** SUMMARY***")
#     print("Total pot {}".format(t.pot))
#     print("Board: [", end="")
#     print(' '.join([str("{}{}".format(card.rank, card.suit)) for card in cCards.board]), end="")
#     print("]")
# =============================================================================
        

# deal and play next street (table, position, cCards, street)
def Street(t, p , c, s, tMode):
    
    if tMode == False:
    # Print cards #
        if s == 1: 
            # print FLOP community cards
            print("*** FLOP *** [", end="")
            print(' '.join([str("{}{}".format(card.rank, card.suit)) for card in c.flop]), end="")
            print("]")
        elif s == 2:    
            # print TURN community cards
            print("*** TURN *** [", end="")
            print(' '.join([str("{}{}".format(card.rank, card.suit)) for card in c.flop]), end="")
            print("] [{}{}]".format(c.turn[0].rank, c.turn[0].suit))
        elif s == 3:  
            # print RIVER community cards
            print("*** RIVER *** [", end="")
            print(' '.join([str("{}{}".format(card.rank, card.suit)) for card in c.flop]), end=" ")
            print("{}{}] [{}{}]".format(c.turn[0].rank, c.turn[0].suit, c.river[0].rank, c.river[0].suit))
    
    
    if not t.allIn >= len(t.inHand) - 1: # if not all in
    
    # Set action on player based on position p
        while True:
            n = 0
            for i in range(0, len(t.players)):
                j = (i + p) % len(t.players)
                player = t.players[j]
                if player.folded != True and player.allIn != True:
                
                    # check if all other players have folded
                    if len(t.inHand) == 1 and t.inHand[0] == t.players[j]:
                        if t.raiser == player.name:
                            player.chips += t.rBet
                            
                            if tMode == False:
                                print("{} returned to {}".format(t.rBet, player.name))
                        
                        r = t.collectPot() 
                        player.chips += r
                        
                        if tMode == False:
                            print("{} collects {} from pot".format(player.name, r))
                        
                        ResetHands(t)
                        return None # end hand
                    
                    elif t.raiser == player:
                        n = 0
                        break
                    
                    elif t.allIn == len(t.inHand):
                        n = 0
                        break
                    
                    if t.allIn == len(t.inHand) - 1 and player.bet == t.bet:
                        n = 0
                        break                    
                    
                     
                    elif t.players[j].folded == False:
                        # prompt player action
                        n += Action(t, t.players[j], tMode)
            if n == 0:
                break
            
        # check if raisers bet is over max call and return chips
        if t.called < t.rBet:
            i = t.rBet - t.called
            t.raiser.chips += i
            t.pot -= i
            t.rBet = 0
            
            if tMode == False:
                print("{} returned to {}".format(i, t.raiser.name))
        
    # reset player bets
    for player in t.players:
        player.bet = 0
    
    t.bet = 0  # reset table bet


 #player action fold/ check/call /raise
def Action(t, player, tMode):

    # player folds
    pAction = input("Action is on {}:".format(player.name))
    if pAction == 'f' or pAction == 'F':
        player.foldHand()
        t.foldPlayer(player)
        player.bet = 0
        
        if tMode == False:
            print("{} Folds".format(player.name))
        
        return 0   
    
    # player calls / checks
    elif pAction =='c' or pAction == 'C':
        if player.bet < t.bet: # player calls
            n = t.bet - player.bet
            #if call puts player all in
            if n >= player.chips:
                n = player.chips
                player.allIn = True
                t.allIn += 1
                if t.called < n:
                    t.called = n
                if tMode == False:
                    print("{} Calls {} (All In)".format(player.name, n))
            
            else: 
                if tMode == False:
                    print("{} Calls {} to {}".format(player.name, n, t.bet))
                t.rBet = 0
            t.pot += n
            player.bet += n
            player.chips -= n
            return 0
        else: # player checks
            if tMode == False:
                print("{} Checks".format(player.name, t.bet))
            return 0
    
    #player bets
    elif pAction.isdigit():

        bet = int(pAction)

        # if bet is less than current raise
        if t.bet > bet + player.bet: 
            return Action(t, player)   
        
        if t.bet < bet + player.bet: # player raises       
            if bet >= player.chips: # bet is all in
                bet = player.chips
                player.allIn = True
                t.allIn += 1
            player.bet += bet # adjust players total bet this round                
            rVal = player.bet - t.bet # find value of raise above current table bet
            t.rBet = rVal   
            player.chips -= bet
            t.pot += bet
            t.bet = player.bet
            t.raiser = player
            
            if player.allIn == True:
                if tMode == False:
                    print("{} Raises {} to {} (All In)".format(player.name, rVal, t.bet))
            else:
                if tMode == False:
                    print("{} Raises {} to {}".format(player.name, rVal, t.bet))
            return 1
    
    else:
        return Action(t, player, tMode)

def Showdown(t, btn, c, tMode):   
    
    if tMode == False:
        print("*** SHOW DOWN ***")
        # print board
        print("Board: [", end="")
        print(' '.join([str("{}{}".format(card.rank, card.suit)) for card in c.board]), end="")
        print("]")

    # set called player
    if t.raiser == "":
        r = btn + 1
    else:
        r = t.players.index(t.raiser)
        
    #set hand score counta
    n, n2 = 0, 0
    
    splitCount = 0

   # print holeCards still in play and evaluate winning hand
    for i in range(0, len(t.players)):
        j = (i + r) % len(t.players)
        player = t.players[j]
        if player.folded != True:
            handVal = HandVal(player)
            player.handVal = handVal
            if handVal[1] < n or handVal[1] == n and handVal[2] < n2 : # muck loosing hand
                t.foldPlayer(player)
                if tMode == False:
                    print("{}: mucks hand [".format(player.name), end ="") 
                    #print hand for testing
                    print(' '.join([str("{}{}".format(card.rank, card.suit)) for card in player.holeCards]), end="")
                    print("] ", end="") 
                    print(handVal[0]) # " (Hand ie pair of Deuces)"   
            else:
                if tMode == False:
                    print("{}: shows [".format(player.name), end="")
                    print(' '.join([str("{}{}".format(card.rank, card.suit)) for card in player.holeCards]), end="")
                    print("] ", end="") 
                    print(handVal[0]) # " (Hand ie pair of Deuces)"
                if n == handVal[1] and n2 == handVal[2]:
                    splitCount += 1
                else:
                    splitCount = 0
                    n, n2 = handVal[1], handVal[2] # " store hand strength
                    bHand = j
    
    # collect winnings
    if splitCount > 0:
        split = int(t.pot / (splitCount + 1))
        for player in t.inHand:
            if n == player.handVal[1] and n2 == player.handVal[2]:
                player.chips += split
                if tMode == False:
                    print("{}: wins {}".format(player.name, split))
    else:
    # todo decide winning player/ split pot + players out of tournement
        if tMode == False:    
            print("{}: wins {}".format(t.players[bHand].name, t.pot))
        t.players[bHand].chips += t.pot

# prepair for next hand   
def ResetHands(t):   
    #reset t, players & comunity cards
    
    for player in reversed(t.players):
        if player.chips == 0:
            print("{} is out of the tournament".format(player.name))
            i = t.seats.index(player)
            t.seats[i] = "Empty"
            t.removePlayer(player)
        else:
            player.newHand()
            
    # move button and re-set for next hand
    while True:
        t.button += 1
        t.button %= len(t.seats)
        if t.seats[t.button] != "Empty":
            break


if __name__ == "__newHand__":
    newHand()

# evaluate best 5 card poker hand

def HandVal(player): # two hole cards and board

    rankDict = {'A': 0, 'K': 0, 'Q': 0, 'J': 0, '10': 0, '9': 0, '8': 0, '7': 0, '6': 0, '5': 0, '4': 0, '3': 0, '2': 0}
    suitC = {'A': 0, 'K': 0, 'Q': 0, 'J': 0, '10': 0, '9': 0, '8': 0, '7': 0, '6': 0, '5': 0, '4': 0, '3': 0, '2': 0}
    suitH = {'A': 0, 'K': 0, 'Q': 0, 'J': 0, '10': 0, '9': 0, '8': 0, '7': 0, '6': 0, '5': 0, '4': 0, '3': 0, '2': 0}
    suitS = {'A': 0, 'K': 0, 'Q': 0, 'J': 0, '10': 0, '9': 0, '8': 0, '7': 0, '6': 0, '5': 0, '4': 0, '3': 0, '2': 0}
    suitD = {'A': 0, 'K': 0, 'Q': 0, 'J': 0, '10': 0, '9': 0, '8': 0, '7': 0, '6': 0, '5': 0, '4': 0, '3': 0, '2': 0}
    
    cardVal = {'A': 13, 'K': 12, 'Q': 11, 'J': 10, '10': 9, '9': 8, '8': 7, '7': 6, '6': 5, '5': 4, '4': 3, '3': 2, '2': 1}

    
    # loop through each card in hand and store binary value ie 1/3/7/15
    for card in player.hand:
        if rankDict[card.rank] == 0:
            rankDict[card.rank] += 1
        else:
            rankDict[card.rank] = rankDict[card.rank] * 2 + 1  
        #store suits in array
        if card.suit == 'c':
            suitC[card.rank] += 1
        elif card.suit == 'h':
            suitH[card.rank] += 1
        elif card.suit == 's':
            suitS[card.rank] += 1
        else:
            suitD[card.rank] += 1
    
    # sum of total value of dict for hand result (not flushes and straights)
    val = sum(rankDict.values())

    # find flush
    if sum(suitC.values()) >= 5:
        flush = (True, "", 0)
        fDraw = suitC
    elif sum(suitH.values()) >= 5:
        flush = (True, "", 0)
        fDraw = suitH
    elif sum(suitS.values()) >= 5:
        flush = (True, "", 0)
        fDraw = suitS
    elif sum(suitD.values()) >= 5:
        flush = (True, "", 0)
        fDraw = suitD
    else:
        flush = (False, "", 0)
    

    if flush[0] == True:  # if flush = true then check for straight flush or flush value 
        fDraw = {k: fDraw[k]*cardVal[k] for k in fDraw} # add card values to flush array
        fVal, fCount = 0, 0 #counters for 5 card flush value
        tVal = 0 # counta for straight flush 
        lCard = '' # to store ace low incase of 5 high straight flush
        fhCard = "" # flush high card
        for r in fDraw.items():
            if r[1] > 0:
                if fhCard == "":
                    fhCard = r[0]
                tVal += 1
                if fCount <=4: # store flush value
                    fVal += r[1]
                    fCount += 1
                if r[0] == 'A':
                    lCard = 1
            else:
                tVal = 0
            #store high card of straight flush
            if tVal == 1:
                hCard = r[0]
            #check for highest streight flush        
            if tVal == 5:
                return ("Straight Flush {} high".format(hCard), 8, cardVal[hCard])
            # check for 5 high straight
            if r[0] == '2' and tVal == 4 and lCard == 1:
                return ("Straight Flush 5 high", 8, 4)
            else:
                flush = (True, "Flush {} high".format(fhCard), fVal)
    
    #4kind
    fKind = ""
    hCard = ""
    if val >= 18:        
        for r in rankDict.items():
            if r[1] == 15:
                fKind = r[0]
            elif r[1] > 0 and hCard == "":
                hCard = r[0]
            if fKind != "" and hCard != "":
                return ("Four of a Kind {}'s".format(fKind), 7, (cardVal[fKind] * 13) + cardVal[hCard])
    
    #full house
    tKind = ""
    tPair = ""
    if val >= 12:
        for r in rankDict.items():
            if r[1] == 7:
                if tKind == "":
                    tKind = r[0]
                elif tPair == "":
                    tPair = r[0]
            if r[1] == 3 and tPair == "":
               tPair = r[0]
            if tKind != "" and tPair != "":
                return ("Full House {}'s over {}'s".format(tKind, tPair), 6, (cardVal[tKind] * 13) + cardVal[tPair])
    
    # return flush
    if flush[0] == True:
        return (flush[1], 5, flush[2])
    
    #check for straights & add card strengths incase high card
    sCount = 0 # counta for 5 cards in a row
    hCard, lCard = "", "" # to store high card and ace low incase of 5 high straight
    hVal, hCount, hCardH = 0, 0, ""  #counter and val store if high card best hand
    for r in rankDict.items():
        if r[1] > 0:
            sCount += 1
            if r[0] == 'A':
                lCard = 1
            
            if val == 7: #add vaues for high card hand
                if hCardH == "":          
                    hCardH = r[0]
                if hCount <= 4: # add values of 5 highest cards for high card hand
                    hVal += cardVal[r[0]]
                    hCount += 1
        
        else:
            sCount = 0 # re-set straight counter
        
        if sCount == 1: # assign high card of straight
            hCard = r[0]
           
        if sCount == 5: #check for highest straight
            return ("Straight {} high".format(hCard), 4, cardVal[hCard])
        if r[0] == '2' and sCount == 4 and lCard == 1: # check for 5 high straight
            return ("Straight {} high".format(hCard), 4, 4)
        
    if val == 7: # if no straight or pairs return high card hand
        return ("High Card {}".format(hCardH), 0, hVal)

        
    #3Kind
    kck1 = ""
    kck2 = ""
    if val == 11:
        for r in rankDict.items():
            if r[1] == 7:
                tKind = r[0]
            elif r[1] == 1:
                if kck1 == "":
                    kck1 = r[0]
                else:
                    kck2 = r[0]
            if tKind != "" and kck1 != "" and kck2 != "":
                hVal = cardVal[tKind] * 26 + cardVal[kck1] * 13 + cardVal[kck2] # calculate sub hand val
                return ("Three of a Kind {}'s".format(tKind), 3, hVal) 
            
    #2pair    
    oPair = ""        
    if val >= 9:
        for r in rankDict.items():
            if r[1] == 3:
                if tPair == "":
                    tPair = r[0]
                else:
                    oPair = r[0]    
            elif r[1] == 1:
                if kck1 == "":
                    kck1 = r[0]
            if tPair != "" and oPair != "" and kck1 != "":
                hVal = cardVal[tPair] * 156 + cardVal[oPair] * 13 + cardVal[kck1] # calculate sub hand val
                return ("Two Pair {}'s over {}'s".format(tPair, oPair), 2, hVal)

    #1Pair            
    kck3 = ""      
    if val == 8:
        for r in rankDict.items():
            if r[1] == 3:
                oPair = r[0]
            elif r[1] == 1:
                if kck1 == "":
                    kck1 = r[0]
                elif kck2 == "":
                    kck2 = r[0]            
                else:
                    kck3 = r[0]
            if oPair != "" and kck1 != "" and kck2 != "" and kck3 != "":
                hVal = cardVal[oPair] * 54 + cardVal[kck1] + cardVal[kck2] + cardVal[kck3] # calculate sub hand val
                return ("One Pair {}'s".format(oPair), 1, hVal) 
   
    

if __name__ == "HandVal":
    HandVal()

# -*- coding: utf-8 -*-
"""
Created on Thu Dec  6 18:12:48 2018

@author: Kevin
"""

import random
import sys
from tabulate import tabulate
#AI schoppen zevenen
#1 schoppen
#2 klaveren
#3 ruiten
#4 harten

def check_input(inputted,minimal,maximal):
    if inputted == 'exit':
        sys.exit()
    try:
        inputted = int(inputted)
    except ValueError:
        print("Dit is geen geldige invoer")
        return(inputted,0)
    inputted = int(inputted)
    if inputted < minimal or inputted > maximal:
        print("Dit is geen geldige invoer")
        return(inputted,0)
    else:
        return(inputted,1)

def add_cart_to_hand(hand):
    cardlist=[0,0]
    success = 0
    while success == 0:
        cardlist[0] = input('Welke kleur kaart wordt ingevoerd? 1) Schoppen 2) Klaveren 3) Ruiten 4) Harten ')
        [cardlist[0],success]= check_input(cardlist[0],1,4)  
    success = 0
    while success == 0:
        cardlist[1] = input('Welke getal kaart wordt ingevoerd? 1) Aas ... 13) Koning ')
        [cardlist[1],success]= check_input(cardlist[1],1,13)
    if (cardlist[0]-1)*13+cardlist[1] not in hand:
        hand +=[(cardlist[0]-1)*13+cardlist[1]]
    return(hand)
    
def insert_hand():
    hand =[]
    success=0
    busy = 1
    print('Eerst moeten mijn kaarten ingevoerd worden.')
    while busy ==1:
        hand= add_cart_to_hand(hand)
        success=0
        while success == 0:
            print('Moeten er nog kaarten nog ingevoerd worden?')
            busy = input('1) Ja 2) Alle kaarten zijn ingevoerd. ')
            [busy,success]= check_input(busy,1,2)        
    return(hand)       

def kaarten_invoer(nr_of_cards):
    unshuffled = list(range(1,53))
    random.shuffle(unshuffled)
    return(unshuffled[:nr_of_cards]) 
    
def tick_board(board,card):
    board[card-1]=1
    return(board)
    
def playable_card(board,card,aces):
    cardlist= [int((card-1)/13),card%13]
    playable = False
    potaces = 0
    if cardlist[1] == 0:
        cardlist[1] =13
    if cardlist[1] == 7:
        return (True,potaces)
    elif cardlist[1] < 7 and cardlist[1] > 1:
        if board[card]==1:
            return (True,potaces)
    elif cardlist[1] > 7 and cardlist[1] < 14:
        if board[card-2]==1:
            return (True,potaces)
    elif cardlist[1] == 1:
        if aces != 2 and board[card] ==1:
            potaces +=1
            playable = True
        if aces != 1 and board[card+11] ==1:
            potaces +=2
            playable = True
    return (playable,potaces)
    
def aces_input():
    print('Ligt de aas hoog of laag?')
    success = 0
    while success == 0:
        aces = input('1) Laag 2) Hoog ')
        [aces,success]= check_input(aces,1,4)  
    return aces

def card_other_player(hand,board,aces):
    cardlist=[0,0]
    success = 0
    while success == 0:
        cardlist[0] = input('Welke kleur kaart is gespeeld? 1) Schoppen 2) Klaveren 3) Ruiten 4) Harten ')
        [cardlist[0],success]= check_input(cardlist[0],1,4)  
    success = 0
    while success == 0:
        cardlist[1] = input('Welke getal kaart is gespeeld? 1) Aas ... 13) Koning ')
        [cardlist[1],success]= check_input(cardlist[1],1,13)    
    input_card=(cardlist[0]-1)*13+cardlist[1]

    if any(owncards==input_card for owncards in hand):
        print("Deze kaart heb ik!")
        return(input_card,aces,False)
    else:
        if not playable_card(board,input_card,aces)[0]:
            print("Deze kaart kan nu niet gespeeld worden.")
            return(input_card,aces,False)
        else:                    
            if cardlist[1] == 1 and aces ==0:
                print("check")
                aces = aces_input()
            return(input_card,aces,True)

def value_pos_sub(hand,board,card_color,start_nr,end_nr): #start_nr <= end_nr
    multiple = [12,10,8,6,4,2,1,6,10,14,18,22,26,30]
    value_ind =0 
    for j in range(start_nr,end_nr):
        if board[(card_color-1)*13+j] == 0:
            value_ind+= multiple[j-1]
            if (card_color-1)*13+j+1 not in hand:
                value_ind+= multiple[j-1]
    return(value_ind)
    
def value_neg_sub(hand,board,card_color,start_nr,end_nr): #start_nr>= end_nr
    return(value_pos_sub(hand,board,card_color,end_nr,start_nr))

def value_card(hand,board,aces,card,potaces):
    value=0
    res_ind =0
    single=[11,10,9,8,6,4,1,2,3,5,7,12,13,14]
    cardlist= [int(card/13-1),((card-1)%13)+1]
    handlist = []
    subsequent_cards=[]
    for handcard in hand:
        handlist.append([int(handcard/13-1),(handcard-1)%13+1])     
            
    if cardlist[1] >= 7 or (cardlist[1] ==0 and aces !=1 and potaces ==2):
        if aces !=1:
            for handcardlist in handlist:
                if handcardlist == [cardlist[0],1]:
                    handcardlist = [cardlist[0],14]
        for i in range(cardlist[1]+1,14):
            if [cardlist[0],i] in handlist:
                subsequent_cards.append(i)
        if subsequent_cards == []:
            value= single[cardlist[1]-1]
        else:
            n= max(subsequent_cards)+1
            for i in range(cardlist[1],n):
                value += value_pos_sub(hand,board,cardlist[0],cardlist[1],i)      
        
    if (cardlist[1] < 7 and cardlist[1] > 1) or (cardlist[1] ==0 and aces !=2 and potaces ==1):
        if aces ==2:
            for handcardlist in handlist:
                if handcardlist == [cardlist[0],1]:
                    handcardlist = [cardlist[0],14]
        for i in range(1,cardlist[1]):
            if [cardlist[0],i] in handlist:
                subsequent_cards.append(i)
        if subsequent_cards == []:
            value= single[cardlist[1]-1]
        else:
            n= min(subsequent_cards)
            for i in range(cardlist[1],n):
                value += value_neg_sub(hand,board,cardlist[0],cardlist[1],i)  
                
    if cardlist[1]==1 and aces ==0:
        for i in range(1,5):
            if cardlist[0] != i:
                for i in range(1,8):
                    res_ind -= value_neg_sub(hand,board,cardlist[0],1,i)
                for i in range(7,14):
                    res_ind += value_pos_sub(hand,board,cardlist[0],i,14)
        if potaces ==1:
            value+= res_ind      
        if potaces ==2:
            value-= res_ind                
    return value
    
def pick_card(hand,board,aces):
    playable_cards=[]
    value_playables =[]
    for owncard in hand:
        if playable_card(board,owncard,aces)[0]:
            if playable_card(board,owncard,aces)[1] == 3:
                playable_cards.append([owncard,1])
                playable_cards.append([owncard,2])
            else:
                playable_cards.append([owncard,playable_card(board,owncard,aces)[1]])        
    for [now_playable_card,now_potaces] in playable_cards:
        value_playables.append(value_card(hand,board,aces,now_playable_card,now_potaces))
        
    result = playable_cards[value_playables.index(max(value_playables))]  
    if aces != 0 and result[1] ==0:
        result[1]=aces
    return result
    
def del_card_from_hand(card,hand):
    for i in range(len(hand)):
        if hand[i]==card:
            del hand[i]
            break
    return hand

def print_board(board):
    color = ['Schoppen ', 'Klaveren', 'Ruiten ','Harten ']
    number = ['','aas', 'twee', 'drie', 'vier', 'vijf', 'zes', 'zeven', 'acht', 'negen', 'tien', 'boer', 'vrouw', 'koning']
    boardsquare = [ [color[i]] + [board[j] for j in range(13*i,13*(i+1))]  for i in range(4) ]
    print(tabulate(boardsquare,headers=number,tablefmt="grid"))
    
def printed_card(hand,card,aces):
    for i in range(len(hand)):
        if hand[i]==card:
            card_nr = i+1
    cardlist = [int((card-1)/13),((card-1)%13)]
    color = ['Schoppen ', 'Klaveren', 'Ruiten ','Harten ']
    number = ['aas', 'twee', 'drie', 'vier', 'vijf', 'zes', 'zeven', 'acht', 'negen', 'tien', 'boer', 'vrouw', 'koning']
    print('Ik speel de', color[cardlist[0]], number[cardlist[1]],'.')
    print('Dit is kaart nummer', card_nr,'in mijn hand.')    
    if card % 13 ==1:
        if aces == 1:
            print('Ik leg de aas laag.')
        if aces == 2:
            print('Ik leg de aas hoog.')        
    return
    
def turn(hand,board,end,aces):
    print('Wat gebeurt er?')
    success = 0
    
    while success == 0:
        sit = input('1) Ik ben aan de beurt! 2) Iemand anders speelt een kaart. 3) Iemand heeft het spel gewonnen. 4) Laat de tafel zien. 5) Voeg kaart toe 6) Laat hand zien. ')
        [sit,success]= check_input(sit,1,6)
    if sit==1:
        if not any(playable_card(board,owncard,aces)[0] for owncard in hand):
            print('Pas.')
        else:
            [card,aces] = pick_card(hand,board,aces)
            printed_card(hand,card,aces)
            board=tick_board(board,card)
            hand = del_card_from_hand(card,hand)
            if hand ==[]:
                end = 1                
    elif sit ==2:
        (card,aces, really_played) = card_other_player(hand,board,aces)
        if really_played == True:
            tick_board(board,card)
    elif sit ==3:
        end=1
    elif sit ==4:
        print_board(board)
    elif sit ==5:
        hand=add_cart_to_hand(hand)
    elif sit ==6:
        print('Hand: ', hand)
    return [hand,board,end,aces]

def game():
    aces=0
    end =0
    starting =0
    board=[0]*52
    #hand= []
    #hand=kaarten_invoer(13)
    hand=insert_hand()
    for i in range(len(hand)):        
        if hand[i]==7:
            del hand[i]
            board=tick_board(board,7)
            print('Ik heb de schoppen zeven!')
            starting =1
            break
    if starting ==0:
        print('Ik mag niet beginnen.')
    while end ==0:
        [hand,board,end,aces]=turn(hand,board,end,aces)   

def main():
    print('Welkom bij de bots voor schoppen zevenen.')
    success = 0
    while success == 0:
        player_nr = input('Kies een speler: 1) Bob ')
        [player_nr,success]= check_input(player_nr,1,1)
    if player_nr == 1:     
        print('Hoi! Ik ben Bob. Gaan wij schoppen zevenen?')
    success = 0
    while success == 0:
        check_start = input('1) Ja 2) Nee ')
        [check_start,success]= check_input(check_start,1,2)
    if check_start == 2:
        sys.exit()
    game()
main()
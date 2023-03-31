# -*- coding: utf-8 -*-
from board import *
from actions import *
from players import *
from aiplayer import AIPlayer1
from aiplayer import AIPlayer2
from time import time_ns
from aiplayer import AIPlayer_v0
from aiplayer import AIPlayer_force_1
from aiplayer import AIPlayer_force_2
from aiplayer import AIPlayer_test

# UN COUP DOIT S EXECUTER EN MOINS DE 10s

def genere_strat_v0(acte, contraint, move):
    st='board.getMarbleCount(self.player) + '+str(acte)+'*acte_moi + '+str(contraint)+'*contraint_moi + '+str(move)+'*move_pour_moi_destination_diff - board.getMarbleCount(-self.player) - '+str(acte)+'*acte_adv - '+str(contraint)+'*contraint_adv - '+str(move)+'*move_pour_adv_destination_diff'
    return str(st)

def genere_strat_v1(carr, move):
    st='board.getMarbleCount(self.player) + '+str(carr)+'*carresuivant_pour_moi + '+str(move)+'*move_pour_moi_destination_diff - board.getMarbleCount(-self.player) - '+str(carr)+'*carresuivant_pour_adv - '+str(move)+'*move_pour_adv_destination_diff'
    return str(st)

def joue_strat_en_1(strat):
    board = Board()
    player1 = AIPlayer_test(strat)
    player1.name = "player1 (%s)"%(player1.name)
    player1.player = -1

    player2 = AIPlayer_v0() #HumanPlayer("nom") si on veut input les coups à la main
    player2.name = "player2 (%s)"%(player2.name)
    player2.player = 1

    current_player = 0
    players = [player1, player2]



    while not board.isTerminal():

        action = players[current_player].getNextMove(board)

        action.apply(players[current_player].player, board)
        current_player = 1-current_player
        

    winner = board.getWinner()
    diff=board.getMarbleCount(winner)
    
    return winner, diff

def joue_strat_en_2(strat):
    board = Board()
    player1 = AIPlayer_v0()
    player1.name = "player1 (%s)"%(player1.name)
    player1.player = -1

    player2 = AIPlayer_test(strat) #HumanPlayer("nom") si on veut input les coups à la main
    player2.name = "player2 (%s)"%(player2.name)
    player2.player = 1

    current_player = 0
    players = [player1, player2]



    while not board.isTerminal():

        action = players[current_player].getNextMove(board)

        action.apply(players[current_player].player, board)
        current_player = 1-current_player
        

    winner = board.getWinner()
    diff=board.getMarbleCount(winner)
    
    return winner, diff


VS_s0={}

def opti_vss0_v0(rangeacte=7, rangecontraint=10, rangemove=10):
    acte=0.25
    contraint=0
    move=0
    compte=0
    for a in range(rangeacte):
        contraint=0
        for c in range(rangecontraint):
            move=0
            for m in range(rangemove):
                debut=time_ns()
                compte+=1
                print("Stratégie numéro %d" %compte)
                strategieactuelle=genere_strat_v0(acte, contraint, move)
                cle=tuple([a,c,m])
                res={}
                for k in range(2):
                    if k==0:
                        resultat1=joue_strat_en_1(strategieactuelle)
                        winner1=resultat1[0]
                        diff1=resultat1[1]
                        if winner1==-1:
                            res['winner1']=1
                        else:
                            res['winner1']=-1
                        res['diff1']=diff1
                    elif k==1:
                        resultat2=joue_strat_en_2(strategieactuelle)
                        winner2=resultat2[0]
                        diff2=resultat2[1]
                        if winner2==-1:
                            res['winner2']=-1
                        else:
                            res['winner2']=1
                        res['diff2']=diff2
                res['nbvictoires']=res['winner1']+res['winner2']
                VS_s0[cle]=res
                fin=time_ns()
                print([acte, contraint, move])
                print(res)
                print("Temps d'éxécution : %f s" %((-debut+fin)/1000000000))
                move+=0.15
            contraint+=0.08
        acte+=0.25
    return VS_s0
                
def opti_vss0_v1(rangecarr=22, rangemove=11):
    carresuiv=0.1
    move=0
    compte=0
    for c in range(rangecarr):
        move=0
        for m in range(rangemove):
            debut=time_ns()
            compte+=1
            print("Stratégie numéro %d" %compte)
            strategieactuelle=genere_strat_v1(carresuiv, move)
            cle=tuple([carresuiv,move])
            res={}
            for k in range(2):
                if k==0:
                    resultat1=joue_strat_en_1(strategieactuelle)
                    winner1=resultat1[0]
                    diff1=resultat1[1]
                    if winner1==-1:
                        res['winner1']=1
                    else:
                        res['winner1']=-1
                    res['diff1']=diff1
                elif k==1:
                    resultat2=joue_strat_en_2(strategieactuelle)
                    winner2=resultat2[0]
                    diff2=resultat2[1]
                    if winner2==-1:
                        res['winner2']=-1
                    else:
                        res['winner2']=1
                    res['diff2']=diff2
            res['nbvictoires']=res['winner1']+res['winner2']
            VS_s0[cle]=res
            fin=time_ns()
            print([carresuiv, move])
            print(res)
            print("Temps d'éxécution : %f s" %((-debut+fin)/1000000000))
            move+=0.12
        carresuiv+=0.1
    return VS_s0

        
resultat=opti_vss0_v1()


# load pickle module
import pickle

# create a binary pickle file 
f = open("VS_s0.pkl","wb")

# write the python object (dict) to pickle file
pickle.dump(resultat,f)

# close file
f.close()





# open file for writing
g = open("VS_s0.txt","w")

# write file
g.write( str(resultat) )

# close file
g.close()



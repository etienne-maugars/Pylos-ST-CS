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

def genere_strat(carre, move, nb):
    st='board.getMarbleCount(self.player) + '+str(carre)+'*carresuivant_pour_moi + '+str(move)+'*move_moi_utile + '+str(nb)+'*nbcarretotal - board.getMarbleCount(-self.player) - '+str(carre)+'*carresuivant_pour_adv - '+str(move)+'*move_adv_utile'
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



          
def opti(rangecarr, rangemove, rangenb):
    debutdebut=time_ns()
    total=rangecarr*rangemove*rangenb
    carresuiv_vs_s0={}
    carresuiv=0.1
    move=0
    nb=0
    compte=0
    for c in range(rangecarr):
        carresuiv_vs_s0[carresuiv]={}
        move=0
        for m in range(rangemove):
            carresuiv_vs_s0[carresuiv][move]={}
            nb=0
            for n in range(rangenb):
                carresuiv_vs_s0[carresuiv][move][nb]={}
                debut=time_ns()
                compte+=1
                print("     - Stratégie numéro %d sur %d : " %(compte,total))
                print([carresuiv, move, nb])                
                strategieactuelle=genere_strat(carresuiv, move, nb)
                for k in range(2):
                    if k==0:
                        resultat1=joue_strat_en_1(strategieactuelle)
                        winner1=resultat1[0]
                        diff1=resultat1[1]
                        if winner1==-1:
                            carresuiv_vs_s0[carresuiv][move][nb]['win1']=1
                        else:
                            carresuiv_vs_s0[carresuiv][move][nb]['win1']=-1
                        carresuiv_vs_s0[carresuiv][move][nb]['diff1']=carresuiv_vs_s0[carresuiv][move][nb]['win1']*diff1
                    elif k==1:
                        resultat2=joue_strat_en_2(strategieactuelle)
                        winner2=resultat2[0]
                        diff2=resultat2[1]
                        if winner2==-1:
                            carresuiv_vs_s0[carresuiv][move][nb]['win2']=-1
                        else:
                            carresuiv_vs_s0[carresuiv][move][nb]['win2']=1
                        carresuiv_vs_s0[carresuiv][move][nb]['diff2']=carresuiv_vs_s0[carresuiv][move][nb]['win2']*diff2
                carresuiv_vs_s0[carresuiv][move][nb]['totalwin']=carresuiv_vs_s0[carresuiv][move][nb]['win1']+carresuiv_vs_s0[carresuiv][move][nb]['win2']
                carresuiv_vs_s0[carresuiv][move][nb]['totaldiff']=carresuiv_vs_s0[carresuiv][move][nb]['diff1']+carresuiv_vs_s0[carresuiv][move][nb]['diff2']
                fin=time_ns()
                print(carresuiv_vs_s0[carresuiv][move][nb])
                print("Temps d'éxécution : %f s" %((-debut+fin)/1000000000))
                print('\n')
                nb+=0.05
            move+=0.05
        carresuiv+=0.05
    finfin=time_ns()
    print("Temps total d'éxécution : %f min" %((finfin-debutdebut)/(1000000000*60)))
    return carresuiv_vs_s0

        
resultat=opti(8, 10, 6)


# load pickle module
import pickle

# create a binary pickle file 
f = open("carresuiv_vs_s0_prof4.pkl","wb")

# write the python object (dict) to pickle file
pickle.dump(resultat,f)

# close file
f.close()





# open file for writing
g = open("carresuiv_vs_s0_prof4.txt","w")

# write file
g.write( str(resultat) )

# close file
g.close()



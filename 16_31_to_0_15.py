from analyse import acte_force_9

# -*- coding: utf-8 -*-
from board import *
from actions import *
from players import *
from aiplayer import AIPlayer1
from aiplayer import AIPlayer2
from time import time_ns
from aiplayer import AIPlayer_v0
from aiplayer import AIPlayer_test

import numpy as np
np.set_printoptions(threshold=16)

# UN COUP DOIT S EXECUTER EN MOINS DE 10s


def genere_strat(carre, move, nb):
    st='board.getMarbleCount(self.player) + center_moi + '+str(carre)+'*acte_moi + '+str(move)+'*move_moi_utile + '+str(nb)+'*nbcarretotal - board.getMarbleCount(-self.player) - center_adv - '+str(carre)+'*acte_adv - '+str(move)+'*move_adv_utile'
    return str(st)


result=np.zeros((32,32))

debutdebut=time_ns()
for i in range(16,32):
    for j in range(16):
        s1=[acte_force_9[i][0][k] for k in range(3)]
        s2=[acte_force_9[j][0][k] for k in range(3)]

        #print(type(s1))

        strat1=genere_strat(s1[0], s1[1], s1[2])
        strat2=genere_strat(s2[0], s2[1], s2[2])

        print(' - Stratégie %s contre %s' %(i,j))
        print(s1,s2)


        board = Board()
        player1 = AIPlayer_test(strat1)
        player1.name = "player1 (%s)"%(player1.name) #Joueur i
        player1.player = -1

        player2 = AIPlayer_test(strat2) #Joueur j
        player2.name = "player2 (%s)"%(player2.name)
        player2.player = 1

        current_player = 0
        players = [player1, player2]

        debut=time_ns()


        while not board.isTerminal():
            action = players[current_player].getNextMove(board)
            action.apply(players[current_player].player, board)
            current_player = 1-current_player
      
        winner = board.getWinner() #Player 1 si c'est -1, Plyaer 2 si c'est 1
        diff=board.getMarbleCount(winner)
        
        if winner==-1:
            print(str(i)+' en P1 a gagné contre '+str(j)+' en P2 %d-0' %diff)
            result[i,j]=diff
        elif winner==1:
            print(str(j)+' en P2 a gagné contre '+str(i)+' en P1 %d-0' %diff)
            result[i,j]=-diff

        fin=time_ns()

        print("Temps de la partie : %f s" %((fin-debut)/1000000000))
        

        print(result)
        
        print('\n')
finfin=time_ns()
print("Temps total d'éxécution : %f min" %((finfin-debutdebut)/(1000000000*60)))

        
        
np.savetxt("tournoi_acte_force_9_16_31_to_0_15.txt", result)


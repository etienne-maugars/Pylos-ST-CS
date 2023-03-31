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

# UN COUP DOIT S EXECUTER EN MOINS DE 10s


result=np.zeros((17,17))

"""
Output : une matrice D 17x17
tq D[i,j]=différence pour i lors du match strati VS stratj
ie si D[i,j]=-3, le joueur 1 qui joue strati a perdu 3 0 contre le joueur 2 qui joue stratj
"""

for i in range(17):
    for j in range(17):
        strat1='s'+str(i)
        strat2='s'+str(j)

        print('Stratégie %s contre %s' %(strat1,strat2))

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
            print(strat1+' en P1 a gagné contre '+strat2+' en P2 %d-0' %diff)
            result[i,j]=diff
        elif winner==1:
            print(strat2+' en P2 a gagné contre '+strat1+' en P1 %d-0' %diff)
            result[i,j]=-diff

        fin=time_ns()

        print("Temps de la partie : %f s" %((fin-debut)/1000000000))
        

        print(result)
        
        print('\n')
        
        
        
        

# open file for writing
g = open("tournoi.txt","w")

# write file
g.write( str(result) )

# close file
g.close()

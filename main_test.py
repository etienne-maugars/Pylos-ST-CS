# -*- coding: utf-8 -*-
from board import *
from actions import *
from players import *
from aiplayer import AIPlayer1
from aiplayer import AIPlayer2
from time import time_ns
from aiplayer import AIPlayer_v0
from aiplayer import AIPlayer_test

# UN COUP DOIT S EXECUTER EN MOINS DE 10s

def genere_strat(carre, move, nb):
    st='board.getMarbleCount(self.player) + center_moi + '+str(carre)+'*acte_moi + '+str(move)+'*move_moi_utile + '+str(nb)+'*nbcarretotal - board.getMarbleCount(-self.player) - center_adv - '+str(carre)+'*acte_adv - '+str(move)+'*move_adv_utile'
    return str(st)


board = Board()
player1 = HumanPlayer("moi") #AIPlayer_test(genere_strat(0.1, 0.25, 0.05))
player1.name = "player1 (%s)"%(player1.name)
player1.player = -1

player2 = AIPlayer_test(genere_strat(0.1, 0.25, 0.05))#AIPlayer_v0() #HumanPlayer("moi") #si on veut input les coups à la main
player2.name = "player2 (%s)"%(player2.name)
player2.player = 1

current_player = 0
players = [player1, player2]

print(board)
print()

debut=time_ns()

maxitime1=-1.
maxitime2=-1.
while not board.isTerminal():
    print("current player: %s"%(players[current_player].name))
    start = time_ns()
    action = players[current_player].getNextMove(board)
    diff=float((time_ns()-start)/1000000.0)
    print("Temps d'execution: %d ms"%(diff))
    if current_player==0: #joueur 1
        if diff>=maxitime1:
            maxitime1=diff
    elif current_player==1: #joueur 2
        if diff>=maxitime2:
            maxitime2=diff
    action.apply(players[current_player].player, board)
    current_player = 1-current_player
    

    try:
        print("Evaluation du plateau pour le joueur 1 : ")
        print(player1.show_heuristic(board))
        print('\n')
    except:
        print()

    try:
        print("Evaluation du plateau pour le joueur 2 : ")
        print(player2.show_heuristic(board))
        print('\n')
    except:
        print()
    
    print(board)
    print()
    
    

    
winner = board.getWinner()

fin=time_ns()

if winner == -1: 
    print(player1.name+" won")
elif winner == 1:
    print(player2.name+" won")
else:
    print("No winner")
    
print("Temps max joueur 1 (ms) : %f"%maxitime1)
print("Temps max joueuer 2 (ms) : %f"%maxitime2)

print("Temps de la partie : %f s" %((fin-debut)/1000000000))
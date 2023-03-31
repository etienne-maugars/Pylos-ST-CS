# Etienne MAUGARS

# -*- coding: utf-8 -*-

from cmath import inf
from typing import List
from players import Player
from actions import *
from board import Board
from math import inf

"""
    Historique de mon travail :

Après avoir joué plusieurs parties contre l'heuristique naïve pour me familiariser
avec les mécaniques du jeu, je me suis dit qu'il fallait 'prendre de l'avance' sur l'arbre de jeu,
en détectant certaines situations favorables à un joueur sans pour autant aller trop profond
dans l'arbre de jeu.
Ainsi, j'ai d'abord voulu coder une fonction de reconnaissance de '3/4', 
ie de situations comme ceci :

  i
j 0 W
  W W

C'est la fonction possible_square_next_move.

Ensuite, j'ai voulu détecter si on pouvait bouger une bille à un étage supérieur.
C'est la fonction possiblemove qui utilise les fonctions auxiliaires places_en_haut et getfree.

J'ai ensuite analysé un peu ce que j'ai mesuré, et défini différentes variantes de ces mesures (notamment en introduisant
des grandeurs 'utiles').

Une fois ces fonctions codées, j'ai testé avec quelques coefficients choisis au hasard de jouer contre ces stratégies.
Les résultats étaient pas vraiment satisfaisants puisque je gagnais toujours avec de grands scores.
Les stratégies que j'ai testées sont celles qui s'appellent entre s1 et s17.

Evidemment, je me suis rendu compte après plusieurs tests (en affichant les grandeurs au cours de partie) que
mes fonctions étaient complètement buguées.
Donc j'ai résolu ce problème, pour que ce avec quoi on calcule l'heuristique ait une vraie signification.

J'ai ensuite encore une fois mis des coeffs un peu au pif, et d'un coup ça marchait mieux.
Tout ça a été fait en profondeur 4.

Du coup pour mettre des coeffs plus appropriés, j'ai voulu faire jouer ces stratégies contre l'heuristique naïve, pour avoir un référentiel :
pour chaque variante de 3/4 et mov, j'ai fait varier les coeffs entre deux valeurs que je définissais,
et en faisant en sorte qu'il y ait au moins 10 valeurs différentes pour chaque variante.

J'ai commencé à run ce tournoi en profondeur 4, et c'était très (trop) lent.
Donc j'ai essayé de rendre l'évaluation de l'heuristique plus performante.
Je savais comment améliorer la performance : avant, je parcourais tout le plateau une fois pour les 3/4, 
3 fois pour les move. Mais je pouvais le parcourir une seule fois en regroupant ces fonctions en une seule.
J'ai donc codé la fonction donne_tout, qui renvoie les grandeurs d'évaluation nécessaires en ne parcourant qu'une fois
le plateau.
Elle introduit aussi une nouvelle grandeur que j'appelle les 'presque carrés' :
  j
i 0 W
  B B
car j'ai remarqué qu'il ne faut pas créer de carré en premier car cela crée une opportunité pour l'adversaire de monter
Ainsi, introduire cette mesure faisait créer un 'pavage' de presque carrés à chaque niveau, et c'est ce que je souhaitais.
 
Cela améliorait beaucoup le temps d'éxécution, mais il me restait maintenant à trier les coups.
Pour cela, j'ai vu que les classes du fichier actions.py étaient :
- la classe d'action où l'on ajoute une nouvelle bille depuis notre stock
- la classe d'action où l'on bouge une bille
- la classe d'action où l'on complète un carré
J'ai donc trié les coups en faisant évaluer d'abord les coups qui font compléter un carré, puis les moves, puis
l'ajout de bille depuis son stock.
Cela a un peu amélioré le temps, mais pas autant que l'optimisation de donne_tout.

Pour tester si je pouvais aller plus loin en profondeur, j'ai essayé la profondeur 5. Je me suis alors rendu compte
que l'IA joue toujours son premier coup (quand elle est en P1) à la case (1,1), ce qui n'est pas le cas en profondeur 4.
Je me suis donc dit que c'était mieux de commencer ici (et ça ne me semblait pas bête au vu des mécaniques du jeu).
J'ai donc introduit une grandeur center_moi/center_adv qui est non nulle uniquement s'il y a moins de 4 billes sur le plateau.
Elle fait commencer l'IA en (1,1).

Finalement, j'ai lancé mon tournoi, qui faisait donc varier les coefficients associés aux moves, aux 3/4 et aux presque_carrés.
Il a pris environ 36h à s'éxécuter (en profondeur 4).
J'ai mesuré les résultats en produisant un dictionnaire dont les clés étaient les coefficients de chaque grandeur,
et dont les valeurs étaient la différence de bille finale entre mon IA et la stratégie naïve, pour mon IA qui joue en P1
mais aussi lorsqu'elle joue en P2.
Ainsi, je mesurais la performance de mes stratégies aussi bien en P1 qu'en P2.

En analysant les résultats, il se trouve que les meilleures stratégies battaient la stratégie naïve 4-0 en jouant en P1,
et 5-0 en jouant en P2.
Il y avait en tout 32 stratégies qui arrivaient à cela.
Elles utilisaient toutes les grandeurs center_moi/adv, acte_moi/adv, move_moi/adv_utile, nbcarretotal.

Je me suis alors concentré sur ces 32 stratégies.

Pour les départager, je les ai fait jouer cette fois-ci entre elles.
J'ai donc produit une matrice D telle que
D[i,j] = différence de bille finale entre joueur 1 et joueur 2, où joueur1 joue la stratégie i et joueur 2 joue la stratégie j.
Exemple : si D[i,j] = -3, alors strat_j en P2 a gagné 3-0 contre strat_i en P1.
Encore une fois, je pouvais alors mesurer leur performance en tant que P1 et aussi en tant que P2.

Dans cette matrice, il n'y avait aucun coefficient positif : aucune stratégie n'était gagnante en jouant en P1.
Mais certaines perdaient plus que d'autres.
Ainsi, j'ai appliqué le procédé suivant pour les départager :
Pour une stratégie i, on veut qu'elle perde le moins possible en P1, ie 
que la somme des coefficients de la ligne i soit maximale.
On veut aussi qu'elle gagne avec le plus gros écart en P2, ie
que la somme des coefficients de la colonne i soit minimale.
Ainsi, on veut maximiser (somme des coefficients de la ligne i) - (somme des coefficients de la colonne i).

En effectuant ce filtrage, on aboutit à 8 stratégies (qui offrent donc les meilleures performances).
Parmi ces 8 stratégies, toutes ont un coefficient de move=0.25 et de nbcarretotal=0.05.
Seul le coefficient de acte_moi/adv changeait.

Là, à court d'idées pour les départager, j'ai joué en tant que HumanPlayer contre chacune, à chaque fois en tant que P1 et en tant que P2.
Il y en a 3 que je battais très facilement et dont le comportement ne me plaisait pas (c'était pour les valeurs extrémales de acte_moi/adv).

Pour les 5 autres, après plusieurs parties contre chacune, j'ai décidé de sélectionner une qui me battait tout le temps
et dont le comportement me plaisait.

Voilà comment je suis arrivé à la stratégie que j'ai nommé sdef.

J'ai hésité entre profondeur 4 et 5 car à 4, le temps max que ça prend est ~3s par coup mais en 5, ça peut arriver à 24s
(mais en moyenne c'est 8).

Pour jouer la sécurité par rapport aux 10s, je mets 4 mais c'est un peu frustrant...

Merci d'avoir lu !
"""



s0='board.getMarbleCount(self.player) - board.getMarbleCount(-self.player)'
s1='board.getMarbleCount(self.player) + 2*acte_moi + len(moves_moi) - board.getMarbleCount(-self.player) - 2*acte_adv - len(moves_adv)'
s2='1.5*board.getMarbleCount(self.player) + 2*acte_moi + len(moves_moi) - 1.5*board.getMarbleCount(-self.player) - 2*acte_adv - len(moves_adv)'
s3='1.3*board.getMarbleCount(self.player) + 2*acte_moi + len(moves_moi) - 1.3*board.getMarbleCount(-self.player) - 2*acte_adv - len(moves_adv)'
s4='1.1*board.getMarbleCount(self.player) + 2*acte_moi + len(moves_moi) - 1.1*board.getMarbleCount(-self.player) - 2*acte_adv - len(moves_adv)'
s5='board.getMarbleCount(self.player) + 2*carresuivant_pour_moi + len(moves_moi) - board.getMarbleCount(-self.player) - 2*carresuivant_pour_adv - len(moves_adv)'
s6='board.getMarbleCount(self.player) + 2*carresuivant_pour_moi + 0.15*contraint_moi + len(moves_moi) - board.getMarbleCount(-self.player) - 2*carresuivant_pour_adv - 0.15*contraint_adv - len(moves_adv)'
s7='board.getMarbleCount(self.player) + 2*acte_moi + move_pour_moi_destination_diff - board.getMarbleCount(-self.player) - 2*acte_adv - move_pour_adv_destination_diff'
s8='board.getMarbleCount(self.player) + 2.4*acte_moi + 1.2*move_pour_moi_destination_diff - board.getMarbleCount(-self.player) - 2.4*acte_adv - 1.2*move_pour_adv_destination_diff'
s9='board.getMarbleCount(self.player) + 2.1*acte_moi + 1.05*move_pour_moi_destination_diff - board.getMarbleCount(-self.player) - 2.1*acte_adv - 1.05*move_pour_adv_destination_diff'
s10='board.getMarbleCount(self.player) + 2.1*acte_moi + 0.15*contraint_moi + 1.05*move_pour_moi_destination_diff - board.getMarbleCount(-self.player) - 2.1*acte_adv - 0.15*contraint_adv - 1.05*move_pour_adv_destination_diff'
s11='board.getMarbleCount(self.player) + 2*acte_moi + 0.15*contraint_moi + 1.05*move_pour_moi_destination_diff - board.getMarbleCount(-self.player) - 2*acte_adv - 0.15*contraint_adv - 1.05*move_pour_adv_destination_diff'
s12='board.getMarbleCount(self.player) + 2*acte_moi + 0.1*contraint_moi + len(moves_moi) - board.getMarbleCount(-self.player) - 2*acte_adv - 0.1*contraint_adv - len(moves_adv)'
s13='board.getMarbleCount(self.player) + 2.4*acte_moi + 0.1*contraint_moi + 1.2*move_pour_moi_destination_diff - board.getMarbleCount(-self.player) - 2.4*acte_adv - 0.1*contraint_adv - 1.2*move_pour_adv_destination_diff'
s14='board.getMarbleCount(self.player) + 0.5*acte_moi + 0.05*contraint_moi + 0.2*move_pour_moi_destination_diff - board.getMarbleCount(-self.player) - 0.5*acte_adv - 0.05*contraint_adv - 0.2*move_pour_adv_destination_diff'
s15='board.getMarbleCount(self.player) + 0.5*acte_moi + 0.05*contraint_moi + 0.2*move_pour_moi_destination_diff + 0.2*nbcarretotal- board.getMarbleCount(-self.player) - 0.5*acte_adv - 0.05*contraint_adv - 0.2*move_pour_adv_destination_diff'
stest='board.getMarbleCount(self.player) + 0.5*carresuivant_pour_moi + 0.2*move_pour_moi_destination_diff + 0.2*nbcarretotal - board.getMarbleCount(-self.player) - 0.5*carresuivant_pour_adv - 0.2*move_pour_adv_destination_diff'
stest1='board.getMarbleCount(self.player) + 1*center_moi + 0.25*carresuivant_pour_moi + 0.2*move_pour_moi_destination_diff + 0.2*nbcarretotal - board.getMarbleCount(-self.player) - 1*center_adv - 0.25*carresuivant_pour_adv - 0.2*move_pour_adv_destination_diff'
stest2='board.getMarbleCount(self.player) + 0.5*carresuivant_pour_moi + 0.4*move_pour_moi_destination_diff + 0.2*nbcarretotal - board.getMarbleCount(-self.player) - 0.5*carresuivant_pour_adv - 0.4*move_pour_adv_destination_diff'
stest3='board.getMarbleCount(self.player) + center_moi + 0.1*acte_moi + 0.25*move_moi_utile + 0.05*nbcarretotal - board.getMarbleCount(-self.player) - center_adv - 0.1*acte_adv - 0.25*move_adv_utile'
stest4='board.getMarbleCount(self.player) + center_moi + 0.1*acte_moi + 0.25*move_moi_utile + 0.05*nbcarretotal - board.getMarbleCount(-self.player)'
s16='board.getMarbleCount(self.player) + 0.8*acte_moi + 0.48*contraint_moi + 1.2*move_pour_moi_destination_diff - board.getMarbleCount(-self.player) - 2.4*acte_adv - 0.1*contraint_adv - 1.2*move_pour_adv_destination_diff'

sdef='board.getMarbleCount(self.player) + center_moi + 0.1*acte_moi + 0.25*move_moi_utile + 0.05*nbcarretotal - board.getMarbleCount(-self.player) - center_adv - 0.1*acte_adv - 0.25*move_adv_utile'




class AIPlayer(Player):
    """Artificial Intelligence based player"""
    def __init__(self):
        super().__init__("MAUGARS Etienne") #A CHANGER EN METTANT SON NOM
        self.__maxdepth = 4 #mettez ici la profondeur max de votre alpha beta en n'oubliant que vous devez répondre en 10s)

    def getNextMove(self, board: Board) -> Action: #Pas toucher
        """Gets the next move to play"""
        return self.alphabeta(board)

    def heuristic(self, board:Board) -> float: #Là on peut toucher
        """Heuristic for alpha-beta, to be modified by the students"""
        if board.getTop() == self.player or board.getMarbleCount(-self.player) == 0:
            return inf
        elif board.getTop() == -self.player or board.getMarbleCount(self.player) == 0:
            return -inf
        else:
            #Calculer ici votre heuristique
            #Une valeur positive et grande indique que le plateau est favorable à votre IA
            #Une valeur très négative indique que le plateau est défavorable à votre IA
            
            tout=[]
            for level in range(3):
                tout.append(self.donne_tout(self.player, level, board))

            """
            tout est [ [possiblesquares(level=0), possiblemove(level=0), nbcarre(0)],
                       [possiblesquares(level=1), possiblemove(level=1), nbcarre(1)],
                       [possiblesquares(level=2), possiblemove(level=2), nbcarre(2)],
                     ]
            """
 
            carresuivant_pour_adv=0
            carresuivant_pour_moi=0
   
            moves_moi=[tout[k][1][0] for k in range(3)]
            moves_adv=[tout[k][1][1] for k in range(3)]
            
            nbcarretotal=0
            
            for k in range(3):
                nbcarretotal+=tout[k][2]
                   
                carresuivant_pour_moi+=tout[k][0][0]
                carresuivant_pour_adv+=tout[k][0][1]
            
                #carresuivant_pour_adv
            #Donne le nombre de situations pour l'adversaire où je suis capable de compléter un carré en un coup
            #S'il y en a un, l'adversaire le contre mais on le contraint l'adversaire
            #S'il y en a deux, on en joue un mais l'autre est bloqué au prochain tour --> contraint l'adversaire
            #S'il y en a trois, on en joue un, deux sont bloqués --> on contraint l'adversaire
            #On accorde 0,2 au fait de contraindre l'adversaire (mais on multiplie par 2 dans le return)
            #donc ce qui nous intéresse c'est le nombre de carrés que je pourrai compléter sûrement : carresuivant_pour_moi//2
            #et auss ile nombre de coups que je contrains mon adversaire à faire : (carresuivant_pour_moi+1)//2
            contraint_adv=0 #Ca contraint moi
            acte_adv=0
            if carresuivant_pour_adv!=0:
                contraint_adv=(carresuivant_pour_adv)//2
            if carresuivant_pour_adv>=2:
                acte_adv=(carresuivant_pour_adv+1)//2
            carresuivant_pour_adv_utile = acte_adv + 0.1*contraint_adv            
            
            
                #carresuivant_pour_moi
            #Donne le nombre de situations pour moi où je suis capable de compléter un carré en un coup
            #S'il y en a un, l'adversaire le contre mais on le contraint l'adversaire
            #S'il y en a deux, on en joue un mais l'autre est bloqué au prochain tour --> contraint l'adversaire
            #S'il y en a trois, on en joue un, deux sont bloqués --> on contraint l'adversaire
            #On accorde 0,2 au fait de contraindre l'adversaire (mais on multiplie par 2 dans le return)
            #donc ce qui nous intéresse c'est le nombre de carrés que je pourrai compléter sûrement : carresuivant_pour_moi//2
            #et auss ile nombre de coups que je contrains mon adversaire à faire : (carresuivant_pour_moi+1)//2
            contraint_moi=0 #Ca contraint l'adversaire
            acte_moi=0
            if carresuivant_pour_moi!=0:
                contraint_moi=(carresuivant_pour_moi+1)//2
            if carresuivant_pour_moi>=2:
                acte_moi=carresuivant_pour_moi//2
            carresuivant_pour_moi_utile = acte_moi + 0.1*contraint_moi
            
            
                #moves_moi = [moves_moi_level1, moves_moi_level2, moves_moi_level2]
            #Ce qui est important ici, c'est qu'il y ait au moins 2 endroits où bouger puisque s'il y en a qu'un, le spot va être pris par l'adversaire
            
            #On compte donc le nombre de destinations possibles, ie le nombre de valeurs de chaque dic
            move_pour_moi_destination_diff=0
            deja_vus_moi=[]
            
            for moves_moi_level in moves_moi:
                for bougeable in moves_moi_level:
                    for elt in moves_moi_level[bougeable]: #les destinations
                        if elt not in deja_vus_moi:
                            move_pour_moi_destination_diff+=1
                            deja_vus_moi.append(elt)
                        
            #On peut aussi simplement compter le nombre de billes bougeables :
            nb_moves_possibles_moi=0
            for elt in moves_moi:
                nb_moves_possibles_moi+=len(elt)
                
            #On définit un move_utile
            move_moi_utile=min(move_pour_moi_destination_diff, nb_moves_possibles_moi)

                #moves_adv = [moves_adv_level1, moves_adv_level2, moves_adv_level2]
            #Ce qui est important ici, c'est qu'il y ait au moins 2 endroits où bouger puisque s'il y en a qu'un, le spot va être pris par l'adversaire
            #On compte donc le nombre de destinations possibles
            move_pour_adv_destination_diff=0
            deja_vus_adv=[]
            
            for moves_adv_level in moves_adv:
                for bougeable in moves_adv_level:
                    for elt in moves_adv_level[bougeable]: #les destinations
                        if elt not in deja_vus_adv:
                            move_pour_adv_destination_diff+=1
                            deja_vus_adv.append(elt)
                        
            #On peut aussi simplement compter le nombre de moves possibles :
            nb_moves_possibles_adv=0
            for elt in moves_adv:
                nb_moves_possibles_adv+=len(elt)  
        
            #On définit un move_utile   
            move_adv_utile=min(move_pour_adv_destination_diff, nb_moves_possibles_adv)
                
            center_moi=0    
            center_adv=0
            if self.compte_actives(board)<=4:
                center_moi+=self.centered_or_not(board, self.player)
                center_adv+=self.centered_or_not(board, -self.player)

            resultat=eval(sdef)
            
            return resultat
 
    def compte_actives(self, board:Board):
        """
        Renvoie le nombre de billes actuellement sur le plateau
        """  
        b=15-board.getMarbleCount(-1)
        w=15-board.getMarbleCount(1)
        return b+w
    
    def getcells(self, board:Board):
        return board.cells
    
    def get_marbles(self, board:Player, player:Player):
        """
        Gets the position of all the marbles of the player
        """        
        result=[]
        plateau=self.getcells(board)
        for level in range(3):
            for i in range(len(plateau[level])):
                for j in range(len(plateau[level][i])):
                    if plateau[level][i][j] == player:
                        result.append((level,i, j)) 
        return result       
    
    def centered_or_not(self, board:Board,player:Player):
        """
        Renvoie la proportion de billes du joueur qui ne sont pas à une extrémité du plateau
        """
        compte=0
        pos=self.get_marbles(board, player)
        for elt in pos:
            lvl,y,x=elt
            n=3-lvl
            if (y!=0 and y!=n) and (x!=0 and x!=n):
                compte+=1
        return compte/len(pos)
        
    def possiblesquares_nextmove(self, level:int, board:Board):
        """Dit si on est à un coup de compléter des carrés"""
        plateau_level=self.getcells(board)[level]
        nb=len(plateau_level) - 1
        countplus=0
        countmoins=0
        
        for y in range(nb):
            for x in range(nb):
                carre=[plateau_level[y][x] , plateau_level[y+1][x] , plateau_level[y][x+1] , plateau_level[y+1][x+1]]
                if carre.count(self.player)==3 and carre.count(0)==1:
                    """
                    situation :
                      x
                    y + +
                      0 +
                      
                    ie 3 billes du même joueur et un zero
                    """
                    countplus+=1
                elif carre.count(-self.player) == 3 and carre.count(0)==1:
                    countmoins+=1
                  
        # Si c'est possible de compléter en un seul coup pour l'autre joueur, c'est plus grave que le bénéfice de pouvoir le faire pour le joueur
        # actuel, vu qu'il pourra jouer que dans deux tours une fois l'heuristique appliquéee (si j'ai bien compris)   
        
        """
        Si countplus >= 2, l heuristique doit donner un résultat très haut puisqu'on est presque
        sûr de pouvoir compléter un carré quand ce sera à nouveau à notre tour de jouer
        
        De même en négatif pour countmoins
        """    
                        
        return (countplus,countmoins)
                       
    def possiblemove(self, level:int, player:Player, board:Board):
        """Dit si on peut bouger une bille, et donc ne pas en prendre une du stock

        Pour ça, il faut une bille sans rien au dessus d'elle et une case libre sur un étage supérieur
        Mais il faut aussi faire attention à ce que la bille 'bougeable' ne casse pas le support de la place libre du dessus
        
        Pour ca, on commence avec une liste candidate et on élimine celles qui cassent le support de toutes les places en haut dispos"""
        
        places_haut=self.places_en_haut(level, board)
        candidate_move=list()
        final={}
        
        for level in range(3):
            candidate_move+=self.getfree(player, level, board) #Les billes qui ne servent pas de support, ie les bougeables
            
        for candidate in candidate_move:
            for dessus in places_haut:
                #On va regarder si candidate se trouve dans support d'un elt de places_haut
                if candidate not in dessus[3]: #candidate n'est pas support de dessus
                    if candidate not in final:
                        final[candidate]=[dessus[:3]]
                    else:
                        a=final[candidate]
                        final.update({candidate:a+[dessus[:3]]})
                        
        #On a donc un dictionnaire qui a comme clés les coordonées des billes bougeables, et en valeur 
        #les coordonnées de là où on peut les bougers
        #Ainsi, si final est vide, on sait qu'on ne peut rien bouger
                 
        #Les fonctions places_en_haut et  getfree peuvent être combinées pour pas faire 2 boucles mais une seule et gagner en rapidité
        
        #Au lieu d'appeler cette fonction pour chaque joueur, on pourrait aussi prendre toutes les cases bougeables et faire un tri ensuite selon la valeur de ces cases (+ rapide)
                 
        return final
            
    def places_en_haut(self, level:int, board:Board):
        """Donne les coordonnées des places libres à l'étage level+1
        et donne aussi la liste des coordonnées de ses 'supports'
        Renvoie une liste dont les éléments sont (level, y, x, supports)"""
        
        plateau=self.getcells(board)
        result=list()
        

        n=len(plateau[level])
        for y in range(n-1):
            for x in range(n-1):
                support=[ [level, y, x] , [level, y+1, x] , [level, y, x+1] , [level, y+1, x+1] ] #Les coordonées des 4 billes qui composent le carré
                support_composantes=[plateau[level][y][x] , plateau[level][y+1][x] , plateau[level][y][x+1] , plateau[level][y+1][x+1]]   
                if 0 not in support_composantes and plateau[level+1][y][x]==0:
                    #Toutes les places du carré sont remplies et celle au dessus est libre
                    result.append([level+1, y, x, support])
                    
        return result
    
    def donne_tout(self, player:Player, level:int, board:Board):
        """
        Le but est de réunir les fonctions possible_squares_next_move et possiblemove (et donc getfree et places_en_haut)
        en une seule fonction pour limiter les boucles et donc réduire le temps d'éxécution
        
        Output : [possiblesquares_nextmove(), possiblemove(), nbcarres]
        """
        
        #Déclaration des variables nécessaires
        getfree_plateau_level_courant=self.getcells(board)[level]
        getfree_plateau_level_dessus=self.getcells(board)[level+1]
        getfree_nb=len(getfree_plateau_level_courant)
        getfree_candidats_moi=list()
        getfree_candidats_adv=list()      
        
        nb=len(getfree_plateau_level_courant)  
        
        places_en_haut_plateau=self.getcells(board)
        places_en_haut_result=list()        
        
        possiblesquares_nextmove_plateau_level=self.getcells(board)[level]
        possiblesquares_nextmove_countplus=0
        possiblesquares_nextmove_countmoins=0        
        
        nbcarres=0

        #Début partie indispensable à getfree
        for y in range(getfree_nb):
            for x in range(getfree_nb):
                if getfree_plateau_level_courant[y][x]==player:
                    getfree_candidats_moi.append((level,y,x)) #On ne garde que les coordonnées des cases remplies
                if getfree_plateau_level_courant[y][x]==-player:
                    getfree_candidats_adv.append((level,y,x)) #On ne garde que les coordonnées des cases remplies        
        #Fin partie indispensable à getfree
        
        
        #On s'attaque maintenant à la seule double boucle nécessaire. 
        #Elle parcourt range('nombre de billes par côté au niveau level' - 1)        
        for y in range(nb-1):
            for x in range(nb-1):
                
            #Début partie getfree
                #On va voir les emplacements du niveau au dessus
                if getfree_plateau_level_dessus[y][x]!=0: #L'emplacement est occupé
                    #On supprime les 4 billes support de la liste candidats
                    a_supprimer=[(level,y,x),(level,y,x+1),(level,y+1,x),level,(y+1,x+1)]
                    for elt in a_supprimer:
                        if elt in getfree_candidats_moi:
                            getfree_candidats_moi.remove(elt)
                        elif elt in getfree_candidats_adv:
                            getfree_candidats_adv.remove(elt)      
                # A return : (getfree_candidats_moi, getfree_candidats_adv)
            #Fin partie getfree
            
            #Début partie places_en_haut
                places_en_haut_support=[ (level, y, x) , (level, y+1, x) , (level, y, x+1) , (level, y+1, x+1) ] #Les coordonées des 4 billes qui composent le carré
                places_en_haut_support_composantes=[places_en_haut_plateau[level][y][x] , places_en_haut_plateau[level][y+1][x] , places_en_haut_plateau[level][y][x+1] , places_en_haut_plateau[level][y+1][x+1]]   
                if 0 not in places_en_haut_support_composantes and places_en_haut_plateau[level+1][y][x]==0:
                    #Toutes les places du carré sont remplies et celle au dessus est libre
                    places_en_haut_result.append([level+1, y, x, places_en_haut_support])  
                    
                    """
                    Le problème ici est que comme on fonctionne level par level,
                    on ne couvre pas la situation où une bille du niveau 0 peut être
                    bougée au niveau 2.
                    On traite donc ce cas à part
                    (on comprend bien ce que je fais si on dessine la situation)
                    """
                    if level==0 and x!=2 and y!=2:
                        apartee_places_en_haut_support=[ [1, y, x] , [1, y+1, x] , [1, y, x+1] , [1, y+1, x+1] ]
                        apartee_places_en_haut_support_composantes=[places_en_haut_plateau[1][y][x] , places_en_haut_plateau[1][y+1][x] , places_en_haut_plateau[1][y][x+1] , places_en_haut_plateau[1][y+1][x+1]]
                        if 0 not in apartee_places_en_haut_support_composantes and places_en_haut_plateau[2][y][x]==0:
                            places_en_haut_result.append([2, y, x, apartee_places_en_haut_support])  
                # A return : places_en_haut_result    
            #Fin partie places_en_haut    
            
            #Début partie possiblesquares_nextmove
                possiblesquares_nextmove_carre=[possiblesquares_nextmove_plateau_level[y][x] , possiblesquares_nextmove_plateau_level[y+1][x] , possiblesquares_nextmove_plateau_level[y][x+1] , possiblesquares_nextmove_plateau_level[y+1][x+1]]
                if possiblesquares_nextmove_carre.count(self.player)==3 and possiblesquares_nextmove_carre.count(0)==1:
                    """
                    situation :
                      x
                    y + +
                      0 +
                      
                    ie 3 billes du même joueur et un zero
                    """
                    possiblesquares_nextmove_countplus+=1
                elif possiblesquares_nextmove_carre.count(-self.player) == 3 and possiblesquares_nextmove_carre.count(0)==1:
                    possiblesquares_nextmove_countmoins+=1            
                # A return : (possiblesquares_nextmove_countplus, possiblesquares_nextmove_countmoins)
            #Fin partie possiblesquares_nextmove
                    
            #Je rajoute une partie pour compter le nombre de 3/4 sans tenir compte du propriétaire des 3     
                if possiblesquares_nextmove_carre.count(0)==1:
                    """
                    situation :
                      x
                    y i i
                      0 i
                      
                    où i != 0
                    
                    ie à un coup de compléter un carré (et donc de créer une place en haut)
                    """                    
                    nbcarres+=1
                           

    #Début partie possiblemove
        possiblemove_places_haut=places_en_haut_result
        possiblemove_candidate_move_moi=getfree_candidats_moi
        possiblemove_candidate_move_adv=getfree_candidats_adv
        possiblemove_final_moi={}
        possiblemove_final_adv={}

        for possiblemove_candidate_moi in possiblemove_candidate_move_moi:
            for possiblemove_dessus in possiblemove_places_haut:
                #On va regarder si candidate se trouve dans support d'un elt de places_haut
                if possiblemove_candidate_moi not in possiblemove_dessus[3]: #candidate n'est pas support de dessus
                    if possiblemove_candidate_moi not in possiblemove_final_moi:
                        possiblemove_final_moi[possiblemove_candidate_moi]=[possiblemove_dessus[:3]]
                    else:
                        a_moi=possiblemove_final_moi[possiblemove_candidate_moi]
                        possiblemove_final_moi.update({possiblemove_candidate_moi:a_moi+[possiblemove_dessus[:3]]})        
        
        for possiblemove_candidate_adv in possiblemove_candidate_move_adv:
            for possiblemove_dessus in possiblemove_places_haut:
                #On va regarder si candidate se trouve dans support d'un elt de places_haut
                if possiblemove_candidate_adv not in possiblemove_dessus[3]: #candidate n'est pas support de dessus
                    if possiblemove_candidate_adv not in possiblemove_final_adv:
                        possiblemove_final_adv[possiblemove_candidate_adv]=[possiblemove_dessus[:3]]
                    else:
                        a_adv=possiblemove_final_adv[possiblemove_candidate_adv]
                        possiblemove_final_adv.update({possiblemove_candidate_adv:a_adv+[possiblemove_dessus[:3]]})
        #A return : (possiblemove_final_moi, possiblemove_final_adv)
    #Fin partie possiblemove        
        
        return [(possiblesquares_nextmove_countplus, possiblesquares_nextmove_countmoins), (possiblemove_final_moi, possiblemove_final_adv), nbcarres]    
    
    def getfree(self, player:Player, level:int, board:Board):
        """
        Donne les coordonnées des billes du niveau level qui ne servent pas de support à une au dessus
        Output : ([coordonnées des billes libres du joueur actuel], [coordonnées des billes libres de l'adversaire du joueur actuel])
        """
        plateau_level_courant=self.getcells(board)[level]
        plateau_level_dessus=self.getcells(board)[level+1]
        
        nb=len(plateau_level_courant)
        candidats_moi=list()
        candidats_adv=list()
        for y in range(nb):
            for x in range(nb):
                if plateau_level_courant[y][x]==player:
                    candidats_moi.append((y,x)) #On ne garde que les coordonnées des cases remplies
                if plateau_level_courant[y][x]==-player:
                    candidats_adv.append((y,x)) #On ne garde que les coordonnées des cases remplies
        
        for y in range(nb-1):
            for x in range(nb-1):
                #On va voir les emplacements du niveau au dessus
                if plateau_level_dessus[y][x]!=0: #L'emplacement est occupé
                    #On supprime les 4 billes support de la liste candidats
                    a_supprimer=[(y,x),(y,x+1),(y+1,x),(y+1,x+1)]
                    for elt in a_supprimer:
                        if elt in candidats_moi:
                            candidats_moi.remove(elt)
                        elif elt in candidats_adv:
                            candidats_adv.remove(elt)
                        
        #A ce stade, on a supprimé les coordonnées de toutes les billes qui servent de support.
        #On peut donc renvoyer candidats, qui ne contient plus que les coordonnées des billes 'libres'
        
        return (candidats_moi, candidats_adv)

    def sortmoves(self, actionlist: List[Action]) -> List[Action]:
        """Sort the moves"""
        #As you noticed during the class, alpha beta performances depend on the order of the actions
        #if you feel it, you can sort the action list
        #by default, it is not

        sorted=[]
        new=[]
        move=[]
        square=[]
        for elt in actionlist:
            if elt.__class__== NewMarble:
                new.append(elt)
            elif elt.__class__== MoveMarble:
                move.append(elt)
            elif elt.__class__== MakeSquare:
                square.append(elt)
        return square+move+new

    def alphabeta(self, board:Board) -> Action:
        """Decision made by alpha beta, returns the best action"""
        possiblemoves = self.sortmoves(Player.getPossibleMoves(self.player, board))
        if len(possiblemoves)==0:
            raise Exception("cannot have 0 possible play")
        elif len(possiblemoves)==1:
            return possiblemoves[0]
        else:
            best_score = -inf
            beta = inf
            coup = None
            for action in possiblemoves:
                action.apply(self.player, board)
                v = self.__minvalue(board, best_score, beta, 1)
                action.unapply(self.player, board)
                if v>best_score:
                    best_score = v
                    coup = action

            if coup == None:
                #we are going towards a defeat whatever the coup
                coup = possiblemoves[0]
            return coup


    def __maxvalue(self, board:Board, alpha:float, beta:float, depth:int) -> float:
        """For max nodes"""
        #terminal test
        if depth >= self.__maxdepth or board.isTerminal():
            return self.heuristic(board)
            
        v = -inf
        for action in Player.getPossibleMoves(self.player, board):            
            action.apply(self.player, board)
            v = max(v,self.__minvalue(board, alpha, beta, depth+1))
            action.unapply(self.player, board)
            if v>=beta:
                return v
            alpha = max(alpha,v)
        return v


    def __minvalue(self, board:Board, alpha:float, beta:float, depth:int) -> float:
        """For min nodes"""
        #terminal test
        if depth >= self.__maxdepth or board.isTerminal():
            return self.heuristic(board)
            
        v = inf
        for action in Player.getPossibleMoves(-self.player,board):
            action.apply(-self.player, board)
            #print('autre : ', self.__maxvalue(board, alpha, beta, depth+1), type(self.__maxvalue(board, alpha, beta, depth+1)))
            #print('autre : ', self.__maxvalue(board, alpha, beta, depth+1))
            v = min(v,float(self.__maxvalue(board, alpha, beta, depth+1)))
            action.unapply(-self.player, board)
            if v<=alpha:
                return v
            beta = min(beta,v)
        return v
    
    
# -*- coding: utf-8 -*-

from cmath import inf
from typing import List
from players import Player
from actions import *
from board import Board
from math import inf
import copy

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

stest='board.getMarbleCount(self.player) + 0.8*acte_moi + 0.48*contraint_moi + 1.2*move_pour_moi_destination_diff - board.getMarbleCount(-self.player) - 2.4*acte_adv - 0.1*contraint_adv - 1.2*move_pour_adv_destination_diff'


s70='board.getMarbleCount(self.player) + 2.2*carresuivant_pour_moi_utile + 0.65*move_pour_moi_utile - board.getMarbleCount(-self.player) - 2.2*carresuivant_pour_adv_utile - 0.65*move_pour_adv_utile'
s80='board.getMarbleCount(self.player) + 2*carresuivant_pour_moi_utile + 0.5*move_pour_moi_utile - board.getMarbleCount(-self.player) - 2*carresuivant_pour_adv_utile - 0.5*move_pour_adv_utile'




class AIPlayer_test(Player):
    """Artificial Intelligence based player"""
    def __init__(self, strat, depth):
        super().__init__("le test") #A CHANGER EN METTANT SON NOM
        self.__maxdepth = depth #mettez ici la profondeur max de votre alpha beta en n'oubliant que vous devez répondre en 10s)
        self.strat=strat

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
            tout est [ [possiblesquares(level=0), possiblemove(level=0)],
                       [possiblesquares(level=1), possiblemove(level=1)],
                       [possiblesquares(level=2), possiblemove(level=2)],
                     ]
            """
 
            carresuivant_pour_adv=0
            carresuivant_pour_moi=0
            for k in range(3):
                carresuivant_pour_moi+=tout[k][0][0]
                carresuivant_pour_adv+=tout[k][0][1]
                
            moves_moi=[tout[k][1][0] for k in range(3)]
            moves_adv=[tout[k][1][1] for k in range(3)]
                

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
            
            for moves_moi_level in moves_moi: #on enumere les dicos
                for bougeable in moves_moi_level:
                    for elt in moves_moi_level[bougeable]: #les destinations
                        if elt not in deja_vus_moi:
                            move_pour_moi_destination_diff+=1
                            deja_vus_moi.append(elt)
                        
            #On peut aussi simplement compter le nombre de moves possibles :
            nb_moves_possibles_moi=0
            for elt in moves_moi:
                nb_moves_possibles_moi+=len(elt)



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
            
            

            resultat=eval(stest)
            
            return resultat
 
    
    
    def show_heuristic(self, board:Board) -> float: #Là on peut toucher
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
            tout est [ [possiblesquares(level=0), possiblemove(level=0)],
                       [possiblesquares(level=1), possiblemove(level=1)],
                       [possiblesquares(level=2), possiblemove(level=2)],
                     ]
            """
 
            carresuivant_pour_adv=0
            carresuivant_pour_moi=0
            for k in range(3):
                carresuivant_pour_moi+=tout[k][0][0]
                carresuivant_pour_adv+=tout[k][0][1]
                
            moves_moi=[tout[k][1][0] for k in range(3)]
            moves_adv=[tout[k][1][1] for k in range(3)]
                

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
                        
            #On peut aussi simplement compter le nombre de moves possibles :
            nb_moves_possibles_moi=0
            for elt in moves_moi:
                nb_moves_possibles_moi+=len(elt)



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
            
        
            return [(carresuivant_pour_moi, moves_moi), (carresuivant_pour_adv, moves_adv)]
    
    
    
    
    
    def getcells(self, board:Board):
        return board.cells
    
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
        
        Output : [possiblesquares_nextmove(), possiblemove()]
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
        
        return [(possiblesquares_nextmove_countplus, possiblesquares_nextmove_countmoins), (possiblemove_final_moi, possiblemove_final_adv)]    
        

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
        return actionlist

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
    
    







class AIPlayer1(Player):
    """Artificial Intelligence based player"""
    def __init__(self):
        super().__init__("le méchant 1") #A CHANGER EN METTANT SON NOM
        self.__maxdepth = 1 #mettez ici la profondeur max de votre alpha beta en n'oubliant que vous devez répondre en 10s)

    def getNextMove(self, board: Board) -> Action: #Pas toucher
        """Gets the next move to play"""
        return self.alphabeta(board)





    def show_heuristic(self, board:Board) -> float: #Là on peut toucher
        """Heuristic for alpha-beta, to be modified by the students"""
        if board.getTop() == self.player or board.getMarbleCount(-self.player) == 0:
            return inf
        elif board.getTop() == -self.player or board.getMarbleCount(self.player) == 0:
            return -inf
        else:
            #Calculer ici votre heuristique
            #Une valeur positive et grande indique que le plateau est favorable à votre IA
            #Une valeur très négative indique que le plateau est défavorable à votre IA
            
            
            carresuivant_pour_adv=0
            for level in range(3):
                carresuivant_pour_adv+=self.possiblesquares_nextmove(level, board)[1]
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
            
            
            carresuivant_pour_moi=0
            for level in range(3):
                carresuivant_pour_moi+=self.possiblesquares_nextmove(level, board)[0]
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
            
            
            
            moves_moi=self.possiblemove(self.player, board) #Dictionnaire {[coordonnées bille bougeable] : [[coordonnées où la bouger]]}
            #Ce qui est important ici, c'est qu'il y ait au moins 2 endroits où bouger puisque s'il y en a qu'un, le spot va être pris par l'adversaire
            
            #On compte donc le nombre de destinations possibles
            move_pour_moi_destination_diff=0
            deja_vus_moi=[]
            for bougeable in moves_moi:
                for elt in moves_moi[bougeable]:
                    if elt not in deja_vus_moi:
                        move_pour_moi_destination_diff+=1
                        deja_vus_moi.append(elt)
                        
            move_pour_moi_utile=move_pour_moi_destination_diff



            moves_adv=self.possiblemove(-self.player, board) #Dictionnaire {[coordonnées bille bougeable] : [[coordonnées où la bouger]]}
            #Ce qui est important ici, c'est qu'il y ait au moins 2 endroits où bouger puisque s'il y en a qu'un, le spot va être pris par l'adversaire
            
            #On compte donc le nombre de destinations possibles
            move_pour_adv_destination_diff=0
            deja_vus_adv=[]
            for bougeable in moves_adv:
                for elt in moves_adv[bougeable]:
                    if elt not in deja_vus_adv:
                        move_pour_adv_destination_diff+=1
                        deja_vus_adv.append(elt)
                        
            move_pour_adv_utile=move_pour_adv_destination_diff
            #On peut introduire une pénalité de contrainte mais plus complexe à mettre en place --> à voir
            
            
            
            
            return [(carresuivant_pour_moi, moves_moi), (carresuivant_pour_adv, moves_adv)]
 









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
            
            
            carresuivant_pour_adv=0
            for level in range(3):
                carresuivant_pour_adv+=self.possiblesquares_nextmove(level, board)[1]
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
            
            
            carresuivant_pour_moi=0
            for level in range(3):
                carresuivant_pour_moi+=self.possiblesquares_nextmove(level, board)[0]
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
            
            
            
            moves_moi=self.possiblemove(self.player, board) #Dictionnaire {[coordonnées bille bougeable] : [[coordonnées où la bouger]]}
            #Ce qui est important ici, c'est qu'il y ait au moins 2 endroits où bouger puisque s'il y en a qu'un, le spot va être pris par l'adversaire
            
            #On compte donc le nombre de destinations possibles
            move_pour_moi_destination_diff=0
            deja_vus_moi=[]
            for bougeable in moves_moi:
                for elt in moves_moi[bougeable]:
                    if elt not in deja_vus_moi:
                        move_pour_moi_destination_diff+=1
                        deja_vus_moi.append(elt)
                        
            move_pour_moi_utile=move_pour_moi_destination_diff



            moves_adv=self.possiblemove(-self.player, board) #Dictionnaire {[coordonnées bille bougeable] : [[coordonnées où la bouger]]}
            #Ce qui est important ici, c'est qu'il y ait au moins 2 endroits où bouger puisque s'il y en a qu'un, le spot va être pris par l'adversaire
            
            #On compte donc le nombre de destinations possibles
            move_pour_adv_destination_diff=0
            deja_vus_adv=[]
            for bougeable in moves_adv:
                for elt in moves_adv[bougeable]:
                    if elt not in deja_vus_adv:
                        move_pour_adv_destination_diff+=1
                        deja_vus_adv.append(elt)
                        
            move_pour_adv_utile=move_pour_adv_destination_diff
            #On peut introduire une pénalité de contrainte mais plus complexe à mettre en place --> à voir
            
            
            #s='s'+str(self.number)

            resultat=eval(stest)
            
            return resultat
 
    
    def getcells(self, board:Board):
        return board.cells
    
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
                       
                       
                       
    def possiblemove(self, player:Player, board:Board):
        """Dit si on peut bouger une bille, et donc ne pas en prendre une du stock

        Pour ça, il faut une bille sans rien au dessus d'elle et une case libre sur un étage supérieur
        Mais il faut aussi faire attention à ce que la bille 'bougeable' ne casse pas le support de la place libre du dessus
        
        Pour ca, on commence avce une liste candidate et on élimine celles qui cassent le support de toutes les places en haut dispos"""
        
        places_haut=self.places_en_haut(board) #liste de tuples
        candidate_move=list()
        final={}
        
        for level in range(3):
            candidate_move+=self.getfree(player, level, board)
            
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
        
    def places_en_haut(self, board:Board):
        """Donne les coordonnées des places libres sur les étages autre que le zero
        et donne aussi la liste des coordonnées de ses 'supports'
        Renvoie une liste dont les éléments sont (level, y, x, supports)"""
        
        plateau=self.getcells(board)
        result=list()
        
        for level in range(3):
            n=len(plateau[level]) - 1
            for y in range(n):
                for x in range(n):
                    support=[ (level, y, x) , (level, y+1, x) , (level, y, x+1) , (level, y+1, x+1) ] #Les coordonées des 4 billes qui composent le carré
                    support_composantes=[plateau[level][y][x] , plateau[level][y+1][x] , plateau[level][y][x+1] , plateau[level][y+1][x+1]]   
                    if 0 not in support_composantes and plateau[level+1][y][x]==0:
                        #Toutes les places du carré sont remplies et celle au dessus est libre
                        result.append([level+1, y, x, support])
                    
        return result
    
    def isok(self,a,n):
        """Dit si a est dans [0,n]"""
        b = a<=n and 0<=a
        return b

    def test_eligible(self,x,y,n):
        l=list()
        if self.isok(x-1, n) and self.isok(y-1, n):
            l.append((y-1, x-1))
        elif self.isok(x-1, n) and self.isok(y, n):
            l.append((y, x-1))    
        elif self.isok(x, n) and self.isok(y-1, n):
            l.append((y-1, x))        
        elif self.isok(x, n) and self.isok(y, n):
            l.append((y, x))    
        return l

    def getfree(self, player:Player, level:int, board:Board):
        """Donne les coordonnées des billes du niveau level qui ne servent pas de support à une au dessus et qui appartiennent au joueur actuel"""
        plateau_level_courant=self.getcells(board)[level]
        plateau_level_dessus=self.getcells(board)[level+1]
        
        nb=len(plateau_level_courant)
        candidats=list()
        for y in range(nb):
            for x in range(nb):
                if plateau_level_courant[y][x]==player:
                    candidats.append((level,y,x)) #On ne garde que les coordonnées des cases remplies
        
        for y in range(nb-1):
            for x in range(nb-1):
                #On va voir les emplacements du niveau au dessus
                if plateau_level_dessus[y][x]!=0: #L'emplacement est occupé
                    #On supprime les 4 billes support de la liste candidats
                    a_supprimer=[(level,y,x),(level,y,x+1),(level,y+1,x),(level,y+1,x+1)]
                    for elt in a_supprimer:
                        if elt in candidats:
                            candidats.remove(elt)
                        
        #A ce stade, on a supprimé les coordonnées de toutes les billes qui servent de support.
        #On peut donc renvoyer candidats, qui ne contient plus que les coordonnées des billes 'libres'
        
        return candidats

    def sortmoves(self, actionlist: List[Action]) -> List[Action]:
        """Sort the moves"""
        #As you noticed during the class, alpha beta performances depend on the order of the actions
        #if you feel it, you can sort the action list
        #by default, it is not
        return actionlist

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
    
    
    
    
class AIPlayer2(Player):
    """Artificial Intelligence based player"""
    def __init__(self):
        super().__init__("le méchant 2") #A CHANGER EN METTANT SON NOM
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
            
            
            carresuivant_pour_adv=0
            for level in range(3):
                carresuivant_pour_adv+=self.possiblesquares_nextmove(level, board)[1]
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
            
            
            carresuivant_pour_moi=0
            for level in range(3):
                carresuivant_pour_moi+=self.possiblesquares_nextmove(level, board)[0]
            #Donne le nombre de situations pour moi où je suis capable de compléter un carré en un coup
            #S'il y en a un, l'adversaire le contre mais on le contraint l'adversaire
            #S'il y en a deux, on en joue un mais l'autre est bloqué au prochain tour --> contraint l'adversaire
            #S'il y en a trois, on en joue un, deux sont bloqués --> on contraint l'adversaire
            #On accorde 0,2 au fait de contraindre l'adversaire (mais on multiplie par 2 dans le return)
            #donc ce qui nous intéresse c'est le nombre de carrés que je pourrai compléter sûrement : carresuivant_pour_moi//2
            #et auss ile nombre de coups que je contrains mon adversaire à faire : (carresuivant_pour_moi+1)//2
            contraint_moi=0 #Contraint l'adv
            acte_moi=0
            if carresuivant_pour_moi!=0:
                contraint_moi=(carresuivant_pour_moi+1)//2
            if carresuivant_pour_moi>=2:
                acte_moi=carresuivant_pour_moi//2
            carresuivant_pour_moi_utile = acte_moi + 0.1*contraint_moi
            
            
            
            moves_moi=self.possiblemove(self.player, board) #Dictionnaire {[coordonnées bille bougeable] : [[coordonnées où la bouger]]}
            #Ce qui est important ici, c'est qu'il y ait au moins 2 endroits où bouger puisque s'il y en a qu'un, le spot va être pris par l'adversaire
            
            #On compte donc le nombre de destinations possibles
            move_pour_moi_destination_diff=0
            deja_vus_moi=[]
            for bougeable in moves_moi:
                for elt in moves_moi[bougeable]:
                    if elt not in deja_vus_moi:
                        move_pour_moi_destination_diff+=1
                        deja_vus_moi.append(elt)
                        
            move_pour_moi_utile=move_pour_moi_destination_diff



            moves_adv=self.possiblemove(-self.player, board) #Dictionnaire {[coordonnées bille bougeable] : [[coordonnées où la bouger]]}
            #Ce qui est important ici, c'est qu'il y ait au moins 2 endroits où bouger puisque s'il y en a qu'un, le spot va être pris par l'adversaire
            
            #On compte donc le nombre de destinations possibles
            move_pour_adv_destination_diff=0
            deja_vus_adv=[]
            for bougeable in moves_adv:
                for elt in moves_adv[bougeable]:
                    if elt not in deja_vus_adv:
                        move_pour_adv_destination_diff+=1
                        deja_vus_adv.append(elt)
                        
            move_pour_adv_utile=move_pour_adv_destination_diff
            #On peut introduire une pénalité de contrainte mais plus complexe à mettre en place --> à voir
            
            
            #s='s'+str(self.number)

            resultat=eval(eval(sp2))
            
            return resultat
 
    
    def getcells(self, board:Board):
        return board.cells
    
    def possiblesquares_nextmove(self, level:int, board:Board):
        """Dit si on est à un coup de compléter des carrés"""
        plateau_level=AIPlayer2().getcells(board)[level]
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
                       
    def possiblemove(self, player:Player, board:Board):
        """Dit si on peut bouger une bille, et donc ne pas en prendre une du stock

        Pour ça, il faut une bille sans rien au dessus d'elle et une case libre sur un étage supérieur
        Mais il faut aussi faire attention à ce que la bille 'bougeable' ne casse pas le support de la place libre du dessus
        
        Pour ca, on commence avce une liste candidate et on élimine celles qui cassent le support de toutes les places en haut dispos"""
        
        places_haut=self.places_en_haut(board)
        candidate_move=list()
        final={}
        
        for level in range(3):
            candidate_move+=self.getfree(player, level, board)
            
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
        
    def places_en_haut(self, board:Board):
        """Donne les coordonnées des places libres sur les étages autre que le zero
        et donne aussi la liste des coordonnées de ses 'supports'
        Renvoie une liste dont les éléments sont (level, y, x, supports)"""
        
        plateau=AIPlayer2().getcells(board)
        result=list()
        
        for level in range(3):
            n=len(plateau[level]) - 1
            for y in range(n):
                for x in range(n):
                    support=[ [level, y, x] , [level, y+1, x] , [level, y, x+1] , [level, y+1, x+1] ] #Les coordonées des 4 billes qui composent le carré
                    support_composantes=[plateau[level][y][x] , plateau[level][y+1][x] , plateau[level][y][x+1] , plateau[level][y+1][x+1]]   
                    if 0 not in support_composantes and plateau[level+1][y][x]==0:
                        #Toutes les places du carré sont remplies et celle au dessus est libre
                        result.append([level+1, y, x, support])
                    
        return result
    
    def isok(self,a,n):
        """Dit si a est dans [0,n]"""
        b = a<=n and 0<=a
        return b

    def test_eligible(self,x,y,n):
        l=list()
        if self.isok(x-1, n) and self.isok(y-1, n):
            l.append((y-1, x-1))
        elif self.isok(x-1, n) and self.isok(y, n):
            l.append((y, x-1))    
        elif self.isok(x, n) and self.isok(y-1, n):
            l.append((y-1, x))        
        elif self.isok(x, n) and self.isok(y, n):
            l.append((y, x))    
        return l

    def getfree(self, player:Player, level:int, board:Board):
        """Donne les coordonnées des billes du niveau level qui ne servent pas de support à une au dessus et qui appartiennent au joueur actuel"""
        plateau_level_courant=AIPlayer2().getcells(board)[level]
        plateau_level_dessus=AIPlayer2().getcells(board)[level+1]
        
        nb=len(plateau_level_courant)
        candidats=list()
        for y in range(nb):
            for x in range(nb):
                if plateau_level_courant[y][x]==player:
                    candidats.append((y,x)) #On ne garde que les coordonnées des cases remplies
        
        for y in range(nb-1):
            for x in range(nb-1):
                #On va voir les emplacements du niveau au dessus
                if plateau_level_dessus[y][x]!=0: #L'emplacement est occupé
                    #On supprime les 4 billes support de la liste candidats
                    a_supprimer=[(y,x),(y,x+1),(y+1,x),(y+1,x+1)]
                    for elt in a_supprimer:
                        if elt in candidats:
                            candidats.remove(elt)
                        
        #A ce stade, on a supprimé les coordonnées de toutes les billes qui servent de support.
        #On peut donc renvoyer candidats, qui ne contient plus que les coordonnées des billes 'libres'
        
        return candidats

    def sortmoves(self, actionlist: List[Action]) -> List[Action]:
        """Sort the moves"""
        #As you noticed during the class, alpha beta performances depend on the order of the actions
        #if you feel it, you can sort the action list
        #by default, it is not
        return actionlist

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
    
 
 
class AIPlayer_force_1(Player):
    """Artificial Intelligence based player"""
    def __init__(self, strat):
        super().__init__("le méchant 1") #A CHANGER EN METTANT SON NOM
        self.__maxdepth = 4 #mettez ici la profondeur max de votre alpha beta en n'oubliant que vous devez répondre en 10s)
        self.strat=strat

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
            
            
            carresuivant_pour_adv=0
            for level in range(3):
                carresuivant_pour_adv+=self.possiblesquares_nextmove(level, board)[1]
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
            
            
            carresuivant_pour_moi=0
            for level in range(3):
                carresuivant_pour_moi+=self.possiblesquares_nextmove(level, board)[0]
            #Donne le nombre de situations pour moi où je suis capable de compléter un carré en un coup
            #S'il y en a un, l'adversaire le contre mais on le contraint l'adversaire
            #S'il y en a deux, on en joue un mais l'autre est bloqué au prochain tour --> contraint l'adversaire
            #S'il y en a trois, on en joue un, deux sont bloqués --> on contraint l'adversaire
            #On accorde 0,2 au fait de contraindre l'adversaire (mais on multiplie par 2 dans le return)
            #donc ce qui nous intéresse c'est le nombre de carrés que je pourrai compléter sûrement : carresuivant_pour_moi//2
            #et auss ile nombre de coups que je contrains mon adversaire à faire : (carresuivant_pour_moi+1)//2
            contraint_moi=0 #Contraint l'adv
            acte_moi=0
            if carresuivant_pour_moi!=0:
                contraint_moi=(carresuivant_pour_moi+1)//2
            if carresuivant_pour_moi>=2:
                acte_moi=carresuivant_pour_moi//2
            carresuivant_pour_moi_utile = acte_moi + 0.1*contraint_moi
            
            
            
            moves_moi=self.possiblemove(self.player, board) #Dictionnaire {[coordonnées bille bougeable] : [[coordonnées où la bouger]]}
            #Ce qui est important ici, c'est qu'il y ait au moins 2 endroits où bouger puisque s'il y en a qu'un, le spot va être pris par l'adversaire
            
            #On compte donc le nombre de destinations possibles
            move_pour_moi_destination_diff=0
            deja_vus_moi=[]
            for bougeable in moves_moi:
                for elt in moves_moi[bougeable]:
                    if elt not in deja_vus_moi:
                        move_pour_moi_destination_diff+=1
                        deja_vus_moi.append(elt)
                        
            move_pour_moi_utile=move_pour_moi_destination_diff



            moves_adv=self.possiblemove(-self.player, board) #Dictionnaire {[coordonnées bille bougeable] : [[coordonnées où la bouger]]}
            #Ce qui est important ici, c'est qu'il y ait au moins 2 endroits où bouger puisque s'il y en a qu'un, le spot va être pris par l'adversaire
            
            #On compte donc le nombre de destinations possibles
            move_pour_adv_destination_diff=0
            deja_vus_adv=[]
            for bougeable in moves_adv:
                for elt in moves_adv[bougeable]:
                    if elt not in deja_vus_adv:
                        move_pour_adv_destination_diff+=1
                        deja_vus_adv.append(elt)
                        
            move_pour_adv_utile=move_pour_adv_destination_diff
            #On peut introduire une pénalité de contrainte mais plus complexe à mettre en place --> à voir
            
            
            #s='s'+str(self.number)

            resultat=eval(self.strat)
            
            return resultat
 
    
    def getcells(self, board:Board):
        return board.cells
    
    def possiblesquares_nextmove(self, level:int, board:Board):
        """Dit si on est à un coup de compléter des carrés"""
        plateau_level=AIPlayer2().getcells(board)[level]
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
                       
    def possiblemove(self, player:Player, board:Board):
        """Dit si on peut bouger une bille, et donc ne pas en prendre une du stock

        Pour ça, il faut une bille sans rien au dessus d'elle et une case libre sur un étage supérieur
        Mais il faut aussi faire attention à ce que la bille 'bougeable' ne casse pas le support de la place libre du dessus
        
        Pour ca, on commence avce une liste candidate et on élimine celles qui cassent le support de toutes les places en haut dispos"""
        
        places_haut=self.places_en_haut(board)
        candidate_move=list()
        final={}
        
        for level in range(3):
            candidate_move+=self.getfree(player, level, board)
            
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
        
    def places_en_haut(self, board:Board):
        """Donne les coordonnées des places libres sur les étages autre que le zero
        et donne aussi la liste des coordonnées de ses 'supports'
        Renvoie une liste dont les éléments sont (level, y, x, supports)"""
        
        plateau=AIPlayer2().getcells(board)
        result=list()
        
        for level in range(3):
            n=len(plateau[level]) - 1
            for y in range(n):
                for x in range(n):
                    support=[ [level, y, x] , [level, y+1, x] , [level, y, x+1] , [level, y+1, x+1] ] #Les coordonées des 4 billes qui composent le carré
                    support_composantes=[plateau[level][y][x] , plateau[level][y+1][x] , plateau[level][y][x+1] , plateau[level][y+1][x+1]]   
                    if 0 not in support_composantes and plateau[level+1][y][x]==0:
                        #Toutes les places du carré sont remplies et celle au dessus est libre
                        result.append([level+1, y, x, support])
                    
        return result
    
    def isok(self,a,n):
        """Dit si a est dans [0,n]"""
        b = a<=n and 0<=a
        return b

    def test_eligible(self,x,y,n):
        l=list()
        if self.isok(x-1, n) and self.isok(y-1, n):
            l.append((y-1, x-1))
        elif self.isok(x-1, n) and self.isok(y, n):
            l.append((y, x-1))    
        elif self.isok(x, n) and self.isok(y-1, n):
            l.append((y-1, x))        
        elif self.isok(x, n) and self.isok(y, n):
            l.append((y, x))    
        return l

    def getfree(self, player:Player, level:int, board:Board):
        """Donne les coordonnées des billes du niveau level qui ne servent pas de support à une au dessus et qui appartiennent au joueur actuel"""
        plateau_level_courant=AIPlayer2().getcells(board)[level]
        plateau_level_dessus=AIPlayer2().getcells(board)[level+1]
        
        nb=len(plateau_level_courant)
        candidats=list()
        for y in range(nb):
            for x in range(nb):
                if plateau_level_courant[y][x]==player:
                    candidats.append((y,x)) #On ne garde que les coordonnées des cases remplies
        
        for y in range(nb-1):
            for x in range(nb-1):
                #On va voir les emplacements du niveau au dessus
                if plateau_level_dessus[y][x]!=0: #L'emplacement est occupé
                    #On supprime les 4 billes support de la liste candidats
                    a_supprimer=[(y,x),(y,x+1),(y+1,x),(y+1,x+1)]
                    for elt in a_supprimer:
                        if elt in candidats:
                            candidats.remove(elt)
                        
        #A ce stade, on a supprimé les coordonnées de toutes les billes qui servent de support.
        #On peut donc renvoyer candidats, qui ne contient plus que les coordonnées des billes 'libres'
        
        return candidats

    def sortmoves(self, actionlist: List[Action]) -> List[Action]:
        """Sort the moves"""
        #As you noticed during the class, alpha beta performances depend on the order of the actions
        #if you feel it, you can sort the action list
        #by default, it is not
        return actionlist

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
    
    
    
    
class AIPlayer_force_2(Player):
    """Artificial Intelligence based player"""
    def __init__(self, strat):
        super().__init__("le méchant 2") #A CHANGER EN METTANT SON NOM
        self.__maxdepth = 4 #mettez ici la profondeur max de votre alpha beta en n'oubliant que vous devez répondre en 10s)
        self.strat=strat

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
            
            
            carresuivant_pour_adv=0
            for level in range(3):
                carresuivant_pour_adv+=self.possiblesquares_nextmove(level, board)[1]
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
            
            
            carresuivant_pour_moi=0
            for level in range(3):
                carresuivant_pour_moi+=self.possiblesquares_nextmove(level, board)[0]
            #Donne le nombre de situations pour moi où je suis capable de compléter un carré en un coup
            #S'il y en a un, l'adversaire le contre mais on le contraint l'adversaire
            #S'il y en a deux, on en joue un mais l'autre est bloqué au prochain tour --> contraint l'adversaire
            #S'il y en a trois, on en joue un, deux sont bloqués --> on contraint l'adversaire
            #On accorde 0,2 au fait de contraindre l'adversaire (mais on multiplie par 2 dans le return)
            #donc ce qui nous intéresse c'est le nombre de carrés que je pourrai compléter sûrement : carresuivant_pour_moi//2
            #et auss ile nombre de coups que je contrains mon adversaire à faire : (carresuivant_pour_moi+1)//2
            contraint_moi=0 #Contraint l'adv
            acte_moi=0
            if carresuivant_pour_moi!=0:
                contraint_moi=(carresuivant_pour_moi+1)//2
            if carresuivant_pour_moi>=2:
                acte_moi=carresuivant_pour_moi//2
            carresuivant_pour_moi_utile = acte_moi + 0.1*contraint_moi
            
            
            
            moves_moi=self.possiblemove(self.player, board) #Dictionnaire {[coordonnées bille bougeable] : [[coordonnées où la bouger]]}
            #Ce qui est important ici, c'est qu'il y ait au moins 2 endroits où bouger puisque s'il y en a qu'un, le spot va être pris par l'adversaire
            
            #On compte donc le nombre de destinations possibles
            move_pour_moi_destination_diff=0
            deja_vus_moi=[]
            for bougeable in moves_moi:
                for elt in moves_moi[bougeable]:
                    if elt not in deja_vus_moi:
                        move_pour_moi_destination_diff+=1
                        deja_vus_moi.append(elt)
                        
            move_pour_moi_utile=move_pour_moi_destination_diff



            moves_adv=self.possiblemove(-self.player, board) #Dictionnaire {[coordonnées bille bougeable] : [[coordonnées où la bouger]]}
            #Ce qui est important ici, c'est qu'il y ait au moins 2 endroits où bouger puisque s'il y en a qu'un, le spot va être pris par l'adversaire
            
            #On compte donc le nombre de destinations possibles
            move_pour_adv_destination_diff=0
            deja_vus_adv=[]
            for bougeable in moves_adv:
                for elt in moves_adv[bougeable]:
                    if elt not in deja_vus_adv:
                        move_pour_adv_destination_diff+=1
                        deja_vus_adv.append(elt)
                        
            move_pour_adv_utile=move_pour_adv_destination_diff
            #On peut introduire une pénalité de contrainte mais plus complexe à mettre en place --> à voir
            
            
            #s='s'+str(self.number)

            resultat=eval(self.strat)
            
            return resultat
 
    
    def getcells(self, board:Board):
        return board.cells
    
    def possiblesquares_nextmove(self, level:int, board:Board):
        """Dit si on est à un coup de compléter des carrés"""
        plateau_level=AIPlayer2().getcells(board)[level]
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
                       
    def possiblemove(self, player:Player, board:Board):
        """Dit si on peut bouger une bille, et donc ne pas en prendre une du stock

        Pour ça, il faut une bille sans rien au dessus d'elle et une case libre sur un étage supérieur
        Mais il faut aussi faire attention à ce que la bille 'bougeable' ne casse pas le support de la place libre du dessus
        
        Pour ca, on commence avce une liste candidate et on élimine celles qui cassent le support de toutes les places en haut dispos"""
        
        places_haut=self.places_en_haut(board)
        candidate_move=list()
        final={}
        
        for level in range(3):
            candidate_move+=self.getfree(player, level, board)
            
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
        
    def places_en_haut(self, board:Board):
        """Donne les coordonnées des places libres sur les étages autre que le zero
        et donne aussi la liste des coordonnées de ses 'supports'
        Renvoie une liste dont les éléments sont (level, y, x, supports)"""
        
        plateau=AIPlayer2().getcells(board)
        result=list()
        
        for level in range(3):
            n=len(plateau[level]) - 1
            for y in range(n):
                for x in range(n):
                    support=[ [level, y, x] , [level, y+1, x] , [level, y, x+1] , [level, y+1, x+1] ] #Les coordonées des 4 billes qui composent le carré
                    support_composantes=[plateau[level][y][x] , plateau[level][y+1][x] , plateau[level][y][x+1] , plateau[level][y+1][x+1]]   
                    if 0 not in support_composantes and plateau[level+1][y][x]==0:
                        #Toutes les places du carré sont remplies et celle au dessus est libre
                        result.append([level+1, y, x, support])
                    
        return result
    
    def isok(self,a,n):
        """Dit si a est dans [0,n]"""
        b = a<=n and 0<=a
        return b

    def test_eligible(self,x,y,n):
        l=list()
        if self.isok(x-1, n) and self.isok(y-1, n):
            l.append((y-1, x-1))
        elif self.isok(x-1, n) and self.isok(y, n):
            l.append((y, x-1))    
        elif self.isok(x, n) and self.isok(y-1, n):
            l.append((y-1, x))        
        elif self.isok(x, n) and self.isok(y, n):
            l.append((y, x))    
        return l

    def getfree(self, player:Player, level:int, board:Board):
        """Donne les coordonnées des billes du niveau level qui ne servent pas de support à une au dessus et qui appartiennent au joueur actuel"""
        plateau_level_courant=AIPlayer2().getcells(board)[level]
        plateau_level_dessus=AIPlayer2().getcells(board)[level+1]
        
        nb=len(plateau_level_courant)
        candidats=list()
        for y in range(nb):
            for x in range(nb):
                if plateau_level_courant[y][x]==player:
                    candidats.append((y,x)) #On ne garde que les coordonnées des cases remplies
        
        for y in range(nb-1):
            for x in range(nb-1):
                #On va voir les emplacements du niveau au dessus
                if plateau_level_dessus[y][x]!=0: #L'emplacement est occupé
                    #On supprime les 4 billes support de la liste candidats
                    a_supprimer=[(y,x),(y,x+1),(y+1,x),(y+1,x+1)]
                    for elt in a_supprimer:
                        if elt in candidats:
                            candidats.remove(elt)
                        
        #A ce stade, on a supprimé les coordonnées de toutes les billes qui servent de support.
        #On peut donc renvoyer candidats, qui ne contient plus que les coordonnées des billes 'libres'
        
        return candidats

    def sortmoves(self, actionlist: List[Action]) -> List[Action]:
        """Sort the moves"""
        #As you noticed during the class, alpha beta performances depend on the order of the actions
        #if you feel it, you can sort the action list
        #by default, it is not
        return actionlist

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
    
    
    
class AIPlayer_v0(Player):
    """Artificial Intelligence based player"""
    def __init__(self):
        super().__init__("le méchant") #A CHANGER EN METTANT SON NOM
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
            
            
            return board.getMarbleCount(self.player) - board.getMarbleCount(-self.player)
 
    
    def getcells(self, board:Board):
        return board.cells
    


    def sortmoves(self, actionlist: List[Action]) -> List[Action]:
        """Sort the moves"""
        #As you noticed during the class, alpha beta performances depend on the order of the actions
        #if you feel it, you can sort the action list
        #by default, it is not
        return actionlist

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
            v = min(v,self.__maxvalue(board, alpha, beta, depth+1))
            action.unapply(-self.player, board)
            if v<=alpha:
                return v
            beta = min(beta,v)
        return v
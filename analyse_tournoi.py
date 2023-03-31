import numpy as np
import sys
np.set_printoptions(threshold=sys.maxsize)
from operator import itemgetter
from analyse import acte_force_9


from_0_to_0=np.loadtxt('tournoi_acte_force_9_0_15_to_0_15.txt')
from_0_to_15=np.loadtxt('tournoi_acte_force_9_0_15_to_16_31.txt')
from_16_to_0=np.loadtxt('tournoi_acte_force_9_16_31_to_0_15.txt')
from_16_to_16=np.loadtxt('tournoi_acte_force_9_16_31_to_16_31.txt')


all=from_0_to_0+from_0_to_15+from_16_to_0+from_16_to_16

#print(all)

def trouve(arr, v):
    n=len(arr)
    m=len(arr[0])
    result=list()
    for i in range(n):
        for j in range(m):
            if arr[i,j]==v:
                result.append((i,j))
    return result

def find_best_ligne(a):
    l_s = a.sum(axis=1)
    #print(l_s)
    #print(max(l_s))
    #print(np.where(np.isclose(l_s, max(l_s)))[0])
    return np.where(np.isclose(l_s, max(l_s)))[0]

def find_best_col(a):
    l_s = a.sum(axis=0)
    #print(min(l_s))
    #print(np.where(np.isclose(l_s, min(l_s)))[0])
    return np.where(np.isclose(l_s, min(l_s)))[0]

def montresomme(a):
    somcol=a.sum(axis=0)
    soligne=a.sum(axis=1)
    res=list()
    for k in range(len(somcol)):
        res.append((soligne[k], somcol[k]))
    print(res)

#montresomme(all)
#print(find_best_ligne(all))
#print(find_best_col(all))

def intersect(a1, a2):
    n1=len(a1)
    n2=len(a2)
    result=list()
    for k in range(n1):
        if a1[k] in a2:
            result.append(a1[k])
    return result
            
#print(intersect(find_best_ligne(all), find_best_col(all)))

def compromis(a):
    n1=len(a)
    
    som_l=a.sum(axis=1)
    som_c=a.sum(axis=0)
    result=[]
    
    for k in range(n1):
        l=som_l[k]
        c=som_c[k]
        #on veut som_l max et som_c min
        #Donc max(som_l - som_c)
        result.append([l-c,k])
    result2=(sorted(result, key=itemgetter(0), reverse=True))
    return result2

def get_bests(l):
    #Pour le triée, renvoie l'indice des strats qui donnent le compromis max
    m=l[0][0]
    result=list()
    for elt in l:
        if elt[0]==m:
            result.append(elt[1])
        else:
            return result

print(len(get_bests(compromis(all))))
        
def montre(l):
    for elt in l:
        print("Stratégie %d" %elt)
        print(acte_force_9[elt])
        print()
        print()                   

#montre(get_bests(compromis(all)))
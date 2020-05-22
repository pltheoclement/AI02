# Création du vocabulaire
from typing import Dict, Tuple, List, Union
from lib.gopherpysat import Gophersat

N = 4 # Taille de la grille 

## Ligne à remplacer avec VOTRE emplacement et nom de l'exécutable gophersat :
## Attention ! Sous Windows, il faut remplacer les '\' par des '/' dans le chemin

gophersat_exec = "/home/theo/go/bin/gophersat"

def creationVoc(n) -> List[str] : #Création des variables pour les 5 éléments du monde (W, S, G, P, B) pour un monde de taille n*n
    voc = []
    for i in range(n):
        for j in range(n):
            voc.append("W{}{}".format(i, j))
            voc.append("S{}{}".format(i, j))
            voc.append("G{}{}".format(i, j))
            voc.append("P{}{}".format(i, j))
            voc.append("B{}{}".format(i, j))
    return voc

def ajoutClausesBreeze(gs, i, j):
    r = ["-B{}{}".format(i, j)]
    if(i-1 > 0):
        gs.push_pretty_clause(["B{}{}".format(i, j), "-P{}{}".format(i-1, j)])
        r.append("P{}{}".format(i-1, j))
    if(i+1 < N):
        gs.push_pretty_clause(["B{}{}".format(i, j), "-P{}{}".format(i+1, j)])
        r.append("P{}{}".format(i+1, j))
    if(j-1 > 0):
        gs.push_pretty_clause(["B{}{}".format(i, j), "-P{}{}".format(i, j-1)])
        r.append("P{}{}".format(i, j-1))
    if(j+1 < N):
        gs.push_pretty_clause(["B{}{}".format(i, j), "-P{}{}".format(i, j+1)])
        r.append("P{}{}".format(i, j+1))
    gs.push_pretty_clause(r)
    
def ajoutClausesStench(gs, i, j):
    r = ["-S{}{}".format(i, j)]
    if(i-1 > 0):
        gs.push_pretty_clause(["S{}{}".format(i, j), "-W{}{}".format(i-1, j)])
        r.append("W{}{}".format(i-1, j))
    if(i+1 < N):
        gs.push_pretty_clause(["S{}{}".format(i, j), "-W{}{}".format(i+1, j)])
        r.append("W{}{}".format(i+1, j))
    if(j-1 > 0):
        gs.push_pretty_clause(["S{}{}".format(i, j), "-W{}{}".format(i, j-1)])
        r.append("W{}{}".format(i, j-1))
    if(j+1 < N):
        gs.push_pretty_clause(["S{}{}".format(i, j), "-W{}{}".format(i, j+1)])
        r.append("W{}{}".format(i, j+1))
    gs.push_pretty_clause(r)

if __name__ == "__main__":
    
    voc = creationVoc(N)
    gs = Gophersat(gophersat_exec, voc)
    gs.push_pretty_clause(["-P00"])
    gs.push_pretty_clause(["-W00"])
    print(gs.dimacs())
    print(gs.solve())
    print(gs.get_pretty_model())
    print(gs.get_model())
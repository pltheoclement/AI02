# Création du vocabulaire
from typing import Dict, Tuple, List, Union
from lib.gopherpysat import Gophersat

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
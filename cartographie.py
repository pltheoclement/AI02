#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Création du vocabulaire
from typing import Dict, Tuple, List, Union
from lib.gopherpysat import Gophersat
from wumpus import WumpusWorld

N = 4 # Taille de la grille

## Ligne à remplacer avec VOTRE emplacement et nom de l'exécutable gophersat :
## Attention ! Sous Windows, il faut remplacer les '\' par des '/' dans le chemin

gophersat_exec = "/Users/felixpoullet-pages/Desktop/proj IA/gophersat"

def creationVoc(n) -> List[str] : #Création des variables pour les 5 éléments du monde (W, S, G, P, B) pour un monde de taille n*n
    voc = []
    for i in range(n):
        for j in range(n):
            voc.append("W{}_{}".format(i, j)) #wumpus
            voc.append("S{}_{}".format(i, j)) #stench puanteur
            voc.append("G{}_{}".format(i, j)) #gold
            voc.append("P{}_{}".format(i, j)) #puit
            voc.append("B{}_{}".format(i, j)) #breeze
    return voc

def ajoutClausesBreeze(gs, i, j):
    r = ["-B{}_{}".format(i, j)]
    if(i-1 > 0):
        gs.push_pretty_clause(["B{}_{}".format(i, j), "-P{}_{}".format(i-1, j)])
        r.append("P{}_{}".format(i-1, j))
    if(i+1 < N):
        gs.push_pretty_clause(["B{}_{}".format(i, j), "-P{}_{}".format(i+1, j)])
        r.append("P{}_{}".format(i+1, j))
    if(j-1 > 0):
        gs.push_pretty_clause(["B{}_{}".format(i, j), "-P{}_{}".format(i, j-1)])
        r.append("P{}_{}".format(i, j-1))
    if(j+1 < N):
        gs.push_pretty_clause(["B{}_{}".format(i, j), "-P{}_{}".format(i, j+1)])
        r.append("P{}_{}".format(i, j+1))
    gs.push_pretty_clause(r)

def ajoutClausesStench(gs, i, j):
    r = ["-S{}_{}".format(i, j)]
    if(i-1 > 0):
        gs.push_pretty_clause(["S{}_{}".format(i, j), "-W{}_{}".format(i-1, j)])
        r.append("W{}_{}".format(i-1, j))
    if(i+1 < N):
        gs.push_pretty_clause(["S{}_{}".format(i, j), "-W{}_{}".format(i+1, j)])
        r.append("W{}_{}".format(i+1, j))
    if(j-1 > 0):
        gs.push_pretty_clause(["S{}_{}".format(i, j), "-W{}_{}".format(i, j-1)])
        r.append("W{}_{}".format(i, j-1))
    if(j+1 < N):
        gs.push_pretty_clause(["S{}_{}".format(i, j), "-W{}_{}".format(i, j+1)])
        r.append("W{}_{}".format(i, j+1))
    gs.push_pretty_clause(r)

def ajoutClauseEmpty(gs, i, j):
    gs.push_pretty_clause(["-W{}_{}".format(i, j)])
    gs.push_pretty_clause(["-B{}_{}".format(i, j)])
    gs.push_pretty_clause(["-S{}_{}".format(i, j)])
    gs.push_pretty_clause(["-P{}_{}".format(i, j)])
    gs.push_pretty_clause(["-G{}_{}".format(i, j)])
    r = ["-S{}_{}".format(i, j)]
    if(i-1 > 0):
        gs.push_pretty_clause(["S{}_{}".format(i, j), "-W{}_{}".format(i-1, j)])
        r.append("W{}_{}".format(i-1, j))
    if(i+1 < N):
        gs.push_pretty_clause(["S{}_{}".format(i, j), "-W{}_{}".format(i+1, j)])
        r.append("W{}_{}".format(i+1, j))
    if(j-1 > 0):
        gs.push_pretty_clause(["S{}_{}".format(i, j), "-W{}_{}".format(i, j-1)])
        r.append("W{}_{}".format(i, j-1))
    if(j+1 < N):
        gs.push_pretty_clause(["S{}_{}".format(i, j), "-W{}_{}".format(i, j+1)])
        r.append("W{}_{}".format(i, j+1))
    gs.push_pretty_clause(r)

def isWumpus(gs,i,j):
    gs.push_pretty_clause(["-W{}_{}".format(i, j)])
    isWumpus = not(gs.solve())
    gs.pop_clause()
    return isWumpus

def isPuit(gs,i,j):
    gs.push_pretty_clause(["-P{}_{}".format(i, j)])
    isPuit = not(gs.solve())
    gs.pop_clause()
    return isPuit

def fullKnowledge():
    knowledge=ww.get_knowledge()
    parcours = True
    for i in range(ww.get_n()):
        for j in range(ww.get_n()):
            if (knowledge[i][j]=="?"):
                parcours=False
    return parcours

def globalProbe():
    knowledge=ww.get_knowledge()
    for a in range(ww.get_n()):
        for b in range(ww.get_n()):
            if knowledge[a][b]=='?': #on ne connait pas la case
            
                if isWumpus(gs, 0, 0)==False and isPuit(gs, 0, 0)==False:
                    
                    print("la case (",a,",",b,") est safe! j'utilise un probe")
                    probe1=ww.probe(a, b)
                    knowledge=ww.get_knowledge()
                    print(knowledge)
                    if (probe1[1]=="."): #la case est empty
                        ajoutClauseEmpty(gs, a, b)
                        
                    if (probe1[1]=="B"): #la case est breeze
                        ajoutClausesBreeze(gs, a, b)
                
                    if (probe1[1]=="S"): #la case est stenchy
                        ajoutClausesStench(gs, a, b)

def cautious():
    knowledge=ww.get_knowledge()        
    for a in range(ww.get_n()):
        for b in range(ww.get_n()):
            if knowledge[a][b]=='?':
                probe1=ww.cautious_probe(a,b)
                knowledge=ww.get_knowledge()
                print(knowledge)
                if (probe1[1]=="."): #la case est empty
                    ajoutClauseEmpty(gs, a, b)
                    
                if (probe1[1]=="B"): #la case est breeze
                    ajoutClausesBreeze(gs, a, b)
            
                if (probe1[1]=="S"): #la case est stenchy
                    ajoutClausesStench(gs, a, b)
                return

# Les rêgles sont les mêmes partout donc à l'initialisation :
#   Ajouter les rêgle de Breeze et de Stench et de Empty à toutes les cases (j'ai bien codé l'équivalence,
#                                   faire un "ajoutClausesBreeze(gs, i, j)" ne signifie pas qu'il y a un Breeze à la case i, j
#                                   sela signifie simplement que s'il y en a un, alors les autres cases doivent se comporter ainsi)
# Les rêgles de empty à coder :
#
# empty(i, j) <-> -W(i, j) ^ -W(i-1, j) ^ -W(i+1, j) ^ -W(i, j-1) ^ -W(i, j+1)
#               ^ -P(i, j) ^ -P(i-1, j) ^ -P(i+1, j) ^ -P(i, j-1) ^ -P(i, j+1)
#               ^ -B(i, j)
#               ^ -S(i, j)
#               ^ -G(i, j)
#
# 1) On check toutes les cases pour savoir si elles sont safe ou non.
# 2) Si une case est safe, on fait un prob sur cette case
# on relance le check sur toutes les cases
# ...
# Si pas de nouvelle clause ajoutée, on fait un cautious probe




if __name__ == "__main__":
    
# =============================================================================
#     voc = creationVoc(N)
#     gs = Gophersat(gophersat_exec, voc)
#     gs.push_pretty_clause(["-P0_0"])
#     gs.push_pretty_clause(["-W0_0"])
#     print(gs.dimacs())
#     print(gs.solve())
#     print(gs.get_pretty_model())
#     print(gs.get_model())
# =============================================================================
    
    # variables
    ww = WumpusWorld()
    voc = creationVoc(ww.get_n())
    gs = Gophersat(gophersat_exec, voc)
    
    #état des lieux 1: on ne sait rien
    print(ww.get_knowledge())
    
    #on probe l'unique case safe
    probe1=ww.probe(0, 0)
    if (probe1[1]=="."): #la case est empty
        ajoutClauseEmpty(gs, 0, 0)
        
    if (probe1[1]=="B"): #la case est breeze
        ajoutClausesBreeze(gs, 0, 0)

    if (probe1[1]=="S"): #la case est stenchy
        ajoutClausesStench(gs, 0, 0)
    
    #début du bordel
    while fullKnowledge()==False:
        globalProbe()
        print("toutes les cases inconnues restantes sont unsafe, je n'ai pas le choix j'utilise un seul cautious probe pour me dépatouiller")
        cautious()
    print("toutes les cases ont été sondés! je connais à présent ma géographie!")
    print(ww.get_knowledge())
     




#==============================================================================


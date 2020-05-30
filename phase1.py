#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 21 17:31:00 2020

@author: theo
"""

from typing import Dict, Tuple, List, Union
from lib.gopherpysat import Gophersat
from wumpus import WumpusWorld

N = 4 # Taille de la grille 

## Ligne à remplacer avec VOTRE emplacement et nom de l'exécutable gophersat :
## Attention ! Sous Windows, il faut remplacer les '\' par des '/' dans le chemin

gophersat_exec = "/home/theo/go/bin/gophersat"


def creationVoc(n) -> List[str] : #Création des variables pour les 5 éléments du monde (W, S, G, P, B) pour un monde de taille n*n
    voc = []
    for i in range(n):
        for j in range(n):
            voc.append("W{}_{}".format(i, j))
            voc.append("S{}_{}".format(i, j))
            voc.append("G{}_{}".format(i, j))
            voc.append("P{}_{}".format(i, j))
            voc.append("B{}_{}".format(i, j))
            voc.append("E{}_{}".format(i, j))
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
    gs.push_pretty_clause(["B{}_{}".format(i, j), "S{}_{}".format(i, j), "P{}_{}".format(i, j), "W{}_{}".format(i, j), "G{}_{}".format(i, j), "E{}_{}".format(i, j)])
    gs.push_pretty_clause(["-E{}_{}".format(i, j), "-B{}_{}".format(i, j)])
    gs.push_pretty_clause(["-E{}_{}".format(i, j), "-S{}_{}".format(i, j)])
    gs.push_pretty_clause(["-E{}_{}".format(i, j), "-P{}_{}".format(i, j)])
    gs.push_pretty_clause(["-E{}_{}".format(i, j), "-W{}_{}".format(i, j)])
    gs.push_pretty_clause(["-E{}_{}".format(i, j), "-G{}_{}".format(i, j)])
    
    
def isWumpus(gs,i,j):
    gs.push_pretty_clause(["-W{}_{}".format(i, j)])
    isWumpus = not(gs.solve())
    gs.pop_clause()
    return isWumpus

def isStench(gs,i,j):
    gs.push_pretty_clause(["-S{}_{}".format(i, j)])
    isStench = not(gs.solve())
    gs.pop_clause()
    return isStench

def isBreeze(gs,i,j):
    gs.push_pretty_clause(["-B{}_{}".format(i, j)])
    isBreeze = not(gs.solve())
    gs.pop_clause()
    return isBreeze

def isPuit(gs,i,j):
    gs.push_pretty_clause(["-P{}_{}".format(i, j)])
    isPuit = not(gs.solve())
    gs.pop_clause()
    return isPuit

def isEmpty(gs,i,j):
    gs.push_pretty_clause(["-E{}_{}".format(i, j)])
    isEmpty = not(gs.solve())
    gs.pop_clause()
    return isEmpty

def isSafe(gs, i, j):
    gs.push_pretty_clause(["P{}_{}".format(i, j)])
    resPuit = gs.solve()
    gs.pop_clause()
    gs.push_pretty_clause(["W{}_{}".format(i, j)])
    resWumpus = gs.solve()
    gs.pop_clause()
    if((resPuit or resWumpus) == False):
        return True
    else :
        return False

def fullKnowledge(knowledge):
    parcours = True
    for i in range(len(knowledge)):
        for j in range(len(knowledge)):
            if (knowledge[i][j]==''):
                parcours = False
    return parcours

def globalProbe(knowledge):
    knowledgeOld = []
    while(knowledge != knowledgeOld):
        knowledgeOld = knowledge
        for a in range(len(knowledge)):
            for b in range(len(knowledge)):
                if (knowledge[a][b]==''): #on ne connait pas la case
                    if(isWumpus(gs, a, b) or isStench(gs, a, b) or isBreeze(gs, a, b) or isPuit(gs, a, b) or isEmpty(gs, a, b)):
                        if(isWumpus(gs, a, b)):
                            gs.push_pretty_clause(["W{}_{}".format(a, b)])
                            knowledge[a][b] += "W"
                        if(isStench(gs, a, b)):
                            gs.push_pretty_clause(["S{}_{}".format(a, b)])
                            knowledge[a][b] += "S"
                        if(isBreeze(gs, a, b)):
                            gs.push_pretty_clause(["B{}_{}".format(a, b)])
                            knowledge[a][b] += "B"
                        if(isPuit(gs, a, b)):
                            gs.push_pretty_clause(["P{}_{}".format(a, b)])
                            knowledge[a][b] += "P"
                        if(isEmpty(gs, a, b)):
                            gs.push_pretty_clause(["E{}_{}".format(a, b)])
                            knowledge[a][b] = "."
                
                    elif(isSafe(gs, a, b)):
                        
                        print("la case (",a,",",b,") est safe! j'utilise un probe")
                        probe1=ww.probe(a, b)
                        knowledge[a][b] = probe1[1] 
                        print(knowledge)
                        if ('.' in probe1[1]): #la case est empty
                            gs.push_pretty_clause(["E{}_{}".format(a, b)])
                            
                        if ('B' in probe1[1]): #la case est breeze
                            gs.push_pretty_clause(["B{}_{}".format(a, b)])
                    
                        if ('S' in probe1[1]): #la case est stenchy
                            gs.push_pretty_clause(["S{}_{}".format(a, b)])
                        
                        if ('G' in probe1[1]): #la case est stenchy
                            gs.push_pretty_clause(["G{}_{}".format(a, b)])
    return knowledge

def verif(gs, knowledge):
    for a in range (len(knowledge)):
        for b in range (len(knowledge)):
            if(isWumpus(gs, a, b) and not("W" in knowledge[a][b])):
                knowledge[a][b] += "W"
            if(isStench(gs, a, b) and not("S" in knowledge[a][b])):
                knowledge[a][b] += "S"
            if(isBreeze(gs, a, b) and not("B" in knowledge[a][b])):
                knowledge[a][b] += "B"
            if(isPuit(gs, a, b) and not("P" in knowledge[a][b])):
                knowledge[a][b] += "P"
            if(isEmpty(gs, a, b) and not("." in knowledge[a][b])):
                knowledge[a][b] = "."
    return knowledge

def cautious(knowledge):     
    for a in range(len(knowledge)):
        for b in range(len(knowledge)):
            if knowledge[a][b]=='':
                print("la case (",a,",",b,") est pas sure! j'utilise un cautious probe")
                probe1=ww.cautious_probe(a,b)
                knowledge[a][b] = probe1[1]
                print(knowledge)
                if ('.' in probe1[1]): #la case est empty
                    gs.push_pretty_clause(["E{}_{}".format(a, b)])
                    
                if ('B' in probe1[1]): #la case est breeze
                    gs.push_pretty_clause(["B{}_{}".format(a, b)])
            
                if ('S' in probe1[1]): #la case est stenchy
                    gs.push_pretty_clause(["S{}_{}".format(a, b)])
                
                if ('G' in probe1[1]): #la case est gold
                    gs.push_pretty_clause(["G{}_{}".format(a, b)])
                    
                if ('W' in probe1[1]): #la case est Wumpus
                    gs.push_pretty_clause(["W{}_{}".format(a, b)])
                
                if ('P' in probe1[1]): #la case est Puit
                    gs.push_pretty_clause(["P{}_{}".format(a, b)])
                return knowledge


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
    knowledge = [[]] * ww.get_n()
    for i in range(ww.get_n()):
        knowledge[i] = [''] * ww.get_n()
        for j in range(ww.get_n()):
            ajoutClauseEmpty(gs, i, j)
            ajoutClausesBreeze(gs, i, j)
            ajoutClausesStench(gs, i, j)
            
            
    #on probe l'unique case safe
    probe1=ww.probe(0, 0)
    knowledge[0][0] = probe1[1]
    if ('.' in probe1[1]): #la case est empty
        gs.push_pretty_clause(["E0_0"])
        
    if ('B' in probe1[1]): #la case est breeze
        gs.push_pretty_clause(["B0_0"])

    if ('S' in probe1[1]): #la case est stenchy
        gs.push_pretty_clause(["S0_0"])
        
    if ('G' in probe1[1]): #la case est stenchy
        gs.push_pretty_clause(["G0_0"])
    
    #début du bordel
    while fullKnowledge(knowledge)==False:
        knowledge = globalProbe(knowledge)
        print("toutes les cases inconnues restantes sont unsafe, je n'ai pas le choix j'utilise un seul cautious probe pour me dépatouiller")
        knowledge = cautious(knowledge)
    knowledge = verif(gs, knowledge)
    print("toutes les cases ont été sondés! je connais à présent ma géographie!")
    print(knowledge)
    print(ww.get_cost())


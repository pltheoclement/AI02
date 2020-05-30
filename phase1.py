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

def isPuit(gs,i,j):
    gs.push_pretty_clause(["-P{}_{}".format(i, j)])
    isPuit = not(gs.solve())
    gs.pop_clause()
    return isPuit

def fullKnowledge():
    knowledge = ww.get_knowledge()
    parcours = True
    for i in range(ww.get_n()):
        for j in range(ww.get_n()):
            if (knowledge[i][j]=="?"):
                parcours = False
    return parcours

def globalProbe():
    knowledge = ww.get_knowledge()
    knowledgeOld = []
    while(knowledge != knowledgeOld):
        knowledgeOld = knowledge
        for a in range(ww.get_n()):
            for b in range(ww.get_n()):
                if knowledge[a][b]=='?': #on ne connait pas la case
                
                    if isWumpus(gs, a, b)==False and isPuit(gs, a, b)==False:
                        
                        print("la case (",a,",",b,") est safe! j'utilise un probe")
                        probe1=ww.probe(a, b)
                        knowledge=ww.get_knowledge()
                        print(knowledge)
                        if ('.' in probe1[1]): #la case est empty
                            gs.push_pretty_clause(["E{}_{}".format(a, b)])
                            
                        if ('B' in probe1[1]): #la case est breeze
                            gs.push_pretty_clause(["B{}_{}".format(a, b)])
                    
                        if ('S' in probe1[1]): #la case est stenchy
                            gs.push_pretty_clause(["S{}_{}".format(a, b)])
                        
                        if ('G' in probe1[1]): #la case est stenchy
                            gs.push_pretty_clause(["G{}_{}".format(a, b)])
        

def cautious():
    knowledge=ww.get_knowledge()        
    for a in range(ww.get_n()):
        for b in range(ww.get_n()):
            if knowledge[a][b]=='?':
                probe1=ww.cautious_probe(a,b)
                knowledge=ww.get_knowledge()
                print(knowledge)
                if ('.' in probe1[1]): #la case est empty
                    gs.push_pretty_clause(["E{}_{}".format(a, b)])
                    
                if ('B' in probe1[1]): #la case est breeze
                    gs.push_pretty_clause(["B{}_{}".format(a, b)])
            
                if ('S' in probe1[1]): #la case est stenchy
                    gs.push_pretty_clause(["S{}_{}".format(a, b)])
                
                if ('G' in probe1[1]): #la case est stenchy
                    gs.push_pretty_clause(["G{}_{}".format(a, b)])
                    
                if ('W' in probe1[1]): #la case est stenchy
                    gs.push_pretty_clause(["W{}_{}".format(a, b)])
                
                if ('P' in probe1[1]): #la case est stenchy
                    gs.push_pretty_clause(["P{}_{}".format(a, b)])
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
    ww = WumpusWorld(10, True)
    voc = creationVoc(ww.get_n())
    gs = Gophersat(gophersat_exec, voc)
    
    #état des lieux 1: on ne sait rien
    print(ww.get_knowledge())
    
    for i in range(ww.get_n()):
        for j in range(ww.get_n()):
            ajoutClauseEmpty(gs, i, j)
            ajoutClausesBreeze(gs, i, j)
            ajoutClausesStench(gs, i, j)
            
    #on probe l'unique case safe
    probe1=ww.probe(0, 0)
    if ('.' in probe1[1]): #la case est empty
        gs.push_pretty_clause(["E0_0"])
        
    if ('B' in probe1[1]): #la case est breeze
        gs.push_pretty_clause(["B0_0"])

    if ('S' in probe1[1]): #la case est stenchy
        gs.push_pretty_clause(["S0_0"])
        
    if ('G' in probe1[1]): #la case est stenchy
        gs.push_pretty_clause(["G0_0"])
    
    #début du bordel
    while fullKnowledge()==False:
        globalProbe()
        print("toutes les cases inconnues restantes sont unsafe, je n'ai pas le choix j'utilise un seul cautious probe pour me dépatouiller")
        cautious()
    print("toutes les cases ont été sondés! je connais à présent ma géographie!")
    print(ww.get_knowledge())
    print(ww.get_cost())


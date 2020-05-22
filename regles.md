# Document de travail.

### Utilisation du solveur SAT :
#### Variables à utiliser : 

- W : Un Wumpus est sur la case
- S : Il y a une odeur sur la case (signifie que le Wumpus est sur une case adjacente)
- G : Il y a de l'or sur la case
- P : Il y a un puit sur la case
- B : Il y a du vent sur la case (signifie qu'il y a un (ou plusieurs) puit(s) sur la (les) cases adjacentes.

Les variables seront donc :

Wumpus :

- W00 : Il y a un wumpus à la case (0, 0)
- W01 : Il y a un wumpus à la case (0, 1)
- ...
- W44 : Il y a un wumpus à la case (4, 4)

Stench :

- S00 : Il y a une odeur à la case (0, 0)
- S01 : Il y a une odeur à la case (0, 1)
- ...
- S44 : Il y a une odeur à la case (4, 4)

Gold :

- G00 : Il y a de l'or à la case (0, 0)
- G01 : Il y a de l'or à la case (0, 1)
- ...
- G44 : Il y a de l'or à la case (4, 4)

Puit :

- P00 : Il y a un puit à la case (0, 0)
- P01 : Il y a un puit à la case (0, 1)
- ...
- P44 : Il y a un puit à la case (4, 4)

Breeze :

- B00 : Il y a du vent à la case (0, 0)
- B01 : Il y a du vent à la case (0, 1)
- ...
- B44 : Il y a du vent à la case (4, 4)

On à donc un total de **80** variables

## Rêgles du jeu :

#### Règle 1 : Il n'y a pas de puits en 0, 0 

- R1: ¬P00

#### Règle 2 : Il n'y a pas de Wumpus en 0, 0

- R2: ¬W00

#### Règle 3 : Autour de chaque puits il y a de la brise

cela signifie que Bnn ↔ Pn(n-1) ∨ Pn(n+1) ∨ P(n-1)n ∨ P(n+1)n
ce qui se réécrit :
(¬Bnn ∨ Pn(n-1) ∨ Pn(n+1) ∨ P(n-1)n ∨ P(n+1)n) ∧ (Bnn ∨ (¬Pn(n-1) ∧ ¬Pn(n+1) ∧ ¬P(n-1)n ∧ ¬P(n+1)n))
On a donc :
- R3 : ¬Bnn Pn(n-1) Pn(n+1) P(n-1)n P(n+1)n)
- R4 : Bnn ¬Pn(n-1)
- R5 : Bnn ¬Pn(n+1)
- R6 : Bnn ¬P(n-1)n
- R7 : Bnn ¬P(n+1)n

#### Règle 4 : Autour du Wumpus, il y a une odeur fétide
Même raisonnement qu'au dessus : 

cela signifie que Snn ↔ Wn(n-1) ∨ Wn(n+1) ∨ W(n-1)n ∨ W(n+1)n
ce qui se réécrit :
(¬Snn ∨ Wn(n-1) ∨ Wn(n+1) ∨ W(n-1)n ∨ W(n+1)n) ∧ (Snn ∨ (¬Wn(n-1) ∧ ¬Wn(n+1) ∧ ¬W(n-1)n ∧ ¬W(n+1)n))
On a donc :
- R3 : ¬Snn Wn(n-1) Wn(n+1) W(n-1)n W(n+1)n)
- R4 : Snn ¬Wn(n-1)
- R5 : Snn ¬Wn(n+1)
- R6 : Snn ¬W(n-1)n
- R7 : Snn ¬W(n+1)n
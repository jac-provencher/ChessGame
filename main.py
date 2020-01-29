"""
Note sur les bitwise operations:
======================================================================================================
~ : inverse tous les chiffres
1001100 donne,
0110011
Note:
- Pour avoir la position des pions ou les cases disponibles, on utiliserait cet opérateur.
~(positions des noirs | positions des blancs) = cases restantes
~(cases restantes) = etat de jeu
======================================================================================================
& : 1 si les deux chiffres sont des 1 sinon 0 (équivaut à l'intersection des ensembles)
   0100110
 & 1010101
=  0000100
Note:
- Permettrait d'avoir les deplacements et les attaques légales pour le roi et le cheval
cases vides & les deplacements = deplacements légaux
pions adverses & les deplacements = attaques légales
======================================================================================================
| : 0 si aucun chiffre est 1 sinon 1
   0010010
 | 1001010
=  1011010
Note:
- L'union de chaque type de pion pour une couleur = etat de jeu de cette couleur
- L'union de la position des pions blancs et noirs = l'état de jeu
======================================================================================================
^ : si les deux chiffres sont pairs 0 sinon 1
   0100101
 ^ 1001001
=  0010011
Note:
- Permettrait d'avoir les deplacements et les attaques legales pour la reine, le fou et la tour
On ajoute les coups jusqu'à temps de croiser un pion (1 croise un autre 1) = deplacements legale
Si on croise un pion,
qu'on fait l'intersection de sa position avec celles des pions adverses, on verifiera si le pion est adverse ou non = attaques legales
======================================================================================================
<< : shift les nombres vers la gauche d'une valeur n
10 << 2 = 40
bin(10) = 1010
Donc, 10 << 2 = 1010 << 2 = 101000 = 40

>> : même chose que <<, mais vers la droite

Note:
- Permettrait de faire le deplacement des pions
======================================================================================================
Méthode utilisée pour moveGenerator

    Pour K et C,
    legalMoves = freeSpots & moveBank(piece)

    Pour P,
    si sur la ligne de depart, takewhile aucune rencontre de pion
    Autrement, si la position (x, y+1) pour les blancs ou (x, y-1)
    pour les noirs est valide, yield cette position

    Pour Q, F, et T,
    takewhile aucune rencontre de pion, yield les positions stored

=============================================
Méthode utilisée pour killGenerator

    Pour K et C,
    legalAttacks = pions adverse & moveBank(piece)

    Pour P,
    si les positions d'attaques sont dans les pions adverses,
    yield la position

    Pour Q, F et T,
    Dans chaque direction, si on croise un pion, on store sa position.
    Si cette position est dans les pions adverses,
    yield la position

=============================================
Méthode utilisée pour isCheckmate

    S'il n'y a pas échec, return False

    Pour tous les coups possibles, si aucun des ses coups permet
    de parer l'échec, le roi est nécessairement échec et mat.

=============================================
Méthode utilisée pour isCheck

    Si la position du roi est dans les attaques
    adverses, return True. Autrement, False

    (l'intersection entre la position du roi et les attaques
    adverses serait une autre solution)

======================================================================================================
"""

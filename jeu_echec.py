from copy import deepcopy
from itertools import chain, takewhile
from more_itertools import first_true, flatten, take, tail
from random import randint

"""
TODO LIST:
(1) OK les méthodes isValidPosition, takeWhile et pawnPositions doivent pouvoir prendre en argument un etat de jeu
(2) OK Faire les méthodes movePiece et killPiece
(3) OK Trouver un moyen de simplifier moveBank
(4) OK Faire isCheckmate
(5) OK Faire isCheck
(6) Apprendre à travailler avec les files (pour avoir un historique des coups joués)
(7) Voir si possible d'implanter la sous-promotion
(8) OK Faire un affichage avec pygame
(9) OK Faire algorithme minimax
(10) Implanter le roque
(11) OK Arranger killGenerator
"""

class ChessError(Exception):
    """Classe pour les erreurs soulevées par chess."""

class chess:

    def __init__(self):
        self.etat = {
        'black':
        {
        (1, 7): 'P', (2, 7): 'P', (3, 7): 'P', (4, 7): 'P',
        (5, 7): 'P', (6, 7): 'P', (7, 7): 'P', (8, 7): 'P',
        (1, 8): 'T', (8, 8): 'T', (7, 8): 'C', (2, 8): 'C',
        (3, 8): 'F', (6, 8): 'F', (5, 8): 'K', (4, 8): 'Q'
        },
        'white':
        {
        (1, 2): 'P', (2, 2): 'P', (3, 2): 'P', (4, 2): 'P',
        (5, 2): 'P', (6, 2): 'P', (7, 2): 'P', (8, 2): 'P',
        (1, 1): 'T', (8, 1): 'T', (2, 1): 'C', (7, 1): 'C',
        (3, 1): 'F', (6, 1): 'F', (5, 1): 'K', (4, 1): 'Q'
        }
        }
        self.uniCode = {
        'black': {'P': '♙', 'C': '♘', 'F': '♗', 'Q': '♕', 'K': '♔', 'T': '♖'},
        'white': {'P': '♟', 'C': '♞', 'F': '♝', 'Q': '♛', 'K': '♚', 'T': '♜'}
        }
        self.vectors = [(0, 1), (0, -1), (-1, 0), (1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1)]
        self.pawnValue = {'P':10, 'C':30, 'F':30, 'T':50, 'Q':90, 'K':1000}
        self.oppo = {'black':'white', 'white':'black'}
        self.pawnKilled = {'black': [], 'white': []}
        self.startingLine = {'black': 7, 'white': 2}
        self.endingLine = {'black': 1, 'white': 8}
        self.boardPositions = lambda: ((x, y) for x in range(1, 9) for y in range(1, 9))
        self.onBoard = lambda position: 1 <= position[0] <= 8 and 1 <= position[1] <= 8
        self.pawnPositions = lambda state: chain(state['black'], state['white'])
        self.infinity = 999_999_999_999
        self.pieces = ['BP', 'BQ', 'BK', 'BF', 'BT', 'BC', 'WP', 'WQ', 'WK', 'WF', 'WT', 'WC']
        self.colorDico = {'black': 'B', 'white': 'W'}
        self.turnCode = {'black': randint(0, self.infinity), 'white': randint(0, self.infinity)}
        self.positionCodes = {(x, y): {piece: randint(0, self.infinity) for piece in self.pieces} for x in range(1, 9) for y in range(1, 9)}
        self.transpositionTable = {}
        self.hits = 0
        self.petitRoque = False
        self.grandRoque = False

    def __str__(self):
        """Retourne une représentation en ASCII du board"""
        board = [['.' for x in range(8)] for y in range(8)]
        for color, positions in self.etat.items():
            for position, piece in positions.items():
                x, y = position
                board[8-y][x-1] = self.uniCode[color][piece]

        return '='*16 + '\n' + '\n'.join(' '.join(spot for spot in row) for row in board) + '\n' + '='*16

    def moveBank(self, position, piece):
        """
        Méthode qui retourne un tuple des coups légals
        pour la piece à la position en argument
        :returns: tuple
        """
        x, y = position
        if piece == 'K':
            return ((x+i, y+j) for i, j in self.vectors)
        elif piece == 'T':
            return (((x+i*n, y+j*n) for n in range(1, 9)) for i, j in take(4, self.vectors))
        elif piece == 'Q':
            return (((x+i*n, y+j*n) for n in range(1, 9)) for i, j in self.vectors)
        elif piece == 'F':
            return (((x+i*n, y+j*n) for n in range(1, 9)) for i, j in tail(4, self.vectors))
        elif piece == 'C':
            return ((x+1, y+2), (x-1, y+2), (x+2, y+1), (x-2, y+1), (x+2, y-1), (x-2, y-1), (x+1, y-2), (x-1, y-2))

    def moveGenerator(self, state, color, position):
        """
        Méthode qui génère les déplacement légals pour la position demandée
        """
        isValidPosition = lambda position: position not in self.pawnPositions(state) and self.onBoard(position)
        notCheck = lambda move: not self.isCheck(self.simulateState(state, color, position, move), color)
        piece = state[color][position]

        # Pions portés fixes
        if piece in ('K', 'C'):
            freeSpots = set(self.boardPositions()) - set(self.pawnPositions(state))
            legalMoves = filter(notCheck, freeSpots & set(self.moveBank(position, piece)))
            for move in legalMoves:
                yield move

        # Pions
        elif piece == 'P':
            x, y = position
            deplacements = ((x, y+1), (x, y+2)) if color == 'white' else ((x, y-1), (x, y-2))
            if y == self.startingLine[color]:
                legalMoves = filter(notCheck, takewhile(isValidPosition, deplacements))
                for move in legalMoves:
                    yield move
            elif isValidPosition(move := deplacements[0]) and notCheck(deplacements[0]):
                    yield move

        # Pions longues portées
        else:
            legalMoves = map(lambda direction: filter(notCheck, takewhile(isValidPosition, direction)), self.moveBank(position, piece))
            for moves in legalMoves:
                for move in moves:
                    yield move

    def killGenerator(self, state, color, position):
        """
        Méthode qui génère les attaques possibles pour la
        position demandée selon le state donné
        """
        notCheck = lambda attack: not self.isCheck(self.simulateState(state, color, position, attack), color)
        piece = state[color][position]
        oppoPawnPositions = state[self.oppo[color]]

        # Pions portés fixes
        if piece in ('K', 'C'):
            if attacks := filter(notCheck, set(oppoPawnPositions) & set(self.moveBank(position, piece))):
                for attack in attacks:
                    yield attack

        # Pions
        elif piece == 'P':
            x, y = position
            attacks = ((x+1, y+1), (x-1, y+1)) if color == 'white' else ((x+1, y-1), (x-1, y-1))
            for attack in attacks:
                if attack in oppoPawnPositions and notCheck(attack):
                    yield attack

        # Pions longues portées
        else:
            isPawn = lambda position: position in self.pawnPositions(state)
            attacks = map(lambda direction: first_true(direction, default=False, pred=isPawn), self.moveBank(position, piece))
            for attack in attacks:
                if attack in oppoPawnPositions and notCheck(attack):
                    yield attack

    def getZobristCode(self, state, color):
        """
        Méthode permettant de générer un code unique
        pour l'état 'state' donné.
        :returns: int
        """
        codes = [self.positionCodes[position][f"{self.colorDico[color]}"+piece] for color, pieces in state.items() for position, piece in pieces.items()]
        stateCode = codes[0]
        for code in codes[1:]:
            stateCode ^= code

        return stateCode ^ self.turnCode[color]

    def isCastling(self, state, color):
        """
        Méthode qui vérifie si le roque est possible
        selon l'état 'state' pour la couleur 'color'.
        :returns: bool

        Conditions pour roquer:
        - Ni le roi, ni la tour n'ont été déplacé.
        - Aucun pion ne doit se trouver entre le roi et la tour.
        - Aucunes des cases entre le roi et la tour ne doivent être menacés par l'adversaire.
        - Le roi n'est pas échec.
        - La position finale du roi ne le mettrait pas en échec.
        """
        pass

    def movePiece(self, color, pos1, pos2):
        """
        Méthode qui permet de déplacer le pion
        à pos1 vers pos2.
        """
        # Déplacement du pion (pos1 --> pos2)
        piece = self.etat[color][pos1]
        self.etat[color].update({pos2:piece})
        del self.etat[color][pos1]

        # Check si promotion possible
        if position := self.pawnPromotion(self.etat, color):
            self.etat[color].update({position:'Q'})

        # Check si echec et mat
        elif winner := self.isCheckmate(self.etat, self.oppo[color]):
            raise ChessError(winner)

    def killPiece(self, color, pos1, pos2):
        """
        Méthode qui permet d'attaquer le pion
        à pos2 avec le pion à pos1
        """
        # Check l'input
        if pos2 not in self.etat[self.oppo[color]]:
            raise ChessError("Aucun pion adverse ne peut être mangé à cette position.")

        # Déplacement du pion (pos1 --> pos2)
        self.movePiece(color, pos1, pos2)

        # Suppression du pion à pos2
        target = self.etat[self.oppo[color]][pos2]
        self.pawnKilled[self.oppo[color]].append(target)
        del self.etat[self.oppo[color]][pos2]

    def getMove(self, color, pos1=None, pos2=None):
        """
        Méthode qui prend le input de l'utilisateur
        Appel la méthode approprié selon le coup.
        """
        # Check l'input
        self.isValidInput(color, pos1, pos2)

        # Appel de la bonne méthode
        if pos2 in self.etat[self.oppo[color]]:
            self.killPiece(color, pos1, pos2)
        else:
            self.movePiece(color, pos1, pos2)

    def isValidInput(self, color, pos1, pos2):
        """
        Méthode qui valide si le input rentrer
        par l'utilisateur est valide. Raise une
        ChessError
        """
        if not isinstance(color, str):
            raise ChessError("La couleur doit être une chaine de caractère.")
        if color not in ('black', 'white'):
            raise ChessError("Couleur invalide.")
        if not isinstance(pos1, tuple) or not isinstance(pos2, tuple):
            raise ChessError("Au moins une des positions n'a pas le bon format, soit (x, y).")
        if len(pos1) != 2 or len(pos2) != 2:
            raise ChessError("Au moins une des positions n'a pas le bon nombre d'éléments.")
        if not self.onBoard(pos1) or not self.onBoard(pos2):
            raise ChessError("Au moins une des positions n'est pas sur l'échiquier")
        if pos1 not in self.etat[color]:
            raise ChessError(f"La case sélectionné n'est pas occupé par un pion {color}")
        if pos2 not in chain(self.moveGenerator(self.etat, color, pos1), self.killGenerator(self.etat, color, pos1)):
            raise ChessError("Ce coup ne respecte pas les règles du jeu.")

    def isCheckmate(self, state, color):
        """
        Méthode qui verifie si le roi 'color'
        est en situation d'échec et mat.
        Retourne le gagnant si oui,
        False autrement.
        """
        if not self.isCheck(state, color):
            return False

        canMove = flatten(map(
        lambda position: chain(
        self.moveGenerator(state, color, position),
        self.killGenerator(state, color, position)
        ), state[color]))

        return False if any(canMove) else f"Le gagnant est le joueur {self.oppo[color]}!"

    def isCheck(self, state, color):
        """
        Vérifie si un des roi est en échec.
        Retourne un bool
        """
        isPawn = lambda position: position in self.pawnPositions(state)
        opponents = state[self.oppo[color]]

        # get king's position
        for position, piece in state[color].items():
            if piece == 'K':
                kingPosition = position

        # Direction en x et en +
        for pion in ('F', 'T'):
            pionsFound = map(lambda direction: first_true(direction, default=False, pred=isPawn), self.moveBank(kingPosition, pion))
            for position in pionsFound:
                if opponents.get(position) in (pion, 'Q'):
                    return True

        # Pour le cavalier
        pionsFound = set(opponents) & set(self.moveBank(kingPosition, 'C'))
        for position in pionsFound:
            if opponents[position] == 'C':
                return True

        # Pour le pion
        x, y = kingPosition
        dy = +1 if color == 'white' else -1
        for position in ((x+1, y+dy), (x-1, y+dy)):
            if opponents.get(position) == 'P':
                return True

        return False

    def pawnPromotion(self, state, color):
        """
        Méthode qui vérifie si la promotion d'un pion 'color'
        est possible. Si oui, retourne sa position,
        autrement, retourne False
        """
        linePositions = ((x, self.endingLine[color]) for x in range(1, 9))
        for position in linePositions:
            if state.get(color).get(position) == 'P':
                return position
        return False

    def simulateState(self, etatCourant, color, pos1, pos2):
        """
        Méthode qui permet de déplacer conditionnellement un pion
        Retourne un état de partie
        """
        piece = etatCourant[color][pos1]
        futureState = deepcopy(etatCourant)
        if pos2 in futureState[self.oppo[color]]:
            del futureState[self.oppo[color]][pos2]
        futureState[color].update({pos2:piece})
        del futureState[color][pos1]

        return futureState

    def autoplay(self, color):
        """
        Méthode qui joue un coup automatiquement
        pour les pions 'color'
        """
        pos1, pos2 = self.minimax(3, self.etat, color, -self.infinity, self.infinity, True)[1]

        # Appel de la bonne méthode
        if pos2 in self.etat[self.oppo[color]]:
            self.killPiece(color, pos1, pos2)
        else:
            self.movePiece(color, pos1, pos2)

    def minimax(self, depth, state, color, alpha, beta,  isMaximizing):
        """
        Méthode permettant de chercher, à partir de l'arbre de récursion,
        le coup le plus avantageux pour le joueur 'color'.
        :returns: (value, position)
        """
        # Critères d'arrêt
        if depth == 0 or self.isCheckmate(state, color):
            return (-1 if not isMaximizing else 1)*self.staticEvaluation(state, color), None

        # Vérification si l'état 'state' a déjà été évalué (Si non, l'ajouter)
        stateCode = self.getZobristCode(state, color)
        if evaluation := self.transpositionTable.get(stateCode):
            self.hits += 1
            return evaluation[0], evaluation[1]

        elif isMaximizing:
            maxEval, bestMove = -self.infinity, None

            for position in state[color]:
                possibleMoves = chain(self.killGenerator(state, color, position), self.moveGenerator(state, color, position))
                for move in possibleMoves:
                    temporaryState = self.simulateState(state, color, position, move)

                    # Maximisation du score
                    bestReply = self.minimax(depth-1, temporaryState, self.oppo[color], alpha, beta, not isMaximizing)[0]
                    if bestReply > maxEval:
                        maxEval, bestMove = bestReply, (position, move)

                    # Alpha-beta pruning
                    alpha = max(alpha, maxEval)
                    if beta <= alpha:
                        return maxEval, bestMove

                    # Ajout de l'évaluation à la table de transposition
                    self.transpositionTable[stateCode] = (maxEval, bestMove)

            return maxEval, bestMove

        else:
            minEval, bestMove = self.infinity, None

            for position in state[color]:
                possibleMoves = chain(self.killGenerator(state, color, position), self.moveGenerator(state, color, position))
                for move in possibleMoves:
                    temporaryState = self.simulateState(state, color, position, move)
                    stateCode = self.getZobristCode(temporaryState, color)
                    self.transpositionTable[stateCode] = self.minimax(depth-1, temporaryState, self.oppo[color], alpha, beta, not isMaximizing)

                    # Minimisation du score
                    bestReply = self.minimax(depth-1, temporaryState, self.oppo[color], alpha, beta, not isMaximizing)[0]
                    if bestReply < minEval:
                        minEval, bestMove = bestReply, (position, move)

                    # Alpha-beta pruning
                    beta = min(beta, minEval)
                    if beta <= alpha:
                        return minEval, bestMove

                    # Ajout de l'évaluation à la table de transposition
                    self.transpositionTable[stateCode] = (minEval, bestMove)

            return minEval, bestMove

    def staticEvaluation(self, state, color):
        """
        Méthode permettant d'obtenir la valeur utilitaire de
        l'état de jeu 'state' en fonction des paramètres désirés.
        :returns: int
        """
        materialDifference = self.getMaterialValue(state, color) - self.getMaterialValue(state, self.oppo[color])

        return materialDifference

    def getMaterialValue(self, state, color):
        """
        Méthode qui retourne la valeur matériel pour le joueur
        'color'.
        :returns: int
        """
        return sum(self.pawnValue[piece] for piece in state[color].values())

a = chess()
print(a)
print(a.getZobristCode(a.etat, 'white'))

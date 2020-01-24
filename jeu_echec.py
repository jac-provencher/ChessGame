import sys
from itertools import chain, takewhile

"""
TODO LIST:
(1) OK les méthodes isValidPosition, takeWhile et pawnPositions doivent pouvoir prendre en argument un etat de jeu
(2) Faire les méthodes movePiece et killPiece
(3) Trouver un moyen de simplifier moveBank
"""

class chess:

    def __init__(self):
        self.etat = {
        'black':
        {
        (1, 7): 'P', (2, 7): 'P', (3, 7): 'P', (4, 7): 'P',
        (5, 7): 'P', (6, 7): 'P', (7, 7): 'P', (8, 7): 'P',
        (1, 8): 'T', (8, 8): 'T', (2, 8): 'C', (7, 8): 'C',
        (3, 8): 'F', (6, 8): 'F', (5, 8): 'K', (4, 8): 'Q'
        },
        'white':
        {
        (1, 2): 'P', (2, 2): 'P', (3, 2): 'P', (4, 2): 'P',
        (5, 2): 'P', (6, 2): 'P', (7, 2): 'P', (8, 2): 'P',
        (1, 1): 'T', (8, 1): 'T', (2, 1): 'C', (7, 1): 'C',
        (3, 1): 'F', (6, 1): 'F', (4, 1): 'K', (5, 1): 'Q'
        }
        }
        self.uniCode = {
        'white': {'P': '♙', 'C': '♘', 'F': '♗', 'Q': '♕', 'K': '♔', 'T': '♖'},
        'black': {'P': '♟', 'C': '♞', 'F': '♝', 'Q': '♛', 'K': '♚', 'T': '♜'}
        }
        self.oppo = {'black':'white', 'white':'black'}
        self.pawnKilled = {'black':[], 'white':[]}
        self.startingLine = {'black': 7, 'white': 2}
        self.endingLine = {'black': 1, 'white': 8}
        self.boardPositions = lambda: ((x, y) for x in range(1, 9) for y in range(1,9))
        self.pawnPositions = lambda state: chain(state['black'], state['white'])

    def __str__(self):
        board = [['.' for x in range(8)] for y in range(8)]
        for color, positions in self.etat.items():
            for position, piece in positions.items():
                x, y = position
                board[y-1][x-1] = self.uniCode[color][piece]

        return '\n'.join(' '.join(spot for spot in row) for row in board)

    def moveBank(self, position, piece):
        """
        Méthode qui retourne un tuple des coups légals
        pour la piece à la position en argument
        :returns: tuple
        """
        x, y = position
        if piece == 'K':
            return (
            (x, y+1), (x, y-1), (x+1, y), (x-1, y),
            (x+1, y+1), (x-1, y+1), (x+1, y-1), (x-1, y-1)
            )
        elif piece == 'C':
            return (
            (x+1, y+2), (x-1, y+2), (x+2, y+1), (x-2, y+1),
            (x+2, y-1), (x-2, y-1), (x+1, y-2), (x-1, y-2)
            )
        elif piece == 'T':
            return (
            ((x+i, y) for i in range(1, 9)), ((x-i, y) for i in range(1, 9)),
            ((x, y+i) for i in range(1, 9)), ((x, y-i) for i in range(1, 9))
            )
        elif piece == 'Q':
            return (
            ((x, y+i) for i in range(1, 9)), ((x, y-i) for i in range(1, 9)),
            ((x+i, y) for i in range(1, 9)), ((x-i, y) for i in range(1, 9)),
            ((x+i, y+i) for i in range(1, 9)), ((x-i, y+i) for i in range(1, 9)),
            ((x+i, y-i) for i in range(1, 9)), ((x-i, y-i) for i in range(1, 9))
            )
        elif piece == 'F':
            return (
            ((x+i, y+i) for i in range(1, 9)), ((x+i, y-i) for i in range(1, 9)),
            ((x-i, y+i) for i in range(1, 9)), ((x-i, y-i) for i in range(1, 9))
            )

    def moveGenerator(self, state, color, position):
        """
        Méthode qui génère les déplacement légals pour la position demandée
        """
        isValidPosition = lambda position: position not in self.pawnPositions(state) and position in self.boardPositions()
        piece = state[color][position]
        x, y = position

        # Kings et Chevals
        if piece in ['K', 'C']:
            freeSpots = set(self.boardPositions()) - set(self.pawnPositions(state))
            legalMoves = freeSpots & set(self.moveBank(position, piece))
            for move in legalMoves:
                yield move

        # Pions
        elif piece == 'P':
            if y == self.startingLine[color]:
                deplacements = ((x, y+1), (x, y+2)) if color == 'white' else ((x, y-1), (x, y-2))
                legalMoves = takewhile(isValidPosition, (move for move in deplacements))
                for move in legalMoves:
                    yield move
            elif move := deplacements[0] not in state and move in self.boardPositions():
                yield move

        # Queens, Tours, Fous
        else:
            legalMoves = map(lambda direction: takewhile(isValidPosition, direction), self.moveBank(position, piece))
            for moves in legalMoves:
                for move in moves:
                    yield move

    def killGenerator(self, state, color, position):
        """
        Méthode qui génère les attaques possibles pour la
        position demandée selon le state donné
        """
        piece = state[color][position]
        oppoPawnPositions = state[self.oppo[color]].keys()
        x, y = position

        # Pions portés fixes
        if piece in ('K', 'C'):
            if attacks := set(oppoPawnPositions) & set(self.moveBank(position, piece)):
                for attack in attacks:
                    yield attack

        # Pions
        elif piece == 'P':
            legalAttacks = ((x+1, y+1), (x-1, y+1)) if color == 'white' else ((x+1, y-1), (x-1, y-1))
            for attack in legalAttacks:
                if attack in oppoPawnPositions:
                    yield attack

        # Pions longues portées
        else:
            for direction in self.moveBank(position, piece):
                for move in direction:
                    # Out of bound, break
                    if move not in self.boardPositions():
                        break
                    # Case libre, aucun pion à manger, continue
                    elif move not in self.pawnPositions(state):
                        continue
                    # Case occupée mais pas pion adverse, break
                    elif move not in oppoPawnPositions:
                        break
                    # Nécessairement, une attaque est possible
                    yield move
                    break

    def movePiece(self, color, pos1, pos2):
        pass

    def killPiece(self, color, pos1, pos2):
        pass

    def isCheckmate(self, state):
        pass

    def isCheck(self, state):
        pass

    def pawnPromotion(self, state, color):
        """
        Méthode qui vérifie si la promotion d'un pion 'color'
        est possible. Si oui, retourne sa position,
        autrement, retourne False
        """
        linePositions = ((x, self.endingLine[color]) for x in range(1, 9))
        for position in linePositions:
            if position in chain(state['black'], state['white']):
                return position
        return False

    def simulateState(self, etatCourant, color, pos1, pos2):
        """
        Méthode qui permet de déplacer conditionnellement un pion
        Retourne un état de partie
        """
        piece, modification = etatCourant[color][pos1], {color:{pos2:piece}}
        etatCourant.update(modification)
        del etatCourant[color][pos1]

        return etatCourant

    def displayLegalMoves(self, state):
        for color, positions in state.items():
            print(f"{color}:")
            for position, piece in positions.items():
                legalMoves = ', '.join(str(move) for move in self.moveGenerator(state, color, position))
                legalKills = ', '.join(str(attack) for attack in self.killGenerator(state, color, position))
                print(f"{piece}: {position} → Moves: {legalMoves}, Attacks: {legalKills}")

jeu = chess()
print(jeu)
jeu.displayLegalMoves(jeu.etat)

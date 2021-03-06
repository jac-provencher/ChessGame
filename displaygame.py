import pygame
from more_itertools import tail
from jeu_echec import ChessError, chess

pygame.init()

class display(chess):

    def __init__(self):
        super().__init__()

        # Caractéristiques de la fenêtre
        pygame.display.set_caption("Échecs")
        self.dx = 104
        self.boardHeight = 696
        self.boardWidth = 696
        self.squareX, self.squareY = self.boardWidth//8, self.boardHeight//8
        self.screen = pygame.display.set_mode((self.boardWidth + self.dx, self.boardHeight))
        self.screen.fill((104, 103, 98))

        # Images
        self.board = pygame.image.load("images/board.png")
        self.contour = pygame.image.load("images/contour.png")
        self.circle = pygame.image.load("images/circle.png")
        self.pieces = {
        'black':
        {
        'P': pygame.image.load("images/pion_noir.png"),
        'T': pygame.image.load("images/tour_noir.png"),
        'F': pygame.image.load("images/fou_noir.png"),
        'Q': pygame.image.load("images/reine_noir.png"),
        'K': pygame.image.load("images/roi_noir.png"),
        'C': pygame.image.load("images/cheval_noir.png")
        },
        'white':
        {
        'P': pygame.image.load("images/pion_blanc.png"),
        'T': pygame.image.load("images/tour_blanc.png"),
        'F': pygame.image.load("images/fou_blanc.png"),
        'Q': pygame.image.load("images/reine_blanc.png"),
        'K': pygame.image.load("images/roi_blanc.png"),
        'C': pygame.image.load("images/cheval_blanc.png")
        }
        }
        self.button = {True: pygame.image.load("images/on.png"), False: pygame.image.load("images/off.png")}

        # Suivi des clicks
        self.boardClickPosition = [(0, 0), (0, 0)]
        self.cursorPosition = None

        # Fonctions anonymes pour les positions
        self.windowToBoard = lambda position: (position[0]//self.squareX+1, 8-position[1]//self.squareY)
        self.boardToWindow = lambda position: ((position[0]-1)*self.squareX, self.boardHeight - (position[1])*self.squareY)
        self.getLastPositions = lambda positions: list(tail(2, positions))
        self.scaleX = lambda index: self.boardWidth + (index // 6) * ((self.boardWidth // 8) // 3)
        self.scaleY = lambda index, color: (index % 6) * ((self.boardHeight // 8) // 3) + self.colorPosition[color]

        # Boolean values
        self.showMove = True

        # Importation de sons
        self.moveSound = pygame.mixer.Sound("sons/moveSound.wav")
        self.buttonSound = pygame.mixer.Sound("sons/switchSound.wav")

        # Placements des pions mangés par couleur
        self.colorPosition = {'black': 0, 'white': (self.boardHeight // 8)*6}

    def redrawScreen(self, screen):
        """
        Méthode qui regénère la fenêtre à chaque loop
        """
        screen.blit(self.board, (0, 0))

        # Positions des pions
        for color, positions in self.etat.items():
            for position, piece in positions.items():
                pos = self.boardToWindow(position)
                screen.blit(self.pieces[color][piece], pos)

        # Show les deplacements et attaques valides
        if self.cursorPosition in self.etat['white'] and self.showMove:
            for move in self.moveGenerator(self.etat, 'white', self.cursorPosition):
                pos = self.boardToWindow(move)
                screen.blit(self.contour, pos)
            for attack in self.killGenerator(self.etat, 'white', self.cursorPosition):
                pos = self.boardToWindow(attack)
                screen.blit(self.circle, pos)

        # Update button state
        position = (self.boardWidth, (self.boardHeight-55)//2)
        screen.blit(self.button[self.showMove], position)

        # Display les pions mangés
        for color, pions in self.pawnKilled.items():
            for i, pion in enumerate(pions):
                pawnScaled = pygame.transform.scale(self.pieces[color][pion], (self.squareX//3, self.squareY//3))
                screen.blit(pawnScaled, (self.scaleX(i), self.scaleY(i, color)))

        pygame.display.update()

    def isClicked(self, clickPosition):
        x, y = clickPosition
        booleanDico = {
        'showMove': self.boardWidth <= x <= self.boardWidth + self.dx and self.boardHeight/2 - 59/2 <= y <= self.boardHeight/2 + 59/2,
        }
        if booleanDico['showMove']:
            self.showMove = not self.showMove
            self.buttonSound.play()

partie = display()
running = True
turn = 'white'
while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouseClick = partie.windowToBoard(event.pos)
            partie.isClicked(event.pos)
            partie.boardClickPosition.append(mouseClick)
            try:
                pos1, pos2 = partie.getLastPositions(partie.boardClickPosition)
                partie.getMove('white', pos1, pos2)
                partie.moveSound.play()
            except ChessError:
                turn = 'white'
                continue
            else:
                turn = 'black'

            if turn == 'black':
                partie.autoplay('black')
                turn = 'white'
                print(partie)
                print(f"La table contient {len(partie.transpositionTable)} états")
                print(f"La table de transposition a été hit {partie.hits} fois")

    partie.cursorPosition = partie.windowToBoard(pygame.mouse.get_pos())

    partie.redrawScreen(partie.screen)

pygame.quit()

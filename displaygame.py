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
        self.screenHeight = 696
        self.screenWidth = 696
        self.squareX, self.squareY = self.screenWidth//8, self.screenHeight//8
        self.screen = pygame.display.set_mode((self.screenWidth + self.dx, self.screenHeight))
        self.screen.fill((104, 103, 98))

        # Images
        self.board = pygame.image.load("board.png")
        self.contour = pygame.image.load("contour.png")
        self.circle = pygame.image.load("circle.png")
        self.pieces = {
        'black':
        {
        'P': pygame.image.load("pion_noir.png"),
        'T': pygame.image.load("tour_noir.png"),
        'F': pygame.image.load("fou_noir.png"),
        'Q': pygame.image.load("reine_noir.png"),
        'K': pygame.image.load("roi_noir.png"),
        'C': pygame.image.load("cheval_noir.png")
        },
        'white':
        {
        'P': pygame.image.load("pion_blanc.png"),
        'T': pygame.image.load("tour_blanc.png"),
        'F': pygame.image.load("fou_blanc.png"),
        'Q': pygame.image.load("reine_blanc.png"),
        'K': pygame.image.load("roi_blanc.png"),
        'C': pygame.image.load("cheval_blanc.png")
        }
        }

        # Suivi des clicks
        self.boardClickPosition = [(0, 0), (0, 0)]
        self.cursorPosition = None

        # Fonctions anonymes pour les positions
        self.windowToBoard = lambda position: (position[0]//self.squareX+1, 8-position[1]//self.squareY)
        self.boardToWindow = lambda position: ((position[0]-1)*self.squareX, self.screenHeight - (position[1])*self.squareY)
        self.getPos = lambda positions: list(tail(2, positions))
        self.scaleX = lambda index: self.screenWidth + (index // 3) * ((self.screenWidth // 8) // 3)
        self.scaleY = lambda index: (index % 4) * ((self.screenHeight // 8) // 3) + (self.screenHeight // 8) // 10

        # Boolean values
        self.showMove = True
        self.button = {True: pygame.image.load("on.png"), False: pygame.image.load("off.png")}

        # Importation de sons
        self.moveSound = pygame.mixer.Sound("moveSound.wav")

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
        position = (self.screenWidth, (self.screenHeight-55)//2)
        screen.blit(self.button[self.showMove], position)

        # Display les pions mangés
        for color, pions in self.pawnKilled.items():
            for i, pion in enumerate(sorted(pions)):
                pawnScaled = pygame.transform.scale(self.pieces[color][pion], (self.squareX//3, self.squareY//3))
                screen.blit(pawnScaled, (self.scaleX(i), self.scaleY(i)))

        pygame.display.update()

    def isClicked(self, button, clickPosition):
        x, y = clickPosition
        middleY, dy = self.screenHeight/2, 59/2
        booleanDico = {
        'showMove': self.screenWidth <= x <= self.screenWidth + self.dx and middleY - dy <= y <= middleY + dy
        }
        self.showMove = not self.showMove if booleanDico['showMove'] else self.showMove

partie = display()
running = True
turn = 'white'
while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouseClick = partie.windowToBoard(event.pos)
            partie.isClicked('showMove', event.pos)
            partie.boardClickPosition.append(mouseClick)
            try:
                pos1, pos2 = partie.getPos(partie.boardClickPosition)
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

    partie.cursorPosition = partie.windowToBoard(pygame.mouse.get_pos())

    partie.redrawScreen(partie.screen)

pygame.quit()

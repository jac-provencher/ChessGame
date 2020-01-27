import pygame
from more_itertools import tail
from jeu_echec import ChessError, chess

pygame.init()

class display(chess):

    def __init__(self):
        super().__init__()
        pygame.display.set_caption("Échecs")
        self.screenWidth = 800
        self.screenHeight = 696
        self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        self.screen.fill((104, 103, 98))
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
        self.clickPosition = [(0, 0), (0, 0)]
        self.cursorPosition = None
        self.windowToBoard = lambda position:(position[0]//87+1, 8-position[1]//87)
        self.boardToWindow = lambda position: ((position[0]-1)*87, self.screenHeight - (position[1])*87)
        self.getPos = lambda positions: list(tail(2, positions))
        self.showMove = True
        self.button = {True: pygame.image.load("on.png"), False: pygame.image.load("off.png")}
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
        position = self.boardToWindow((9, 5))
        screen.blit(self.button[self.showMove], position)

        pygame.display.update()

partie = display()
running = True
turn = 'white'
while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouseClick = partie.windowToBoard(event.pos)

            if mouseClick in ((9, 5), (10, 5)):
                partie.showMove = not partie.showMove

            partie.clickPosition.append(mouseClick)
            try:
                pos1, pos2 = partie.getPos(partie.clickPosition)
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

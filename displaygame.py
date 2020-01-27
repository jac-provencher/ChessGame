import pygame
from more_itertools import tail
from jeu_echec import ChessError, chess

pygame.init()

class display(chess):

    def __init__(self):
        super().__init__()
        pygame.display.set_caption("Échecs")
        self.screenWidth = self.screenHeight = 696
        self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight))
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
        self.convert = lambda position:(position[0]//87+1, 8-position[1]//87)
        self.cursorPosition = None

    def getPos(self, positions):
        pos1, pos2 = list(tail(2, positions))
        return pos1, pos2

    def redrawScreen(self, screen):
        """
        Méthode qui regénère la fenêtre à chaque loop
        """
        screen.blit(self.board, (0, 0))

        # Positions des pions
        for color, positions in self.etat.items():
            for position, piece in positions.items():
                x = (position[0]-1)*(self.screenWidth//8)
                y = self.screenHeight - (position[1])*(self.screenHeight//8)
                screen.blit(self.pieces[color][piece], (x, y))

        # Show les deplacements valides
        if self.cursorPosition in self.etat['white']:
            for move in self.moveGenerator(self.etat, 'white', self.cursorPosition):
                x = (move[0]-1)*(self.screenWidth//8)
                y = self.screenHeight - (move[1])*(self.screenHeight//8)
                self.screen.blit(self.contour, (x, y))
            for attack in self.killGenerator(self.etat, 'white', self.cursorPosition):
                x = (attack[0]-1)*(self.screenWidth//8)
                y = self.screenHeight - (attack[1])*(self.screenHeight//8)
                self.screen.blit(self.circle, (x, y))

        pygame.display.update()

partie = display()
running = True
turn = 'white'
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            partie.clickPosition.append(partie.convert(event.pos))
            try:
                pos1, pos2 = partie.getPos(partie.clickPosition)
                partie.getMove('white', pos1, pos2)
            except ChessError:
                turn = 'white'
                continue
            else:
                turn = 'black'

            if turn == 'black':
                partie.autoplay('black')
                turn = 'white'

    partie.cursorPosition = partie.convert(pygame.mouse.get_pos())

    partie.redrawScreen(partie.screen)

pygame.quit()

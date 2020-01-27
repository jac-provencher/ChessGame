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

    def getPos(self, positions):
        pos1, pos2 = list(tail(2, positions))
        return pos1, pos2

    def draw(self, screen):
        screen.blit(self.board, (0, 0))
        for color, positions in self.etat.items():
            for position, piece in positions.items():
                x = (position[0]-1)*(self.screenWidth//8)
                y = self.screenHeight - (position[1])*(self.screenHeight//8)
                screen.blit(self.pieces[color][piece], (x, y))

        pygame.display.update()

partie = display()
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            position = (event.pos[0]//87+1, 8-event.pos[1]//87)
            partie.clickPosition.append(position)
            try:
                pos1, pos2 = partie.getPos(partie.clickPosition)
                partie.getMove('white', pos1, pos2)
            except ChessError as err:
                print(err)
                continue

    partie.draw(partie.screen)

pygame.quit()

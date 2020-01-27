import pygame
from jeu_echec import ChessError, chess

pygame.init()

class display(chess):

    def __init__(self):
        super().__init__()
        self.screenWidth = self.screenHeight = 696
        self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        pygame.display.set_caption("Échecs")
        self.board = pygame.image.load("board.png")
        self.pieces = {
        'white':
        {
        'P': pygame.image.load("pion_noir.png"),
        'T': pygame.image.load("tour_noir.png"),
        'F': pygame.image.load("fou_noir.png"),
        'Q': pygame.image.load("reine_noir.png"),
        'K': pygame.image.load("roi_noir.png"),
        'C': pygame.image.load("cheval_noir.png")
        },
        'black':
        {
        'P': pygame.image.load("pion_blanc.png"),
        'T': pygame.image.load("tour_blanc.png"),
        'F': pygame.image.load("fou_blanc.png"),
        'Q': pygame.image.load("reine_blanc.png"),
        'K': pygame.image.load("roi_blanc.png"),
        'C': pygame.image.load("cheval_blanc.png")
        }
        }

    def draw(self, screen):
        screen.blit(self.board, (0, 0))
        for color, positions in self.etat.items():
            for position, piece in positions.items():
                x, y = position[0]-1, position[1]-1
                screen.blit(self.pieces[color][piece], (x*87, y*87))

        pygame.display.update()

partie = display()
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    partie.draw(partie.screen)

pygame.quit()

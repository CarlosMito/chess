import sys
# import pygame

from game.surfaces import *
from utils.matrix import *

# Pieces image by User:Cburnett - Own work, CC BY-SA 3.0, https://commons.wikimedia.org/w/index.php?curid=1499806

if __name__ == '__main__':
    # t1 = Board(4)
    # print(t1.board)

    pygame.init()
    pygame.display.set_caption('Chess')
    screen = pygame.display.set_mode((800, 500))

    board = BoardSurface(screen)
    print(board.board)

    while True:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                sys.exit()

        pygame.display.flip()

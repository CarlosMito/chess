import pygame

from game.surfaces import *
from utils.matrix import *

import copy

# Pieces image by User:Cburnett - Own work, CC BY-SA 3.0, https://commons.wikimedia.org/w/index.php?curid=1499806

# TODO: Add Castling
# TODO: Add En Passant


class Phone:
    def __init__(self, OS) -> None:
        self.OS = OS
        self.x = 10
        self.y = 20


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Chess')
    screen = pygame.display.set_mode((800, 500))

    running = True
    board = BoardSurface(screen)
    # print(board)

    while running:
        for event in pygame.event.get():
            # print(event)
            # print(board.next)

            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                board.select(event.pos)

            elif event.type == pygame.MOUSEBUTTONUP:
                board.unselect(event.pos)
                board.update()

            elif event.type == pygame.MOUSEMOTION:
                board.update(event)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    board.reset()
                    board.update()

        pygame.display.flip()

import pygame
from enum import Enum
from game.models.board import Board
from game.models.piece import *


class Colors(Enum):
    WHITE = (240, 240, 240)
    BLUE = (90, 152, 166)
    BLACK = (28, 28, 28)


class BoardSurface(Board):
    def __init__(self, parent, squares, size=50):
        super().__init__(squares=squares)

        self.size = size
        self.surface = pygame.Surface((squares * size, squares * size))

        for i, row in enumerate(self.board.matrix):
            for j, column in enumerate(row):
                pygame.draw.rect(
                    self.surface,
                    Colors.BLUE.value if (i + j) % 2 else Colors.WHITE.value,
                    (size * i, size * j, size, size))

        parent.blit(self.surface, (0, 0))

    def update():
        pass

    pass

import pygame
from pygame.constants import CONTROLLER_BUTTON_MAX
from game.models import *
from enum import Enum


class Colors(Enum):
    WHITE = (240, 240, 240)
    BLACK = (90, 152, 166)


class BoardSurface(Board):
    DEFAULT_SQUARE = 50

    def __init__(self, parent, size, ratio):
        super().__init__(size=size)

        self.ratio = ratio
        self.surface = pygame.Surface(
            (size * BoardSurface.DEFAULT_SQUARE,
             size * BoardSurface.DEFAULT_SQUARE)
        )

        for i, row in enumerate(self._matrix):
            for j, column in enumerate(row):
                self._matrix[i][j] = pygame.draw.rect(
                    self.surface,
                    Colors.BLACK.value if (i + j) % 2 else Colors.WHITE.value,
                    (BoardSurface.DEFAULT_SQUARE * i, BoardSurface.DEFAULT_SQUARE *
                     j, BoardSurface.DEFAULT_SQUARE, BoardSurface.DEFAULT_SQUARE)
                )

        parent.blit(self.surface, (0, 0))

        pass

    def update():
        pass

    pass

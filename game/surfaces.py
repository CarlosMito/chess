import pygame
from enum import Enum
from game.models.board import Board
from game.models.piece import *


class Colors(Enum):
    WHITE = (240, 240, 240)
    BLUE = (90, 152, 166)
    BLACK = (28, 28, 28)


class BoardSurface(Board):
    DEFAULT_SQUARE = 50

    def __init__(self, parent, size, ratio):
        super().__init__(size=size)

        self.ratio = ratio
        self.surface = pygame.Surface(
            (size * BoardSurface.DEFAULT_SQUARE,
             size * BoardSurface.DEFAULT_SQUARE)
        )

        self.pieces = {
            'black': [],
            'white': []
        }

        for i, row in enumerate(self._matrix):
            for j, column in enumerate(row):
                self._matrix[i][j] = pygame.draw.rect(
                    self.surface,
                    Colors.BLUE.value if (i + j) % 2 else Colors.WHITE.value,
                    (BoardSurface.DEFAULT_SQUARE * i, BoardSurface.DEFAULT_SQUARE *
                     j, BoardSurface.DEFAULT_SQUARE, BoardSurface.DEFAULT_SQUARE)
                )

        self.reset()

        parent.blit(self.surface, (0, 0))

    def reset(self):
        for key in self.pieces:
            self.pieces[key].clear()
            for column in range(self._size):
                row = 1 if key == 'white' else 6
                self.pieces[key].append(Pawn(key))

    def update():
        pass

    pass

import os
import pygame
from enum import Enum

from pygame.version import PygameVersion
from game.models.board import Board
from game.models.piece import *


class Colors(Enum):
    WHITE = (250, 250, 250)
    BLUE = (90, 152, 166)
    BLACK = (28, 28, 28)


class BoardSurface(Board):
    def __init__(self, parent, squares=8, size=45):
        super().__init__(squares=squares)

        self.size = size
        self.images = []

        self.surface = pygame.Surface((squares * size, squares * size))

        for i, row in enumerate(self.board.matrix):
            for j, piece in enumerate(row):
                pygame.draw.rect(
                    self.surface,
                    Colors.BLUE.value if (i + j) % 2 else Colors.WHITE.value,
                    (size * i, size * j, size, size))

        for i, row in enumerate(self.board.matrix):
            for j, piece in enumerate(row):
                if piece is not None:
                    image = pygame.image.load(os.path.join(
                        'assets', 'images', 'pieces', piece.color, piece.name + '.svg'))

                    self.images.append(image.get_rect())

                    # O número da linha define a coordenada y da imagem
                    self.surface.blit(image, (j * size, i * size))

        parent.blit(self.surface, (0, 0))

    def update():
        pass

    pass

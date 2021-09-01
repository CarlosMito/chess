import os
import pygame
from enum import Enum
from pygame.display import update
from pygame.draw import rect

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

        self.counter = 0

        self.parent = parent
        self.size = size
        self.images = []

        self.__selected = None

        self.surface = pygame.Surface((squares * size, squares * size))

        self.draw_board()
        self.draw_pieces()

        parent.blit(self.surface, (0, 0))

    def draw_board(self):
        for i in range(self.board.rows):
            for j in range(self.board.columns):
                pygame.draw.rect(
                    self.surface,
                    Colors.BLUE.value if (i + j) % 2 else Colors.WHITE.value,
                    (self.size * i, self.size * j, self.size, self.size))

    def draw_pieces(self):
        for i, row in enumerate(self.board.matrix):
            for j, piece in enumerate(row):
                if piece is not None:
                    image = pygame.image.load(os.path.join(
                        'assets', 'images', 'pieces', piece.color, piece.name + '.svg'))

                    self.images.append(image)

                    # O número da linha define a coordenada y da imagem
                    self.surface.blit(image, (j * self.size, i * self.size))

    def draw_selected(self, position):
        image = pygame.image.load(os.path.join(
            'assets', 'images', 'pieces', self.__selected.color, self.__selected.name + '.svg'))

        size = image.get_size()
        rectangle = image.get_rect()

        centered = (position[0] - size[0] / 2, position[1] - size[1] / 2)

        rectangle.move_ip(centered)
        self.surface.blit(image, rectangle)

    def select(self, position):
        i = position[1] // self.size
        j = position[0] // self.size

        if -1 < i < 8 and -1 < j < 8:
            self.__selected = self.board.matrix[i][j]
            self.board.set_element(i, j, None)

    def unselect(self, position):
        if self.__selected:
            i = position[1] // self.size
            j = position[0] // self.size

            if -1 < i < 8 and -1 < j < 8:
                self.board.set_element(i, j, self.__selected)
                self.__selected = None

    def update(self, event):
        # print(self.counter)
        self.counter += 1

        self.draw_board()
        self.draw_pieces()

        if self.__selected is not None:
            self.draw_selected(event.pos)

        self.parent.blit(self.surface, (0, 0))

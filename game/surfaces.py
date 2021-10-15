import os
import sys
import pygame
from enum import Enum

from game.models.board import Board
from game.models.piece import *

# Ferramenta para debug
IGNORE_TURN = False


class Colors(Enum):
    WHITE = (250, 250, 250)
    BLUE = (90, 150, 170)
    GREEN = (120, 230, 120)
    DARK_GREEN = (30, 120, 30)
    RED = (230, 120, 120)
    DARK_RED = (120, 30, 30)
    BLACK = (30, 30, 30)


class BoardSurface:
    def __init__(self, parent, board, size=45):
        self.parent = parent
        self.board = board
        self.size = size

        self.__selected = None
        self.__possible = []
        self.__images = {
            'white': {},
            'black': {}
        }

        self.surface = pygame.Surface((board.size * size, board.size * size))

        self.load_images()
        self.update()

    def load_images(self):
        for color in self.__images:
            for name in ['pawn', 'rook', 'knight', 'bishop', 'king', 'queen']:
                path = os.path.join('assets', 'images',
                                    'pieces', color, name + '.svg')

                self.__images[color][name] = pygame.image.load(path)

    def draw_board(self):
        for i in range(self.board.size):
            for j in range(self.board.size):
                pygame.draw.rect(
                    self.surface,
                    Colors.BLUE.value if (i + j) % 2 else Colors.WHITE.value,
                    (self.size * i, self.size * j, self.size, self.size))

    def draw_pieces(self):
        for color in self.board.pieces:
            for piece in self.board.pieces[color]:
                if piece.square is not None and piece != self.__selected:
                    # O número da linha define a coordenada y da imagem
                    position = (piece.square[1] * self.size,
                                piece.square[0] * self.size)

                    self.surface.blit(
                        self.__images[color][piece.name], position)

    def draw_selected(self, position):
        if self.__selected:
            image = self.__images[self.__selected.color][self.__selected.name]

            size = image.get_size()
            rectangle = image.get_rect()

            centered = (position[0] - size[0] / 2, position[1] - size[1] / 2)

            rectangle.move_ip(centered)
            self.surface.blit(image, rectangle)

    def select(self, position):
        if self.board.running and not self.__selected:
            i = position[1] // self.size
            j = position[0] // self.size

            if -1 < i < self.board.size and -1 < j < self.board.size:
                piece = self.board.get_piece((i, j))

                # Adiciona as jogadas por turnos
                if piece is not None and (self.board.next == piece.color or IGNORE_TURN):
                    self.__selected = piece
                    self.__possible = piece.possible_moves(self.board.pieces)

                    occupied = {
                        'ally': self.board.get_occupied(piece.color),
                        'enemy': self.board.get_occupied(piece.opponent)
                    }

                    # Remove os movimentos que capturam peças aliadas
                    for move in self.__possible[::]:
                        if move in occupied['ally']:
                            self.__possible.remove(move)

                    # Adiciona os movimentos de captura do peão
                    if type(piece) is Pawn:
                        for square in piece.possible_takes(self.board.pieces):
                            if square in occupied['enemy'] or square == self.board.passant[piece.opponent]:
                                self.__possible.append(square)

    def unselect(self, position):
        if self.__selected:
            i = position[1] // self.size
            j = position[0] // self.size

            if -1 < i < self.board.size and -1 < j < self.board.size:
                if (i, j) in self.__possible:
                    self.board.move(self.__selected, (i, j))

            self.__selected = None

    def draw_moves(self):
        border_width = 2

        if self.__selected:
            for move in self.__possible:
                x = self.size * move[1]
                y = self.size * move[0]

                pygame.draw.rect(
                    self.surface,
                    Colors.DARK_GREEN.value,
                    (x, y, self.size, self.size))

                inner_size = self.size - border_width * 2

                pygame.draw.rect(
                    self.surface,
                    Colors.GREEN.value,
                    (x + border_width, y + border_width, inner_size, inner_size))

    def update(self, event=None):
        self.draw_board()
        self.draw_moves()
        self.draw_pieces()

        if event is not None:
            self.draw_selected(event.pos)

        self.parent.blit(self.surface, (0, 0))

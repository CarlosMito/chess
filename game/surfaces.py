import os
import sys
import pygame
from enum import Enum

from game.models.board import Board
from game.models.piece import *

IGNORE_TURN = True


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

        self.__images = {
            'white': {},
            'black': {}
        }

        self.__counter = 0
        self.__selected = None

        self.__passant = {
            'white': None,
            'black': None,
        }

        self.__check = {
            'white': False,
            'black': False,
        }

        # Utilizado quando o jogador tenta colocar uma peça em um lugar
        # que a mesma não alcança, ou quando sua movimentação causa cheque.
        # Nesses casos, a peça volta para a casa onde ela estava.
        self.__backup = (0, 0)
        self.__possible = []

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
                if piece.square is not None:
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
                    self.__backup = (i, j)
                    self.__selected = piece
                    self.__possible = piece.possible_moves(self.board.pieces)

                    occupied = {
                        'ally': self.board.get_occupied(piece.color),
                        'enemy': self.board.get_occupied(piece.opponent)
                    }

                    for move in self.__possible[::]:
                        if move in occupied['ally']:
                            self.__possible.remove(move)

                    if type(piece) is Pawn:
                        self.__possible += [x for x in piece.possible_takes(self.board.pieces)
                                            if x in occupied['enemy'] or x == self.__passant[piece.opponent]]

                    piece.square = None

    def unselect(self, position):
        if self.__selected:
            i = position[1] // self.size
            j = position[0] // self.size

            if -1 < i < self.board.size and -1 < j < self.board.size:
                piece = self.__selected

                if (i, j) in self.__possible:
                    self.__passant[piece.color] = None

                    direction = 0
                    taken = None

                    # [Move]: En Passant
                    if type(piece) is Pawn:
                        direction = 1 if piece.color == 'white' else -1

                        if abs(self.__backup[0] - i) == 2:
                            self.__passant[piece.color] = (i - direction, j)

                    taken = self.board.get_piece((i - direction, j))

                    if taken is not None:
                        taken.square = None

                    piece.square = (i, j)

                    # Verifica se a movimentação causou cheque
                    if not self.board.is_safe(self.board.kings[piece.color].square, piece.color):
                        piece.square = self.__backup
                        self.__selected = None

                        if taken is not None:
                            taken.square = (i, j)

                        return

                    # [Move]: Castling
                    if type(piece) is King:
                        distance = j - self.__backup[1]

                        if abs(distance) == 2:
                            last = 7 if distance > 0 else 0
                            rook = self.board.get_piece((i, last))
                            rook.square = (i, j - distance // 2)

                    # [Rule]: Pawn Promotion
                    if type(piece) is Pawn:
                        pass

                    # [Rule]: Checkmate
                    if self.board.is_checkmate(piece.opponent):
                        print('CHECKMATE')
                        self.running = False

                    piece.first_move = False
                    self.next = piece.opponent

                else:
                    self.__selected.square = self.__backup

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

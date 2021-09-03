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


class BoardSurface(Board):
    def __init__(self, parent, squares=8, size=45):
        super().__init__(squares=squares)

        self.counter = 0

        self.parent = parent
        self.size = size
        self.images = []

        self.__selected = None

        self.__passant = {
            'white': None,
            'black': None,
        }

        self.__check = {
            'white': False,
            'black': False,
        }

        self.__king = {
            'white': (0, 3),
            'black': (7, 3),
        }

        # Utilizado quando o jogador tenta colocar a peça em um lugar
        # que a mesma não alcança, nesse caso, ela volta para a casa
        # onde ela estava.
        self.__backup = (0, 0)
        self.__possible = []

        self.surface = pygame.Surface((squares * size, squares * size))

        self.update()

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
        if self.__selected:
            image = pygame.image.load(os.path.join(
                'assets', 'images', 'pieces', self.__selected.color, self.__selected.name + '.svg'))

            size = image.get_size()
            rectangle = image.get_rect()

            centered = (position[0] - size[0] / 2, position[1] - size[1] / 2)

            rectangle.move_ip(centered)
            self.surface.blit(image, rectangle)

    def select(self, position):
        if not self.__selected:
            i = position[1] // self.size
            j = position[0] // self.size

            if -1 < i < 8 and -1 < j < 8:
                # Adiciona as jogadas por turnos
                if self.board.matrix[i][j] is not None and (self.next == self.board.matrix[i][j].color or IGNORE_TURN):
                    self.__backup = (i, j)
                    self.__selected = self.board.matrix[i][j]
                    self.board.set_element(i, j, None)

                    piece = self.__selected
                    self.__possible = piece.calculate_moves((i, j), self)

                    for move in self.__possible[::]:
                        if move in self.occupied_squares[piece.color]:
                            self.__possible.remove(move)

                    if type(piece) is Pawn:
                        possible_takes = piece.calculate_takes((i, j), self)

                        for take in possible_takes:
                            if take in self.occupied_squares[piece.opponent] or take == self.__passant[piece.opponent]:
                                self.__possible.append(take)

                    elif type(piece) is King:
                        for square in self.__possible[::]:
                            if not self.is_safe(square, piece.color):
                                self.__possible.remove(square)

    def unselect(self, position):
        if self.__selected:
            piece = self.__selected

            i = position[1] // self.size
            j = position[0] // self.size

            if -1 < i < 8 and -1 < j < 8:
                # [possible_moves] inclui casas fora do tabuleiro.
                # A condição acima faz o tratamento desse problema
                # Estou pensando em alterar a estrutura do código, então
                # qualquer coisa, lembrar de realizar essa condição em outro lugar

                if (i, j) in self.__possible:
                    backup = self.board.matrix[i][j]

                    self.board.set_element(i, j, piece)

                    if type(piece) is King:
                        self.__king[piece.color] = (i, j)

                    if not self.is_safe(self.__king[piece.color], piece.color):
                        self.board.set_element(
                            self.__backup[0],
                            self.__backup[1],
                            self.__selected
                        )

                        self.board.set_element(i, j, backup)
                        self.__selected = None

                        if type(piece) is King:
                            self.__king[piece.color] = (
                                self.__backup[0],
                                self.__backup[1]
                            )

                        return

                    if self.is_checkmate(piece.opponent):
                        print('CHECKMATE!')

                    self.next = piece.opponent
                    piece.first_move = False
                    self.__passant[piece.color] = None

                    # [Move]: En Passant
                    if type(piece) is Pawn:
                        distance = i - self.__backup[0]

                        if abs(distance) == 2:
                            direction = 1 if piece.color == 'white' else -1
                            self.__passant[piece.color] = (i - direction, j)

                        elif (i, j) == self.__passant[piece.opponent]:
                            direction = 1 if piece.opponent == 'white' else -1
                            self.board.set_element(i + direction, j, None)

                        # [Rule]: Pawn Promotion
                        end = 0 if piece.color == 'black' else 7

                        if i == end:
                            # Bastar trocar a peça pelo o que irá se transformar
                            # Terá um problema para ajustar as peças comidas
                            # pelo oponente e algumas outras coisas
                            self.board.set_element(i, j, Queen(piece.color))
                            self.board.matrix[i][j].first_move = False

                    # [Move]: Castling
                    elif type(piece) is King:
                        self.__king[piece.color] = (i, j)
                        distance = j - self.__backup[1]

                        if abs(distance) == 2:
                            last = 7 if distance > 0 else 0
                            rook = self.board.matrix[i][last]
                            self.board.set_element(i, j - distance // 2, rook)
                            self.board.set_element(i, last, None)

                else:
                    self.board.set_element(
                        self.__backup[0],
                        self.__backup[1],
                        piece
                    )

                self.__selected = None

    def draw_moves(self):
        border_width = 1

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

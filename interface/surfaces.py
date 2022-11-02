from turtle import width
import pygame
from models.boards.board import Board
from enum import Enum
from pathlib import Path

# from game.models.board import Board
# from game.models.pieces.piece import *

# Ferramenta para DEBUG
IGNORE_TURN = True


class Colors(Enum):
    WHITE = (250, 250, 250)
    BLUE = (90, 150, 170)
    GREEN = (120, 230, 120)
    RED = (230, 120, 120)
    DARK_GREEN = (30, 120, 30)
    DARK_RED = (120, 30, 30)
    DARK_BLUE = (20, 40, 80)
    GREY = (80, 80, 80, 80)
    BLACK = (30, 30, 30)


class BoardSurface:
    def __init__(self, parent: pygame.Surface, board: Board, size: int = 45):
        self.parent = parent
        self.board = board
        self.size = size

        self.__selected = None
        self.__possible = []
        self.__images = {
            'white': {},
            'black': {}
        }

        self.surface = pygame.Surface((board.size * size, board.size * size), pygame.SRCALPHA)

        self.load_images()
        self.update()

    def load_images(self):
        for color in self.__images:
            for name in ['pawn', 'rook', 'knight', 'bishop', 'king', 'queen']:
                path = Path(f"assets/images/pieces/{color}/{name}.svg")
                self.__images[color][name] = pygame.image.load(path)

    def draw_board(self):
        for i in range(self.board.size):
            for j in range(self.board.size):
                pygame.draw.rect(
                    self.surface,
                    Colors.BLUE.value if (i + j) % 2 else Colors.WHITE.value,
                    (self.size * i, self.size * j, self.size, self.size))

    def draw_pieces(self):
        for piece in self.board.pieces:
            if piece.position is not None and piece != self.__selected:

                # O índice da linha define a coordenada Y da imagem
                coordinate = (piece.position[1] * self.size, piece.position[0] * self.size)

                color = piece.color.name.lower()
                name = piece.__class__.__name__.lower()

                self.surface.blit(self.__images[color][name], coordinate)

    def draw_selected(self, position):
        if self.__selected:
            color = self.__selected.color.name.lower()
            name = self.__selected.__class__.__name__.lower()

            image = self.__images[color][name]

            size = image.get_size()
            rectangle = image.get_rect()

            centered = (position[0] - size[0] / 2, position[1] - size[1] / 2)

            rectangle.move_ip(centered)
            self.surface.blit(image, rectangle)

    def select(self, position):
        if self.board.running and not self.__selected:
            i = position[1] // self.size
            j = position[0] // self.size

            if self.board.is_inside((i, j)):
                piece = self.board.matrix[i][j]

                # Adiciona as jogadas por turnos
                if piece is not None and (self.board.turn == piece.color or IGNORE_TURN):
                    self.__selected = piece
                    self.__possible = piece.get_moves(self.board.pieces, self.board.size)

                    # occupied = {
                    #     'ally': self.board.get_occupied(piece.color),
                    #     'enemy': self.board.get_occupied(piece.opponent)
                    # }

                    # # Remove os movimentos que capturam peças aliadas
                    # for move in self.__possible[::]:
                    #     if move in occupied['ally']:
                    #         self.__possible.remove(move)

                    # # Adiciona os movimentos de captura do peão
                    # if type(piece) is Pawn:
                    #     for square in piece.possible_takes(self.board.pieces):
                    #         if square in occupied['enemy'] or square == self.board.passant[piece.opponent]:
                    #             self.__possible.append(square)

    def unselect(self, position):
        if self.__selected:
            i = position[1] // self.size
            j = position[0] // self.size

            if self.board.is_inside((i, j)):
                if (i, j) in self.__possible:
                    self.board.move(self.__selected, (i, j))

            self.__selected = None

    def draw_moves(self):
        if self.__selected:
            for move in self.__possible:
                x = self.size * move[1]
                y = self.size * move[0]

                center = (x + self.size / 2, y + self.size / 2)
                occupied = [piece.position for piece in self.board.pieces]

                if move in occupied:
                    pygame.draw.rect(
                        self.surface,
                        Colors.DARK_RED.value,
                        (x, y, self.size, self.size)
                    )

                    border = 4

                    pygame.draw.rect(
                        self.surface,
                        Colors.RED.value,
                        (x + border / 2, y + border / 2, self.size - border, self.size - border)
                    )
                else:
                    colors = [Colors.BLACK.value, Colors.WHITE.value] if (move[0] + move[1]) % 2 else [Colors.GREY.value, Colors.WHITE.value]

                    pygame.draw.circle(
                        self.surface,
                        colors[0],
                        center,
                        6
                    )

                    border = 2

                    pygame.draw.circle(
                        self.surface,
                        colors[1],
                        center,
                        6 - border
                    )

    def update(self, event=None):
        self.draw_board()
        self.draw_moves()
        self.draw_pieces()

        if event is not None:
            self.draw_selected(event.pos)

        self.parent.blit(self.surface, (0, 0))

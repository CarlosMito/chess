import os
from enum import Enum
from abc import ABC, abstractmethod, abstractproperty


class Piece(ABC):
    def __init__(self, color, isAlive=True):
        self.name = ''
        self.color = color
        self.isAlive = isAlive

    @abstractmethod
    def possible_moves(self, position, board):
        pass

    def __repr__(self) -> str:
        return self.color[0].upper()


class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.name = 'pawn'
        self.first_move = True

    def possible_moves(self, position, board):
        moves = []

        direction = 1 if self.color == 'white' else -1
        moves.append((position[0] + 1 * direction, position[1]))

        if self.first_move:
            moves.append((position[0] + 2 * direction, position[1]))
            self.first_move = False

        return moves

    def __repr__(self) -> str:
        return super().__repr__() + 'P'


class King(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.name = 'king'

    def possible_moves(self, position, board):
        moves = []
        return moves

    def __repr__(self) -> str:
        return super().__repr__() + 'K'


class Queen(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.name = 'queen'

    def possible_moves(self, position, board):
        moves = []
        return moves

    def __repr__(self) -> str:
        return super().__repr__() + 'Q'


class Knight(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.name = 'knight'

    def possible_moves(self, position, board):
        moves = []
        return moves

    def __repr__(self) -> str:
        return super().__repr__() + 'N'


class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.name = 'bishop'

    def possible_moves(self, position, board):
        moves = []
        return moves

    def __repr__(self) -> str:
        return super().__repr__() + 'B'


class Rook(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.name = 'rook'

    def possible_moves(self, position, board):
        moves = []
        return moves

    def __repr__(self) -> str:
        return super().__repr__() + 'R'

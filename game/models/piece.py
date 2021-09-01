import os
from enum import Enum
from abc import ABC, abstractmethod, abstractproperty


class Piece(ABC):
    def __init__(self, color, isAlive=True):
        self.name = ''
        self.color = color

        self.moves = []
        self.takes = []

    @abstractmethod
    def calculate_actions(self, position, board) -> None:
        pass

    @property
    def opponent(self):
        return 'white' if self.color == 'black' else 'black'

    def __repr__(self) -> str:
        return self.color[0].upper()


class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.name = 'pawn'
        self.first_move = True
        self.direction = 1 if self.color == 'white' else -1

    def calculate_actions(self, position, board) -> None:
        row = position[0] + self.direction

        self.moves = []
        self.takes = []

        occupied_squares = board.occupied_squares[self.opponent] + \
            board.occupied_squares[self.color]

        if (row, position[1]) not in occupied_squares:
            self.moves.append((row, position[1]))

            if self.first_move and (row + self.direction, position[1]) not in occupied_squares:
                self.moves.append((row + self.direction, position[1]))

        self.takes = [(row, position[1] + 1), (row, position[1] - 1)]

    def __repr__(self) -> str:
        return super().__repr__() + 'P'


class King(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.name = 'king'
        self.directions = [(i, j) for i in [1, 0, -1] for j in [1, 0, -1]]

    def calculate_actions(self, position, board) -> None:
        self.moves = []
        self.takes = []

        # TODO: Verificar condição de cheque
        for direction in self.directions:
            if direction != (0, 0):
                square = (position[0] + direction[0],
                          position[1] + direction[1])

                self.takes.append(square)

                if square not in board.occupied_squares[self.color]:
                    self.moves.append(square)

    def __repr__(self) -> str:
        return super().__repr__() + 'K'


class Queen(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.name = 'queen'

    def calculate_actions(self, position, board) -> None:
        self.moves = []
        self.takes = []

        # Debug purposes
        # for i in range(8):
        #     for j in range(8):
        #         moves.append((i, j))

    def __repr__(self) -> str:
        return super().__repr__() + 'Q'


class Knight(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.name = 'knight'
        self.directions = [
            (1, 2), (1, -2), (-1, 2), (-1, -2),
            (2, 1), (2, -1), (-2, 1), (-2, -1)
        ]

    def calculate_actions(self, position, board) -> None:
        self.moves = []
        self.takes = []

        for direction in self.directions:
            move = (position[0] + direction[0], position[1] + direction[1])

            if -1 < move[0] < 8 and -1 < move[1] < 8:
                self.takes.append(move)

                if move not in board.occupied_squares[self.color]:
                    self.moves.append(move)

    def __repr__(self) -> str:
        return super().__repr__() + 'N'


class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.name = 'bishop'

    def calculate_actions(self, position, board) -> None:
        self.moves = []
        self.takes = []

        for direction in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            square = (position[0] + direction[0], position[1] + direction[1])

            while -1 < square[0] < 8 and -1 < square[1] < 8:
                self.takes.append(square)

                if square in board.occupied_squares[self.color]:
                    break

                self.moves.append(square)
                square = (square[0] + direction[0], square[1] + direction[1])

    def __repr__(self) -> str:
        return super().__repr__() + 'B'


class Rook(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.name = 'rook'

    def calculate_actions(self, position, board):
        self.moves = []
        self.takes = []

        for direction in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            square = (position[0] + direction[0], position[1] + direction[1])

            while -1 < square[0] < 8 and -1 < square[1] < 8:
                self.takes.append(square)

                if square in board.occupied_squares[self.color]:
                    break

                self.moves.append(square)
                square = (square[0] + direction[0], square[1] + direction[1])

    def __repr__(self) -> str:
        return super().__repr__() + 'R'

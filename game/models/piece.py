import os
from enum import Enum
from abc import ABC, abstractmethod, abstractproperty


class Piece(ABC):
    def __init__(self, color):
        self.name = ''
        self.color = color
        self.first_move = True
        self.directions = []

    def calculate_moves(self, position, board):
        moves = []

        for direction in self.directions:
            move = (position[0] + direction[0], position[1] + direction[1])

            while -1 < move[0] < 8 and -1 < move[1] < 8:
                moves.append(move)

                if move in board.occupied_squares[self.color] + board.occupied_squares[self.opponent]:
                    break

                move = (move[0] + direction[0], move[1] + direction[1])

        return moves

    @property
    def opponent(self):
        return 'white' if self.color == 'black' else 'black'

    def __repr__(self) -> str:
        return self.color[0].upper()


class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.name = 'pawn'
        self.direction = 1 if self.color == 'white' else -1

    def calculate_moves(self, position, board):
        row = position[0] + self.direction

        moves = []

        occupied_squares = board.occupied_squares[self.opponent] + \
            board.occupied_squares[self.color]

        if (row, position[1]) not in occupied_squares:
            moves.append((row, position[1]))

            if self.first_move and (row + self.direction, position[1]) not in occupied_squares:
                moves.append((row + self.direction, position[1]))

        return moves

    def calculate_takes(self, position, board):
        row = position[0] + self.direction
        return [(row, position[1] + 1), (row, position[1] - 1)]

    def __repr__(self) -> str:
        return super().__repr__() + 'P'


class King(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.name = 'king'
        self.directions = [(i, j) for i in [1, 0, -1] for j in [1, 0, -1]]

    def calculate_moves(self, position, board):
        moves = []

        for direction in self.directions:
            if direction != (0, 0):
                move = (position[0] + direction[0],
                        position[1] + direction[1])

                if -1 < move[0] < 8 and -1 < move[1] < 8:
                    moves.append(move)

        if self.first_move:
            row = 0 if self.color == 'white' else 7
            squares = [(row, 0), (row, 7)]

            for square in squares:
                direction = 2 if square[1] - position[1] > 0 else -2
                piece = board.board.matrix[square[0]][square[1]]

                if type(piece) is Rook and piece.first_move:
                    if position in piece.calculate_moves(square, board):
                        moves.append((row, position[1] + direction))

        return moves

    def __repr__(self) -> str:
        return super().__repr__() + 'K'


class Queen(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.name = 'queen'
        self.directions = [(i, j) for i in [1, 0, -1]
                           for j in [1, 0, -1] if i != 0 or j != 0]

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

    def calculate_moves(self, position, board):
        moves = []

        for direction in self.directions:
            move = (position[0] + direction[0], position[1] + direction[1])

            if -1 < move[0] < 8 and -1 < move[1] < 8:
                moves.append(move)

        return moves

    def __repr__(self) -> str:
        return super().__repr__() + 'N'


class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.name = 'bishop'
        self.directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

    def __repr__(self) -> str:
        return super().__repr__() + 'B'


class Rook(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.name = 'rook'
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    def __repr__(self) -> str:
        return super().__repr__() + 'R'

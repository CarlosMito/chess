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

    def possible_moves(self, position, board):
        moves = []

        direction = 1 if self.color == 'white' else -1

        row = position[0] + 1 * direction

        if (row, position[1] + 1) in board.occupied_squares[self.opponent]:
            moves.append((row, position[1] + 1))

        if (row, position[1] - 1) in board.occupied_squares[self.opponent]:
            moves.append((row, position[1] - 1))

        if (row, position[1]) not in board.occupied_squares[self.opponent] + board.occupied_squares[self.color]:
            moves.append((row, position[1]))

            if self.first_move and (row + direction, position[1]) not in board.occupied_squares[self.opponent] + board.occupied_squares[self.color]:
                moves.append((row + direction, position[1]))

        return moves

    def __repr__(self) -> str:
        return super().__repr__() + 'P'


class King(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.name = 'king'

    def possible_moves(self, position, board):
        moves = []

        # Verificar condição de cheque ao invés de proibir casas ocupadas
        for i in range(-1, 2):
            for j in range(-1, 2):
                square = (position[0] + i, position[1] + j)
                if (i, j) != (0, 0) and (square[0], square[1]) not in board.occupied_squares:
                    moves.append((square[0], square[1]))

        return moves

    def __repr__(self) -> str:
        return super().__repr__() + 'K'


class Queen(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.name = 'queen'

    def possible_moves(self, position, board):
        moves = []

        # Debug purposes
        for i in range(8):
            for j in range(8):
                moves.append((i, j))

        return moves

    def __repr__(self) -> str:
        return super().__repr__() + 'Q'


class Knight(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.name = 'knight'

    def possible_moves(self, position, board):
        moves = []

        directions = [(1, 2), (1, -2), (-1, 2), (-1, -2),
                      (2, 1), (2, -1), (-2, 1), (-2, -1)]

        for direction in directions:
            move = (position[0] + direction[0], position[1] + direction[1])

            if -1 < move[0] < 8 and -1 < move[1] < 8:
                if move not in board.occupied_squares[self.color]:
                    moves.append(move)

        return moves

    def __repr__(self) -> str:
        return super().__repr__() + 'N'


class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.name = 'bishop'

    def possible_moves(self, position, board):
        moves = []

        for direction in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            move = (position[0] + direction[0], position[1] + direction[1])

            while -1 < move[0] < 8 and -1 < move[1] < 8:
                if move in board.occupied_squares[self.color]:
                    break

                moves.append(move)

                if move in board.occupied_squares[self.opponent]:
                    break

                move = (move[0] + direction[0], move[1] + direction[1])

        return moves

    def __repr__(self) -> str:
        return super().__repr__() + 'B'


class Rook(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.name = 'rook'

    def possible_moves(self, position, board):
        moves = []

        for direction in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            move = (position[0] + direction[0], position[1] + direction[1])

            while -1 < move[0] < 8 and -1 < move[1] < 8:
                if move in board.occupied_squares[self.color]:
                    break

                moves.append(move)

                if move in board.occupied_squares[self.opponent]:
                    break

                move = (move[0] + direction[0], move[1] + direction[1])

        return moves

    def __repr__(self) -> str:
        return super().__repr__() + 'R'

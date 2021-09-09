from enum import Enum
from abc import ABC, abstractmethod, abstractproperty


class Piece(ABC):
    def __init__(self, color, square=None):
        self.name = ''
        self.color = color
        self.square = square
        self.first_move = True
        self.directions = []

    def possible_moves(self, others):
        moves = []

        if self.square:
            for direction in self.directions:
                move = (self.square[0] + direction[0],
                        self.square[1] + direction[1])

                blocked = False

                while -1 < move[0] < 8 and -1 < move[1] < 8 and not blocked:
                    moves.append(move)

                    for color in others:
                        for piece in others[color]:
                            if move == piece.square:
                                blocked = True
                                break

                        if blocked:
                            break

                    move = (move[0] + direction[0], move[1] + direction[1])

        return moves

    def possible_takes(self, others):
        return self.possible_moves(others)

    @property
    def opponent(self):
        return 'white' if self.color == 'black' else 'black'

    def __repr__(self) -> str:
        return self.color[0].upper()


class Pawn(Piece):
    def __init__(self, color, square=None):
        super().__init__(color, square)
        self.name = 'pawn'
        self.direction = 1 if self.color == 'white' else -1

    def possible_moves(self, others):
        moves = []

        if self.square:
            row = self.square[0] + self.direction

            occupied = [
                piece.square for color in others for piece in others[color]
            ]

            if (row, self.square[1]) not in occupied:
                moves.append((row, self.square[1]))

                move = (row + self.direction, self.square[1])

                if self.first_move and move not in occupied:
                    moves.append(move)

        return moves

    def possible_takes(self, others):
        if self.square:
            row = self.square[0] + self.direction
            return [(row, self.square[1] + 1), (row, self.square[1] - 1)]
        else:
            return []

    def __repr__(self) -> str:
        return super().__repr__() + 'P'


class Knight(Piece):
    def __init__(self, color, square=None):
        super().__init__(color, square)
        self.name = 'knight'
        self.directions = [
            (1, 2), (1, -2), (-1, 2), (-1, -2),
            (2, 1), (2, -1), (-2, 1), (-2, -1)
        ]

    def possible_moves(self, others):
        moves = []

        if self.square:
            for direction in self.directions:
                move = (self.square[0] + direction[0],
                        self.square[1] + direction[1])

                if -1 < move[0] < 8 and -1 < move[1] < 8:
                    moves.append(move)

        return moves

    def __repr__(self) -> str:
        return super().__repr__() + 'N'


class Queen(Piece):
    def __init__(self, color, square=None):
        super().__init__(color, square)
        self.name = 'queen'
        self.directions = [(i, j) for i in [1, 0, -1]
                           for j in [1, 0, -1] if i != 0 or j != 0]

    def __repr__(self) -> str:
        return super().__repr__() + 'Q'


class Bishop(Piece):
    def __init__(self, color, square=None):
        super().__init__(color, square)
        self.name = 'bishop'
        self.directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

    def __repr__(self) -> str:
        return super().__repr__() + 'B'


class Rook(Piece):
    def __init__(self, color, square=None):
        super().__init__(color, square)
        self.name = 'rook'
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    def __repr__(self) -> str:
        return super().__repr__() + 'R'


class King(Piece):
    def __init__(self, color, square=None):
        super().__init__(color, square)
        self.name = 'king'
        self.directions = [(i, j) for i in [1, 0, -1]
                           for j in [1, 0, -1] if i != 0 or j != 0]

    def possible_moves(self, others):
        moves = []

        for direction in self.directions:
            move = (self.square[0] + direction[0],
                    self.square[1] + direction[1])

            if -1 < move[0] < 8 and -1 < move[1] < 8:
                for enemy in others[self.opponent]:
                    if enemy.square is not None and move in enemy.possible_takes(others):
                        break
                else:
                    moves.append(move)

        # [Move]: Castling
        if self.first_move:
            for ally in others[self.color]:
                if type(ally) is Rook:
                    if ally.first_move and ally.square:
                        direction = 1 if ally.square[1] - \
                            self.square[1] > 0 else -1

                        if self.square in ally.possible_moves(others):
                            move = (self.square[0],
                                    self.square[1] + 2 * direction)
                            moves.append(move)

        return moves

    def possible_takes(self, others):
        takes = []

        for direction in self.directions:
            move = (self.square[0] + direction[0],
                    self.square[1] + direction[1])

            if -1 < move[0] < 8 and -1 < move[1] < 8:
                takes.append(move)

        return takes

    def __repr__(self) -> str:
        return super().__repr__() + 'K'

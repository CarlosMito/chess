from enum import Enum
from abc import ABC, abstractmethod
from utils.position import Position
from typing import Tuple


class Color(Enum):
    WHITE = 1
    BLACK = -1

    def __str__(self):
        return str(self.name)


class Piece(ABC):

    @abstractmethod
    def __init__(self, color: Color, position: Tuple[int, int] | None = None):
        self.color = color
        self.position = position
        self.first_move = True

    @property
    def code(self) -> str:
        piecename = self.__class__.__name__
        colorname = str(self.color)
        return f"{colorname[0]}{piecename[0]}"

    # def possible_moves(self, others):
    #     moves = []

    #     for direction in self.directions:
    #         move = (self.position[0] + direction[0],
    #                 self.position[1] + direction[1])

    #         blocked = False

    #         while -1 < move[0] < 8 and -1 < move[1] < 8 and not blocked:
    #             moves.append(move)

    #             for color in others:
    #                 for piece in others[color]:
    #                     if move == piece.square:
    #                         blocked = True
    #                         break

    #                 if blocked:
    #                     break

    #             move = (move[0] + direction[0], move[1] + direction[1])

    #     return moves

    # def possible_takes(self, others):
    #     return self.possible_moves(others)

    # @property
    # def opponent(self):
    #     return 'white' if self.color == 'black' else 'black'

    def __str__(self) -> str:
        piecename = self.__class__.__name__
        position = self.position or "OUT"
        return f"[{str(self.color)} {piecename.upper()} : {position}]"


class Queen(Piece):
    def __init__(self, color, square=None):
        super().__init__(color, square)
        self.directions = [(i, j) for i in [1, 0, -1]
                           for j in [1, 0, -1] if i != 0 or j != 0]


class King(Piece):
    def __init__(self, color, square=None):
        super().__init__(color, square)
        self.name = 'king'
        self.directions = [(i, j) for i in [1, 0, -1]
                           for j in [1, 0, -1] if i != 0 or j != 0]

    def possible_moves(self, others):
        # TODO: Refatorar a parte de remoção dos movimentos inválidos
        # Está com muito for desnecessário

        moves = []

        # Remove o Tei para verificar possíveis ameaças
        backup = self.square
        self.square = None

        for direction in self.directions:
            move = (backup[0] + direction[0],
                    backup[1] + direction[1])

            if -1 < move[0] < 8 and -1 < move[1] < 8:
                for enemy in others[self.opponent]:
                    if enemy.square is not None and move in enemy.possible_takes(others):
                        break
                else:
                    moves.append(move)

        self.square = backup

        in_check = False

        for enemy in others[self.opponent]:
            if enemy.square is not None and self.square in enemy.possible_takes(others):
                in_check = True
                break

        # [Move]: Castling
        # O Rei não pode estar em cheque no castling
        if self.first_move and not in_check:
            for ally in others[self.color]:
                if type(ally) is Rook:
                    if ally.first_move and ally.position:
                        direction = 1 if ally.position[1] - \
                            self.square[1] > 0 else -1

                        if self.square in ally.possible_moves(others):
                            move = (self.square[0],
                                    self.square[1] + 2 * direction)

                            # Remove o movimento caso o Rei fique em cheque
                            for enemy in others[self.opponent]:
                                if enemy.square is not None and move in enemy.possible_takes(others):
                                    break
                            else:
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

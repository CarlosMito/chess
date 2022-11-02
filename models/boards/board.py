from typing import List, Tuple
from models.pieces.piece import Piece
from utils.exceptions import *
from abc import ABC, abstractmethod


class Board(ABC):

    @abstractmethod
    def __init__(self, size):
        self.size: int = size
        self.pieces: List[Piece] = []
        self.running: bool = False
        self.turn: int = 0

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def clear(self):
        pass

    @property
    def matrix(self) -> List[List[Piece | None]]:
        matrix = [[None for _ in range(self.size)] for _ in range(self.size)]

        for piece in self.pieces:
            if position := piece.position:
                matrix[position[0]][position[1]] = piece

        return matrix

    def is_inside(self, coordinate: Tuple[int, int]):
        return (-1 < coordinate[0] < self.size) and (-1 < coordinate[1] < self.size)

    def move(self, piece: Piece, coordinate: Tuple[int, int]):

        for other in self.pieces:
            if other.position == coordinate:
                other.position = None

        piece.position = coordinate
        piece.first_move = False

    def __str__(self):

        rows = []

        for row in self.matrix[::-1]:
            codes = list(map(lambda e: "  " if e is None else e.code, row))
            rows.append(f"[ {' '.join(codes)} ]")

        return "\n".join(rows)


# class Board:
#     def __init__(self, size=8):
#         self.size = size

#         self.running = True
#         self.next = 'white'

#         self.pieces = {
#             'black': [],
#             'white': []
#         }

#         self.kings = {
#             'black': None,
#             'white': None
#         }

#         self.passant = {
#             'white': None,
#             'black': None,
#         }

#         self.history = []

#         self.reset()

#     def reset(self):
#         self.next = 'white'
#         self.running = True

#         self.passant['white'] = None
#         self.passant['black'] = None

#         self.history.clear()

#         for color in self.pieces:
#             self.pieces[color].clear()

#             row = 0 if color == 'white' else self.size - 1

#             king = King(color, (row, self.size // 2 - 1))
#             self.kings[color] = king

#             self.pieces[color].append(king)
#             self.pieces[color].append(Queen(color, (row, self.size // 2)))

#             column = 0

#             for j in [1, -1]:
#                 self.pieces[color].append(Rook(color, (row, column)))
#                 self.pieces[color].append(Knight(color, (row, column + j)))
#                 self.pieces[color].append(Bishop(color, (row, column + 2 * j)))
#                 column = self.size - 1

#             row += 1 if color == 'white' else -1

#             for column in range(self.size):
#                 self.pieces[color].append(Pawn(color, (row, column)))

#     def to_file(self, index):
#         files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
#         return files[-(index + 1)]

#     def to_rank(self, index):
#         return str(index + 1)

#     def save_move(self, piece, square, additional):
#         if additional['castling']:
#             move = 'O-O-O' if square[1] > 3 else 'O-O'
#             self.history.append(move)
#             print(move)
#             return

#         move = ''

#         # Adicionar desambiguação aqui

#         if type(piece) is not Pawn:
#             move += str(piece)[1]

#         move += additional['taken']
#         move += self.to_file(square[1]) + self.to_rank(square[0])
#         move += additional['passant']
#         move += additional['promotion']

#         self.history.append(move)
#         print(move)

#     def move(self, piece, square):
#         additional = {
#             x: '' for x in ['castling', 'taken', 'passant', 'promotion']
#         }

#         backup = piece.square
#         self.passant[piece.color] = None

#         passing = 0
#         taken = None

#         # [Move]: En Passant
#         if type(piece) is Pawn:
#             direction = 1 if piece.color == 'white' else -1

#             if abs(backup[0] - square[0]) == 2:
#                 self.passant[piece.color] = (square[0] - direction, square[1])

#             # square[1] != backup[1]
#             elif square == self.passant[piece.opponent]:
#                 passing = direction
#                 additional['passant'] = 'e.p.'

#         taken = self.get_piece((square[0] - passing, square[1]))

#         if taken is not None:
#             taken.square = None
#             additional['taken'] = 'x'

#         piece.position = square

#         # Verifica se a movimentação causou cheque
#         if not self.is_safe(self.kings[piece.color].square, piece.color):
#             piece.position = backup

#             if taken is not None:
#                 taken.square = square

#             return

#         # [Move]: Castling
#         if type(piece) is King:
#             distance = square[1] - backup[1]

#             if abs(distance) == 2:
#                 last = 7 if distance > 0 else 0
#                 rook = self.get_piece((square[0], last))
#                 rook.square = (square[0], square[1] - distance // 2)
#                 additional['castling'] = True

#         # [Rule]: Pawn Promotion
#         if type(piece) is Pawn:
#             promotion_row = 0 if piece.color == 'black' else 7

#             if square[0] == promotion_row:
#                 promotion = input('Choose a type [Q, B, N, R]: ')

#                 self.pieces[piece.color].remove(piece)

#                 chessmen = {
#                     'Q': Queen,
#                     'B': Bishop,
#                     'N': Knight,
#                     'R': Rook
#                 }

#                 promoted = chessmen[promotion](piece.color, piece.position)
#                 promoted.first_move = False

#                 self.pieces[piece.color].append(promoted)
#                 additional['promotion'] = '=' + str(promoted)[1]

#         self.save_move(piece, square, additional)

#         # [Rule]: Checkmate
#         if self.is_checkmate(piece.opponent):
#             print('CHECKMATE')
#             self.running = False

#         piece.first_move = False
#         self.next = piece.opponent

#     # [color] Cor das peças ocupantes
#     def get_occupied(self, color=None):
#         squares = []

#         for piece_color in self.pieces:
#             if color == None or piece_color == color:
#                 for piece in self.pieces[piece_color]:
#                     squares.append(piece.square)

#         return squares

#     def get_piece(self, square):
#         for color in self.pieces:
#             for piece in self.pieces[color]:
#                 if piece.square == square:
#                     return piece

#         return None

#     # [color] Cor das peças atacantes
#     def get_attackers(self, target, color):
#         attackers = []

#         for piece in self.pieces[color]:
#             if target in piece.possible_takes(self.pieces):
#                 attackers.append(piece)

#         return attackers

#     # [color] = Cor da peça em ameaça
#     def is_safe(self, square, color) -> bool:
#         opponent = 'white' if color == 'black' else 'black'

#         for piece in self.pieces[opponent]:
#             if square in piece.possible_takes(self.pieces):
#                 return False

#         return True

#     # [color] Cor de quem está tomando cheque mate
#     def is_checkmate(self, color) -> bool:
#         king = self.kings[color]

#         # Verifica se o Rei está seguro
#         if self.is_safe(king.square, color):
#             return False

#         occupied = self.get_occupied(color)

#         # Verifica se o Rei possui casas de fuga
#         moves = king.possible_moves(self.pieces)

#         for move in moves[::]:
#             if move in occupied or not self.is_safe(move, color):
#                 moves.remove(move)

#         if len(moves) > 0:
#             return False

#         # Caso haja 2 fontes de ameaça, não é possível se defender
#         attackers = self.get_attackers(king.square, king.opponent)

#         if len(attackers) > 1:
#             return True

#         # Observação: Não tem como um Rei causar cheque no Rei inimigo
#         defenders = self.get_attackers(attackers[0].square, king.color)

#         # Verifica se é possível capturar a peça atacante
#         for defender in defenders:
#             # Quando o defensor sair, o Rei não pode ficar em cheque
#             if type(defender) is not King:
#                 auxiliar = defender.square

#                 defender.square = attackers[0].square
#                 attackers[0].square = None

#                 king_is_safe = self.is_safe(king.square, king.color)

#                 attackers[0].square = defender.square
#                 defender.square = auxiliar

#                 if king_is_safe:
#                     return False

#         # Verifica se é possível entrar na frente da peça atacante
#         if type(attackers[0]) in [Rook, Bishop, Queen]:
#             vector = (king.square[0] - attackers[0].square[0],
#                       king.square[1] - attackers[0].square[1])

#             direction = (
#                 1 if vector[0] > 0 else -1 if vector[0] < 0 else 0,
#                 1 if vector[1] > 0 else -1 if vector[1] < 0 else 0,
#             )

#             block_square = (attackers[0].square[0] + direction[0],
#                             attackers[0].square[1] + direction[1])

#             while -1 < block_square[0] < 7 and -1 < block_square[1] < 7 and block_square != king.square:
#                 blockers = self.get_blockers(block_square, king.color)

#                 for blocker in blockers:
#                     auxiliar = blocker.square
#                     blocker.square = block_square
#                     king_is_safe = self.is_safe(king.square, king.color)
#                     blocker.square = auxiliar

#                     if king_is_safe:
#                         return False

#                 block_square = (block_square[0] + direction[0],
#                                 block_square[1] + direction[1])

#         return True

#     # [color] Cor das peças bloqueadoras
#     def get_blockers(self, target, color):
#         blockers = []

#         for blocker in self.pieces[color]:
#             if target in blocker.possible_moves(self.pieces):
#                 blockers.append(blocker)

#         return blockers

#     def __repr__(self):
#         board = Matrix(self.size, self.size)

#         for color in self.pieces:
#             for piece in self.pieces[color]:
#                 if piece.square:
#                     board.set_element(piece.square, piece)

#         string = ''

#         for row in board.matrix:
#             string += '['

#             for piece in row:
#                 string += f' {"  " if piece is None else str(piece)} '

#             string += ']\n'

#         return string

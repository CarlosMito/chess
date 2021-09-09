from utils.matrix import Matrix
from utils.exceptions import *
from game.models.piece import *


'''
Adicionar um enum player.black = -1 e player.white = 1
Adicionar extensão do enum para string
Verificar se é possível definir uma enum a partir de seu value, exemplo
-1 * -1 = 1 e definir um enum 1 que seria player.white
'''


class Board:
    def __init__(self, size=8):
        self.size = size

        self.running = True
        self.next = 'white'

        self.pieces = {
            'black': [],
            'white': []
        }

        self.kings = {
            'black': None,
            'white': None
        }

        self.reset()

    def reset(self):
        self.next = 'white'
        self.running = True

        for color in self.pieces:
            self.pieces[color].clear()

            row = 0 if color == 'white' else self.size - 1

            king = King(color, (row, self.size // 2 - 1))
            self.kings[color] = king

            self.pieces[color].append(king)
            self.pieces[color].append(Queen(color, (row, self.size // 2)))

            column = 0

            for j in [1, -1]:
                self.pieces[color].append(Rook(color, (row, column)))
                self.pieces[color].append(Knight(color, (row, column + j)))
                self.pieces[color].append(Bishop(color, (row, column + 2 * j)))
                column = self.size - 1

            row += 1 if color == 'white' else -1

            for column in range(self.size):
                self.pieces[color].append(Pawn(color, (row, column)))

    # [color] Cor das peças ocupantes
    def get_occupied(self, color=None):
        squares = []

        for piece_color in self.pieces:
            if color == None or piece_color == color:
                for piece in self.pieces[piece_color]:
                    squares.append(piece.square)

        return squares

    def get_piece(self, square):
        for color in self.pieces:
            for piece in self.pieces[color]:
                if piece.square == square:
                    return piece

        return None

    # [color] Cor das peças atacantes
    def get_attackers(self, target, color):
        attackers = []

        for piece in self.pieces[color]:
            if target in piece.possible_takes(self.pieces):
                attackers.append(piece)

        return attackers

    # [color] = Cor do atacado
    def is_safe(self, square, color) -> bool:
        opponent = 'white' if color == 'black' else 'black'

        for piece in self.pieces[opponent]:
            if square in piece.possible_takes(self.pieces):
                return False

        return True

    # [color] Cor de quem está tomando cheque mate
    # [square] Casa do Rei para o cheque-mate
    def is_checkmate(self, color) -> bool:
        king = self.kings[color]

        # Verifica se o Rei está seguro
        if self.is_safe(king.square, color):
            return False

        occupied = self.get_occupied(color)

        # Verifica se o Rei possui casas de fuga
        moves = king.possible_moves(self.pieces)

        for move in moves[::]:
            if move in occupied:
                moves.remove(move)

        if len(moves) > 0:
            return False

        # Caso haja 2 fontes de ameaça, não é possível se defender
        attackers = self.get_attackers(king.square, king.opponent)

        if len(attackers) > 1:
            return True

        # Observação: Não tem como um Rei causar cheque no Rei inimigo
        defenders = self.get_attackers(attackers[0].square, king.color)

        # Verifica se é possível capturar a peça atacante
        for defender in defenders:
            # Quando o defensor sair, o Rei não pode ficar em cheque
            if type(defender) is not King:
                auxiliar = defender.square

                defender.square = attackers[0].square
                attackers[0].square = None

                king_is_safe = self.is_safe(king.square, king.color)

                attackers[0].square = defender.square
                defender.square = auxiliar

                if king_is_safe:
                    return False

        # Verifica se é possível entrar na frente da peça atacante
        if type(attackers[0]) in [Rook, Bishop, Queen]:
            vector = (king.square[0] - attackers[0].square[0],
                      king.square[1] - attackers[0].square[1])

            direction = (
                1 if vector[0] > 0 else -1 if vector[0] < 0 else 0,
                1 if vector[1] > 0 else -1 if vector[1] < 0 else 0,
            )

            block_square = (attackers[0].square[0] + direction[0],
                            attackers[0].square[1] + direction[1])

            while -1 < block_square[0] < 7 and 1 < block_square[1] < 7 and block_square != king.square:
                blockers = self.get_blockers(block_square, king.color)

                for blocker in blockers:
                    auxiliar = blocker.square
                    blocker.square = block_square
                    king_is_safe = self.is_safe(king.square, king.color)
                    blocker.square = auxiliar

                    if king_is_safe:
                        return False

                block_square = (block_square[0] + direction[0],
                                block_square[1] + direction[1])

        return True

    # [color] Cor das peças bloqueadoras
    def get_blockers(self, target, color):
        blockers = []

        for blocker in self.pieces[color]:
            if target in blocker.possible_moves(self.pieces):
                blockers.append(blocker)

        return blockers

    def __repr__(self):
        board = Matrix(self.size, self.size)

        for color in self.pieces:
            for piece in self.pieces[color]:
                if piece.square:
                    board.set_element(piece.square, piece)

        string = ''

        for row in board.matrix:
            string += '['

            for piece in row:
                string += f' {"  " if piece is None else str(piece)} '

            string += ']\n'

        return string

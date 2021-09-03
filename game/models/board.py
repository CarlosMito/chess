from utils.matrix import Matrix
from utils.exceptions import *
from game.models.piece import *
import copy


'''
Adicionar um enum player.black = -1 e player.white = 1
Adicionar extensão do enum para string
Verificar se é possível definir uma enum a partir de seu value, exemplo
-1 * -1 = 1 e definir um enum 1 que seria player.white
'''

# TODO: Eu movi um peão que causou cheque, isso não deveria ser permitido


class Board:
    def __init__(self, squares=8):
        if squares < 4:
            raise TooFewBoardSquares

        self.__squares = squares
        self.__board = Matrix(squares, squares)

        self.next = 'white'

        # Isso aqui tá meio inútil
        self.pieces = {
            'black': [],
            'white': []
        }

        self.reset()

    def reset(self):
        self.__board = Matrix(self.__squares, self.__squares)

        for color in self.pieces:
            self.pieces[color].clear()
            row = 0 if color == 'white' else self.__squares - 1

            king = King(color)
            queen = Queen(color)

            self.__board.set_element(row, self.squares // 2 - 1, king)
            self.__board.set_element(row, self.squares // 2, queen)
            self.pieces[color].append(king)
            self.pieces[color].append(queen)

            # Reescrever isso depois
            r1 = Rook(color)
            r2 = Rook(color)
            b1 = Bishop(color)
            b2 = Bishop(color)
            n1 = Knight(color)
            n2 = Knight(color)

            self.__board.set_element(row, 0, r1)
            self.__board.set_element(row, 7, r2)
            self.__board.set_element(row, 1, n1)
            self.__board.set_element(row, 6, n2)
            self.__board.set_element(row, 2, b1)
            self.__board.set_element(row, 5, b2)

            self.pieces[color].extend([r1, r2, b1, b2, n1, n2])

            row += 1 if color == 'white' else -1

            for column in range(self.__squares):
                piece = Pawn(color)
                self.__board.set_element(row, column, piece)
                self.pieces[color].append(piece)

            self.next = 'white'

    @property
    def board(self):
        return self.__board

    @property
    def squares(self):
        return self.__squares

    @squares.setter
    def squares(self, squares):
        if (self.__squares < 4):
            raise TooFewBoardSquares

        self.__board.rows = squares
        self.__board.columns = squares

    @property
    def occupied_squares(self):
        squares = {
            'black': [],
            'white': []
        }

        for i, row in enumerate(self.__board.matrix):
            for j, piece in enumerate(row):
                if piece is not None:
                    squares[piece.color].append((i, j))

        return squares

    # [color] = Cor do atacado
    def is_safe(self, square, color) -> bool:
        opponent = 'white' if color == 'black' else 'black'

        for position in self.occupied_squares[opponent]:
            if square != position:
                piece = self.board.matrix[position[0]][position[1]]

                if type(piece) is Pawn:
                    if square in piece.calculate_takes(position, self):
                        return False

                elif square in piece.calculate_moves(position, self):
                    return False

        return True

    # [color] Cor de quem está tomando cheque mate
    # [square] Casa do Rei para o cheque-mate
    def is_checkmate(self, color) -> bool:
        king = king_square = None

        for square in self.occupied_squares[color]:
            piece = self.board.matrix[square[0]][square[1]]
            if type(piece) is King:
                king_square = square
                king = piece
                break
        else:
            # Não encontrou o Rei no tabuleiro
            return True

        # Verifica se o Rei está em cheque
        if self.is_safe(king_square, color):
            return False

        print('King in check')

        # Verifica se o Rei possui casas de fuga
        king_moves = king.calculate_moves(square, self)

        for move in king_moves[::]:
            if move in self.occupied_squares[king.color]:
                king_moves.remove(move)

        for move in king_moves[::]:
            if not self.is_safe(move, piece.color):
                king_moves.remove(move)

        if len(king_moves) > 0:
            return False

        print('King can\'t move')

        # Caso haja 2 fontes de ameaça, não é possível se defender
        attackers = self.get_attackers(king_square, king.opponent)

        if len(attackers) > 1:
            return True

        print('Only one attacker')

        attacker = attackers[0]
        attacker_piece = self.board.matrix[attacker[0]][attacker[1]]

        # Observação: Não tem como um Rei causar cheque no Rei inimigo
        defenders = self.get_attackers(attackers[0], king.color)

        # Verifica se é possível capturar a peça atacante
        for defender in defenders:
            # Quando o defensor sair, o Rei não pode ficar em cheque
            piece = self.board.matrix[defender[0]][defender[1]]

            if type(piece) is not King:
                self.board.set_element(defender[0], defender[1], None)
                self.board.set_element(attacker[0], attacker[1], piece)

                king_safe = self.is_safe(king_square, king.color)

                # Volta o tabuleiro ao normal
                self.board.set_element(defender[0], defender[1], piece)
                self.board.set_element(
                    attacker[0], attacker[1], attacker_piece)

                if king_safe:
                    return False

        print('Can\'t capture attacker')

        # Verifica se é possível entrar na frente da peça atacante
        if type(attacker_piece) in [Rook, Bishop, Queen]:
            vector = (king_square[0] - attacker[0],
                      king_square[1] - attacker[1])

            direction = (
                1 if vector[0] > 0 else -1 if vector[0] < 0 else 0,
                1 if vector[1] > 0 else -1 if vector[1] < 0 else 0,
            )

            block_square = (attacker[0] + direction[0],
                            attacker[1] + direction[1])

            while -1 < block_square[0] < 7 and 1 < block_square[1] < 7 and block_square != king_square:
                blockers = self.get_blockers(block_square, king.color)

                for blocker in blockers:
                    # Quando o defensor sair, o Rei não pode ficar em cheque
                    piece = self.board.matrix[blocker[0]][blocker[1]]

                    if type(piece) is King:
                        continue

                    self.board.set_element(blocker[0], blocker[1], None)
                    self.board.set_element(
                        block_square[0],
                        block_square[1],
                        piece
                    )

                    king_safe = self.is_safe(king_square, king.color)

                    # Volta o tabuleiro ao normal
                    self.board.set_element(blocker[0], blocker[1], piece)
                    self.board.set_element(
                        block_square[0],
                        block_square[1],
                        None
                    )

                    if king_safe:
                        return False

                block_square = (block_square[0] + direction[0],
                                block_square[1] + direction[1])

        print('Can\'t defend king')

        return True

    # [color] Cor das peças atacantes
    def get_attackers(self, target, color):
        attackers = []

        for square in self.occupied_squares[color]:
            piece = self.board.matrix[square[0]][square[1]]
            takes = piece.calculate_moves if type(
                piece) is not Pawn else piece.calculate_takes

            if target in takes(square, self):
                attackers.append(square)

        return attackers

    # [color] Cor das peças bloqueadoras
    def get_blockers(self, target, color):
        blockers = []

        for square in self.occupied_squares[color]:
            piece = self.board.matrix[square[0]][square[1]]

            if target in piece.calculate_moves(square, self):
                blockers.append(square)

        return blockers

    def __repr__(self):
        string = ''

        for row in self.board.matrix:
            string += '['

            for piece in row:
                string += f' {"  " if piece is None else str(piece)} '

            string += ']\n'

        return string

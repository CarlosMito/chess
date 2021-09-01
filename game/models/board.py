from utils.matrix import Matrix
from utils.exceptions import *
from game.models.piece import *


class Board:
    def __init__(self, squares=8):
        if squares < 4:
            raise TooFewBoardSquares

        self.__squares = squares
        self.__board = Matrix(squares, squares)

        self.pieces = {
            'black': [],
            'white': []
        }

        self.reset()

    def reset(self):
        for color in self.pieces:
            self.pieces[color].clear()
            row = 0 if color == 'white' else self.__squares - 1

            king = King(color)
            queen = Queen(color)

            self.__board.set_element(row, self.squares // 2 - 1, king)
            self.__board.set_element(row, self.squares // 2, queen)
            self.pieces[color].append(king)
            self.pieces[color].append(queen)

            # Somente para testes
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

    def __repr__(self):
        string = ''

        for row in self.board.matrix:
            string += '['

            for piece in row:
                string += f' {"  " if piece is None else str(piece)} '

            string += ']\n'

        return string

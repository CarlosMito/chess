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
        for key in self.pieces:
            self.pieces[key].clear()
            for column in range(self.__squares):
                row = 1 if key == 'white' else self.__squares - 2
                self.__board.set_element(row, column, Pawn(key))

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

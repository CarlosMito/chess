from game.exceptions import *


class Board:
    def __init__(self, size=8):
        self.__size = size
        self._matrix = [[None for _ in range(self.__size)]
                        for _ in range(self.__size)]

    def get_matrix(self):
        return self._matrix

    def set_matrix(self, matrix):
        size = len(matrix)

        if size == 0:
            raise NonSquareMatrix

        for row in matrix:
            if len(row) != size:
                raise NonSquareMatrix

        self._matrix = matrix
        self.__size = size

    def __repr__(self):
        string = ''

        for row in self._matrix:
            string += str(row) + '\n'

        return string

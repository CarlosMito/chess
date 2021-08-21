from game.exceptions import *


class Board:
    def __init__(self, size=8):
        self.__size = size
        self.__matrix = [[None for _ in range(self.__size)]
                         for _ in range(self.__size)]

        self._teste = 10

    def get_matrix(self):
        return self.__matrix

    def set_matrix(self, matrix):
        size = len(matrix)

        if size == 0:
            raise NonSquareMatrix

        for row in matrix:
            if len(row) != size:
                raise NonSquareMatrix

        self.__matrix = matrix
        self.__size = size

    def __repr__(self):
        string = ''

        for row in self.__matrix:
            string += str(row) + '\n'

        return string

from utils.matrix import Matrix


class Board:
    def __init__(self, size=8):
        self._size = size
        self._matrix = Matrix(size, size)

    def get_size(self):
        return self._size

    def set_size(self, size):
        self._matrix = Matrix(size, size)

    def __repr__(self):
        string = ''

        for row in self._matrix:
            string += str(row) + '\n'

        return string

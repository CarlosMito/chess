from .piece import Piece


class Rook(Piece):
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    def __init__(self, color, square=None):
        super().__init__(color, square)

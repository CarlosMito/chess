from .piece import Piece


class Rook(Piece):

    movements = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    infinite = True
    jumps = False

    def __init__(self, color, square=None):
        super().__init__(color, square)

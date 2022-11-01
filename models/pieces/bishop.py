from .piece import Piece


class Bishop(Piece):

    movements = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    infinite = True
    jumps = False

    def __init__(self, color, square=None):
        super().__init__(color, square)

from .piece import Piece
from .king import King


class Queen(Piece):

    movements = King.movements
    infinite = True
    jumps = False

    def __init__(self, color, square=None):
        super().__init__(color, square)

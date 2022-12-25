from .piece import Piece
from .bishop import Bishop
from .rook import Rook


class King(Piece):

    movements = Rook.movements + Bishop.movements
    infinite = False

    def __init__(self, color, square=None):
        super().__init__(color, square)

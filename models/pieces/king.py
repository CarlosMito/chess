from .piece import Piece
from .bishop import Bishop
from .rook import Rook


class King(Piece):
    """
    The king's movement will be restricted by the [ChessBoard], which is responsible for
    calculating the check state. So when any piece piece moves, king included, and the
    resulting state is a check for the color that moved, the movement will be canceled.
    """

    movements = Rook.movements + Bishop.movements
    infinite = False

    def __init__(self, color, square=None):
        super().__init__(color, square)

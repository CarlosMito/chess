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

    def get_moves(self, board):
        moves = super().get_moves(board)

        if self.first_move:
            allies = [other for other in board.pieces if other.color == self.color]
            rooks = [piece for piece in allies if isinstance(piece, Rook)]
            occupied_squares = [other.position for other in board.pieces]

            for rook in rooks:
                direction = 1 if rook.position[1] - self.position[1] > 0 else -1
                y_range = range(rook.position[1] - direction, self.position[1], -direction)
                squares_between = [(self.position[0], y) for y in y_range]
                blocked = False

                for square in squares_between:
                    if square in occupied_squares:
                        blocked = True

                if rook.first_move and not blocked:
                    square = (self.position[0], self.position[1] + direction * 2)
                    moves.append(square)

        return moves

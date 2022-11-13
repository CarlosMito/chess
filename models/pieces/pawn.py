from typing import List
from .piece import Piece


class Pawn(Piece):

    movements = [(1, 0)]
    infinite = False
    jumps = False

    def __init__(self, color, position=None):
        super().__init__(color, position)

    def get_moves(self, board):
        """
        Params
        ------

        - pieces : A list of all the other pieces on the board.
        - limit : Corresponds to the board size the piece is on.
        """

        moves = []

        if self.position is None:
            return moves

        allies = [other.position for other in board.pieces if other.color == self.color]
        enemies = [other.position for other in board.pieces if other.color != self.color]

        direction = Pawn.movements[0][0] * self.color.value

        for i in [1, 2] if self.first_move else [1]:
            square = (self.position[0] + direction * i, self.position[1])

            if board.is_inside(square):
                if square not in allies and square not in enemies:
                    moves.append(square)
                    continue

                break

        for attack in [-1, 1]:
            square = (self.position[0] + direction, self.position[1] + attack)

            if board.is_inside(square):

                en_passant = False

                if board.en_passant["square"] is not None:
                    epcolor = self.color.opposite == board.en_passant["color"]
                    epsquare = square == board.en_passant["square"]
                    en_passant = epcolor and epsquare

                if square in enemies or en_passant:
                    moves.append(square)

        return moves

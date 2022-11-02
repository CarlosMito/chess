from typing import List
from .piece import Piece


class Pawn(Piece):

    movements = [(1, 0)]
    infinite = False
    jumps = False

    def __init__(self, color, position=None):
        super().__init__(color, position)
        # self.direction = self.color.value

    def get_moves(self, pieces: List[Piece], limit: int = 8):
        """
        Params
        ------

        - pieces : A list of all the other pieces on the board.
        - limit : Corresponds to the board size the piece is on.
        """

        moves = []

        allies = [other.position for other in pieces if other.color == self.color]
        enemies = [other.position for other in pieces if other.color != self.color]

        direction = Pawn.movements[0][0] * self.color.value

        square = (self.position[0] + direction, self.position[1])

        if -1 < square[0] < limit and -1 < square[1] < limit:
            if square not in allies and square not in enemies:
                moves.append(square)

        if self.first_move and moves:
            square = (self.position[0] + 2 * direction, self.position[1])

            if -1 < square[0] < limit and -1 < square[1] < limit:
                if square not in allies and square not in enemies:
                    moves.append(square)

        return moves

    # def possible_moves(self, others):
    #     moves = []

    #     if self.position:
    #         row = self.position[0] + self.direction

    #         occupied = [
    #             piece.square for color in others for piece in others[color]
    #         ]

    #         if (row, self.position[1]) not in occupied:
    #             moves.append((row, self.position[1]))

    #             move = (row + self.direction, self.position[1])

    #             if self.first_move and move not in occupied:
    #                 moves.append(move)

    #     return moves

    def possible_takes(self, others):
        if self.position:
            row = self.position[0] + self.direction
            return [(row, self.position[1] + 1), (row, self.position[1] - 1)]
        else:
            return []

    # def __str__(self) -> str:
    #     piece = self.__class__.__name__
    #     return f"[{super().__str__()} {piece.upper()} - {1}]"

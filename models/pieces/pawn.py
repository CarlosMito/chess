from .piece import Piece


class Pawn(Piece):
    def __init__(self, color, position=None):
        super().__init__(color, position)
        self.direction = self.color.value

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

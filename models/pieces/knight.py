from .piece import Piece


class Knight(Piece):
    def __init__(self, color, square=None):
        super().__init__(color, square)
        self.name = 'knight'
        self.directions = [
            (1, 2), (1, -2), (-1, 2), (-1, -2),
            (2, 1), (2, -1), (-2, 1), (-2, -1)
        ]

    def possible_moves(self, others):
        moves = []

        if self.position:
            for direction in self.directions:
                move = (self.position[0] + direction[0],
                        self.position[1] + direction[1])

                if -1 < move[0] < 8 and -1 < move[1] < 8:
                    moves.append(move)

        return moves

    def __repr__(self) -> str:
        return super().__repr__() + 'N'

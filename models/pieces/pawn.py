from models.pieces.piece import Piece


class Pawn(Piece):
    def __init__(self, color, square=None):
        super().__init__(color, square)
        self.name = 'pawn'
        self.direction = 1 if self.color == 'white' else -1

    def possible_moves(self, others):
        moves = []

        if self.position:
            row = self.position[0] + self.direction

            occupied = [
                piece.square for color in others for piece in others[color]
            ]

            if (row, self.position[1]) not in occupied:
                moves.append((row, self.position[1]))

                move = (row + self.direction, self.position[1])

                if self.first_move and move not in occupied:
                    moves.append(move)

        return moves

    def possible_takes(self, others):
        if self.position:
            row = self.position[0] + self.direction
            return [(row, self.position[1] + 1), (row, self.position[1] - 1)]
        else:
            return []

    def __repr__(self) -> str:
        return super().__repr__() + 'P'

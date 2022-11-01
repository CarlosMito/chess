from .piece import Piece


class Knight(Piece):

    movements = [
        (1, 2), (1, -2), (-1, 2), (-1, -2),
        (2, 1), (2, -1), (-2, 1), (-2, -1)
    ]
    infinite = False
    jumps = True

    def __init__(self, color, square=None):
        super().__init__(color, square)

    @property
    def code(self) -> str:
        code = "N"
        colorname = str(self.color)
        return f"{colorname[0]}{code}"

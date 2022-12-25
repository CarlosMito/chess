from typing import List
from .piece import Piece


class Pawn(Piece):

    movements = [(1, 0)]
    infinite = False
    jumps = False

    def __init__(self, color, position=None):
        super().__init__(color, position)

from .board import Board
from models.pieces.piece import Color
from models.pieces import *


class ChessBoard(Board):
    def __init__(self):
        super().__init__(8)
        self.reset()

    def reset(self):
        self.turn = Color.WHITE
        self.running = True

        default = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]

        for index in range(self.size):

            whites = [Pawn(Color.WHITE, (1, index)), default[index](Color.WHITE, (0, index))]
            blacks = [Pawn(Color.BLACK, (6, index)), default[index](Color.BLACK, (7, index))]

            self.pieces += whites + blacks

    def clear(self):
        self.turn = None
        self.running = False
        self.pieces.clear()

from models.pieces.piece import Color
from models.pieces.rook import Rook
from .board import Board
from models.pieces import *


class ChessBoard(Board):
    def __init__(self):
        super().__init__(8)
        self.reset()

    def reset(self):
        self.turn = Color.WHITE
        self.running = True

        default = {Rook, Knight, Bishop, Queen, King}

        for index in range(self.size):
            white = Pawn(Color.WHITE, (1, index))
            black = Pawn(Color.BLACK, (6, index))
            self.pieces.append(white)
            self.pieces.append(black)

    def clear(self):
        self.turn = None
        self.running = False
        self.pieces.clear()

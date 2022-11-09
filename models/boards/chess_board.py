from .board import Board
from typing import Tuple
from models.pieces.piece import Color, Piece
from models.pieces import Pawn, Rook, Knight, Bishop, Queen, King


class ChessBoard(Board):
    def __init__(self):
        super().__init__(8)
        self.reset()

    def reset(self):
        self.turn = Color.WHITE
        self.running = True
        self.pieces.clear()
        self.en_passant = {"color": None, "square": None}

        default = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]

        for index in range(self.size):

            whites = [Pawn(Color.WHITE, (1, index)), default[index](Color.WHITE, (0, index))]
            blacks = [Pawn(Color.BLACK, (6, index)), default[index](Color.BLACK, (7, index))]

            self.pieces += whites + blacks

    def __apply_en_passant(self, piece, origin, destination):

        # Remove pawn if the movement is En Passant
        if self.en_passant["square"] == destination:
            x = 3 if self.en_passant["color"] is Color.WHITE else 4
            captured = (x, destination[1])

            for cpiece in self.pieces:
                if cpiece.position == captured:
                    cpiece.position = None

        # En Passant Rule. The pawn must be captured immediately after the two-square advance.
        # So there's no need to store the square for both players.
        self.en_passant = {"color": None, "square": None}
        dy = origin[0] - piece.position[0]

        if isinstance(piece, Pawn) and abs(dy) > 1:
            self.en_passant["color"] = piece.color
            self.en_passant["square"] = (origin[0] - dy // 2, origin[1])

    def move(self, piece: Piece, destination: Tuple[int, int]):
        origin = super().move(piece, destination)

        self.__apply_en_passant(piece, origin, destination)

    def clear(self):
        self.turn = None
        self.running = False
        self.pieces.clear()

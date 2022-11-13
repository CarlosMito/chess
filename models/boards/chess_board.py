from .board import Board
from typing import Tuple
from models.pieces.piece import Color, Piece
from models.pieces import Pawn, Rook, Knight, Bishop, Queen, King
import copy
from typing import List


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

    def get_pieces(self, color: Color) -> List[Piece]:
        return [piece for piece in self.pieces if piece.color == color]

    def in_check(self, color: Color) -> bool:
        enemies = self.get_pieces(color.opposite)
        king = next(piece for piece in self.pieces if isinstance(piece, King) and piece.color == color)

        for enemy in enemies:
            if king.position in enemy.get_moves(self):
                return True

        return False

    def get_attackers(self, color: Color) -> List[Piece]:
        enemies = self.get_pieces(color.opposite)
        king = next(piece for piece in self.pieces if isinstance(piece, King) and piece.color == color)
        attackers = []

        for enemy in enemies:
            if king.position in enemy.get_moves(self):
                attackers.append(enemy)

        return attackers

    def is_checkmate(self, color: Color) -> bool:
        allies = self.get_pieces(color)
        attackers = self.get_attackers(color)
        moves = []

        for ally in allies:
            moves += ally.get_moves()

        moves = set(moves)

        # When a double check happens, it's impossible to capture
        # both pieces nor defend more than one path.

        for attacker in attackers:
            # Verify if the piece can be taken
            if attacker.position in moves:
                pass

        print("CHECKMATE!")
        return True

    def __apply_en_passant(self, piece: Piece, origin: Tuple[int, int]):

        # Remove pawn if the movement is En Passant
        if self.en_passant["square"] == piece.position:
            x = 3 if self.en_passant["color"] is Color.WHITE else 4
            captured = (x, piece.position[1])

            for cpiece in self.pieces:
                if cpiece.position == captured:
                    cpiece.position = None

        # En Passant Rule. The pawn must be captured immediately after the two-square advance.
        # So there's no need to store the square for both players.
        self.en_passant = {"color": None, "square": None}
        dy = piece.position[0] - origin[0]

        if isinstance(piece, Pawn) and abs(dy) > 1:
            self.en_passant["color"] = piece.color
            self.en_passant["square"] = (origin[0] + dy // 2, origin[1])

    def __apply_castling(self, piece: Piece, origin: Tuple[int, int]):

        dx = piece.position[1] - origin[1]
        direction = 1 if dx > 0 else -1

        if isinstance(piece, King) and abs(dx) > 1:

            rook = None

            for cpiece in self.pieces:
                if cpiece.color == piece.color and isinstance(cpiece, Rook):
                    cdx = cpiece.position[1] - origin[1]

                    # The value will be positive only if [cdx] and [dx] have the same sign
                    # which means they are pointing to the same direction
                    if cdx * dx > 0:
                        rook = cpiece
                        break

            rook.position = (piece.position[0], piece.position[1] - direction)

    def __apply_promotion(self, piece: Piece):
        promotion_row = 7 if piece.color is Color.WHITE else 0

        if isinstance(piece, Pawn) and piece.position[0] == promotion_row:

            # TODO: Add the possibility to choose the type of piece to promote to

            promoted = Queen(piece.color, piece.position)
            promoted.first_move = False
            piece.position = None
            self.pieces.append(promoted)

    def move(self, piece: Piece, destination: Tuple[int, int]):

        backup = copy.deepcopy(self.pieces)

        origin = super().move(piece, destination)

        self.__apply_en_passant(piece, origin)
        self.__apply_castling(piece, origin)
        self.__apply_promotion(piece)

        if self.in_check(piece.color):
            self.pieces = backup

    def clear(self):
        self.turn = None
        self.running = False
        self.pieces.clear()

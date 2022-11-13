from models.boards import ChessBoard
from models.pieces import Pawn, Rook, Knight, Bishop, Queen, King


def test_default_chess_board():
    board = ChessBoard()
    assert board.size == 8 and len(board.pieces) == 32


def test_en_passant():
    board = ChessBoard()

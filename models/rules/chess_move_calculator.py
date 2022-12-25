import copy
from typing import List, Tuple
from collections import defaultdict

from models.boards.chess_board import ChessBoard
from models.pieces.piece import Piece
from models.pieces import Pawn, King, Rook


class ChessMoveCalculator:

    @staticmethod
    def __get_moves_king(king: King, board: ChessBoard) -> List[Tuple[int, int]]:

        moves = ChessMoveCalculator.__get_moves_base(king, board)

        if king.position is None:
            return moves

        # [Castling]
        if king.first_move:

            # TODO: Disable castling when an enemy is attacking the King or the path between the King and the Rook

            allies = [other for other in board.pieces if other.color == king.color]
            rooks = [piece for piece in allies if isinstance(piece, Rook)]
            occupied_squares = [other.position for other in board.pieces]

            for rook in rooks:
                direction = 1 if rook.position[1] - king.position[1] > 0 else -1
                y_range = range(rook.position[1] - direction, king.position[1], -direction)
                squares_between = [(king.position[0], y) for y in y_range]
                blocked = False

                for square in squares_between:
                    if square in occupied_squares:
                        blocked = True

                if rook.first_move and not blocked:
                    square = (king.position[0], king.position[1] + direction * 2)
                    moves.append(square)

        return moves

    @staticmethod
    def __get_moves_pawn(pawn: Pawn, board: ChessBoard) -> List[Tuple[int, int]]:

        moves = []

        if pawn.position is None:
            return moves

        allies = board.get_squares(pawn.color)
        enemies = board.get_squares(pawn.color.opposite)

        direction = Pawn.movements[0][0] * pawn.color.value

        for i in [1, 2] if pawn.first_move else [1]:
            square = (pawn.position[0] + direction * i, pawn.position[1])

            if board.is_inside(square):
                if square not in allies + enemies:
                    moves.append(square)
                    continue

                break

        for attack in [-1, 1]:
            square = (pawn.position[0] + direction, pawn.position[1] + attack)

            if board.is_inside(square):

                en_passant = False

                if board.en_passant["square"] is not None:
                    epcolor = pawn.color.opposite == board.en_passant["color"]
                    epsquare = square == board.en_passant["square"]
                    en_passant = epcolor and epsquare

                if square in enemies or en_passant:
                    moves.append(square)

        return moves

    @staticmethod
    def __get_moves_base(piece: Piece, board: ChessBoard) -> List[Tuple[int, int]]:

        moves = []

        if piece.position is None:
            return moves

        allies = board.get_squares(piece.color)
        enemies = board.get_squares(piece.color.opposite)

        for movement in piece.movements:

            square = (piece.position[0] + movement[0], piece.position[1] + movement[1])
            blocked = False
            counter = 1

            while (counter == 1 or piece.infinite) and not blocked:
                i = piece.position[0] + movement[0] * counter
                j = piece.position[1] + movement[1] * counter

                square = (i, j)
                inside = board.is_inside(square)
                blocked = (square in allies + enemies) or not inside

                if inside and square not in allies:
                    moves.append(square)

                counter += 1

        return moves

    def __filter_moves(piece: Piece, board: ChessBoard, moves: List[Tuple[int, int]]):

        def causes_check(move):
            board.move(piece, move)

            if board.in_check(piece.color):
                board.undo()
                return False

            board.undo()
            return True

        filtered = list(filter(causes_check, moves))

        return filtered

    @staticmethod
    def get_moves(piece: Piece, board: ChessBoard, verify_check=True):

        controller = defaultdict(lambda: ChessMoveCalculator.__get_moves_base)

        controller[King] = ChessMoveCalculator.__get_moves_king
        controller[Pawn] = ChessMoveCalculator.__get_moves_pawn

        moves = controller[type(piece)](piece, board)

        if verify_check:
            moves = ChessMoveCalculator.__filter_moves(piece, board, moves)

        return moves

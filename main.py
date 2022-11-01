import pygame

# from game.surfaces import *
# from utils.matrix import *

from models import Pawn
from models.boards.board import Board
from models.boards.chess_board import ChessBoard

from models.pieces.piece import Piece
from models.pieces.piece import Color
from models.pieces.knight import Knight
from models.pieces.rook import Rook
from utils.position import Position

# Pieces image by User:Cburnett - Own work, CC BY-SA 3.0, https://commons.wikimedia.org/w/index.php?curid=1499806

# TODO: Add Castling [OK]
# TODO: Add En Passant [OK]
# TODO: Add Pawn Promotion [OK]
# TODO: Add Check Condition [OK]
# TODO: Add Checkmate [OK]
# TODO: Add Stalemate
# TODO: Add Play History
# TODO: Change all rules [castling, en passant] to Board/Piece class [OK]


# class Phone:
#     def __init__(self, OS) -> None:
#         self.OS = OS
#         self.x = 10
#         self.y = 20

# def play():
#     pygame.init()
#     pygame.display.set_caption('Chess')
#     screen = pygame.display.set_mode((800, 500))

#     running = True

#     board = Board()
#     # print(board)
#     # print(board.get_squares())

#     surface = BoardSurface(screen, board)

#     while running:
#         for event in pygame.event.get():
#             # print(event)
#             # print(board.next)

#             if event.type == pygame.QUIT:
#                 running = False

#             elif event.type == pygame.MOUSEBUTTONDOWN:
#                 surface.select(event.pos)

#             elif event.type == pygame.MOUSEBUTTONUP:
#                 surface.unselect(event.pos)
#                 surface.update()
#                 pass

#             elif event.type == pygame.MOUSEMOTION:
#                 surface.update(event)

#             elif event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_r:
#                     surface.board.reset()
#                     surface.update()

#         pygame.display.flip()


def debug():
    pass
    # print(Color(1))
    # print(Color(-1))

    # print(Piece(Color.WHITE))
    # print(Pawn(Color.WHITE))
    print(Rook(Color.WHITE))
    print(Rook(Color.WHITE).code)

    # print(Board(4))
    print(ChessBoard().pieces)
    # print(Knight(Color.BLACK))

    # print(get_square((7, 7)))


if __name__ == '__main__':
    debug()

import pygame
from interface.surfaces import BoardSurface

# from game.surfaces import *
# from utils.matrix import *

from collections import defaultdict

from models import Pawn
from models.boards.board import Board
from models.boards.chess_board import ChessBoard

from models.pieces.piece import Piece
from models.pieces.piece import Color
from models.pieces.knight import Knight
from models.pieces.rook import Rook

# Pieces image by User:Cburnett - Own work, CC BY-SA 3.0, https://commons.wikimedia.org/w/index.php?curid=1499806

# TODO: Add Castling [OK]
# TODO: Add En Passant [OK]
# TODO: Add Pawn Promotion [OK]
# TODO: Add Check Condition [OK]
# TODO: Add Checkmate [OK]
# TODO: Add Stalemate
# TODO: Add Play History
# TODO: Change all rules [castling, en passant] to Board/Piece class [OK]


# Chess Annotations
# Check has + sign -> example: e6+ (moves pawn to e6 and causes check)
# the capture is x ->  example: nxe5 (knight captures a piece in e5)

# hxg6 -> pawn capture
# e.p. -> optional
# a checkmate move has the symbol # at the end > example: hxg6# -> (en passant that delivers checkmate)
# king side castling 0-0
# queen side castling 0-0-0
# Nbd2 -> ambigous positions needs to have the starting piece file (column) / rank (row) before the final square
# R4a5

# class Phone:
#     def __init__(self, OS) -> None:
#         self.OS = OS
#         self.x = 10
#         self.y = 20

def play():
    pygame.init()
    pygame.display.set_caption('Chess')

    running = True
    screen = pygame.display.set_mode((800, 500))
    surface = BoardSurface(screen, ChessBoard())

    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                surface.select(event.pos)

            elif event.type == pygame.MOUSEBUTTONUP:
                surface.unselect(event.pos)
                surface.update()

            elif event.type == pygame.MOUSEMOTION:
                surface.update(event)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    surface.board.reset()
                    surface.update()

                if event.key == pygame.K_z:
                    surface.board.undo()
                    surface.update()

        pygame.display.flip()

    pygame.quit()


def debug():
    # print(ChessBoard())
    # print(Color(-1).opposite)
    pass


if __name__ == '__main__':
    # debug()
    play()

import pygame
from interface.surfaces import BoardSurface

# from game.surfaces import *
# from utils.matrix import *

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


# class Phone:
#     def __init__(self, OS) -> None:
#         self.OS = OS
#         self.x = 10
#         self.y = 20

def play():
    pygame.init()
    pygame.display.set_caption('Chess')

    running = True
    board = ChessBoard()
    screen = pygame.display.set_mode((800, 500))
    surface = BoardSurface(screen, board)

    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            # elif event.type == pygame.MOUSEBUTTONDOWN:
            #     screen.select(event.pos)

            # elif event.type == pygame.MOUSEBUTTONUP:
            #     screen.unselect(event.pos)
            #     screen.update()
            #     pass

            # elif event.type == pygame.MOUSEMOTION:
            #     screen.update(event)

            # elif event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_r:
            #         screen.board.reset()
            #         screen.update()

        pygame.display.flip()

    pygame.quit()


def debug():
    print(ChessBoard())


if __name__ == '__main__':
    # debug()
    play()


# # Simple pygame program

# # Import and initialize the pygame library
# import pygame
# pygame.init()

# # Set up the drawing window
# screen = pygame.display.set_mode([500, 500])

# # Run until the user asks to quit
# running = True
# while running:

#     # Did the user click the window close button?
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     # Fill the background with white
#     screen.fill((255, 255, 255))

#     # Draw a solid blue circle in the center
#     pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)

#     # Flip the display
#     pygame.display.flip()

# # Done! Time to quit.
# pygame.quit()

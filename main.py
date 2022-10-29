# import pygame

# from game.surfaces import *
# from utils.matrix import *

# import copy

# # Pieces image by User:Cburnett - Own work, CC BY-SA 3.0, https://commons.wikimedia.org/w/index.php?curid=1499806

# # TODO: Add Castling [OK]
# # TODO: Add En Passant [OK]
# # TODO: Add Pawn Promotion [OK]
# # TODO: Add Check Condition [OK]
# # TODO: Add Checkmate [OK]
# # TODO: Add Stalemate
# # TODO: Add Play History
# # TODO: Change all rules [castling, en passant] to Board/Piece class [OK]


# class Phone:
#     def __init__(self, OS) -> None:
#         self.OS = OS
#         self.x = 10
#         self.y = 20


# if __name__ == '__main__':
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

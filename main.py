import pygame

from game.surfaces import *
from utils.matrix import *

# Pieces image by User:Cburnett - Own work, CC BY-SA 3.0, https://commons.wikimedia.org/w/index.php?curid=1499806


class Phone:
    def __init__(self, OS) -> None:
        self.OS = OS
        self.x = 10
        self.y = 20


if __name__ == '__main__':
    # t1 = Board(4)
    # print(t1.board)

    pygame.init()
    pygame.display.set_caption('Chess')
    screen = pygame.display.set_mode((800, 500))

    running = True
    board = BoardSurface(screen)
    # print(board)

    while running:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                board.select(event.pos)

            elif event.type == pygame.MOUSEBUTTONUP:
                board.unselect(event.pos)
                board.update(event)

            elif event.type == pygame.MOUSEMOTION:
                board.update(event)

        pygame.display.flip()


# Move rectangle with mouse

# import os
# import pygame

# moving = False

# screen = pygame.display.set_mode((800, 500))
# # rect = pygame.draw.rect(screen, (255, 255, 255), (0, 0, 100, 100))
# running = True
# speed = [0.2, 0.2]

# image = pygame.image.load(os.path.join(
#     'assets', 'images', 'pieces', 'white', 'pawn.svg'))

# screen.blit(image, (200, 100))
# rect = image.get_rect()

# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#         elif event.type == pygame.MOUSEBUTTONDOWN:
#             print(rect)
#             if rect.collidepoint(event.pos):
#                 moving = True

#         elif event.type == pygame.MOUSEBUTTONUP:
#             moving = False

#         elif event.type == pygame.MOUSEMOTION and moving:
#             rect.move_ip(event.rel)

#     # pygame.draw.rect(screen, (255, 0, 0), rect)
#     # if moving:
#     #     pygame.draw.rect(screen, (0, 0, 255), rect, 4)

#     # rect = rect.move(speed)
#     # screen.blit(image, rect)
#     pygame.display.flip()

# pygame.quit()

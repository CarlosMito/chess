import pygame
from game.models import *


class BoardSurface(Board):
    DEFAULT_SQUARE = 50

    def __init__(self, parent, size, ratio):
        super().__init__(size=size)

        self.ratio = ratio
        self.surface = pygame.Surface(
            (size * BoardSurface.DEFAULT_SQUARE,
             size * BoardSurface.DEFAULT_SQUARE)
        )

        pygame.draw.rect(
            self.surface,
            (255, 255, 255),
            (200, 200, 200, 200)
        )

        # pygame.Surface.blit(self.surface, parent)

        pass

    def update():
        pass

    pass

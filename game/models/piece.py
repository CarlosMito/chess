import os
from enum import Enum
from abc import ABC, abstractmethod, abstractproperty


class Piece(ABC):
    def __init__(self, color, isAlive=True):
        self._color = color
        self._isAlive = isAlive

    @abstractmethod
    def project_move(self):
        pass

    def __repr__(self):
        return ' ' + self._color[0].upper()


class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)

    def project_move(self):
        print('Projecting moves...')

    def __repr__(self):
        return super().__repr__() + 'P '

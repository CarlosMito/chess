import os
from enum import Enum
from abc import ABC, abstractmethod, abstractproperty


class Piece(ABC):
    def __init__(self, color, isAlive=True):
        self.name = ''
        self.color = color
        self.isAlive = isAlive

    @abstractmethod
    def project_move(self):
        pass

    def __repr__(self) -> str:
        return ' ' + self.color[0].upper()


class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.name = 'pawn'

    def project_move(self):
        print('Projecting moves...')

    def __repr__(self) -> str:
        return super().__repr__() + 'P '


class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.name = 'pawn'

    def project_move(self):
        print('Projecting moves...')

    def __repr__(self) -> str:
        return super().__repr__() + 'P '


class King(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.name = 'king'

    def project_move(self):
        print('Projecting moves...')

    def __repr__(self) -> str:
        return super().__repr__() + 'K '


class Queen(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.name = 'queen'

    def project_move(self):
        print('Projecting moves...')

    def __repr__(self) -> str:
        return super().__repr__() + 'Q '


class Knight(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.name = 'knight'

    def project_move(self):
        print('Projecting moves...')

    def __repr__(self) -> str:
        return super().__repr__() + 'N '


class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.name = 'bishop'

    def project_move(self):
        print('Projecting moves...')

    def __repr__(self) -> str:
        return super().__repr__() + 'B '


class Rook(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.name = 'rook'

    def project_move(self):
        print('Projecting moves...')

    def __repr__(self) -> str:
        return super().__repr__() + 'R '

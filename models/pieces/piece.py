from __future__ import annotations
from typing import Tuple, List
from enum import Enum
from abc import ABC, abstractmethod


class Color(Enum):
    WHITE = 1
    BLACK = -1

    def __str__(self):
        return str(self.name)

    @property
    def opposite(self) -> Color:
        return Color(self.value * -1)


class Piece(ABC):

    movements = []
    infinite = None
    jumps = None

    @abstractmethod
    def __init__(self, color: Color, position: Tuple[int, int] | None = None):
        self.color = color
        self.position = position
        self.first_move = True

    @property
    def code(self) -> str:
        piecename = self.__class__.__name__
        colorname = str(self.color)
        return f"{colorname[0]}{piecename[0]}"

    def get_moves(self, board, verify_check=True) -> List[Tuple[int, int]]:
        from models.rules import ChessMoveCalculator
        return ChessMoveCalculator.get_moves(self, board, verify_check)

    def __str__(self) -> str:
        piecename = self.__class__.__name__
        position = self.position or "OUT"
        return f"[{str(self.color)} {piecename.upper()} : {position}]"

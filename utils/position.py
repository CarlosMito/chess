from __future__ import annotations

from typing import Tuple
from utils.exceptions import InvalidPosition


class Position:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    @property
    def value(self) -> Tuple[int, int]:
        return (self.x, self.y)

    @property
    def code(self) -> str:
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        return f"{letters[self.x]}{self.y + 1}"

    def is_outside(self):
        return not -1 < self.x < 8 or not -1 < self.y < 8

    def __add__(self, other: Position) -> Position:
        return Position(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Position) -> Position:
        return Position(self.x - other.x, self.y - other.y)

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"


# def get_square(position: Tuple[int, int]) -> str:
#     if not -1 < position[0] < 8 or not -1 < position[1] < 8:
#         raise InvalidPosition(position)

#     row = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
#     return f"{row[position[0]]}{position[1] + 1}"

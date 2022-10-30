from typing import Tuple

from utils.exceptions import InvalidPosition


def get_square(position: Tuple[int, int]) -> str:
    if not -1 < position[0] < 8 or not -1 < position[1] < 8:
        raise InvalidPosition(position)

    row = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    return f"{row[position[0]]}{position[1] + 1}"

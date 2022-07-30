from enum import Enum
from typing import Dict, Union, Tuple

# Personal Typing.
Slice = Union[slice, int]
TupleSlice = Tuple[Slice, Slice]

# Dictionary to change the color of the text
_COLORS: Dict[str, str] = {
    "green": "\033[38;5;46m{}\033[0;0m",
    "red": "\033[38;5;1m{}\033[0;0m",
    "yellow": "\033[38;5;226m{}\033[0;0m",
    "orange": "\033[38;5;208m{}\033[0;0m",
    "blue": "\033[38;5;21m{}\033[0;0m",
    "white": "\033[38;5;252m{}\033[0;0m"
}


class Color(Enum):
    """
    Enumerator for the colors of the faces of a Rubik's cube.
    """
    GREEN = "green"
    RED = "red"
    YELLOW = "yellow"
    ORANGE = "orange"
    BLUE = "blue"
    WHITE = "white"

    def __repr__(self) -> str:
        return _COLORS[self.value].format(self.name[0])

    def __hash__(self) -> int:
        return {
            "green": 1, "red": 2, "yellow": 3,
            "orange": 4, "blue": 5, "white": 6
        }.get(self.value, 0)


# Slice to indicate that the entire row/column will be obtained.
_ALL: Slice = slice(None, None)

# Dictionary of different slices for the arrays.
_DICT_TUPLE_SLICES: dict[int, TupleSlice] = {
    0: (0, _ALL), 1: (_ALL, -1),
    2: (-1, _ALL), 3: (_ALL, 0)
}


class Direction(Enum):
    """
    Enumerator to indicate which direction a face is adjacent to another face.
    """
    U = 0
    R = 1
    D = 2
    L = 3

    def generate_slice(self) -> TupleSlice:
        return _DICT_TUPLE_SLICES.get(self.value, (_ALL, _ALL))

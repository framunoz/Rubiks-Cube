import enum

from colorama import Fore, Style

_COLORS = {
    "green": Fore.GREEN,
    "red": Fore.RED,
    "yellow": Fore.YELLOW,
    "orange": Style.BRIGHT + Fore.RED,
    "blue": Fore.BLUE,
    "white": Style.DIM + Fore.WHITE
}


class Color(enum.Enum):
    """
    Enumerator for the colors of the faces of a Rubik's cube.
    """
    GREEN = "green"
    RED = "red"
    YELLOW = "yellow"
    ORANGE = "orange"
    BLUE = "blue"
    WHITE = "white"

    def __repr__(self):
        return _COLORS[self.value] + self.name[0] + Style.RESET_ALL


class Direction(enum.Enum):
    U = 0
    R = 1
    D = 2
    L = 3

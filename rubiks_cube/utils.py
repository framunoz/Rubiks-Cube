import enum

# Dictionary to change the color of teh text
_COLORS = {
    "green": "\033[38;5;46m{}\033[0;0m",
    "red": "\033[38;5;1m{}\033[0;0m",
    "yellow": "\033[38;5;226m{}\033[0;0m",
    "orange": "\033[38;5;208m{}\033[0;0m",
    "blue": "\033[38;5;21m{}\033[0;0m",
    "white": "\033[38;5;252m{}\033[0;0m"
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
        return _COLORS[self.value].format(self.name[0])


class Direction(enum.Enum):
    """
    Enumerator to indicate wich direction a face is adjacent to another face.
    """
    U = 0
    R = 1
    D = 2
    L = 3

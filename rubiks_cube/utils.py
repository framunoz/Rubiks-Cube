import enum

_COLORS = {
    "green": "\033[38;5;46m",
    "red": "\033[38;5;1m",
    "yellow": "\033[38;5;226m",
    "orange": "\033[38;5;208m",
    "blue": "\033[38;5;21m",
    "white": "\033[38;5;252m"
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
        return f"{_COLORS[self.value]}{self.name[0]}\033[0;0m"


class Direction(enum.Enum):
    U = 0
    R = 1
    D = 2
    L = 3


def main():
    for c in Color:
        print(repr(c))


if __name__ == '__main__':
    main()

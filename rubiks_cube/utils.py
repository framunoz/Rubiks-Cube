import enum


class Color(enum.Enum):
    """
    Enumerator for the colors of the faces of a Rubik's cube.
    """
    GREEN = enum.auto()
    RED = enum.auto()
    YELLOW = enum.auto()
    ORANGE = enum.auto()
    BLUE = enum.auto()
    WHITE = enum.auto()

    def __repr__(self):
        return self.name[0]


class Direction(enum.Enum):
    U = enum.auto()
    R = enum.auto()
    D = enum.auto()
    L = enum.auto()

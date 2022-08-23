from __future__ import annotations

import abc
from enum import Enum
from typing import Optional

from rubiks_cube.faces import Face


# TODO: Agregar el resto de movimientos, como también sus transformaciones inversas.
class BaseMove(abc.ABC):
    """Abstract clase for every movement."""
    def __init__(self, times: int = 1):
        # Times that moves in the clockwise direction
        self.times = times

    @abc.abstractmethod
    def face(self, cube) -> Face:
        """To use template pattern. It is the face that is rotated."""
        pass

    def move_the_cube(self, cube):
        """Method that make a movement on the cube."""
        self.face(cube).rotate(self.times)

    def __repr__(self) -> str:
        return self.__class__.__name__


class R(BaseMove):
    """Moves the Right Face in the clockwise direction."""
    def face(self, cube) -> Face:
        return cube.right


class R2(R):
    """Moves the Right Face in the clockwise direction twice."""
    def __init__(self):
        super().__init__(2)


class L(BaseMove):
    """Moves the Left Face in the clockwise direction."""
    def face(self, cube) -> Face:
        return cube.left


class L2(L):
    """Moves the Left Face in the clockwise direction twice."""
    def __init__(self):
        super().__init__(2)


class U(BaseMove):
    """Moves the Up Face in the clockwise direction."""
    def face(self, cube) -> Face:
        return cube.up


class U2(U):
    """Moves the Up Face in the clockwise direction twice."""
    def __init__(self):
        super().__init__(2)


class D(BaseMove):
    """Moves the Down Face in the clockwise direction."""
    def face(self, cube) -> Face:
        return cube.down


class D2(D):
    """Moves the Down Face in the clockwise direction twice."""
    def __init__(self):
        super().__init__(2)


class CubeMove(Enum):
    """Enumerator that sum up the movements."""
    R = R
    R2 = R2
    L = L
    L2 = L2
    U = U
    U2 = U2
    D = D
    D2 = D2

    def __repr__(self):
        return self.name

    def move_the_cube(self, cube):
        """To use double dispatch over RubikCube."""
        self.value().move_the_cube(cube)

    @classmethod
    def from_str(cls, move_as_str: str) -> Optional[CubeMove]:
        """Returns a CubeMove given a string that represents it."""
        return {m.name: getattr(cls, m.name) for m in cls}.get(move_as_str, None)

from __future__ import annotations

import abc
from enum import Enum
from typing import Optional

from rubiks_cube.faces import Face


# TODO: Agregar el resto de movimientos, como también sus transformaciones inversas.
class BaseMove(abc.ABC):
    """Abstract clase for every movement."""
    def __init__(self, times):
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


class BaseF(BaseMove, abc.ABC):
    """Abstract class for the Front Moves"""

    def face(self, cube) -> Face:
        return cube.front


class F(BaseF):
    def __init__(self):
        super().__init__(1)


class F2(BaseF):
    def __init__(self):
        super().__init__(2)


class BaseB(BaseMove, abc.ABC):
    """Abstract class for the Back Moves"""

    def face(self, cube) -> Face:
        return cube.back


class B(BaseB):
    def __init__(self):
        super().__init__(1)


class B2(BaseB):
    def __init__(self):
        super().__init__(2)


class BaseU(BaseMove, abc.ABC):
    """Abstract class for the Upper Moves"""

    def face(self, cube) -> Face:
        return cube.up


class U(BaseU):
    """Moves the Up Face in the clockwise direction."""

    def __init__(self):
        super().__init__(1)


class U2(BaseU):
    """Moves the Up Face in the clockwise direction twice."""

    def __init__(self):
        super().__init__(2)


class BaseD(BaseMove, abc.ABC):
    """Abstract class for the Down Moves"""

    def face(self, cube) -> Face:
        return cube.down


class D(BaseD):
    """Moves the Down Face in the clockwise direction."""

    def __init__(self):
        super().__init__(1)


class D2(BaseD):
    """Moves the Down Face in the clockwise direction twice."""

    def __init__(self):
        super().__init__(2)


class BaseL(BaseMove, abc.ABC):
    """Abstract class for the Left Moves"""

    def face(self, cube) -> Face:
        return cube.left


class L(BaseL):
    """Moves the Left Face in the clockwise direction."""

    def __init__(self):
        super().__init__(1)


class L2(BaseL):
    """Moves the Left Face in the clockwise direction twice."""

    def __init__(self):
        super().__init__(2)


class BaseR(BaseMove, abc.ABC):
    """Abstract class for the Right Moves"""

    def face(self, cube) -> Face:
        return cube.right


class R(BaseR):
    """Moves the Right Face in the clockwise direction."""

    def __init__(self):
        super().__init__(1)


class R2(BaseR):
    """Moves the Right Face in the clockwise direction twice."""

    def __init__(self):
        super().__init__(2)


class CubeMove(Enum):
    """Enumerator that sum up the movements."""
    F = F
    F2 = F2
    B = B
    B2 = B2
    U = U
    U2 = U2
    D = D
    D2 = D2
    L = L
    L2 = L2
    R = R
    R2 = R2

    def __repr__(self):
        return self.name

    def move_the_cube(self, cube):
        """To use double dispatch over RubikCube."""
        self.value().move_the_cube(cube)

    @classmethod
    def from_str(cls, move_as_str: str) -> Optional[CubeMove]:
        """Returns a CubeMove given a string that represents it."""
        return {m.name: getattr(cls, m.name) for m in cls}.get(move_as_str, None)

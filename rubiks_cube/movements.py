import abc
from enum import Enum

from rubiks_cube.faces import Face


class CubeMove(abc.ABC):
    def __init__(self, times: int = 1):
        self.times = times

    @abc.abstractmethod
    def face(self, cube) -> Face:
        pass

    def move_the_cube(self, cube):
        self.face(cube).rotate(self.times)


class R(CubeMove):
    def face(self, cube) -> Face:
        return cube.right


class R2(R):
    def __init__(self):
        super().__init__(2)


class L(CubeMove):
    def face(self, cube) -> Face:
        return cube.left


class L2(L):
    def __init__(self):
        super().__init__(2)


class U(CubeMove):
    def face(self, cube) -> Face:
        return cube.up


class U2(U):
    def __init__(self):
        super().__init__(2)


class D(CubeMove):
    def face(self, cube) -> Face:
        return cube.down


class D2(D):
    def __init__(self):
        super().__init__(2)


class Movement(Enum):
    R = R()
    R2 = R2()
    L = L()
    L2 = L2()
    U = U()
    U2 = U2()
    D = D()
    D2 = D2()

    def move_the_cube(self, cube):
        self.value.move_the_cube(cube)

    def __repr__(self):
        return self.value.__class__.__name__

import unittest

from rubiks_cube.cube import RubikCube
from rubiks_cube.faces import Face
from rubiks_cube.movements import CubeMove
from rubiks_cube.utils import R, Y, G, W, B
from tests.test_base import TestBase


class TestBaseMove(TestBase):
    def setUp(self) -> None:
        super(TestBaseMove, self).setUp()
        self.rc = RubikCube(*self.faces)

    def _test_move_the_cube(self, move: CubeMove, expected: RubikCube):
        rc_moved = self.rc.make_movements(move)
        self.assertEqual(
            rc_moved, expected,
            f"'{repr(move)}' movement does not works."
        )


class TestR2(TestBaseMove):
    def test_move_the_cube(self):
        expected = RubikCube(
            Face([[R, Y]]),
            Face([[R], [G], [W]]),
            Face([[G, G],
                  [R, B],
                  [W, R]]),
            Face([[Y], [R], [B]]),
            Face([[B, B],
                  [W, Y],
                  [Y, W]]),
            Face([[W, B]])
        )
        self._test_move_the_cube(CubeMove.R2, expected)


class TestL2(TestBaseMove):
    def test_move_the_cube(self):
        expected = RubikCube(
            Face([[W, B]]),
            Face([[W], [G], [R]]),
            Face([[W, Y],
                  [Y, W],
                  [B, B]]),
            Face([[B], [R], [Y]]),
            Face([[R, W],
                  [B, R],
                  [G, G]]),
            Face([[R, Y]])
        )
        self._test_move_the_cube(CubeMove.L2, expected)


class TestU2(TestBaseMove):
    def test_move_the_cube(self):
        expected = RubikCube(
            Face([[B, R]]),
            Face([[B], [G], [W]]),
            Face([[R, B],
                  [R, W],
                  [W, B]]),
            Face([[R], [R], [Y]]),
            Face([[G, Y],
                  [B, Y],
                  [G, W]]),
            Face([[W, Y]])
        )
        self._test_move_the_cube(CubeMove.U2, expected)


class TestD2(TestBaseMove):
    def test_move_the_cube(self):
        expected = RubikCube(
            Face([[R, B]]),
            Face([[R], [G], [Y]]),
            Face([[G, Y],
                  [R, W],
                  [G, W]]),
            Face([[B], [R], [W]]),
            Face([[R, B],
                  [B, Y],
                  [W, B]]),
            Face([[Y, W]])
        )
        self._test_move_the_cube(CubeMove.D2, expected)


if __name__ == '__main__':
    unittest.main()

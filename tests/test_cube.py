import copy
import unittest

from rubiks_cube.cube import RubikCube
from rubiks_cube.faces import Face
from rubiks_cube.movements import CubeMove
from rubiks_cube.utils import R, B, Y, G, W
from tests.test_base import TestBase


class TestRubikCube(TestBase):
    def setUp(self) -> None:
        super().setUp()
        self.rc: RubikCube = RubikCube(*self.faces)
        self.rc2: RubikCube = RubikCube.from_dims((3, 2, 1))
        self.rc3: RubikCube = RubikCube.from_dims((3, 2, 1))

    def test_faces(self):
        self.assertEqual(
            self.rc.faces, self.faces,
            "'faces' method does not work.")

    def test_hash(self):
        # Similar instances must have the same hash code
        self.assertEqual(
            hash(self.rc2), hash(self.rc3),
            "Similar instances must have the same hash code.")
        # Different instances must have different hash code
        self.assertNotEqual(
            hash(self.rc), hash(self.rc3),
            "Different instances must have different hash code.")
        # Creating sets
        set_of_rubik_cubes = {copy.deepcopy(self.rc)}
        # Make a movement and add to the set
        self.rc.make_movements_from_str("U2")
        set_of_rubik_cubes.add(copy.deepcopy(self.rc))
        # Rubik's cube similar to the first
        self.rc.make_movements_from_str("U2")
        set_of_rubik_cubes.add(copy.deepcopy(self.rc))
        # Make a different Rubik's Cube
        self.rc.make_movements_from_str("L2")
        set_of_rubik_cubes.add(copy.deepcopy(self.rc))
        self.assertEqual(
            len(set_of_rubik_cubes), 3,
            "Creating a set does not work correctly.")

    def test_make_a_move(self):
        expected = RubikCube(
            Face([[R, Y]]),
            Face([[R], [G], [W]]),
            Face([
                [G, G],
                [R, B],
                [W, R]
            ]),
            Face([[Y], [R], [B]]),
            Face([
                [B, B],
                [W, Y],
                [Y, W]
            ]),
            Face([[W, B]])
        )
        self.rc.make_a_move(CubeMove.R2)
        self.assertEqual(
            self.rc, expected,
            "'make_a_move' method does not work.")

    def test_make_movements_from_list(self):
        expected = RubikCube(
            Face([[Y, R]]),
            Face([[Y], [G], [W]]),
            Face([
                [B, B],
                [R, B],
                [W, R]
            ]),
            Face([[R], [R], [B]]),
            Face([
                [G, G],
                [W, Y],
                [Y, W]
            ]),
            Face([[W, B]])
        )
        self.rc.make_movements_from_list([CubeMove.R2, CubeMove.U2])
        self.assertEqual(
            self.rc, expected,
            "'make_movements_from_list' method does not work.")

    def test_make_movements_from_str(self):
        expected = RubikCube(
            Face([[Y, R]]),
            Face([[Y], [G], [W]]),
            Face([
                [B, B],
                [R, B],
                [W, R]
            ]),
            Face([[R], [R], [B]]),
            Face([
                [G, G],
                [W, Y],
                [Y, W]
            ]),
            Face([[W, B]])
        )
        self.rc.make_movements_from_str("R2 U2")
        self.assertEqual(
            self.rc, expected,
            "'make_movements_from_str' method does not work.")

    def test_deepcopy(self):
        other_rc: RubikCube = copy.deepcopy(self.rc)

        other_rc.make_movements_from_str("L2")

        self.assertNotEqual(
            self.rc, other_rc,
            "Method deepcopy does not work.")


if __name__ == '__main__':
    unittest.main()

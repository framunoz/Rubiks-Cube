import unittest
from unittest import TestCase

import numpy as np

from rubiks_cube.faces import Face
from rubiks_cube.utils import Color


class TestFace(TestCase):
    def setUp(self) -> None:
        self.face = Face(Color.RED, (3, 2))
        self.up = Face(Color.BLUE, (2, 2))
        self.down = Face(Color.GREEN, (2, 2))
        self.right = Face(Color.ORANGE, (3, 2))
        self.left = Face(Color.ORANGE, (3, 2))
        self.faces = [self.up, self.down, self.right, self.left]

    def test_instance_well_created(self):
        r = Color.RED
        expected = np.array([[r, r], [r, r], [r, r]])
        np.testing.assert_array_equal(
            self.face.central_face, expected,
            "The face has not been created correctly.")

    def test_add_faces(self):
        self.face.add_faces(
            up_tuple=(self.up, 2), right_tuple=(self.right, 3), down_tuple=(self.down, 0), left_tuple=(self.left, 1)
        )
        np.testing.assert_array_equal(
            self.face.up.central_face, self.up.central_face,
            "The 'up' face is not correct."
        )
        np.testing.assert_array_equal(
            self.face.right.central_face, self.right.central_face,
            "The 'right' face is not correct."
        )
        np.testing.assert_array_equal(
            self.face.down.central_face, self.down.central_face,
            "The 'down' face is not correct."
        )
        np.testing.assert_array_equal(
            self.face.left.central_face, self.left.central_face,
            "The 'left' face is not correct."
        )


if __name__ == '__main__':
    unittest.main()

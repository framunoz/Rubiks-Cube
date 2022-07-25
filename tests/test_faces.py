import unittest
from unittest import TestCase

import numpy as np

from rubiks_cube.faces import Face
from rubiks_cube.utils import Color


class TestFace(TestCase):
    def setUp(self) -> None:
        self.face = Face(Color.RED, (3, 2))
        self.up = Face(Color.BLUE, (2, 2))
        self.right = Face(Color.ORANGE, (3, 2))
        self.down = Face(Color.GREEN, (2, 2))
        self.left = Face(Color.YELLOW, (3, 2))
        self.faces = [(self.up, 2), (self.right, 3), (self.down, 0), (self.left, 1)]
        self.face.add_faces(*self.faces)

    def test_instance_well_created(self):
        r = Color.RED
        expected = np.array([[r, r], [r, r], [r, r]])
        np.testing.assert_array_equal(
            self.face.central_face, expected,
            "The face has not been created correctly.")

    def test_add_faces(self):
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

    def test_rotate(self):
        # Change a corner
        self.face.central_face[0, 0] = Color.WHITE
        # List of news faces
        g, r, y, o, b, w = Color.GREEN, Color.RED, Color.YELLOW, Color.ORANGE, Color.BLUE, Color.WHITE
        up = np.array([
            [b, b],
            [g, g]
        ])
        right = np.array([
            [y, o],
            [y, o],
            [y, o],
        ])
        expected_list = [up, right, up, right]
        central = np.array([
            [r, r],
            [r, r],
            [r, w],
        ])
        # Do a rotation
        self.face.rotate(2)
        np.testing.assert_array_equal(
            self.face.cf, central,
            "The 'central' face does not rotate correctly."
        )
        for res, exp in zip(self.face.faces, expected_list):
            np.testing.assert_array_equal(
                res.cf, exp,
                "A face does not rotate correctly."
            )


if __name__ == '__main__':
    unittest.main()

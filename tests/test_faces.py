import unittest
from unittest import TestCase

import numpy as np

from rubiks_cube.faces import Face
from rubiks_cube.utils import Color

G, R, Y, O, B, W = Color.GREEN, Color.RED, Color.YELLOW, Color.ORANGE, Color.BLUE, Color.WHITE

Rc, Bc, Oc, Gc, Yc, Wc = (repr(Color.RED), repr(Color.BLUE), repr(Color.ORANGE),
                          repr(Color.GREEN), repr(Color.YELLOW), repr(Color.WHITE))


class TestFace(TestCase):
    def setUp(self) -> None:
        # Principal face
        self.face = Face(
            np.array([
                [B],
                [R],
                [Y]
            ])
        )
        # Other faces
        self.up = Face(np.array([
            [R, B]
        ]))
        self.right = Face(np.array([
            [R, B],
            [B, Y],
            [G, W]
        ]))
        self.down = Face(np.array([
            [W, Y]
        ]))
        self.left = Face(np.array([
            [G, Y],
            [R, W],
            [W, B]
        ]))
        self.faces = [(self.up, 1), (self.right, 3), (self.down, 1), (self.left, 1)]
        # Add the other faces
        self.face.add_faces(*self.faces)
        self.face2 = Face.from_color(R, (3, 2))

    def test_instance_well_created(self):
        expected = np.array([
            [B], [R], [Y]
        ])
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
        # List of news faces
        up = np.array([
            [R, Y]
        ])
        right = np.array([
            [B, B],
            [W, Y],
            [Y, W],
        ])
        down = np.array([
            [W, B]
        ])
        left = np.array([
            [G, G],
            [R, B],
            [W, R],
        ])
        expected_list = [up, right, down, left]
        central = np.array([
            [Y], [R], [B]
        ])
        # Do a rotation
        self.face.rotate(2)
        np.testing.assert_array_equal(
            self.face.central_face, central,
            "The 'central' face does not rotate correctly."
        )
        for res, exp in zip(self.face.faces, expected_list):
            np.testing.assert_array_equal(
                res.central_face, exp,
                "A face does not rotate correctly."
            )

    def test_repr(self):
        expected = (f"{Rc} {Rc}\n" * 3)[:-1]
        self.assertEqual(
            repr(self.face2), expected,
            "Representation are not equal as it must be.")
        expected = (
                f"   {Bc}\n\n"
                + f"{Yc}  {Bc}  {Rc}\n"
                + f"{Wc}  {Rc}  {Bc}\n"
                + f"{Bc}  {Yc}  {Gc}\n\n"
                + f"   {Yc}"
        )
        self.assertEqual(
            repr(self.face), expected,
            "Representation are not equal as it must be.")


if __name__ == '__main__':
    unittest.main()

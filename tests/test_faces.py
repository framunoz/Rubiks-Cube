import unittest

import numpy as np

from rubiks_cube.faces import Face
from rubiks_cube.utils import R, Y, B, W, G, Bc, Yc, Wc, Rc, Gc
from tests.test_base import TestBase


class TestFace(TestBase):
    def setUp(self) -> None:
        super().setUp()
        # Define the faces to use
        self.central = self.f4
        self.up, self.right, self.down, self.left = self.f1, self.f5, self.f6, self.f3
        # Attach the faces into the central face
        self.central.add_faces((self.up, 1), (self.right, 3), (self.down, 1), (self.left, 1))
        # Other face to compare
        self.face2: Face = Face.from_color(R, (3, 2))
        self.face3: Face = Face.from_color(R, (3, 2))

    def test_instance_well_created(self):
        expected = np.array([
            [B], [R], [Y]
        ])
        np.testing.assert_array_equal(
            self.central.central_face, expected,
            "The face has not been created correctly.")

    def test_hash(self):
        self.assertEqual(
            hash(self.face2), hash(self.face3),
            "Two equals instances had different hash code.")
        self.assertNotEqual(
            hash(self.central), hash(self.face3),
            "Two different instances had equals hash code.")

    def test_add_faces(self):
        self.assertEqual(
            self.central.up, self.up,
            "The 'up' face is not correct.")
        self.assertEqual(
            self.central.right, self.right,
            "The 'right' face is not correct."
        )
        self.assertEqual(
            self.central.down, self.down,
            "The 'down' face is not correct."
        )
        self.assertEqual(
            self.central.left, self.left,
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
        self.central.rotate(2)
        np.testing.assert_array_equal(
            self.central.central_face, central,
            "The 'central' face does not rotate correctly."
        )
        for res, exp in zip(self.central.faces, expected_list):
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
            repr(self.central), expected,
            "Representation are not equal as it must be.")


if __name__ == '__main__':
    unittest.main()

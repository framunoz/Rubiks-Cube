import unittest

from rubiks_cube.faces import Face
from rubiks_cube.utils import R, B, G, W, Y


class TestBase(unittest.TestCase):
    def setUp(self) -> None:
        # Up
        self.f1 = Face([[R, B]])
        # Left
        self.f2 = Face([
            [R],
            [G],
            [W]
        ])
        # Front
        self.f3 = Face([
            [G, Y],
            [R, W],
            [W, B]
        ])
        # Right
        self.f4 = Face([
            [B],
            [R],
            [Y]
        ])
        # Back
        self.f5 = Face([
            [R, B],
            [B, Y],
            [G, W]
        ])
        # Down
        self.f6 = Face([
            [W, Y]
        ])
        # Faces
        self.faces = [self.f1, self.f2, self.f3, self.f4, self.f5, self.f6]


if __name__ == '__main__':
    unittest.main()

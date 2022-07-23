from __future__ import annotations

from typing import Tuple, Optional
import numpy as np

from rubiks_cube.utils import Color
from rubiks_cube.utils import Direction as Direc


def generate_slice_from_direction(direction):
    all_ = slice(None, None)
    if direction == Direc.U:
        return 0, all_
    elif direction == Direc.R:
        return all_, -1
    elif direction == Direc.D:
        return -1, all_
    elif direction == Direc.L:
        return all_, 0
    return None


class Face:
    def __init__(self, color: Color, shape: Tuple[int, int]):
        self.color: Color = color
        self.shape: Tuple[int, int] = shape

        self.central_face: np.ndarray[Color] = np.tile(color, shape)
        self.up: Optional[Face] = None
        self.right: Optional[Face] = None
        self.down: Optional[Face] = None
        self.left: Optional[Face] = None
        self._slice_list = None

    @property
    def cf(self) -> np.ndarray[Color]:
        return self.central_face

    def __repr__(self):
        return self.central_face.__repr__()

    def add_faces(self, up_tuple, right_tuple, down_tuple, left_tuple):
        # TODO: Agregar algo para que valide que las caras realmente se ajusten? onda que
        #  si la cara central es de (2, 2) que el de la izquierda sea de (2, 100) y no de (100, 100).
        (up, up_s), (right, right_s), (down, down_s), (left, left_s) = up_tuple, right_tuple, down_tuple, left_tuple
        self.up, self.right, self.down, self.left = up, right, down, left
        self._slice_list = up_s, right_s, down_s, left_s

    def rotate_once(self):
        # TODO: Agregar validadores para chequear que el movimiento se puede hacer (?)
        up_s, right_s, down_s, left_s = self._slice_list
        self.up.cf[up_s], self.right.cf[right_s], self.down.cf[down_s], self.left.cf[left_s] = \
            self.left.cf[left_s], self.up.cf[up_s], self.right.cf[right_s], self.down.cf[down_s]

    def rotate_inverse(self):
        # TODO: Agregar validadores para chequear que el movimiento se puede hacer (?)
        up_s, right_s, down_s, left_s = self._slice_list
        self.up.cf[up_s], self.right.cf[right_s], self.down.cf[down_s], self.left.cf[left_s] = \
            self.right.cf[right_s], self.down.cf[down_s], self.left.cf[left_s], self.up.cf[up_s]

    def rotate_twice(self):
        # TODO: Agregar validadores para chequear que el movimiento se puede hacer (?)
        up_s, right_s, down_s, left_s = self._slice_list
        self.up.cf[up_s], self.right.cf[right_s], self.down.cf[down_s], self.left.cf[left_s] = \
            self.down.cf[down_s], self.left.cf[left_s], self.up.cf[up_s], self.right.cf[right_s]


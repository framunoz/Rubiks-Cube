from __future__ import annotations

from typing import Tuple, List, Union

import numpy as np

from rubiks_cube.utils import Color
from rubiks_cube.utils import Direction as Direc

Slice = Union[slice, int]
TupleSlice = Tuple[Slice, Slice]


def generate_slice(direction) -> TupleSlice:
    all_ = slice(None, None)
    if direction == Direc.U:
        return 0, all_
    elif direction == Direc.R:
        return all_, -1
    elif direction == Direc.D:
        return -1, all_
    elif direction == Direc.L:
        return all_, 0
    return all_, all_


class Face:
    def __init__(self, color: Color | str, shape: Tuple[int, int]):
        self.color: Color = Color(color)
        self.shape: Tuple[int, int] = shape

        # Central Face
        matrix = np.ones(self.shape, dtype=object)
        matrix[:, :] = self.color
        self.central_face: np.ndarray[Color] = matrix

        # Faces
        self.up: Face | None = None
        self.right: Face | None = None
        self.down: Face | None = None
        self.left: Face | None = None

        self._slice_list: List[TupleSlice] | None = None

    @property
    def cf(self) -> np.ndarray[Color]:
        return self.central_face

    @property
    def faces(self) -> List[Face]:
        return [self.up, self.right, self.down, self.left]

    @property
    def pieces(self):
        u_s, r_s, d_s, l_s = self._slice_list
        to_return: List[np.ndarray] = [self.up.cf[u_s], self.right.cf[r_s], self.down.cf[d_s], self.left.cf[l_s]]
        return [arr.copy() for arr in to_return]

    @pieces.setter
    def pieces(self, to_set):
        u_s, r_s, d_s, l_s = self._slice_list
        self.up.cf[u_s], self.right.cf[r_s], self.down.cf[d_s], self.left.cf[l_s] = to_set

    def __repr__(self):
        return self.central_face.__repr__()

    def add_faces(self, up_tuple, right_tuple, down_tuple, left_tuple):
        # TODO: Agregar algo para que valide que las caras realmente se ajusten? onda que
        #  si la cara central es de (2, 2) que el de la izquierda sea de (2, 100) y no de (100, 100).
        (up, up_d), (right, right_d), (down, down_d), (left, left_d) = up_tuple, right_tuple, down_tuple, left_tuple
        self.up, self.right, self.down, self.left = up, right, down, left
        self._slice_list = [generate_slice(Direc(s)) for s in [up_d, right_d, down_d, left_d]]

    def rotate(self, times: int):
        times = times % 4
        # TODO: Agregar validadores para chequear que el movimiento se puede hacer (?)
        self.pieces = np.roll(self.pieces, times)
        self.central_face = np.rot90(self.central_face, times)

from __future__ import annotations

from typing import Tuple, List, Union

import numpy as np

from rubiks_cube.utils import Color
from rubiks_cube.utils import Direction as Direc

Slice = Union[slice, int]
TupleSlice = Tuple[Slice, Slice]

_ALL: Slice = slice(None, None)

_DICT_TUPLE_SLICES: dict[Direc, TupleSlice] = {
    Direc.U: (0, _ALL),
    Direc.R: (_ALL, -1),
    Direc.D: (-1, _ALL),
    Direc.L: (_ALL, 0)
}


def generate_slice(direction) -> TupleSlice:
    return _DICT_TUPLE_SLICES.get(direction, (_ALL, _ALL))


class Face:
    def __init__(self, color: Color | str, shape: Tuple[int, int]):
        self.color: Color = Color(color)
        self.shape: Tuple[int, int] = shape

        # Central Face
        self.central_face: np.ndarray[Color] = np.tile(self.color, self.shape)

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
    def pieces(self) -> np.ndarray[np.ndarray]:
        u_s, r_s, d_s, l_s = self._slice_list
        to_return: List[np.ndarray] = [self.up.cf[u_s], self.right.cf[r_s], self.down.cf[d_s], self.left.cf[l_s]]
        return np.array([arr.copy() for arr in to_return], dtype=object)

    @pieces.setter
    def pieces(self, to_set):
        u_s, r_s, d_s, l_s = self._slice_list
        self.up.cf[u_s], self.right.cf[r_s], self.down.cf[d_s], self.left.cf[l_s] = to_set

    def __repr__(self):
        return self.central_face.__str__()

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

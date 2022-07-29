from __future__ import annotations

from collections import deque
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

        self._direc_list: List[Direc] | None = None
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
        return [list(arr) for arr in to_return]

    @pieces.setter
    def pieces(self, to_set):
        u_s, r_s, d_s, l_s = self._slice_list
        self.up.cf[u_s], self.right.cf[r_s], self.down.cf[d_s], self.left.cf[l_s] = to_set

    def repr_central_face(self, space: int = 0) -> str:
        str_to_return = ""
        for row in self.central_face:
            str_to_return += " " * space + " ".join([repr(e) for e in row]) + "\n"
        return str_to_return[:-1]

    def __repr__(self):
        if None in self.faces:
            return self.repr_central_face()
        def color_to_str(list_of_colors: List[Color]):
            return [repr(c) for c in list_of_colors]
        p_up, p_right, p_down, p_left = [color_to_str(loc) for loc in self.pieces]
        str_to_return = "   "
        str_to_return += " ".join(p_up) + "\n\n"
        central_face_list = self.repr_central_face().split("\n")
        for left, central, right in zip(p_left, central_face_list, p_right):
            str_to_return += f"{left}  {central}  {right}\n"
        str_to_return += "\n   " + " ".join(p_down)
        return str_to_return

    def add_faces(self, up_tuple, right_tuple, down_tuple, left_tuple):
        # TODO: Agregar algo para que valide que las caras realmente se ajusten? onda que
        #  si la cara central es de (2, 2) que el de la izquierda sea de (2, 100) y no de (100, 100).
        (up, up_d), (right, right_d), (down, down_d), (left, left_d) = up_tuple, right_tuple, down_tuple, left_tuple
        self.up, self.right, self.down, self.left = up, right, down, left
        self._direc_list = [Direc(s) for s in [up_d, right_d, down_d, left_d]]
        self._slice_list = [generate_slice(d) for d in self._direc_list]

    def rotate(self, times: int):
        times = times % 4
        # TODO: Agregar validadores para chequear que el movimiento se puede hacer (?)
        roll = deque(self.pieces)
        roll.rotate(times)
        self.pieces = roll
        self.central_face = np.rot90(self.central_face, times)

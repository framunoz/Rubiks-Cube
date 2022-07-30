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


_LIST_DIRECTIONS_TO_INV = [
    {Direc.U, Direc.R}, {Direc.U},
    {Direc.D, Direc.L}, {Direc.D}
]


def generate_slice(direction) -> TupleSlice:
    return _DICT_TUPLE_SLICES.get(direction, (_ALL, _ALL))

    
def color_to_str(list_of_colors: List[Color]) -> List[str]:
    return [repr(c) for c in list_of_colors]


def invert_piece(piece, direction=-1) -> List[Color]:
    if direction < 0:
        return list(reversed(piece))
    return piece


def rotate_pieces(list_of_pieces, times) -> List[List[Color]]:
    even, odd = [1, 1, -1, -1], [1, -1, -1, 1]
    list_of_directions = [even, odd, even, odd]
    new_list_of_pieces = deque()
    for piece, directions in zip(list_of_pieces, list_of_directions):
        new_list_of_pieces.append(invert_piece(piece, directions[times]))
    new_list_of_pieces.rotate(times)
    return new_list_of_pieces


def invert_piece(piece, direction) -> List[Color]:
    if direction < 0:
        return list(reversed(piece))
    return piece


def rotate_pieces(list_of_pieces, times) -> List[List[Color]]:
    even, odd = [1, 1, -1, -1], [1, -1, -1, 1]
    list_of_directions = [even, odd, even, odd]
    new_list_of_pieces = deque()
    for piece, directions in zip(list_of_pieces, list_of_directions):
        new_list_of_pieces.append(invert_piece(piece, directions[times]))
    new_list_of_pieces.rotate(times)
    return new_list_of_pieces


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

    def __getitem__(self, index) -> np.ndarray[Color]:
        return self.central_face.__getitem__(index)

    def __setitem__(self, index, item):
        self.central_face[index] = item

    @property
    def faces(self) -> List[Face]:
        return [self.up, self.right, self.down, self.left]

    def _invert_pieces(self, list_of_pieces) -> List[List[Color]]:
        to_return: List[List[Color]] = [list(elem) for elem in list_of_pieces]
        for i, dir_set in enumerate(_LIST_DIRECTIONS_TO_INV):
            if self._direc_list[i] in dir_set:
                to_return[i] = invert_piece(to_return[i])
        return to_return

    @property
    def pieces(self) -> List[List[Color]]:
        u_s, r_s, d_s, l_s = self._slice_list
        return self._invert_pieces([self.up[u_s], self.right[r_s], self.down[d_s], self.left[l_s]])

    @pieces.setter
    def pieces(self, value_to_set):
        u_s, r_s, d_s, l_s = self._slice_list
        self.up[u_s], self.right[r_s], self.down[d_s], self.left[l_s] = self._invert_pieces(value_to_set)

    def repr_central_face(self, space: int = 0) -> str:
        str_to_return = ""
        for row in self.central_face:
            str_to_return += " " * space + " ".join([repr(e) for e in row]) + "\n"
        return str_to_return[:-1]

    def __repr__(self):
        if None in self.faces:
            return self.repr_central_face()

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
        self.pieces = rotate_pieces(self.pieces, times)
        self.central_face = np.rot90(self.central_face, 4-times)

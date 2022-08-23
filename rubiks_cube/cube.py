from __future__ import annotations

import copy
from typing import List, Tuple

from rubiks_cube.faces import Face
from rubiks_cube.movements import CubeMove
from rubiks_cube.utils import Color, Direction

# Directions
_U, _R, _D, _L = Direction.U, Direction.R, Direction.D, Direction.L


class NotPermittedMovementError(Exception):
    """
    Custom error in the cases of a user make a wrong movement.
    """
    pass


class RubikCube:
    """Class that represents a Rubik's Cube."""

    def __init__(self, up: Face, left: Face, front: Face, right: Face, back: Face, down: Face,
                 permitted_movements: set[CubeMove] = None):
        # TODO: Podría ser util tener un validador para determinar si las caras coinciden 
        #  en las dimensiones.

        # Different Faces
        self.front: Face = front
        self.back: Face = back
        self.left: Face = left
        self.right: Face = right
        self.up: Face = up
        self.down: Face = down

        # Attach every face with its correspondent faces
        front.add_faces(
            up_tuple=(up, _D), right_tuple=(right, _L), down_tuple=(down, _U), left_tuple=(left, _R))
        back.add_faces(
            up_tuple=(up, _U), right_tuple=(left, _L), down_tuple=(down, _D), left_tuple=(right, _R))
        left.add_faces(
            up_tuple=(up, _L), right_tuple=(front, _L), down_tuple=(down, _L), left_tuple=(back, _R))
        right.add_faces(
            up_tuple=(up, _R), right_tuple=(back, _L), down_tuple=(down, _R), left_tuple=(front, _R))
        up.add_faces(
            up_tuple=(back, _U), right_tuple=(right, _U), down_tuple=(front, _U), left_tuple=(left, _U))
        down.add_faces(
            up_tuple=(front, _D), right_tuple=(right, _D), down_tuple=(back, _D), left_tuple=(left, _D))

        # Set of permitted movements
        self.permitted_movements: set[CubeMove] = permitted_movements or {m for m in CubeMove}
        
        # Dimensions
        self.dims = self.front.shape[0], self.front.shape[1], self.right.shape[1]

    @classmethod
    def from_dims(cls, dims: Tuple[int, int, int], permitted_movements: set[CubeMove] = None) -> RubikCube:
        """Factory method that generates a RubikCube instance given the dimensions and permitted movements."""
        height, width, length = dims
        cls_to_return = cls(
            front=Face.from_color(Color.RED, (height, width)), back=Face.from_color(Color.ORANGE, (height, width)),
            left=Face.from_color(Color.GREEN, (height, length)), right=Face.from_color(Color.BLUE, (height, length)),
            up=Face.from_color(Color.WHITE, (length, width)), down=Face.from_color(Color.YELLOW, (length, width)),
            permitted_movements=permitted_movements,
        )
        return cls_to_return

    @property
    def faces(self):
        """Iterates over every face in the current cube."""
        return self.up, self.left, self.front, self.right, self.back, self.down

    def __eq__(self, other):
        if isinstance(other, RubikCube):
            return self.faces == other.faces
        return False

    def __hash__(self):
        return hash(self.faces)

    def __copy__(self) -> RubikCube:
        up = copy.copy(self.up)
        left = copy.copy(self.left)
        front = copy.copy(self.front)
        right = copy.copy(self.right)
        back = copy.copy(self.back)
        down = copy.copy(self.down)
        # permitted_movements = copy.copy(self.permitted_movements)

        new = self.__class__(up, left, front, right, back, down, self.permitted_movements)
        new.__dict__.update(self.__dict__)

        return new

    def __deepcopy__(self, memo=None) -> RubikCube:
        if memo is None:
            memo = {}

        up = copy.deepcopy(self.up, memo)
        left = copy.deepcopy(self.left, memo)
        front = copy.deepcopy(self.front, memo)
        right = copy.deepcopy(self.right, memo)
        back = copy.deepcopy(self.back, memo)
        down = copy.deepcopy(self.down, memo)
        # permitted_movements = copy.deepcopy(self.permitted_movements, memo)

        new = self.__class__(up, left, front, right, back, down, self.permitted_movements)
        new.__dict__ = copy.deepcopy(self.__dict__, memo)

        return new

    def clone(self) -> RubikCube:
        return copy.deepcopy(self)

    def __repr__(self):
        _, _, length = self.dims

        # Up face
        str_to_return = ""
        str_to_return += self.up.repr_central_face(2 * length + 1) + "\n\n"

        # Left, front, right and back face
        left_list = self.left.repr_central_face().split("\n")
        front_list = self.front.repr_central_face().split("\n")
        right_list = self.right.repr_central_face().split("\n")
        back_list = self.back.repr_central_face().split("\n")
        for le, fr, ri, ba in zip(left_list, front_list, right_list, back_list):
            str_to_return += f"{le}  {fr}  {ri}  {ba}\n"
        str_to_return += "\n"

        # Down face
        str_to_return += self.down.repr_central_face(2 * length + 1)

        return str_to_return

    def make_a_move(self, move: CubeMove):
        """Make a move in the current cube."""
        if move not in self.permitted_movements:
            raise NotPermittedMovementError(
                f"Movement not allowed. Please choose one of the list: {self.permitted_movements}.")
        move.move_the_cube(self)

    def make_movements_from_list(self, list_of_moves: List[CubeMove]):
        """Make movements from a list of CubeMoves."""
        for move in list_of_moves:
            self.make_a_move(move)

    def make_movements_from_str(self, str_of_moves: str):
        """Make movements from a string, separated by spaces."""
        list_of_str = str_of_moves.split()
        list_of_moves = [CubeMove.from_str(m_str) for m_str in list_of_str]
        self.make_movements_from_list(list_of_moves)

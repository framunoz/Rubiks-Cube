from __future__ import annotations

from typing import Tuple

from rubiks_cube.faces import Face
from rubiks_cube.movements import CubeMove
from rubiks_cube.utils import Color


class NotPermittedMovementError(Exception):
    """
    Custom error in the cases of a user make a wrong movement.
    """
    pass


class RubikCube:
    """Class that represents a Rubik's Cube."""

    def __init__(self, front: Face, back: Face, left: Face, right: Face, up: Face, down: Face,
                 permitted_movements: set[CubeMove] = None):
        # TODO: Podría ser util tener un validador para determinar si las caras coinciden en las dimensiones.
        # Different Faces
        self.front: Face = front 
        self.back: Face = back 
        self.left: Face = left 
        self.right: Face = right 
        self.up: Face = up
        self.down: Face = down

        # Attach every face
        front.add_faces(
            up_tuple=(up, 2), right_tuple=(right, 3), down_tuple=(down, 0), left_tuple=(left, 1))
        back.add_faces(
            up_tuple=(up, 0), right_tuple=(left, 3), down_tuple=(down, 2), left_tuple=(right, 1))
        left.add_faces(
            up_tuple=(up, 3), right_tuple=(front, 3), down_tuple=(down, 3), left_tuple=(back, 1))
        right.add_faces(
            up_tuple=(up, 1), right_tuple=(back, 3), down_tuple=(down, 1), left_tuple=(front, 1))
        up.add_faces(
            up_tuple=(back, 0), right_tuple=(right, 0), down_tuple=(front, 0), left_tuple=(left, 0))
        down.add_faces(
            up_tuple=(front, 2), right_tuple=(right, 2), down_tuple=(back, 2), left_tuple=(left, 2))

        # Set of permitted movements
        self.permitted_movements: set[CubeMove] = permitted_movements or {m for m in CubeMove}
        
        # Dimensions
        self.dims = self.front.shape[0], self.front.shape[1], self.right.shape[1]

    @classmethod
    def from_dims(cls, dims: Tuple[int, int, int], permitted_movements: set[CubeMove] = None) -> RubikCube:
        """Factory method that generates a RubikCube instance given the dimensions and permitted movements."""
        height, width, length = dims# Different Faces
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
        return [self.up, self.left, self.front, self.right, self.back, self.down]

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
        for le, f, r, b in zip(left_list, front_list, right_list, back_list):
            str_to_return += f"{le}  {f}  {r}  {b}\n"
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

from typing import Tuple

from rubiks_cube.faces import Face
from rubiks_cube.movements import Movement
from rubiks_cube.utils import Color


class NotPermittedMovementError(Exception):
    """
    Custom error in the cases of a user make a wrong movement.
    """
    pass


class RubikCube:
    def __init__(self, dims: Tuple[int, int, int], permitted_movements: set[Movement] = None):
        # Dimensions
        height, width, length = self.dims = dims

        # Set of permitted movements
        self.permitted_movements = permitted_movements or Movement

        # Different Faces
        front = Face(Color.RED, (height, width))
        back = Face(Color.ORANGE, (height, width))
        left = Face(Color.GREEN, (height, length))
        right = Face(Color.BLUE, (height, length))
        up = Face(Color.WHITE, (length, width))
        down = Face(Color.YELLOW, (length, width))

        # Attach every face
        front.add_faces(up_tuple=(up, 2), right_tuple=(right, 3),
                        down_tuple=(down, 0), left_tuple=(left, 1))
        back.add_faces(up_tuple=(up, 0), right_tuple=(left, 3),
                       down_tuple=(down, 2), left_tuple=(right, 1))
        left.add_faces(up_tuple=(up, 3), right_tuple=(front, 3),
                       down_tuple=(down, 3), left_tuple=(back, 1))
        right.add_faces(up_tuple=(up, 1), right_tuple=(back, 3),
                        down_tuple=(down, 1), left_tuple=(front, 1))
        up.add_faces(up_tuple=(back, 0), right_tuple=(right, 0),
                     down_tuple=(front, 0), left_tuple=(left, 0))
        down.add_faces(up_tuple=(front, 2), right_tuple=(right, 2),
                       down_tuple=(back, 2), left_tuple=(left, 2))

        # Make a pointer to the frontal face
        self.front: Face = front

    @property
    def back(self):
        return self.front.right.right

    @property
    def left(self):
        return self.front.left

    @property
    def right(self):
        return self.front.right

    @property
    def up(self):
        return self.front.up

    @property
    def down(self):
        return self.front.down

    @property
    def faces(self):
        return [self.up, self.left, self.front, self.right, self.back, self.down]

    def __repr__(self):
        height, width, length = self.dims
        str_to_return = ""
        str_to_return += self.up.repr_central_face(2 * length + 1) + "\n\n"
        left_list = self.left.repr_central_face().split("\n")
        front_list = self.front.repr_central_face().split("\n")
        right_list = self.right.repr_central_face().split("\n")
        back_list = self.back.repr_central_face().split("\n")
        for le, f, r, b in zip(left_list, front_list, right_list, back_list):
            str_to_return += f"{le}  {f}  {r}  {b}\n"
        str_to_return += "\n"
        str_to_return += self.down.repr_central_face(2 * length + 1)
        return str_to_return

    def make_a_move(self, move: Movement):
        if move not in self.permitted_movements:
            raise NotPermittedMovementError(
                f"Movement not allowed. Please choose one of the list: {self.permitted_movements}.")
        move.move_the_cube(self)


def main():
    rc = RubikCube((3, 2, 1), {Movement.R2, Movement.L2, Movement.U2, Movement.D2})
    print(rc, end="\n\n")
    rc.make_a_move(Movement.R2)
    print(rc)


if __name__ == '__main__':
    main()

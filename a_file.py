from rubiks_cube.cube import RubikCube
from rubiks_cube.faces import Face, rotate_pieces
from rubiks_cube.movements import CubeMove
from rubiks_cube.utils import Color


def main():
    f = Face(Color.BLUE, (2, 2))
    print(f)
    print(None in f.faces)

    rc = RubikCube((3, 2, 1), {CubeMove.R2, CubeMove.L2, CubeMove.U2, CubeMove.D2})
    print(repr(rc.front))
    print(None in rc.front.faces)
    print(rc, end="\n\n")
    rc.make_a_move(CubeMove.U2)
    print(rc.right)
    rc.make_a_move(CubeMove.R2)
    print(rc, end="\n\n")
    print(rc.right, end="\n\n")

    # pieces = rc.right.pieces
    # print(pieces)
    # print(rotate_pieces(pieces, 2))


if __name__ == '__main__':
    main()

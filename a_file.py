from rubiks_cube.cube import RubikCube
from rubiks_cube.movements import CubeMove


def main():
    rc = RubikCube((3, 2, 1), {CubeMove.R2, CubeMove.L2, CubeMove.U2, CubeMove.D2})
    print(rc, end="\n\n")
    rc.make_a_move(CubeMove.U2)
    rc.make_a_move(CubeMove.R2)
    print(rc)


if __name__ == '__main__':
    main()

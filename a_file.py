from rubiks_cube.cube import RubikCube
from rubiks_cube.movements import CubeMove
from rubiks_cube.utils import Color


def main():
    # f = Face(Color.BLUE, (2, 2))

    rc = RubikCube.from_dims(
        (3, 2, 1), 
        {CubeMove.R2, CubeMove.L2, CubeMove.U2, CubeMove.D2}
    )
    print(rc, end="\n\n")
    # list_of_movements = [
    #     CubeMove.U, CubeMove.R, CubeMove.D, CubeMove.L,
    #     CubeMove.D, CubeMove.R, CubeMove.D, CubeMove.R
    # ]
    list_of_movements = [
        CubeMove.U2, CubeMove.R2, CubeMove.D2, CubeMove.L2,
        CubeMove.D2, CubeMove.R2, CubeMove.D2, CubeMove.R2
    ]
    for m in list_of_movements:
        print(f"{m=}")
        rc.make_a_move(m)
        print(rc, end="\n\n")

    print("Faces")
    for f in rc.faces:
        print(f, end="\n\n")

    print(CubeMove.R)

    print(hash(Color.BLUE), hash(Color.BLUE))
    print(hash("blue"), hash("blue"))


if __name__ == '__main__':
    main()

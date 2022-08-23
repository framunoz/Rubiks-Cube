import matplotlib.pyplot as plt
import networkx as nx

from rubiks_cube.cube import RubikCube
from rubiks_cube.graph import make_graph
from rubiks_cube.movements import CubeMove
from rubiks_cube.utils import Color

CM = CubeMove


def main():
    # f = Face(Color.BLUE, (2, 2))

    rc = RubikCube.from_dims(
        (3, 2, 1),
        {CubeMove.R2, CubeMove.L2, CubeMove.U2, CubeMove.D2}
    )
    print(rc, end="\n\n")
    rc.make_movements_from_str("L2 U2")
    print("\n", rc, "\n", sep="")
    # list_of_movements = [
    #     CubeMove.U, CubeMove.R, CubeMove.D, CubeMove.L,
    #     CubeMove.D, CubeMove.R, CubeMove.D, CubeMove.R
    # ]
    list_of_movements = [
        CubeMove.U2, CubeMove.R2, CubeMove.D2, CubeMove.L2,
        CubeMove.D2, CubeMove.R2, CubeMove.D2, CubeMove.R2
    ]
    for m in list_of_movements:
        print(f"{m = }")
        rc.make_a_move(m)
        print(rc, end="\n\n")

    print("Faces")
    for f in rc.faces:
        print(f, end="\n\n")

    print(CubeMove.R)

    print(hash(Color.BLUE), hash(Color.BLUE))
    print(hash("blue"), hash("blue"))


def other_main():
    g = make_graph((3, 2, 1), {CM.R2, CM.U2, CM.D2})
    for i, rc in enumerate(g.nodes):
        print(f"Estado {i = }")
        print(rc)
        print("Vecinos:")
        print(g[rc])
    options = {
        'node_color': 'red',
        'node_size': 50,
        'edge_color': 'blue',
        'width': 3,
    }
    nx.draw_kamada_kawai(g, **options)
    plt.show()


if __name__ == '__main__':
    other_main()

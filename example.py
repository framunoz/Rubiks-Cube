import networkx as nx
from matplotlib import pyplot as plt

from rubiks_cube.cube import RubikCube
from rubiks_cube.graph import make_graph
from rubiks_cube.movements import CubeMove as CM
from rubiks_cube.plotters import GraphPlotter
from rubiks_cube.utils import Color


def main():
    # f = Face(Color.BLUE, (2, 2))

    rc = RubikCube.from_dims(
        (1, 3, 2),
        # {CM.R2, CM.U2, CM.D2}
    )
    print(rc, end="\n\n")
    rc = rc.make_movements("hola")
    print("\n", rc, "\n", sep="")
    # list_of_movements = [
    #     CM.U, CM.R, CM.D, CM.L,
    #     CM.D, CM.R, CM.D, CM.R
    # ]
    list_of_movements = [
        CM.U2, CM.R2, CM.D2, CM.L2,
        CM.D2, CM.R2, CM.D2, CM.R2
    ]
    for m in list_of_movements:
        print(f"{m = }")
        rc = rc.make_a_move(m)
        print(rc, end="\n\n")

    print("Faces")
    for f in rc.faces:
        print(f, end="\n\n")

    print(CM.R)

    print(hash(Color.BLUE), hash(Color.BLUE))
    print(hash("blue"), hash("blue"))


def main2():
    g: nx.Graph = make_graph(
        (1, 3, 2),
        {CM.R2, CM.L2, CM.B2}
    )
    # for i, rc in enumerate(g.nodes):
    #     print(f"Estado {i = }")
    #     print(rc)
    #     print(g.nodes[rc])
    #     print("Vecinos:")
    #     neighbors = list(g[rc].keys())
    #     neighbors.sort(key=lambda x: hash(x))
    #     print(g[rc])
    gp = GraphPlotter(g)
    gp.compute_kamada_kawai_layout()
    U, V = gp.find_bipartite()
    gp.draw()

    # Dictionaries in the convention id - Rubik's Cube. Bipartition
    print({g.nodes[n]["id"]: n for n in U})
    print({g.nodes[n]["id"]: n for n in V})

    plt.show()


def main3():
    g: nx.Graph = make_graph((1, 3, 2), {CM.R2, CM.D2, CM.U2})
    U, V = nx.algorithms.bipartite.sets(g)
    print(U, V)
    print(len(U), len(V))


if __name__ == '__main__':
    main2()

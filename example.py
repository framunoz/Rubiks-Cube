import networkx as nx
from matplotlib import pyplot as plt

from rubiks_cube.cube import RubikCube
from rubiks_cube.graph import make_graph, generate_file
from rubiks_cube.movements import CubeMove as CM
from rubiks_cube.plotters import GraphPlotter
from rubiks_cube.satisfiability import solve_clause_interpreted, generate_cnf_file
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
    n: int = len(g)
    m: int = g.number_of_edges()
    print(f"{n = }, {m = }")
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
    g: nx.Graph = make_graph((1, 3, 2), {CM.R2, CM.L2, CM.B2})
    U, V = nx.algorithms.bipartite.sets(g)
    print(U, V)
    print(len(U), len(V))


def main4():
    g: nx.Graph = make_graph((1, 3, 2), {CM.R2, CM.L2, CM.B2})
    # clauses = generate_clauses(g, 0, 1)

    # print("Generando fórmulas en CNF")
    # generate_cnf_file(g, RubikCube.from_dims((1, 3, 2)))

    print("Resolviendo primera fórmula")
    # model = solve_clause("clauses/rubik-1.cnf")
    model = solve_clause_interpreted(g, "clauses/rubik-7.cnf")

    print("Revisando parámetros")
    for v in model:
        print(v)


def main5():
    # model = solve_clause("clauses/rubik-1.cnf")
    model = solve_clause_interpreted("clauses/rubik-1.cnf")

    for v in model:
        print(v)


def main6():
    g: nx.Graph = make_graph(
        (1, 3, 3),
        {CM.R2, CM.L2, CM.B2, CM.F2}
    )
    n: int = len(g)
    m: int = g.number_of_edges()
    print(f"{n = }, {m = }")
    generate_file(g)
    generate_cnf_file(g, RubikCube.from_dims((1, 3, 3)), "clauses_1_3_3", verbose=True)

    for i, rc in enumerate(g.nodes):
        print(f"Estado {i = }")
        print(f'{rc = }')
        print(f'{g.nodes[rc] = }')
        print("Vecinos:")
        neighbors = list(g[rc].keys())
        neighbors.sort(key=lambda x: hash(x))
        print(g[rc])

    # gp = GraphPlotter(g)
    # U, V = gp.compute_bipartite_layout(scale=1, aspect_ratio=2000000000)
    # gp.compute_kamada_kawai_layout(scale=10)
    # U, V = gp.find_bipartite()
    # gp.draw()

    # Dictionaries in the convention id - Rubik's Cube. Bipartition
    # print({g.nodes[n]["id"]: n for n in U})
    # print({g.nodes[n]["id"]: n for n in V})

    # plt.show()


def main7():
    g: nx.Graph = make_graph(
        (1, 3, 3),
        {CM.R2, CM.L2, CM.B2, CM.F2}
    )
    n: int = len(g)
    m: int = g.number_of_edges()
    print(f"{n = }, {m = }")
    generate_file(g)
    generate_cnf_file(g, RubikCube.from_dims((1, 3, 3)), "clauses_1_3_3", verbose=True)


if __name__ == '__main__':
    main7()
    # main5()

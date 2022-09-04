import os.path
from itertools import product
from typing import Iterable

import networkx as nx
from pysat.formula import CNF

from rubiks_cube.cube import RubikCube
from rubiks_cube.movements import CubeMove


def make_graph(dims: tuple[int, int, int], permitted_movements: set[CubeMove] = None) -> nx.Graph:
    """
    Creates a graph with dimensions `dims` and permitted movements `permitted_movements` using a Rubik's Cube as node,
    and two Rubik's Cubes are connected if you can draw it with one movement.

    :param dims: A tuple with the dimensions of a Rubik's Cube
    :param permitted_movements: A set of permitted movements
    :return: A graph as described
    """
    # Principal Rubik's Cube
    rc = RubikCube.from_dims(dims, permitted_movements)
    # Queue to make a BFS
    queue = [rc]
    # The graph
    g = nx.Graph()
    g.add_node(rc)
    while queue:  # While d is not empty
        current_rc = queue.pop()  # Actualize the current cube
        # Make every permitted movement and add the new cube to the graph
        for m in permitted_movements:
            other_rc = current_rc.make_movements(m)
            if other_rc not in g.nodes:
                queue.append(other_rc)  # Add to the queue
                g.add_node(other_rc)  # Add to the graph
            if other_rc not in g[current_rc]:
                g.add_edge(current_rc, other_rc, move=set())
            g[current_rc][other_rc]["move"].add(m)

    def order_list_of_rc(iterable: Iterable[RubikCube]) -> list[RubikCube]:
        ordered_iterable: list[RubikCube] = list(iterable)
        ordered_iterable.sort(key=lambda x: hash(x))
        return ordered_iterable

    for i, rc in enumerate(order_list_of_rc(g.nodes)):
        g.nodes[rc]["id"] = i
    return g


def find_bipartite(g: nx.Graph) -> tuple[set[RubikCube], set[RubikCube]]:
    """
    Find a bipartite in the graph g and label it. Returns the bipartite.

    :param g: A graph.
    :return: two sets.
    """
    U, V = nx.algorithms.bipartite.sets(g)
    for n in g.nodes:
        if n in U:
            g.nodes[n].update(color="blue", bipartite=0)
        else:
            g.nodes[n].update(color="red", bipartite=1)
    return U, V


def make_simple_graph(complex_graph: nx.Graph) -> dict[int, set[int]]:
    """
    Make a simple graph (a dict of sets) from a complex graph (the nx.Graph instance).

    :param complex_graph: A complex graph.
    :return: A simple graph.
    """
    simple_graph: dict[int, set[int]] = {}
    for n in complex_graph.nodes:
        n_id: int = complex_graph.nodes[n]["id"]
        simple_graph[n_id] = {complex_graph.nodes[other]["id"] for other in complex_graph[n]}
    return simple_graph


def generate_variables(graph: nx.Graph) -> tuple[dict[tuple[int, int], int], dict[int, tuple[int, int]]]:
    neighbours = make_simple_graph(graph)

    # Making the X_{u, i} variables
    n: int = len(neighbours)
    X: dict[tuple[int, int], int] = {}
    for index, (u, i) in enumerate(product(range(n), repeat=2)):
        X[u, i] = index + 1

    X_: set[int, tuple[int, int]] = {X[k]: k for k in X.keys()}

    return X, X_


def generate_clauses(g: nx.Graph, s: int, t: int) -> list[list[int, ...]]:
    """
    Generates a codification for the SAT Solver.

    :param g: A nx.Graph instance.
    :param s: The start node's id.
    :param t: The final node's id.
    :return: A list of list with the desired codification.
    """
    X, _ = generate_variables(g)
    neighbours: dict[int, set[int]] = make_simple_graph(g)
    n: int = len(neighbours)

    # Making the clauses
    # Impose that node s has the position 0 and the node t the position (n-1)
    clauses: list[list[int, ...]] = [[X[s, 0]], [X[t, n - 1]]]

    # Each vertex has a position
    for u in range(n):
        clauses.append([X[u, i] for i in range(n)])

    # Each position has a vertex
    for i in range(n):
        clauses.append([X[u, i] for u in range(n)])

    # The set V - t
    V_m_t: set[int] = set(range(n))
    V_m_t.discard(t)

    # Verify that the path is Hamiltonian
    for u, i in zip(V_m_t, range(n - 1)):
        clauses.append([-X[u, i]] + [X[v, i + 1] for v in neighbours[u]])

    return clauses


def generate_cnf_file(graph: nx.Graph, t: RubikCube, source_path="clauses", name_format="rubik-{}.cnf"):
    """
    Creates the necessary files with the cnf format.

    :param graph: A graph to make the clauses
    :param t:
    :param source_path:
    :param name_format:
    :return:
    """
    # t id node
    t_ = graph.nodes[t]["id"]
    # Finding the bipartite
    U, V = find_bipartite(graph)
    W = V if t in U else U

    # Making the directory in the case that it does not exist
    if not os.path.isdir(source_path):
        os.mkdir(source_path)

    for s in W:
        s_ = graph.nodes[s]["id"]
        clauses = generate_clauses(graph, s_, t_)
        cnf = CNF(from_clauses=clauses)
        cnf.to_file(os.path.join(source_path, name_format.format(s_)))


def generate_file(g: nx.Graph, path=None):
    """
    Creates a file in the format "'number of nodes' 'number of edges'"
    and the different edges with its nodes.

    :param g: A graph
    :param path: A path
    :return: Nothing.
    """
    path = path or "graph.txt"

    simple_graph = make_simple_graph(g)

    def sort_list(other):
        lst = list(other)
        lst.sort()
        return lst

    with open(path, "w") as f:
        # Write n and m
        f.write(f"{len(g.nodes)} {len(g.edges)}\n")
        # Write the edges
        for u in sort_list(simple_graph.keys()):
            for v in sort_list(simple_graph[u]):
                if u < v:
                    f.write(f"{u} {v}\n")

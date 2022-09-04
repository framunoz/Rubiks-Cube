import os
from itertools import product, combinations
from typing import Optional

import networkx as nx
from pysat.formula import CNF
from pysat.solvers import Solver

from rubiks_cube.cube import RubikCube
from rubiks_cube.graph import make_simple_graph, find_bipartite


def generate_variables(graph: nx.Graph) -> tuple[dict[tuple[int, int], int], dict[int, tuple[int, int]]]:
    """
    Given a graph, generates tho dictionaries with a convention to name variables. It also returns other dictionary,
     that given an integer, returns the tuple as the convention.

    :param graph: A graph to generate the variables.
    :return: Two dictionaries. One that receives a tuple and returns an integer,
     and the other is the "inverse function".
    """
    # Making the X_{u, i} variables
    n: int = len(graph)  # Number of nodes in the graph
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
    :return: A list of list with the desired clauses.
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

    # Cardinality constraints
    for i in range(n):
        for u, v in combinations(range(n), 2):
            clauses.append([-X[u, i], -X[v, i]])

    # The set V - t
    V_m_t: set[int] = set(range(n))
    V_m_t.discard(t)

    # Verify that the path is Hamiltonian
    for u, i in zip(V_m_t, range(n - 1)):
        clauses.append([-X[u, i]] + [X[v, i + 1] for v in neighbours[u]])

    return clauses


def generate_cnf_file(graph: nx.Graph, t: RubikCube,
                      source_path="clauses", name_format="rubik-{}.cnf"):
    """
    Creates the necessary files with the cnf format.

    :param graph: A graph to make the clauses
    :param t: The final node as a RubikCube instance
    :param source_path: The source folder where the files will be saved.
    :param name_format: The format of how the files will be saved.
    :return: Nothing.
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


def solve_clause(file_name: str, solver_name="cd", use_timer=False) -> Optional[list[int]]:
    # Boolean Formula
    f = CNF(from_file=file_name)

    # Solver
    with Solver(name=solver_name, bootstrap_with=f, use_timer=use_timer) as s:
        # Solving CNF
        is_solved = s.solve()

        if is_solved:
            # Getting the model
            model: list[int] = s.get_model()

            return model

    return None


def solve_clause_interpreted(g: nx.Graph, file_name: str, solver_name="cd", use_timer=False):
    model = solve_clause(file_name, solver_name, use_timer)

    _, X_ = generate_variables(g)

    answer = [X_[k] for k in model if k > 0]
    answer.sort(key=lambda x: x[1])

    id_to_rc = {g.nodes[n]["id"]: n for n in g.nodes}

    answer_ = []
    for i, _ in answer:
        answer_.append(id_to_rc[i])

    return answer_

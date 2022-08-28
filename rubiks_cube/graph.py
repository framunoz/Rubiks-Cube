from typing import Iterable

import networkx as nx

from rubiks_cube.cube import RubikCube
from rubiks_cube.movements import CubeMove


def _order_list_of_rc(iterable: Iterable[RubikCube]) -> list[RubikCube]:
    ordered_iterable: list[RubikCube] = list(iterable)
    ordered_iterable.sort(key=lambda x: hash(x))
    return ordered_iterable


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
    g.add_node(rc, hash_id=hash(rc))
    while queue:  # While d is not empty
        current_rc = queue.pop()  # Actualize the current cube
        # Make every permitted movement and add the new cube to the graph
        for m in permitted_movements:
            other_rc = current_rc.make_movements(m)
            if other_rc not in g.nodes:
                queue.append(other_rc)  # Add to the queue
                g.add_node(other_rc, hash_id=hash(other_rc))  # Add to the graph
            if other_rc not in g[current_rc]:
                g.add_edge(current_rc, other_rc, move=set())
            g[current_rc][other_rc]["move"].add(m)

    for i, rc in enumerate(_order_list_of_rc(g.nodes)):
        g.nodes[rc]["id"] = i
    return g


def generate_file(g: nx.Graph, path=None):
    """
    Creates a file in the format "'number of nodes' 'number of edges'"
    and the different edges with its nodes.

    :param g: A graph
    :param path: A path
    :return: Nothing.
    """
    path = path or "graph.txt"

    with open(path, "w") as f:
        # Write n and m
        f.write(f"{len(g.nodes)} {len(g.edges)}\n")
        for u in _order_list_of_rc(g.nodes):
            for v in _order_list_of_rc(g[u].keys()):
                u_id, v_id = g.nodes[u]['id'], g.nodes[v]['id']
                if u_id < v_id:
                    f.write(f"{u_id} {v_id}\n")

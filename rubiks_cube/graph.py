from collections import deque

import networkx as nx

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
    d = deque([rc])
    # The graph
    g = nx.Graph()
    g.add_node(rc)
    # While d is not empty
    while d:
        # Actualize the current cube
        rc = d.pop()
        # Make every permitted movement and add the new cube to the graph
        for m in permitted_movements:
            other_rc = rc.make_a_move(m)
            if other_rc not in g.nodes:
                # Add to the queue
                d.append(other_rc)
                # Add to the graph
                g.add_node(other_rc)
            if other_rc not in g[rc]:
                g.add_edge(rc, other_rc, move=set())
            g[rc][other_rc]["move"].add(m)
    for i, n in enumerate(g.nodes):
        g.nodes[n]["id"] = i
    return g


def generate_file(g: nx.Graph, path=None):
    """
    Creates a file in the format "'number of nodes' 'number of edges'"
    and the different edges with its nodes.

    :param g: A graph
    :param path: A path
    :return: Nothing.
    """
    path = path or "file.txt"

    with open(path, "w") as f:
        # Write n and m
        f.write(f"{len(g.nodes)} {len(g.edges)}\n")
        for u in g.nodes:
            for v in g[u]:
                u_id, v_id = g.nodes[u]['id'], g.nodes[v]['id']
                if u_id < v_id:
                    f.write(f"{u_id} {v_id}\n")

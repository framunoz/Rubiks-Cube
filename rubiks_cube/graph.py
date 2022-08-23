from collections import deque

import networkx as nx

from rubiks_cube.cube import RubikCube
from rubiks_cube.movements import CubeMove


def make_graph(dims: tuple[int, int, int], permitted_movements: set[CubeMove] = None) -> nx.Graph:
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
            # g.add_edge(rc, other_rc, move=m)
    return g

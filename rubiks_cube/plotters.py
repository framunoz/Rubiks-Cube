import copy
from typing import Any

import networkx as nx
from networkx import Graph

from rubiks_cube.graph import find_bipartite


class GraphPlotter:

    def __init__(self, g: Graph):
        self.g: Graph = copy.deepcopy(g)  # The current graph
        # Personal options for the graph
        self._options: dict[str, Any] = dict(
            node_color='red', font_color='white', node_size=350, width=3,
        )
        # Update the labels
        self._options.update(
            labels={n: g.nodes[n]["id"] for n in g.nodes},
        )

    def compute_kamada_kawai_layout(self, *args, **kwargs):
        """
        Compute the Kamada Kawai layout and save the configuration in the plotting options.

        :param args: arguments for the function
        :param kwargs: key arguments for the function
        :return: Nothing.
        """
        options = dict(scale=3)
        options.update(kwargs)
        self._options.update(
            pos=nx.kamada_kawai_layout(self.g, *args, **options)
        )

    def compute_bipartite_layout(self, change_color=True, *args, **kwargs):
        U, V = self.find_bipartite(change_color=change_color)
        options = dict(scale=3)
        options.update(kwargs)
        self._options.update(
            pos=nx.bipartite_layout(self.g, U, *args, **kwargs)
        )
        return U, V

    def draw(self, *args, **kwargs):
        """
        Draw the graph with the desired configurations.

        :param args: Arguments for the draw function
        :param kwargs: Key arguments for the draw function
        :return: Nothing.
        """
        self._options.update(kwargs)
        nx.draw(self.g, *args, **self._options)

    def find_bipartite(self, change_color=True):
        """
        Find a bipartite in the graph and plot the colours of the bipartite graph.

        :param change_color: True if you want to change the color in the plot.
        :param change_layout: True if you want to change the layout in the plot.
        :return: Nothing.
        """
        U, V = find_bipartite(self.g)
        if change_color:
            colors = nx.get_node_attributes(self.g, "color")
            self._options.update(node_color=colors.values())

        return U, V

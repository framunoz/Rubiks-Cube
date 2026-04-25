import os

import networkx as nx
from matplotlib import pyplot as plt

from rubiks_cube.graph import make_graph
from rubiks_cube.movements import CubeMove as CM
from rubiks_cube.plotters import GraphPlotter


def main():
    # 1. Create the graph
    g = make_graph((3, 2, 1), {CM.R2, CM.D2, CM.U2})
    
    # 2. Setup the plotter
    gp = GraphPlotter(g)
    
    # 3. Compute layout - Using NetworkX 2.8.8 and default params
    gp.compute_kamada_kawai_layout()
    
    # 4. Find bipartite sets to set colors
    gp.find_bipartite()
    
    # 5. Draw the graph
    # Reverting to the version without font modifications
    plt.figure()
    fig = plt.gcf()
    fig.set_size_inches(8, 4.8)
    fig.patch.set_alpha(0)
    ax = plt.gca()
    ax.patch.set_alpha(0)
    
    # Use white for edges
    gp.draw(edge_color='gray')
    
    # Save the image with transparent background
    output_path = "img/graph_transparent.png"
    plt.savefig(output_path, transparent=True, dpi=300, bbox_inches='tight')
    print(f"Graph saved to {output_path}")

if __name__ == '__main__':
    main()

# Rubiks-Cube

Library that implements a representation of a
Rubik's Cube. The purpose of this implementation is
to use it for research purposes.

## How to use it?

The easiest way to create a Rubik's Cube is with
the `RubikCube` class. Here is an example:

```python
from rubiks_cube.cube import RubikCube
rc = RubikCube.from_dims((3, 2, 1))
print(rc)
```

Noting that a `RubikCube` instance is a hashable and immutable object (with the current methods).

![Representation of a Rubik's Cube of 3x2x1.](img/representation01.png)

### Making move on the Rubik's Cube

If you want to make a move on the Rubik's Cube,
you can do it like the example:

```python
from rubiks_cube.cube import RubikCube
from rubiks_cube.movements import CubeMove

rc = RubikCube.from_dims((3, 2, 1))
rc = rc.make_movements(CubeMove.L2)
print(rc)
```

![img.png](img/move_L2.png)

You can make a series of movements with a list of `CubeMove`:

```python
from rubiks_cube.cube import RubikCube
from rubiks_cube.movements import CubeMove

rc = RubikCube.from_dims((3, 2, 1))
rc = rc.make_movements([CubeMove.L2, CubeMove.U2])
print(rc)
```

![img.png](img/move_L2_U2.png)

Or with a string with the representation of `CubeMove`:

```python
from rubiks_cube.cube import RubikCube

rc = RubikCube.from_dims((3, 2, 1))
rc = rc.make_movements("L2 U2")
print(rc)
```

![img.png](img/move_L2_U2.png)

### Making the Graph

Given a set of permitted movements
<img src="https://latex.codecogs.com/gif.latex?M" />
(where the permitted movements are operations over the group of Rubik's Cube), for example,
<img src="https://latex.codecogs.com/gif.latex?M = \{U^2, R^2, D^2\}" />.
We expect to create a graph
<img src="https://latex.codecogs.com/gif.latex?G_M=(V, E_M)" />
where
<img src="https://latex.codecogs.com/gif.latex?V = \{ r | r \text{ is a Rubik's Cube} \}" />
and
<img src="https://latex.codecogs.com/gif.latex?E_M = \{ (r, t) \in V \times V | t = m(r),\ m \in M \}" />.
The described graph can be computed with the following instructions:

```python
import networkx as nx
from matplotlib import pyplot as plt

from rubiks_cube.graph import make_graph
from rubiks_cube.movements import CubeMove as CM

g: nx.Graph = make_graph(
    dims=(3, 2, 1),
    permitted_movements={CM.R2, CM.D2, CM.U2}
)
nx.draw_kamada_kawai(
    g,
    node_color="red", node_size=50,
    edge_color="blue", width=3
)
plt.show()
```

And it plots the following graph:
![A graph](img/graph.png)

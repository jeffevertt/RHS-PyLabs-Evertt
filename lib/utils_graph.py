
import matplotlib.pyplot as plt
from lib.utils import *

import matplotlib.pyplot as plt
import numpy as np

# example usage:
#   graphVector( v2(3, 2), color='red')              # draws vector (3,2) with origin at (0,0)
#   graphVector( (v2(1,0), v2(3, 2)) )               # draws vector (3,2) with origin at (1,0)
#   graphVector( [v2(1,0), v2(3, 2)] , color='blue') # draws list of vectors: (-1,7) (3,2) all with origin at (0,0)
def graphVector(vector, color = None, label = None):
    def drawSingle(start, direction, color='blue', label=None):
        ax.quiver(
            start[0], start[1], direction[0], direction[1],
            angles='xy', scale_units='xy', scale=1, color=color
        )
        if label:
            ax.text(start[0] + direction[0], start[1] + direction[1], '  ' + label,
                    color=color, fontsize=12)

    # normalize input
    if isinstance(vector, np.ndarray):
        vectors = [((0, 0), vector)]
    elif isinstance(vector, tuple):
        start, direction = vector
        vectors = [(tuple(start), np.array(direction))]
    elif isinstance(vector, list):
        vectors = []
        for v in vector:
            if isinstance(v, tuple):
                vectors.append((tuple(v[0]), np.array(v[1])))
            else:
                vectors.append(((0, 0), np.array(v)))
    else:
        raise TypeError("Unsupported vector format")

    # normalize colors and labels
    n = len(vectors)
    if isinstance(color, list):
        colors = color
    elif isinstance(color, str) or color is None:
        colors = [color] * n
    if isinstance(label, list):
        labels = label
    elif isinstance(label, str) or label is None:
        labels = [label] * n

    # Setup plot
    plt.figure()
    ax = plt.gca()
    for i, (start, direction) in enumerate(vectors):
        color = colors[i] if i < len(colors) else 'blue'
        label = labels[i] if i < len(labels) else None
        drawSingle(start, direction, color=color, label=label)

    # compute limits & show the graph
    all_x = [start[0] for start, _ in vectors] + [start[0] + dir[0] for start, dir in vectors]
    all_y = [start[1] for start, _ in vectors] + [start[1] + dir[1] for start, dir in vectors]
    max_range = max(1, max(map(abs, all_x + all_y))) + 1
    ax.set_xlim(-max_range, max_range)
    ax.set_ylim(-max_range, max_range)
    ax.set_aspect('equal')
    plt.grid(True)
    plt.axhline(0, color='gray', lw=1)
    plt.axvline(0, color='gray', lw=1)
    plt.show()


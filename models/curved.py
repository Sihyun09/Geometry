import numpy as np

from physics.vectorfield import (
    curved_field,
    direction_score
)

def simulate(a):

    x = np.linspace(0, 10, 100)

    y = a * (x - 5) ** 2

    Fx, Fy = curved_field(x, a)

    A_score = direction_score(
        Fx,
        Fy
    )

    vecs = np.column_stack([
        np.diff(x),
        np.diff(y)
    ])

    lengths = np.linalg.norm(
        vecs,
        axis=1
    )

    L = np.sum(lengths)

    D_score = (
        1
        +
        (max(y) - min(y))
        / 10
    )

    return {
        "x": x,
        "y": y,
        "A": A_score,
        "D": D_score,
        "L": L,
        "Fx": Fx,
        "Fy": Fy
    }
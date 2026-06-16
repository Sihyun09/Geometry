import numpy as np

def simulate():

    A = np.array([0, 0])
    B = np.array([10, 0])

    v = B - A

    g = np.array([1, 0])

    A_score = (
        np.dot(v, g)
        /
        (
            np.linalg.norm(v)
            *
            np.linalg.norm(g)
        )
    )

    D_score = 1.0

    L = np.linalg.norm(v)

    return {
        "x": [0, 10],
        "y": [0, 0],
        "A": A_score,
        "D": D_score,
        "L": L,
        "Fx": None,
        "Fy": None
    }
import numpy as np

def simulate(theta_deg):

    theta = np.radians(theta_deg)

    S = np.array([0, -4])
    C = np.array([5, -4])

    B1 = C + 5 * np.array([
        np.cos(theta / 2),
        np.sin(theta / 2)
    ])

    B2 = C + 5 * np.array([
        np.cos(theta / 2),
        -np.sin(theta / 2)
    ])

    g = np.array([1, 0])

    v = B1 - C

    A_score = (
        np.dot(v, g)
        /
        (
            np.linalg.norm(v)
            *
            np.linalg.norm(g)
        )
    )

    D_score = (
        1
        +
        np.linalg.norm(B1 - B2)
        / 10
    )

    L = (
        np.linalg.norm(C - S)
        +
        np.linalg.norm(B1 - C)
    )

    return {
        "x": [
            S[0], C[0], B1[0],
            None,
            C[0], B2[0]
        ],
        "y": [
            S[1], C[1], B1[1],
            None,
            C[1], B2[1]
        ],
        "A": A_score,
        "D": D_score,
        "L": L,
        "Fx": None,
        "Fy": None
    }
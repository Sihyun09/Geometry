import numpy as np

g = np.array([1, 0])

def curved_field(x, a):
    Fx = np.ones_like(x)
    Fy = -2 * a * (x - 5)
    return Fx, Fy

def direction_score(Fx, Fy):
    scores = []

    for fx, fy in zip(Fx, Fy):

        F = np.array([fx, fy])

        score = (
            np.dot(F, g)
            /
            (
                np.linalg.norm(F)
                * np.linalg.norm(g)
            )
        )

        scores.append(score)

    return np.mean(scores)
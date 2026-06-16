import numpy as np

from physics.poiseuille import flow_rate

def sensitivity_curve(
    eta,
    L,
    A_score,
    D_score
):

    r_values = np.linspace(
        0.5,
        5,
        100
    )

    E_values = []

    for r in r_values:

        Q = flow_rate(
            r,
            eta,
            L
        )

        E = (
            Q
            *
            A_score
            *
            D_score
        )

        E_values.append(E)

    return (
        r_values,
        E_values
    )
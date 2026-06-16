import numpy as np

def flow_rate(r, eta, L):
    return np.pi * r**4 / (8 * eta * L)
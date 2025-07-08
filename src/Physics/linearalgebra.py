"""'linealalgebra' module include mathematical functions for making operations with vectors

Functions:
points_distance: returns the euclidian distance between the two given positions
normalise_vector: returns the unit vector of a given vector
"""

import numpy as np

def points_distance(position_1: np.ndarray, position_2: np.ndarray) -> np.floating:
    """Returns the euclidian distance between the two given positions (3D arrays)"""
    return np.linalg.norm(position_2-position_1)

def normalise_vector(vector:np.ndarray) -> np.ndarray:   
    """Returns the unit vector of a given vector (3D array)"""
    module = np.linalg.norm(vector)
    return vector/module
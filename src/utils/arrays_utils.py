"""This module introduces the neccesary functions for 

Functions:
stack_positions: Stack the positions of multiple particles into a single numpy array.
"""
import numpy as np
from functools import wraps
from typing import Callable, Any, ParamSpec
P = ParamSpec('P')  # For type hinting *args, **kwargs
from icecream import ic


import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from settings import CONFIGURATION

def stack_positions(*particles_positions: np.ndarray) -> np.ndarray:
    """Stack the positions of multiple particles into a single numpy array.
    
    Arguments:
    *particles_positions: [m] Variable number of numpy arrays of shape n×3 being n: number of time steps; and 3: x, y, z coordinates.
    
    Returns:
    [m] numpy array of shape n×m×3 being n: number of time steps; m: number of particles; and 3: x, y, z coordinates.
    """
    return np.stack(particles_positions, axis=1)

def rotation_matrix_x(phi: float) -> np.ndarray:
    s = np.sin(phi)
    c = np.cos(phi)
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])

def rotation_matrix_y(theta: float) -> np.ndarray:
    s = np.sin(theta)
    c = np.cos(theta)
    return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])

def rotation_matrix_z(psi: float) -> np.ndarray:
    s = np.sin(psi)
    c = np.cos(psi)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])

def rotation_matrix(phi: float = 0., theta: float = 0., psi: float = 0.) -> np.ndarray:
    return rotation_matrix_x(phi) @ rotation_matrix_y(theta) @ rotation_matrix_z(psi)

def rotation_matrix_axis(axis: int | str, angle: float) -> np.ndarray:
    """Return the rotation matrix for a given axis (1: x, 2: y, 3: z) and angle."""
    match str(axis):
        case "0" | "x":
            return rotation_matrix_x(angle)
        case "1" | "y":
            return rotation_matrix_y(angle)
        case "2" | "z":
            return rotation_matrix_z(angle)
        case _:
            raise ValueError(f"Invalid axis: {axis!r} is not (1, 2, 3)")

def rotation_matrix_sequenced(angle_1: float = 0., angle_2: float = 0., angle_3: float = 0., sequence: str = "xyz") -> np.ndarray:
    angles = angle_1, angle_2, angle_3
    rotation_matrix = np.identity(3)
    for axis, angle in zip(sequence, angles):
        rotation_matrix = rotation_matrix_axis(axis, angle) @ rotation_matrix
    return rotation_matrix
    


if __name__ == "__main__":
    a = np.array([1, 2, 3])
    rot1 = rotation_matrix(0.5, 1, 2)
    rot2 = rotation_matrix_sequenced(0.5, 1, 2)
    ic(rot1 == rot2)


    

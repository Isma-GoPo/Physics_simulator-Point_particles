"""This module introduces the neccesary functions for printing an animation of the simulation

Functions:
stack_positions: Stack the positions of multiple particles into a single numpy array.
"""
import numpy as np
from functools import wraps
from typing import Callable, Any, ParamSpec
P = ParamSpec('P')  # For type hinting *args, **kwargs

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

def limit_force_module(force_func: Callable[P, np.ndarray], max_force_module: float | np.ndarray = CONFIGURATION.simulation.max_allowed_force) -> Callable[P, np.ndarray]: # type: ignore
    @wraps(force_func) # Copy attributes (e.g. `__doc__`) from the wrapped function (debbuging)
    def wrapper_function(*args, **kwargs):
        return_force = force_func(*args, **kwargs)
        return_force_module = np.linalg.norm(return_force)
        return return_force if return_force_module <= max_force_module else max_force_module * return_force/return_force_module
    return wrapper_function

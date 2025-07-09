"""This module introduces the neccesary functions for printing an animation of the simulation

Functions:
stack_positions: Stack the positions of multiple particles into a single numpy array.
"""
import numpy as np

def stack_positions(*particles_positions: np.ndarray) -> np.ndarray:
    """Stack the positions of multiple particles into a single numpy array.
    
    Arguments:
    *particles_positions: [m] Variable number of numpy arrays of shape n×3 being n: number of time steps; and 3: x, y, z coordinates.
    
    Returns:
    [m] numpy array of shape n×m×3 being n: number of time steps; m: number of particles; and 3: x, y, z coordinates.
    """
    return np.stack(particles_positions, axis=1)
"""This module introduces functions for initialasing just a Particle in some default ways

Functions:
"""

import numpy as np

# Relative imports
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import physics

def free_falling_particle(initial_position: np.ndarray | None = None) -> physics.Particle:
    """Creates a particle with mass=1, Vx=1 and with gravity field."""
    initial_position = initial_position if initial_position is not None else np.zeros(3)
    particle = physics.Particle(1.0, initial_position=initial_position, initial_velocity = np.array([1.0,0.0,0.0]), acceleration_field = physics.GRAVITY_FIELD)
    return particle

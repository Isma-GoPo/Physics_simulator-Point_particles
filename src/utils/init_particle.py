"""This module introduces functions for initialasing just a Particle in some default ways

Functions:
print_simulation_static: Open a window to show a static plot of the position of one particle.
print_simulation_animation: Open a window to show the simulation animation of the position of one particle.
"""

import numpy as np

# Relative imports
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import physics
from constants import *

def free_falling_particle() -> physics.Particle:
    """Creates a particle with mass=1, Vx=1 and with gravity field."""
    particle = physics.Particle(1.0, initial_velocity = np.array([1.0,0.0,0.0]), acceleration_field = physics.GRAVITY)
    return particle
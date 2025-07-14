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

def free_falling_particle(initial_position: np.ndarray | None = None) -> physics.Particle:
    """Creates a particle with mass=1, Vx=1 and with gravity field."""
    initial_position = initial_position if initial_position is not None else np.zeros(3)
    particle = physics.Particle(1.0, initial_position=initial_position, initial_velocity = np.array([1.0,0.0,0.0]), acceleration_field = physics.GRAVITY)
    return particle



def orbiting_particles(initial_position: np.ndarray | None = None) -> physics.ParticleSpace:
    """Creates a particle space with mass=1, Vx=1 and with gravity field."""
    initial_position = initial_position if initial_position is not None else np.array([0.0, 0.0, 1.])
    initial_velocity = np.array([0.5, 0.0, 0.0])  # Perpendicular to the position vector for circular orbit
    space = physics.ParticleSpace()
    space.append(physics.Particle(1.0, initial_position=initial_position, initial_velocity = initial_velocity))
    space.append(physics.Particle(1.0, initial_position=-initial_position, initial_velocity = -initial_velocity))
    return space
"""This module introduces functions for initialasing just a Particle in some default ways

Functions:
"""

import numpy as np
from functools import partial

# Relative imports
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import physics

def orbiting_particles(initial_position: np.ndarray | None = None) -> physics.ParticleSpace:
    """Creates a particle space with mass=1, Vx=1 and with gravity field."""
    initial_position = initial_position if initial_position is not None else np.array([0.0, 0.0, 1.])
    initial_velocity = np.array([0.5, 0.0, 0.0])  # Perpendicular to the position vector for circular orbit
    space = physics.ParticleSpace()
    space.append(physics.Particle(1.0, initial_position=initial_position, initial_velocity = initial_velocity))
    space.append(physics.Particle(1.0, initial_position=-initial_position, initial_velocity = -initial_velocity))
    space.set_forces_to_apply(couple_forces_array=(physics.dynamics.forces.cinematic_atraction_force,))
    return space


def orbiting_decelerating_particles(initial_position: np.ndarray | None = None) -> physics.ParticleSpace:
    """Creates a particle space with mass=1, Vx=1 and with gravity field."""
    initial_position = initial_position if initial_position is not None else np.array([0.0, 0.0, 1.])
    initial_velocity = np.array([0.5, 0.0, 0.0])  # Perpendicular to the position vector for circular orbit
    space = physics.ParticleSpace()
    space.append(physics.Particle(1.0, initial_position=initial_position, initial_velocity = initial_velocity))
    space.append(physics.Particle(1.0, initial_position=-initial_position, initial_velocity = -initial_velocity))
    space.set_forces_to_apply(couple_forces_array=(physics.dynamics.forces.cinematic_atraction_force,),
                              single_forces_array=(partial(physics.dynamics.forces.viscosity_force,viscosity_constant=0.1),))
    return space

def circular_motion_particle(initial_position: np.ndarray | None = None) -> physics.ParticleSpace:
    """Creates a particle space with mass=1, Vx=1 and with gravity field."""
    initial_position = initial_position if initial_position is not None else np.array([0.0, 0.0, 1.])
    initial_velocity = np.array([1, 0.0, 0.0])  # Perpendicular to the position vector for circular orbit
    space = physics.ParticleSpace()
    space.append(physics.Particle(1.0, initial_position=initial_position, 
                                  initial_velocity = initial_velocity, 
                                  acceleration_field=np.array([0.0, 0.0, -0.2])))
    space.set_forces_to_apply(single_forces_array=( partial(physics.dynamics.forces.cinematic_cross_velocity_force, field_vector=np.array([0.0, -1.0, 0.0])), ))
    return space
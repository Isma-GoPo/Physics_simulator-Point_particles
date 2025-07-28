"""This module introduces functions for initialasing just a Particle in some default ways

Functions:
"""

import numpy as np
from functools import partial

# My modules
from .arrays_utils import rotation_matrix_axis

# Relative imports
import sys; import os; sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import physics


def three_elliptical_orbits() -> tuple[physics.ParticleSpace, dict]:
    """
    Creates a particle space with three orbiting particle with symetric ellipsis

    Return:
    - Space particle of three particles rotated 120º
    - Custom settings dictionary for configuration: set simulation and adaptability
    """
    custom_settings = {
        "simulation": {
            "simulation_time": 40,
            "time_step": 0.01,
            "min_relative_time_step_reduction": 1e2,
            "adaptability": {
                "is_adaptive": True,
                "max_quantile": 1.1,
                "quantile_ignored_extremes": 15,
            },
        },
    }

    distance:float = 2
    velocity:float = 0.3

    rot = partial(rotation_matrix_axis, "y")
    rot_2 = rot(2*np.pi*1/3)
    rot_3 = rot(2*np.pi*2/3)

    distance_1 = np.array([0.0, 0.0, distance])
    velocity_2 = np.array([-velocity, 0.0, 0.0])

    space = physics.ParticleSpace()
    space.append(physics.Particle(1.0, 
        initial_position=np.array(distance_1),
        initial_velocity= np.array(velocity_2),
        ))
    space.append(physics.Particle(1.0, 
        initial_position=np.array(rot_2 @ distance_1),
        initial_velocity= np.array(rot_2 @ velocity_2),
        ))
    space.append(physics.Particle(1.0, 
        initial_position=np.array(rot_3 @ distance_1),
        initial_velocity= np.array(rot_3 @ velocity_2),
        ))
    
    space.set_forces_to_apply(couple_forces_array=(physics.dynamics.forces.cinematic_atraction_force,))

    return space, custom_settings

def solar_system() -> tuple[physics.ParticleSpace, dict]:
    """Creates a particle space simulating the solar system until mars.
    
    Return:
    - Space particle with sun, mercury, venus, earth with moon and mars
    - Custom settings dictionary for configuration: set simulation, plotting, dot_sizes
    """
    solar_system_data=[[1.989e30, 0.0, 0.0], #sun
                       [3.285e23, 47e9, 58.97e3], #mercury
                       [4.87e24, 107.48e9, 36.259e3], #venus
                       [5.972e24, 147.098e9, 30.29e3], #earth
                       [6.4169e23, 206.62e9, 26.50e3], #mars
                       [7.342e22, 147.098e9+363e6, 30.29e3+1.082e3], #moon
                      ]
    
    custom_settings = {
        "simulation": {
            "simulation_time": 3.156e+7,
            "time_step": 8640,
            "is_adaptative": True,
            "max_velocity_diff": 200
        },
        "plotting": {
            "plotting_time": 10,
            "refresh_rate": 20,
            "dot_sizes": {
                "min": 15.0,
                "max": 75.0,
                "difference": 12.0,
                "exponent_factor": 0.66
            }
        }
    }

    space = physics.ParticleSpace()
    for mass, x, v in solar_system_data:
        space.append(physics.Particle(mass, 
            initial_position=np.array([x, 0.0, 0.0]), 
            initial_velocity = np.array([0.0, 0.0, v])))

    space.set_forces_to_apply(couple_forces_array=(physics.dynamics.forces.gravitational_force,),
                              single_forces_array=())
    return space, custom_settings

def two_particles_from_repose(initial_position: np.ndarray | None = None) -> tuple[physics.ParticleSpace, dict]:
    """Creates a particle space with mass=1, Vx=1 and with gravity field."""
    custom_settings = {
        "simulation": {
            "simulation_time": 96213*2, #1.05,
            "time_step": 10.,
            "min_relative_time_step_reduction": 1e2,
            "adaptability": {
                "is_adaptive": True,
                "max_quantile": 4.,
                "quantile_ignored_extremes": 10.,
                "max_absolute_value": np.inf,
            },
            
        },
        "plotting": {
            "plotting_time": 3.,
            "refresh_rate": 20,
            "do_repeat": False
        }
    }

    initial_position = initial_position if initial_position is not None else np.array([0.0, 0.0, 0.5])
    space = physics.ParticleSpace()
    space.append(physics.Particle(1.0, initial_position=np.array(initial_position)))
    space.append(physics.Particle(1.0, initial_position=np.array(-initial_position)))
    space.set_forces_to_apply(couple_forces_array=(physics.dynamics.forces.gravitational_force,))
    return space, custom_settings

def two_particles_from_repose_adaptative(initial_position: np.ndarray | None = None) -> tuple[physics.ParticleSpace, dict]:
    """Creates a particle space with mass=1, Vx=1 and with gravity field."""
    custom_settings = {
        "simulation": {
            "simulation_time": 96213*2,
            "time_step": 100,
            "is_adaptative": True,
            "max_velocity_diff": 0.00005
        },
        "plotting": {
            "plotting_time": 3,
            "refresh_rate": 20,
            "do_repeat": False
        }
    }

    initial_position = initial_position if initial_position is not None else np.array([0.0, 0.0, 0.5])
    space = physics.ParticleSpace()
    space.append(physics.Particle(1.0, initial_position=np.array(initial_position)))
    space.append(physics.Particle(1.0, initial_position=np.array(-initial_position)))
    space.set_forces_to_apply(couple_forces_array=(physics.dynamics.forces.gravitational_force,))
    return space, custom_settings

def orbiting_decelerating_particles(initial_position: np.ndarray | None = None) -> tuple[physics.ParticleSpace, dict]:
    """Creates a particle space with mass=1, Vx=1 and with gravity field."""
    custom_settings = {
        "simulation": {
            "simulation_time": 40,
            "time_step": 0.01,
            #"min_relative_time_step_reduction": 3e1,
            #"adaptability": {
            #    "is_adaptive": True,
            #    "max_quantile": 1.1,
            #    "quantile_ignored_extremes": 20,
            #},
        },
        "plotting": {
            "plotting_time": 10,
            "refresh_rate": 20,
            "do_repeat": False
        }
    }

    initial_position = initial_position if initial_position is not None else np.array([0.0, 0.0, 1.])
    initial_velocity = np.array([0.5, 0.0, 0.0])  # Perpendicular to the position vector for circular orbit
    space = physics.ParticleSpace()
    space.append(physics.Particle(1.0, initial_position=initial_position, initial_velocity = initial_velocity))
    space.append(physics.Particle(1.0, initial_position=-initial_position, initial_velocity = -initial_velocity))
    space.set_forces_to_apply(couple_forces_array=(physics.dynamics.forces.cinematic_atraction_force,),
                              single_forces_array=(partial(physics.dynamics.forces.viscosity_force,viscosity_constant=0.1),))
    return space, custom_settings

def orbiting_particles(initial_position: np.ndarray | None = None) -> physics.ParticleSpace:
    """Creates a particle space with mass=1, Vx=1 and with gravity field."""
    initial_position = initial_position if initial_position is not None else np.array([0.0, 0.0, 1.])
    initial_velocity = np.array([0.5, 0.0, 0.0])  # Perpendicular to the position vector for circular orbit
    space = physics.ParticleSpace()
    space.append(physics.Particle(1.0, initial_position=initial_position, initial_velocity = initial_velocity))
    space.append(physics.Particle(1.0, initial_position=-initial_position, initial_velocity = -initial_velocity))
    space.set_forces_to_apply(couple_forces_array=(physics.dynamics.forces.cinematic_atraction_force,))
    return space


def circular_motion_particle(initial_position: np.ndarray | None = None) -> physics.ParticleSpace:
    """Creates a particle space with mass=1, Vx=1 and with gravity field."""
    initial_position = initial_position if initial_position is not None else np.array([0.0, 0.0, 1.])
    initial_velocity = np.array([1, 0.0, 0.0])  # Perpendicular to the position vector for circular orbit
    space = physics.ParticleSpace()
    space.append(physics.Particle(1.0, initial_position=initial_position, 
                                  initial_velocity = initial_velocity))
    space.set_forces_to_apply(single_forces_array=( partial(physics.dynamics.forces.cinematic_cross_velocity_force, field_vector=np.array([0.0, -1.0, 0.0])), ))
    return space

def circular_motion_decelerating_particle(initial_position: np.ndarray | None = None) -> physics.ParticleSpace:
    """Creates a particle space with mass=1, Vx=1 and with gravity field."""
    initial_position = initial_position if initial_position is not None else np.array([0.0, 0.0, 1.])
    initial_velocity = np.array([1, 0.0, 0.0])  # Perpendicular to the position vector for circular orbit
    space = physics.ParticleSpace()
    space.append(physics.Particle(1.0, initial_position=initial_position, 
                                  initial_velocity = initial_velocity))
    space.set_forces_to_apply(single_forces_array=( partial(physics.dynamics.forces.cinematic_cross_velocity_force, field_vector=np.array([0.0, -1.0, 0.0])), 
                                                   partial(physics.dynamics.forces.viscosity_force,viscosity_constant=0.1)))
    return space

def circular_motion_accelerated_particle(initial_position: np.ndarray | None = None) -> physics.ParticleSpace:
    """Creates a particle space with mass=1, Vx=1 and with gravity field."""
    initial_position = initial_position if initial_position is not None else np.array([0.0, 0.0, 1.])
    initial_velocity = np.array([1, 0.0, 0.0])  # Perpendicular to the position vector for circular orbit
    space = physics.ParticleSpace()
    space.append(physics.Particle(1.0, initial_position=initial_position, 
                                  initial_velocity = initial_velocity, 
                                  acceleration_field=np.array([0.0, 0.0, -0.2])))
    space.set_forces_to_apply(single_forces_array=( partial(physics.dynamics.forces.cinematic_cross_velocity_force, field_vector=np.array([0.0, -1.0, 0.0])), ))
    return space
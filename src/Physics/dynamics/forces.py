"""This module contains dynamic functions to calculate forces that affect particles

Functions:
- Fictional forces: forces created for testing and creating interesting simulations
  - Single forces: only operates whith and over one particle
    - cinematic_cross_velocity_force: force perpendicular to the field and velocity -> Allows circular motion
  - Couple forces: operates whith and over couple of particles (symmetrically)
    - cinematic_atraction_force: force inversily proportional to the square distance
- Realistic forces: realistic forces
  - Single forces:
    - viscosity_force: force depending of the particle velocity
  - Couple forces:
    - gravitational_force: Newton gravitational force between two particles
"""
import numpy as np
#from typing import Callable, Any # Allow to use Callable (what means function) for type hints (specifying the input output of the function as argument)
from functools import partial, wraps
from icecream import ic

# My modules

# Relative imports
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from particle import Particle
from physics.physics_constants import *
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'utils')))



# --- Fictional forces functions --- 

# Single forces

def cinematic_cross_velocity_force(particle: Particle, field_vector: np.ndarray | None = None) -> np.ndarray:
    """Calculate a force perpendicular to the field and velocity -> Allows circular motion."""
    velocity_vector: np.ndarray = particle.velocity.copy()
    field_vector = field_vector if field_vector is not None else np.array([0.0, -1.0, 0.0])  # Default field vector
    force: np.ndarray = np.linalg.cross(velocity_vector, field_vector)
    return force

# Couple forces

def cinematic_atraction_force(particle1: Particle, particle2: Particle, atraction_constant: np.floating|float = 1.0) -> np.ndarray:
    """Calculate a unitary force between two particles, inversily proportional to the square distance."""
    distance_vector: np.ndarray = particle2.position - particle1.position
    distance: np.floating = np.linalg.norm(distance_vector)
    force_module: np.floating = atraction_constant / distance**2
    force_direction: np.ndarray = distance_vector / distance if distance != 0 else np.zeros(3) # Force = 0 if same position
    return force_module * force_direction

# --- Realistic forces functions ---

# Single forces

def viscosity_force(particle: Particle, viscosity_constant: np.floating|float = 1.0) -> np.ndarray:
    """Calculate a unitary viscosity force depending of the particle velocity."""
    velocity_vector: np.ndarray = particle.velocity.copy()
    velocity_module: np.floating = np.linalg.norm(velocity_vector)
    force_module: np.floating = viscosity_constant * velocity_module
    force_direction: np.ndarray = - velocity_vector / velocity_module if velocity_module != 0 else np.zeros(3)
    return force_module * force_direction
#unitary_viscosity_force = partial(viscosity_force, viscosity_constant=1.0)

# Couple forces

def gravitational_force(particle1: Particle, particle2: Particle) -> np.ndarray:
    """Calculate the Newton gravitational force between two particles."""
    distance_vector: np.ndarray = particle2.position - particle1.position
    distance: np.floating = np.linalg.norm(distance_vector)
    force_module: np.floating = GRAVITATIONAL_CONSTANT * (particle1.mass * particle2.mass) / distance**2
    force_direction: np.ndarray = distance_vector / distance if distance != 0 else np.zeros(3) # Force = 0 if same position
    return force_module * force_direction
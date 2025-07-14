"""This module contains dynamics operations to calculate forces

Functions:
"""
import numpy as np
#from typing import Callable, Any # Allow to use Callable (what means function) for type hints (specifying the input output of the function as argument)

# My modules

# Relative imports
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from particle import Particle
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'utils')))
from arrays_utils import limit_force_module

# Forces functions
@limit_force_module
def gravitational_force(particle1: Particle, particle2: Particle) -> np.ndarray:
    """Calculate the gravitational force between two particles."""
    distance_vector: np.ndarray = particle2.position - particle1.position
    distance: np.floating = np.linalg.norm(distance_vector)
    force_module: np.floating = (particle1.mass * particle2.mass) / distance**2
    force_direction: np.ndarray = distance_vector / distance if distance != 0 else np.zeros(3)
    return force_module * force_direction
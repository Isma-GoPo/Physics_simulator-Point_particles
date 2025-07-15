"""DEPRECATED: This module is deprecated and should not be used.

This module contains dynamic operations which take self or couple particles as arguments and operate on them.
(These operations are used in the `ParticleSpace` class to advance the simulation.)

Functions:
"""
import numpy as np
from icecream import ic
from functools import wraps
from typing import Callable, Any # Allow to use Callable (what means function) for type hints (specifying the input output of the function as argument)

# Relative imports
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from particle import Particle
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'utils')))
from arrays_utils import limit_force_module
# ---

# Decorators / higher-order functions
def force_applier(force_func: Callable[[Particle, Particle], np.ndarray] | Any) -> Callable[[Particle, Particle], None] | Any:
    """Decorator to apply a force (returned by force_func) to both particles.
    
    Arguments:
    force_func: Callable[[Particle, Particle, *args, **kwargs], np.ndarray] -> A function that takes a Particle / couple of Particles and returns a force.
    
    Returns:
    Callable[[Particle, Particle, *args, **kwargs], None] -> A function that takes a couple of particles and applies the force.
    """
    @wraps(force_func)
    def wrapper_function(particle1: Particle, particle2: Particle, *args, **kwargs):
        # limited_force_funct = limit_force_module(force_func)
        return_force: np.ndarray = force_func(particle1, particle2, *args, **kwargs)
        ic("Applying force: ", return_force)
        particle1.apply_force(return_force)
        particle2.apply_force(-return_force)
    return wrapper_function

# Force functions
@force_applier
@limit_force_module
def gravitational_force(particle1: Particle, particle2: Particle) -> np.ndarray:
    distance_vector: np.ndarray = particle2.position - particle1.position
    distance: np.floating = np.linalg.norm(distance_vector)
    force_module: np.floating = (particle1.mass * particle2.mass) / distance**2
    force_direction: np.ndarray = distance_vector / distance if distance != 0 else np.zeros(3)
    return force_module * force_direction
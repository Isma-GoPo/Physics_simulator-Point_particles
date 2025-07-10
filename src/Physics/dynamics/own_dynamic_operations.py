"""This module contains dynamic operations which take one particles as argument and operate on them.
(These operations are used in the `ParticleSpace` class to advance the simulation.)

Functions:
"""
import numpy as np
from functools import wraps
from typing import Callable, Any # Allow to use Callable (what means function) for type hints (specifying the input output of the function as argument)

#import couple_dynamic_operations as couple

# Relative imports
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from particle import Particle


# ---

# Decorators / higher-order functions
def force_applier(force_func: Callable[[Particle], np.ndarray] | Any) -> Callable[[Particle], None] | Any:
    """Decorator to apply a force (returned by force_func) to both particles.
    
    Arguments:
    force_func: Callable[[Particle, *args, **kwargs], np.ndarray] -> A function that takes a Particle (or a couple) and returns a force.
    
    Returns:
    Callable[[Particle, *args, **kwargs], None] -> A function that takes one particle and applies the force.
    """
    @wraps(force_func)
    def wrapper_function(particle: Particle, *args, **kwargs):
        return_force: np.ndarray = force_func(particle, *args, **kwargs)
        particle.apply_force(return_force)
    return wrapper_function



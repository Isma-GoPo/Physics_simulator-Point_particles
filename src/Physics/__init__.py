"""This is a package where the physics functions are developed.

The package includes:
- 'Particle' class: contains all the information that a puntual charge must have.
"""

from .particle import Particle
from . import linearalgebra
from .physics_constants import *

__all__ = ["Particle", "linearalgebra", "physics_constants"]
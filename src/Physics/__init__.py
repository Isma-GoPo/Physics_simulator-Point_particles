"""This is a package where the physics objects are developed.

The package includes:
- 'Particle' class: contains all the information that a puntual particle must have.
- 'ParticleSpace' class: defines a collection/space of particles and methods to simulate their dynamics.
- 'physics_constants' module: contains the physical constants used in the simulation.
- 'dynamics' package: contains physics/dynamic operations which take one or couple particles as arguments and operate on them.
"""

from .particle import Particle
from .particle_space import ParticleSpace
from .physics_constants import *
from .dynamics import *

# from . import linearalgebra

__all__ = ["Particle", "ParticleSpace", "physics_constants", "forces"]
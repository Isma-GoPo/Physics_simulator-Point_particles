"""This is a package where the plotting functions and objects are developed.

The package includes:
- 'Dot' class: contains all the information I need a Particle to have for the plotting of the simulation.
- 'space_plotting' module: contains the functions for running the simulation from an ParticleSpace object.
"""

from .dot import PlottingDot
#from .space_plotting import print_animated_simulation_by_space

# from . import linearalgebra

__all__ = ["PlottingDot"]
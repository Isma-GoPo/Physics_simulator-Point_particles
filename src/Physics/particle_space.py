"""`particle_space` module include the `ParticleSpace` class"""

import numpy as np

from .particle import Particle

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from plotting import print_simulation_animated

class ParticleSpace(list):
    """A class for managing a space containing multiple particles. Inherits from list."""
    def __init__(self, *particles: Particle) -> None:
        super().__init__(particles)

    def __str__(self) -> str:
        class_name = self.__class__.__name__
        attributes = '\n'.join(f"  {i}: {value}" for i, value in enumerate(self))
        return f"<{class_name} object at {hex(id(self))}>\n{attributes}"

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        attributes = ', '.join(repr(p) for p in self)
        return f"{class_name}([{attributes}])"

    def add_particle(self, particle: Particle) -> None:
        """Add a particle to the space."""
        self.append(particle)

    def advance_time_step(self, time_step: float= 1.) -> None:
        """Advance all particles in the space by a given time step."""
        for particle in self:
            particle.advance_time_step(time_step)

    def iterate_time_step(self, time_step: float = 1.) -> None:
        """Advance all particles in the space for the given steps."""
        # functions for applying forces/acceleration to the particles...
        ...
        self.advance_time_step(time_step)

    def run_simulation(self, numer_of_time_steps: int, time_step: float = 1.) -> None:
        """Iterates all particles in the space for the given steps."""
        for _ in range(numer_of_time_steps):
            self.iterate_time_step(time_step)
        print_simulation_animated(*[p.position_history for p in self])
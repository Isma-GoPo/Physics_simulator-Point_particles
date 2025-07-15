"""`particle_space` module include the `ParticleSpace` class"""

import numpy as np
from icecream import ic
from collections.abc import Callable # Allow to use Callable (what means function) for type hints (specifying the input output of the function as argument)

from .particle import Particle

import sys
import os
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#from plotting import print_simulation_animated

class ParticleSpace(list):
    """A class for managing a space containing multiple particles. Inherits from list."""
    def __init__(self, 
                 *particles: tuple[Particle], 
                 single_forces_array: tuple[Callable[[Particle], np.ndarray], ...] | None = None,
                 couple_forces_array: tuple[Callable[[Particle, Particle], np.ndarray], ...] | None = None
                 ) -> None:
        super().__init__(particles)
        self._single_forces_array = single_forces_array if single_forces_array is not None else ()
        self._couple_forces_array = couple_forces_array if couple_forces_array is not None else ()

    # --- PROPERTIES ---
    
    @property
    def single_forces_array(self) -> tuple[Callable[[Particle], np.ndarray], ...]:
        """Get the tuple of forces fucntions that are applied on individual particles."""
        return self._single_forces_array

    @property
    def couple_forces_array(self) -> tuple[Callable[[Particle, Particle], np.ndarray], ...]:
        """Get the tuple of forces fucntions that are applied on pairs of particles."""
        return self._couple_forces_array
    
    def set_forces_to_apply(self, /, 
                            single_forces_array: tuple[Callable[[Particle], np.ndarray], ...] | None = None,
                            couple_forces_array: tuple[Callable[[Particle, Particle], np.ndarray], ...] | None = None
                            ) -> None:
        """Set the tuple of functions that operate on individual particles.
        
        Keyword Arguments:
        single_forces_array: A tuple of functions that will be applied to each particle in the space individually.
        couple_forces_array: A tuple of functions that will be applied to each pair of particles in the space.
        """
        if single_forces_array is not None:
            # If single_forces_array is not None, set it. Otherwise, keep the existing value
            self._single_forces_array = single_forces_array
        if couple_forces_array is not None:
            # If couple_forces_array is not None, set it. Otherwise, keep the existing value
            self._couple_forces_array = couple_forces_array

    @property
    def position_history_array(self) -> tuple[np.ndarray, ...]:
        """Return a tuple of position history arrays for each particle in the space."""
        return tuple(p.position_history for p in self)

    # --- METHODS ---

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

    def reduced_position_history_array(self, steps_relation: int = 1) -> tuple[np.ndarray, ...]:
        return tuple(p.position_history[::steps_relation] for p in self)


    def advance_time_step(self, time_step: float= 1.) -> None:
        """Advance all particles in the space by a given time step."""
        for particle in self:
            particle.advance_time_step(time_step)

    def apply_single_forces_array(self, 
                                  single_forces_array: tuple[Callable[[Particle], np.ndarray], ...] = (),
                                  ) -> None:
        """Apply the forces (self ones and passed) to each particle in the space individually."""
        for particle in self:
            for force in self._single_forces_array + single_forces_array:
                particle.apply_force(force(particle))
    
    def apply_couple_forces_array(self,
                                  couple_forces_array: tuple[Callable[[Particle, Particle], np.ndarray], ...] = (),
                                  ) -> None:
        """Apply the forces (self ones and passed) to each pair of particles in the space."""
        for i, particle1 in enumerate(self):
            
            for particle2 in self[i+1:]:
                for force in self._couple_forces_array + couple_forces_array:
                    force_to_apply: np.ndarray = force(particle1, particle2)
                    particle1.apply_force(force_to_apply)
                    particle2.apply_force(-force_to_apply)

    def iterate_time_step(self, time_step: float = 1., 
                          single_forces_array: tuple[Callable[[Particle], np.ndarray], ...] = (), 
                          couple_forces_array: tuple[Callable[[Particle, Particle], np.ndarray], ...] = ()
                          ) -> None:
        """Advance all particles in the space for the given steps operating with the given functions.
        
        Arguments:
        time_step: [s] the time step to advance each particle.
        single_forces_array: A tuple of functions that will be applied to each particle in the space individually.
        couple_forces_array: A tuple of functions that will be applied to each pair of particles in the space.
        """
        # Apply self operations to each particle
        self.apply_single_forces_array(single_forces_array)
        
        # Apply couple operations to each pair of particles
        self.apply_couple_forces_array(couple_forces_array)
        
        self.advance_time_step(time_step)


    def run_simulation(self, 
                       numer_of_time_steps: int, 
                       time_step: float = 1.,
                       single_forces_array: tuple[Callable[[Particle], np.ndarray], ...] = (), 
                       couple_forces_array: tuple[Callable[[Particle, Particle], np.ndarray], ...] = ()) -> None:
        """Iterates all particles in the space for the given steps applying them the given function/operations.
        
        Arguments:
        numer_of_time_steps: [s] the number of time steps to advance each particle.
        time_step: [s] the time step to advance each particle.
        single_forces_array: A tuple of functions that will be applied to each particle in the space individually.
        couple_forces_array: A tuple of functions that will be applied to each pair of particles in the space.
          Better if they are set in `self.set_forces_to_apply()` (the default).
        """
        for _ in range(numer_of_time_steps):
            self.iterate_time_step(time_step, single_forces_array, couple_forces_array)
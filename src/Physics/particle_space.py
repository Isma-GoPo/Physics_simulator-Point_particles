"""`particle_space` module include the `ParticleSpace` class"""

import numpy as np
from collections.abc import Callable # Allow to use Callable (what means function) for type hints (specifying the input output of the function as argument)

from .particle import Particle

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from plotting import print_simulation_animated

class ParticleSpace(list):
    """A class for managing a space containing multiple particles. Inherits from list."""
    def __init__(self, 
                 *particles: Particle, 
                 own_dynamic_operation_array: tuple[Callable[[Particle], None], ...] | None = None,
                 couple_dynamic_operation_array: tuple[Callable[[Particle, Particle], None], ...] | None = None
                 ) -> None:
        super().__init__(particles)
        self._space_own_dynamics = own_dynamic_operation_array if own_dynamic_operation_array is not None else ()
        self._space_couple_dynamics = couple_dynamic_operation_array if couple_dynamic_operation_array is not None else ()

    # --- PROPERTIES ---
    
    @property
    def own_dynamic_operation_array(self) -> tuple[Callable[[Particle], None], ...]:
        """Get the tuple of functions that operate on individual particles."""
        return self._space_own_dynamics
    # 
    # @own_dynamic_operation_array.setter
    # def own_dynamic_operation_array(self, own_dynamic_operation_array: tuple[Callable[[Particle], None], ...]) -> None:
    #     """Set the tuple of functions that operate on individual particles."""
    #     self._space_own_dynamics = own_dynamic_operation_array

    
    @property
    def couple_dynamic_operation_array(self) -> tuple[Callable[[Particle, Particle], None], ...]:
        """Get the tuple of functions that operate on pairs of particles."""
        return self._space_couple_dynamics
    # 
    # @couple_dynamic_operation_array.setter
    # def couple_dynamic_operation_array(self, couple_dynamic_operation_array: tuple[Callable[[Particle], None], ...]) -> None:
    #     """Set the tuple of functions that operate on pairs of particles."""
    #     self._space_couple_dynamics = couple_dynamic_operation_array
    
    def set_dynamic_operations(self, /, 
                                          own_dynamic_operation_array: tuple[Callable[[Particle], None], ...] | None = None,
                                          couple_dynamic_operation_array: tuple[Callable[[Particle, Particle], None], ...] | None = None
                                          ) -> None:
        """Set the tuple of functions that operate on individual particles."""
        if own_dynamic_operation_array is not None:
            # If own_dynamic_operation_array is not None, set it. Otherwise, keep the existing value
            self._space_own_dynamics = own_dynamic_operation_array
        if couple_dynamic_operation_array is not None:
            # If couple_dynamic_operation_array is not None, set it. Otherwise, keep the existing value
            self._space_couple_dynamics = couple_dynamic_operation_array

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



    def advance_time_step(self, time_step: float= 1.) -> None:
        """Advance all particles in the space by a given time step."""
        for particle in self:
            particle.advance_time_step(time_step)

    def apply_own_dynamic_operations(self, 
                                     own_dynamic_operation_array: tuple[Callable[[Particle], None], ...] = (),
                                     ) -> None:
        """Apply the own dynamic operations (self ones and passed) to each particle in the space."""
        for particle in self:
            for operation in self._space_own_dynamics + own_dynamic_operation_array:
                operation(particle)
    
    def apply_couple_dynamic_operations(self,
                                        couple_dynamic_operation_array: tuple[Callable[[Particle, Particle], None], ...] = (),
                                        ) -> None:
        """Apply the couple dynamic operations (self ones and passed) to each pair of particles in the space."""
        for i, particle1 in enumerate(self):
            for particle2 in self[i+1:]:
                for operation in self._space_couple_dynamics + couple_dynamic_operation_array:
                    operation(particle1, particle2)

    def iterate_time_step(self, time_step: float = 1., 
                          own_dynamic_operation_array: tuple[Callable[[Particle], None], ...] = (), 
                          couple_dynamic_operation_array: tuple[Callable[[Particle, Particle], None], ...] = ()
                          ) -> None:
        """Advance all particles in the space for the given steps operating with the given functions.
        
        Arguments:
        time_step: [s] the time step to advance each particle.
        own_dynamic_operation_array: A tuple of functions that will be applied to each particle in the space.
        couple_dynamic_operation_array: A tuple of functions that will be applied to pairs of particles in the space.
        """
        # Apply self operations to each particle
        self.apply_own_dynamic_operations(own_dynamic_operation_array)
        
        # Apply couple operations to each pair of particles
        self.apply_couple_dynamic_operations(couple_dynamic_operation_array)
        
        self.advance_time_step(time_step)

    def run_simulation(self, 
                       numer_of_time_steps: int, 
                       time_step: float = 1.,
                       own_dynamic_operation_array: tuple[Callable[[Particle], None], ...] = (), 
                       couple_dynamic_operation_array: tuple[Callable[[Particle, Particle], None], ...] = ()) -> None:
        """Iterates all particles in the space for the given steps applying them the given function/operations.
        
        Arguments:
        numer_of_time_steps: [s] the number of time steps to advance each particle.
        time_step: [s] the time step to advance each particle.
        own_dynamic_operation_array: A tuple of functions that will be applied to each particle in the space.
          Better if it is set in `self.space_own_dynamics` (the default).
        couple_dynamic_operation_array: A tuple of functions that will be applied to pairs of particles in the space.
          Better if it is set in `self.space_couple_dynamics` (the default).
        """
        for _ in range(numer_of_time_steps):
            self.iterate_time_step(time_step, own_dynamic_operation_array, couple_dynamic_operation_array)
        print_simulation_animated(*[p.position_history for p in self])
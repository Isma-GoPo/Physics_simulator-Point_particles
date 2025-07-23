"""`particle_space` module include the `ParticleSpace` class"""

import numpy as np
from collections.abc import Callable # Allow to use Callable (what means function) for type hints (specifying the input output of the function as argument)
from typing import Any
from icecream import ic


# My modules
from .particle import Particle
# Relative imports
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from settings.config_subclasses import ConfigSimulation 
from settings.settings import Config



class ParticleSpace(list):
    """A class for managing a space containing multiple particles. Inherits from list."""
    def __init__(self, 
                 *particles: tuple[Particle], 
                 single_forces_array: tuple[Callable[[Particle], np.ndarray], ...] | None = None,
                 simulation_config: ConfigSimulation = Config().simulation,
                 couple_forces_array: tuple[Callable[[Particle, Particle], np.ndarray], ...] | None = None,
                 ) -> None:
        super().__init__(particles)
        self._single_forces_array = single_forces_array if single_forces_array is not None else ()
        self._couple_forces_array = couple_forces_array if couple_forces_array is not None else ()
        self.config = simulation_config
        self._life_time = 0.0
        
        self._is_being_adaptative = False

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

    @property
    def life_time(self) -> float:
        """Read-only access to the life the particle have lived."""
        return self._life_time
    
    @property
    def is_being_adaptative(self) -> bool:
        return self._is_being_adaptative

    @is_being_adaptative.setter
    def is_being_adaptative(self, state: bool) -> None:
        state = bool(state)
        if state != self._is_being_adaptative:    # Only works if it alternate it state
            self._is_being_adaptative = state
            for particle in self:
                particle.is_being_adaptative = state
            
            if state == True:
                pass
            else:
                pass

    @property
    def config(self) -> ConfigSimulation:
        return self._config.copy
    
    @config.setter
    def config(self, new_simulation_config: ConfigSimulation) -> None:
        self._config = new_simulation_config
        #for particle in self:
        #    particle.config = new_simulation_config
        ic("Config updated")
            
    # --- METHODS ---


    # --- RETURNING METHODS ---

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

    def get_particle_property_array(self, property_name: str) -> tuple[np.ndarray, ...]:
        """Return a tuple of arrays for the given property of each particle in the space."""
        return tuple(getattr(particle, property_name) for particle in self)

    def get_particle_property_list(self, property_name: str) -> list[Any]:
        """Return a list of arrays for the given property of each particle in the space."""
        return [getattr(particle, property_name) for particle in self]

    def reduced_position_history_array(self, steps_relation: int = 1) -> tuple[np.ndarray, ...]:
        return tuple(particle.position_history[::steps_relation] for particle in self)
    
    def check_adaptative_ok(self, time_step: float) -> bool:
        """Return wheter the  tuple of the velocity difference arrays for each particle in the space.
        
        Arguments:
        time_step: [s] the time step (to advance each particle) that will be checked

        Returns:
        True if the step size is okay, False if it should be shorter
        """
        return all((particle.check_adaptative_ok(time_step, self.config.adaptability) for particle in self))

    # --- INITIALASING METHODS ---

    # --- OPERATING METHODS ---

    def advance_particles_time_step(self, time_step: float= 1.) -> None:
        """Advance all particles in the space by a given time step."""
        for particle in self:
            particle.advance_time_step(time_step)

    def apply_single_forces_array(self) -> None:
        """Apply the forces (in self) to each particle in the space individually."""
        for particle in self:
            for force in self._single_forces_array:
                particle.apply_force(force(particle))
    
    def apply_couple_forces_array(self) -> None:
        """Apply the forces (in self) to each pair of particles in the space."""
        for i, particle1 in enumerate(self):
            
            for particle2 in self[i+1:]:
                for force in self._couple_forces_array:
                    force_to_apply: np.ndarray = force(particle1, particle2)
                    particle1.apply_force(force_to_apply)
                    particle2.apply_force(-force_to_apply)

    def apply_all_forces_array(self) -> None:
        """Group the application of all the forces"""
        self.apply_single_forces_array()
        self.apply_couple_forces_array()

    def adapatative_recursive_iteration(self, time_step: float) -> None:
        if self.check_adaptative_ok(time_step):
            self.advance_particles_time_step(time_step)
        else:
            self.is_being_adaptative = True
            lower_time_step = time_step/2
            
            self.adapatative_recursive_iteration(lower_time_step)
            self.apply_all_forces_array() # from one advance_particles_time_step to the other
            self.adapatative_recursive_iteration(lower_time_step)

    def adapatative_iterate_time_step(self, time_step: float) -> None:
        self.apply_all_forces_array()
        self.adapatative_recursive_iteration(time_step)
        self._life_time += time_step
        self.is_being_adaptative = False

    def iterate_time_step(self, time_step: float = 1.) -> None:
        """Advance all particles in the space for the given steps operating with the given functions.
        
        Arguments:
        time_step: [s] the time step to advance each particle.
        """
        self.apply_all_forces_array()
        self.advance_particles_time_step(time_step)
        self._life_time += time_step


    def run_simulation(self, 
                       numer_of_time_steps: int, 
                       time_step: float = 1.) -> None:
        """Iterates all particles in the space for the given steps applying them the given function/operations.
        
        Arguments:
        numer_of_time_steps: [s] the number of time steps to advance each particle.
        time_step: [s] the time step to advance each particle.
        """
        if not self.config.adaptability.is_adaptative:
            for _ in range(numer_of_time_steps):
                self.iterate_time_step(time_step)
        else: 
            for _ in range(numer_of_time_steps):
                self.adapatative_iterate_time_step(time_step)

"""`particle_space` module include the `ParticleSpace` class"""

import numpy as np
from collections.abc import Callable # Allow to use Callable (what means function) for type hints (specifying the input output of the function as argument)
from typing import Any
from icecream import ic


# My modules
from physics.particle import Particle
# Relative imports
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from settings.config_subclasses import ConfigSimulation 
from settings import Config, CONFIGURATION
from utils import print_run_time





class ParticleSpace(list):
    """A class for managing a space containing multiple particles. Inherits from list."""
    def __init__(self, 
                 *particles: tuple[Particle], 
                 single_forces_array: tuple[Callable[[Particle], np.ndarray], ...] | None = None,
                 simulation_config: ConfigSimulation = CONFIGURATION.simulation,
                 couple_forces_array: tuple[Callable[[Particle, Particle], np.ndarray], ...] | None = None,
                 ) -> None:
        super().__init__(particles)
        self._single_forces_array = single_forces_array if single_forces_array is not None else ()
        self._couple_forces_array = couple_forces_array if couple_forces_array is not None else ()
        self.config = simulation_config
        
        self._life_time = 0.0
        
        self._is_being_adaptive = False

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
    def recommended_division_for_steps(self) -> int:
        return_value = int(max(particle.adaptability.recommended_division_for_steps for particle in self))
        return return_value
    
    @property
    def life_time(self) -> float:
        """Read-only access to the life the particle have lived."""
        return self._life_time
    
    @property
    def is_being_adaptive(self) -> bool:
        return self._is_being_adaptive

    @is_being_adaptive.setter
    def is_being_adaptive(self, state: bool) -> None:
        state = bool(state)
        if state != self._is_being_adaptive:    # Only works if it alternate it state
            self._is_being_adaptive = state
            for particle in self:
                particle.is_being_adaptive = state
            
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
        for particle in self:
            particle.adaptability.config = new_simulation_config.adaptability
        ic("Config updated")
            
    # --- INITIALASING METHODS ---
    # --- METHODS ---
    
    def add_particle(self, particle: Particle) -> None:
        """Append/add a particle to the space."""
        self.append(particle)


    # --- RETURNING METHODS ---

    def __str__(self) -> str:
        class_name = self.__class__.__name__
        attributes = '\n'.join(f"  {i}: {value}" for i, value in enumerate(self))
        return f"<{class_name} object at {hex(id(self))}>\n{attributes}"

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        attributes = ', '.join(repr(p) for p in self)
        return f"{class_name}([{attributes}])"

    def get_particle_property_array(self, property_name: str) -> tuple[np.ndarray, ...]:
        """Return a tuple of arrays for the given property of each particle in the space."""
        return tuple(getattr(particle, property_name) for particle in self)
    
    def get_particle_property_list(self, property_name: str) -> list[Any]:
        """Return a list of arrays for the given property of each particle in the space."""
        return [getattr(particle, property_name) for particle in self]

    def get_reduced_position_history_array(self, steps_relation: int = 1) -> tuple[np.ndarray, ...]:
        """Return a tuple of reduced position history (`steps_relation` times smaller) arrays for each particle in the space."""
        return tuple(particle.position_history[::steps_relation] for particle in self)
    
    def check_adaptive_ok(self, time_step: float) -> bool:
        """Return wheter if the given time step is okay (adaptatibely correct) forall the particles in the space.

        Returns:
        True if the step size is okay, False if it should be shorter
        """
        return all(particle.adaptability.check_adaptive_ok(time_step) for particle in self)


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

    def _adapatative_recursive_iteration(self, time_step: float) -> None:
        """Check if the time step is okay. Advance step if okay, or recursevilly reduce the time step if not.
        """
        # I cannot use `self.apply_all_forces_array` here because if it recursevilly rerun, it would apply it twice before advancing step
        
        if self.check_adaptive_ok(time_step):
            self.advance_particles_time_step(time_step)
        else:
            self.is_being_adaptive = True
            time_steps_division:int = self.recommended_division_for_steps
            lower_time_step = time_step/time_steps_division
            assert not time_steps_division ==1 # Because if not, it could cause a loop (recursion error)
            self._adapatative_recursive_iteration(lower_time_step)
            for _ in range(time_steps_division-1):
                self._adapatative_recursive_iteration(lower_time_step)
                self.apply_all_forces_array()

    def adapatative_iterate_time_step(self, time_step: float) -> None:
        """Advance all particles in the space applying the forces adapting the given step into an scale that fulfil the "adaptability check".
        """
        self.apply_all_forces_array()
        self._adapatative_recursive_iteration(time_step)
        self._life_time += time_step
        self.is_being_adaptive = False

    def iterate_time_step(self, time_step: float = 1.) -> None:
        """Advance all particles in the space applying the forces for the given step. No adaptability.
        """
        self.apply_all_forces_array()
        self.advance_particles_time_step(time_step)
        self._life_time += time_step

    @print_run_time
    def run_simulation(self) -> None:
        """Iterates all particles in the space for the given steps applying them the given function/operations.
        
        Uses from ConfigSimulation:
        numer_of_time_steps: [s] the number of time steps to advance each particle.
        time_step: [s] the time step to advance each particle.
        adaptability.is_adaptive: [bool] if I want to run an adaptative simulation
        """
        if CONFIGURATION.simulation.could_crass:    
            raise Exception("Too many time steps could crash")
        
        if not self.config.adaptability.is_adaptive:
            for _ in range(self.config.number_of_time_steps):
                self.iterate_time_step(self.config.time_step)
        else: 
            for _ in range(self.config.number_of_time_steps):
                self.adapatative_iterate_time_step(self.config.time_step)

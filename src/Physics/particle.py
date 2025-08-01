"""`particle` module include the `Particle` class"""

import numpy as np
from icecream import ic
from functools import wraps
from typing import Any, Callable, TypeVar, ParamSpec
P = ParamSpec('P')  # For type hinting *args, **kwargs
InstanceType = TypeVar('InstanceType') # When decorating a method *within* AdaptabilityManager, InstanceType will be AdaptabilityManager



# My modules
from physics.adaptability_manager import AdaptabilityManager
from utils.functions_utils import run_if_condition

# relative imports
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from settings.config_subclasses import ConfigAdapt
from settings import CONFIGURATION
#from plotting.dot import PlottingDot

class Particle:
    def __init__(self, mass: float, 
                 initial_position: np.ndarray | None = None, 
                 initial_velocity: np.ndarray | None = None, 
                 initial_acceleration: np.ndarray | None = None,
                 *,
                 acceleration_field: np.ndarray | None = None,
                 ) -> None:
        """Init a 'Particle' object

        Possitional-Keyword arguments:
        mass: [kg] the mass of the particle (only +)
        initial_position: [m] a 3D numpy array for initial coordinates x, y, z. Default: (0, 0, 0)
        initial_velocity: [m/s] a 3D numpy array for initial velocities in x, y, z. Default: (0, 0, 0)
        initial_acceleration: [m/s2] a 3D numpy array for initial accelerations in x, y, z. Default: (0, 0, 0)
            Do not include the acceleration due to the acceleration field
        
        Keyword arguments:
        acceleration_field: [m/s2] a 3D numpy array for a constant acceleration that will be always applied when updating
            to the next step. In x, y, z. Default: (0, 0, 0)
        """
        self.mass = mass
        # np.ndarray is mutable, so initializing with None and then setting to np.zeros(3) is needed
        self.position = initial_position if initial_position is not None else np.zeros(3)
        self.velocity = initial_velocity if initial_velocity is not None else np.zeros(3)
        self.acceleration_field = acceleration_field if acceleration_field is not None else np.zeros(3)
        self.reset_acceleration() # Add the acceleration field to the initial acceleration
        
        self._last_velocity = np.zeros(3)
        self._last_acceleration = np.zeros(3)
        self._position_history = np.empty((0, 3), float)
        self._velocity_diff_history = np.empty((0), float) # For adaptive
        self._life_time = 0.0
        self._is_being_adaptive: bool = False
        self._is_first_substep: bool = True

        self.adaptability = AdaptabilityManager(self._velocity_differential)

    # --- PROPERTIES ---

    @property
    def last_velocity(self) -> np.ndarray:
        """Read-only access to the last step velocity of the particle."""
        return self._last_velocity.copy()

    @property
    def last_acceleration(self) -> np.ndarray:
        """Read-only access to the last step acceleration of the particle."""
        return self._last_acceleration.copy()

    @property
    def velocity_to_apply(self) -> np.ndarray:
        """Returns the velocity of the particle that should have when translating the particle positions"""
        return (self.velocity + self.last_velocity) / 2
    
    @property
    def acceleration_to_apply(self) -> np.ndarray:
        """Returns the acceleration of the particle that should have when translating the particle positions"""
        return self.acceleration #(self.acceleration + self.last_acceleration) / 2

    @property
    def position_history(self) -> np.ndarray:
        """Read-only access to the position history."""
        return self._position_history.copy()
    
    @property
    def life_time(self) -> float:
        """Read-only access to the life the particle have lived."""
        return self._life_time
    
    @property
    def is_being_adaptive(self) -> bool:
        """Read the state (adapatative) of the particle.
        
        If the particle is being adaptive, it means that the time steps that its running are shorter than normally,
        so it should behave in a different way:
        - store_position_in_history only should work when it stop to be adapatative"""
        return self._is_being_adaptive
    
    @is_being_adaptive.setter
    def is_being_adaptive(self, state: bool) -> None:
        """Set the state (adapatative) of the particle. 
        Forcing to store the values it couldn't when it was being adaptative."""
        state = bool(state)
        if state != self._is_being_adaptive:    # Only works if it alternate it state
            self._is_being_adaptive = state
            
            if state == False:
                if self._is_first_substep == False: 
                # This means as least one step have run from when it was setted adaptative
                    self._store_position_in_history()
                    self._is_first_substep = True
            else:
                pass
    
    # --- METHODS ---        
    
    # --- RETURNING METHODS ---
    def __str__(self) -> str:
        class_name = self.__class__.__name__
        attributes = '\n'.join(f"  {key}: {value}" for key, value in self.__dict__.items())
        return f"<{class_name} object at {hex(id(self))}>\n{attributes}"

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        attributes = ', '.join(f"{key} = {repr(value)}" for key, value in self.__dict__.items())
        return f"{class_name}({attributes})"
    
    # --- adaptive METHODS ---
    
    def _velocity_differential(self, time_step: float = 1.0) -> float:
        """Returns the velocity differential caused by the acceleration and the time step size.
        It is used as meassure for adaptability"""
        value = float( np.linalg.norm(self.acceleration_to_apply) * time_step )
        return value
    
    def _set_acceleration_from_threshold_value(self, time_step) -> None:
        """Try to make the oposite of `velocity_differential`, returning an acceleration using the velocity_differential of the `AdaptabilityManager`"""
        if self.adaptability.do_last_failed:
            max_acceleration = self.adaptability.last_threshold_absolute_value / time_step
            self.acceleration = self.acceleration/np.linalg.norm(self.acceleration) * max_acceleration
        #else:
        #    raise Exception("Tried to set acceleration_from_threshold when the last step of the particle was adaptative-ok")
        #ic(self.acceleration)

    # --- OPERATING METHODS ---

    def _do_translate(self, time_step: float = 1.0) -> None:
        """Translate (move) the position of the particle according to the particle velocity during the given time step.
        """
        # A `force_translate` function could be added to pass the velocity as an argument
        self.position += self.velocity_to_apply * time_step

    def _do_accelerate(self, time_step: float = 1.0) -> None:
        """Updates the velocity of the particle according to the particle acceleration during the given time step.
        """
        # A `force_accelerate` function could be added to pass the velocity as an argument
        self.velocity += self.acceleration_to_apply * time_step

    def apply_force(self, applied_force: np.ndarray) -> None:
        """Applies a force to the particle, updating its acceleration.

        Keyword arguments:
        applied_force: [N] a 3D numpy array for the force in x, y, z
        """
        self.apply_acceleration( applied_force / self.mass)

    def apply_acceleration(self, applied_acceleration: np.ndarray) -> None:
        """Applies an acceleration to the particle, updating its acceleration.

        Keyword arguments:
        applied_acceleration: [m/s2] a 3D numpy array for the acceleration in x, y, z
        """
        self.acceleration += applied_acceleration

    @run_if_condition(lambda self: not self._is_being_adaptive) # Only run if is not being adaptive
    def _store_position_in_history(self) -> None:
        """Stores the current position in the position history."""
        self._position_history = np.vstack((self.position_history, [self.position]))

    @run_if_condition(lambda self: self._is_first_substep) # Only run if is not being adaptive
    def _store_adaptability_value_in_history(self, time_step: float) -> None:
        """Stores the velocity difference in the adaptability propierty history."""
        self.adaptability.store_value_in_history(time_step)

    def reset_acceleration(self) -> None:
        """Reset the acceleration, making it equal to the acceleration field."""
        self.acceleration = self.acceleration_field.copy()

    def _shift_cinematic_properties(self) -> None:
        """Shift velocity, accelearation properties to `last` and reset acceleration."""
        self._last_velocity = self.velocity.copy() # .copy() because ndarray is mutable
        # velocity is preserved (conservation of momentum)
        self._last_acceleration = self.acceleration.copy() # .copy() because ndarray is mutable
        self.reset_acceleration()

    def store_current_state(self) -> None:
        """Stores the current position in history and velocity and acceleration as the last ones and reset them."""
        self._store_position_in_history()
        self._shift_cinematic_properties()

    def advance_time_step(self, time_step: float = 1.0) -> None:
        """Advances the particle's state by one time step, accelerating and translating it.

        Keyword arguments:
        time_step: [s] for how much time do the acceleration occurs. Default: (0, 0, 0)
        """
        #ic(self._is_first_substep)
        self._store_adaptability_value_in_history(time_step)
        if time_step < self.adaptability.config.min_time_step:
            self._set_acceleration_from_threshold_value(time_step)
        self._do_accelerate(time_step)
        self._do_translate(time_step)
        self.store_current_state()
        self._life_time += time_step
        
        # last thing to do in step
        if self._is_being_adaptive and self._is_first_substep == True:
            self._is_first_substep = False


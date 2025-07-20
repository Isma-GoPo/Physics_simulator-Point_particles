"""`particle` module include the `Particle` class"""

import numpy as np
from icecream import ic

import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from plotting.dot import PlottingDot

class Particle:
    def __init__(self, mass: float, 
                 initial_position: np.ndarray | None = None, 
                 initial_velocity: np.ndarray | None = None, 
                 initial_acceleration: np.ndarray | None = None,
                 *,
                 acceleration_field: np.ndarray | None = None,
                 plotting_dot: PlottingDot | None = None,
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
        initial_acceleration = initial_acceleration if initial_acceleration is not None else np.zeros(3)
        self.acceleration = initial_acceleration + self.acceleration_field # Add the acceleration field to the initial acceleration
        
        self._last_velocity = np.zeros(3)
        self._last_acceleration = np.zeros(3)
        self._position_history = np.empty((0, 3), float)
        self._life_time = 0.0
        self._is_being_adaptative: bool = False

        # plotting properties
        self.plotting = plotting_dot if plotting_dot is not None else PlottingDot(weight=self.mass)

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
    def is_being_adaptative(self) -> bool:
        """Read the state (adapatative) of the particle.
        
        If the particle is being adaptative, it means that the time steps that its running are shorter than normally,
        so it should behave in a different way:
        - store_position_in_history only should work when it stop to be adapatative"""
        return self._is_being_adaptative
    
    @is_being_adaptative.setter
    def is_being_adaptative(self, state: bool) -> None:
        state = bool(state)
        if state != self._is_being_adaptative:    # Only works if it alternate it state
            self._is_being_adaptative = state
            
            if state == True:
                pass
                # This means that some functions works different:
                # - store_position_in_history
            else:
                self.store_position_in_history()
    
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
    
    def velocity_differential(self, time_step: float = 1.0) -> float:
        return float( np.linalg.norm(self.acceleration_to_apply) * time_step )
    
    def is_adaptative_ok(self, time_step: float, max_velocity_diff: float | np.floating) -> bool:
        """Return wheter the  tuple of the velocity difference arrays for each particle in the space."""
        return self.velocity_differential(time_step) < float(max_velocity_diff)

    # --- OPERATING METHODS ---

    def do_translate(self, time_step: float = 1.0, forced_velocity: np.ndarray | None = None) -> None:
        """Translate (move) the position of the particle according to the velocity (inner or given) during the given time step.

        Keyword arguments:
        time_step: [s] for how much time do the acceleration occurs. Default: (0, 0, 0)
        forced_velocity: [m/s] a 3D numpy array for velocity in x, y, z
          If no velocity is given, it takes the velocity of the object
        """
        if forced_velocity is None:
            velocity = self.velocity_to_apply
        else:
            velocity = forced_velocity
        
        self.position += velocity * time_step

    def do_accelerate(self, time_step: float = 1.0, forced_acceleration: np.ndarray | None = None) -> None:
        """Updates the velocity of the particle according to the acceleration (inner or given) during the given time step.

        Keyword arguments:
        time_step: [s] for how much time do the acceleration occurs. Default: (0, 0, 0)
        forced_acceleration: [m/s2] a 3D numpy array for acceleration in x, y, z
          If no acceleration is given, it takes the acceleration of the object
        """
        if forced_acceleration is None:
            acceleration = self.acceleration_to_apply
        else:
            acceleration = forced_acceleration
        
        self.velocity += acceleration * time_step

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

    def store_position_in_history(self) -> None:
        """Stores the current position in the position history."""
        if not self.is_being_adaptative:
            self._position_history = np.vstack((self.position_history, [self.position]))

    def store_current_state(self) -> None:
        """Stores the current position in history and velocity and acceleration as the last ones and reset them."""
        self.store_position_in_history()
        self._last_velocity = self.velocity.copy() # .copy() because ndarray is mutable
        # velocity is preserved (conservation of momentum)
        self._last_acceleration = self.acceleration.copy() # .copy() because ndarray is mutable
        self.acceleration = self.acceleration_field.copy()  # Reset acceleration to the field value

    def advance_time_step(self, time_step: float = 1.0) -> None:
        """Advances the particle's state by one time step, accelerating and translating it.

        Keyword arguments:
        time_step: [s] for how much time do the acceleration occurs. Default: (0, 0, 0)
        """
        self.do_accelerate(time_step)
        self.do_translate(time_step)
        self.store_current_state()
        self._life_time += time_step

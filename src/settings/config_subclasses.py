import numpy as np
from icecream import ic
import math
#from typing import Callable, Any
from dataclasses import dataclass

# My modules
from .nestedhash import NestedHash

# --- Partial Config classes: for properties and methods ---

# May be should be dataclass

class ConfigAdapt(NestedHash):
    def __init__(self) -> None:
        self.is_adaptative = bool()
        self.max_percentile = float()
        self.max_deviation = float()
        self.max_velocity_diff = float()

    @property
    def max_absolute_value(self) -> float:
        return self.max_velocity_diff #should generally have this name, but because it is for velocity, it is more clear as it


class ConfigSimulation(NestedHash):
    def __init__(self) -> None:
        self.simulation_time = float()
        self.time_step = float()
        self.max_allowed_force = float()
        self.adaptability = ConfigAdapt()
    
    @property
    def number_of_time_steps(self) -> int:
        """How many time steps will be done in the simulation"""
        return int(self.simulation_time / self.time_step) # type: ignore
    
    @property
    def could_crass(self) -> bool:
        could_crass = int(self.simulation_time / self.time_step) > 100_000 # type: ignore
        return could_crass


class ConfigPlotting(NestedHash):
    def __init__(self) -> None:
        self.plotting_time = float()
        self.refresh_rate = int()
        self.do_repeat = bool()
        self.dot_sizes = ConfigSizes()
    
    @property
    def number_of_plotting_steps(self) -> int:
        """How many plotting steps will be done in the simulation"""
        return int(self.plotting_time * self.refresh_rate) # type: ignore
    
    def plotting_relative_time_step(self, number_of_time_steps: int) -> int:
        return int(math.ceil(number_of_time_steps / (self.plotting_time * self.refresh_rate))) # type: ignore

class ConfigSizes(NestedHash):
    def __init__(self) -> None:
        self.min = float()
        self.max = float()
        self.difference = float()
        self.exponent_factor =float()
        
    @property
    def size_per_difference(self) -> float | np.float64:
        return (self.max - self.min)/self.difference # type: ignore



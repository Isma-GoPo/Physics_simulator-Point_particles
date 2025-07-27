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
    """Configuration for the adaptability of the steps in the simulation"""
    def __init__(self) -> None:
        self.is_adaptive = bool()
        self.max_quantile = float()
        self.max_deviation = float()
        self.max_velocity_diff = float()
        self.max_relative_log_diff = float()
        self.min_time_step = float()
        self.quantile_ignored_extremes = float()

    @property
    def max_absolute_value(self) -> float:# should generally have this name, but because it is for velocity, it is more clear as it
        return self.max_velocity_diff 
    
    @max_absolute_value.setter
    def max_absolute_value(self, value: float) -> None:
        self.max_velocity_diff = value

class ConfigSimulation(NestedHash):
    """Configuration for the setting of the simulation"""
    def __init__(self) -> None:
        self.simulation_time = float()
        self.adaptability = ConfigAdapt()
        self._time_step = float() # private because updates `adaptability`

    @property
    def time_step(self) -> float:
        return self._time_step

    @time_step.setter
    def time_step(self, value: float) -> None:
        last_value = self.time_step
        self._time_step = value
        if last_value == 0.:
            last_value = 1.
        self.adaptability.min_time_step = self.adaptability.min_time_step / last_value * value


    @property
    def min_relative_time_step_reduction(self) -> float:
        try: 
            return_value =  self.time_step / self.adaptability.min_time_step
        except:
            return_value =  self.time_step
        return return_value
    
    @min_relative_time_step_reduction.setter
    def min_relative_time_step_reduction(self, value: float) -> None:
        ic(self.time_step, value)
        if value == 0.:
            value = 1.
        self.adaptability.min_time_step = self.time_step / value
    
    @property
    def number_of_time_steps(self) -> int:
        """How many time steps will be done in the simulation"""
        return int(self.simulation_time / self.time_step) # type: ignore
    
    @property
    def could_crass(self) -> bool:
        could_crass = int(self.simulation_time / self.time_step) > 100_000 # type: ignore
        return could_crass

class ConfigPlotting(NestedHash):
    """Configuration for the setting of the plotting of the simulation results"""
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
    """Configuration for the points sizes used in the plotting"""
    def __init__(self) -> None:
        self.min = float()
        self.max = float()
        self.difference = float()
        self.exponent_factor =float()
        
    @property
    def size_per_difference(self) -> float | np.float64:
        return (self.max - self.min)/self.difference # type: ignore



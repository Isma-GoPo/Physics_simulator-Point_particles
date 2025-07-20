import numpy as np
from icecream import ic
#from typing import Callable, Any

# My modules
from .nestedhash import NestedHash

# --- Partial Config classes: for properties and methods ---
class ConfigSimulation(NestedHash):
    @property
    def number_of_time_steps(self) -> int:
        """How many time steps will be done in the simulation"""
        return int(self.simulation_time / self.time_step) # type: ignore
    
    def _could_crass(self) -> bool:
        could_crass = int(self.simulation_time / self.time_step) > 100_000 # type: ignore
        return could_crass


class ConfigPlotting(NestedHash):
    @property
    def number_of_plotting_steps(self) -> int:
        """How many plotting steps will be done in the simulation"""
        return int(self.plotting_time * self.refresh_rate) # type: ignore
    
    def plotting_relative_time_step(self, number_of_time_steps: int) -> int:
        return int(math.ceil(number_of_time_steps / (self.plotting_time * self.refresh_rate))) # type: ignore

class ConfigSizes(NestedHash):
    @property
    def size_per_difference(self) -> float | np.float64:
        return (self.max - self.min)/self.difference # type: ignore



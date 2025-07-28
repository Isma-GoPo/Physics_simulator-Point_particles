import yaml
from typing import Any
from icecream import ic
import numpy as np

# My modules
from . import config_subclasses as configs
from .nestedhash import NestedHash

# relative imports
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from constants import USER_SETTING_DICT


# --- Default values ---
class Config(NestedHash):
    """
    Group all the constants/settings/config for the simulation and plotting that could be changed by a user or a init_space function
    Inherit from NestedHash"""
    def __init__(self) -> None:
        cls = self.__class__
        
        self.simulation = configs.ConfigSimulation()
        self.simulation.simulation_time = 10.0
            # How much the simulation last (in [s])
        self.simulation.time_step = 0.01
            # How much it "tick" advance the time in the simulation (in [s])

        self.simulation.adaptability = configs.ConfigAdapt()
        self.simulation.adaptability.is_adaptive = True
            # If True, the simulation will be adaptive
        self.simulation.adaptability.max_velocity_diff = np.inf
        self.simulation.adaptability.max_quantile = -1. # If quantile is < 0, it doesn't check for it
            # Recommended > 1 and greater (>2) if particles get toguether frequently
        self.simulation.adaptability.max_deviation = 0.   # If deviation is <= 0, it doesn't check for it
            # defines the the adapatative accuracy
        self.simulation.adaptability.max_relative_log_diff = 0. # If deviation is <= 0, it doesn't check for it
        self.simulation.adaptability.min_time_step = self.simulation.time_step / 10
            # Overwrite min_relative_time_step_reduction
        self.simulation.adaptability.quantile_ignored_extremes = 10.
            # greater if particles get toguether frequently

        self.plotting = configs.ConfigPlotting()
        self.plotting.plotting_time = 10.0
            # How much the plotting of the simulation last (in [s])
        self.plotting.refresh_rate = 20
            # Recommended to make it so it plots 30 step every second
        self.plotting.do_repeat = False
            # If True, the plotting will repeat the last frame when it ends
        self.plotting.rotation = (-90., 0., 0.) # tuple of three angles (in degrees)
            # This default totation print →x and ↑z in combination with "xyz" sequence
        self.plotting.rotation_sequence = "xyz" # order of the rotation of the three angles

        self.plotting.dot_sizes = configs.ConfigSizes()
        self.plotting.dot_sizes.min = 15.0               
        self.plotting.dot_sizes.max = 75.0                  
        self.plotting.dot_sizes.difference = 6.0           
        self.plotting.dot_sizes.exponent_factor = 0.666     

CONFIGURATION = Config() # Just one istance of the object shared in all modules
#CONFIGURATION.update(USER_SETTING_DICT)
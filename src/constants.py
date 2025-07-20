"""This module introduces the constants for the program

Constants:

"""


import numpy as np
import math
from icecream import ic
from typing import Any



# My modules

SETTING_FILE_PATH: str = r"src\settings.yaml"

# default settings must contains all the keys used in CONSTANTS with their default value, 
  # so if some miss in the settings.yaml, the programm take the default one
DEFAULT_SETTINGS_DICT: dict[str, Any] = {
    "simulation": {
        "simulation_time": 40,
        "time_step": 0.01,
        "max_allowed_force": np.inf,
        "is_adaptative": True,
        "max_velocity_diff": 100, # meassure the adapatative accuracy
    },
    "plotting": {
        "plotting_time": 10,
        "refresh_rate": 20,
        "do_repeat": False,
        "dot_sizes": {
            "min": 15.0,
            "max": 75.0,
            "difference": 6.0,
            "exponent_factor": 0.666
        }
    },
}
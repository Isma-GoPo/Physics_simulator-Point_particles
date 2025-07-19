from configparser import ConfigParser
import yaml
from typing import Any
from omegaconf import OmegaConf
import numpy as np

import os, sys; sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from settings import merge_dicts


SETTING_FILE_PATH: str = r"src\settings.yaml"

default_settings = {
    "simulation": {
        "simulation_time": 40,
        "time_step": 0.01,
        "max_allowed_force": np.inf,
    },
    "plotting": {
        "plotting_time": 10,
        "refresh_rate": 20,
        "do_repeat": False,
        # max_velocity_diff:
        "dot_sizes": {
            "min": 15,
            "max": 75,
            "size_difference": 6,
            "exponent_factor": 0.666
        }
    },
}

def open_user_settings() -> dict[str, Any]:
    with open(r"src\settings.yaml") as file:
        return yaml.safe_load(file)

user_config = open_user_settings()

merged_config = merge_dicts(default_settings, user_config)

config = OmegaConf.create(merged_config)

print(config.plotting)

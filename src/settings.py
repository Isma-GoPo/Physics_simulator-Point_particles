import yaml
from typing import Any
from icecream import ic


def merge_dicts(default: dict, overrider: dict) -> dict:
    """Merge two dictionaries, ensuring each child key is also merged. So each branch of keys is present in the return"""
    if not isinstance(default, dict) or not isinstance(overrider, dict):
        if isinstance(default, dict):
            return default
        elif isinstance(overrider, dict):
            return overrider
        else:
            return overrider
    return_dict: dict = default | overrider
    for k, v in default.items():
        if isinstance(v, dict):
            if overrider.get(k) is None:
                overrider[k] = {}
            return_dict[k] = merge_dicts( default[k], overrider[k])
    return return_dict

def open_user_settings() -> dict[str, Any]:
    with open(r"src\settings.yaml") as file:
        return yaml.safe_load(file)

user_settings = open_user_settings()

# default settings must contains all the keys used in CONSTANTS with their default value, 
  # so if some miss in the settings.yaml, the programm take the default one
default_settings = {
    "simulation": {
        "simulation_time": 40,
        "time_step": 0.01,
        "max_allowed_force": 100,
    },
    "plotting": {
        "plotting_time": 10,
        "refresh_rate": 20,
        "do_repeat": False
        # max_velocity_diff:
    },
    "test": {
        "test": {
            "test": 1
        }
    }
}

SETTINGS: dict[str, Any] = merge_dicts(default_settings, user_settings)

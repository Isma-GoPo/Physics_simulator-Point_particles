import yaml
from typing import Any
from icecream import ic
import numpy as np

# My modules
from .config_class import Config

# relative imports
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from constants import SETTING_FILE_PATH, DEFAULT_SETTINGS_DICT


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
    with open(SETTING_FILE_PATH) as file:
        return yaml.safe_load(file)

USER_SETTINGS_DICT: dict[str, Any] = open_user_settings()

DEFAULT_CONFIGURATION: Config = Config(DEFAULT_SETTINGS_DICT)

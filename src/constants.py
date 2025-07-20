"""This module introduces the constants for the program

Constants:

"""


import numpy as np
import math
from icecream import ic
from typing import Any
import yaml



# My modules

_SETTING_FILE_PATH: str = r"src\settings.yaml"

def open_user_settings() -> dict[str, Any]:
    with open(_SETTING_FILE_PATH) as file:
        return yaml.safe_load(file)

USER_SETTING_DICT: dict[str, Any] = open_user_settings()
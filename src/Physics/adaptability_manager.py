"""`adaptativility` module include the `AdaptabilityManager` class"""

import numpy as np
from collections.abc import Callable # Allow to use Callable (what means function) for type hints (specifying the input output of the function as argument)
from typing import Any
from icecream import ic


# My modules
# Relative imports
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from settings.config_subclasses import ConfigAdapt
from settings.settings import Config


class AdaptabilityManager:
    def __init__(self, 
                 get_value_function: Callable[[float], float],
                 adaptativility_config: ConfigAdapt = Config().simulation.adaptability,
                 ) -> None:
        """Init a 'AdaptabilityManager' object

        Possitional-Keyword arguments:
        - adaptative_config: Config instance that defines:
          - max_absolute_value: the max velocity different that will be allowed to occur in a time step (default None -> it isn't checked)
          - max_percentile: the percentile in the velocity_diff_history that will be detected as non-ok if adaptative_deviation is high enough (default None -> it isn't checked)
          - max_deviation: the standard deviation in the velocity_diff against velocity_diff_history that will be detected as non-ok if adaptative_percentile is high enough
        - 
        """            
        self.config: ConfigAdapt = adaptativility_config
        
        self.get_value: Callable[[float], float] = get_value_function # when called (no arguments) returns a value for storing it in history
        self._value_history: np.ndarray = np.empty((0), float)

    def store_value_in_history(self, time_step: float) -> None:
        self._value_history = np.append(self._value_history, self.get_value(self.time_step))
    
    # --- CHACK ADAPTATIVE METHODS ---

    def _check_adpatative_by_absolute(self, time_step: float) -> bool:
        return self.get_value(time_step) < float(self.config.max_absolute_value)
    
    def _check_adpatative_by_percentile(self, time_step: float):
        value = np.quantile(self._value_history, self.config.max_percentile, method='higher')
        return self.get_value(time_step) < float(value)

    def _check_adpatative_by_deviation(self, time_step: float):
        value = np.mean(self._value_history) + self.config.max_deviation * np.std(self._value_history)
        return self.get_value(time_step) < float(value)


    def check_adaptative_ok(self, time_step: float) -> bool:
        self.time_step = time_step
        
        # Ordered by computational cost

        if self.config.max_absolute_value is not None \
            and self.config.max_absolute_value < np.inf:
            ok_absolute_value = self._check_adpatative_by_absolute(time_step)
            if not ok_absolute_value:
                return False
        
        if self.config.max_percentile is not None \
            and self.config.max_percentile < 1. \
            and len(self._value_history >= 10): # Because percentile of less doesn't make sense
            ok_percentile = self._check_adpatative_by_percentile(time_step)
            if not ok_percentile:
                return False
            
        if self.config.max_deviation is not None \
            and self.config.max_deviation > 0. \
            and len(self._value_history) >= 2: # Because deviation of less doesn't make sense
            ok_deviation = self._check_adpatative_by_deviation(time_step)
            if not ok_deviation:
                return False
        
        return True


if __name__ == "__main__":
    config = Config().simulation.adaptability

    config.update({
        "max_velocity_diff": np.inf,
        "max_percentile": None,
        "max_deviation": 1.9
    })

    obj = AdaptabilityManager(lambda t: t, config)
    for i in range(20):
        ic(obj.check_adaptative_ok(i))
        obj.store_value_in_history(i)
    #ic(obj._value_history)


    ic(config)
    if (config.max_percentile is not None \
        and config.max_percentile < 0.9) \
        and True:
        print(True)
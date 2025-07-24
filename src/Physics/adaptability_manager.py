"""`adaptativility` module include the `AdaptabilityManager` class"""

import numpy as np
from collections.abc import Callable # Allow to use Callable (what means function) for type hints (specifying the input output of the function as argument)
from typing import Any, TypeVar
InstanceType = TypeVar('InstanceType') # When decorating a method *within* AdaptabilityManager, InstanceType will be AdaptabilityManager.
from icecream import ic
from functools import partial, wraps


# My modules
# Relative imports
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from settings.config_subclasses import ConfigAdapt
from settings import CONFIGURATION
#from plotting.dot import PlottingDot


class AdaptabilityManager:
    def __init__(self, 
                 get_value_function: Callable[[float], float],
                 adaptativility_config: ConfigAdapt = CONFIGURATION.simulation.adaptability,
                 ) -> None:
        """Init a 'AdaptabilityManager' object

        Possitional-Keyword arguments:
        - adaptive_config: Config instance that defines:
          - max_absolute_value: the max velocity different that will be allowed to occur in a time step (default None -> it isn't checked)
          - max_quantile: the quantile in the velocity_diff_history that will be detected as non-ok if adaptive_deviation is high enough (default None -> it isn't checked)
          - max_deviation: the standard deviation in the velocity_diff against velocity_diff_history that will be detected as non-ok if adaptive_quantile is high enough
        - 
        """            
        self.config: ConfigAdapt = adaptativility_config
        
        self.get_value: Callable[[float], float] = get_value_function # when called (no arguments) returns a value for storing it in history
            # very prouf of using a function in this way for not having to access the Particle object
        self._value_history: np.ndarray = np.empty((0), float)
        self._value_log_history: np.ndarray = np.empty((0), float)

    def store_value_in_history(self, time_step: float) -> None:
        if self.config.is_adaptive:
            self._value_history = np.append(self._value_history, self.get_value(time_step))
            self._value_log_history = np.append(self._value_log_history, np.log(self.get_value(time_step))) 
    
    # --- CHACK adaptive METHODS ---

    def _ckeck_corresponding_absolute_value(self, time_step: float, corresponding_absolute_value: float) -> bool:
        return self.get_value(time_step) < corresponding_absolute_value

    @staticmethod
    def _check_adaptive_ok_decorator(get_value_by_function: Callable[[InstanceType], float]) -> Callable[[InstanceType, float], bool]:
        """Transform a get_value function to a function that takes the time_step and check (return True if ok, False if not
        if the value getted is ok for the given time step."""
        @wraps(get_value_by_function)
        def wrapper_function(self, time_step: float) -> bool:
            corresponding_absolute_value = get_value_by_function(self)
            actual_absolute_value = self.get_value(time_step)
            is_ok:bool = actual_absolute_value < corresponding_absolute_value
            if not is_ok:
                ic(time_step, corresponding_absolute_value, actual_absolute_value)
                #ic(self._value_history)
                #ic(time_step)
                
                pass
            return is_ok
        return wrapper_function

    @_check_adaptive_ok_decorator
    def _check_adpatative_by_absolute(self) -> float:
        return float(self.config.max_absolute_value)

    @_check_adaptive_ok_decorator
    def _check_adpatative_by_quantile(self) -> float:
        return float(np.quantile(self._value_history, self.config.max_quantile, method='higher'))

    @_check_adaptive_ok_decorator
    def _check_adpatative_by_deviation(self) -> float:
        return float(np.mean(self._value_history) + self.config.max_deviation * np.std(self._value_history))
    
    @_check_adaptive_ok_decorator
    def _check_adpatative_by_relative_log_diff(self) -> float:
        IGNORED_EXTREMES = 0.1 # in %
        log_diff = np.percentile(self._value_log_history, 100-IGNORED_EXTREMES, method="higher") - np.percentile(self._value_log_history, IGNORED_EXTREMES, method="lower")
        log_mean = np.mean(self._value_log_history[:-2])
        log_value = log_mean + log_diff * self.config.max_relative_log_diff
        #ic(self._value_log_history[:-2])
        #ic(log_value, log_mean, np.mean(self._value_history), log_diff)
        #ic(np.exp(log_mean), np.mean(self._value_history))
        return float(np.exp(log_value))


    def check_adaptive_ok(self, time_step: float) -> bool:
        if not self.config.is_adaptive:
            return True
        
        # Ordered by computational cost

        if self.config.max_absolute_value is not None \
            and self.config.max_absolute_value < np.inf:
            ok_absolute_value = self._check_adpatative_by_absolute(time_step)
            if not ok_absolute_value:
                return False
        
        if self.config.max_quantile is not None \
            and self.config.max_quantile < 1. \
            and len(self._value_history >= 10): # Because quantile of less doesn't make sense
            ok_quantile = self._check_adpatative_by_quantile(time_step)
            if not ok_quantile:
                return False
            
        if self.config.max_relative_log_diff is not None \
            and self.config.max_relative_log_diff > 0. \
            and len(self._value_history) >= 6: # Because function of less doesn't make sense
            ok = self._check_adpatative_by_relative_log_diff(time_step)
            if not ok:
                return False
            
        
        if self.config.max_deviation is not None \
            and self.config.max_deviation > 0. \
            and len(self._value_history) >= 2: # Because deviation of less doesn't make sense
            ok_deviation = self._check_adpatative_by_deviation(time_step)
            if not ok_deviation:
                #ic(ok_deviation)
                return False
        
        return True


if __name__ == "__main__":
    config = CONFIGURATION.simulation.adaptability

    config.update({
        "max_velocity_diff": 19,
        "max_quantile": None,
        "max_deviation": 1.9
    })

    obj = AdaptabilityManager(lambda t: t, config)
    for i in range(20):
        ic(obj.check_adaptive_ok(i))
        obj.store_value_in_history(i)
    #ic(obj._value_history)


    ic(config)
    if (config.max_quantile is not None \
        and config.max_quantile < 0.9) \
        and True:
        print(True)
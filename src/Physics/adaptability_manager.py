"""`adaptativility` module include the `AdaptabilityManager` class"""

import numpy as np
from collections.abc import Callable # Allow to use Callable (what means function) for type hints (specifying the input output of the function as argument)
from typing import Any, TypeVar
InstanceType = TypeVar('InstanceType') # When decorating a method *within* AdaptabilityManager, InstanceType will be AdaptabilityManager.
from icecream import ic
from functools import partial, wraps
from deprecated import deprecated
from pprint import pprint

# turn off -ic()-
#ic.disable()

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
        - get_value_function: a function that when called return an absolute (positive) value which decrease proportionally with time_step
          It return the value that `AdaptabilityManager` study 
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
        
        self.threshold_absolute_value: float = 0.
        self.do_last_failed:bool = False
        self.recommended_division_for_steps:int = 2

    def store_value_in_history(self, time_step: float) -> None:
        if self.config.is_adaptive:
            self._value_history = np.append(self._value_history, self.get_value(time_step))
            #self._value_log_history = np.append(self._value_log_history, np.log(self.get_value(time_step))) 
    
    # --- CHECK adaptive METHODS ---
    def check_adaptive_ok_by_threshold(self, threshold_absolute_value: float, time_step: float) -> bool:
        #threshold_absolute_value
        actual_absolute_value = self.get_value(time_step)
        #ic(threshold_absolute_value, actual_absolute_value)
        is_ok: bool = actual_absolute_value < threshold_absolute_value
        if not is_ok:
            self.do_last_failed = True
            self.last_threshold_absolute_value = threshold_absolute_value
            self.set_recommended_division_for_steps(time_step, actual_absolute_value, threshold_absolute_value)
            #ic(self.recommended_division_for_steps)
            pass
        else:
            self.do_last_failed = False
        return is_ok

    def set_recommended_division_for_steps(self, time_step, actual_absolute_value, threshold_absolute_value) -> None:
        reccommended_division = int(np.ceil(actual_absolute_value / threshold_absolute_value))
        max_division = int(np.ceil(time_step/self.config.min_time_step))
        self.recommended_division_for_steps =max(min(reccommended_division, max_division), 2)


    def get_threshold_by_absolute(self) -> float:
        """Returns the absolute threshold value."""
        return float(self.config.max_absolute_value)

    def _get_value_by_extrapolated_quantile(self, extrapolated_quantile: float) -> float:
        IGNORED_EXTREMES = self.config.quantile_ignored_extremes
            # 2-1 it sweet spot (2 to 0.5)
        relative_diff = np.percentile(self._value_history, 100-IGNORED_EXTREMES, method="higher") \
            / np.percentile(self._value_history, IGNORED_EXTREMES, method="lower")
        value_mean = np.mean(self._value_history[:-2])
        value = value_mean * relative_diff * (self.config.max_quantile-0.5) # because mean is ~quantile 0.5
        return float(value)

    def get_threshold_by_quantile(self) -> float:
        """Returns the quantile-based threshold value. If quantile > 1 it returns a useful extrapolation"""
        if self.config.max_quantile <= 1.:
            value = np.quantile(self._value_history, self.config.max_quantile, method='higher')
        else: # self.config.max_quantile > 1.:
            value = self._get_value_by_extrapolated_quantile(self.config.max_quantile)
        #ic(value)
        return float(value)

    def get_threshold_by_deviation(self) -> float:
        """Returns the deviation-based threshold value."""
        return float(np.mean(self._value_history) + self.config.max_deviation * np.std(self._value_history))
    
    @deprecated("Better to use `max_quantile`>1. instead")
    def get_threshold_by_relative_log_diff(self) -> float:
        IGNORED_EXTREMES = 0.1 # in %
        log_diff = np.percentile(self._value_log_history, 100-IGNORED_EXTREMES, method="higher") \
            - np.percentile(self._value_log_history, IGNORED_EXTREMES, method="lower")
        log_mean = np.mean(self._value_log_history[:-2])
        log_value = log_mean + log_diff * (self.config.max_relative_log_diff-0.5) # because mean is ~quantile 0.5
        return float(np.exp(log_value))

    def get_worst_threshold_value(self) -> float:
        """Returns the worst threshold value. -1 if there is no calculation possible for the threshold, so it is ckecked coorrectly"""

        # Ordered by computational cost
        worst_threshold_value = -1.
        
        # Ordered by computational cost

        if self.config.max_absolute_value is not None \
            and self.config.max_absolute_value < np.inf:
            worst_threshold_value = max(worst_threshold_value, self.get_threshold_by_absolute())

        if self.config.max_quantile is not None \
            and self.config.max_quantile >= 0. \
            and len(self._value_history) >= 10: # Because quantile of less doesn't make sense
            worst_threshold_value = max(worst_threshold_value, self.get_threshold_by_quantile())
        
        if self.config.max_deviation is not None \
            and self.config.max_deviation > 0. \
            and len(self._value_history) >= 2: # Because deviation of less doesn't make sense
            worst_threshold_value = max(worst_threshold_value, self.get_threshold_by_deviation())
        
        return worst_threshold_value

    def check_adaptive_ok(self, time_step: float) -> bool:
        """Main class method to check if the time step is acceptable using all the different methods."""
        if not self.config.is_adaptive:
            return True
        
        worst_threshold_value = self.get_worst_threshold_value()
        #ic(worst_threshold_value)

        if worst_threshold_value == -1:
            return True
        else: 
            self.last_threshold_absolute_value = worst_threshold_value
            is_ok = self.check_adaptive_ok_by_threshold(worst_threshold_value, time_step)

        if time_step < self.config.min_time_step:
            #ic("min time step reached", self.last_threshold_absolute_value, self.get_value(time_step))
            return True
        return is_ok













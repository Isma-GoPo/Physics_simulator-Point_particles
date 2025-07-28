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
    """
    AdaptabilityManager is a class that manages the adaptability of time steps: Whether or not they should run and how much the should decrease.


    Class workings:
        - `check` methods returns True or False along doing some changes in property accordanly
        - `get` for only getting return value and not making changes
    """
    def __init__(self, 
                 get_value_function: Callable[[float], float],
                 adaptativility_config: ConfigAdapt = CONFIGURATION.simulation.adaptability,
                 ) -> None:
        """Init a 'AdaptabilityManager' object

        Possitional-Keyword arguments:
        - get_value_function: a function that when called return an absolute (positive) value which decrease proportionally with time_step
          It return the value that `AdaptabilityManager` study 
        - adaptive_config: Optional config instance that defines the adaptability parameters

        """            
        self.config: ConfigAdapt = adaptativility_config
        
        self.get_value: Callable[[float], float] = get_value_function # when called (no arguments) returns a value for storing it in history
            # very prouf of using a function in this way for not having to access the Particle object
        self._value_history: np.ndarray = np.empty((0), float)
        
        self._last_threshold_absolute_value: float = -1. # Only used when `do_last_failed` is false
        self.do_last_failed: bool = False
        self.recommended_division_for_steps:int = 2

    @property
    def last_threshold_absolute_value(self) -> float:
        if self.do_last_failed:
            return self._last_threshold_absolute_value
        else:
            raise AttributeError("You are not allowed to use last_threshold_absolute_value when the last check was ok")


    def store_value_in_history(self, time_step: float) -> None:
        """Store the defined value from `get_value` function in the history, for a given time_step."""
        if self.config.is_adaptive:
            self._value_history = np.append(self._value_history, self.get_value(time_step))
    
    # --- CHECK adaptive METHODS ---
    def is_adaptive_ok_by_threshold(self, threshold_absolute_value: float, time_step: float) -> bool:
        """Return wheteher the given threshold value makes the real value adaptative-ok (-1. means is ok)"""
        if threshold_absolute_value == -1:
            is_ok = True
        else:
            assert self.get_value(1.) != 0
            actual_absolute_value = self.get_value(time_step)
            is_ok = actual_absolute_value < threshold_absolute_value
        return is_ok
    
    def _set_last_checked_fail(self, threshold_absolute_value: float, time_step: float) -> None:
        actual_absolute_value = self.get_value(time_step)
        self.do_last_failed = True
        self._last_threshold_absolute_value = threshold_absolute_value
        self._set_recommended_division_for_steps(time_step, actual_absolute_value, threshold_absolute_value)

    def _set_last_checked_okay(self) -> None:
        self.do_last_failed = False

    
    def _set_recommended_division_for_steps(self, time_step, actual_absolute_value, threshold_absolute_value) -> None:
        reccommended_division = int(np.ceil(actual_absolute_value / threshold_absolute_value))
        max_division = int(np.ceil(time_step/self.config.min_time_step))
        self.recommended_division_for_steps =max(min(reccommended_division, max_division), 2)


    def get_threshold_by_absolute(self) -> float:
        """Returns the absolute threshold value."""
        return float(self.config.max_absolute_value)

    def _get_value_by_extrapolated_quantile(self, extrapolated_quantile: float) -> float:
        IGNORED_EXTREMES = self.config.quantile_ignored_extremes # In %
            # 2-1 it sweet spot (2 to 0.5)
        relative_diff = np.percentile(self._value_history, 100-IGNORED_EXTREMES, method="higher") \
            / np.percentile(self._value_history, IGNORED_EXTREMES, method="lower")
        relative_diff /= 1 - (2*IGNORED_EXTREMES/100)
        value_mean = np.mean(self._value_history[:-2])
        value = value_mean * relative_diff * (self.config.max_quantile-0.5) # because mean is ~quantile 0.5
        return float(value)

    def get_threshold_by_quantile(self) -> float:
        """Returns the quantile-based threshold value. If quantile > 1 it returns a useful extrapolation"""
        if self.config.max_quantile <= 1.:
            value = np.quantile(self._value_history, self.config.max_quantile, method='higher')
        else: # self.config.max_quantile > 1.:
            value = self._get_value_by_extrapolated_quantile(self.config.max_quantile)
        return float(value)

    def get_threshold_by_deviation(self) -> float:
        """Returns the deviation-based threshold value."""
        return float(np.mean(self._value_history) + self.config.max_deviation * np.std(self._value_history))

    def get_worst_threshold_value(self) -> float:
        """Returns the worst threshold value. -1 if there is no calculation possible for the threshold, so it is ckecked coorrectly"""
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
        """Main class method to check if the time step is acceptable using all the different methods.
        Returns whether the step could run or not (decrease time step if not by `self.recommended_division_for_steps`)
        Saves the results of the ckeck and worst_threshold value
        """
        if not self.config.is_adaptive:
            return True
        
        worst_threshold_value = self.get_worst_threshold_value()

        if self.get_value(time_step) == 0:
            print("WARNING: You are checking adaptability before applying forces or not having forces to apply")
            #raise Exception("You are checking adaptability before applying forces or not having forces to apply")

        is_ok = self.is_adaptive_ok_by_threshold(worst_threshold_value, time_step)
        
        if not is_ok:
            self._set_last_checked_fail(worst_threshold_value, time_step)
        else:
            self._set_last_checked_okay()

        if time_step < self.config.min_time_step:
            ic("min time step reached", self._last_threshold_absolute_value, self.get_value(time_step))
            ic.disable()
            return True
        
        return is_ok
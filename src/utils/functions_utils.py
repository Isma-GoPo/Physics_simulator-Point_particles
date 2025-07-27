"""This module introduces the neccesary functions for 

Functions:
limit_force_module: Decorator
: Decorator
"""
import numpy as np
from functools import wraps
from typing import Callable, Any, ParamSpec
P = ParamSpec('P')  # For type hinting *args, **kwargs

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from settings import CONFIGURATION

# Decorators
def limit_force_module(force_func: Callable[P, np.ndarray], max_force_module: float | np.ndarray = CONFIGURATION.simulation.max_allowed_force) -> Callable[P, np.ndarray]: # type: ignore
    @wraps(force_func) # Copy attributes (e.g. `__doc__`) from the wrapped function (debbuging)
    def wrapper_function(*args, **kwargs):
        return_force = force_func(*args, **kwargs)
        return_force_module = np.linalg.norm(return_force)
        return return_force if return_force_module <= max_force_module else max_force_module * return_force/return_force_module
    return wrapper_function

def print_run_time(func: Callable[P, Any]) -> Callable[P, Any]:
    @wraps(func)
    def wrapper_function(*args, **kwargs):
        import time
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.6f} seconds to run.")
        return result
    return wrapper_function

def run_if_condition(condition: Callable[..., bool]) -> Callable[..., Callable[..., Any | None]]:
    """Returns a decorator that runs it wrapped function if the condition is met"""
    def run_if_condition_decorator(adaptative_dependant_function: Callable[..., Any]) -> Callable[..., Any | None]:
        """Diseable the taged function if the particle is in an adaptive state."""
        @wraps(adaptative_dependant_function)
        def wrapper_function(self, *args, **kwargs) -> Any | None:
            if condition(self):
                return adaptative_dependant_function(self, *args, **kwargs)
            #else:
                #ic(condition, condition(self))
        return wrapper_function
    return run_if_condition_decorator
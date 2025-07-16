"""This module introduces the constants for the program

Constants:
TIME_STEP: [s] (float) How much it "tick" advance the time in the simulation
SIMULATION_TIME: [s] (float) How much the simulation last
NUMBER_OF_TIME_STEPS: [int] number time steps will be done in the simulation
"""
import numpy as np
import math
from icecream import ic

# My modules
from settings import SETTINGS

# --- SIMULATION PHYSICS CONSTANTS ---
MAX_FORCE_MODULE: float | np.float64 = np.float64( SETTINGS["simulation"]["max_allowed_force"] )
    # Maximum force module (norm) that can be applied to a particle (in [N]) `np.inf` means no limit

# --- SIMULATION TIME CONSTANTS ---
TIME_STEP: float | np.float64 = np.float64( SETTINGS["simulation"]["time_step"] )
    # How much it "tick" advance the time in the simulation (in [s])
    # 0.001 slow but really accurate
SIMULATION_TIME: float | np.float64 = np.float64( SETTINGS["simulation"]["simulation_time"] )
    # How much the simulation last (in [s])
NUMBER_OF_TIME_STEPS: int = int(SIMULATION_TIME / TIME_STEP)  
if NUMBER_OF_TIME_STEPS > 100_000: raise Exception("Too many time steps could crash")
    # How many time steps will be done in the simulation

# --- PLOTTING CONSTANTS ---
PLOTTING_TIME: float | np.float64 = np.float64( SETTINGS["plotting"]["plotting_time"] )
    # How much the plotting of the simulation last (in [s])

#X_Y_Z_FRAME_LIMIT = np.array([1, 1, 1], dtype=float)
PLOTTING_STEPS_PER_SECOND: int = int(SETTINGS["plotting"]["refresh_rate"])
    # Recommended to make it so it plots 30 step every second
NUMBER_OF_PLOTTING_STEPS: int = int(PLOTTING_TIME * PLOTTING_STEPS_PER_SECOND)  
    # How many plotting steps will be done in the simulation
PLOTTING_RELATIVE_TIME_STEP: int = int(math.ceil(NUMBER_OF_TIME_STEPS / (PLOTTING_TIME * PLOTTING_STEPS_PER_SECOND))) 
    # How much time steps get merged in a plotting step (in [ratio])
    # This is for fluency/performance reasons, so the plotting is not too slow.

DO_REPEAT_PLOTTING: bool = bool( SETTINGS["plotting"]["do_repeat"] )
    # If True, the plotting will repeat the last frame when it ends


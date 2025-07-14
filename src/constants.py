"""This module introduces the constants for the program

Constants:
TIME_STEP: [s] (float) How much it "tick" advance the time in the simulation
SIMULATION_TIME: [s] (float) How much the simulation last
NUMBER_OF_TIME_STEPS: [int] number time steps will be done in the simulation
X_Y_Z_FRAME_LIMIT: [m] (ndarray) The positive distance in the 3D space on wich the particles can be. Negative distant will be symetric
"""
import numpy as np
import math

# --- SIMULATION PHYSICS CONSTANTS ---
MAX_FORCE_MODULE: float | np.ndarray = 10#np.inf  # Maximum force module (norm) that can be applied to a particle (in [N]) `np.inf` means no limit

# --- SIMULATION TIME CONSTANTS ---
TIME_STEP: float = 0.01  # How much it "tick" advance the time in the simulation (in [s])
SIMULATION_TIME: float = 40.0  # How much the simulation last (in [s])
NUMBER_OF_TIME_STEPS: int = int(SIMULATION_TIME / TIME_STEP)  # How many time steps will be done in the simulation

# --- PLOTTING CONSTANTS ---
PLOTTING_TIME: float = 10.0  # How much the plotting of the simulation last (in [s])
#X_Y_Z_FRAME_LIMIT = np.array([1, 1, 1], dtype=float)
PLOTTING_STEPS_PER_SECOND: int = 20  # Recommended to make it so it plots 30 step every second
NUMBER_OF_PLOTTING_STEPS: int = int(PLOTTING_TIME * PLOTTING_STEPS_PER_SECOND)  # How many plotting steps will be done in the simulation
PLOTTING_RELATIVE_TIME_STEP: int = int(math.ceil(NUMBER_OF_TIME_STEPS / (PLOTTING_TIME * PLOTTING_STEPS_PER_SECOND))) # How much time steps get merged in a plotting step (in [ratio])
print(f"{PLOTTING_RELATIVE_TIME_STEP=}")
# This is for fluency/performance reasons, so the plotting is not too slow. 

DO_REPEAT_PLOTTING: bool = True  # If True, the plotting will repeat the last frame when it ends


"""This module introduces the constants for the program

Constants:
TIME_STEP: [s] (float) How much it "tick" advance the time in the simulation
SIMULATION_TIME: [s] (float) How much the simulation last
NUMBER_OF_TIME_STEPS: [int] number time steps will be done in the simulation
X_Y_Z_FRAME_LIMIT: [m] (ndarray) The positive distance in the 3D space on wich the particles can be. Negative distant will be symetric
"""
import numpy as np

TIME_STEP: float = 0.1  # How much it "tick" advance the time in the simulation (in [s])
SIMULATION_TIME: float = 10.0  # How much the simulation last (in [s])
NUMBER_OF_TIME_STEPS: int = int(SIMULATION_TIME / TIME_STEP)  # How many time steps will be done in the simulation

#X_Y_Z_FRAME_LIMIT = np.array([1, 1, 1], dtype=float)

MAX_FORCE_MODULE: float = np.inf  # Maximum force module (norm) that can be applied to a particle (in [N])
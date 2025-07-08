"""This module introduces the neccesary functions for printing an animation of the simulation

Functions:
print_simulation_animation: Open a window to show the simulation animation of the particles.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from constants import *


def print_simulation_animation(particles_positions: np.ndarray) -> None:
    """Open a window to show the simulation animation of the particles.
    
    Arguments:
    particles_positions: [m] numpy array of shape n×3 being n the number of time steps and 3 x, y, z coordinates.
    """
    t = np.linspace(0, SIMULATION_TIME, NUMBER_OF_TIME_STEPS+1)

    x = particles_positions[:,0]
    y = particles_positions[:,2]

    fig, axis = plt.subplots()
    axis.plot(x, y)

    # axis.set_xlim(-X_Y_Z_FRAME_LIMIT[0], X_Y_Z_FRAME_LIMIT[0])
    # axis.set_ylim(-X_Y_Z_FRAME_LIMIT[2], X_Y_Z_FRAME_LIMIT[2])
    # axis.set_xlabel('X Position [m]')
    # axis.set_ylabel('Z Position [m]')

    plt.show()

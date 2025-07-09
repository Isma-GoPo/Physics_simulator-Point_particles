"""This module introduces the neccesary functions for printing an animation of the simulation

Functions:
print_simulation_static: Open a window to show a static plot of the position of one particle.
print_simulation_animated: Open a window to show the simulation animation of multiple particles.
print_simulation_animated_one_particle: Open a window to show the simulation animation of a single particle.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.lines import Line2D # For type hinting in the update function

from constants import *
import utils


t = np.linspace(0, SIMULATION_TIME, NUMBER_OF_TIME_STEPS)

def print_simulation_animated(*particle_positions: np.ndarray) -> None:
    """Open a window to show the simulation animation of multiple particles.
    
    Arguments:
    *particle_positions: [m] Variable number of numpy arrays of shape m×n×3 being n: number of time steps; and 3: x, y, z coordinates.
    """
    t = np.linspace(0, SIMULATION_TIME, NUMBER_OF_TIME_STEPS+1)

    particles_positions = utils.stack_positions(*particle_positions) # ndarray of shape n×m×3 being n: number of time steps; m: number of particles; and 3: x, y, z coordinates.

    x = particles_positions[:,:,0]
    y = particles_positions[:,:,2]

    fig, axis = plt.subplots()
    axis.set_xlim(np.min(x), np.max(x))
    axis.set_ylim(np.min(y), np.max(y))

    # Initialize the line as empty so the display is empty at the start
    line, = axis.plot([], [], "o") # "o" for points ("-" for lines)

    def update_plot_data(frame: int) -> tuple[Line2D]:
        line.set_data(x[frame], y[frame])
        return line, # "," because it expects a tuple

    animation = FuncAnimation(fig=plt.gcf(), 
                              func=update_plot_data, 
                              frames = NUMBER_OF_TIME_STEPS, 
                              #repeat=False,
                              interval=TIME_STEP*1000
                              )

    plt.show()


def print_simulation_static(particle_positions: np.ndarray) -> None:
    """Open a window to show the simulation animation of the particles.
    
    Arguments:
    particle_positions: [m] numpy array of shape n×3 being n the number of time steps and 3 x, y, z coordinates.
    """

    x = particle_positions[:,0]
    y = particle_positions[:,2]

    fig, axis = plt.subplots()
    axis.plot(x, y)

    # axis.set_xlim(-X_Y_Z_FRAME_LIMIT[0], X_Y_Z_FRAME_LIMIT[0])
    # axis.set_ylim(-X_Y_Z_FRAME_LIMIT[2], X_Y_Z_FRAME_LIMIT[2])
    # axis.set_xlabel('X Position [m]')
    # axis.set_ylabel('Z Position [m]')

    plt.show()


def print_simulation_animated_one_particle(particle_positions: np.ndarray) -> None:
    """Open a window to show the simulation animation of a single particle.

    Arguments:
    particle_positions: [m] numpy array of shape n×3 being n the number of time steps and 3 x, y, z coordinates.
    """
    t = np.linspace(0, SIMULATION_TIME, NUMBER_OF_TIME_STEPS)

    x = particle_positions[:,0]
    y = particle_positions[:,2]

    fig, axis = plt.subplots()
    axis.set_xlim(np.min(x), np.max(x))
    axis.set_ylim(np.min(y), np.max(y))

    # Initialize the line as empty so the display is empty at the start
    line, = axis.plot([], [], "o") # "o" for points ("-" for lines)

    def update_plot_data(frame: int) -> tuple[Line2D]:
        start = max(0, frame-1)
        line.set_data(x[start:frame], y[start:frame])
        return line, # "," because it expects a tuple

    animation = FuncAnimation(fig=plt.gcf(), 
                              func=update_plot_data, 
                              frames = NUMBER_OF_TIME_STEPS, 
                              #repeat=False,
                              interval=TIME_STEP*1000
                              )

    plt.show()

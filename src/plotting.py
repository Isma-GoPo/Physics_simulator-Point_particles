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
from physics import ParticleSpace
# ---

t = np.linspace(0, SIMULATION_TIME, NUMBER_OF_TIME_STEPS)


def print_animated_poistion_by_array(stacked_particle_positions_array: np.ndarray) -> None:
    """Open a window to show the simulation animation of multiple particles.
    
    Arguments:
    *particle_positions: [m] numpy array of shape n×m×3 being n: number of time steps; m: number of particles; and 3: x, y, z coordinates.
    """
    x = stacked_particle_positions_array[:,:,0]
    y = stacked_particle_positions_array[:,:,2]
    number_of_frames = stacked_particle_positions_array.shape[0]

    fig, axis = plt.subplots()
    axis.set_xlim(np.min(x), np.max(x))
    axis.set_ylim(np.min(y), np.max(y))

    # erase the axis limit
    #axis.set_xlim(-1, 1)
    #axis.set_ylim(-1, 1)

    # Initialize the line as empty so the display is empty at the start
    line, = axis.plot([], [], "o") # "o" for points ("-" for lines)

    def update_plot_data(frame: int) -> tuple[Line2D]:
        line.set_data(x[frame], y[frame])
        return (line,)

    animation = FuncAnimation(fig=plt.gcf(), 
                              func=update_plot_data, 
                              frames = number_of_frames, 
                              repeat=DO_REPEAT_PLOTTING,
                              interval=1/PLOTTING_STEPS_PER_SECOND*1000
                              )

    plt.show()


def print_animated_simulation_by_space(particle_space: ParticleSpace) -> None:
    """Open a window to show the simulation animation of multiple particles.
    
    Arguments:
    particle_space: [ParticleSpace] space that contains the simulated particles
    """
    position_history_array = particle_space.reduced_position_history_array(PLOTTING_RELATIVE_TIME_STEP)
    stacked_position_history_array = utils.arrays_utils.stack_positions(*position_history_array)

    print_animated_poistion_by_array(stacked_position_history_array)


# def print_simulation_static(particle_positions: np.ndarray) -> None:
#     """Open a window to show the simulation animation of the particles.
#     
#     Arguments:
#     particle_positions: [m] numpy array of shape n×3 being n the number of time steps and 3 x, y, z coordinates.
#     """
# 
#     x = particle_positions[:,0]
#     y = particle_positions[:,2]
# 
#     fig, axis = plt.subplots()
#     axis.plot(x, y)
# 
#     # axis.set_xlim(-X_Y_Z_FRAME_LIMIT[0], X_Y_Z_FRAME_LIMIT[0])
#     # axis.set_ylim(-X_Y_Z_FRAME_LIMIT[2], X_Y_Z_FRAME_LIMIT[2])
#     # axis.set_xlabel('X Position [m]')
#     # axis.set_ylabel('Z Position [m]')
# 
#     plt.show()
# 
# 
# def print_simulation_animated_one_particle(particle_positions: np.ndarray) -> None:
#     """Open a window to show the simulation animation of a single particle.
# 
#     Arguments:
#     particle_positions: [m] numpy array of shape n×3 being n the number of time steps and 3 x, y, z coordinates.
#     """
#     t = np.linspace(0, SIMULATION_TIME, NUMBER_OF_TIME_STEPS)
# 
#     x = particle_positions[:,0]
#     y = particle_positions[:,2]
# 
#     fig, axis = plt.subplots()
#     axis.set_xlim(np.min(x), np.max(x))
#     axis.set_ylim(np.min(y), np.max(y))
# 
#     # Initialize the line as empty so the display is empty at the start
#     line, = axis.plot([], [], "o") # "o" for points ("-" for lines)
# 
#     def update_plot_data(frame: int) -> tuple[Line2D]:
#         start = max(0, frame-1)
#         line.set_data(x[start:frame], y[start:frame])
#         return line, # "," because it expects a tuple
# 
#     animation = FuncAnimation(fig=plt.gcf(), 
#                               func=update_plot_data, 
#                               frames = NUMBER_OF_TIME_STEPS, 
#                               #repeat=False,
#                               interval=TIME_STEP*1000
#                               )
# 
#     plt.show()

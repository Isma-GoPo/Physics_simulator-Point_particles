import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.lines import Line2D # For type hinting in the update function
import matplotlib.colors as mcolors
import itertools
from icecream import ic

# My modules

import constants
import utils
from physics import ParticleSpace
from settings import CONFIGURATION
from plotting.dot import PlottingDot

# ---


def print_animated_simulation_by_space(particle_space: ParticleSpace) -> None:
    """Open a window to show the simulation animation of multiple particles.
    
    Arguments:
    particle_space: [ParticleSpace] space that contains the simulated particles
    """
    position_history_array = particle_space.get_reduced_position_history_array(CONFIGURATION.plotting.plotting_relative_time_step(CONFIGURATION.simulation.number_of_time_steps))  # constants.PLOTTING_RELATIVE_TIME_STEP
    stacked_position_history_array = utils.arrays_utils.stack_positions(*position_history_array)

    rotation_array = np.array(CONFIGURATION.plotting.rotation)*np.pi/180
    rotation_matrix = utils.arrays_utils.rotation_matrix_sequenced(*rotation_array, sequence=CONFIGURATION.plotting.rotation_sequence)
    ic(rotation_matrix)
    
    rotated_stacked_position_history_array = stacked_position_history_array @ rotation_matrix.T # Same as rotation_matrix @ array only taking its last axis
    
    x = rotated_stacked_position_history_array[:,:,0]
    y = rotated_stacked_position_history_array[:,:,1]

    number_of_frames = stacked_position_history_array.shape[0]
    number_of_particles = len(particle_space)

    fig, axis = plt.subplots()
    axis.set_xlim(np.min(x), np.max(x))
    axis.set_ylim(np.min(y), np.max(y))

    colours_list = PlottingDot.get_colours_list(number_of_particles)
    size_list = PlottingDot.get_plotting_size_list_from_masses(particle_space.get_particle_property_list("mass"))


    # Initialize the scatter plot. Using scatter is better for individual point properties.
    scatter = axis.scatter(x[0], y[0], 
                           c=colours_list, 
                           s=size_list) # s for size. 25 is roughly markersize=5

    def update_plot_data(frame: int):
        """Updates the data of the scatter plot for each animation frame."""
        offsets = np.c_[x[frame], y[frame]]
        scatter.set_offsets(offsets)
        return (scatter,)

    animation = FuncAnimation(fig=plt.gcf(), 
                              func=update_plot_data, 
                              frames = number_of_frames, 
                              repeat=CONFIGURATION.plotting.do_repeat, #type: ignore #constants.DO_REPEAT_PLOTTING,
                              interval=1/CONFIGURATION.plotting.refresh_rate*1000, #type: ignore  #constants.PLOTTING_STEPS_PER_SECOND*1000,
                              blit=True
                              )

    plt.show()



# --- deprecated functions ---
# def print_animated_poistion_by_array(stacked_particle_positions_array: np.ndarray) -> None:
#     """Open a window to show the simulation animation of multiple particles.
#     
#     Arguments:
#     *particle_positions: [m] numpy array of shape n×m×3 being n: number of time steps; m: number of particles; and 3: x, y, z coordinates.
#     """
#     x = stacked_particle_positions_array[:,:,0]
#     y = stacked_particle_positions_array[:,:,2]
#     number_of_frames = stacked_particle_positions_array.shape[0]
#
#     fig, axis = plt.subplots()
#     axis.set_xlim(np.min(x), np.max(x))
#     axis.set_ylim(np.min(y), np.max(y))
#
#     # erase the axis limit
#     #axis.set_xlim(-1, 1)
#     #axis.set_ylim(-1, 1)
#
#     # Initialize the line as empty so the display is empty at the start
#     line, = axis.plot([], [], "o") # "o" for points ("-" for lines)
#
#     def update_plot_data(frame: int) -> tuple[Line2D]:
#         line.set_data(x[frame], y[frame])
#         return (line,)
#
#     animation = FuncAnimation(fig=plt.gcf(), 
#                               func=update_plot_data, 
#                               frames = number_of_frames, 
#                               repeat=DO_REPEAT_PLOTTING,
#                               interval=1/PLOTTING_STEPS_PER_SECOND*1000
#                               )
#
#     plt.show()
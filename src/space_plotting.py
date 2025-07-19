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
# ---

#t = np.linspace(0, SIMULATION_TIME, NUMBER_OF_TIME_STEPS)

def get_colours_list(len: int) -> list[str]:
    colours = mcolors.TABLEAU_COLORS
    colours_list = list(itertools.islice(itertools.cycle(colours), len))
    return colours_list

def get_dot_size_list(particle_space) -> list[float]:
    sizes = np.array([particle.plotting.size for particle in particle_space])
    exp = constants.PLOTTING_SIZE_EXPONENT_FACTOR
    geometric_size = relativise_size(sizes)**exp * constants.PLOTTING_SIZE_DIFFERENCE**(1-exp) # Make something similar to the geometric mean (because area != proprotional mass)
    return list(geometric_size*constants.PLOTTING_SIZE_PER_DIFFERENCE+constants.PLOTTING_SIZE_MIN)

def relativise_size(sizes: np.ndarray) -> np.ndarray:
    default_difference = constants.PLOTTING_SIZE_DIFFERENCE
    max = np.max(sizes)
    min = np.min(sizes)
    difference = max - min
    if difference <= default_difference:
        return sizes-min
    else:
        relative = lambda size: (size-min)*default_difference/difference
        return np.vectorize(relative)(sizes)  # like map()


def print_animated_simulation_by_space(particle_space: ParticleSpace) -> None:
    """Open a window to show the simulation animation of multiple particles.
    
    Arguments:
    particle_space: [ParticleSpace] space that contains the simulated particles
    """
    position_history_array = particle_space.reduced_position_history_array(constants.PLOTTING_RELATIVE_TIME_STEP)
    stacked_position_history_array = utils.arrays_utils.stack_positions(*position_history_array)

    x = stacked_position_history_array[:,:,0]
    y = stacked_position_history_array[:,:,2]
    number_of_frames = stacked_position_history_array.shape[0]
    number_of_particles = len(particle_space)

    fig, axis = plt.subplots()
    axis.set_xlim(np.min(x), np.max(x))
    axis.set_ylim(np.min(y), np.max(y))

    colours_list = get_colours_list(number_of_particles)
    size_list = get_dot_size_list(particle_space)


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
                              repeat=constants.DO_REPEAT_PLOTTING,
                              interval=1/constants.PLOTTING_STEPS_PER_SECOND*1000,
                              blit=True
                              )

    plt.show()
# General modules
import numpy as np
from icecream import ic
import os
# clear terminal
os.system('cls')

# My modules
from constants import *
import utils
from time import perf_counter
import physics
#from plotting import print_animated_poistion_by_array, print_animated_simulation_by_space
from space_plotting import print_animated_simulation_by_space, get_dot_size_list


# Running the file
if __name__=="__main__":
    #space = utils.init_space.circular_motion_decelerating_particle()
    space = utils.init_space.solar_system()
    space.adaptative_max_velocity_diff = 200

    space.run_simulation(NUMBER_OF_TIME_STEPS, TIME_STEP)

    #ic(space.get_particle_property_array("velocity"))
    
    print_animated_simulation_by_space(space)
# General modules
import numpy as np
from icecream import ic
import os
# clear terminal
os.system('cls')

# My modules
#from functions import *
from constants import *
import utils
from time import perf_counter
import physics
from plotting import print_animated_poistion_by_array, print_animated_simulation_by_space


# Running the file
if __name__=="__main__":
    ic(SETTINGS)
    #space = utils.init_space.orbiting_decelerating_particles()
    space = utils.init_space.circular_motion_decelerating_particle()

    space.run_simulation(NUMBER_OF_TIME_STEPS, TIME_STEP)
    
    print_animated_simulation_by_space(space)
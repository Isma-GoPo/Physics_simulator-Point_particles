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
from space_plotting import print_animated_simulation_by_space
from settings import CONFIGURATION
from constants import USER_SETTING_DICT

CONFIGURATION.update(USER_SETTING_DICT)


# Running the file
if __name__=="__main__":
    #space = utils.init_space.circular_motion_decelerating_particle()
    #space, custom_settings  = utils.init_space.orbiting_decelerating_particles()
    space, custom_settings  = utils.init_space.two_particles_from_repose()
    CONFIGURATION.update(custom_settings)
    
    space.update_simulation_properties_from_configuration(CONFIGURATION.copy)


    if CONFIGURATION.simulation.could_crass:    
        raise Exception("Too many time steps could crash")
    
    space.run_simulation(CONFIGURATION.simulation.number_of_time_steps, CONFIGURATION.simulation.time_step)  
    
    print(CONFIGURATION)
    print_animated_simulation_by_space(space) 
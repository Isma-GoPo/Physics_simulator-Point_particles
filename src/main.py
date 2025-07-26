# General modules
import numpy as np
from icecream import ic
import os
from pprint import pprint

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


ic(CONFIGURATION)
CONFIGURATION.update(USER_SETTING_DICT)
#ic(CONFIGURATION)

ic.disable()


def main():
    #space = utils.init_space.circular_motion_decelerating_particle()
    space, custom_settings  = utils.init_space.orbiting_decelerating_particles()
    #space, custom_settings  = utils.init_space.two_particles_from_repose()
    CONFIGURATION.update(custom_settings)
    
    #CONFIGURATION.simulation.update(
    #    {"simulation_time": 192426,
    #    "time_step": 10 }) #96213*2

    space.config = CONFIGURATION.simulation

    #ic(CONFIGURATION)
    pprint(CONFIGURATION.simulation.as_dictionary)
    
    pprint(space[0].adaptaptability.config.as_dictionary)
    pprint(space[1].adaptaptability.config.as_dictionary)
    

    space.run_simulation(CONFIGURATION.simulation.number_of_time_steps, CONFIGURATION.simulation.time_step)  
    
    print(CONFIGURATION)
    print_animated_simulation_by_space(space) 
    

# Running the file
if __name__=="__main__":
    main()
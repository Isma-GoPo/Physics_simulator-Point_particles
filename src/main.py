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

#ic.disable()


def main():
    #init_space = utils.init_space.orbiting_decelerating_particles
    init_space = utils.init_space.solar_system
    #init_space = utils.init_space.two_particles_from_repose

    space, custom_settings  = init_space()

    CONFIGURATION.update(custom_settings)
    
    new_sim_settings = {
        #"simulation_time": 384852,
        #"time_step": 100.,
        "adaptability": {
            "is_adaptive": True,
            "max_absolute_value": np.inf,
        },
    }

    CONFIGURATION.simulation.update(new_sim_settings)

    space.config = CONFIGURATION.simulation

    #ic(CONFIGURATION)
    pprint(CONFIGURATION.simulation.as_dictionary)
    

    space.run_simulation()  
    
    print(CONFIGURATION)
    print_animated_simulation_by_space(space) 

    #ic(space.position_history_array)
    #ic(space[0].adaptability._value_history)
    

# Running the file
if __name__=="__main__":
    main()
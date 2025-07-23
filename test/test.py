# General modules
import numpy as np
from icecream import ic
from typing import Callable, Any
import os
# clear terminal
os.system('cls')

# My modules
import sys; sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from constants import *
import utils
#from time import perf_counter
import physics
#from plotting import print_animated_poistion_by_array, print_animated_simulation_by_space
from space_plotting import print_animated_simulation_by_space

"""# Running the file
if __name__=="__main__":
    #space = utils.init_space.circular_motion_decelerating_particle()
    space = utils.init_space.solar_system()

    space.run_simulation(NUMBER_OF_TIME_STEPS, TIME_STEP)

    acceleration_vector = space.get_particle_property_array("last_acceleration")
    acceleration_module = np.linalg.norm(acceleration_vector, axis=1)
    ic(acceleration_vector)
    ic(acceleration_module)
    ic(acceleration_module<2.)
    
    print_animated_simulation_by_space(space)"""
    
    
    
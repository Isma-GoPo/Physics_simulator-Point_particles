# General modules
import numpy as np
from icecream import ic

# My modules
#from functions import *
from constants import *
import utils
import physics
from plotting import print_simulation_animated

# Running the file
if __name__=="__main__":
    #space = utils.init_space.orbiting_decelerating_particles()
    space = utils.init_space.circular_motion_particle()
    print(space)
    #print(repr(space))

    space.run_simulation(NUMBER_OF_TIME_STEPS, TIME_STEP) 